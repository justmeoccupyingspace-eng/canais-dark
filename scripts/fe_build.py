"""Monta áudio e linha do tempo de um vídeo de oração / história bíblica.
Uso: python scripts/fe_build.py specs/fe/<id>.json out/
Gera: out/fe.json (props do Remotion), out/audio.wav (voz + trilha), out/yt.json (metadados), out/gates.json.
Voz: edge-tts por frase (duração exata de cada frase → legenda sincronizada). Trilha: incompetech (CC BY 4.0)."""
import asyncio, json, os, subprocess, sys, urllib.parse, urllib.request

spec = json.load(open(sys.argv[1], encoding="utf-8"))
OUT = sys.argv[2]
os.makedirs(OUT + "/v", exist_ok=True)
SR = 48000
UA = {"User-Agent": "canais-dark-bot/1.0 (+https://github.com/justmeoccupyingspace-eng/canais-dark)"}


def sh(*a):
    subprocess.run(a, check=True)


def dur(f):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).decode().strip())


async def tts_all(lines):
    import edge_tts
    for i, ln in enumerate(lines):
        f = f"{OUT}/v/{i:03d}.mp3"
        for k in range(4):
            try:
                await edge_tts.Communicate(ln["text"], spec["voice"], rate=spec.get("rate", "-6%"), pitch=spec.get("pitch", "+0Hz")).save(f)
                if os.path.getsize(f) > 2000:
                    break
            except Exception as e:
                print("tts tentativa", k, i, repr(e)[:200])
                await asyncio.sleep(3 + 5 * k)
        else:
            raise SystemExit(f"::error title=tts::frase {i} sem áudio")


lines = spec["lines"]
asyncio.run(tts_all(lines))

# linha do tempo
FPS = 30
t = float(spec.get("intro", 3.6 if spec.get("title") else 0.8))
parts, tl = [], []
for i, ln in enumerate(lines):
    f = f"{OUT}/v/{i:03d}.mp3"
    d = dur(f)
    tl.append({"text": ln.get("show", ln["text"]), "t0": round(t, 3), "t1": round(t + d, 3), **({"ref": ln["ref"]} if ln.get("ref") else {})})
    parts.append((f, t))
    t += d + float(ln.get("pause", spec.get("pause", 0.7)))
outro_at = t + 0.4
total = outro_at + (4.5 if spec.get("outro") else 1.0)

# voz numa faixa só
inputs, filt = [], []
for k, (f, at) in enumerate(parts):
    inputs += ["-i", f]
    filt.append(f"[{k}:a]aresample={SR},adelay={int(at * 1000)}|{int(at * 1000)}[a{k}]")
mix = "".join(f"[a{k}]" for k in range(len(parts)))
# amix em blocos de 64 entradas para não estourar o filtro
voice = f"{OUT}/voice.wav"
if len(parts) <= 64:
    sh("ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filt) + f";{mix}amix=inputs={len(parts)}:normalize=0,apad=whole_dur={total:.2f}[o]", "-map", "[o]", "-ac", "1", "-ar", str(SR), voice)
else:
    blocks = []
    for b in range(0, len(parts), 60):
        sub = parts[b:b + 60]
        ins, ff = [], []
        for k, (f, at) in enumerate(sub):
            ins += ["-i", f]
            ff.append(f"[{k}:a]aresample={SR},adelay={int(at * 1000)}|{int(at * 1000)}[a{k}]")
        bf = f"{OUT}/vb{b}.wav"
        sh("ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(ff) + ";" + "".join(f"[a{k}]" for k in range(len(sub))) + f"amix=inputs={len(sub)}:normalize=0,apad=whole_dur={total:.2f}[o]", "-map", "[o]", "-ac", "1", "-ar", str(SR), bf)
        blocks.append(bf)
    ins = sum([["-i", b] for b in blocks], [])
    sh("ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", "".join(f"[{k}:a]" for k in range(len(blocks))) + f"amix=inputs={len(blocks)}:normalize=0[o]", "-map", "[o]", "-ac", "1", "-ar", str(SR), voice)

# trilha (com alternativas se a primeira não baixar)
music = None
for tr in [spec.get("music", {}).get("track")] + spec.get("music", {}).get("alt", []) + ["Meditation Impromptu 02", "Dreamer", "Healing"]:
    if not tr:
        continue
    try:
        url = "https://incompetech.com/music/royalty-free/mp3-royaltyfree/" + urllib.parse.quote(tr) + ".mp3"
        open(f"{OUT}/m.mp3", "wb").write(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read())
        if os.path.getsize(f"{OUT}/m.mp3") > 100000:
            music = tr
            break
    except Exception as e:
        print("trilha falhou", tr, repr(e)[:120])
vol = spec.get("music", {}).get("vol", 0.16)
if music:
    sh("ffmpeg", "-v", "error", "-y", "-i", voice, "-stream_loop", "-1", "-i", f"{OUT}/m.mp3",
       "-filter_complex", f"[1:a]aresample={SR},volume={vol},afade=t=in:d=2,afade=t=out:st={max(0, total - 3):.2f}:d=3[m];[0:a][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=11[o]",
       "-map", "[o]", "-ar", str(SR), "-ac", "2", f"{OUT}/audio.wav")
else:
    sh("ffmpeg", "-v", "error", "-y", "-i", voice, "-af", "loudnorm=I=-15:TP=-1.5:LRA=11", "-ar", str(SR), "-ac", "2", f"{OUT}/audio.wav")

vert = spec.get("format") == "short"
fe = {k: spec.get(k) for k in ("scene", "seed", "img", "kicker", "title", "subtitle", "outro", "outro2", "cross", "thumb") if spec.get(k) is not None}
fe.update({"w": 1080 if vert else 1920, "h": 1920 if vert else 1080, "total": round(total, 2), "lines": tl, "outro_at": round(outro_at, 2), "title_end": round(min(tl[0]["t0"], 3.6) if tl else 3.0, 2)})
json.dump(fe, open(f"{OUT}/fe.json", "w"), ensure_ascii=False)

yt = dict(spec["yt"])
cred = f"\n\nMúsica: \"{music}\" — Kevin MacLeod (incompetech.com), licencia CC BY 4.0." if (music and spec.get("lang") == "es") else (f"\n\nMusic: \"{music}\" by Kevin MacLeod (incompetech.com), licensed under CC BY 4.0." if music else "")
yt["description"] = yt.get("description", "").replace("{music}", cred.strip()) if "{music}" in yt.get("description", "") else yt.get("description", "") + cred
json.dump({"yt": yt, "publish": spec.get("publish", {})}, open(f"{OUT}/yt.json", "w"), ensure_ascii=False)

words = sum(len(l["text"].split()) for l in lines)
speech = sum(x["t1"] - x["t0"] for x in tl)
g = {"total_s": round(total, 1), "words": words, "wpm": round(words / max(1, speech) * 60), "music": music, "lines": len(tl)}
json.dump(g, open(f"{OUT}/gates.json", "w"))
print("ok", g)

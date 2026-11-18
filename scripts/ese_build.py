"""Monta voz, tempos e trilha de um "E se...?" (canal B, PT-BR).
Uso: python scripts/ese_build.py specs/ese/<id>.json out/<id>/
Voz: Gemini TTS (blocos de até ~170 palavras; cai para Edge se a cota acabar) → Whisper (pt) palavra a palavra → cada beat começa
quando a 1ª palavra dele é dita; legenda palavra a palavra. Trilha incompetech (CC BY 4.0) baixa por baixo.
Saídas: es.json (props do Remotion), audio.wav, yt.json, gates.json"""
import json, os, re, subprocess, sys, unicodedata, urllib.parse, urllib.request
import numpy as np
import soundfile as sf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ltts  # gemini(), edge(), tighten(), clean(), SR

spec = json.load(open(sys.argv[1], encoding="utf-8"))
OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
SR = ltts.SR
UA = {"User-Agent": "canais-dark-bot/1.0 (+https://github.com/justmeoccupyingspace-eng/canais-dark)"}
beats = spec["beats"]

# ---- blocos de fala (quebra só entre beats) ----
blocks, cur, n = [], [], 0
for i, b in enumerate(beats):
    w = len(b["say"].split())
    if cur and n + w > int(spec.get("block", 230)):
        blocks.append(cur); cur, n = [], 0
    cur.append(i); n += w
if cur: blocks.append(cur)

models = [m for m in spec.get("models", "gemini-3.1-flash-tts-preview,gemini-3.8-flash-tts").split(",") if m]
style = spec.get("style_prompt") or ("Read this in English as a documentary narrator: confident, clear, brisk pace, short pauses before dates and numbers. Read the text exactly as written." if spec.get("lang", "pt").startswith("en") else None) or spec.get("tts_style", "Narre em português do Brasil, como um canal de curiosidades e simulações: voz masculina animada, confiante e envolvente, ritmo ágil (cerca de 170 palavras por minuto), "
                         "com pequenas pausas dramáticas antes dos números e das reviravoltas. Nunca soe como propaganda nem como audiolivro. Leia exatamente o texto, sem acrescentar nada.")
audio, engines = [], []
for bl in blocks:
    text = " ".join(beats[i]["say"] for i in bl)
    try:
        x, model = ltts.gemini(text, spec.get("voice", "Fenrir"), style, models)
        engines.append(model)
    except Exception as e:
        print("::warning title=voz::gemini falhou, usando edge:", repr(e)[:200])
        x = ltts.edge(text, spec.get("edge_voice", "pt-BR-AntonioNeural")); engines.append("edge")
    x = ltts.tighten(ltts.clean(x), cap=0.42)
    # voz lenta (18/11: 3.8 devolveu 95 ppm num short) → tenta de novo com outro modelo; se seguir lenta, acelera até ~165 ppm (máx x1,35)
    nw_b = len(text.split()); min_wpm = float(spec.get("min_wpm", 140))
    wpm_b = nw_b / (len(x) / SR) * 60
    if wpm_b < min_wpm and engines[-1] != "edge":
        print(f"::warning title=voz lenta::{engines[-1]} {wpm_b:.0f} ppm < {min_wpm:.0f}, tentando outro modelo")
        alt = [m for m in models if m != engines[-1]] + [engines[-1]]
        try:
            y, m2 = ltts.gemini(text, spec.get("voice", "Fenrir"), style, alt)
            y = ltts.tighten(ltts.clean(y), cap=0.42)
            if len(y) < len(x):
                x = y; engines[-1] = m2
        except Exception as e:
            print("::warning title=voz::nova tentativa falhou:", repr(e)[:160])
        wpm_b = nw_b / (len(x) / SR) * 60
    if wpm_b < min_wpm:
        k = min(1.35, float(spec.get("target_wpm", 165)) / wpm_b)
        print(f"::warning title=voz lenta::{wpm_b:.0f} ppm, acelerando x{k:.2f}")
        x = ltts.tempo(x, k).astype(np.float32)
    audio.append(x); audio.append(np.zeros(int(0.22 * SR), np.float32))
voice = np.concatenate(audio)
lead = float(spec.get("lead", 0.35))
voice = np.concatenate([np.zeros(int(lead * SR), np.float32), voice])
# Shorts: no máximo 3 min — se a voz passar de ~176 s, acelera o necessário (atempo)
if spec.get("format", "short") == "short":
    lim = 176.0 - float(spec.get("tail", 1.4))
    if len(voice) / SR > lim:
        k = (len(voice) / SR) / lim
        print(f"::warning title=duração::voz {len(voice)/SR:.1f}s > {lim:.0f}s, acelerando x{k:.3f}")
        voice = ltts.tempo(voice, k).astype(np.float32)
sf.write(f"{OUT}/voice.wav", voice, SR)

# ---- Whisper (pt) + alinhamento ----
def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in w if unicodedata.category(c) != "Mn"))

from faster_whisper import WhisperModel
import librosa
wm = WhisperModel(os.environ.get("WHISPER", "small"), compute_type="int8")
x16 = librosa.resample(voice, orig_sr=SR, target_sr=16000)
segs, _ = wm.transcribe(x16, language=spec.get("lang", "pt"), word_timestamps=True, vad_filter=False, beam_size=5)
hyp = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]

script = []  # (palavra exibida, índice do beat)
for i, b in enumerate(beats):
    for w in b["say"].split():
        script.append((w, i))
import difflib
A = [norm(w) for w, _ in script]; B = [norm(w) for w, _, _ in hyp]
sm = difflib.SequenceMatcher(a=A, b=B, autojunk=False)
t0 = [None] * len(script); t1 = [None] * len(script)
for blk in sm.get_matching_blocks():
    for k in range(blk.size):
        t0[blk.a + k] = hyp[blk.b + k][1]; t1[blk.a + k] = hyp[blk.b + k][2]
matched = sum(v is not None for v in t0) / max(1, len(script))
known = [i for i, v in enumerate(t0) if v is not None]
dur = len(voice) / SR
for i in range(len(script)):
    if t0[i] is None:
        p = max([k for k in known if k < i], default=None); q = min([k for k in known if k > i], default=None)
        a = t1[p] if p is not None else lead
        b = t0[q] if q is not None else dur - 0.3
        np_ = (i - (p if p is not None else -1)); nq = ((q if q is not None else len(script)) - (p if p is not None else -1))
        t0[i] = a + (b - a) * (np_ - 0.5) / nq; t1[i] = t0[i] + 0.22
words = [{"w": re.sub(r"[|]", "", w), "t0": round(t0[i], 3), "t1": round(max(t1[i], t0[i] + 0.12), 3)} for i, (w, _) in enumerate(script)]
first = {}
for i, (_, bi) in enumerate(script):
    first.setdefault(bi, t0[i])
total = round(words[-1]["t1"] + float(spec.get("tail", 1.4)), 2)

# ---- trilha ----
music = None
for tr in [spec.get("music", {}).get("track")] + spec.get("music", {}).get("alt", []) + ["Investigations", "Hidden Agenda", "Curiosity"]:
    if not tr: continue
    try:
        url = "https://incompetech.com/music/royalty-free/mp3-royaltyfree/" + urllib.parse.quote(tr) + ".mp3"
        open(f"{OUT}/m.mp3", "wb").write(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read())
        if os.path.getsize(f"{OUT}/m.mp3") > 100000:
            music = tr; break
    except Exception as e:
        print("trilha falhou", tr, repr(e)[:100])
vol = spec.get("music", {}).get("vol", 0.13)
pad = f"apad=whole_dur={total}"
if music:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{OUT}/voice.wav", "-stream_loop", "-1", "-i", f"{OUT}/m.mp3", "-filter_complex",
                    f"[0:a]aresample=48000,{pad}[v];[1:a]aresample=48000,volume={vol},afade=t=out:st={max(0, total - 1.5):.2f}:d=1.5[m];[v][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[o]",
                    "-map", "[o]", "-ac", "2", "-ar", "48000", "-t", str(total), f"{OUT}/audio.wav"], check=True)
else:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{OUT}/voice.wav", "-af", f"aresample=48000,{pad},loudnorm=I=-14:TP=-1.5:LRA=9", "-ac", "2", "-t", str(total), f"{OUT}/audio.wav"], check=True)

vert = spec.get("format", "short") == "short"
bs = []
for i, b in enumerate(beats):
    d = {k: v for k, v in b.items() if k != "say"}
    d["t0"] = round(max(0.0, first.get(i, 0) - 0.12) if i else 0.0, 3)
    bs.append(d)
es = {"w": 1080 if vert else 1920, "h": 1920 if vert else 1080, "total": total, "beats": bs, "words": words, "hook": spec.get("hook"), "hook_end": spec.get("hook_end", 2.8), "tag": spec.get("tag"), "thumb": spec.get("thumb", {}),
      **{k: spec[k] for k in ("badge", "uf", "skin", "style", "basemap") if k in spec}}
json.dump(es, open(f"{OUT}/es.json", "w"), ensure_ascii=False)
yt = dict(spec["yt"])
cred = (f"\n\nMusic: \"{music}\" by Kevin MacLeod (incompetech.com), licensed under CC BY 4.0." if spec.get("lang", "pt").startswith("en")
        else f"\n\nMúsica: \"{music}\" — Kevin MacLeod (incompetech.com), licença CC BY 4.0.") if music else ""
yt["description"] = yt.get("description", "") + cred
json.dump({"yt": yt, "publish": spec.get("publish", {})}, open(f"{OUT}/yt.json", "w"), ensure_ascii=False)
nw = len(script)
g = {"total_s": total, "words": nw, "wpm": round(nw / max(1, words[-1]["t1"] - words[0]["t0"]) * 60), "align": round(matched, 3), "engines": engines, "music": music}
json.dump(g, open(f"{OUT}/gates.json", "w"))
print("ok", g)
if matched < 0.7:
    print(f"::error title=alinhamento::{matched:.2f} (<0.70)"); sys.exit(1)

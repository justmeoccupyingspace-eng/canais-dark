"""Monta os cortes verticais (Shorts) de um vídeo longo a partir da timeline (palavras com tempo).
Uso: python scripts/clips.py specs/clips/<x>.json /tmp/tl.json out/clips
Gera out/clips/<i>.props.json (para o Remotion) e out/clips/<i>.yt.json (metadados do upload)."""
import json, os, sys

cfg = json.load(open(sys.argv[1]))
tl = json.load(open(sys.argv[2]))
out = sys.argv[3]
os.makedirs(out, exist_ok=True)
by = {s["id"]: s for s in tl["shots"]}
ids = [s["id"] for s in tl["shots"]]
for i, c in enumerate(cfg["clips"]):
    a, b = ids.index(c["from"]), ids.index(c["to"])
    shots = [by[x] for x in ids[a:b + 1]]
    t0 = max(0.0, shots[0]["t0"] + c.get("pad_in", 0.0))
    t1 = min(tl["total"], shots[-1]["t_speech_end"] + c.get("pad_out", 0.7))
    words = [dict(w=w["w"], t0=w["t0"], t1=w["t1"]) for s in shots for w in s.get("words", []) if t0 <= w["t0"] <= t1]
    dur = t1 - t0
    if dur > 59.5:
        print(f"::warning title=clips::corte {i} tem {dur:.1f}s (> 59,5 s)")
    props = dict(channel=cfg["channel"], src="clips/src.mp4", t0=round(t0, 3), t1=round(t1, 3), words=words, hook=c["hook"],
                 cta=c.get("cta", "Full video on the channel"), longTitle=cfg.get("longTitle", ""))
    json.dump({"c": props}, open(f"{out}/{i}.props.json", "w"), ensure_ascii=False)
    desc = (f"{c.get('desc', '')}\n\nFull video: https://youtu.be/{cfg['long']}\n\n"
            f"{cfg.get('sources', '')}\n{cfg.get('music_credits', '')}\nNarration is AI-generated.\n\n#shorts {cfg.get('hashtags', '')}").strip()
    yt = dict(yt=dict(title=c["title"][:100], description=desc, tags=cfg.get("tags", []), lang="en"))
    json.dump(yt, open(f"{out}/{i}.yt.json", "w"), ensure_ascii=False, indent=1)
    print(f"corte {i}: {c['from']}–{c['to']} {t0:.1f}–{t1:.1f}s ({dur:.1f}s) | {c['title']} | {c.get('at', '')}")
json.dump([c.get("at", "") for c in cfg["clips"]], open(f"{out}/at.json", "w"))

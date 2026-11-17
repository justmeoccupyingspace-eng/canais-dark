"""Compilação longa (16:9) a partir de Shorts "E se" já produzidos: reaproveita voz/tempos de cada run (artefato eseprep),
re-enquadra em 1920x1080, corta o pedido de comentário do fim de cada trecho (fica só no último) e prepara a junção.
Uso: python scripts/ese_comp.py comp.json out/   (os artefatos já baixados em out/seg<i>/<id>/)"""
import json, os, subprocess, sys
comp = json.load(open(sys.argv[1], encoding="utf-8")); OUT = sys.argv[2]
segs = comp["segments"]; info = []
for i, sg in enumerate(segs):
    spec = json.load(open(sg["spec"], encoding="utf-8")); sid = spec["id"]
    d = f"{OUT}/seg{i}/{sid}"
    es = json.load(open(f"{d}/es.json"))
    es["w"], es["h"] = 1920, 1080
    # visual ATUAL do spec sobre os tempos da voz (corrige códigos/bandeiras que mudaram depois do Short)
    if len(es["beats"]) == len(spec["beats"]):
        es["beats"] = [{**{k: v for k, v in b.items() if k != "say"}, "t0": o["t0"]} for b, o in zip(spec["beats"], es["beats"])]
    for k in ("badge", "uf", "skin", "style", "basemap", "terr"):
        if k in spec: es[k] = spec[k]
    last = i == len(segs) - 1
    if not last and sg.get("cut_cta", True) and len(es["beats"]) > 2:
        cut = es["beats"][-1]["t0"] + 0.15
        es["beats"] = es["beats"][:-1]; es["words"] = [w for w in es["words"] if w["t0"] < cut - 0.1]
        es["total"] = round(cut + 0.6, 2)
    es["thumb"] = comp.get("thumb", {})
    if sg.get("hook"): es["hook"] = sg["hook"]
    json.dump(es, open(f"{d}/es_long.json", "w"), ensure_ascii=False)
    # áudio do trecho: corta no novo fim com fade curto
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{d}/audio.wav", "-t", str(es["total"]), "-af", f"afade=t=out:st={max(0, es['total'] - 0.5):.2f}:d=0.5",
                    "-ar", "48000", "-ac", "2", f"{d}/audio_long.wav"], check=True)
    info.append({"i": i, "id": sid, "dir": d, "total": es["total"], "music": json.load(open(f"{d}/yt.json"))["yt"].get("description", "").split("Música:")[-1].strip() if "Música:" in json.load(open(f"{d}/yt.json"))["yt"].get("description", "") else ""})
json.dump(info, open(f"{OUT}/segs.json", "w"), ensure_ascii=False, indent=1)
tot = sum(x["total"] for x in info)
# capítulos na descrição (o YouTube exige o 1º em 0:00 e pelo menos 3)
t, chap = 0.0, []
for sg, x in zip(segs, info):
    chap.append(f"{int(t // 60)}:{int(t % 60):02d} {sg['chapter']}"); t += x["total"]
creds = sorted({x["music"] for x in info if x["music"]})
desc = comp["yt"]["description"] + "\n\n" + "\n".join(chap) + ("\n\nMúsica: " + " / ".join(creds) if creds else "")
json.dump({"yt": {**comp["yt"], "description": desc}, "publish": comp.get("publish", {})}, open(f"{OUT}/yt.json", "w"), ensure_ascii=False)
json.dump({"w": 1920, "h": 1080, "thumb": {**comp.get("thumb", {}), "w": 1280, "h": 720}, "beats": [], "words": [], "total": 1}, open(f"{OUT}/thumb_es.json", "w"), ensure_ascii=False)
print("total", round(tot, 1), "s", len(info), "trechos"); print("\n".join(chap))

"""Reaproveita voz e tempos de um run anterior (out/<id>/es.json, audio.wav) e aplica o visual ATUAL do spec
(câmera, donos, bolinhas, cartões, título, miniatura, textos do YouTube). As falas precisam ser as mesmas.
Uso: python scripts/ese_rebeat.py specs/ese/<id>.json out/<id>/"""
import json, sys
spec = json.load(open(sys.argv[1], encoding="utf-8")); OUT = sys.argv[2]
es = json.load(open(f"{OUT}/es.json"))
old = es["beats"]
if len(old) != len(spec["beats"]):
    sys.exit(f"::error::número de beats mudou ({len(old)} → {len(spec['beats'])}); precisa gerar a voz de novo")
es["beats"] = [{**{k: v for k, v in b.items() if k != "say"}, "t0": o["t0"]} for b, o in zip(spec["beats"], old)]
for k in ("hook", "tag", "badge", "uf", "skin", "basemap"):
    if k in spec: es[k] = spec[k]
es["hook_end"] = spec.get("hook_end", es.get("hook_end", 2.8)); es["thumb"] = spec.get("thumb", {})
json.dump(es, open(f"{OUT}/es.json", "w"), ensure_ascii=False)
y = json.load(open(f"{OUT}/yt.json"))
cred = y["yt"].get("description", "").split("\n\nMúsica:")
yt = dict(spec["yt"]); yt["description"] = yt.get("description", "") + ("\n\nMúsica:" + cred[1] if len(cred) > 1 else "")
json.dump({"yt": yt, "publish": spec.get("publish", {})}, open(f"{OUT}/yt.json", "w"), ensure_ascii=False)
print("ok: visual do spec aplicado sobre a voz existente", len(es["beats"]), "beats")

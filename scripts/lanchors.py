"""Confere se toda âncora "at" (keys, labels, react, items, stats, cues) existe no texto da narração do próprio shot — o prep falha com "frase não encontrada" se não existir.
Uso: python3 scripts/lanchors.py specs/long/a-L24.json [...]"""
import json, re, sys
bad = 0
norm = lambda t: re.sub(r"\s+", " ", t.replace("{p}", " ").replace("{pp}", " ").replace("<soft>", "").replace("</soft>", "")).lower()
for f in sys.argv[1:]:
    for s in json.load(open(f))["shots"]:
        n = norm(s.get("narration", ""))
        for k in ("keys", "labels", "react", "items", "stats", "cues"):
            for a in s.get(k) or []:
                if isinstance(a, dict) and a.get("at") and norm(a["at"]) not in n:
                    bad += 1; print(f"{f} {s['id']} {k}: '{a['at']}' não está na narração")
print("âncoras ok" if not bad else f"{bad} âncoras faltando"); sys.exit(1 if bad else 0)

"""Aplica correções de TEXTO do spec numa timeline já pronta (prep reaproveitado), sem mexer em tempos.
Uso: python scripts/lpatch.py specs/long/x.json public/build/<id>.json
Só troca campos string com a mesma estrutura (mesmo shot id, mesma posição na lista); 'at'/'narration' ficam como estão."""
import json, sys

SKIP = {"at", "until", "at_b", "id", "type", "narration", "act"}


def patch(tl, sp, path, log):
    if isinstance(sp, dict) and isinstance(tl, dict):
        for k, v in sp.items():
            if k in SKIP:
                continue
            if isinstance(v, str):
                if tl.get(k) != v:
                    log.append(f"{path}.{k}: {tl.get(k)!r} → {v!r}")
                    tl[k] = v
            elif isinstance(v, (dict, list)) and k in tl:
                patch(tl[k], v, f"{path}.{k}", log)
    elif isinstance(sp, list) and isinstance(tl, list) and len(sp) == len(tl):
        for i, (a, b) in enumerate(zip(tl, sp)):
            patch(a, b, f"{path}[{i}]", log)


if __name__ == "__main__":
    spec, tlp = json.load(open(sys.argv[1])), sys.argv[2]
    tl = json.load(open(tlp))
    by = {s["id"]: s for s in spec["shots"]}
    log = []
    for s in tl["shots"]:
        if s["id"] in by:
            patch(s, by[s["id"]], s["id"], log)
    for k in ("yt", "thumb", "chapter0"):
        if k in spec:
            tl[k] = spec[k]
    json.dump(tl, open(tlp, "w"), ensure_ascii=False)
    for l in log:
        print("::notice title=lpatch::" + l[:300])
    print(f"lpatch: {len(log)} textos atualizados")

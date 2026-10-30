"""Aplica correções de TEXTO do spec numa timeline já pronta (prep reaproveitado), sem mexer em tempos.
Uso: python scripts/lpatch.py specs/long/x.json public/build/<id>.json
Só troca campos string com a mesma estrutura (mesmo shot id, mesma posição na lista); 'narration' fica como está.
Deixas ('at', 'until', 'at_b', 'reveal_last') trocadas no spec são recalculadas pelas palavras já alinhadas do shot."""
import json, re, sys

SKIP = {"id", "type", "narration", "act"}
CUEKEYS = {"at": "t", "until": "t_until", "at_b": "t_b", "reveal_last": "t_last"}


def norm(s):
    return [w for w in (re.sub(r"[^a-z0-9']", "", x.lower().replace("’", "'")) for x in s.split()) if w]


def find(words, phrase):
    p, n = norm(phrase), [norm(w["w"])[0] if norm(w["w"]) else "" for w in words]
    for i in range(len(n) - len(p) + 1):
        if n[i:i + len(p)] == p:
            return words[i]["t0"]
    return None


def patch(tl, sp, path, log, words=None):
    if isinstance(sp, dict) and isinstance(tl, dict):
        for k, v in sp.items():
            if k in SKIP:
                continue
            if k in CUEKEYS and isinstance(v, str):
                if tl.get(k) != v:
                    t = find(words or [], v)
                    if t is None:
                        log.append(f"{path}.{k}: deixa {v!r} não encontrada nas palavras do shot, mantida {tl.get(k)!r}")
                    else:
                        tl[k], tl[CUEKEYS[k]] = v, round(t + sp.get("delay", 0), 3)
                        log.append(f"{path}.{k}: deixa → {v!r} @ {tl[CUEKEYS[k]]}s")
                continue
            if isinstance(v, str):
                if tl.get(k) != v:
                    log.append(f"{path}.{k}: {tl.get(k)!r} → {v!r}")
                    tl[k] = v
            elif isinstance(v, (dict, list)) and k in tl:
                patch(tl[k], v, f"{path}.{k}", log, words)
    elif isinstance(sp, list) and isinstance(tl, list) and len(sp) == len(tl):
        for i, (a, b) in enumerate(zip(tl, sp)):
            patch(a, b, f"{path}[{i}]", log, words)


if __name__ == "__main__":
    spec, tlp = json.load(open(sys.argv[1])), sys.argv[2]
    tl = json.load(open(tlp))
    by = {s["id"]: s for s in spec["shots"]}
    log = []
    for s in tl["shots"]:
        if s["id"] in by:
            patch(s, by[s["id"]], s["id"], log, s.get("words"))
    for k in ("yt", "thumb", "chapter0"):
        if k in spec:
            tl[k] = spec[k]
    json.dump(tl, open(tlp, "w"), ensure_ascii=False)
    for l in log:
        print("::notice title=lpatch::" + l[:300])
    print(f"lpatch: {len(log)} textos atualizados")

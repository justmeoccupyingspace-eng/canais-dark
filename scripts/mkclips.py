"""Cria specs/clips/<id>.json a partir dos 'clips' do spec do longo, depois que ele subiu.
Uso: python scripts/mkclips.py specs/long/a-L03.json <videoId> <run_final> <run_prep> <hora1,hora2,...>
- run_final: execução cujo branch long-<run> tem a prévia 720p; run_prep: execução cujo lprep-<run> tem a timeline.
- horas em ISO UTC (uma por corte)."""
import json, os, re, sys

spec = json.load(open(sys.argv[1]))
vid, rfin, rprep, ats = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5].split(",")
yt = spec["yt"]
srcs = re.search(r"Sources:([^\n]+)", yt.get("description", ""))
cfg = dict(channel=spec["channel"], long=vid, longTitle=yt["title"], preview=f"long-{rfin}", timeline=f"lprep-{rprep}", timeline_file=spec["id"] + ".json",
           sources=("Sources:" + srcs.group(1)) if srcs else "", music_credits="Music by Kevin MacLeod (incompetech.com), CC BY 4.0.",
           hashtags=" ".join(t for t in yt.get("description", "").split() if t.startswith("#"))[:80], tags=yt.get("tags", [])[:8] + ["shorts"],
           clips=[dict(c, at=ats[i] if i < len(ats) else "") for i, c in enumerate(spec.get("clips", []))])
name = os.path.basename(sys.argv[1]).replace(".py", "").replace(".json", "")
out = f"specs/clips/{name}.json"
json.dump(cfg, open(out, "w"), ensure_ascii=False, indent=1)
print(out, len(cfg["clips"]), "cortes")

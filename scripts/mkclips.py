"""Cria specs/clips/<id>.json a partir dos 'clips' do spec do longo, depois que ele subiu.
Uso: python scripts/mkclips.py specs/long/a-L03.json <videoId> <run_final> <run_prep> <hora1,hora2,...>
- run_final: execução cujo branch long-<run> tem a prévia 720p; run_prep: execução cujo lprep-<run> tem a timeline.
- horas: `auto:<publishAt do longo em ISO UTC>` (padrão do Kauan, 29/10: 2 cortes na noite do longo + 2 na manhã seguinte,
  antes do próximo longo) ou lista ISO UTC explícita (só se seguir o padrão; senão o script recusa).
  A (longo 15:00 BRT): 19:00, 22:00, +1d 09:00, +1d 12:00 BRT · B (longo 17:00 BRT): 20:00, 23:00, +1d 10:00, +1d 13:00 BRT."""
import datetime as dt, json, os, re, sys
BRT = dt.timezone(dt.timedelta(hours=-3))
STD = {"A": [(0, 19), (0, 22), (1, 9), (1, 12)], "B": [(0, 20), (0, 23), (1, 10), (1, 13)]}
def iso(x): return dt.datetime.fromisoformat(x.replace("Z", "+00:00"))
def auto(ch, long_at):
    d = iso(long_at).astimezone(BRT)
    out = [dt.datetime(d.year, d.month, d.day, h, tzinfo=BRT) + dt.timedelta(days=k) for k, h in STD[ch]]
    out = [t if t > d + dt.timedelta(hours=2) else d + dt.timedelta(hours=2 + 3 * i) for i, t in enumerate(out)]  # longo atrasado
    return [t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") for t in out]

spec = json.load(open(sys.argv[1]))
vid, rfin, rprep, ats = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5].split(",")
ch = {"chartbound": "A", "howitticks": "B"}.get(str(spec["channel"]).lower().replace(" ", "").replace("-", ""), os.path.basename(sys.argv[1])[:1].upper())
if ats[0].startswith("auto:"):
    ats = auto(ch, ats[0][5:])
else:
    ok_h = {(h + 3) % 24 for _, h in STD[ch]}
    bad = [a for a in ats if iso(a).hour not in ok_h or iso(a).minute]
    if bad:
        sys.exit(f"horários fora do padrão do canal {ch}: {bad}. Use auto:<publishAt do longo> (ver QUEUE.md).")
print("cortes em:", ats)
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

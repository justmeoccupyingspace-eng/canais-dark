"""Despeja séries do World Bank WDI para explorar pauta antes de roteirizar.
Uso: python scripts/wbdump.py '{"ind": ["NY.GDP.PCAP.PP.CD"], "isos": ["KWT","USA"], "from": 1990, "to": 2025}' /tmp/dump.json"""
import json, sys, time, urllib.request

q = json.loads(sys.argv[1])
out = {}
for ind in q["ind"]:
    url = f"https://api.worldbank.org/v2/country/{';'.join(q['isos'])}/indicator/{ind}?format=json&date={q.get('from', 1990)}:{q.get('to', 2025)}&per_page=20000"
    for i in range(5):
        try:
            d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (data pipeline)"}), timeout=120))
            break
        except Exception as e:
            print("retry", i, ind, repr(e)[:80]); time.sleep(3 + 4 * i)
    s = {}
    if not isinstance(d, list) or len(d) < 2:
        out[ind] = {"error": str(d)[:300]}; print("sem dados", ind, str(d)[:200]); continue
    for r in (d[1] or []):
        if r["value"] is not None:
            s.setdefault(r["countryiso3code"], {})[r["date"]] = r["value"]
    out[ind] = {"name": (d[1] or [{}])[0].get("indicator", {}).get("value"), "data": s}
for e in q.get("estat", []):  # {"name","ds","filters"} via ldata.eurostat (isos ISO3)
    sys.path.insert(0, "scripts")
    from ldata import eurostat
    try:
        g = eurostat(e["ds"], e.get("filters", {}), q["isos"], q.get("from", 1990), q.get("to", 2026))
        out[e["name"]] = {"name": e["ds"] + " " + json.dumps(e.get("filters", {})), "data": {i: {str(y): v for y, v in d.items()} for i, d in g.items() if d}}
    except Exception as ex:
        out[e["name"]] = {"error": repr(ex)[:300]}
json.dump(out, open(sys.argv[2], "w"), indent=0)
print({k: len(v.get("data", {})) for k, v in out.items()})

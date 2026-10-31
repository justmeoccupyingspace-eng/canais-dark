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
    for r in (d[1] or []):
        if r["value"] is not None:
            s.setdefault(r["countryiso3code"], {})[r["date"]] = r["value"]
    out[ind] = {"name": (d[1] or [{}])[0].get("indicator", {}).get("value"), "data": s}
json.dump(out, open(sys.argv[2], "w"), indent=0)
print({k: len(v["data"]) for k, v in out.items()})

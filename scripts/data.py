"""Preenche cenas 'chart' com dados reais (FRED) e resolve {placeholders} na narração/legendas.
Uso: python scripts/data.py spec.json spec_out.json
Cena: {"type":"chart","source":{"fred":"MSPUS","from":1990,"to":2024,"step":5}} """
import csv, io, json, sys, urllib.request
from collections import defaultdict

def fred_annual(series, y0, y1):
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}&cosd={y0}-01-01&coed={y1}-12-31"
    raw = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read().decode()
    by = defaultdict(list)
    for row in list(csv.reader(io.StringIO(raw)))[1:]:
        if len(row) < 2 or row[1] in ("", "."):
            continue
        by[int(row[0][:4])].append(float(row[1]))
    return {y: sum(v) / len(v) for y, v in sorted(by.items())}

def worldbank_annual(ind, country, y0, y1):
    url = f"https://api.worldbank.org/v2/country/{country}/indicator/{ind}?format=json&per_page=200&date={y0}:{y1}"
    for attempt in range(3):
        try:
            data = json.load(urllib.request.urlopen(url, timeout=30))
            break
        except Exception as e:
            if attempt == 2:
                raise
    rows = data[1] or []
    return {int(r["date"]): float(r["value"]) for r in sorted(rows, key=lambda r: r["date"]) if r["value"] is not None}

def main(src, dst):
    spec = json.load(open(src, encoding="utf-8"))
    ctx = {}
    raw = {}
    for sc in spec["scenes"]:
        s = sc.get("source")
        if sc.get("type") == "chart" and s:
            if "worldbank" in s:
                ann = worldbank_annual(s["worldbank"], s.get("country", "USA"), s["from"], s["to"])
            else:
                ann = fred_annual(s["fred"], s["from"], s["to"])
            step = s.get("step", 1)
            years = [y for y in ann if (y - s["from"]) % step == 0]
            if years[-1] != max(ann):
                years.append(max(ann))
            sc["data"] = [{"x": str(y), "y": round(ann[y] * s.get("scale", 1), s.get("round", 1))} for y in years]
            f, l = sc["data"][0]["y"], sc["data"][-1]["y"]
            ctx.update(first_y=years[0], last_y=years[-1], first=f, last=l,
                       pct=round((l / f - 1) * 100), times=round(l / f, 1))
            def fmt(k, v):
                if k in ("first_y", "last_y"):
                    return str(v)
                if isinstance(v, float) and abs(v) >= 1000:
                    v = round(v)
                return f"{v:,}" if isinstance(v, (int, float)) and abs(v) >= 1000 else v
            raw.update({k: v for k, v in ctx.items() if k not in raw or not isinstance(v, str)})
            ctx.update({k: fmt(k, v) for k, v in raw.items()})
    def sub(t):
        return t.format(**ctx) if isinstance(t, str) and "{" in t else t
    for sc in spec["scenes"]:
        for k in ("narration", "caption", "text", "sub", "label", "title", "subtitle", "note", "hl"):
            if k in sc:
                sc[k] = sub(sc[k])
        if sc.get("type") == "stat" and "value_from" in sc:
            sc["value"] = raw[sc["value_from"]]
    if "yt" in spec:
        for k in ("title", "description"):
            spec["yt"][k] = sub(spec["yt"].get(k, ""))
    json.dump(spec, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("data ok", ctx)

if __name__ == "__main__":
    main(*sys.argv[1:3])

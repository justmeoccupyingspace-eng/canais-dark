"""Preenche cenas 'chart' com dados reais (FRED) e resolve {placeholders} na narração/legendas.
Uso: python scripts/data.py spec.json spec_out.json
Cena: {"type":"chart","source":{"fred":"MSPUS","from":1990,"to":2024,"step":5}} """
import csv, hashlib, io, json, sys, urllib.request
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

def ipca_series(first):
    """IPCA variação mensal (BCB SGS 433). first='AAAA-MM'. Retorna [(AAAA-MM, %)]."""
    y, m = first.split("-")
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json&dataInicial=01/{m}/{y}"
    last = None
    for i in range(3):
        try:
            rows = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30))
            break
        except Exception:
            if i == 2:
                raise
    out = []
    for r in rows:
        d, mo, yy = r["data"].split("/")
        out.append((f"{yy}-{mo}", float(r["valor"])))
    return out

MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]

def brl(v):
    return "R$ " + f"{round(v):,}".replace(",", ".")

def compute_blocks(spec, ctx, raw):
    c = spec.get("compute") or {}
    if "hash" in c:
        h = c["hash"]
        a, b = h["a"], h["b"]
        ha, hb = hashlib.sha256(a.encode()).hexdigest(), hashlib.sha256(b.encode()).hexdigest()
        ba, bb = bin(int(ha, 16))[2:].zfill(256), bin(int(hb, 16))[2:].zfill(256)
        flips = [x != y for x, y in zip(ba, bb)]
        raw.update(bits=sum(flips), word_a=a, word_b=b)
        data = {"a": a, "b": b, "ha": ha, "hb": hb, "flips": flips}
        for sc in spec["scenes"]:
            if sc.get("art") in ("hash-compare", "hash-one", "bitgrid"):
                sc["hashdata"] = data
    if "ipca" in c:
        i = c["ipca"]
        ser = ipca_series(i["from"]) if "series" not in i else i["series"]
        ser = [(m, v) for m, v in ser if m > i["from"]]
        f = 1.0
        for _, v in ser:
            f *= 1 + v / 100
        y, mo = i["from"].split("-")
        ly, lm = ser[-1][0].split("-")
        amt = i.get("amount", 100)
        from num2words import num2words
        say = lambda v: num2words(int(round(v)), lang="pt_BR")
        raw.update(ipca_needed_say=say(amt * f) + " reais", ipca_amount_say=say(amt) + " reais", ipca_pct_say=say((f - 1) * 100),
                   ipca_factor=round(f, 2), ipca_amount_n=amt, ipca_needed_n=round(amt * f), ipca_pct=round((f - 1) * 100), ipca_needed=brl(amt * f), ipca_amount=brl(amt),
                   ipca_from=f"{MESES[int(mo) - 1]} de {y}", ipca_to=f"{MESES[int(lm) - 1]} de {ly}")
        ctx.update({k: v for k, v in raw.items() if k.startswith("ipca")})

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
    compute_blocks(spec, ctx, raw)
    ctx.update({k: (v if not isinstance(v, (int, float)) or k in ('first_y','last_y') else v) for k, v in raw.items() if k not in ctx})
    def sub(t):
        return t.format(**ctx) if isinstance(t, str) and "{" in t else t
    for sc in spec["scenes"]:
        for k in ("narration", "caption", "text", "sub", "label", "title", "subtitle", "note", "hl", "big", "l1", "v1", "l2", "v2"):
            if k in sc:
                sc[k] = sub(sc[k])
        for k in [k for k in sc if k.endswith("_from") and k != "value_from"]:
            sc[k[:-5]] = raw[sc[k]]
        if sc.get("type") == "stat" and "value_from" in sc:
            sc["value"] = raw[sc["value_from"]]
    if "yt" in spec:
        for k in ("title", "description"):
            spec["yt"][k] = sub(spec["yt"].get(k, ""))
    json.dump(spec, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("data ok", ctx)

if __name__ == "__main__":
    main(*sys.argv[1:3])

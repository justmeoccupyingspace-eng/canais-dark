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

MESES_EN = ["January","February","March","April","May","June","July","August","September","October","November","December"]

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
            if sc.get("art") in ("hash-compare", "hash-one", "bitgrid") or sc.get("type") in ("hashcmp", "hashbox", "grid"):
                sc["hashdata"] = data
    if "terms" in c:
        from num2words import num2words
        first = min(t["from"] for t in c["terms"])
        ser = c["terms"][0].get("series") or ipca_series(first)
        last_m = ser[-1][0]
        for n, t in enumerate(c["terms"], 1):
            to = t.get("to") or last_m
            vs = [v for m, v in ser if t["from"] <= m <= to]
            f = 1.0
            for v in vs:
                f *= 1 + v / 100
            avg = (f ** (12 / len(vs)) - 1) * 100
            dec = f"{avg:.1f}".replace(".", ",")
            raw.update({f"t{n}_name": t["name"], f"t{n}_avg": round(avg, 1), f"t{n}_avg_s": dec,
                        f"t{n}_say": num2words(round(avg, 1), lang="pt_BR"), f"t{n}_acc": round((f - 1) * 100),
                        f"t{n}_meses": len(vs)})
        ctx.update({k: v for k, v in raw.items() if k.startswith("t") and k[1].isdigit()})
    if "cpi" in c:
        from num2words import num2words
        i = c["cpi"]
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCSL&cosd={i['from']}-01-01"
        rows = None
        annual = False
        for _ in range(3):
            try:
                rows = list(csv.reader(io.StringIO(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read().decode())))[1:]
                rows = [(r[0], float(r[1])) for r in rows if len(r) > 1 and r[1] not in ("", ".")]
                break
            except Exception as e:
                print("fred falhou:", e)
        if not rows:
            wb = worldbank_annual("FP.CPI.TOTL", "USA", i["from"], i["from"] + 40)
            rows = [(f"{y}-12-01", v) for y, v in sorted(wb.items())]
            annual = True
            print("CPI via World Bank (anual)")
        f = rows[-1][1] / rows[0][1]
        amt = i.get("amount", 100)
        ly, lm = rows[-1][0].split("-")[:2]
        raw.update(cpi_amount_n=amt, cpi_needed_n=round(amt * f), cpi_pct=round((f - 1) * 100),
                   cpi_amount_say=num2words(amt, lang="en"), cpi_needed_say=num2words(round(amt * f), lang="en"),
                   cpi_pct_say=num2words(round((f - 1) * 100), lang="en"), cpi_from=(str(i['from']) if annual else f"January {i['from']}"),
                   cpi_to=(ly if annual else f"{MESES_EN[int(lm) - 1]} {ly}"), cpi_year=i["from"])
        ctx.update({k: v for k, v in raw.items() if k.startswith("cpi")})
    if "ipv4" in c:
        from num2words import num2words
        pop = worldbank_annual("SP.POP.TOTL", "WLD", 2018, 2026)
        py = max(pop)
        addr = 2 ** 32 / 1e9
        people = pop[py] / 1e9
        raw.update(ipv4_n=round(addr, 1), people_n=round(people, 1), people_year=py, ipv4_ratio=round(people / addr, 1),
                   ipv4_say=num2words(round(addr, 1), lang="en"), people_say=num2words(round(people, 1), lang="en"),
                   ipv4_ratio_say=num2words(round(people / addr, 1), lang="en"))
        ctx.update({k: v for k, v in raw.items() if k.startswith(("ipv4", "people"))})
    if "wbratio" in c:
        from num2words import num2words
        w = c["wbratio"]
        A = worldbank_annual(w["ind"], w["a"], w["from"], w.get("to", w["from"] + 30))
        B = worldbank_annual(w["ind"], w["b"], w["from"], w.get("to", w["from"] + 30))
        ys = sorted(set(A) & set(B))
        y0, y1 = ys[0], ys[-1]
        r0, r1 = A[y0] / B[y0] * 100, A[y1] / B[y1] * 100
        raw.update(wr_from=y0, wr_to=y1, wr_r0=round(r0), wr_r1=round(r1), wr_r0_say=num2words(round(r0), lang="en"),
                   wr_r1_say=num2words(round(r1), lang="en"), wr_a_t=round(A[y1] / 1e12, 1), wr_b_t=round(B[y1] / 1e12, 1),
                   wr_a_t_say=num2words(round(A[y1] / 1e12, 1), lang="en"), wr_b_t_say=num2words(round(B[y1] / 1e12, 1), lang="en"))
        ctx.update({k: v for k, v in raw.items() if k.startswith("wr_")})
    if "floatsum" in c:
        from num2words import num2words
        fs = c["floatsum"]
        v = fs["a"] + fs["b"]
        raw.update(f_a=fs["a"], f_b=fs["b"], f_sum=repr(v), f_target=fs["target"], f_equal=str(v == fs["target"]).lower(),
                   f_digits=len(repr(v)) - 2)
        ctx.update({k: v2 for k, v2 in raw.items() if k.startswith("f_")})
    if "unix2038" in c:
        import datetime
        from num2words import num2words
        mx = 2 ** 31 - 1
        d = datetime.datetime.fromtimestamp(mx, datetime.timezone.utc)
        raw.update(u_max=mx, u_max_say=num2words(mx, lang="en"), u_date=f"{MESES_EN[d.month - 1]} {d.day}, {d.year}",
                   u_year=d.year, u_time=d.strftime("%H:%M:%S") + " UTC", u_bits=32)
        ctx.update({k: v for k, v in raw.items() if k.startswith("u_")})
    if "minwage" in c:
        from num2words import num2words
        m = c["minwage"]
        y, mo = m["from"].split("-")
        url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.1619/dados?formato=json&dataInicial=01/{mo}/{y}"
        rows = None
        for _ in range(3):
            try:
                rows = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60))
                break
            except Exception as e:
                print("sgs1619 falhou:", e)
        a, b = float(rows[0]["valor"]), float(rows[-1]["valor"])
        ly, lm = rows[-1]["data"].split("/")[2], rows[-1]["data"].split("/")[1]
        ser = [(mm, v) for mm, v in ipca_series(m["from"]) if mm > m["from"]]
        f = 1.0
        for _, v in ser:
            f *= 1 + v / 100
        say = lambda v: num2words(int(round(v)), lang="pt_BR")
        mw_pct, ip_pct = (b / a - 1) * 100, (f - 1) * 100
        real = (b / a / f - 1) * 100
        raw.update(mw_a=round(a), mw_b=round(b), mw_pct=round(mw_pct), ip_pct=round(ip_pct), mw_real=round(real),
                   mw_a_say=say(a) + " reais", mw_b_say=say(b) + " reais", mw_pct_say=say(mw_pct), ip_pct_say=say(ip_pct), mw_real_say=say(real),
                   mw_from=f"{MESES[int(mo) - 1]} de {y}", mw_to=f"{MESES[int(lm) - 1]} de {ly}")
        ctx.update({k: v for k, v in raw.items() if k.startswith(("mw_", "ip_"))})
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
            if sc.get("as_str"):
                sc["str"] = str(raw[sc["value_from"]])
                sc["value"] = 0
            else:
                sc["value"] = raw[sc["value_from"]]
    if "yt" in spec:
        for k in ("title", "description"):
            spec["yt"][k] = sub(spec["yt"].get(k, ""))
    json.dump(spec, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("data ok", ctx)

if __name__ == "__main__":
    main(*sys.argv[1:3])

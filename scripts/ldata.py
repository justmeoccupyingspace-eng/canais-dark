"""Dados do vídeo longo: puxa World Bank / IMF, monta os 'sets' usados pelo spec e confere cada número falado.
Uso: python scripts/ldata.py specs/long/a-L01.json public/build/a-L01.data.json
Falha (exit 1) se algum check do roteiro não bater com a fonte."""
import json, sys, time, urllib.request

WB = "https://api.worldbank.org/v2/country/{c}/indicator/{ind}?format=json&date={a}:{b}&per_page=5000"
IMF = "https://www.imf.org/external/datamapper/api/v1/{ind}"
EU27_2009 = ["AUT", "BEL", "DNK", "FIN", "FRA", "DEU", "GRC", "IRL", "ITA", "LUX", "NLD", "PRT", "ESP", "SWE", "GBR",
             "CZE", "EST", "CYP", "LVA", "LTU", "HUN", "MLT", "SVN", "SVK", "POL", "BGR", "ROU"]


def fetch(url, tries=5):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (data pipeline)"})
            return json.load(urllib.request.urlopen(req, timeout=90))
        except Exception as e:
            print("retry", i, url[:90], repr(e)[:80])
            time.sleep(3 + i * 4)
    raise RuntimeError("falhou " + url)


def wb(ind, isos, a, b):
    d = fetch(WB.format(c=";".join(isos), ind=ind, a=a, b=b))
    out = {i: {} for i in isos}
    for r in d[1] or []:
        if r["value"] is not None:
            out.setdefault(r["countryiso3code"], {})[int(r["date"])] = float(r["value"])
    return out


_imf = {}


def imf(ind, isos, a, b):
    if ind not in _imf:
        _imf[ind] = fetch(IMF.format(ind=ind))["values"][ind]
    v = _imf[ind]
    return {i: {int(y): float(x) for y, x in v.get(i, {}).items() if x is not None and a <= int(y) <= b} for i in isos}


def build_generic(spec):
    """datasets no spec: {set, wb, isos, from, to} | {set, derive: mul|ratio|div, a:[set,iso], b:[set,iso], k} |
    {set, wb, isos, year, flat: true}; snapshot: [{set, iso, year, value, src}] (fontes citadas, fora das APIs)."""
    S = {}
    for d in spec["datasets"]:
        st = d["set"]
        if "wb" in d and d.get("flat"):
            g = wb(d["wb"], d["isos"], d["year"], d["year"])
            S[st] = {i: g[i][d["year"]] for i in d["isos"] if d["year"] in g.get(i, {})}
        elif "wb" in d:
            got = wb(d["wb"], d["isos"], d.get("from", 1960), d.get("to", 2024))
            S.setdefault(st, {}).update(got)
        elif d.get("derive"):
            (sa, ia), (sb, ib) = d["a"], d["b"]
            A, B = S[sa][ia], S[sb][ib]
            k = d.get("k", 1)
            op = {"mul": lambda x, y: x * y * k, "ratio": lambda x, y: x / y * 100 * k, "div": lambda x, y: x / y * k}[d["derive"]]
            S.setdefault(st, {})[d.get("iso", ia)] = {y: op(A[y], B[y]) for y in A if y in B and B[y]}
    for p in spec.get("snapshot", []):
        S.setdefault(p["set"], {}).setdefault(p["iso"], {})[int(p["year"])] = float(p["value"])
    return S


def build(spec):
    if "datasets" in spec:
        return build_generic(spec)
    S = {}
    # histórico: World Bank (API aberta) até o último ano; projeção: pontos do FMI (WEO) gravados no spec com fonte
    snap = spec.get("imf_snapshot", {})
    S["ppp"] = wb("NY.GDP.PCAP.PP.CD", ["POL", "JPN", "ESP", "DEU", "GRC", "PRT"], 1990, 2024)
    for y, row in snap.get("PPPPC", {}).items():
        for i, v in row.items():
            if i in S["ppp"]:
                S["ppp"][i][int(y)] = float(v)
    S["ratio"] = {"POL": {y: S["ppp"]["POL"][y] / S["ppp"]["JPN"][y] * 100 for y in S["ppp"]["POL"] if y in S["ppp"]["JPN"]}}
    S["pppwb"] = wb("NY.GDP.PCAP.PP.CD", ["POL", "UKR"], 1990, 2024)
    S["nom"] = wb("NY.GDP.PCAP.CD", ["POL", "JPN"], 1990, 2024)
    S["fx"] = wb("PA.NUS.FCRF", ["JPN"], 2010, 2024)
    S["tfr"] = wb("SP.DYN.TFRT.IN", ["POL", "JPN", "KOR"], 1990, 2024)
    S["unemp"] = wb("SL.UEM.TOTL.ZS", ["POL"], 1991, 2024)
    S["infl"] = wb("FP.CPI.TOTL.ZG", ["POL"], 1989, 1995)
    S["growth"] = wb("NY.GDP.MKTP.KD.ZG", ["POL", "JPN"], 1990, 2024)
    g = wb("NY.GDP.MKTP.KD.ZG", EU27_2009, 2009, 2009)
    S["g2009"] = {i: g[i][2009] for i in EU27_2009 if 2009 in g.get(i, {})}
    S["pop"] = wb("SP.POP.TOTL", ["POL"], 1990, 2024)
    S["wap"] = wb("SP.POP.1564.TO", ["JPN"], 1980, 2024)
    S["debt"] = {i: {int(y): float(v)} for y, row in snap.get("GGXWDG_NGDP", {}).items() for i, v in row.items()}
    return S


def val(S, st, iso, year):
    ser = S[st][iso] if isinstance(S[st].get(iso), dict) else S[st]
    if isinstance(year, str) and year.startswith("max:"):
        a, b = map(int, year[4:].split("-"))
        y = max((y for y in ser if a <= y <= b), key=lambda y: ser[y])
        return ser[y], y
    return ser[int(year)], int(year)


def check(S, c):
    r = c.get("rule")
    try:
        if not r:
            v, y = val(S, c["set"], c["iso"], c["year"])
            ok = True
            if "approx" in c:
                ok &= abs(v - c["approx"]) <= c["tol"] * abs(c["approx"])
            if "min" in c:
                ok &= v >= c["min"]
            if "max" in c:
                ok &= v <= c["max"]
            return ok, f"{v:.4g} ({y})"
        if r == "cross":
            a, b = S[c["set"]][c["a"]], S[c["set"]][c["b"]]
            first = min(y for y in a if y in b and a[y] > b[y] and y > 1990)
            return first == c["year"], f"primeiro ano {c['a']}>{c['b']}: {first} ({a[first]:.0f} vs {b[first]:.0f})"
        if r == "allpos":
            ser = S[c["set"]][c["iso"]]
            neg = [y for y in range(c["a"], c["b"] + 1) if ser.get(y, -1) <= 0]
            return not neg, f"anos ≤0: {neg}"
        if r == "countneg":
            ser = S[c["set"]][c["iso"]]
            neg = [y for y in range(c["a"], c["b"] + 1) if ser.get(y, 0) < 0]
            return len(neg) == c["equal"], f"{len(neg)} anos negativos: {neg}"
        if r == "onlypos":
            pos = [i for i, v in S[c["set"]].items() if v > 0]
            return pos == [c["iso"]], f"positivos: {pos} (n={len(S[c['set']])})"
        if r == "fxloss":
            ser = S[c["set"]][c["iso"]]
            loss = 1 - ser[c["a"]] / ser[c["b"]]
            return c["min"] <= loss <= c["max"], f"perda {loss:.2%} ({ser[c['a']]:.1f}→{ser[c['b']]:.1f})"
        if r == "tied":
            a, b = S[c["set"]][c["a"]][c["year"]], S[c["set"]][c["b"]][c["year"]]
            return abs(a / b - 1) <= c["tol"], f"{a:.0f} vs {b:.0f}"
        if r == "gt":
            a, b = S[c["set"]][c["a"]][c["year"]], S[c["set"]][c["b"]][c["year"]]
            return a > b, f"{a:.0f} vs {b:.0f}"
        if r == "ratio":
            a, b = S[c["set"]][c["a"]][c["year"]], S[c["set"]][c["b"]][c["year"]]
            return c["min"] <= a / b <= c["max"], f"{a / b:.3f}"
        if r == "peak":
            ser = S[c["set"]][c["iso"]]
            y = max(ser, key=lambda k: ser[k])
            return c["a"] <= y <= c["b"] and ser[max(ser)] < ser[y], f"pico {y} ({ser[y]:.4g}), último {max(ser)} ({ser[max(ser)]:.4g})"
        if r == "passorder":
            a = S[c["set"]][c["a"]]
            firsts = []
            for o in c["order"]:
                b = S[c["set"]][o]
                common = [z for z in sorted(a) if z in b and z <= c["by"]]
                ys = [y for y in common if all(a[z] > b[z] for z in common if z >= y)]
                firsts.append(ys[0] if ys else None)
            ok = all(firsts) and firsts == sorted(firsts) and firsts[-1] <= c["by"]
            return ok, f"passou (de vez) em {dict(zip(c['order'], firsts))}"
        if r == "expr":  # conta em Python (expressões do próprio spec)
            v = eval(c["expr"], {"__builtins__": __builtins__})
            return v == c["equal"], f"{c['expr']} = {v!r}"
        if r == "lastrise":  # ano anterior mais recente em que a série subiu (antes de 'year')
            ser = S[c["set"]][c["iso"]]
            ys = sorted(y for y in ser if y < c["year"] and y - 1 in ser and ser[y] > ser[y - 1])
            return (ys[-1] if ys else None) == c["equal"], f"última alta antes de {c['year']}: {ys[-1] if ys else None}"
        if r == "avgratio":  # média de a1..b1 / média de a2..b2
            ser = S[c["set"]][c["iso"]]
            m1 = sum(ser[y] for y in range(c["a1"], c["b1"] + 1)) / (c["b1"] - c["a1"] + 1)
            m2 = sum(ser[y] for y in range(c["a2"], c["b2"] + 1)) / (c["b2"] - c["a2"] + 1)
            return c["min"] <= m1 / m2 <= c.get("max", 99), f"{m1:.0f} / {m2:.0f} = {m1 / m2:.2f}"
        if r == "conv":  # valor em moeda local convertido pelo câmbio do ano
            fx = S[c["set"]][c["iso"]][c["year"]]
            v = c["local"] / fx
            return c["min"] <= v <= c["max"], f"{c['local']:.4g} / {fx:.1f} = {v:.4g}"
        if r == "maxof":
            v = S[c["set"]][c["iso"]][c["year"]]
            others = {o: S[c["set"]].get(o, {}).get(c["year"]) for o in c["others"]}
            ok = v >= c["min"] and all(x is None or x < v for x in others.values())
            return ok, f"{v:.1f} vs {others}"
    except Exception as e:
        return False, "erro " + repr(e)[:120]
    return False, "regra desconhecida"


def main(src, dst):
    spec = json.load(open(src))
    S = build(spec)
    bad = 0
    for c in spec.get("checks", []):
        ok, info = check(S, c)
        print(("OK  " if ok else "FALHA ") + c["say"] + " → " + info)
        if not ok:
            bad += 1
            print(f"::error title=dado::{c['say']} → {info}")
    out = {k: ({i: {str(y): v for y, v in s.items()} for i, s in d.items()} if isinstance(next(iter(d.values()), None), dict) else d) for k, d in S.items()}
    json.dump(out, open(dst, "w"), indent=0)
    if bad and not spec.get("allow_bad_checks"):
        sys.exit(1)


if __name__ == "__main__":
    try:
        main(*sys.argv[1:3])
    except SystemExit:
        raise
    except Exception as e:
        import traceback
        tb = traceback.format_exc().strip().splitlines()
        print(f"::error title=ldata::{repr(e)[:300]} | " + " | ".join(l.strip() for l in tb[-6:])[:900])
        sys.exit(1)

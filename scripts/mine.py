"""Garimpo de pautas com número próprio (World Bank WDI; o datamapper do IMF bloqueia os runners com 403).
Procura ultrapassagens recentes/iminentes entre países, quem mais subiu e quem mais caiu.
Uso: python scripts/mine.py /tmp/mine.json"""
import json, sys, time, urllib.request

API = "https://api.worldbank.org/v2/"
NOTABLE = set("USA JPN DEU GBR FRA ITA CAN ESP KOR AUS CHN IND BRA RUS MEX TUR SAU ARG ZAF IDN NLD CHE SWE NOR PRT GRC ISR NZL IRL BEL AUT DNK FIN SGP".split())


def fetch(path, tries=5):
    for i in range(tries):
        try:
            req = urllib.request.Request(API + path, headers={"User-Agent": "Mozilla/5.0 (data pipeline)"})
            return json.load(urllib.request.urlopen(req, timeout=120))
        except Exception as e:
            print("retry", i, path, repr(e)[:80])
            time.sleep(3 + i * 4)
    raise RuntimeError(path)


def series(ind, scale=1.0):
    d = fetch(f"country/all/indicator/{ind}?format=json&date=2000:2026&per_page=20000")
    out = {}
    for r in d[1] or []:
        if r["value"] is not None and r["countryiso3code"]:
            out.setdefault(r["countryiso3code"], {})[int(r["date"])] = float(r["value"]) * scale
    return out


meta = fetch("country?format=json&per_page=400")[1]
names = {m["id"]: m["name"] for m in meta if m["region"]["value"] != "Aggregates"}
pop = series("SP.POP.TOTL", 1e-6)  # milhões
ind = {"PPPPC": series("NY.GDP.PCAP.PP.CD"), "NGDPDPC": series("NY.GDP.PCAP.CD"), "NGDPD": series("NY.GDP.MKTP.CD")}
LAST = max(y for c in ("USA", "DEU", "POL") for y in ind["PPPPC"].get(c, {}))
print("último ano no WDI:", LAST)
real = {c for c in names if c in pop and max(pop[c].values() or [0]) >= 1.0}


def score(a, b, s):
    base = s.get(a, {}).get(2000), s.get(b, {}).get(2000)
    gap = (base[0] / base[1]) if all(base) else 1.0
    fame = (3 if b in NOTABLE else 1) * (2 if a in NOTABLE else 1)
    return round(fame * (1.2 - min(gap, 1.0)) * (max(pop[a].values() or [1]) ** 0.25), 3), round(gap, 3)


out = {"last": LAST, "crossings": [], "risers": [], "fallers": []}
for k, s in ind.items():
    cs = [c for c in real if c in s]
    if k == "NGDPD":
        top = sorted(cs, key=lambda c: -s[c].get(LAST, 0))[:40]
        cs = top
    for y in range(LAST - 2, LAST + 1):
        for a in cs:
            for b in cs:
                if a == b:
                    continue
                pa, pb = s[a].get(y - 1), s[b].get(y - 1)
                ca, cb = s[a].get(y), s[b].get(y)
                if None in (pa, pb, ca, cb):
                    continue
                if pa < pb and ca >= cb:
                    sc, gap = score(a, b, s)
                    out["crossings"].append({"ind": k, "year": y, "a": a, "b": b, "an": names.get(a), "bn": names.get(b),
                                             "a_prev": round(pa), "b_prev": round(pb), "a_now": round(ca), "b_now": round(cb),
                                             "gap2000": gap, "score": sc, "proj": False})
out["crossings"].sort(key=lambda r: -r["score"])
out["crossings"] = out["crossings"][:150]

s = ind["PPPPC"]
us = s["USA"]
rel = []
for c in real:
    if c in s and all(y in s[c] for y in (2010, LAST)) and max(pop[c].values() or [0]) >= 3:
        r10, r26 = s[c][2010] / us[2010], s[c][LAST] / us[LAST]
        rel.append({"c": c, "n": names.get(c), "vsUS_2010": round(r10, 3), "vsUS_last": round(r26, 3), "chg": round(r26 - r10, 3),
                    "pop": round(max(pop[c].values() or [0]), 1)})
rel.sort(key=lambda r: -r["chg"])
out["risers"] = rel[:30]
out["fallers"] = rel[-30:][::-1]
json.dump(out, open(sys.argv[1], "w"), indent=1, ensure_ascii=False)
print(len(out["crossings"]), "ultrapassagens")

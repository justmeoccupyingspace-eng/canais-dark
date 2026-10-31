"""Garimpo de pautas com número próprio (IMF WEO via datamapper).
Procura ultrapassagens recentes/iminentes entre países, quem mais subiu e quem mais caiu.
Uso: python scripts/mine.py /tmp/mine.json"""
import json, sys, time, urllib.request

API = "https://www.imf.org/external/datamapper/api/v1/"
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


def series(ind):
    v = fetch(ind)["values"][ind]
    return {c: {int(y): float(x) for y, x in d.items() if x is not None} for c, d in v.items() if len(c) == 3}


names = {c: d.get("label") for c, d in fetch("countries")["countries"].items()}
pop = series("LP")  # milhões
ind = {"PPPPC": series("PPPPC"), "NGDPDPC": series("NGDPDPC"), "NGDPD": series("NGDPD")}
real = {c for c in names if c in pop and pop[c].get(2025, 0) >= 1.0}


def score(a, b, s):
    base = s.get(a, {}).get(2000), s.get(b, {}).get(2000)
    gap = (base[0] / base[1]) if all(base) else 1.0
    fame = (3 if b in NOTABLE else 1) * (2 if a in NOTABLE else 1)
    return round(fame * (1.2 - min(gap, 1.0)) * (pop[a].get(2025, 1) ** 0.25), 3), round(gap, 3)


out = {"crossings": [], "risers": [], "fallers": []}
for k, s in ind.items():
    cs = [c for c in real if c in s]
    if k == "NGDPD":
        top = sorted(cs, key=lambda c: -s[c].get(2025, 0))[:40]
        cs = top
    for y in range(2023, 2029):
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
                                             "gap2000": gap, "score": sc, "proj": y > 2025})
out["crossings"].sort(key=lambda r: -r["score"])
out["crossings"] = out["crossings"][:150]

s = ind["PPPPC"]
us = s["USA"]
rel = []
for c in real:
    if c in s and all(y in s[c] for y in (2010, 2026)) and pop[c].get(2025, 0) >= 3:
        r10, r26 = s[c][2010] / us[2010], s[c][2026] / us[2026]
        rel.append({"c": c, "n": names.get(c), "vsUS_2010": round(r10, 3), "vsUS_2026": round(r26, 3), "chg": round(r26 - r10, 3),
                    "pop": round(pop[c].get(2025, 0), 1)})
rel.sort(key=lambda r: -r["chg"])
out["risers"] = rel[:30]
out["fallers"] = rel[-30:][::-1]
json.dump(out, open(sys.argv[1], "w"), indent=1, ensure_ascii=False)
print(len(out["crossings"]), "ultrapassagens")

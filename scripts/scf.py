"""SCF 2025 (Federal Reserve, Survey of Consumer Finances) — extrato resumido público.
Baixa o CSV, calcula percentis ponderados por faixa de idade e grava research/scf2025.json. Uso: python scripts/scf.py <out.json>"""
import io, json, sys, urllib.request, zipfile
import numpy as np, pandas as pd

URLS = ["https://www.federalreserve.gov/econres/files/scfp2025excel.zip", "https://www.federalreserve.gov/econres/files/scfp2025s.zip"]
UA = {"User-Agent": "Mozilla/5.0 (research; Chartbound)"}

def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180).read()

df = None
for u in URLS:
    try:
        z = zipfile.ZipFile(io.BytesIO(get(u)))
        names = z.namelist(); print("zip", u, names)
        for n in names:
            if n.lower().endswith(".csv"):
                df = pd.read_csv(z.open(n)); break
            if n.lower().endswith(".dta"):
                df = pd.read_stata(z.open(n)); break
        if df is not None: print("ok", u, df.shape); break
    except Exception as e:
        print("falhou", u, repr(e)[:200])
if df is None:
    sys.exit("sem dados")
df.columns = [c.upper() for c in df.columns]
print("colunas", [c for c in df.columns][:80])

def wq(x, w, qs):
    o = np.argsort(x); x, w = np.asarray(x)[o], np.asarray(w)[o]
    c = np.cumsum(w) / w.sum()
    return {str(q): float(np.interp(q / 100, c, x)) for q in qs}

def wshare(mask, w):
    return float(w[mask].sum() / w.sum())

bands = {"<35": (0, 34), "35-44": (35, 44), "45-54": (45, 54), "55-64": (55, 64), "65-74": (65, 74), "75+": (75, 200), "all": (0, 200), "55+": (55, 200), "65+": (65, 200)}
Q = [10, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90, 95, 99]
out = {"source": "Federal Reserve, 2025 Survey of Consumer Finances, summary extract public data (2025 dollars)", "n_rows": int(len(df)), "bands": {}}
W = df["WGT"].to_numpy()
for b, (a, z) in bands.items():
    m = (df["AGE"] >= a) & (df["AGE"] <= z)
    d = df[m]; w = d["WGT"].to_numpy()
    r = {"households_weight_share": float(w.sum() / W.sum()),
         "networth_pct": wq(d["NETWORTH"], w, Q),
         "networth_mean": float(np.average(d["NETWORTH"], weights=w)),
         "share_nw_ge": {str(k): wshare(d["NETWORTH"].to_numpy() >= k, w) for k in [100_000, 250_000, 500_000, 1_000_000, 2_000_000, 5_000_000]},
         "share_nw_le0": wshare(d["NETWORTH"].to_numpy() <= 0, w),
         "income_pct": wq(d["INCOME"], w, [10, 25, 50, 75, 90, 95]) if "INCOME" in d else None}
    if "RETQLIQ" in d:
        has = d["RETQLIQ"].to_numpy() > 0
        r["ret_share_has"] = wshare(has, w)
        r["ret_pct_holders"] = wq(d["RETQLIQ"][has], w[has], [25, 50, 75, 90])
        r["ret_mean_holders"] = float(np.average(d["RETQLIQ"][has], weights=w[has]))
        r["ret_share_ge"] = {str(k): wshare(d["RETQLIQ"].to_numpy() >= k, w) for k in [100_000, 250_000, 500_000, 1_000_000]}
    for col in ["HOUSES", "FIN", "NFIN", "DEBT", "HOMEEQ", "LIQ"]:
        if col in d:
            r[col.lower() + "_median_all"] = wq(d[col], w, [50])["50"]
    if "HOUSES" in d:
        r["homeowner_share"] = wshare(d["HOUSES"].to_numpy() > 0, w)
    out["bands"][b] = r
    print(b, {k: round(v) for k, v in r["networth_pct"].items()}, "≥1M", round(r["share_nw_ge"]["1000000"], 3))
json.dump(out, open(sys.argv[1], "w"), indent=1)

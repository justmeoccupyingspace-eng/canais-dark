"""Gera specs/long/a-L04.json — Chartbound longo #4 (RASCUNHO/probe de dados): países que estão encolhendo (Bulgária, Letônia, Lituânia...).
Este arquivo por enquanto só puxa os dados (mode=data) para o roteiro ser escrito em cima dos números reais."""
import json, os

ISOS = ["BGR", "LVA", "LTU", "ROU", "HRV", "EST", "SRB", "BIH", "MDA", "ALB", "UKR", "POL", "HUN", "GRC", "PRT", "DEU", "ITA", "ESP", "JPN", "KOR", "USA", "EUU"]
EUP = ["BGR", "LVA", "LTU", "ROU", "HRV", "EST", "POL", "HUN", "GRC", "PRT", "DEU", "ITA", "ESP", "EU"]
datasets = [
    dict(set="pop", wb="SP.POP.TOTL", isos=ISOS, **{"from": 1960, "to": 2024}),
    dict(set="tfr", wb="SP.DYN.TFRT.IN", isos=ISOS, **{"from": 1960, "to": 2024}),
    dict(set="netmig", wb="SM.POP.NETM", isos=ISOS, **{"from": 1990, "to": 2024}),
    dict(set="lem", wb="SP.DYN.LE00.MA.IN", isos=ISOS, **{"from": 1990, "to": 2024}),
    dict(set="lef", wb="SP.DYN.LE00.FE.IN", isos=ISOS, **{"from": 1990, "to": 2024}),
    dict(set="o65", wb="SP.POP.65UP.TO.ZS", isos=ISOS, **{"from": 1990, "to": 2024}),
    dict(set="cbr", wb="SP.DYN.CBRT.IN", isos=ISOS, **{"from": 1990, "to": 2024}),
    dict(set="cdr", wb="SP.DYN.CDRT.IN", isos=ISOS, **{"from": 1990, "to": 2024}),
    dict(set="gdppc", wb="NY.GDP.PCAP.PP.CD", isos=ISOS, **{"from": 1990, "to": 2024}),
    dict(set="proj", eurostat="proj_23np", filters={"projection": "BSL", "sex": "T", "age": "TOTAL", "unit": "PER"}, isos=EUP, **{"from": 2025, "to": 2100}),
]
shots = [dict(act=0, type="host", bg="none", narration="probe", items=[], react=[])]
for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"
spec = dict(id="a-L04-shrinking", clips=[], channel="chartbound", chapter0="", w=1920, h=1080, fps=30, acts=["probe"], shots=shots, checks=[],
            datasets=datasets, snapshot=[], voice=dict(model="", name="Charon", style=""), music=[], yt=dict(title="probe", description="", tags=[], lang="en"))
json.dump(spec, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "a-L04.json"), "w"), ensure_ascii=False, indent=1)
print("probe a-L04")

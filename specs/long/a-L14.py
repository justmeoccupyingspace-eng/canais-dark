"""Gera specs/long/a-L14.json — Chartbound longo #14 (linha de foco "quem está passando quem", série Polônia).
ETAPA 1 (02/11): só datasets, para rodar longo.yml mode=data e escrever o roteiro com os números reais."""
import json, os

EU27 = ["AUT", "BEL", "BGR", "HRV", "CYP", "CZE", "DNK", "EST", "FIN", "FRA", "DEU", "GRC", "HUN", "IRL", "ITA", "LVA", "LTU", "LUX", "MLT", "NLD", "POL", "PRT", "ROU", "SVK", "SVN", "ESP", "SWE"]
K = ["GRC", "POL", "HRV", "ROU", "PRT", "HUN", "BGR", "EUU"]
datasets = [
    dict(set="usd", wb="NY.GDP.PCAP.CD", isos=K, **{"from": 1995, "to": 2025}),
    dict(set="ppp", wb="NY.GDP.PCAP.PP.CD", isos=K, **{"from": 1995, "to": 2025}),
    dict(set="rpc", wb="NY.GDP.PCAP.PP.KD", isos=K, **{"from": 1995, "to": 2025}),
    dict(set="gdppps", eurostat="prc_ppp_ind", filters={"na_item": "VI_PPS_EU27_2020_HAB", "ppp_cat": "GDP"}, isos=EU27, **{"from": 2000, "to": 2025}),
    dict(set="aic", eurostat="prc_ppp_ind", filters={"na_item": "VI_PPS_EU27_2020_HAB", "ppp_cat": "A01"}, isos=EU27, **{"from": 2000, "to": 2025}),
    dict(set="unemp", wb="SL.UEM.TOTL.ZS", isos=["GRC", "POL", "HRV", "ROU"], **{"from": 2000, "to": 2025}),
    dict(set="yunemp", wb="SL.UEM.1524.ZS", isos=["GRC", "POL", "HRV", "ROU"], **{"from": 2000, "to": 2025}),
    dict(set="debt", eurostat="gov_10dd_edpt1", filters={"unit": "PC_GDP", "na_item": "GD", "sector": "S13"}, isos=["GRC", "POL", "HRV", "ROU"], **{"from": 2000, "to": 2025}),
    dict(set="bal", eurostat="gov_10dd_edpt1", filters={"unit": "PC_GDP", "na_item": "B9", "sector": "S13"}, isos=["GRC", "POL", "HRV", "ROU"], **{"from": 2015, "to": 2025}),
    dict(set="pop", wb="SP.POP.TOTL", isos=["GRC", "POL", "HRV", "ROU"], **{"from": 1995, "to": 2025}),
    dict(set="mw", eurostat="earn_mw_cur", filters={"currency": "EUR"}, isos=["GRC", "POL", "HRV", "ROU", "PRT"], **{"from": 2005, "to": 2025}),
    dict(set="gdpg", wb="NY.GDP.MKTP.KD.ZG", isos=["GRC", "POL", "HRV", "ROU", "EUU"], **{"from": 2005, "to": 2025}),
    dict(set="le", wb="SP.DYN.LE00.IN", isos=["GRC", "POL", "HRV", "ROU"], **{"from": 2000, "to": 2024}),
    dict(set="gfcf", wb="NE.GDI.FTOT.ZS", isos=["GRC", "POL", "HRV", "ROU", "EUU"], **{"from": 2000, "to": 2025}),
]
spec = dict(id="a-L14-greece", channel="chartbound", shots=[], checks=[], datasets=datasets, snapshot=[], acts=[], w=1920, h=1080, fps=30)
json.dump(spec, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "a-L14.json"), "w"), ensure_ascii=False, indent=1)
print("datasets", len(datasets))

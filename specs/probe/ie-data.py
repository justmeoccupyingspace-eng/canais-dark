"""Sonda de dados para o A-L03 (Irlanda): só baixa, sem checks."""
import json, os
EU = ["IRL", "LUX", "DEU", "NLD", "DNK", "AUT", "BEL", "FRA", "ITA", "ESP", "POL", "EU"]
datasets = [
    dict(set="gdppc", wb="NY.GDP.PCAP.CD", isos=["IRL", "USA", "DEU", "GBR", "LUX", "CHE", "NOR", "DNK", "FRA", "EUU", "SGP"], **{"from": 1990, "to": 2024}),
    dict(set="ppp", wb="NY.GDP.PCAP.PP.CD", isos=["IRL", "USA", "DEU", "LUX", "EUU", "NOR", "SGP"], **{"from": 1990, "to": 2024}),
    dict(set="gdpg", wb="NY.GDP.MKTP.KD.ZG", isos=["IRL", "EUU", "USA"], **{"from": 1990, "to": 2024}),
    dict(set="gdp", wb="NY.GDP.MKTP.CN", isos=["IRL"], **{"from": 1995, "to": 2024}),
    dict(set="gni", wb="NY.GNP.MKTP.CN", isos=["IRL"], **{"from": 1995, "to": 2024}),
    dict(set="pop", wb="SP.POP.TOTL", isos=["IRL"], **{"from": 1995, "to": 2024}),
    dict(set="aic", eurostat="prc_ppp_ind", filters={"na_item": "VI_PPS_EU27_2020_HAB", "ppp_cat": "A01"}, isos=EU, **{"from": 1995, "to": 2025}),
    dict(set="gdpidx", eurostat="prc_ppp_ind", filters={"na_item": "VI_PPS_EU27_2020_HAB", "ppp_cat": "GDP"}, isos=EU, **{"from": 1995, "to": 2025}),
]
spec = dict(id="probe-ie", channel="chartbound", acts=["x"], shots=[dict(id="s00", act=0, type="host", narration="x")], checks=[], datasets=datasets, snapshot=[])
json.dump(spec, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ie-data.json"), "w"))

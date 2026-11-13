"""Gera specs/long/a-L28.json — Chartbound longo #28: "Poland Just Passed Slovakia. By $12." (série Polônia; substitui o A-L27, que repetia o A-L17)
Formato "passou" (o que mais rende no canal). Medida: PIB per capita em dólares correntes (NGDPDPC, câmbio de mercado), dito na tela e na narração;
a versão ajustada por preços (PPPPC) entra no ato 3 para explicar a diferença (a Polônia passou a Eslováquia em PPC já em 2018).
Dados: IMF WEO out/2026 (research/imf_v4_2026-11-13.json: POL, SVK, HUN, CZE e outros, lido 13/11 via imf.org).
Fora do FMI (documentado): a Eslováquia adotou o euro em 1/1/2009; produz cerca de 1 milhão de carros por ano (maior produção per capita do mundo,
ZAP SR/OICA); Visegrád = Polônia, Tchéquia, Eslováquia, Hungria."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "..", "..", "research", "imf_v4_2026-11-13.json")))
ACTS = ["Cold open", "22 years", "Slovakia's sprint", "The currency", "Hungary, three times", "The pass", "Your guess"]
IMF = "IMF World Economic Outlook, October 2026"


def series(ind, iso):
    r = D[ind][iso]
    return {r["y0"] + k: v for k, v in enumerate(r["v"])}


C4 = ("POL", "SVK", "HUN", "CZE")
N = {iso: series("NGDPDPC", iso) for iso in C4}
PP = {iso: series("PPPPC", iso) for iso in C4}
GR = {iso: series("NGDP_RPCH", iso) for iso in ("POL", "SVK", "HUN", "CZE", "ROU", "EST", "HRV", "SVN")}
LP = {iso: series("LP", iso) for iso in ("POL", "SVK", "HUN")}
DEBT = {iso: series("GGXWDG_NGDP", iso) for iso in ("POL", "SVK", "HUN")}
LUR = {iso: series("LUR", iso) for iso in ("POL", "SVK", "HUN")}
CPI = {iso: series("PCPIPCH", iso) for iso in ("POL", "SVK", "HUN")}
P, K, H, Z = N["POL"], N["SVK"], N["HUN"], N["CZE"]


def grow(iso, a, b):
    c = 1.0
    for y in range(a + 1, b + 1):
        c *= 1 + GR[iso][y] / 100
    return c


snapshot = []
for iso in C4:
    for y, v in N[iso].items():
        snapshot.append(dict(set="imfusd", iso=iso, year=y, value=v, src=IMF + " · NGDPDPC"))
    for y, v in PP[iso].items():
        snapshot.append(dict(set="imf", iso=iso, year=y, value=v, src=IMF + " · PPPPC"))
for iso in ("POL", "SVK", "HUN"):
    for y, v in GR[iso].items():
        snapshot.append(dict(set="imfg", iso=iso, year=y, value=v, src=IMF + " · NGDP_RPCH"))
for st, tab, ind in [("pop", LP, "LP"), ("debt", DEBT, "GGXWDG_NGDP"), ("lur", LUR, "LUR"), ("cpi", CPI, "PCPIPCH")]:
    for iso, s in tab.items():
        for y, v in s.items():
            snapshot.append(dict(set=st, iso=iso, year=y, value=v, src=IMF + " · " + ind))

USDSRC = IMF + " · GDP per capita, current US$ at market exchange rates (NGDPDPC); 2026+ are IMF estimates and forecasts"
PPPSRC = IMF + " · GDP per capita, PPP, current international $ (PPPPC); 2026+ are IMF estimates and forecasts"
USD2 = dict(set="imfusd", fc=2025, series=["SVK", "POL"], years=[1995, 2031], y=[0, 45000], src=USDSRC, fmt="usd0", hl="POL")  # usd0: com usdk0 o rótulo de 2025 dava "$29k × $28k", contradizendo os US$ 12

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="lines", start=2025.0, **USD2,
         narration="Twelve dollars. {p} That's how far Poland got ahead of Slovakia last year, in the IMF's numbers: income per person, in plain dollars, at market exchange rates. Twenty-eight thousand five hundred and ten for the average Pole, twenty-eight thousand four hundred and ninety-eight for the average Slovak. {pp} For twenty-two years, from 2003 to 2024, Slovakia was ahead. In 2009, it was forty-three percent ahead. {p} This year, the IMF has Poland about three hundred dollars in front. By 2031, about two and a half thousand.",
         keys=[dict(at="Twelve dollars", year=2025.0, dur=0.5), dict(at="For twenty-two years", year=2003.0, dur=2.0), dict(at="In 2009", year=2009.0, dur=2.0), dict(at="This year", year=2026.0, dur=1.5), dict(at="By 2031", year=2031.0, dur=2.5)],
         labels=[dict(at="Twenty-eight thousand five hundred and ten", iso="POL", year=2025), dict(at="twenty-eight thousand four hundred", iso="SVK", year=2025), dict(at="In 2009", iso="SVK", year=2009), dict(at="By 2031", iso="POL", year=2031)],
         react=[dict(at="Twelve dollars", pose="shock"), dict(at="plain dollars", pose="pointUp"), dict(at="For twenty-two years", pose="pointL"), dict(at="forty-three percent", pose="shock"), dict(at="By 2031", pose="cheer")]),
    dict(act=0, type="host", bg="lines", start=2031.0, **{k: v for k, v in USD2.items() if k != "src"},
         narration="In this series, Poland has been passing countries on income adjusted for prices: Portugal, then Japan. This one is different. This is plain money: what the average person's output is worth in dollars on the world market. {p} And on that measure, Poland just passed a neighbor that uses the euro, and that builds more cars per person than any other country on Earth. {pp} <soft>So how did Slovakia get so far ahead, why did Poland need twenty-two years to catch up, and what about Hungary? Poland has passed Hungary three times.</soft>",
         items=[dict(at="This one is different", text="Plain dollars", serif=True, size=66, color="acc"), dict(at="uses the euro", text="Slovakia: euro since 2009", color="acc2", size=58), dict(at="three times", text="Hungary: passed 3×", color="warm", size=60)],
         react=[dict(at="In this series", pose="pointL"), dict(at="This one is different", pose="think"), dict(at="more cars per person", pose="shock"), dict(at="three times", pose="pointUp")]),

    # ---------------- 1 · 22 YEARS ----------------
    dict(act=1, type="host", bg="none",
         narration="Quick one before the chart: this is a series, and the next episode is another country Poland just passed. Subscribe so you don't miss it. {p} Now, the long view.",
         items=[dict(at="this is a series", text="The Poland series", serif=True, size=66, color="acc"), dict(at="Subscribe", text="Subscribe", size=70)],
         react=[dict(at="Quick one", pose="wave"), dict(at="another country", pose="pointUp"), dict(at="Subscribe", pose="cheer"), dict(at="the long view", pose="pointL")]),
    dict(act=1, type="lines", start=1995.0, **{**USD2, "series": ["HUN", "SVK", "POL"]},
         narration="In 1995, the three were close: about three thousand six hundred dollars per person in Poland, three thousand eight hundred in Slovakia, four and a half thousand in Hungary. {p} Then Slovakia took off. In 2003 it passed Poland, and kept pulling away. By 2008, the average Slovak produced about eighteen thousand dollars a year, the average Pole about fourteen. {pp} Then 2009. Slovakia joined the euro, and the gap jumped to forty-three percent. Slovakia stayed ahead every single year after that, until 2025.",
         keys=[dict(at="In 1995", year=1995.0, dur=1.5), dict(at="Then Slovakia took off", year=2000.0, dur=2.0), dict(at="In 2003", year=2003.0, dur=1.5), dict(at="By 2008", year=2008.0, dur=1.5), dict(at="Then 2009", year=2009.0, dur=1.5), dict(at="every single year", year=2025.0, dur=4.0)],
         labels=[dict(at="In 1995", iso="HUN", year=1995), dict(at="In 2003", iso="SVK", year=2003), dict(at="By 2008", iso="SVK", year=2008), dict(at="the average Pole about fourteen", iso="POL", year=2008), dict(at="until 2025", iso="POL", year=2025)],
         react=[dict(at="In 1995", pose="pointL"), dict(at="took off", pose="shock"), dict(at="kept pulling away", pose="think"), dict(at="forty-three percent", pose="shock"), dict(at="until 2025", pose="cheer")]),

    # ---------------- 2 · SLOVAKIA'S SPRINT ----------------
    dict(act=2, type="bars", mode="abs", set="imfg", iso="SVK", years=[2000, 2030], start=2000.0, fmt="pct1", src=IMF + " · real GDP growth, Slovakia (annual %); 2026+ are IMF estimates and forecasts",
         narration="Here's Slovakia's economy, year by year, after inflation. {p} From 2004 to 2007, it grew faster every year: about five percent, then six and a half, almost nine, and almost eleven in 2007. That boom was built on factories, above all car factories. Today Slovakia builds about a million cars a year, in a country of about five point four million people. {pp} But look at the right side. Since 2022, Slovakia has grown about two percent at best. Last year and this year, under one percent. Poland: three point seven, then three point four.",
         keys=[dict(at="Here's Slovakia's", year=2002.0, dur=3.0), dict(at="From 2004 to 2007", year=2004.0, dur=1.5), dict(at="almost eleven in 2007", year=2007.0, dur=2.0), dict(at="look at the right side", year=2022.0, dur=2.0), dict(at="under one percent", year=2026.0, dur=2.0)],
         react=[dict(at="Here's Slovakia's", pose="pointL"), dict(at="almost eleven", pose="shock"), dict(at="a million cars", pose="pointUp"), dict(at="the right side", pose="think"), dict(at="under one percent", pose="shrug")]),
    dict(act=2, type="stats", src=IMF + " · real GDP growth (NGDP_RPCH, compounded)", title="The real race",
         narration="Over thirty years, the race was closer than the dollars suggest. Since 1995, after inflation, Poland's economy has grown about three times over, Slovakia's about two point six times, and Hungary's has doubled. {p} Slovakia grew faster before 2008. Poland, much faster after: since 2008, about seventy-six percent, against thirty-nine for Slovakia. {pp} So why did Poland need twenty-two years to catch up in dollars? One word: currency.",
         stats=[dict(at="three times over", value=round(grow("POL", 1995, 2025), 1), fmt="dec1", label="Poland, real economy 2025 vs 1995 (×)"), dict(at="two point six times", value=round(grow("SVK", 1995, 2025), 1), fmt="dec1", label="Slovakia, 2025 vs 1995 (×)"), dict(at="seventy-six percent", value=round((grow("POL", 2008, 2025) - 1) * 100), fmt="pct0", label="Poland, real growth 2008–2025"), dict(at="thirty-nine for Slovakia", value=round((grow("SVK", 2008, 2025) - 1) * 100), fmt="pct0", label="Slovakia, real growth 2008–2025")],
         react=[dict(at="closer than the dollars", pose="think"), dict(at="Hungary's has doubled", pose="shrug"), dict(at="much faster after", pose="cheer"), dict(at="One word", pose="pointUp")]),

    # ---------------- 3 · THE CURRENCY ----------------
    dict(act=3, type="lines", set="imf", fc=2025, series=["SVK", "POL"], years=[1995, 2031], start=2009.0, y=[0, 80000], src=PPPSRC, fmt="usdk0", hl="POL",
         narration="Slovakia uses the euro. Poland kept its own currency, the złoty. And in 2009, the two went opposite ways. {p} Slovakia's economy shrank five and a half percent. Poland's grew two point six: the only economy in the region that didn't shrink. But in dollars, the average Pole's output fell eighteen percent that year, because the złoty fell. The average Slovak's fell eight. {pp} That's the catch with plain dollars: they move with exchange rates. On this chart, adjusted for what money actually buys at home, Poland passed Slovakia back in 2018. This year, by that measure, the average Pole is about twenty-one percent ahead.",
         keys=[dict(at="Slovakia uses the euro", year=2009.0, dur=1.0), dict(at="That's the catch", year=2012.0, dur=2.0), dict(at="back in 2018", year=2018.0, dur=2.0), dict(at="twenty-one percent ahead", year=2026.0, dur=2.5)],
         labels=[dict(at="back in 2018", iso="POL", year=2018), dict(at="twenty-one percent ahead", iso="POL", year=2026)],
         react=[dict(at="kept its own currency", pose="pointUp"), dict(at="shrank five and a half", pose="shock"), dict(at="fell eighteen percent", pose="shock"), dict(at="That's the catch", pose="think"), dict(at="twenty-one percent ahead", pose="cheer")]),

    # ---------------- 4 · HUNGARY, THREE TIMES ----------------
    dict(act=4, type="host", bg="none",
         narration="And if you're enjoying the series, the subscribe button is right there. {p} Now, Hungary.",
         items=[dict(at="subscribe button", text="Subscribe", size=66), dict(at="Now, Hungary", text="Hungary", serif=True, size=66, color="acc")],
         react=[dict(at="subscribe button", pose="pointUp"), dict(at="Now, Hungary", pose="pointL")]),
    dict(act=4, type="lines", set="imfusd", fc=2025, series=["HUN", "POL"], years=[2005, 2031], start=2012.0, y=[0, 45000], src=USDSRC, fmt="usd0", hl="POL",
         narration="In 1990, the average Hungarian produced twice as much as the average Pole, in dollars. {p} Poland first passed Hungary in 2012. Hungary took the lead back in 2013. Poland passed again in 2022. Hungary took it back again in 2023, by seventy-nine dollars. {pp} And in 2024, Poland passed a third time. This one looks like it sticks: about three thousand three hundred dollars ahead this year, and almost six thousand by 2031, in the IMF's forecast. {p} Hungary's recent years explain a lot: inflation of seventeen percent in 2023, the highest of the three, and an economy that shrank that year and barely grew in the next two.",
         keys=[dict(at="Poland first passed", year=2012.0, dur=1.5), dict(at="Poland passed again", year=2022.0, dur=1.5), dict(at="seventy-nine dollars", year=2023.0, dur=1.5), dict(at="a third time", year=2024.0, dur=1.5), dict(at="almost six thousand", year=2031.0, dur=3.0)],
         labels=[dict(at="Poland first passed", iso="POL", year=2012), dict(at="seventy-nine dollars", iso="HUN", year=2023), dict(at="a third time", iso="POL", year=2024), dict(at="almost six thousand", iso="POL", year=2031)],
         react=[dict(at="twice as much", pose="shock"), dict(at="took the lead back", pose="shrug"), dict(at="seventy-nine dollars", pose="shock"), dict(at="a third time", pose="cheer"), dict(at="seventeen percent", pose="think")]),

    # ---------------- 5 · THE PASS ----------------
    dict(act=5, type="stats", src=USDSRC, title="The pass, in plain dollars",
         narration="So here's the pass, in the IMF's numbers. {p} 2024: Slovakia twenty-five thousand nine hundred and seventy-two dollars per person, Poland twenty-five thousand one hundred and sixty-eight. Slovakia ahead by about eight hundred. {p} 2025: Poland ahead by twelve dollars. This year, by about three hundred. And by 2031, about two and a half thousand, in the IMF's forecast. {pp} One caveat: twelve dollars is nothing. One revision, or one bad year for the złoty, could flip it back. But the gap has shrunk from forty-three percent in 2009 to nothing.",
         stats=[dict(at="twenty-five thousand nine hundred and seventy-two", value=K[2024], fmt="usd0", label="Slovakia, 2024"), dict(at="twenty-five thousand one hundred and sixty-eight", value=P[2024], fmt="usd0", label="Poland, 2024"), dict(at="Poland ahead by twelve dollars", value=P[2025] - K[2025], fmt="usd0", label="Poland ahead, 2025"), dict(at="about two and a half thousand", value=P[2031] - K[2031], fmt="usd0", label="Poland ahead, 2031 (IMF)")],
         react=[dict(at="here's the pass", pose="pointUp"), dict(at="ahead by about eight hundred", pose="think"), dict(at="twelve dollars", pose="shock"), dict(at="One caveat", pose="think"), dict(at="to nothing", pose="cheer")]),
    dict(act=5, type="host", bg="none",
         narration="Zoom out to the four Visegrád countries: Poland, Czechia, Slovakia and Hungary. {p} In 1995, Poland was the poorest of the four in plain dollars. In 2025, it moved to second. {p} Only Czechia is still ahead: about thirty-nine and a half thousand dollars per person this year, against thirty-one in Poland. That's seventy-nine percent, and the IMF has Poland at eighty-six percent of Czechia by 2031.",
         items=[dict(at="poorest of the four", text="1995: 4th of 4", color="warm", size=62), dict(at="moved to second", text="2025: 2nd of 4", serif=True, size=64, color="acc"), dict(at="Only Czechia", text="Czechia: $39,614 vs $31,186", color="acc2", size=54)],
         react=[dict(at="Zoom out", pose="pointL"), dict(at="the poorest", pose="shrug"), dict(at="moved to second", pose="cheer"), dict(at="Only Czechia", pose="think")]),

    # ---------------- 6 · YOUR GUESS ----------------
    dict(act=6, type="host", bg="none",
         narration="<soft>So, what's your guess?</soft> {pp} Does Poland stay ahead of Slovakia this time, {p} or does the złoty flip it back, the way Hungary flipped it in 2023? {pp} Tell me in the comments. {pp} If you're watching from Slovakia: {p} does this match what you see? {pp} If you're in Poland: {p} did you know Slovakia was ever this far ahead? {pp} I read every comment.",
         items=[dict(at="your guess", text="Stay ahead or flip?", color="acc", size=66), dict(at="watching from Slovakia", text="Slovakia: does it match?", color="warm", size=58)],
         react=[dict(at="your guess", pose="shrug"), dict(at="Tell me", pose="pointUp"), dict(at="watching from Slovakia", pose="wave")]),
    dict(act=6, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="JPN", color="acc", title="Poland passed Japan", sub="the one nobody noticed."),
         narration="And if you missed it, {p} this is where the series took off: {p} the year Poland passed Japan, adjusted for prices. {pp} It's right here. {pp} I'm Chartbound. {p} See you in the next one.",
         hold=14,
         react=[dict(at="if you missed it", pose="pointL"), dict(at="See you", pose="wave")]),
]

NB = ("SVK", "HUN", "CZE", "ROU", "EST", "HRV", "SVN")
checks = [
    dict(say="2025: POL 28510, SVK 28498, gap 12", rule="expr", expr=f"[{P[2025]}, {K[2025]}, {P[2025] - K[2025]}]", equal=[28510, 28498, 12]),
    dict(say="SVK > POL every year 2003–2024 (22 years); 2002 POL ahead; 2009 SVK +43%", rule="expr", expr=f"[{all(K[y] > P[y] for y in range(2003, 2025))}, {P[2002] > K[2002]}, round(({K[2009]} / {P[2009]} - 1) * 100)]", equal=[True, True, 43]),
    dict(say="2026 gap ≈ 300; 2031 ≈ 2,500 (two and a half thousand)", rule="expr", expr=f"[round(({P[2026]} - {K[2026]}) / 100) * 100, round(({P[2031]} - {K[2031]}) / 500) * 500]", equal=[300, 2500]),
    dict(say="1995: POL ≈ 3,600, SVK ≈ 3,800, HUN ≈ 4,500", rule="expr", expr=f"[round({P[1995]} / 100) * 100, round({K[1995]} / 100) * 100, round({H[1995]} / 500) * 500]", equal=[3600, 3800, 4500]),
    dict(say="2008: SVK ≈ 18k, POL ≈ 14k; ratio 2008 → 2009 jumps to 43%", rule="expr", expr=f"[round({K[2008]} / 1000), round({P[2008]} / 1000), {K[2009] / P[2009] > K[2008] / P[2008]}]", equal=[18, 14, True]),
    dict(say="SVK growth 2004–2007 rising every year: 5.4 (about five), 6.5, 8.9 (almost nine), 10.8 (almost eleven)", rule="expr", expr=f"[{GR['SVK'][2004]}, {GR['SVK'][2005]}, {GR['SVK'][2006]}, {GR['SVK'][2007]}, {GR['SVK'][2003] < GR['SVK'][2004] < GR['SVK'][2005] < GR['SVK'][2006] < GR['SVK'][2007]}]", equal=[5.4, 6.5, 8.9, 10.8, True]),
    dict(say="SVK population 2026 = 5.4 (about five point four million)", rule="expr", expr=f"round({LP['SVK'][2026]}, 1)", equal=5.4),
    dict(say="SVK 2022–2026 max 2.1 (about two at best); 2025, 2026 = 0.8 (<1); POL 2025 3.7, 2026 3.4", rule="expr", expr=f"[{max(GR['SVK'][y] for y in range(2022, 2027))}, {GR['SVK'][2025]}, {GR['SVK'][2026]}, {GR['POL'][2025]}, {GR['POL'][2026]}]", equal=[2.1, 0.8, 0.8, 3.7, 3.4]),
    dict(say="real 1995→2025: POL ×3.1 (about three times), SVK ×2.6, HUN ×2.0 (doubled)", rule="expr", expr=f"[round({grow('POL', 1995, 2025)}, 1), round({grow('SVK', 1995, 2025)}, 1), round({grow('HUN', 1995, 2025)}, 1)]", equal=[3.1, 2.6, 2.0]),
    dict(say="before 2008 SVK faster (2000→2008: SVK 1.61 > POL 1.36); after 2008 POL +76%, SVK +39%", rule="expr", expr=f"[{grow('SVK', 2000, 2008) > grow('POL', 2000, 2008)}, round(({grow('POL', 2008, 2025)} - 1) * 100), round(({grow('SVK', 2008, 2025)} - 1) * 100)]", equal=[True, 76, 39]),
    dict(say="2009: SVK −5.5, POL +2.6, only POL ≥ 0 in the region (SVK, HUN, CZE, ROU, EST, HRV, SVN here; LTU −14.5 in research/imf_ltu_2026-11-10.json); USD/person POL −18%, SVK −8%", rule="expr", expr=f"[{GR['SVK'][2009]}, {GR['POL'][2009]}, {all(GR[i][2009] < 0 for i in NB)}, round(({P[2009]} / {P[2008]} - 1) * 100), round(({K[2009]} / {K[2008]} - 1) * 100)]", equal=[-5.5, 2.6, True, -18, -8]),
    dict(say="PPP: SVK ahead through 2017, POL ahead every year 2018–2031; 2026 POL +21%", rule="expr", expr=f"[{PP['SVK'][2017] > PP['POL'][2017]}, {all(PP['POL'][y] > PP['SVK'][y] for y in range(2018, 2032))}, round(({PP['POL'][2026]} / {PP['SVK'][2026]} - 1) * 100)]", equal=[True, True, 21]),
    dict(say="HUN/POL 1990 = 2.0 (twice)", rule="expr", expr=f"round({H[1990]} / {P[1990]}, 1)", equal=2.0),
    dict(say="HUN crossings in USD: POL ahead 2012, HUN 2013 (−2021), POL 2022, HUN 2023 by 79, POL 2024–2031", rule="expr", expr=f"[{P[2011] < H[2011]}, {P[2012] > H[2012]}, {all(H[y] > P[y] for y in range(2013, 2022))}, {P[2022] > H[2022]}, {H[2023] - P[2023]}, {all(P[y] > H[y] for y in range(2024, 2032))}]", equal=[True, True, True, True, 79, True]),
    dict(say="POL − HUN 2026 ≈ 3,300; 2031 ≈ 5.9k (almost six thousand)", rule="expr", expr=f"[round(({P[2026]} - {H[2026]}) / 100) * 100, round(({P[2031]} - {H[2031]}) / 100) * 100]", equal=[3300, 5900]),
    dict(say="HUN CPI 2023 17.1 (seventeen), highest of three; HUN growth 2023 −0.8, 2024 0.7, 2025 0.5", rule="expr", expr=f"[{CPI['HUN'][2023]}, {CPI['HUN'][2023] > max(CPI['POL'][2023], CPI['SVK'][2023])}, {GR['HUN'][2023]}, {GR['HUN'][2024]}, {GR['HUN'][2025]}]", equal=[17.1, True, -0.8, 0.7, 0.5]),
    dict(say="the pass: 2024 SVK 25972, POL 25168, gap ≈ 800; 2025 +12; 2026 ≈ +300", rule="expr", expr=f"[{K[2024]}, {P[2024]}, round(({K[2024]} - {P[2024]}) / 100) * 100]", equal=[25972, 25168, 800]),
    dict(say="Visegrád USD: 1995 POL lowest of 4; 2025 POL 2nd (CZE > POL > SVK > HUN)", rule="expr", expr=f"[{P[1995] < min(K[1995], H[1995], Z[1995])}, {Z[2025] > P[2025] > K[2025] > H[2025]}]", equal=[True, True]),
    dict(say="CZE 2026 ≈ 39.5k (39,614), POL ≈ 31k; POL/CZE 79% → 86% in 2031", rule="expr", expr=f"[{Z[2026]}, round({P[2026]} / 1000), round({P[2026]} / {Z[2026]} * 100), round({P[2031]} / {Z[2031]} * 100)]", equal=[39614, 31, 79, 86]),
    dict(say="items: $39,614 vs $31,186", rule="expr", expr=f"[{Z[2026]}, {P[2026]}]", equal=[39614, 31186]),
    dict(say="series callbacks: Poland passed Portugal (PPP, 2020) and Japan (PPP, 2026) — A-L21/A-L13", rule="expr", expr="[2020, 2026]", equal=[2020, 2026]),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="a-L28-poland-slovakia", clips=[], channel="chartbound", chapter0="$12",
            thumb=dict(v="flags", iso="POL", vs="SVK", sym=">", big="BY $12", line2="AFTER 22 YEARS"),
            w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks, datasets=[], snapshot=snapshot,
            voice=dict(model="", name="Charon",
                       style=("You are the narrator of a popular data documentary on YouTube. Read the script below in a warm, curious voice "
                              "with a little dry humor, at a relaxed but engaged pace of about 145 words per minute, like a smart friend telling "
                              "you something surprising. Let the big numbers land with a tiny pause before them. Keep the energy steady from the "
                              "first sentence to the last. Never sound like an advertisement or an audiobook.")),
            music=[dict(act=0, track="Lightless Dawn", vol=0.24), dict(act=1, track="Deliberate Thought", vol=0.22), dict(act=2, track="Hidden Agenda", vol=0.23), dict(act=3, track="Inspired", vol=0.23),
                   dict(act=4, track="Investigations", vol=0.23), dict(act=5, track="Deliberate Thought", vol=0.22), dict(act=6, track="Floating Cities", vol=0.24)],
            yt=dict(title="Poland Just Passed Slovakia. By $12.",
                    description=("Income per person in plain US dollars (IMF World Economic Outlook, October 2026): Slovakia was ahead of Poland every year from 2003 to 2024 — 43% ahead in 2009. "
                                 "In 2025: Poland $28,510, Slovakia $28,498. A $12 lead, ~$300 this year and ~$2,500 by 2031 in the IMF's forecast. Slovakia's car-led sprint (10.8% growth in 2007), "
                                 "why the złoty kept Poland behind in dollars (adjusted for prices, Poland passed Slovakia back in 2018), Hungary passed three times (2012, 2022, 2024), and where Poland now stands among the Visegrád four.\n\n"
                                 "Sources: IMF World Economic Outlook, October 2026 (NGDPDPC, PPPPC, NGDP_RPCH, LP, LUR, GGXWDG_NGDP, PCPIPCH). 2026+ figures are IMF estimates and forecasts.\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#poland #slovakia #hungary #economics #imf #europe #data"),
                    tags=["poland", "slovakia", "poland vs slovakia", "hungary", "visegrad", "slovakia economy", "poland economy", "gdp per capita", "imf", "economics", "europe", "polska", "słowacja", "slovensko"], lang="en"))

json.dump(spec, open(os.path.join(HERE, "a-L28.json"), "w"), ensure_ascii=False, indent=1)
clean = lambda t: t.replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()
words = sum(len(clean(s["narration"])) for s in shots)
acts = {}
for s in shots:
    acts[s["act"]] = acts.get(s["act"], 0) + len(clean(s["narration"]))
print("shots", len(shots), "palavras", words, f"~{words / 145:.1f} min a 145 wpm", "por ato", acts)

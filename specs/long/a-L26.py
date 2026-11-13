"""Gera specs/long/a-L26.json — Chartbound longo #26: "France Grew 0.4% This Year. Poland Is Closing In." (série Polônia, PLANO.md L1/L3)
Intro (PLANO R2): número nos primeiros 2 s. CTA de série no minuto 1 com gancho do próximo episódio (Polônia × Espanha, que a Polônia passa em 2027 no FMI).
Dados: IMF WEO out/2026 (research/imf_ita_2026-11-07.json: POL, FRA, GBR, ESP, lido 07/11). Fora do FMI (documentado): inflação HICP 2022 da França
(5,9%) foi a mais baixa da zona do euro, com teto de preços de energia ("bouclier tarifaire") e parque nuclear."""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "..", "..", "research", "imf_ita_2026-11-07.json")))
ACTS = ["Cold open", "Twins", "France's slow years", "Where France wins", "Where Poland wins", "The date", "Your guess"]
IMF = "IMF World Economic Outlook, October 2026"


def series(ind, iso):
    r = D[ind][iso]
    return {r["y0"] + k: v for k, v in enumerate(r["v"])}


P, F, G, E = series("PPPPC", "POL"), series("PPPPC", "FRA"), series("PPPPC", "GBR"), series("PPPPC", "ESP")
GR = {iso: series("NGDP_RPCH", iso) for iso in ("POL", "FRA")}
LP = {iso: series("LP", iso) for iso in ("POL", "FRA")}
N = {iso: series("NGDPDPC", iso) for iso in ("POL", "FRA")}
DEBT = {iso: series("GGXWDG_NGDP", iso) for iso in ("POL", "FRA")}
LUR = {iso: series("LUR", iso) for iso in ("POL", "FRA")}
CPI = {iso: series("PCPIPCH", iso) for iso in ("POL", "FRA")}

Y0, Y1 = 1990, 2031
R = {y: P[y] / F[y] for y in range(Y0, Y1 + 1)}
GAP = {y: F[y] - P[y] for y in range(Y0, Y1 + 1)}
first_at = lambda th: next(y for y in range(Y0, Y1 + 1) if R[y] >= th)


def grow(iso, a, b):
    c = 1.0
    for y in range(a + 1, b + 1):
        c *= 1 + GR[iso][y] / 100
    return c


k_recent = math.log(R[2026] / R[2016]) / 10
k_imf = math.log(R[2031] / R[2026]) / 5
par_recent = 2026 + math.log(1 / R[2026]) / k_recent
par_imf = 2031 + math.log(1 / R[2031]) / k_imf

snapshot = []
for y in range(Y0, Y1 + 1):
    snapshot.append(dict(set="rat", iso="POL", year=y, value=round(R[y] * 100, 2), src=IMF + " · Poland's GDP per capita (PPP) as % of France's"))
for iso, s in (("POL", P), ("FRA", F), ("GBR", G)):
    for y, v in s.items():
        snapshot.append(dict(set="imf", iso=iso, year=y, value=v, src=IMF + " · PPPPC"))
for iso in ("POL", "FRA"):
    for y, v in GR[iso].items():
        snapshot.append(dict(set="imfg", iso=iso, year=y, value=v, src=IMF + " · NGDP_RPCH"))
for st, tab, ind in [("pop", LP, "LP"), ("debt", DEBT, "GGXWDG_NGDP"), ("lur", LUR, "LUR"), ("imfusd", N, "NGDPDPC"), ("cpi", CPI, "PCPIPCH")]:
    for iso, s in tab.items():
        for y, v in s.items():
            snapshot.append(dict(set=st, iso=iso, year=y, value=v, src=IMF + " · " + ind))

RATSRC = IMF + " · Poland's GDP per capita, PPP, as % of France's; 2026+ are IMF estimates and forecasts"
RATCH = dict(set="rat", fc=2025, series=["POL"], years=[Y0, Y1], y=[0, 110], src=RATSRC, fmt="pct0", hl="POL", ref=dict(value=100, label="France = 100%", pos="left"))

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="lines", start=2026.0, **RATCH,
         narration="Zero point four percent. {p} That's how much the French economy grows this year, after inflation, in the IMF's estimate. Poland's: three point four. {pp} And that's how the gap closes. In 1990, the average Pole was at thirty-four percent of the average French person: income per person, adjusted for prices. Half by 2008. Seventy percent in 2019. Eighty-seven percent this year: about sixty thousand dollars against sixty-nine thousand. {p} The IMF has ninety percent in 2028, and ninety-five in 2031.",
         keys=[dict(at="Zero point four", year=2026.0, dur=0.5), dict(at="In 1990", year=1990.0, dur=1.5), dict(at="Half by 2008", year=2008.0, dur=1.5), dict(at="Seventy percent in 2019", year=2019.0, dur=1.5), dict(at="Eighty-seven percent this year", year=2026.0, dur=2.0), dict(at="ninety percent in 2028", year=2028.0, dur=1.5), dict(at="ninety-five in 2031", year=2031.0, dur=2.5)],
         labels=[dict(at="Eighty-seven percent this year", iso="POL", year=2026), dict(at="In 1990", iso="POL", year=1990), dict(at="Half by 2008", iso="POL", year=2008), dict(at="Seventy percent in 2019", iso="POL", year=2019), dict(at="ninety percent in 2028", iso="POL", year=2028)],
         react=[dict(at="Zero point four", pose="shock"), dict(at="three point four", pose="pointUp"), dict(at="In 1990", pose="pointL"), dict(at="Eighty-seven percent", pose="cheer"), dict(at="ninety-five in 2031", pose="think")]),
    dict(act=0, type="host", bg="lines", start=2031.0, **{k: v for k, v in RATCH.items() if k != "src"},
         narration="Last episode was Britain, and if these numbers sound familiar, there's a reason. This year, France and Britain are almost exactly as rich as each other per person: about sixty-eight thousand eight hundred dollars in France, sixty-eight thousand five hundred in Britain. {p} So Poland is catching both at the same speed. But France has its own story: the slowest growth of the two this year, the bigger debt, and the higher unemployment. {pp} <soft>Here's how fast the gap closed, where France still wins, and when Poland could pass it.</soft>",
         items=[dict(at="France and Britain", text="France ≈ Britain", serif=True, size=66, color="acc"), dict(at="sixty-eight thousand eight hundred", text="$68,852 vs $68,476", color="acc2", size=60), dict(at="the same speed", text="Poland: 87% of both", color="warm", size=60)],
         react=[dict(at="Last episode", pose="pointL"), dict(at="almost exactly as rich", pose="shock"), dict(at="the same speed", pose="pointUp"), dict(at="its own story", pose="think"), dict(at="when Poland could pass", pose="cheer")]),

    # ---------------- 1 · TWINS ----------------
    dict(act=1, type="host", bg="none",
         narration="Quick one before the chart: this is a series, and the next episode is Spain, the country Poland passes next year in the IMF's forecast. Subscribe so you don't miss it. {p} Now, the long view.",
         items=[dict(at="this is a series", text="The Poland series", serif=True, size=66, color="acc"), dict(at="Spain", text="Next: Poland vs Spain", color="acc2", size=62), dict(at="Subscribe", text="Subscribe", size=70)],
         react=[dict(at="Quick one", pose="wave"), dict(at="Spain", pose="pointUp"), dict(at="Subscribe", pose="cheer"), dict(at="the long view", pose="pointL")]),
    dict(act=1, type="lines", start=1990.0, **RATCH,
         narration="In 1990, the average French person produced almost twenty thousand dollars a year, adjusted for prices. The average Pole, about six thousand seven hundred. In 2004, the year Poland joined the European Union: about thirty-two thousand five hundred in France, about fourteen and a half thousand in Poland. {p} Since then, Poland's economy has grown about three and a half times, after inflation. France's, about one point seven times. {pp} For the first eighteen years, Poland gained slowly: thirty-four percent in 1990, forty-five when it joined the European Union in 2004. Then, after 2008, the line gets steep: Poland gained almost thirty points on France in sixteen years, from fifty-two percent in 2008 to eighty-one in 2024.",
         keys=[dict(at="In 1990", year=1990.0, dur=1.5), dict(at="Since then", year=2000.0, dur=2.5), dict(at="forty-five when it joined", year=2004.0, dur=1.5), dict(at="after 2008", year=2008.0, dur=1.5), dict(at="eighty-one in 2024", year=2024.0, dur=2.5)],
         labels=[dict(at="forty-five when it joined", iso="POL", year=2004), dict(at="eighty-one in 2024", iso="POL", year=2024)],
         react=[dict(at="In 1990", pose="pointL"), dict(at="three and a half times", pose="cheer"), dict(at="one point seven", pose="shrug"), dict(at="gets steep", pose="shock"), dict(at="eighty-one in 2024", pose="pointUp")]),

    # ---------------- 2 · FRANCE'S SLOW YEARS ----------------
    dict(act=2, type="bars", mode="abs", set="imfg", iso="FRA", years=[2000, 2031], start=2000.0, fmt="pct1", src=IMF + " · real GDP growth, France (annual %); 2026+ are IMF estimates and forecasts",
         narration="Here's France's economy, year by year, after inflation. Since 1990, it has shrunk in only three years: 1993, 2009 and 2020. France's problem isn't crashes. It's slow growth. {p} The 2010s: about one and a half percent a year on average. Poland, in the same decade: almost four. {pp} 2020: minus seven and a half percent. Then a rebound, and then a slowdown: under one percent last year, zero point four this year. {p} And the IMF's forecast doesn't see much more: about one percent a year until 2031. Poland, in the same forecast: two and a half.",
         keys=[dict(at="Here's France's", year=2005.0, dur=3.0), dict(at="The 2010s", year=2015.0, dur=2.0), dict(at="2020: minus", year=2020.0, dur=1.5), dict(at="zero point four this year", year=2026.0, dur=1.5), dict(at="until 2031", year=2031.0, dur=2.0)],
         react=[dict(at="Here's France's", pose="pointL"), dict(at="almost four", pose="pointUp"), dict(at="minus seven and a half", pose="shock"), dict(at="zero point four", pose="shrug"), dict(at="two and a half", pose="cheer")]),
    dict(act=2, type="stats", src=IMF + " · real GDP growth (NGDP_RPCH), population (LP)", title="Since 2019, and people",
         narration="Put the last six years side by side: from 2019 to 2025, the French economy grew about six percent in total. Poland's grew about eighteen. {p} And there's population. Since 1990, France has grown from about fifty-eight million people to sixty-nine million. Poland has shrunk, from thirty-eight million to thirty-six. {pp} More people sharing slower growth means income per person rises slowly in France. Fewer people sharing faster growth means it rises fast in Poland. That's the whole race in one sentence.",
         stats=[dict(at="about six percent", value=round((grow("FRA", 2019, 2025) - 1) * 100), fmt="pct0", label="France, real growth 2019–2025"), dict(at="about eighteen", value=round((grow("POL", 2019, 2025) - 1) * 100), fmt="pct0", label="Poland, real growth 2019–2025"), dict(at="sixty-nine million", value=round(LP["FRA"][2026], 1), fmt="dec1", label="million people in France, 2026 (1990: 58.0)"), dict(at="thirty-eight million to thirty-six", value=round(LP["POL"][2026], 1), fmt="dec1", label="million people in Poland, 2026 (1990: 38.2)")],
         react=[dict(at="side by side", pose="pointUp"), dict(at="about eighteen", pose="cheer"), dict(at="Poland has shrunk", pose="think"), dict(at="the whole race", pose="pointL")]),

    # ---------------- 3 · WHERE FRANCE WINS ----------------
    dict(act=3, type="stats", src=IMF + " · GDP per capita, current US$ (NGDPDPC); inflation (PCPIPCH)", title="Where France still wins",
         narration="Now, what France still does better. First, plain dollars. Without adjusting for prices, the average French person produces about fifty-one thousand dollars this year, and the average Pole about thirty-one thousand. Poland is at sixty-one percent there, not eighty-seven. {p} In 1990, it was thirteen times more. Now it's less than twice. {pp} Second: inflation. In 2022, the year energy prices exploded, French inflation was about six percent, the lowest in the euro area, thanks partly to price caps on energy. Poland's was over fourteen. {p} So for a Polish worker, a salary in France still goes a lot further in plain euros, even if rent in Paris eats a big part of it.",
         stats=[dict(at="about fifty-one thousand", value=N["FRA"][2026], fmt="usd0", label="France, plain US$, 2026"), dict(at="about thirty-one thousand", value=N["POL"][2026], fmt="usd0", label="Poland, plain US$, 2026"), dict(at="sixty-one percent", value=round(N["POL"][2026] / N["FRA"][2026] * 100), fmt="pct0", label="Poland vs France, plain dollars, 2026"), dict(at="about six percent", value=CPI["FRA"][2022], fmt="pct1", label="France, inflation, 2022 (Poland: 14.4%)")],
         react=[dict(at="still does better", pose="pointUp"), dict(at="not eighty-seven", pose="shrug"), dict(at="thirteen times", pose="shock"), dict(at="price caps", pose="think"), dict(at="over fourteen", pose="pointL")]),

    # ---------------- 4 · WHERE POLAND WINS ----------------
    dict(act=4, type="host", bg="none",
         narration="And if you're enjoying the series, the subscribe button is right there. Spain is next. {p} Now, where Poland already wins.",
         items=[dict(at="subscribe button", text="Subscribe", size=66), dict(at="already wins", text="Where Poland wins", serif=True, size=66, color="acc")],
         react=[dict(at="subscribe button", pose="pointUp"), dict(at="already wins", pose="cheer")]),
    dict(act=4, type="duel", set="debt", year=2026, a="POL", b="FRA", fmt="pct0", src=IMF + " · general government gross debt (% of GDP), 2026 estimate and 2031 forecast", title="Government debt, % of GDP, 2026", badge="LOWER IN POLAND",
         cues=[dict(at="about sixty-seven", show="a"), dict(at="France's: about a hundred and nineteen", show="b")],
         narration="Government debt this year: Poland, about sixty-seven percent of its economy. {pp} France's: about a hundred and nineteen, and still rising in the IMF's forecast, to about a hundred and twenty-four by 2031. Poland's debt rises too in that forecast, to about eighty-two, but it starts much lower. {p} And unemployment: about three point two percent in Poland. In France, eight point four. More than two and a half times as high.",
         react=[dict(at="Government debt", pose="pointUp"), dict(at="a hundred and nineteen", pose="shock"), dict(at="still rising", pose="think"), dict(at="eight point four", pose="pointL")]),

    # ---------------- 5 · THE DATE ----------------
    dict(act=5, type="stats", src=IMF + " · PPPPC; parity years are Chartbound extrapolations of the 2016–2026 and IMF 2026–2031 paces, not IMF forecasts", title="When does Poland pass France?",
         narration="So, when does Poland pass France? {p} The gap in dollars, adjusted for prices, was widest in 2006: about eighteen thousand eight hundred. This year, it's about eight thousand eight hundred. In the IMF's forecast, about three thousand eight hundred by 2031. {p} Beyond that, two honest extrapolations. At the pace of the last ten years, when Poland gained almost three percent a year on France, it passes around 2031. At the IMF's slower pace, around 2034. {pp} The exact same dates we got for Britain. These two really are twins.",
         stats=[dict(at="eighteen thousand eight hundred", value=GAP[2006], fmt="usd0", label="PPP gap, 2006 (the widest)"), dict(at="about eight thousand eight hundred", value=GAP[2026], fmt="usd0", label="PPP gap, 2026"), dict(at="around 2031", value=math.ceil(par_recent), fmt="yr", label="parity at the 2016–2026 pace"), dict(at="around 2034", value=math.ceil(par_imf), fmt="yr", label="parity at the IMF's 2026–2031 pace")],
         react=[dict(at="when does Poland pass", pose="pointUp"), dict(at="widest in 2006", pose="pointL"), dict(at="two honest", pose="think"), dict(at="around 2031", pose="cheer"), dict(at="really are twins", pose="shrug")]),
    dict(act=5, type="host", bg="none",
         narration="Think about what that means. In the early nineties, France was the kind of country Poles looked up to: three times richer per person, adjusted for prices. Within about a decade, by these numbers, the average Pole could produce as much as the average French person. {p} Prices, wages and pensions in plain euros will still be higher in France for a long time. But measured by what money actually buys, the race is nearly over.",
         items=[dict(at="three times richer", text="1990: France ≈ 3× Poland", color="warm", size=60), dict(at="nearly over", text="2026: Poland = 87%", serif=True, size=64, color="acc")],
         react=[dict(at="Think about", pose="think"), dict(at="three times richer", pose="shock"), dict(at="the average Pole could", pose="cheer"), dict(at="nearly over", pose="pointUp")]),

    # ---------------- 6 · YOUR GUESS ----------------
    dict(act=6, type="host", bg="none",
         narration="<soft>So, your guess: 2031, 2034, or later?</soft> Tell me in the comments. {p} If you're watching from France: does zero point four percent feel right from where you are? {p} If you're in Poland: did you expect to be this close to France? {p} And Spain: you're next. I read every comment.",
         items=[dict(at="your guess", text="2031, 2034 or later?", color="acc", size=66), dict(at="watching from France", text="France: does 0.4% feel right?", color="warm", size=56)],
         react=[dict(at="your guess", pose="shrug"), dict(at="Tell me", pose="pointUp"), dict(at="watching from France", pose="wave")]),
    dict(act=6, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="GBR", color="acc", title="Poland vs Britain: 88%", sub="France's twin."),
         narration="And if you missed it, Poland versus Britain is the twin of this one: eighty-eight percent, and the story of the Poles who moved there. That's right here. {p} I'm Chartbound. See you in the next one.",
         hold=14,
         react=[dict(at="if you missed it", pose="pointL"), dict(at="See you", pose="wave")]),
]

checks = [
    dict(say="FRA growth 2026 = 0.4 (IMF estimate); POL 2026 = 3.4", rule="expr", expr=f"[{GR['FRA'][2026]}, {GR['POL'][2026]}]", equal=[0.4, 3.4]),
    dict(say="1990 34%; ≥50% 2008; ≥70% 2019; 2026 87% (≈ $60k vs $69k); ≥90% 2028; 2031 95%", rule="expr", expr=f"[round({R[1990]} * 100), {first_at(0.5)}, {first_at(0.7)}, round({R[2026]} * 100), round({P[2026]} / 1000), round({F[2026]} / 1000), {first_at(0.9)}, round({R[2031]} * 100)]", equal=[34, 2008, 2019, 87, 60, 69, 2028, 95]),
    dict(say="FRA ≈ GBR 2026: $68.9k vs $68.5k (sixty-eight thousand eight hundred / five hundred); POL/GBR 88 ≈ POL/FRA 87", rule="expr", expr=f"[round({F[2026]} / 100) * 100, round({G[2026]} / 100) * 100]", equal=[68900, 68500]),
    dict(say="FRA vs GBR 2026: FRA slower growth (0.4 vs GBR), higher debt (118 vs 102), higher unemployment (8.4 vs 5.3) — GBR do A-L25", rule="expr", expr=f"[{GR['FRA'][2026]} < {series('NGDP_RPCH', 'GBR')[2026]}, round({DEBT['FRA'][2026]}) > 102, {LUR['FRA'][2026]} > 5.3]", equal=[True, True, True]),
    dict(say="ESP: POL passes in 2027 (IMF)", rule="expr", expr=f"[{P[2026] < E[2026]}, {P[2027] > E[2027]}]", equal=[True, True]),
    dict(say="1990: FRA ≈ $19.7k (almost twenty thousand), POL ≈ $6.7k", rule="expr", expr=f"[round({F[1990]} / 100) * 100, round({P[1990]} / 100) * 100]", equal=[19700, 6700]),
    dict(say="real 1990→2025: POL ×3.5, FRA ×1.7", rule="expr", expr=f"[round({grow('POL', 1990, 2025)}, 1), round({grow('FRA', 1990, 2025)}, 1)]", equal=[3.5, 1.7]),
    dict(say="2004: 45% (44.6); 2008: 52%; 2024: 81%", rule="expr", expr=f"[round({R[2004]} * 100), round({R[2008]} * 100), round({R[2024]} * 100)]", equal=[45, 52, 81]),
    dict(say="FRA avg 2010–2019 ≈ 1.4 (about one and a half), POL 3.8 (almost four)", rule="expr", expr=f"[round({sum(GR['FRA'][y] for y in range(2010, 2020)) / 10}, 1), round({sum(GR['POL'][y] for y in range(2010, 2020)) / 10}, 1)]", equal=[1.4, 3.8]),
    dict(say="FRA 2020 −7.6 (minus seven and a half); 2025 0.9 (under one percent); 2027–2031 0.7–1.2 (about one percent); POL 2027–2031 2.5", rule="expr", expr=f"[{GR['FRA'][2020]}, {GR['FRA'][2025]}, {all(0.7 <= GR['FRA'][y] <= 1.2 for y in range(2027, 2032))}, {sorted(set(GR['POL'][y] for y in range(2027, 2032)))}]", equal=[-7.6, 0.9, True, [2.5]]),
    dict(say="2019→2025: FRA ≈ +6%, POL ≈ +18%", rule="expr", expr=f"[round(({grow('FRA', 2019, 2025)} - 1) * 100), round(({grow('POL', 2019, 2025)} - 1) * 100)]", equal=[6, 18]),
    dict(say="population 1990→2026: FRA 58.0 → 69.1; POL 38.2 → 36.3", rule="expr", expr=f"[round({LP['FRA'][1990]}), round({LP['FRA'][2026]}), round({LP['POL'][1990]}), round({LP['POL'][2026]})]", equal=[58, 69, 38, 36]),
    dict(say="nominal 2026: FRA ≈ $51k, POL ≈ $31k, 61%; 1990 13×; 2026 < 2×", rule="expr", expr=f"[round({N['FRA'][2026]} / 1000), round({N['POL'][2026]} / 1000), round({N['POL'][2026]} / {N['FRA'][2026]} * 100), round({N['FRA'][1990]} / {N['POL'][1990]}), {N['FRA'][2026] / N['POL'][2026] < 2}]", equal=[51, 31, 61, 13, True]),
    dict(say="inflation 2022: FRA 5.9 (about six; HICP mais baixo da zona do euro — Eurostat), POL 14.4 (over fourteen)", rule="expr", expr=f"[{CPI['FRA'][2022]}, {CPI['POL'][2022]}]", equal=[5.9, 14.4]),
    dict(say="debt: POL 2026 ≈ 67; FRA 2026 118.5 (tela mostra 119 → narração 'a hundred and nineteen'), 2031 ≈ 124, rising", rule="expr", expr=f"[round({DEBT['POL'][2026]}), {DEBT['FRA'][2026]}, round({DEBT['FRA'][2031]})]", equal=[67, 118.5, 124]),
    dict(say="unemployment 2026: POL 3.2, FRA 8.4; ratio > 2.5", rule="expr", expr=f"[{LUR['POL'][2026]}, {LUR['FRA'][2026]}, {LUR['FRA'][2026] / LUR['POL'][2026] > 2.5}]", equal=[3.2, 8.4, True]),
    dict(say="PPP gap widest 2006 ≈ $18.8k; 2026 ≈ $8.8k; 2031 ≈ $3.8k", rule="expr", expr=f"[{max(GAP, key=GAP.get)}, round({GAP[2006]} / 100) * 100, round({GAP[2026]} / 100) * 100, round({GAP[2031]} / 100) * 100]", equal=[2006, 18800, 8800, 3800]),
    dict(say="pace 2016–2026 ≈ 2.8%/yr (almost three) → 2031 (2030.8); IMF → 2034 (2033.8); same as GBR (A-L25: 2031/2034)", rule="expr", expr=f"[round({k_recent} * 100, 1), {math.ceil(par_recent)}, {math.ceil(par_imf)}]", equal=[2.8, 2031, 2034]),
    dict(say="1990: FRA ≈ 3× POL per person (PPP); 'within about a decade' parity 2031–2034", rule="expr", expr=f"round({F[1990]} / {P[1990]}, 1)", equal=2.9),
    dict(say="2004: FRA ≈ $32.5k, POL ≈ $14.5k", rule="expr", expr=f"[round({F[2004]} / 500) * 500, round({P[2004]} / 500) * 500]", equal=[32500, 14500]),
    dict(say="FRA contraction years 1991–2031: 1993, 2009, 2020", rule="expr", expr=f"{[y for y in range(1991, 2032) if GR['FRA'][y] < 0]}", equal=[1993, 2009, 2020]),
    dict(say="POL debt 2031 ≈ 82", rule="expr", expr=f"round({DEBT['POL'][2031]})", equal=82),
    dict(say="2008→2024: +29 pts (almost thirty) in sixteen years", rule="expr", expr=f"[round(({R[2024]} - {R[2008]}) * 100), 2024 - 2008]", equal=[29, 16]),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="a-L26-poland-france", clips=[], channel="chartbound", chapter0="0.4% vs 3.4%",
            thumb=dict(v="flags", iso="POL", vs="FRA", sym="vs", big="87% → 100%?", line2="WHEN POLAND PASSES FRANCE"),
            w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks, datasets=[], snapshot=snapshot,
            voice=dict(model="", name="Charon",
                       style=("You are the narrator of a popular data documentary on YouTube. Read the script below in a warm, curious voice "
                              "with a little dry humor, at a relaxed but engaged pace of about 145 words per minute, like a smart friend telling "
                              "you something surprising. Let the big numbers land with a tiny pause before them. Keep the energy steady from the "
                              "first sentence to the last. Never sound like an advertisement or an audiobook.")),
            music=[dict(act=0, track="Lightless Dawn", vol=0.24), dict(act=1, track="Deliberate Thought", vol=0.22), dict(act=2, track="Hidden Agenda", vol=0.23), dict(act=3, track="Inspired", vol=0.23),
                   dict(act=4, track="Investigations", vol=0.23), dict(act=5, track="Deliberate Thought", vol=0.22), dict(act=6, track="Floating Cities", vol=0.24)],
            yt=dict(title="France Grew 0.4% This Year. Poland Is Closing In.",
                    description=("Income per person, adjusted for prices (IMF World Economic Outlook, October 2026): Poland was 34% of France in 1990, half in 2008, 70% in 2019 and 87% this year; "
                                 "the IMF has 90% in 2028 and 95% in 2031. France grows 0.4% this year in the IMF's estimate, Poland 3.4%. France and Britain are now almost exactly as rich per person, "
                                 "so Poland is catching both at the same speed. Plain dollars (Poland 61%), inflation, debt (118% vs 67%), unemployment (8.4% vs 3.2%), and two dates for parity: "
                                 "~2031 at the 2016–2026 pace, ~2034 at the IMF's pace.\n\n"
                                 "Sources: IMF World Economic Outlook, October 2026 (PPPPC, NGDPDPC, NGDP_RPCH, LP, LUR, GGXWDG_NGDP, PCPIPCH). Parity years are extrapolations, not IMF forecasts.\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#poland #france #economics #imf #europe #data"),
                    tags=["poland", "france", "poland vs france", "france economy", "poland economy", "gdp per capita", "imf", "economics", "europe", "data", "polska", "francja", "pologne"], lang="en"))

json.dump(spec, open(os.path.join(HERE, "a-L26.json"), "w"), ensure_ascii=False, indent=1)
clean = lambda t: t.replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()
words = sum(len(clean(s["narration"])) for s in shots)
acts = {}
for s in shots:
    acts[s["act"]] = acts.get(s["act"], 0) + len(clean(s["narration"]))
print("shots", len(shots), "palavras", words, f"~{words / 145:.1f} min a 145 wpm", "por ato", acts, "paridade", round(par_recent, 2), round(par_imf, 2))

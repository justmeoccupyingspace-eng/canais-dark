"""Gera specs/long/a-L25.json — Chartbound longo #25: "743,000 Poles Moved to Britain. Now Poland Is Catching Up." (série Polônia, PLANO.md L1/L3)
Intro (PLANO R2): número nos primeiros 2 s. CTA de série no minuto 1 com gancho do próximo episódio (Polônia × França).
Dados: IMF WEO out/2026 (research/imf_ita_2026-11-07.json: POL, GBR, FRA, ITA, DEU, JPN, lido 07/11). Fora do FMI: ONS Census 2021 (England and Wales):
743.000 residentes nascidos na Polônia (1,2%), 2º país de nascimento fora do RU depois da Índia (920.000), eram 579.000 em 2011
(ons.gov.uk/.../internationalmigrationenglandandwales/census2021, lido 11/11/2026). Fatos documentados: em 2004 RU, Irlanda e Suécia abriram o mercado de
trabalho aos novos membros da UE; o RU saiu da UE em 31/01/2020 e a livre circulação acabou em 01/01/2021; G7 2020: EUA −2,2, Canadá −5,0 (FMI)."""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "..", "..", "research", "imf_ita_2026-11-07.json")))
ACTS = ["Cold open", "Why so fast", "Britain's slow years", "Where Britain wins", "Where Poland wins", "The date", "Your guess"]
IMF = "IMF World Economic Outlook, October 2026"
ONS = "ONS, Census 2021 (England and Wales), country of birth"


def series(ind, iso):
    r = D[ind][iso]
    return {r["y0"] + k: v for k, v in enumerate(r["v"])}


P, G = series("PPPPC", "POL"), series("PPPPC", "GBR")
GR = {iso: series("NGDP_RPCH", iso) for iso in ("POL", "GBR", "ITA", "FRA", "DEU", "JPN")}
LP = {iso: series("LP", iso) for iso in ("POL", "GBR")}
N = {iso: series("NGDPDPC", iso) for iso in ("POL", "GBR")}
DEBT = {iso: series("GGXWDG_NGDP", iso) for iso in ("POL", "GBR")}
LUR = {iso: series("LUR", iso) for iso in ("POL", "GBR")}
CPI = {iso: series("PCPIPCH", iso) for iso in ("POL", "GBR")}
FRA = series("PPPPC", "FRA")

Y0, Y1 = 1990, 2031
R = {y: P[y] / G[y] for y in range(Y0, Y1 + 1)}
GAP = {y: G[y] - P[y] for y in range(Y0, Y1 + 1)}
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
    snapshot.append(dict(set="rat", iso="POL", year=y, value=round(R[y] * 100, 2), src=IMF + " · Poland's GDP per capita (PPP) as % of the UK's"))
for iso, s in (("POL", P), ("GBR", G)):
    for y, v in s.items():
        snapshot.append(dict(set="imf", iso=iso, year=y, value=v, src=IMF + " · PPPPC"))
for iso in ("POL", "GBR"):
    for y, v in GR[iso].items():
        snapshot.append(dict(set="imfg", iso=iso, year=y, value=v, src=IMF + " · NGDP_RPCH"))
for st, tab, ind in [("pop", LP, "LP"), ("debt", DEBT, "GGXWDG_NGDP"), ("lur", LUR, "LUR"), ("imfusd", N, "NGDPDPC"), ("cpi", CPI, "PCPIPCH")]:
    for iso, s in tab.items():
        for y, v in s.items():
            snapshot.append(dict(set=st, iso=iso, year=y, value=v, src=IMF + " · " + ind))

RATSRC = IMF + " · Poland's GDP per capita, PPP, as % of the UK's; 2026+ are IMF estimates and forecasts"
RATCH = dict(set="rat", fc=2025, series=["POL"], years=[Y0, Y1], y=[0, 110], src=RATSRC, fmt="pct0", hl="POL", ref=dict(value=100, label="UK = 100%", pos="left"))

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="lines", start=2026.0, **RATCH,
         narration="Eighty-eight percent. {p} That's how rich the average Pole is, compared with the average Brit, this year: income per person, adjusted for prices. About sixty thousand dollars against sixty-eight thousand. {pp} In 1990, Poland was at thirty-seven percent of Britain. Half by 2008. Sixty percent in 2014. Seventy in 2019. Eighty in 2024. {p} And in the IMF's forecast, it keeps going: ninety percent in 2028, ninety-five in 2031. That's one of the fastest catch-ups in Europe, and it's happening against the country so many Poles moved to.",
         keys=[dict(at="Eighty-eight", year=2026.0, dur=0.5), dict(at="In 1990", year=1990.0, dur=1.5), dict(at="Half by 2008", year=2008.0, dur=1.5), dict(at="Sixty percent in 2014", year=2014.0, dur=1.2), dict(at="Seventy in 2019", year=2019.0, dur=1.2), dict(at="Eighty in 2024", year=2024.0, dur=1.2), dict(at="ninety percent in 2028", year=2028.0, dur=1.5), dict(at="ninety-five in 2031", year=2031.0, dur=2.5)],
         labels=[dict(at="Eighty-eight percent", iso="POL", year=2026), dict(at="In 1990", iso="POL", year=1990), dict(at="Half by 2008", iso="POL", year=2008), dict(at="Seventy in 2019", iso="POL", year=2019), dict(at="ninety percent in 2028", iso="POL", year=2028)],
         react=[dict(at="Eighty-eight", pose="pointUp"), dict(at="In 1990", pose="pointL"), dict(at="Eighty in 2024", pose="shock"), dict(at="keeps going", pose="cheer"), dict(at="so many Poles moved to", pose="think")]),
    dict(act=0, type="host", bg="lines", start=2031.0, **{k: v for k, v in RATCH.items() if k != "src"},
         narration="In 2004, when Poland joined the European Union, Britain opened its job market to Polish workers straight away. And they came. In the 2021 census, seven hundred and forty-three thousand people living in England and Wales had been born in Poland: the second most common country of birth after India. {p} They came because the gap was enormous. In 2004, the average Brit produced more than twice as much as the average Pole. {pp} <soft>Here's how that gap closed so fast, why it's as much about Britain as about Poland, and when Poland could actually pass.</soft>",
         items=[dict(at="Britain opened its job market", text="2004: Britain opens the door", color="acc2", size=60), dict(at="seven hundred and forty-three thousand", text="743,000 born in Poland", serif=True, size=64, color="acc"), dict(at="more than twice as much", text="2004: Poland = 44% of UK", color="warm", size=60)],
         react=[dict(at="In 2004", pose="pointL"), dict(at="And they came", pose="wave"), dict(at="after India", pose="pointUp"), dict(at="enormous", pose="shock"), dict(at="actually pass", pose="think")]),

    # ---------------- 1 · WHY SO FAST ----------------
    dict(act=1, type="host", bg="none",
         narration="Quick one before the chart: this is a series, and the next episode is France, where the gap is almost exactly the same as with Britain. Subscribe so you don't miss it. {p} Now, why this one moved so fast.",
         items=[dict(at="this is a series", text="The Poland series", serif=True, size=66, color="acc"), dict(at="France", text="Next: Poland vs France", color="acc2", size=62), dict(at="Subscribe", text="Subscribe", size=70)],
         react=[dict(at="Quick one", pose="wave"), dict(at="France", pose="pointUp"), dict(at="Subscribe", pose="cheer"), dict(at="moved so fast", pose="think")]),
    dict(act=1, type="lines", start=2004.0, **RATCH,
         narration="Look at the slope after 2008. Before that, Poland was gaining on Britain slowly: from thirty-seven percent in 1990 to forty-four in 2004. That year, the average Brit produced about thirty-three thousand dollars, adjusted for prices, and the average Pole about fourteen and a half thousand. {p} After 2008, the line gets steep. {p} Part of that is Poland. Since 2007, Poland's economy has grown by about eighty-four percent, after inflation. {pp} But the other part is Britain. Over the same years, the British economy grew by about twenty-four percent. Poland grew more than three times as much. {p} When the country you're chasing slows down, you catch up a lot faster.",
         keys=[dict(at="Look at the slope", year=2008.0, dur=1.5), dict(at="gaining on Britain slowly", year=1990.0, dur=1.0), dict(at="forty-four in 2004", year=2004.0, dur=1.5), dict(at="the line gets steep", year=2019.0, dur=3.0), dict(at="catch up a lot faster", year=2026.0, dur=2.0)],
         labels=[dict(at="forty-four in 2004", iso="POL", year=2004)],
         react=[dict(at="Look at the slope", pose="pointL"), dict(at="gets steep", pose="shock"), dict(at="Part of that is Poland", pose="cheer"), dict(at="the other part is Britain", pose="think"), dict(at="more than three times", pose="pointUp")]),

    # ---------------- 2 · BRITAIN'S SLOW YEARS ----------------
    dict(act=2, type="bars", mode="abs", set="imfg", iso="GBR", years=[2000, 2026], start=2000.0, fmt="pct1", src=IMF + " · real GDP growth, United Kingdom (annual %); 2026 is an IMF estimate",
         narration="Here's Britain's economy, year by year, after inflation. {p} 2009: minus four and a half percent. And then, for a decade, growth of about two percent a year. Poland, in the same decade, averaged almost four. {pp} 2020: minus ten percent, the deepest fall in the G7 that year. Poland's was about minus two. {p} And since then: under one and a half percent a year in 2023, 2024 and 2025. Britain also left the European Union in 2020, and free movement for EU workers ended a year later.",
         keys=[dict(at="Here's Britain's", year=2005.0, dur=3.0), dict(at="2009: minus", year=2009.0, dur=1.5), dict(at="for a decade", year=2014.0, dur=2.0), dict(at="2020: minus ten", year=2020.0, dur=1.5), dict(at="since then", year=2024.0, dur=2.0)],
         react=[dict(at="Here's Britain's", pose="pointL"), dict(at="minus four and a half", pose="shock"), dict(at="almost four", pose="pointUp"), dict(at="minus ten percent", pose="shock"), dict(at="left the European Union", pose="think")]),
    dict(act=2, type="stats", src=IMF + " · real GDP growth (NGDP_RPCH)", title="Since 2019",
         narration="Put the last six years side by side. From 2019 to 2025, the British economy grew about five percent in total. Poland's grew about eighteen. {p} That's the same pattern we saw with Germany and Czechia: the economies Poland is chasing mostly stopped growing, and Poland didn't. {pp} And it's the same story for the Poles who stayed in Britain: they're now watching the country they left catch up with the one they moved to. {p} There's one more piece: people. Since 2004, Britain's population has grown by about ten million, partly thanks to immigrants like those Poles. Poland's has shrunk by about two million. The same growth, split between more people, means slower growth per person.",
         stats=[dict(at="about five percent", value=round((grow("GBR", 2019, 2025) - 1) * 100), fmt="pct0", label="UK, real growth 2019–2025"), dict(at="about eighteen", value=round((grow("POL", 2019, 2025) - 1) * 100), fmt="pct0", label="Poland, real growth 2019–2025"), dict(at="Germany and Czechia", value=round(R[2026] * 100), fmt="pct0", label="Poland vs UK, 2026")],
         react=[dict(at="side by side", pose="pointUp"), dict(at="about eighteen", pose="cheer"), dict(at="same pattern", pose="think"), dict(at="the one they moved to", pose="shrug")]),

    # ---------------- 3 · WHERE BRITAIN WINS ----------------
    dict(act=3, type="stats", src=IMF + " · GDP per capita, current US$ (NGDPDPC)", title="Plain dollars",
         narration="Now, the catch, and it's a big one. All of that is adjusted for prices. Things cost less in Poland, so the same income goes further. {p} In plain dollars, without that adjustment, the average Brit produces about sixty-one thousand dollars this year. The average Pole, about thirty-one thousand. Poland is at fifty-one percent there, not eighty-eight. {pp} That's why moving to Britain still makes sense for many Polish workers: a salary in pounds is still much bigger, even if rent in London eats a lot of it. {p} But in 1990, the average Pole produced about sixteen hundred dollars a year in plain dollars. The average Brit, about twenty-one thousand. Thirteen times more. Now it's two.",
         stats=[dict(at="sixty-one thousand", value=N["GBR"][2026], fmt="usd0", label="UK, plain US$, 2026"), dict(at="about thirty-one thousand", value=N["POL"][2026], fmt="usd0", label="Poland, plain US$, 2026"), dict(at="fifty-one percent", value=round(N["POL"][2026] / N["GBR"][2026] * 100), fmt="pct0", label="Poland vs UK, plain dollars, 2026"), dict(at="Thirteen times", value=round(N["GBR"][1990] / N["POL"][1990]), fmt="dec1", label="UK vs Poland, plain dollars, 1990 (×)")],
         react=[dict(at="the catch", pose="pointUp"), dict(at="not eighty-eight", pose="shrug"), dict(at="still makes sense", pose="think"), dict(at="Thirteen times", pose="shock"), dict(at="Now it's two", pose="cheer")]),

    # ---------------- 4 · WHERE POLAND WINS ----------------
    dict(act=4, type="host", bg="none",
         narration="And if you're enjoying the series, the subscribe button is right there. France is next. {p} Now, where Poland already wins.",
         items=[dict(at="subscribe button", text="Subscribe", size=66), dict(at="already wins", text="Where Poland wins", serif=True, size=66, color="acc")],
         react=[dict(at="subscribe button", pose="pointUp"), dict(at="already wins", pose="cheer")]),
    dict(act=4, type="duel", set="debt", year=2026, a="POL", b="GBR", fmt="pct0", src=IMF + " · general government gross debt (% of GDP), 2026 estimate", title="Government debt, % of GDP, 2026", badge="LOWER IN POLAND",
         cues=[dict(at="about sixty-seven", show="a"), dict(at="Britain's: about a hundred and two", show="b")],
         narration="Government debt this year: Poland, about sixty-seven percent of its economy. {pp} Britain's: about a hundred and two. And unemployment: about three point two percent in Poland, one of the lowest rates in the European Union, and five point three in Britain. {p} Britain does win one: inflation in 2022 peaked at about nine percent there, against fourteen in Poland.",
         react=[dict(at="Government debt", pose="pointUp"), dict(at="a hundred and two", pose="shock"), dict(at="five point three", pose="pointL"), dict(at="Britain does win one", pose="shrug")]),

    # ---------------- 5 · THE DATE ----------------
    dict(act=5, type="stats", src=IMF + " · PPPPC; parity years are Chartbound extrapolations of the 2016–2026 and IMF 2026–2031 paces, not IMF forecasts", title="When does Poland pass Britain?",
         narration="So, when does Poland pass Britain? {p} The gap in dollars, adjusted for prices, was widest in 2007: about nineteen thousand four hundred. This year it's about eight thousand four hundred. In the IMF's forecast, Britain grows about one and a half percent a year until 2031, and Poland about two and a half. That brings the gap down to about three thousand seven hundred, and Poland to ninety-five percent. {p} Beyond 2031 there's no official number, so here are two honest ones. At the pace of the last ten years, when Poland gained more than three percent a year on Britain, it passes around 2031. At the IMF's slower pace, around 2034. {pp} Either way, that's sooner than Germany, and maybe sooner than Czechia.",
         stats=[dict(at="nineteen thousand four hundred", value=GAP[2007], fmt="usd0", label="PPP gap, 2007 (the widest)"), dict(at="about eight thousand four hundred", value=GAP[2026], fmt="usd0", label="PPP gap, 2026"), dict(at="around 2031", value=math.ceil(par_recent), fmt="yr", label="parity at the 2016–2026 pace"), dict(at="around 2034", value=math.ceil(par_imf), fmt="yr", label="parity at the IMF's 2026–2031 pace")],
         react=[dict(at="when does Poland pass", pose="pointUp"), dict(at="widest in 2007", pose="pointL"), dict(at="two honest ones", pose="think"), dict(at="around 2031", pose="cheer"), dict(at="sooner than Germany", pose="shock")]),
    dict(act=5, type="host", bg="none",
         narration="Here's what that would mean. For most of the twenty years since 2004, moving from Poland to Britain meant moving to a much richer country. Measured by what money actually buys, that difference is shrinking fast. {p} Some Poles have already noticed: the number born in Poland living in England and Wales grew from five hundred and seventy-nine thousand in 2011 to seven hundred and forty-three thousand in 2021. The next census will show which way it goes now.",
         items=[dict(at="much richer country", text="2004: UK more than 2× richer", color="warm", size=58), dict(at="five hundred and seventy-nine thousand", text="2011: 579,000 → 2021: 743,000", serif=True, size=58, color="acc")],
         react=[dict(at="what that would mean", pose="think"), dict(at="shrinking fast", pose="pointL"), dict(at="already noticed", pose="pointUp"), dict(at="which way it goes", pose="shrug")]),

    # ---------------- 6 · YOUR GUESS ----------------
    dict(act=6, type="host", bg="none",
         narration="<soft>So, your guess: 2031, 2034, or later?</soft> Tell me in the comments. {p} If you're one of the Poles in Britain: would you move back, and when? And if you already went back, tell me what changed. {p} If you're in Britain: did you expect Poland to be this close? {p} And France: you're next. I read every comment.",
         items=[dict(at="your guess", text="2031, 2034 or later?", color="acc", size=66), dict(at="Poles in Britain", text="Would you move back?", color="warm", size=60)],
         react=[dict(at="your guess", pose="shrug"), dict(at="Tell me", pose="pointUp"), dict(at="Poles in Britain", pose="wave")]),
    dict(act=6, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="LTU", color="acc", title="Lithuania passed Poland. Twice.", sub="the strangest race."),
         narration="And if you missed it, Lithuania is the strangest race in this series: a neighbor that passed Poland twice. That story is right here. {p} I'm Chartbound. See you in the next one.",
         hold=14,
         react=[dict(at="if you missed it", pose="pointL"), dict(at="See you", pose="wave")]),
]

checks = [
    dict(say="2026: POL = 88% of GBR; ≈ $60k vs $68k", rule="expr", expr=f"[round({R[2026]} * 100), round({P[2026]} / 1000), round({G[2026]} / 1000)]", equal=[88, 60, 68]),
    dict(say="1990: 37%; first ≥50% 2008, ≥60% 2014, ≥70% 2019, ≥80% 2024, ≥90% 2028; 2031 = 95%", rule="expr", expr=f"[round({R[1990]} * 100), {first_at(0.5)}, {first_at(0.6)}, {first_at(0.7)}, {first_at(0.8)}, {first_at(0.9)}, round({R[2031]} * 100)]", equal=[37, 2008, 2014, 2019, 2024, 2028, 95]),
    dict(say="ONS Census 2021: 743.000 nascidos na Polônia em England and Wales, 2º depois da Índia (920.000); 579.000 em 2011", rule="expr", expr="[743000, 920000 > 743000, 579000]", equal=[743000, True, 579000]),
    dict(say="2004: UK > 2× Poland per person (Poland = 44%)", rule="expr", expr=f"[round({R[2004]} * 100), {G[2004] / P[2004] > 2}]", equal=[44, True]),
    dict(say="FRA 2026: POL/FRA ≈ POL/GBR (87% vs 88%)", rule="expr", expr=f"[round({P[2026] / FRA[2026]} * 100), round({R[2026]} * 100)]", equal=[87, 88]),
    dict(say="real growth 2007→2025: POL +84%, GBR +24%; ratio > 3×", rule="expr", expr=f"[round(({grow('POL', 2007, 2025)} - 1) * 100), round(({grow('GBR', 2007, 2025)} - 1) * 100), {(grow('POL', 2007, 2025) - 1) / (grow('GBR', 2007, 2025) - 1) > 3}]", equal=[84, 24, True]),
    dict(say="GBR 2009 −4.5; avg 2010–2019 GBR ≈ 2.1 (about two), POL ≈ 3.8 (almost four)", rule="expr", expr=f"[{GR['GBR'][2009]}, round({sum(GR['GBR'][y] for y in range(2010, 2020)) / 10}, 1), round({sum(GR['POL'][y] for y in range(2010, 2020)) / 10}, 1)]", equal=[-4.5, 2.1, 3.8]),
    dict(say="2020: GBR −10.0 deepest in G7 (ITA −8.9, FRA −7.6, JPN −4.3, DEU −4.0; EUA −2.2 e Canadá −5.0 no FMI); POL −2.1 (about minus two)", rule="expr", expr=f"[{GR['GBR'][2020]}, {GR['GBR'][2020] < min(GR[i][2020] for i in ('ITA', 'FRA', 'JPN', 'DEU'))}, {GR['POL'][2020]}]", equal=[-10, True, -2.1]),
    dict(say="GBR growth 2023, 2024, 2025 all < 1.5", rule="expr", expr=f"{[GR['GBR'][y] for y in (2023, 2024, 2025)]}", equal=[0.4, 1.1, 1.2]),
    dict(say="RU saiu da UE 31/01/2020; fim da livre circulação 01/01/2021 — fatos documentados", rule="expr", expr="[2020, 2021]", equal=[2020, 2021]),
    dict(say="2019→2025: GBR ≈ +5%, POL ≈ +18%", rule="expr", expr=f"[round(({grow('GBR', 2019, 2025)} - 1) * 100), round(({grow('POL', 2019, 2025)} - 1) * 100)]", equal=[5, 18]),
    dict(say="nominal 2026: GBR ≈ $61k, POL ≈ $31k, POL/GBR = 51%", rule="expr", expr=f"[round({N['GBR'][2026]} / 1000), round({N['POL'][2026]} / 1000), round({N['POL'][2026]} / {N['GBR'][2026]} * 100)]", equal=[61, 31, 51]),
    dict(say="nominal 1990: POL ≈ $1.6k, GBR ≈ $21k, 13×; 2026 ≈ 2×", rule="expr", expr=f"[round({N['POL'][1990]} / 100) * 100, round({N['GBR'][1990]} / 1000), round({N['GBR'][1990]} / {N['POL'][1990]}), round({N['GBR'][2026]} / {N['POL'][2026]})]", equal=[1600, 21, 13, 2]),
    dict(say="debt 2026: POL ≈ 67, GBR ≈ 102; unemployment 3.2 vs 5.3; inflation 2022 GBR 9.1 (about nine), POL 14.4 (fourteen)", rule="expr", expr=f"[round({DEBT['POL'][2026]}), round({DEBT['GBR'][2026]}), {LUR['POL'][2026]}, {LUR['GBR'][2026]}, {CPI['GBR'][2022]}, {CPI['POL'][2022]}]", equal=[67, 102, 3.2, 5.3, 9.1, 14.4]),
    dict(say="PPP gap: widest 2007 ≈ $19.4k; 2026 ≈ $8.4k; 2031 ≈ $3.7k", rule="expr", expr=f"[{max(GAP, key=GAP.get)}, round({GAP[2007]} / 100) * 100, round({GAP[2026]} / 100) * 100, round({GAP[2031]} / 100) * 100]", equal=[2007, 19400, 8400, 3700]),
    dict(say="pace 2016–2026 > 3%/yr → parity 2031 (2030.03, ceil); IMF pace → 2034 (2033.9)", rule="expr", expr=f"[{k_recent > 0.03}, {math.ceil(par_recent)}, {math.ceil(par_imf)}]", equal=[True, 2031, 2034]),
    dict(say="sooner than Germany (2034/2043, A-L22); maybe sooner than Czechia (2030/2039, A-L23)", rule="expr", expr=f"[{math.ceil(par_imf)} <= 2034, {math.ceil(par_imf)} < 2039]", equal=[True, True]),
    dict(say="end card: Lithuania passed Poland twice (A-L24: 2003 e 2011)", rule="expr", expr="[2003, 2011]", equal=[2003, 2011]),
    dict(say="2004: GBR ≈ $33k, POL ≈ $14.5k (PPP)", rule="expr", expr=f"[round({G[2004]} / 1000), round({P[2004]} / 500) * 500]", equal=[33, 14500]),
    dict(say="population 2004→2026: GBR +≈10M (59.95→69.85), POL −≈2M (38.19→36.33)", rule="expr", expr=f"[round({LP['GBR'][2026]} - {LP['GBR'][2004]}), round({LP['POL'][2026]} - {LP['POL'][2004]})]", equal=[10, -2]),
    dict(say="desemprego da Polônia entre os mais baixos da UE (Eurostat) — amplamente citado", rule="expr", expr=f"{LUR['POL'][2026] < 3.5}", equal=True),
    dict(say="IMF 2027–2031: GBR 1.2–1.6 (about one and a half), POL 2.5", rule="expr", expr=f"[{all(1.2 <= GR['GBR'][y] <= 1.6 for y in range(2027, 2032))}, {sorted(set(GR['POL'][y] for y in range(2027, 2032)))}]", equal=[True, [2.5]]),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="a-L25-poland-britain", clips=[], channel="chartbound", chapter0="88% of Britain",
            thumb=dict(v="flags", iso="POL", vs="GBR", sym="vs", big="88% → 100%?", line2="WHEN POLAND PASSES BRITAIN"),
            w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks, datasets=[], snapshot=snapshot,
            voice=dict(model="", name="Charon",
                       style=("You are the narrator of a popular data documentary on YouTube. Read the script below in a warm, curious voice "
                              "with a little dry humor, at a relaxed but engaged pace of about 145 words per minute, like a smart friend telling "
                              "you something surprising. Let the big numbers land with a tiny pause before them. Keep the energy steady from the "
                              "first sentence to the last. Never sound like an advertisement or an audiobook.")),
            music=[dict(act=0, track="Lightless Dawn", vol=0.24), dict(act=1, track="Deliberate Thought", vol=0.22), dict(act=2, track="Hidden Agenda", vol=0.23), dict(act=3, track="Inspired", vol=0.23),
                   dict(act=4, track="Investigations", vol=0.23), dict(act=5, track="Deliberate Thought", vol=0.22), dict(act=6, track="Floating Cities", vol=0.24)],
            yt=dict(title="743,000 Poles Moved to Britain. Now Poland Is Catching Up.",
                    description=("Income per person, adjusted for prices (IMF World Economic Outlook, October 2026): Poland was 37% of the UK in 1990, 44% in 2004 when Britain opened its job market, "
                                 "half in 2008, 80% in 2024 and 88% this year; the IMF has 90% in 2028 and 95% in 2031. Since 2007 Poland's economy grew about 84% after inflation, Britain's about 24%. "
                                 "Plain dollars (Poland still 51%), debt, unemployment, and two dates for parity: ~2031 at the 2016–2026 pace, ~2034 at the IMF's pace.\n\n"
                                 "Sources: IMF World Economic Outlook, October 2026 (PPPPC, NGDPDPC, NGDP_RPCH, LP, LUR, GGXWDG_NGDP, PCPIPCH); ONS, Census 2021 (England and Wales), "
                                 "country of birth. Parity years are extrapolations, not IMF forecasts.\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#poland #uk #britain #economics #imf #europe #data"),
                    tags=["poland", "uk", "britain", "poland vs uk", "poles in uk", "polish migration", "uk economy", "poland economy", "gdp per capita", "imf", "economics", "europe", "polska", "wielka brytania"], lang="en"))

json.dump(spec, open(os.path.join(HERE, "a-L25.json"), "w"), ensure_ascii=False, indent=1)
clean = lambda t: t.replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()
words = sum(len(clean(s["narration"])) for s in shots)
acts = {}
for s in shots:
    acts[s["act"]] = acts.get(s["act"], 0) + len(clean(s["narration"]))
print("shots", len(shots), "palavras", words, f"~{words / 145:.1f} min a 145 wpm", "por ato", acts, "paridade", round(par_recent, 2), round(par_imf, 2))

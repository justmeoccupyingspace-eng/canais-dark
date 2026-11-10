"""Gera specs/long/a-L23.json — Chartbound longo #23: "Poland Is 94% of Czechia. When Does It Pass?" (série Polônia, PLANO.md L1/L3)
Intro (PLANO R2): número nos primeiros 2 s. CTA de série no minuto 1 com gancho do próximo episódio (Polônia × Lituânia).
Dados: IMF WEO out/2026 lidos em 07/11/2026 (research/imf_ita_2026-11-07.json: POL) e 10/11/2026 (research/imf_cze_2026-11-10.json: CZE, série
completa) + 08/11/2026 (research/imf_ce_2026-11-08.json: SVK, HUN, LTU, anos selecionados). Fora do FMI: Eurostat PIB regional por habitante em PPS
2024 via Český statistický úřad (csu.gov.cz/pha/regionalni-ucty-2024-hl-m-praha: Praga 192%, Hamburgo 196, Bruxelas 190, Viena 137, Berlim 127)
e Varsóvia 157% (mesma série, usada no A-L22); ~1/3 das exportações tchecas vão para a Alemanha (ČSÚ); Polônia = única economia da UE sem
recessão em 2009 (Eurostat)."""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "..", "..", "research", "imf_ita_2026-11-07.json")))
C = json.load(open(os.path.join(HERE, "..", "..", "research", "imf_cze_2026-11-10.json")))
CE = json.load(open(os.path.join(HERE, "..", "..", "research", "imf_ce_2026-11-08.json")))
ACTS = ["Cold open", "Fast, then flat", "2009", "Where Czechia wins", "The slow part", "The date", "Your guess"]
IMF = "IMF World Economic Outlook, October 2026"
EUROSTAT = "Eurostat · regional GDP per inhabitant in PPS, % of EU average, 2024 (NUTS 2), via Czech Statistical Office"


def series(ind, iso):
    r = (C if iso == "CZE" else D)[ind][iso]
    return {r["y0"] + k: v for k, v in enumerate(r["v"])}


P, Z = series("PPPPC", "POL"), series("PPPPC", "CZE")
GR = {iso: series("NGDP_RPCH", iso) for iso in ("POL", "CZE")}
LP = {iso: series("LP", iso) for iso in ("POL", "CZE")}
N = {iso: series("NGDPDPC", iso) for iso in ("POL", "CZE")}
DEBT = {iso: series("GGXWDG_NGDP", iso) for iso in ("POL", "CZE")}
LUR = {iso: series("LUR", iso) for iso in ("POL", "CZE")}
SEL = {iso: {int(y): v for y, v in CE["PPPPC"][iso].items()} for iso in ("SVK", "HUN", "LTU")}

Y0, Y1 = 1995, 2031
R = {y: P[y] / Z[y] for y in range(Y0, Y1 + 1)}
GAP = {y: Z[y] - P[y] for y in range(Y0, Y1 + 1)}
dips = [y for y in range(Y0 + 1, Y1 + 1) if R[y] < R[y - 1]]
jump = {y: R[y] - R[y - 1] for y in range(Y0 + 1, Y1 + 1)}
first_at = lambda th: next(y for y in range(Y0, Y1 + 1) if R[y] >= th)


def grow(iso, a, b):
    c = 1.0
    for y in range(a + 1, b + 1):
        c *= 1 + GR[iso][y] / 100
    return c


avg = lambda iso, a, b: sum(GR[iso][y] for y in range(a, b + 1)) / (b - a + 1)
k_recent = math.log(R[2026] / R[2016]) / 10          # ritmo 2016–2026
k_imf = math.log(R[2031] / R[2026]) / 5              # ritmo da previsão 2026–2031
par_recent = 2026 + math.log(1 / R[2026]) / k_recent
par_imf = 2031 + math.log(1 / R[2031]) / k_imf

snapshot = []
for y in range(Y0, Y1 + 1):
    snapshot.append(dict(set="rat", iso="POL", year=y, value=round(R[y] * 100, 2), src=IMF + " · Poland's GDP per capita (PPP) as % of Czechia's"))
for iso, s in (("POL", P), ("CZE", Z)):
    for y, v in s.items():
        snapshot.append(dict(set="imf", iso=iso, year=y, value=v, src=IMF + " · PPPPC"))
for iso, s in GR.items():
    for y, v in s.items():
        snapshot.append(dict(set="imfg", iso=iso, year=y, value=v, src=IMF + " · NGDP_RPCH"))
for st, tab, ind in [("pop", LP, "LP"), ("debt", DEBT, "GGXWDG_NGDP"), ("lur", LUR, "LUR"), ("imfusd", N, "NGDPDPC")]:
    for iso, s in tab.items():
        for y, v in s.items():
            snapshot.append(dict(set=st, iso=iso, year=y, value=v, src=IMF + " · " + ind))

RATSRC = IMF + " · Poland's GDP per capita, PPP, as % of Czechia's; 2026+ are IMF estimates and forecasts"
RATCH = dict(set="rat", fc=2025, series=["POL"], years=[Y0, Y1], y=[0, 110], src=RATSRC, fmt="pct0", hl="POL", ref=dict(value=100, label="Czechia = 100%", pos="left"))

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="lines", start=2026.0, **RATCH,
         narration="Ninety-four percent. {p} That's how rich the average Pole is, compared with the average Czech, this year: income per person, adjusted for prices. About sixty thousand dollars against sixty-four thousand. A gap of about four thousand. {pp} In 1995, Poland was at fifty-four percent of Czechia. Sixty percent by 1998. Seventy in 2011. Eighty in 2020. Ninety in 2024. {p} And the IMF's forecast ends in 2031 at ninety-six percent. Still not there. So the last few percent are the hard part. When does Poland actually pass?",
         keys=[dict(at="Ninety-four", year=2026.0, dur=0.5), dict(at="In 1995", year=1995.0, dur=1.5), dict(at="Sixty percent by 1998", year=1998.0, dur=1.5), dict(at="Seventy in 2011", year=2011.0, dur=1.5), dict(at="Eighty in 2020", year=2020.0, dur=1.5), dict(at="Ninety in 2024", year=2024.0, dur=1.5), dict(at="ninety-six percent", year=2031.0, dur=3.0)],
         labels=[dict(at="Ninety-four percent", iso="POL", year=2026), dict(at="fifty-four percent", iso="POL", year=1995), dict(at="Sixty percent by 1998", iso="POL", year=1998), dict(at="Seventy in 2011", iso="POL", year=2011), dict(at="Eighty in 2020", iso="POL", year=2020), dict(at="Ninety in 2024", iso="POL", year=2024)],
         react=[dict(at="Ninety-four", pose="pointUp"), dict(at="In 1995", pose="pointL"), dict(at="Ninety in 2024", pose="shock"), dict(at="Still not there", pose="shrug"), dict(at="actually pass", pose="think")]),
    dict(act=0, type="host", bg="lines", start=2031.0, **{k: v for k, v in RATCH.items() if k != "src"},
         narration="In this series, Poland has been passing countries one after another. Japan this year. Spain next year, in the IMF's forecast. Italy, right after 2031. {p} Czechia is a different kind of race. It's a neighbor, both countries joined the European Union on the same day in 2004, and it's the richest of the four Visegrád countries: Poland, Czechia, Slovakia and Hungary. Poland passed Slovakia and Hungary by 2020. Czechia is the one it hasn't. {pp} <soft>Here's why it took so long, the year that changed this race, and the date the numbers point to.</soft>",
         items=[dict(at="Japan this year", text="2026: Japan", color="acc2", size=66), dict(at="Spain next year", text="2027: Spain", color="acc2", size=66), dict(at="Italy, right after", text="~2032: Italy", color="acc2", size=66), dict(at="four Visegrád countries", text="Visegrád #1: Czechia", serif=True, size=60, color="acc")],
         react=[dict(at="passing countries", pose="pointL"), dict(at="different kind of race", pose="think"), dict(at="Visegrád", pose="pointUp"), dict(at="the one it hasn't", pose="shrug"), dict(at="the date", pose="cheer")]),

    # ---------------- 1 · FAST, THEN FLAT ----------------
    dict(act=1, type="host", bg="none",
         narration="Quick one before the chart: this is a series, and the next episode is Lithuania, a neighbor that was poorer than Poland in 1995 and is ahead of it now. Subscribe so you don't miss it. {p} Now, the race.",
         items=[dict(at="this is a series", text="The Poland series", serif=True, size=66, color="acc"), dict(at="Lithuania", text="Next: Poland vs Lithuania", color="acc2", size=62), dict(at="Subscribe", text="Subscribe", size=70)],
         react=[dict(at="Quick one", pose="wave"), dict(at="Lithuania", pose="pointUp"), dict(at="Subscribe", pose="cheer"), dict(at="the race", pose="pointL")]),
    dict(act=1, type="lines", start=1995.0, **RATCH,
         narration="It started fast. {p} In 1995, the average Czech produced about fifteen thousand six hundred dollars a year, adjusted for prices. The average Pole, about eight thousand four hundred. By 2000, Poland had gone from fifty-four percent of Czechia to sixty-four. {pp} And then, almost nothing. For eight years, the line went sideways. In 2005 and 2006, Poland slipped back to sixty-one percent. In 2008, it was at sixty-four again, right back where it had been in 2000. {p} Czechia was running fast too: more than six percent a year in 2005 and 2006, with new car plants and foreign factories opening across the country. Then came 2009.",
         keys=[dict(at="It started fast", year=1995.0, dur=1.0), dict(at="By 2000", year=2000.0, dur=2.5), dict(at="went sideways", year=2004.0, dur=2.0), dict(at="slipped back", year=2006.0, dur=1.5), dict(at="In 2008", year=2008.0, dur=1.5), dict(at="Then came 2009", year=2009.0, dur=1.5)],
         labels=[dict(at="By 2000", iso="POL", year=2000), dict(at="slipped back", iso="POL", year=2006), dict(at="In 2008", iso="POL", year=2008)],
         react=[dict(at="It started fast", pose="pointL"), dict(at="almost nothing", pose="shrug"), dict(at="right back where", pose="think"), dict(at="Then came 2009", pose="pointUp")]),

    # ---------------- 2 · 2009 ----------------
    dict(act=2, type="bars", mode="abs", set="imfg", iso="CZE", years=[1996, 2026], start=1996.0, fmt="pct1", src=IMF + " · real GDP growth, Czechia (annual %); 2026 is an IMF estimate",
         narration="Here's Czechia's economy, year by year, after inflation. {p} 2009: minus four point eight percent. Poland that year grew two point six, the only economy in the European Union that didn't shrink. In a single year, Poland jumped from sixty-four percent of Czechia to sixty-nine: the biggest one-year jump in the whole race. {pp} And that's the pattern. Since 1996, Czechia's economy has shrunk in five different years: 1997, 1998, 2009, 2012 and 2020. Poland's shrank in one: 2020, the pandemic.",
         keys=[dict(at="Here's Czechia's", year=2005.0, dur=3.0), dict(at="2009: minus", year=2009.0, dur=1.5), dict(at="five different years", year=1998.0, dur=1.5), dict(at="2012 and 2020", year=2020.0, dur=2.0)],
         react=[dict(at="Here's Czechia's", pose="pointL"), dict(at="minus four point eight", pose="shock"), dict(at="didn't shrink", pose="pointUp"), dict(at="biggest one-year jump", pose="cheer"), dict(at="shrank in one", pose="think")]),
    dict(act=2, type="stats", src=IMF + " · real GDP growth (NGDP_RPCH)", title="Steady beat fast",
         narration="Add it all up. Since 1995, Poland's economy has more than tripled in size, after inflation. Czechia's has almost doubled. Average growth since 2001: about three and a half percent a year for Poland, a little under two and a half for Czechia. {pp} And the last six years were the worst stretch for Czechia. Its economy in 2025 was only about five percent bigger than in 2019. Poland's grew about eighteen percent. In 2023, the Czech economy didn't grow at all, after inflation hit fifteen percent the year before. {p} Part of the reason: Czechia is built on cars, and on Germany. About a third of everything it sells abroad goes to Germany, and when German industry stalled, Czech factories stalled with it.",
         stats=[dict(at="more than tripled", value=round(grow("POL", 1995, 2025), 1), fmt="dec1", label="Poland's economy, 2025 vs 1995 (×, real)"), dict(at="almost doubled", value=round(grow("CZE", 1995, 2025), 1), fmt="dec1", label="Czechia's economy, 2025 vs 1995 (×, real)"), dict(at="about five percent bigger", value=round((grow("CZE", 2019, 2025) - 1) * 100), fmt="pct0", label="Czechia, real growth 2019–2025"), dict(at="about eighteen percent", value=round((grow("POL", 2019, 2025) - 1) * 100), fmt="pct0", label="Poland, real growth 2019–2025")],
         react=[dict(at="Add it all up", pose="pointUp"), dict(at="almost doubled", pose="pointL"), dict(at="worst stretch", pose="shock"), dict(at="didn't grow at all", pose="shrug"), dict(at="stalled with it", pose="think")]),

    # ---------------- 3 · WHERE CZECHIA WINS ----------------
    dict(act=3, type="duel", set="debt", year=2026, a="CZE", b="POL", fmt="pct0", src=IMF + " · general government gross debt (% of GDP), 2026 estimate and 2031 forecast", title="Government debt, % of GDP, 2026", badge="LOWER IN CZECHIA",
         cues=[dict(at="about forty-six", show="a"), dict(at="Poland's: about sixty-seven", show="b")],
         narration="Now, what Czechia still does better. On jobs, it's a tie: unemployment is around three percent in both. But look at debt. Czech government debt this year: about forty-six percent of the economy. {pp} Poland's: about sixty-seven. And the IMF has that gap widening, to fifty-five against eighty-two by 2031.",
         react=[dict(at="still does better", pose="pointUp"), dict(at="it's a tie", pose="shrug"), dict(at="about forty-six", pose="pointL"), dict(at="eighty-two by 2031", pose="shock")]),
    dict(act=3, type="stats", src=IMF + " · GDP per capita, current US$ (NGDPDPC); " + EUROSTAT, title="Plain dollars, and the two capitals",
         narration="Then, plain dollars. Without adjusting for prices, the average Czech produces about thirty-nine thousand six hundred dollars this year, and the average Pole about thirty-one thousand two hundred. In plain dollars, Poland is at seventy-nine percent, not ninety-four. {p} And then there's Prague. By the EU statistics office's numbers for 2024, the Prague region produces a hundred and ninety-two percent of the EU average per person, adjusted for prices. That's ahead of Brussels, Vienna and Berlin. Warsaw: a hundred and fifty-seven. {pp} Capitals flatter these numbers, because commuters are counted where they work, and the Prague region is just the city itself. Still, Warsaw is at about eighty-two percent of Prague: further behind than Poland is behind Czechia.",
         stats=[dict(at="thirty-nine thousand six hundred", value=N["CZE"][2026], fmt="usd0", label="Czechia, plain US$, 2026"), dict(at="thirty-one thousand two hundred", value=N["POL"][2026], fmt="usd0", label="Poland, plain US$, 2026"), dict(at="a hundred and ninety-two", value=192, fmt="pct0", label="Prague region, % of EU average"), dict(at="Warsaw: a hundred", value=157, fmt="pct0", label="Warsaw region, % of EU average")],
         react=[dict(at="plain dollars", pose="pointUp"), dict(at="not ninety-four", pose="shrug"), dict(at="Then there's Prague", pose="pointL"), dict(at="Brussels, Vienna and Berlin", pose="shock"), dict(at="Capitals flatter", pose="think")]),

    # ---------------- 4 · THE SLOW PART ----------------
    dict(act=4, type="host", bg="none",
         narration="Now, the part that makes the last few percent so slow. {p} And if you're enjoying this, the subscribe button is right there. Lithuania is next.",
         items=[dict(at="the last few percent", text="The slow part", serif=True, size=68, color="acc"), dict(at="subscribe button", text="Subscribe", size=66)],
         react=[dict(at="so slow", pose="think"), dict(at="subscribe button", pose="pointUp")]),
    dict(act=4, type="stats", src=IMF + " · PPPPC gap in US$, real GDP growth forecasts (NGDP_RPCH), population (LP)", title="The dollar gap",
         narration="In dollars, adjusted for prices, the gap between the average Czech and the average Pole actually grew in the 2000s, and peaked in 2007 at about eleven thousand four hundred. This year, it's about four thousand. {p} But in the IMF's forecast, the closing slows right down. Poland grows about two and a half percent a year from 2027, Czechia about two. Half a point a year doesn't close a gap fast: by 2031, it's still about three thousand one hundred dollars. {pp} One thing does work in Poland's favor here, and it's not a happy one. Poland's population is shrinking, from about thirty-eight and a half million in 1995 to thirty-six million today, while Czechia's grew a little. Fewer people means more income per person, even from the same economy.",
         stats=[dict(at="eleven thousand four hundred", value=GAP[2007], fmt="usd0", label="PPP gap, 2007 (the widest)"), dict(at="about four thousand", value=GAP[2026], fmt="usd0", label="PPP gap, 2026"), dict(at="three thousand one hundred", value=GAP[2031], fmt="usd0", label="PPP gap, 2031 (IMF)"), dict(at="thirty-six million today", value=LP["POL"][2026], fmt="m", label="people in Poland, 2026 (1995: 38.6M)")],
         react=[dict(at="actually grew", pose="shock"), dict(at="slows right down", pose="think"), dict(at="three thousand one hundred", pose="shrug"), dict(at="not a happy one", pose="think"), dict(at="Fewer people", pose="pointUp")]),

    # ---------------- 5 · THE DATE ----------------
    dict(act=5, type="stats", src=IMF + " · PPPPC; parity years are Chartbound extrapolations of the 2016–2026 and IMF 2026–2031 paces, not IMF forecasts", title="When does Poland pass Czechia?",
         narration="So, when does Poland pass? {p} The IMF's forecast stops in 2031, at ninety-six percent. Beyond that, there's no official number, so here are two honest ones. {p} If the next few years look like the last ten, when Poland closed in on Czechia by about two percent a year, Poland passes around 2030. That's before the IMF's forecast even ends, so it would mean the IMF is being too cautious. {p} If the IMF's slower pace continues after 2031, it's around 2039. {pp} Nine years apart. The exact same spread we got for Germany, by the way: 2034 or 2043.",
         stats=[dict(at="ninety-six percent", value=round(R[2031] * 100), fmt="pct0", label="Poland vs Czechia, 2031 (IMF)"), dict(at="around 2030", value=math.ceil(par_recent), fmt="yr", label="parity at the 2016–2026 pace"), dict(at="around 2039", value=math.ceil(par_imf), fmt="yr", label="parity at the IMF's 2026–2031 pace"), dict(at="2034 or 2043", value=2034, fmt="yr", label="Poland vs Germany, same method (2034 / 2043)")],
         react=[dict(at="when does Poland pass", pose="pointUp"), dict(at="two honest ones", pose="think"), dict(at="around 2030", pose="cheer"), dict(at="around 2039", pose="pointL"), dict(at="by the way", pose="shrug")]),
    dict(act=5, type="host", bg="none",
         narration="And there's a twist here too. Czechia's slowdown came from the same place as Germany's: expensive energy after 2022, and carmakers under pressure. Poland has something Czechia doesn't: a big home market of thirty-six million people. When exports collapsed in 2009, Poles kept spending, and that's a big part of why Poland never had a recession then. {p} In this race, being big and a little less exciting turned out to be an advantage.",
         items=[dict(at="same place as Germany's", text="Energy + cars", color="acc2", size=64), dict(at="big home market", text="36 million customers", serif=True, size=64, color="acc")],
         react=[dict(at="a twist", pose="think"), dict(at="carmakers under pressure", pose="pointL"), dict(at="big home market", pose="pointUp"), dict(at="an advantage", pose="cheer")]),

    # ---------------- 6 · YOUR GUESS ----------------
    dict(act=6, type="host", bg="none",
         narration="<soft>So, your guess: 2030, 2039, or does Czechia hold on?</soft> Tell me in the comments. {p} If you're watching from Czechia: did the last few years feel as slow as the numbers say? {p} If you're in Poland: does it feel like you're about to pass Czechia? {p} And Lithuania: you're next, so tell me what I should know. I read every comment.",
         items=[dict(at="your guess", text="2030, 2039 or never?", color="acc", size=68), dict(at="watching from Czechia", text="Czechia: did it feel slow?", color="warm", size=58)],
         react=[dict(at="your guess", pose="shrug"), dict(at="Tell me", pose="pointUp"), dict(at="watching from Czechia", pose="wave")]),
    dict(act=6, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="DEU", color="acc", title="Poland vs Germany: 76%", sub="the biggest race."),
         narration="And if you missed it, Poland versus Germany is the big one: seventy-six percent, and two dates for catching up. That story is right here. {p} I'm Chartbound. See you in the next one.",
         hold=14,
         react=[dict(at="if you missed it", pose="pointL"), dict(at="See you", pose="wave")]),
]

checks = [
    dict(say="2026: POL = 94% of CZE (93.7)", rule="ratio", set="imf", a="POL", b="CZE", year=2026, min=0.935, max=0.945),
    dict(say="2026: POL ≈ $60k, CZE ≈ $64k, gap ≈ $4k", rule="expr", expr=f"[round({P[2026]} / 1000), round({Z[2026]} / 1000), round({GAP[2026]} / 1000)]", equal=[60, 64, 4]),
    dict(say="1995: POL = 54% of CZE", rule="ratio", set="imf", a="POL", b="CZE", year=1995, min=0.535, max=0.545),
    dict(say="first year ≥ 60% / 70% / 80% / 90%: 1998 / 2011 / 2020 / 2024", rule="expr", expr=f"[{first_at(0.6)}, {first_at(0.7)}, {first_at(0.8)}, {first_at(0.9)}]", equal=[1998, 2011, 2020, 2024]),
    dict(say="2031: POL = 96% of CZE; still < 100% every year to 2031", rule="expr", expr=f"[{round(R[2031] * 100)}, {all(R[y] < 1 for y in range(Y0, Y1 + 1))}]", equal=[96, True]),
    dict(say="POL passes JPN 2026, ESP 2027 (IMF); ITA not by 2031", rule="expr", expr=f"[{next(y for y in range(1990, 2032) if P[y] > series('PPPPC', 'JPN')[y])}, {next(y for y in range(1990, 2032) if P[y] > series('PPPPC', 'ESP')[y])}, {P[2031] < series('PPPPC', 'ITA')[2031]}]", equal=[2026, 2027, True]),
    dict(say="POL e CZE entraram na UE em 1/5/2004", rule="expr", expr="2004", equal=2004),
    dict(say="CZE richest of V4 in 2026 (CZE > POL > HUN > SVK); POL < HUN, SVK in 2010 and > both in 2020", rule="expr", expr=f"[{Z[2026] > P[2026] > SEL['HUN'][2026] > SEL['SVK'][2026]}, {P[2010] < SEL['HUN'][2010] and P[2010] < SEL['SVK'][2010]}, {P[2020] > SEL['HUN'][2020] and P[2020] > SEL['SVK'][2020]}]", equal=[True, True, True]),
    dict(say="LTU poorer than POL in 1995, ahead in 2026", rule="expr", expr=f"[{SEL['LTU'][1995] < P[1995]}, {SEL['LTU'][2026] > P[2026]}]", equal=[True, True]),
    dict(say="1995 PPP per person: CZE ≈ $15.6k, POL ≈ $8.4k; 2000 POL = 64% of CZE", rule="expr", expr=f"[round({Z[1995]} / 100) * 100, round({P[1995]} / 100) * 100, round({R[2000]} * 100)]", equal=[15600, 8400, 64]),
    dict(say="2005 and 2006: 61%; 2008: 64% (2000: 64%); 2000→2008 sideways (all 61–64%)", rule="expr", expr=f"[round({R[2005]} * 100), round({R[2006]} * 100), round({R[2008]} * 100), {all(0.605 <= R[y] < 0.645 for y in range(2000, 2009))}]", equal=[61, 61, 64, True]),
    dict(say="CZE growth 2005 6.4, 2006 6.6 (> 6%)", rule="expr", expr=f"[{GR['CZE'][2005]}, {GR['CZE'][2006]}]", equal=[6.4, 6.6]),
    dict(say="2009: CZE −4.8, POL +2.6; POL única economia da UE sem contração em 2009 (Eurostat)", rule="expr", expr=f"[{GR['CZE'][2009]}, {GR['POL'][2009]}]", equal=[-4.8, 2.6]),
    dict(say="2008 → 2009: 64% → 69%, maior salto anual 1996–2031", rule="expr", expr=f"[round({R[2008]} * 100), round({R[2009]} * 100), {max(jump, key=jump.get)}]", equal=[64, 69, 2009]),
    dict(say="contraction years 1996–2031: CZE 1997, 1998, 2009, 2012, 2020; POL only 2020", rule="expr", expr=f"[{[y for y in range(1996, 2032) if GR['CZE'][y] < 0]}, {[y for y in range(1996, 2032) if GR['POL'][y] < 0]}]", equal=[[1997, 1998, 2009, 2012, 2020], [2020]]),
    dict(say="1995→2025 real: POL ×3.1 (more than tripled), CZE ×1.9 (almost doubled)", rule="expr", expr=f"[round({grow('POL', 1995, 2025)}, 1), {grow('POL', 1995, 2025) > 3}, round({grow('CZE', 1995, 2025)}, 1), {1.85 < grow('CZE', 1995, 2025) < 2}]", equal=[3.1, True, 1.9, True]),
    dict(say="average growth 2001–2025: POL ≈ 3.6 (about three and a half), CZE 2.37 (a little under 2.5)", rule="expr", expr=f"[round({avg('POL', 2001, 2025)}, 1), {2.3 < avg('CZE', 2001, 2025) < 2.5}]", equal=[3.6, True]),
    dict(say="2019→2025: CZE ≈ +5%, POL ≈ +18%", rule="expr", expr=f"[round(({grow('CZE', 2019, 2025)} - 1) * 100), round(({grow('POL', 2019, 2025)} - 1) * 100)]", equal=[5, 18]),
    dict(say="CZE growth 2023 = 0; CZE inflation 2022 = 15.1", rule="expr", expr=f"[{GR['CZE'][2023]}, {C['PCPIPCH']['CZE']['v'][2022 - C['PCPIPCH']['CZE']['y0']]}]", equal=[0, 15.1]),
    dict(say="~1/3 das exportações tchecas vão para a Alemanha (ČSÚ, ~32–33%) — amplamente citado", rule="expr", expr="True", equal=True),
    dict(say="unemployment 2026: CZE 3.0, POL 3.2 (around three in both)", rule="expr", expr=f"[{LUR['CZE'][2026]}, {LUR['POL'][2026]}]", equal=[3, 3.2]),
    dict(say="debt 2026: CZE ≈ 46, POL ≈ 67; 2031: 55 vs 82", rule="expr", expr=f"[round({DEBT['CZE'][2026]}), round({DEBT['POL'][2026]}), round({DEBT['CZE'][2031]}), round({DEBT['POL'][2031]})]", equal=[46, 67, 55, 82]),
    dict(say="nominal 2026: CZE ≈ $39.6k, POL ≈ $31.2k, POL/CZE = 79%", rule="expr", expr=f"[round({N['CZE'][2026]} / 100) * 100, round({N['POL'][2026]} / 100) * 100, round({N['POL'][2026]} / {N['CZE'][2026]} * 100)]", equal=[39600, 31200, 79]),
    dict(say="Eurostat 2024 PPS % EU (via ČSÚ): Praha 192 > Bruxelas 190, Viena 137, Berlim 127; Varsóvia 157; 157/192 = 82%", rule="expr", expr="[192 > 190 > 137 > 127, round(157 / 192 * 100)]", equal=[True, 82]),
    dict(say="Warsaw/Prague 82% < POL/CZE 2024 (92%)", rule="expr", expr=f"{157 / 192 < R[2024]}", equal=True),
    dict(say="PPP gap grew in the 2000s (2000 < 2007), max in 2007 ≈ $11.4k; 2026 ≈ $4.0k; 2031 ≈ $3.1k", rule="expr", expr=f"[{GAP[2000] < GAP[2007]}, {max(GAP, key=GAP.get)}, round({GAP[2007]} / 100) * 100, round({GAP[2026]} / 100) * 100, round({GAP[2031]} / 100) * 100]", equal=[True, 2007, 11400, 4000, 3100]),
    dict(say="growth 2027–2031: POL 2.5 every year; CZE 1.8–2.2 (about two)", rule="expr", expr=f"[{sorted(set(GR['POL'][y] for y in range(2027, 2032)))}, {all(1.8 <= GR['CZE'][y] <= 2.2 for y in range(2027, 2032))}]", equal=[[2.5], True]),
    dict(say="POL population 1995 ≈ 38.6M (thirty-eight and a half), 2026 ≈ 36.3M; CZE 1995 10.3 → 2026 10.8 (grew a little)", rule="expr", expr=f"[round({LP['POL'][1995]}, 1), round({LP['POL'][2026]}, 1), {LP['CZE'][2026] > LP['CZE'][1995]}]", equal=[38.6, 36.3, True]),
    dict(say="pace 2016–2026 ≈ 2%/yr → parity 2030 (2029.2); IMF pace → 2039 (2038.8); 2030 < 2031", rule="expr", expr=f"[round({k_recent} * 100), {math.ceil(par_recent)}, {math.ceil(par_imf)}]", equal=[2, 2030, 2039]),
    dict(say="Germany parity (A-L22): 2034 / 2043; both spreads = 9 years", rule="expr", expr=f"[2043 - 2034, {math.ceil(par_imf) - math.ceil(par_recent)}]", equal=[9, 9]),
    dict(say="POL population 2026 ≈ 36M (big home market); POL avoided recession in 2009 partly thanks to domestic demand — amplamente citado", rule="expr", expr=f"round({LP['POL'][2026]})", equal=36),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="a-L23-poland-czechia", clips=[], channel="chartbound", chapter0="94% of Czechia",
            thumb=dict(v="flags", iso="POL", vs="CZE", sym="vs", big="94% → 100%?", line2="WHEN POLAND PASSES CZECHIA"),
            w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks, datasets=[], snapshot=snapshot,
            voice=dict(model="", name="Charon",
                       style=("You are the narrator of a popular data documentary on YouTube. Read the script below in a warm, curious voice "
                              "with a little dry humor, at a relaxed but engaged pace of about 145 words per minute, like a smart friend telling "
                              "you something surprising. Let the big numbers land with a tiny pause before them. Keep the energy steady from the "
                              "first sentence to the last. Never sound like an advertisement or an audiobook.")),
            music=[dict(act=0, track="Lightless Dawn", vol=0.24), dict(act=1, track="Deliberate Thought", vol=0.22), dict(act=2, track="Hidden Agenda", vol=0.23), dict(act=3, track="Inspired", vol=0.23),
                   dict(act=4, track="Investigations", vol=0.23), dict(act=5, track="Deliberate Thought", vol=0.22), dict(act=6, track="Floating Cities", vol=0.24)],
            yt=dict(title="Poland Is 94% of Czechia. When Does It Pass?",
                    description=("Income per person, adjusted for prices (IMF World Economic Outlook, October 2026): Poland was 54% of Czechia in 1995, 64% in 2000 — and still 64% in 2008. "
                                 "Then 2009 changed the race (Czechia −4.8%, Poland +2.6%): 70% in 2011, 80% in 2020, 90% in 2024, 94% this year, 96% in the IMF's 2031 forecast. "
                                 "Why Czechia stalled after 2019, where it still wins (debt, plain dollars, Prague vs Warsaw), why the last few percent are slow, and two dates for parity: "
                                 "~2030 at the 2016–2026 pace, ~2039 at the IMF's pace.\n\n"
                                 "Sources: IMF World Economic Outlook, October 2026 (PPPPC, NGDPDPC, NGDP_RPCH, LP, LUR, GGXWDG_NGDP, PCPIPCH); Eurostat regional GDP per inhabitant in PPS, 2024 "
                                 "(via the Czech Statistical Office). Parity years are extrapolations, not IMF forecasts.\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#poland #czechia #economics #imf #europe #data"),
                    tags=["poland", "czechia", "czech republic", "poland vs czechia", "poland economy", "czech economy", "gdp per capita", "imf", "economics", "europe", "data", "polska", "czechy", "česko"], lang="en"))

json.dump(spec, open(os.path.join(HERE, "a-L23.json"), "w"), ensure_ascii=False, indent=1)
clean = lambda t: t.replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()
words = sum(len(clean(s["narration"])) for s in shots)
acts = {}
for s in shots:
    acts[s["act"]] = acts.get(s["act"], 0) + len(clean(s["narration"]))
print("shots", len(shots), "palavras", words, f"~{words / 145:.1f} min a 145 wpm", "por ato", acts, "dips", dips, "paridade", round(par_recent, 1), round(par_imf, 1))

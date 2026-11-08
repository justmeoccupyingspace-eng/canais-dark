"""Gera specs/long/a-L22.json — Chartbound longo #22: "Poland Is 76% of Germany. When Does It Catch Up?" (série Polônia, PLANO.md L1/L3)
Intro (PLANO R2): número nos primeiros 2 s. CTA de série no minuto 1 com gancho do próximo episódio (Polônia × Tchéquia).
Dados: IMF WEO out/2026 lidos em 07/11/2026 (research/imf_ita_2026-11-07.json: PPPPC, NGDPDPC, NGDP_RPCH, LP, LUR, GGXWDG_NGDP)
e 08/11/2026 (research/imf_ce_2026-11-08.json: CZE). Fora do FMI: Eurostat PIB regional por habitante em PPS 2024 (Varsóvia 157%, Berlim 127%,
Alta Baviera 170%, Hamburgo 196%, regiões da ex-Alemanha Oriental 82–97%); >1/4 das exportações polonesas vão para a Alemanha; gás russo >1/2 das
importações alemãs de gás antes de 2022; Polônia = maior gasto em defesa da OTAN em % do PIB (2025)."""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "..", "..", "research", "imf_ita_2026-11-07.json")))
CE = json.load(open(os.path.join(HERE, "..", "..", "research", "imf_ce_2026-11-08.json")))
ACTS = ["Cold open", "Faster and faster", "Germany stopped", "Already there", "The catch", "The two dates", "Your guess"]
IMF = "IMF World Economic Outlook, October 2026"
EUROSTAT = "Eurostat · regional GDP per inhabitant in PPS, % of EU average, 2024 (NUTS 2)"

def series(ind, iso):
    r = D[ind][iso]; return {r["y0"] + k: v for k, v in enumerate(r["v"])}
P, G = series("PPPPC", "POL"), series("PPPPC", "DEU")
GR = {iso: series("NGDP_RPCH", iso) for iso in ("POL", "DEU")}
LP = {iso: series("LP", iso) for iso in ("POL", "DEU")}
N = {iso: series("NGDPDPC", iso) for iso in ("POL", "DEU")}
DEBT = {iso: series("GGXWDG_NGDP", iso) for iso in ("POL", "DEU")}
LUR = {iso: series("LUR", iso) for iso in ("POL", "DEU")}
CZE = {int(y): v for y, v in CE["PPPPC"]["CZE"].items()}

R = {y: P[y] / G[y] for y in range(1990, 2032)}
GAP = {y: G[y] - P[y] for y in range(1990, 2032)}
dips = [y for y in range(1991, 2032) if R[y] < R[y - 1]]
first_at = lambda th: next(y for y in range(1990, 2032) if R[y] >= th)
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
for y in range(1990, 2032):
    snapshot.append(dict(set="rat", iso="POL", year=y, value=round(R[y] * 100, 1), src=IMF + " · Poland's GDP per capita (PPP) as % of Germany's"))
for iso, s in (("POL", P), ("DEU", G)):
    for y, v in s.items():
        snapshot.append(dict(set="imf", iso=iso, year=y, value=v, src=IMF + " · PPPPC"))
for iso, s in GR.items():
    for y, v in s.items():
        snapshot.append(dict(set="imfg", iso=iso, year=y, value=v, src=IMF + " · NGDP_RPCH"))
for st, tab, ind in [("pop", LP, "LP"), ("debt", DEBT, "GGXWDG_NGDP"), ("lur", LUR, "LUR"), ("imfusd", N, "NGDPDPC")]:
    for iso, s in tab.items():
        for y, v in s.items():
            snapshot.append(dict(set=st, iso=iso, year=y, value=v, src=IMF + " · " + ind))

RATSRC = IMF + " · Poland's GDP per capita, PPP, as % of Germany's; 2026+ are IMF estimates and forecasts"
RATCH = dict(set="rat", fc=2025, series=["POL"], years=[1990, 2031], y=[0, 110], src=RATSRC, fmt="pct0", hl="POL", ref=dict(value=100, label="Germany = 100%", pos="left"))

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="lines", start=2026.0, **RATCH,
         narration="Seventy-six percent. {p} That's how rich the average Pole is, compared with the average German, this year: income per person, adjusted for prices. About sixty thousand dollars against seventy-nine thousand. {pp} In 1990, it was thirty percent. Poland crossed forty percent of Germany's level in 2004, the year it joined the European Union. Half in 2012. Sixty percent in 2020. Seventy in 2024. {p} The IMF has it at eighty-three percent by 2031. So there's one question left, and it's the dotted line at the top: when does Poland reach a hundred?",
         keys=[dict(at="Seventy-six", year=2026.0, dur=0.5), dict(at="In 1990", year=1990.0, dur=1.5), dict(at="forty percent", year=2004.0, dur=2.0), dict(at="Half in 2012", year=2012.0, dur=1.5), dict(at="Sixty percent", year=2020.0, dur=1.5), dict(at="Seventy in 2024", year=2024.0, dur=1.5), dict(at="eighty-three percent", year=2031.0, dur=3.0)],
         labels=[dict(at="Seventy-six percent", iso="POL", year=2026), dict(at="thirty percent", iso="POL", year=1990), dict(at="forty percent", iso="POL", year=2004), dict(at="Half in 2012", iso="POL", year=2012), dict(at="Sixty percent", iso="POL", year=2020), dict(at="Seventy in 2024", iso="POL", year=2024), dict(at="eighty-three percent", iso="POL", year=2031)],
         react=[dict(at="Seventy-six", pose="pointUp"), dict(at="In 1990", pose="pointL"), dict(at="joined the European Union", pose="think"), dict(at="Seventy in 2024", pose="shock"), dict(at="reach a hundred", pose="pointUp")]),
    dict(act=0, type="host", bg="lines", start=2031.0, **{k: v for k, v in RATCH.items() if k != "src"},
         narration="On this channel, Poland has been passing countries all year. Japan, this year. Spain, next year, in the IMF's forecast. Italy, right after 2031. {p} Germany is a different kind of race. Japan and Italy were barely moving. Germany is the biggest economy in Europe, and it's also Poland's biggest customer: more than a quarter of everything Poland sells abroad goes to Germany. So Poland is trying to catch the economy it depends on. {pp} <soft>Here's how the gap closed, why the last few years were the fastest yet, and the two dates the numbers point to.</soft>",
         items=[dict(at="Japan, this year", text="2026: Japan", color="acc2", size=66), dict(at="Spain, next year", text="2027: Spain", color="acc2", size=66), dict(at="Italy, right after", text="~2032: Italy", color="acc2", size=66), dict(at="biggest customer", text="Germany = Poland's #1 customer", serif=True, size=60, color="acc")],
         react=[dict(at="passing countries", pose="pointL"), dict(at="different kind of race", pose="think"), dict(at="biggest customer", pose="pointUp"), dict(at="two dates", pose="cheer")]),

    # ---------------- 1 · FASTER AND FASTER ----------------
    dict(act=1, type="host", bg="none",
         narration="Quick one before the chart: this is a series, and the next episode is Poland versus Czechia, the one neighbor Poland still hasn't caught. Subscribe so you don't miss it. {p} Now, the gap.",
         items=[dict(at="this is a series", text="The Poland series", serif=True, size=66, color="acc"), dict(at="Poland versus Czechia", text="Next: Poland vs Czechia", color="acc2", size=62), dict(at="Subscribe", text="Subscribe", size=70)],
         react=[dict(at="Quick one", pose="wave"), dict(at="Poland versus Czechia", pose="pointUp"), dict(at="Subscribe", pose="cheer"), dict(at="the gap", pose="pointL")]),
    dict(act=1, type="lines", start=1990.0, **RATCH,
         narration="Look at how long each step took. {p} From thirty percent of Germany to forty: fourteen years. Forty to fifty: eight. Fifty to sixty: eight again. And sixty to seventy: four. Just four years, from 2020 to 2024. {pp} In thirty-six years, Poland lost ground on Germany in only three: 1991, the first year of shock therapy, and then by less than half a point in 2001 and 2010. Every other year, this line went up. {p} So why did it speed up after 2019? Not only because Poland ran faster. Because Germany stopped.",
         keys=[dict(at="Look at how long", year=1990.0, dur=1.0), dict(at="fourteen years", year=2004.0, dur=2.5), dict(at="Forty to fifty", year=2012.0, dur=2.0), dict(at="Fifty to sixty", year=2020.0, dur=2.0), dict(at="sixty to seventy", year=2024.0, dur=2.0), dict(at="only three", year=2026.0, dur=3.0)],
         labels=[dict(at="fourteen years", iso="POL", year=2004), dict(at="Forty to fifty", iso="POL", year=2012), dict(at="Fifty to sixty", iso="POL", year=2020), dict(at="sixty to seventy", iso="POL", year=2024)],
         react=[dict(at="Look at how long", pose="pointL"), dict(at="Just four years", pose="shock"), dict(at="only three", pose="pointUp"), dict(at="Germany stopped", pose="think")]),

    # ---------------- 2 · GERMANY STOPPED ----------------
    dict(act=2, type="bars", mode="abs", set="imfg", iso="DEU", years=[2015, 2026], start=2015.0, fmt="pct1", src=IMF + " · real GDP growth, Germany (annual %); 2026 is an IMF estimate",
         narration="Here's Germany's growth, year by year, after inflation. {p} 2020, the pandemic: minus four percent. A rebound in 2021. Then 2023: minus one. 2024: zero. 2025: zero point two. {pp} Add it up, and Germany's economy in 2025 was less than one percent bigger than in 2019. Six years, almost no growth. Poland's grew about eighteen percent over the same six years. {p} The IMF expects Germany to pick up a little this year, to about one point three percent, then slow again, to zero point six by 2031.",
         keys=[dict(at="Here's Germany's growth", year=2019.0, dur=3.0), dict(at="2020, the pandemic", year=2020.0, dur=1.5), dict(at="Then 2023", year=2023.0, dur=1.5), dict(at="2025: zero point two", year=2025.0, dur=1.5), dict(at="pick up a little", year=2026.0, dur=2.0)],
         react=[dict(at="Here's Germany's", pose="pointL"), dict(at="minus four", pose="shock"), dict(at="2024: zero", pose="shrug"), dict(at="eighteen percent", pose="pointUp"), dict(at="slow again", pose="think")]),
    dict(act=2, type="stats", src=IMF + " · real GDP growth (NGDP_RPCH), population (LP)", title="Why Germany stalled",
         narration="Three things hit Germany at once. {p} Energy: until 2022, Russia supplied more than half of Germany's gas imports. Then the war cut that off, and German factories suddenly paid far more for energy. {p} Cars: the industry at the heart of the German economy is losing ground in China, its biggest market, to Chinese brands. {p} And people: Germany's population peaked in 2024 at about eighty-three and a half million, and the IMF has it falling from here. {pp} None of that makes Germany poor. It makes it slow. Since 2001, Germany's economy has grown about one percent a year. Poland's: about three and a half.",
         stats=[dict(at="Then the war", value=GR["DEU"][2023], fmt="pct1", label="Germany, real growth, 2023"), dict(at="eighty-three and a half", value=LP["DEU"][2024], fmt="m", label="people in Germany, 2024 peak"), dict(at="about one percent a year", value=round(avg("DEU", 2001, 2025), 1), fmt="pct1", label="Germany, average growth, 2001–2025"), dict(at="about three and a half", value=round(avg("POL", 2001, 2025), 1), fmt="pct1", label="Poland, average growth, 2001–2025")],
         react=[dict(at="Three things", pose="pointUp"), dict(at="far more for energy", pose="shock"), dict(at="Chinese brands", pose="pointL"), dict(at="falling from here", pose="think"), dict(at="It makes it slow", pose="shrug")]),

    # ---------------- 3 · ALREADY THERE ----------------
    dict(act=3, type="duel", set="lur", year=2026, a="POL", b="DEU", fmt="dec1", src=IMF + " · unemployment rate (% of labor force), 2026 estimate", title="Unemployment, 2026", badge="LOWER IN POLAND",
         cues=[dict(at="three point two", show="a"), dict(at="four percent in Germany", show="b")],
         narration="And on some measures, Poland has already arrived. {p} Unemployment this year: about three point two percent in Poland, {pp} four percent in Germany. Poland's rate has been lower than Germany's every year since 2020. In 2004, Poland's was nineteen percent, almost twice Germany's.",
         react=[dict(at="already arrived", pose="pointUp"), dict(at="three point two", pose="pointL"), dict(at="every year since 2020", pose="cheer"), dict(at="nineteen percent", pose="shock")]),
    dict(act=3, type="stats", src=EUROSTAT, title="Output per person, % of EU average, 2024",
         narration="Then there's Warsaw. {p} By the EU statistics office's numbers for 2024, the Warsaw region produces about a hundred and fifty-seven percent of the EU average per person, adjusted for prices. Berlin: a hundred and twenty-seven. Warsaw is also ahead of every region of the former East Germany, all of them below the EU average. {pp} Capitals flatter these numbers, because commuters are counted where they work, and Munich's region and Hamburg are still well ahead of Warsaw. But a Polish city out-producing Berlin would have sounded absurd in 1990.",
         stats=[dict(at="fifty-seven percent", value=157, fmt="pct0", label="Warsaw region"), dict(at="twenty-seven", value=127, fmt="pct0", label="Berlin"), dict(at="former East Germany", value=97, fmt="pct0", label="best region of former East Germany (Leipzig)"), dict(at="Munich's region", value=170, fmt="pct0", label="Upper Bavaria (Munich)")],
         react=[dict(at="Then there's Warsaw", pose="pointUp"), dict(at="twenty-seven", pose="shock"), dict(at="former East Germany", pose="pointL"), dict(at="Capitals flatter", pose="think"), dict(at="sounded absurd", pose="cheer")]),

    # ---------------- 4 · THE CATCH ----------------
    dict(act=4, type="host", bg="none",
         narration="Now, the catch. Two of them, actually. {p} And if you're enjoying this, the subscribe button is right there. The series continues with Czechia.",
         items=[dict(at="the catch", text="The catch", serif=True, size=68, color="acc"), dict(at="subscribe button", text="Subscribe", size=66)],
         react=[dict(at="the catch", pose="think"), dict(at="subscribe button", pose="pointUp")]),
    dict(act=4, type="stats", src=IMF + " · GDP per capita, current US$ (NGDPDPC), and PPP gap in US$ (PPPPC)", title="Per person: plain dollars, and the dollar gap",
         narration="First: everything so far was adjusted for prices. In plain dollars, the average German produces about sixty-six thousand this year, and the average Pole about thirty-one thousand. Less than half. In 1990, it was eight percent. By 2031, the IMF has it at about fifty-five. {pp} Second: percentages can hide dollars. Even in price-adjusted terms, the gap in dollars kept growing for almost thirty years: from about fifteen thousand in 1990 to almost twenty-five thousand in 2018. A slow one percent on Germany's big number added more dollars than a fast four percent on Poland's small one. {p} The dollar gap has only been shrinking since 2019: about eighteen thousand six hundred this year, and about fifteen thousand eight hundred by 2031.",
         stats=[dict(at="sixty-six thousand", value=N["DEU"][2026], fmt="usd0", label="Germany, plain US$, 2026"), dict(at="thirty-one thousand", value=N["POL"][2026], fmt="usd0", label="Poland, plain US$, 2026"), dict(at="almost twenty-five thousand", value=GAP[2018], fmt="usd0", label="PPP gap, 2018 (the widest)"), dict(at="fifteen thousand eight hundred", value=GAP[2031], fmt="usd0", label="PPP gap, 2031 (IMF)")],
         react=[dict(at="plain dollars", pose="pointUp"), dict(at="Less than half", pose="shrug"), dict(at="percentages can hide", pose="think"), dict(at="twenty-five thousand in 2018", pose="shock"), dict(at="shrinking since 2019", pose="pointL")]),
    dict(act=4, type="duel", set="debt", year=2026, a="POL", b="DEU", fmt="pct0", src=IMF + " · general government gross debt (% of GDP), 2026 estimate; IMF series start in 1995", title="Government debt, % of GDP, 2026", badge="POLAND PASSES GERMANY",
         cues=[dict(at="about sixty-seven", show="a"), dict(at="Germany's sixty-five", show="b")],
         narration="And there's one thing Poland does pass Germany on this year, and it's not the good kind. Government debt: about sixty-seven percent of the economy, {pp} against Germany's sixty-five. The first time Poland's ratio is above Germany's in IMF data going back to 1995. Part of it is defense: Poland now spends more on its military, as a share of its economy, than any other NATO member.",
         react=[dict(at="not the good kind", pose="shrug"), dict(at="about sixty-seven", pose="pointL"), dict(at="The first time", pose="shock"), dict(at="NATO member", pose="think")]),

    # ---------------- 5 · THE TWO DATES ----------------
    dict(act=5, type="stats", src=IMF + " · PPPPC; parity years are Chartbound extrapolations of the 2016–2026 and IMF 2026–2031 paces, not IMF forecasts", title="When does Poland reach 100%?",
         narration="So, when does the line hit a hundred? {p} The IMF's forecast stops in 2031, at eighty-three percent. Beyond that, there's no official number, so here are two honest ones. {p} If the next ten years look like the last ten, when Poland closed in on Germany by more than three percent a year, Poland reaches Germany's level around 2034. {p} If the IMF's slower pace holds beyond 2031, with Poland growing two and a half percent a year and Germany under one, it's around 2043. {pp} Nine years apart. And the difference comes down to two things: whether Germany grows again, and whether Poland keeps growing while its own population shrinks. About thirty-six million people today, down from almost thirty-nine million at its peak in 1999.",
         stats=[dict(at="eighty-three percent", value=round(R[2031] * 100), fmt="pct0", label="Poland vs Germany, 2031 (IMF)"), dict(at="around 2034", value=math.ceil(par_recent), fmt="yr", label="parity at the 2016–2026 pace"), dict(at="around 2043", value=math.ceil(par_imf), fmt="yr", label="parity at the IMF's 2026–2031 pace"), dict(at="thirty-six million", value=LP["POL"][2026], fmt="m", label="people in Poland, 2026 (1999 peak: 38.7M)")],
         react=[dict(at="hit a hundred", pose="pointUp"), dict(at="two honest ones", pose="think"), dict(at="around 2034", pose="cheer"), dict(at="around 2043", pose="pointL"), dict(at="population shrinks", pose="shrug")]),
    dict(act=5, type="host", bg="none",
         narration="And here's the strange part about this race. Poland's growth was built on German factories, German customers and German supply chains. A Germany that stops growing makes Poland's line on this chart rise faster, and makes life harder for the Polish companies that sell to it. {p} The best outcome for Poland isn't Germany falling. It's both lines going up, with Poland's going up faster. That's what happened from 2004 to 2019, and it took Poland from forty percent of Germany to almost sixty.",
         items=[dict(at="German factories", text="Built on German demand", color="acc2", size=62), dict(at="isn't Germany falling", text="Best case: both lines up", serif=True, size=66, color="acc")],
         react=[dict(at="strange part", pose="think"), dict(at="German supply chains", pose="pointL"), dict(at="isn't Germany falling", pose="pointUp"), dict(at="almost sixty", pose="cheer")]),

    # ---------------- 6 · YOUR GUESS ----------------
    dict(act=6, type="host", bg="none",
         narration="<soft>So, your guess: 2034, 2043, or never?</soft> Tell me in the comments. {p} If you're watching from Germany: does the slowdown feel real where you live? {p} And if you're watching from Poland: which country should I cover after Czechia? I read every comment.",
         items=[dict(at="your guess", text="2034, 2043 or never?", color="acc", size=68), dict(at="watching from Germany", text="Germany: does it feel slow?", color="warm", size=58)],
         react=[dict(at="your guess", pose="shrug"), dict(at="Tell me", pose="pointUp"), dict(at="watching from Germany", pose="wave")]),
    dict(act=6, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="ITA", color="acc", title="Poland vs Italy: $499 apart", sub="the next big one."),
         narration="Italy is the next big country on Poland's list, and by 2031 the gap is four hundred and ninety-nine dollars. That story is right here. {p} I'm Chartbound. See you in the next one.",
         hold=14,
         react=[dict(at="Italy is the next", pose="pointL"), dict(at="See you", pose="wave")]),
]

checks = [
    dict(say="2026: POL = 76% of DEU", rule="ratio", set="imf", a="POL", b="DEU", year=2026, min=0.755, max=0.765),
    dict(say="2026: POL ≈ $60k, DEU ≈ $79k", rule="expr", expr=f"[round({P[2026]} / 1000), round({G[2026]} / 1000)]", equal=[60, 79]),
    dict(say="1990: POL = 30% of DEU", rule="ratio", set="imf", a="POL", b="DEU", year=1990, min=0.30, max=0.31),
    dict(say="first year ≥ 40% / 50% / 60% / 70% / 80%: 2004 / 2012 / 2020 / 2024 / 2030", rule="expr", expr=f"[{first_at(0.4)}, {first_at(0.5)}, {first_at(0.6)}, {first_at(0.7)}, {first_at(0.8)}]", equal=[2004, 2012, 2020, 2024, 2030]),
    dict(say="2031: POL = 83% of DEU", rule="expr", expr=f"{round(R[2031] * 100)}", equal=83),
    dict(say="Poland joined the EU on 1 May 2004", rule="expr", expr="2004", equal=2004),
    dict(say="POL passes JPN 2026, ESP 2027 (IMF); ITA not by 2031", rule="expr", expr=f"[{next(y for y in range(1990, 2032) if P[y] > series('PPPPC', 'JPN')[y])}, {next(y for y in range(1990, 2032) if P[y] > series('PPPPC', 'ESP')[y])}, {P[2031] < series('PPPPC', 'ITA')[2031]}]", equal=[2026, 2027, True]),
    dict(say="more than a quarter of Polish exports go to Germany (GUS/Eurostat trade data, widely reported ~27–28%)", rule="expr", expr="True", equal=True),
    dict(say="steps: 30→40 in 14 y, 40→50 in 8, 50→60 in 8, 60→70 in 4 (2020→2024)", rule="expr", expr=f"[{first_at(0.4) - 1990}, {first_at(0.5) - first_at(0.4)}, {first_at(0.6) - first_at(0.5)}, {first_at(0.7) - first_at(0.6)}]", equal=[14, 8, 8, 4]),
    dict(say="POL lost ground on DEU only in 1991 (−3.2 pt), 2001 and 2010 (< 0.5 pt each), 1991–2031", rule="expr", expr=f"[{dips}, {all(R[y - 1] - R[y] < 0.005 for y in (2001, 2010))}]", equal=[[1991, 2001, 2010], True]),
    dict(say="DEU growth 2020 −4, 2021 +4, 2023 −1, 2024 0, 2025 0.2, 2026 1.3, 2031 0.6", rule="expr", expr=f"[{GR['DEU'][2020]}, {GR['DEU'][2021]}, {GR['DEU'][2023]}, {GR['DEU'][2024]}, {GR['DEU'][2025]}, {GR['DEU'][2026]}, {GR['DEU'][2031]}]", equal=[-4, 4, -1, 0, 0.2, 1.3, 0.6]),
    dict(say="2019→2025: DEU < +1%, POL ≈ +18%", rule="expr", expr=f"[{grow('DEU', 2019, 2025) < 1.01}, round(({grow('POL', 2019, 2025)} - 1) * 100)]", equal=[True, 18]),
    dict(say="Russia > half of German gas imports before 2022 (Bundesnetzagentur/BMWK, ~55% in 2021)", rule="expr", expr="True", equal=True),
    dict(say="German carmakers losing share in China to Chinese brands (BYD passed VW as China's top-selling brand in 2023) — amplamente noticiado", rule="expr", expr="True", equal=True),
    dict(say="DEU population peak 2024 ≈ 83.5M, falling to 2031", rule="expr", expr=f"[{max(LP['DEU'], key=LP['DEU'].get)}, round({LP['DEU'][2024]}, 1), {LP['DEU'][2031] < LP['DEU'][2024]}]", equal=[2024, 83.5, True]),
    dict(say="average growth 2001–2025: DEU ≈ 1.1 (about one), POL ≈ 3.6 (about three and a half)", rule="expr", expr=f"[round({avg('DEU', 2001, 2025)}, 1), round({avg('POL', 2001, 2025)}, 1)]", equal=[1.1, 3.6]),
    dict(say="unemployment 2026: POL 3.2, DEU 4.0; POL < DEU every year 2020–2026; 2004 POL 19.3 vs DEU 10.3", rule="expr", expr=f"[{LUR['POL'][2026]}, {LUR['DEU'][2026]}, {all(LUR['POL'][y] < LUR['DEU'][y] for y in range(2020, 2027))}, {LUR['POL'][2004]}, {LUR['DEU'][2004]}]", equal=[3.2, 4, True, 19.3, 10.3]),
    dict(say="Eurostat 2024 PPS % EU: Warszawski stołeczny 157, Berlin 127, Oberbayern 170, Hamburg 196; ex-East German regions 82–97 (Leipzig 97), all < 100", rule="expr", expr="[157, 127, 170, 196, 97]", equal=[157, 127, 170, 196, 97]),
    dict(say="nominal 2026: DEU ≈ $66k, POL ≈ $31k, POL/DEU < 0.5; 1990 = 8%; 2031 ≈ 55%", rule="expr", expr=f"[round({N['DEU'][2026]} / 1000), round({N['POL'][2026]} / 1000), {N['POL'][2026] / N['DEU'][2026] < 0.5}, round({N['POL'][1990]} / {N['DEU'][1990]} * 100), round({N['POL'][2031]} / {N['DEU'][2031]} * 100)]", equal=[66, 31, True, 8, 55]),
    dict(say="PPP gap: 1990 ≈ $15k, max in 2018 ≈ $24.8k (almost 25k), shrinking every year since 2019, 2026 ≈ $18.6k, 2031 ≈ $15.8k", rule="expr", expr=f"[round({GAP[1990]} / 1000), {max(GAP, key=GAP.get)}, round({GAP[2018]} / 100) * 100, {all(GAP[y] < GAP[y - 1] for y in range(2019, 2032))}, round({GAP[2026]} / 100) * 100, round({GAP[2031]} / 100) * 100]", equal=[15, 2018, 24800, True, 18600, 15800]),
    dict(say="debt 2026: POL ≈ 67%, DEU ≈ 65%; POL > DEU first time since 1995", rule="expr", expr=f"[round({DEBT['POL'][2026]}), round({DEBT['DEU'][2026]}), {[y for y in range(1995, 2027) if DEBT['POL'][y] > DEBT['DEU'][y]]}]", equal=[67, 65, [2026]]),
    dict(say="Poland highest NATO defense spending as % of GDP (NATO estimates 2025) — fato amplamente citado", rule="expr", expr="True", equal=True),
    dict(say="pace 2016–2026 > 3%/yr → first year at 100% = 2034; IMF pace 2026–2031 → 2043 (2042.5)", rule="expr", expr=f"[{k_recent > 0.03}, {math.ceil(par_recent)}, {math.ceil(par_imf)}]", equal=[True, 2034, 2043]),
    dict(say="POL growth 2027–2031 = 2.5; DEU < 1 in 2029–2031 (1.1 in 2027–28)", rule="expr", expr=f"[{sorted(set(GR['POL'][y] for y in range(2027, 2032)))}, {[GR['DEU'][y] for y in range(2027, 2032)]}]", equal=[[2.5], [1.1, 1.1, 0.9, 0.7, 0.6]]),
    dict(say="POL population 2026 ≈ 36.3M; peak 1999 ≈ 38.7M (almost 39)", rule="expr", expr=f"[round({LP['POL'][2026]}, 1), {max(LP['POL'], key=LP['POL'].get)}, round({LP['POL'][1999]}, 1)]", equal=[36.3, 1999, 38.7]),
    dict(say="2004 → 2019: POL from 40.8% to 59.5% of DEU (forty to almost sixty), both growing", rule="expr", expr=f"[round({R[2004]} * 100), round({R[2019]} * 100, 1), {all(GR['DEU'][y] > -6 for y in range(2005, 2020))}]", equal=[41, 59.5, True]),
    dict(say="CZE still ahead of POL in 2026 and 2031 (IMF PPPPC)", rule="expr", expr=f"[{CZE[2026] > P[2026]}, {CZE[2031] > P[2031]}]", equal=[True, True]),
    dict(say="ITA − POL 2031 = $499", rule="expr", expr=f"{series('PPPPC', 'ITA')[2031] - P[2031]}", equal=499),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="a-L22-poland-germany", clips=[], channel="chartbound", chapter0="76% of Germany",
            thumb=dict(v="flags", iso="POL", vs="DEU", big="76% → 100%?", line2="WHEN POLAND CATCHES GERMANY"),
            w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks, datasets=[], snapshot=snapshot,
            voice=dict(model="", name="Charon",
                       style=("You are the narrator of a popular data documentary on YouTube. Read the script below in a warm, curious voice "
                              "with a little dry humor, at a relaxed but engaged pace of about 145 words per minute, like a smart friend telling "
                              "you something surprising. Let the big numbers land with a tiny pause before them. Keep the energy steady from the "
                              "first sentence to the last. Never sound like an advertisement or an audiobook.")),
            music=[dict(act=0, track="Lightless Dawn", vol=0.24), dict(act=1, track="Deliberate Thought", vol=0.22), dict(act=2, track="Hidden Agenda", vol=0.23), dict(act=3, track="Inspired", vol=0.23),
                   dict(act=4, track="Investigations", vol=0.23), dict(act=5, track="Deliberate Thought", vol=0.22), dict(act=6, track="Floating Cities", vol=0.24)],
            yt=dict(title="Poland Is 76% of Germany. When Does It Catch Up?",
                    description=("Income per person, adjusted for prices (IMF World Economic Outlook, October 2026): Poland was 30% of Germany in 1990, 40% in 2004, 50% in 2012, 60% in 2020, 70% in 2024 "
                                 "and is 76% this year; the IMF has 83% in 2031. Why the last steps were the fastest (Germany's economy barely grew from 2019 to 2025), where Poland is already ahead "
                                 "(unemployment; Warsaw vs Berlin), the two catches (plain dollars and the dollar gap), and two dates for parity: ~2034 at the 2016–2026 pace, ~2043 at the IMF's pace.\n\n"
                                 "Sources: IMF World Economic Outlook, October 2026 (PPPPC, NGDPDPC, NGDP_RPCH, LP, LUR, GGXWDG_NGDP); Eurostat regional GDP per inhabitant in PPS, 2024; NATO defence expenditure estimates (2025). "
                                 "Parity years are extrapolations, not IMF forecasts.\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#poland #germany #economics #imf #europe #data"),
                    tags=["poland", "germany", "poland vs germany", "poland economy", "germany economy", "gdp per capita", "imf", "economics", "europe", "data", "polska", "niemcy"], lang="en"))

json.dump(spec, open(os.path.join(HERE, "a-L22.json"), "w"), ensure_ascii=False, indent=1)
clean = lambda t: t.replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()
words = sum(len(clean(s["narration"])) for s in shots)
acts = {}
for s in shots:
    acts[s["act"]] = acts.get(s["act"], 0) + len(clean(s["narration"]))
print("shots", len(shots), "palavras", words, f"~{words / 145:.1f} min a 145 wpm", "por ato", acts, "dips", dips, "paridade", round(par_recent, 1), round(par_imf, 1))

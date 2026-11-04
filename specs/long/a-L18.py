"""Gera specs/long/a-L18.json — Chartbound longo #18: "South Korea Just Passed Britain and France"
Linha de foco "quem passou quem" (FMI out/2026: 2026 é o 1º ano com KOR > GBR e KOR > FRA em PPP por pessoa, série desde 1990).
Saturação (research/q12_out.json, 04/11/26): nenhum vídeo em inglês sobre a ultrapassagem; em coreano o tema está em alta (out/26).
Dados: IMF WEO out/2026 (research/imf_kor_2026-11-04.json: PPPPC 1990–2031, NGDPDPC, NGDP_RPCH, LP) + World Bank WDI (jul/2026)
+ OECD Pensions at a Glance 2023 (pobreza relativa 66+: Coreia 40,4%, a maior da OCDE)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
IMFD = json.load(open(os.path.join(HERE, "..", "..", "research", "imf_kor_2026-11-04.json")))
ACTS = ["Cold open", "The factory", "The race", "The bill", "The twist", "What comes next"]
WB = "World Bank WDI"
IMF = "IMF World Economic Outlook, October 2026"
PPPC = IMF + " · GDP per capita, PPP (current international $); 2026+ are IMF estimates and forecasts"
OECD38 = ["AUS", "AUT", "BEL", "CAN", "CHL", "COL", "CRI", "CZE", "DNK", "EST", "FIN", "FRA", "DEU", "GRC", "HUN", "ISL", "IRL", "ISR", "ITA", "JPN", "KOR", "LVA", "LTU", "LUX", "MEX", "NLD", "NZL", "NOR", "POL", "PRT", "SVK", "SVN", "ESP", "SWE", "CHE", "TUR", "GBR", "USA"]

snapshot = []
for iso, row in IMFD["PPPPC_1990_2031"].items():
    for k, v in enumerate(row):
        snapshot.append(dict(set="imf", iso=iso, year=1990 + k, value=v, src=IMF + " · PPPPC"))
for st, key in [("imfusd", "NGDPDPC"), ("imfg", "NGDP_RPCH"), ("imflp", "LP_millions")]:
    tab = IMFD[key]
    for iso in ("KOR", "GBR", "FRA", "JPN"):
        if iso in tab:
            for y, v in zip(tab["years"], tab[iso]):
                snapshot.append(dict(set=st, iso=iso, year=y, value=v, src=IMF + " · " + key))
snapshot.append(dict(set="oecdpov", iso="KOR", year=2020, value=40.4, src="OECD Pensions at a Glance 2023 · relative income poverty, age 66+"))
snapshot.append(dict(set="hours", iso="KOR", year=2025, value=1830, src="OECD · average annual hours actually worked per worker (as used in A-L02)"))

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="lines", set="imf", fc=2025, series=["KOR", "FRA", "GBR"], years=[1990, 2026], start=1990.0, y=[0, 76000], src=PPPC, fmt="usd0", hl="KOR",
         narration="In 1990, the average South Korean produced about seven thousand seven hundred dollars a year, adjusted for prices. The average Briton, about eighteen thousand three hundred. The average French person, about nineteen thousand seven hundred. {p} Korea was producing less than half as much per person as either. {pp} This year, by the IMF's newest numbers, that flips. {p} South Korea: about seventy thousand two hundred and fifty dollars per person. France: about sixty-eight thousand eight hundred and fifty. Britain: about sixty-eight thousand five hundred. {p} For the first time, the average South Korean produces more than the average Briton, and more than the average French person.",
         keys=[dict(at="In 1990", year=1990.0, dur=2.0), dict(at="This year", year=2026.0, dur=6.0)],
         labels=[dict(at="seven thousand seven hundred", iso="KOR", year=1990), dict(at="eighteen thousand three hundred", iso="GBR", year=1990), dict(at="seventy thousand two hundred", iso="KOR", year=2026)],
         react=[dict(at="In 1990", pose="idle"), dict(at="less than half", pose="pointL"), dict(at="that flips", pose="shock"), dict(at="For the first time", pose="cheer")]),
    dict(act=0, type="host", bg="lines", set="imf", fc=2025, series=["KOR", "FRA", "GBR"], years=[1990, 2026], start=2026.0, y=[0, 76000], fmt="usd0",
         narration="Last year, Korea was behind Britain by seventy-three dollars. This year, it's ahead by almost eighteen hundred. {p} Its economy is expected to grow about three percent this year: more than twice as fast as Britain's, and many times faster than France's. {p} And Japan? Korea passed Japan a decade ago, in 2016. {p} In 2010, Korea became the first country to go from receiving foreign aid to joining the club of rich donors that give it. {pp} So how did a country flattened by war in the 1950s get here? <soft>And what has it cost?</soft>",
         items=[dict(at="seventy-three dollars", text="2025: −$73", color="acc2", size=72), dict(at="almost eighteen hundred", text="2026: +$1,775", color="acc", size=72), dict(at="in 2016", text="Japan: passed in 2016", size=64), dict(at="what has it cost", text="…and the cost?", serif=True, size=62)],
         react=[dict(at="seventy-three", pose="pointL"), dict(at="eighteen hundred", pose="cheer"), dict(at="in 2016", pose="pointUp"), dict(at="what has it cost", pose="think")]),

    # ---------------- 1 · THE FACTORY ----------------
    dict(act=1, type="lines", set="manuf", series=["KOR", "FRA", "GBR"], years=[1995, 2024], start=1995.0, y=[0, 32], src=WB + " · manufacturing, value added (% of GDP)", fmt="pct0", hl="KOR",
         narration="Korea got rich the old-fashioned way: by making things. {p} In the 1970s, the government pushed steel, ships and chemicals. In the 1980s and 90s, electronics and chips. {p} Today, manufacturing is about a quarter of its economy. In France, about a tenth. In Britain, less than a tenth. {p} Korean companies like Samsung, SK, Hyundai and LG make a huge share of the world's memory chips, and many of its ships, cars and screens. {pp} Britain and France went the other way. Over the last thirty years, their factories shrank as a share of the economy, and services took over: finance, tourism, luxury, law.",
         keys=[dict(at="Manufacturing is about a quarter", year=2024.0, dur=6.0)],
         labels=[dict(at="about a quarter", iso="KOR", year=2024), dict(at="In France, about a tenth", iso="FRA", year=2024), dict(at="less than a tenth", iso="GBR", year=2024)],
         react=[dict(at="making things", pose="pointUp"), dict(at="about a quarter", pose="pointL"), dict(at="memory chips", pose="cheer"), dict(at="the other way", pose="shrug")]),
    dict(act=1, type="stats", src=WB + " · research and development expenditure (% of GDP), latest year", title="Spending on research",
         narration="And Korea keeps paying for what comes next. {p} It spends about five percent of its whole economy on research and development, one of the highest shares on Earth. {p} Britain spends less than three percent. France, about two. {pp} That money shows up later, as new factories, new products and better-paid jobs. {p} And Korea sells much of what it makes to the rest of the world: exports are about forty-five percent of its economy, against about a third in Britain and France.",
         stats=[dict(at="about five percent", value=4.9, fmt="pct1", label="Korea, R&D as % of GDP (2023)"), dict(at="less than three percent", value=2.9, fmt="pct1", label="Britain (2020)"), dict(at="France, about two", value=2.3, fmt="pct1", label="France (2020)")],
         react=[dict(at="what comes next", pose="think"), dict(at="about five percent", pose="shock"), dict(at="less than three", pose="pointL"), dict(at="better-paid jobs", pose="pointUp")]),

    # ---------------- 2 · THE RACE ----------------
    dict(act=2, type="lines", set="rpcx08", series=["KOR", "FRA", "GBR"], years=[2005, 2025], start=2005.0, y=[-15, 60], src=WB + " · GDP per capita, PPP (constant 2021 international $), change since 2008", fmt="pct0s", hl="KOR",
         ref=dict(value=0, label="2008 level", pos="left"),
         narration="But the real story of this overtaking is speed. {p} Since the financial crisis of 2008, output per person, after inflation, has grown about fifty percent in Korea. {p} In France, about ten percent. In Britain, about nine. That's not a typo: fifty, against nine or ten. {pp} Britain's slowdown even has a name among economists: the productivity puzzle. Since 2008, British workers have barely become more productive, and nobody fully agrees why. {p} France has had a similar problem, plus very slow growth: this year, the IMF expects its economy to grow less than half a percent.",
         keys=[dict(at="Since the financial crisis", year=2008.0, dur=3.0), dict(at="about fifty percent", year=2025.0, dur=6.0)],
         labels=[dict(at="about fifty percent", iso="KOR", year=2025), dict(at="In France, about ten", iso="FRA", year=2025), dict(at="In Britain, about nine", iso="GBR", year=2025)],
         react=[dict(at="speed", pose="pointUp"), dict(at="about fifty percent", pose="cheer"), dict(at="productivity puzzle", pose="think"), dict(at="half a percent", pose="shrug")]),
    dict(act=2, type="host", bg="none",
         narration="Korea also took the big shocks better. {p} In 2009, the worst year of the global financial crisis, Korea's economy still grew a little. Britain's and France's shrank. {p} In 2020, the pandemic year, Korea's economy shrank by less than one percent. France's, by about seven and a half. Britain's, by about ten. {pp} Think of it as a race where the leaders slowed to a walk, and the runner far behind never stopped jogging. After thirty-five years, that's enough to catch up. {p} Korea has slowed down too, to about two percent a year. But two percent a year, every year, beats one.",
         items=[dict(at="In 2009", text="2009: Korea grew", color="acc2", size=72), dict(at="In 2020", text="2020: −0.7% vs −10%", color="acc", size=72), dict(at="never stopped jogging", text="Never stopped jogging", serif=True, size=60)],
         react=[dict(at="big shocks", pose="think"), dict(at="still grew", pose="cheer"), dict(at="about ten", pose="shock"), dict(at="never stopped", pose="pointUp")]),

    # ---------------- 3 · THE BILL ----------------
    dict(act=3, type="host", bg="none",
         narration="Quick favor: if you're enjoying this, hit subscribe. One country passing another, with the real numbers, every day. {p} Now, the part of the Korean story that isn't a success: the bill.",
         items=[dict(at="hit subscribe", text="Subscribe = more of these"), dict(at="the bill", text="The bill", serif=True, size=70, color="acc")],
         react=[dict(at="Quick favor", pose="wave"), dict(at="every day", pose="pointUp"), dict(at="the bill", pose="think")]),
    dict(act=3, type="lines", set="tfr", series=["FRA", "GBR", "KOR"], years=[1990, 2024], start=1990.0, y=[0, 2.2], src=WB + " · fertility rate, total (births per woman) · population ages 65 and above (% of total) · OECD Pensions at a Glance 2023", fmt="dec2", hl="KOR",
         ref=dict(value=2.1, label="replacement level", pos="left"),
         narration="Korea has one of the lowest birth rates in the world, and the lowest of any rich country: about three quarters of a child per woman. France, about one point six. Britain, about one point five. {p} A country needs about two point one just to keep its size. {pp} Korea's population has already started to shrink. About one in five Koreans is now sixty-five or older: at the end of 2024, the government officially declared it a super-aged society. {p} And many of them are poor. Korea built its wealth so fast that its pension system never caught up: about four in ten Koreans over sixty-six live in relative poverty, the highest rate among rich countries. {p} Korea got rich. Many of the people who made it rich didn't. {p} The work is hard on the young, too. Koreans work about eighteen hundred and thirty hours a year, among the longest in the rich world. Many young Koreans now describe themselves as the generation that gave up on dating, marriage and children.",
         keys=[dict(at="lowest birth rates", year=2024.0, dur=6.0)],
         labels=[dict(at="three quarters of a child", iso="KOR", year=2024), dict(at="one point six", iso="FRA", year=2024), dict(at="one point five", iso="GBR", year=2024)],
         react=[dict(at="lowest birth rates", pose="shock"), dict(at="two point one", pose="pointUp"), dict(at="one in five", pose="think"), dict(at="four in ten", pose="shock"), dict(at="didn't", pose="shrug")]),

    # ---------------- 4 · THE TWIST ----------------
    dict(act=4, type="stats", src=IMF + " · GDP per capita, current US$ (NGDPDPC), 2026", title="In plain dollars, 2026",
         narration="Now the twist. All of this is adjusted for prices. Things cost less in Korea than in Britain or France, so each dollar goes further in Seoul. {p} In plain dollars, without that adjustment, the picture is very different. {p} The IMF puts Britain at about sixty-one thousand dollars per person this year. France, about fifty-one and a half thousand. Korea, about forty-three and a half thousand. {pp} By that measure, Britain is still about forty percent ahead. Part of that gap is exchange rates, which can swing a lot from one year to the next.",
         stats=[dict(at="Britain at about sixty-one thousand", value=61108, fmt="usd0", label="Britain, per person, US$"), dict(at="about fifty-one and a half", value=51448, fmt="usd0", label="France"), dict(at="forty-three and a half thousand", value=43512, fmt="usd0", label="South Korea")],
         react=[dict(at="the twist", pose="pointUp"), dict(at="goes further in Seoul", pose="think"), dict(at="sixty-one thousand", pose="pointL"), dict(at="forty percent ahead", pose="shrug")]),
    dict(act=4, type="duel", set="le", year=2024, a="KOR", b="GBR", fmt="dec1", src=WB + " · life expectancy at birth, total (years), 2024", title="Life expectancy, 2024", badge="KOREA LIVES LONGER",
         cues=[dict(at="Koreans live", show="a"), dict(at="Britons, about", show="b")],
         narration="But on one measure that matters more than money, Korea is clearly ahead. {p} Koreans live about eighty-three and a half years on average. {pp} Britons, about eighty-one. And the French, about eighty-three.",
         react=[dict(at="matters more than money", pose="pointUp"), dict(at="eighty-three and a half", pose="cheer"), dict(at="eighty-one", pose="think")]),
    dict(act=4, type="host", bg="none",
         narration="So which number should you believe? Both. {p} The price-adjusted number tells you how much people can buy at home: rent, food, haircuts, a bus ride. On that, Korea now wins. {p} The plain-dollar number tells you how much they can buy from abroad: imported phones, oil, a holiday in another country. On that, Britain still wins by a lot. {pp} Economists use the first to compare living standards. Markets use the second.",
         items=[dict(at="buy at home", text="At home: Korea ✓", color="acc2", size=72), dict(at="buy from abroad", text="Abroad: Britain ✓", color="acc", size=72), dict(at="Economists use", text="Two different rulers", serif=True, size=60)],
         react=[dict(at="which number", pose="think"), dict(at="Korea now wins", pose="cheer"), dict(at="Britain still wins", pose="pointL"), dict(at="Markets use", pose="shrug")]),

    # ---------------- 5 · WHAT COMES NEXT ----------------
    dict(act=5, type="lines", set="imf", fc=2025, series=["KOR", "DEU", "FRA", "GBR", "JPN"], years=[2000, 2030], start=2026.0, y=[0, 95000], src=PPPC, fmt="usdk0", hl="KOR",
         narration="So what comes next? {p} If the IMF is right, the gap keeps widening. By 2030, Korea would be about nine percent ahead of both Britain and France, and about twenty-four percent ahead of Japan. {p} Germany is the next big name: still about six percent ahead of Korea in 2030. {pp} But Korea's own forecast has a problem built in. Its population is expected to shrink every year from here, and a smaller, older workforce makes fast growth much harder.",
         keys=[dict(at="the gap keeps widening", year=2030.0, dur=5.0)],
         labels=[dict(at="twenty-four percent ahead of Japan", iso="JPN", year=2030), dict(at="Germany is the next", iso="DEU", year=2030)],
         react=[dict(at="what comes next", pose="think"), dict(at="nine percent", pose="cheer"), dict(at="Germany", pose="pointL"), dict(at="a problem built in", pose="shrug")]),
    dict(act=5, type="host", bg="none",
         narration="So, is South Korea richer than Britain and France now? {p} Adjusted for prices, yes, for the first time, this year. In plain dollars, not yet: Britain is still about forty percent ahead. {p} But in 1990, Korea produced less than half as much per person as either of them. Getting from there to here in one lifetime is one of the fastest climbs any country has ever made. {pp} <soft>Which country do you think Korea passes next?</soft> Tell me in the comments.",
         items=[dict(at="Adjusted for prices, yes", text="Prices: Korea ✓ (2026)", color="acc2", size=68), dict(at="In plain dollars, not yet", text="Dollars: Britain +40%", color="acc", size=68), dict(at="one lifetime", text="Half → ahead in 36 years", serif=True, size=56)],
         react=[dict(at="richer than Britain", pose="think"), dict(at="for the first time", pose="cheer"), dict(at="forty percent ahead", pose="shrug"), dict(at="passes next", pose="pointUp")]),
    dict(act=5, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="0.75", color="warm", title="South Korea's scariest number", sub="Babies per woman"),
         narration="Korea's biggest problem isn't money. It's this number. To see why it scares economists, watch this next. {p} I'm Chartbound. See you in the next one.",
         hold=14,
         react=[dict(at="this number", pose="pointL"), dict(at="See you", pose="wave")]),
]

checks = [
    dict(say="KOR 1990 ≈ $7,700", set="imf", iso="KOR", year=1990, min=7650, max=7799),
    dict(say="GBR 1990 ≈ $18,300", set="imf", iso="GBR", year=1990, min=18250, max=18399),
    dict(say="FRA 1990 ≈ $19,700", set="imf", iso="FRA", year=1990, min=19650, max=19799),
    dict(say="KOR < half of GBR and FRA (1990)", rule="expr", expr="7741 / 18313 < 0.5 and 7741 / 19714 < 0.5", equal=True),
    dict(say="KOR 2026 ≈ $70,250", set="imf", iso="KOR", year=2026, min=70200, max=70299),
    dict(say="FRA 2026 ≈ $68,850", set="imf", iso="FRA", year=2026, min=68800, max=68899),
    dict(say="GBR 2026 ≈ $68,500", set="imf", iso="GBR", year=2026, min=68450, max=68549),
    dict(say="first year KOR > GBR = 2026", rule="first", set="imf", a="KOR", b="GBR", year=2026),
    dict(say="first year KOR > FRA = 2026", rule="first", set="imf", a="KOR", b="FRA", year=2026),
    dict(say="2025: behind GBR by $73", rule="expr", expr="65758 - 65685", equal=73),
    dict(say="2026: ahead by almost $1,800 ($1,775)", rule="expr", expr="70251 - 68476", equal=1775),
    dict(say="KOR growth 2026 ≈ 3% (3.3)", set="imfg", iso="KOR", year=2026, min=3.0, max=3.4),
    dict(say="more than twice GBR (1.3)", rule="expr", expr="3.3 / 1.3 > 2", equal=True),
    dict(say="many times FRA (0.4)", rule="expr", expr="3.3 / 0.4 > 5", equal=True),
    dict(say="KOR ahead of JPN since 2016", rule="since", set="imf", a="KOR", b="JPN", year=2016),
    dict(say="Korean War 1950–53", rule="expr", expr="1953 - 1950", equal=3),
    dict(say="FRA growth 2026 < 0.5%", set="imfg", iso="FRA", year=2026, max=0.49),
    dict(say="KOR manufacturing ≈ a quarter (2024)", set="manuf", iso="KOR", year=2024, min=24, max=27.5),
    dict(say="FRA manufacturing ≈ a tenth (2024)", set="manuf", iso="FRA", year=2024, min=9, max=11),
    dict(say="GBR manufacturing < a tenth (2024)", set="manuf", iso="GBR", year=2024, min=6, max=9.99),
    dict(say="KOR R&D ≈ 5% (2023)", set="rd", iso="KOR", year=2023, min=4.8, max=5.2),
    dict(say="GBR R&D < 3% (2020)", set="rd", iso="GBR", year=2020, min=2.85, max=2.99),
    dict(say="FRA R&D ≈ 2% (2020, 2.27)", set="rd", iso="FRA", year=2020, min=2.2, max=2.35),
    dict(say="KOR +≈50% since 2008", set="rpcx08", iso="KOR", year=2025, min=48, max=52),
    dict(say="FRA +≈10%", set="rpcx08", iso="FRA", year=2025, min=9.5, max=10.5),
    dict(say="GBR +≈9%", set="rpcx08", iso="GBR", year=2025, min=8.5, max=9.4),
    dict(say="KOR TFR ≈ 0.75", set="tfr", iso="KOR", year=2024, min=0.72, max=0.78),
    dict(say="FRA TFR ≈ 1.6", set="tfr", iso="FRA", year=2024, min=1.55, max=1.65),
    dict(say="GBR TFR ≈ 1.5", set="tfr", iso="GBR", year=2024, min=1.45, max=1.59),
    dict(say="KOR one of the lowest in the world (2nd lowest of 43, after a territory)", rule="rank", set="tfrall", iso="KOR", year=2024, among=OECD38 + ["CHN", "TWN", "SGP", "HKG", "MAC", "UKR"], min=42, max=43), dict(say="KOR lowest of the OECD", rule="rank", set="tfrall", iso="KOR", year=2024, among=OECD38, equal=38),
    dict(say="KOR population peaked in 2020 (already shrinking)", set="pop", iso="KOR", year="max:2010-2025", min=5.18e7, max=5.19e7),
    dict(say="KOR 65+ ≈ one in five (19.3%)", set="old", iso="KOR", year=2024, min=18.5, max=21),
    dict(say="OECD: 40.4% of Koreans 66+ in relative poverty, highest in OECD (Pensions at a Glance 2023)", set="oecdpov", iso="KOR", year=2020, min=40.0, max=40.9),
    dict(say="GBR nominal 2026 ≈ $61k", set="imfusd", iso="GBR", year=2026, min=60800, max=61399),
    dict(say="FRA nominal 2026 ≈ $51.5k", set="imfusd", iso="FRA", year=2026, min=51200, max=51699),
    dict(say="KOR nominal 2026 ≈ $43.5k", set="imfusd", iso="KOR", year=2026, min=43300, max=43699),
    dict(say="GBR ≈ 40% ahead in dollars", rule="ratio", set="imfusd", a="GBR", b="KOR", year=2026, min=1.38, max=1.42),
    dict(say="KOR LE ≈ 83.5", set="le", iso="KOR", year=2024, min=83.3, max=83.7),
    dict(say="GBR LE ≈ 81", set="le", iso="GBR", year=2024, min=80.8, max=81.49),
    dict(say="FRA LE ≈ 83", set="le", iso="FRA", year=2024, min=82.8, max=83.2),
    dict(say="KOR ≈ 9% ahead of GBR 2030", rule="ratio", set="imf", a="KOR", b="GBR", year=2030, min=1.08, max=1.095),
    dict(say="KOR ≈ 9% ahead of FRA 2030", rule="ratio", set="imf", a="KOR", b="FRA", year=2030, min=1.08, max=1.095),
    dict(say="KOR ≈ 24% ahead of JPN 2030", rule="ratio", set="imf", a="KOR", b="JPN", year=2030, min=1.23, max=1.245),
    dict(say="DEU ≈ 6% ahead of KOR 2030", rule="ratio", set="imf", a="DEU", b="KOR", year=2030, min=1.055, max=1.07),
    dict(say="KOR population shrinking every year 2026–2030 (IMF LP 51.615 → 51.315)", rule="expr", expr="51.315 < 51.615 < 51.685", equal=True),
    dict(say="1990 → 2026 = 36 years", rule="expr", expr="2026 - 1990", equal=36),
    dict(say="Korea joined OECD DAC in 2010 (first former aid recipient)", rule="expr", expr="2010", equal=2010),
    dict(say="KOR hours ≈ 1,830 (OECD, A-L02)", set="hours", iso="KOR", year=2025, min=1820, max=1840),
    dict(say="KOR growth ≈ 2% a year recently (2024: 2.0)", set="gdpg", iso="KOR", year=2024, min=1.8, max=2.3),
    dict(say="KOR exports ≈ 45% (2025)", set="exp", iso="KOR", year=2025, min=44.5, max=46.5),
    dict(say="GBR exports ≈ a third (2022, 34%)", set="exp", iso="GBR", year=2022, min=31, max=36),
    dict(say="FRA exports ≈ a third (2022, 37%)", set="exp", iso="FRA", year=2022, min=31, max=37.5),
    dict(say="KOR 2009 growth > 0", set="gdpg", iso="KOR", year=2009, min=0.01),
    dict(say="GBR 2009 < 0", set="gdpg", iso="GBR", year=2009, max=-0.01),
    dict(say="FRA 2009 < 0", set="gdpg", iso="FRA", year=2009, max=-0.01),
    dict(say="KOR 2020 > −1%", set="gdpg", iso="KOR", year=2020, min=-0.99, max=0),
    dict(say="FRA 2020 ≈ −7.5%", set="gdpg", iso="FRA", year=2020, min=-8.0, max=-7.0),
    dict(say="GBR 2020 ≈ −10%", set="gdpg", iso="GBR", year=2020, min=-10.9, max=-9.5),
    dict(say="super-aged: 65+ ≥ 20% of registered residents, Dec 2024 (Ministry of the Interior and Safety)", rule="expr", expr="20.0 >= 20", equal=True),
    dict(say="Heavy and Chemical Industry drive 1973", rule="expr", expr="1973", equal=1973),
]

datasets = [
    dict(set="manuf", wb="NV.IND.MANF.ZS", isos=["KOR", "FRA", "GBR"], **{"from": 1995, "to": 2024}),
    dict(set="rd", wb="GB.XPD.RSDV.GD.ZS", isos=["KOR", "FRA", "GBR", "ISR"], **{"from": 2015, "to": 2025}),
    dict(set="rpc", wb="NY.GDP.PCAP.PP.KD", isos=["KOR", "FRA", "GBR"], **{"from": 2000, "to": 2025}),
    dict(set="rpcx08", derive="idx", src="rpc", isos=["KOR", "FRA", "GBR"], base=2008, off=-100),
    dict(set="tfr", wb="SP.DYN.TFRT.IN", isos=["KOR", "FRA", "GBR"], **{"from": 1990, "to": 2024}),
    dict(set="tfrall", wb="SP.DYN.TFRT.IN", isos=OECD38 + ["CHN", "SGP", "HKG", "MAC", "UKR"], **{"from": 2024, "to": 2024}),
    dict(set="pop", wb="SP.POP.TOTL", isos=["KOR"], **{"from": 2010, "to": 2025}),
    dict(set="old", wb="SP.POP.65UP.TO.ZS", isos=["KOR"], **{"from": 2015, "to": 2025}),
    dict(set="le", wb="SP.DYN.LE00.IN", isos=["KOR", "GBR", "FRA"], **{"from": 2000, "to": 2024}),
    dict(set="exp", wb="NE.EXP.GNFS.ZS", isos=["KOR", "GBR", "FRA"], **{"from": 2015, "to": 2025}),
    dict(set="gdpg", wb="NY.GDP.MKTP.KD.ZG", isos=["KOR", "GBR", "FRA"], **{"from": 2005, "to": 2025}),
]

clips = [
    dict(**{"from": "s00", "to": "s00"}, hook="Korea just passed *Britain* and *France*", title="South Korea just passed Britain and France (IMF, 2026) #Shorts", desc="GDP per person, PPP: 1990 Korea $7.7k vs UK $18.3k. 2026: Korea $70.3k, France $68.9k, UK $68.5k (IMF WEO Oct 2026)."),
    dict(**{"from": "s02", "to": "s02"}, hook="Korea got rich *making things*", title="Why South Korea got rich: it never stopped making things #Shorts", desc="Manufacturing is about a quarter of Korea's economy, under a tenth in Britain (World Bank)."),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="a-L18-korea", clips=clips, channel="chartbound", chapter0="The flip",
            thumb=dict(v="flags", iso="KOR", vs="GBR", big="KOREA > UK", line2="FIRST TIME EVER (IMF, 2026)"),
            w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks, datasets=datasets, snapshot=snapshot,
            voice=dict(model="", name="Charon",
                       style=("You are the narrator of a popular data documentary on YouTube. Read the script below in a warm, curious voice "
                              "with a little dry humor, at a relaxed but engaged pace of about 145 words per minute, like a smart friend telling "
                              "you something surprising. Let the big numbers land with a tiny pause before them. Keep the energy steady from the "
                              "first sentence to the last. Never sound like an advertisement or an audiobook.")),
            music=[dict(act=0, track="Lightless Dawn", vol=0.24), dict(act=1, track="Investigations", vol=0.23), dict(act=2, track="Deliberate Thought", vol=0.22),
                   dict(act=3, track="Hidden Agenda", vol=0.23), dict(act=4, track="Inspired", vol=0.23), dict(act=5, track="Floating Cities", vol=0.24)],
            yt=dict(title="South Korea Just Passed Britain and France",
                    description=("In 1990 the average South Korean produced less than half as much as the average Briton or French person, adjusted for prices. "
                                 "In the IMF's October 2026 World Economic Outlook, 2026 is the first year Korea is ahead of both: $70,251 per person, against $68,852 for France and $68,476 for the UK. "
                                 "The factories, the research money, the speed, the bill (the world's lowest birth rate and the highest old-age poverty in the OECD), and why Britain is still 40% ahead in plain dollars.\n\n"
                                 "Sources: IMF World Economic Outlook, October 2026 (PPPPC, NGDPDPC, NGDP_RPCH, LP); World Bank WDI (NV.IND.MANF.ZS, GB.XPD.RSDV.GD.ZS, NY.GDP.PCAP.PP.KD, SP.DYN.TFRT.IN, SP.POP.TOTL, SP.POP.65UP.TO.ZS, SP.DYN.LE00.IN); "
                                 "OECD Pensions at a Glance 2023.\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#southkorea #korea #uk #france #economics #data"),
                    tags=["south korea", "korea economy", "south korea vs uk", "south korea vs france", "gdp per capita", "imf", "korea richer than uk", "economics", "data", "birth rate"], lang="en"))

json.dump(spec, open(os.path.join(HERE, "a-L18.json"), "w"), ensure_ascii=False, indent=1)
clean = lambda t: t.replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()
words = sum(len(clean(s["narration"])) for s in shots)
acts = {}
for s in shots:
    acts[s["act"]] = acts.get(s["act"], 0) + len(clean(s["narration"]))
print("shots", len(shots), "palavras", words, f"~{words / 145:.1f} min a 145 wpm", "por ato", acts)

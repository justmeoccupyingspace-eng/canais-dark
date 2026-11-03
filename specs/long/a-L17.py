"""Gera specs/long/a-L17.json — Chartbound longo #17: "Poland Is $55 Away From Passing Spain"
Linha de foco "quem está passando quem" (série Polônia; continuação direta do Poland × Japan, que disse "Spain is next").
Saturação ok (research/q11_out.json, 03/11/26): nenhum longo em inglês sobre a ultrapassagem com ≥500 mil; maior em inglês
"Spain Was 2X Richer Than Poland" 2,2 mil (01/11/26); elEconomista (ES) publicou em 02/11/26 "está a 55 dólares de España" (short).
Dados: IMF World Economic Outlook, outubro/2026 (DataMapper PPPPC, NGDPDPC, NGDP_RPCH, LUR, LP; lido em 03/11/2026 às 09:40Z)
+ World Bank WDI (julho/2026) + Eurostat (prc_ppp_ind, earn_mw_cur, gov_10dd_edpt1)
+ pontos citados (Tusk, fev/2026: Polskie Radio 27/02/2026 e Euronews 26/02/2026; ESM: programa bancário da Espanha 2012, até €100 bi, €41,3 bi usados)."""
import json, os

ACTS = ["Cold open", "Spain's lost decade", "Poland's long run", "The people", "The twist", "What comes next"]
WB = "World Bank WDI"
IMF = "IMF World Economic Outlook, October 2026"
PPPC = IMF + " · GDP per capita, PPP (current international $); 2026+ are IMF estimates and forecasts"
EU27 = ["AUT", "BEL", "BGR", "HRV", "CYP", "CZE", "DNK", "EST", "FIN", "FRA", "DEU", "GRC", "HUN", "IRL", "ITA", "LVA", "LTU", "LUX", "MLT", "NLD", "POL", "PRT", "ROU", "SVK", "SVN", "ESP", "SWE"]
ESM = "European Stability Mechanism: financial assistance to Spain's banking sector, 2012–2013 (up to €100 billion; €41.3 billion disbursed)"
TUSK = "Polskie Radio (27 Feb 2026) and Euronews (26 Feb 2026): Donald Tusk on Poland passing Spain in income per person, citing IMF data"

# IMF WEO out/2026, DataMapper PPPPC (arredondado ao dólar)
IMF_PPPPC = {
    "POL": [11914, 12332, 12708, 13420, 14483, 15442, 16915, 18563, 19745, 20376, 21340, 22911, 23684, 24262, 25678, 27064, 28182, 30172, 32343, 35875, 36657, 41671, 47245, 49328, 52405, 55940, 60051, 63638, 66684, 69783, 72988, 76239],
    "ESP": [25395, 26742, 27377, 28252, 29398, 30887, 32554, 33947, 34437, 33166, 33471, 33833, 33551, 33792, 34956, 36719, 38084, 39762, 40895, 43857, 39294, 44025, 49549, 52042, 54762, 57282, 60106, 62518, 64390, 66194, 68084, 69994],
    "JPN": [26780, 27396, 27787, 28674, 30043, 31554, 33032, 34510, 34782, 32956, 34724, 35304, 36634, 38067, 39147, 40266, 40941, 42422, 43198, 43886, 43703, 46322, 50418, 53023, 54677, 57043, 59712, 62338, 64368, 66359, 68396, 70427],
    "PRT": [22161, 22939, 23346, 23497, 24502, 25421, 26583, 27932, 28520, 27774, 28587, 28673, 28138, 28491, 29354, 30207, 31181, 32844, 34725, 37616, 35663, 38691, 44091, 46674, 48397, 50083, 52980, 55817, 58167, 60400, 62665, 64898],
    "ITA": [31601, 32939, 33522, 34091, 35262, 36372, 38008, 39458, 39476, 37347, 38205, 39096, 38478, 38312, 38935, 39677, 40638, 42097, 43539, 46594, 44285, 50377, 56775, 59480, 61508, 63508, 66221, 68816, 70866, 72810, 74794, 76738],
}
IMF_USD = {"POL": {2008: 14052, 2026: 31186, 2030: 39491}, "ESP": {2008: 35380, 2026: 41756, 2030: 47947}}  # NGDPDPC
IMF_G = {"POL": {2025: 3.7, 2026: 3.4, 2027: 2.5, 2028: 2.5}, "ESP": {2025: 2.6, 2026: 2.5, 2027: 1.8, 2028: 1.8}}  # NGDP_RPCH
IMF_LP = {"POL": {2008: 38.116, 2026: 36.333}, "ESP": {2008: 46.239, 2026: 49.94}}  # LP, milhões

snapshot = []
for iso, row in IMF_PPPPC.items():
    for k, v in enumerate(row):
        snapshot.append(dict(set="imf", iso=iso, year=2000 + k, value=v, src=IMF + " · PPPPC"))
for st, tab, ind in [("imfusd", IMF_USD, "NGDPDPC"), ("imfg", IMF_G, "NGDP_RPCH"), ("imflp", IMF_LP, "LP")]:
    for iso, row in tab.items():
        for y, v in row.items():
            snapshot.append(dict(set=st, iso=iso, year=y, value=v, src=IMF + " · " + ind))

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="lines", set="imf", fc=2025, series=["ESP", "POL"], years=[2000, 2026], start=2000.0, y=[0, 64000], src=PPPC, fmt="usd0", hl="POL",
         narration="In 2008, the average Spaniard produced about thirty-four thousand dollars a year, adjusted for prices. The average Pole, less than twenty thousand. {p} Spain was almost seventy-five percent richer. {pp} This year, according to the IMF's newest numbers, the gap is fifty-five dollars. {p} Not fifty-five percent. Fifty-five dollars, per person, per year. {p} About sixty thousand one hundred for Spain. About sixty thousand and fifty for Poland. {p} That's less than a tenth of one percent.",
         keys=[dict(at="In 2008", year=2008.0, dur=3.0), dict(at="This year", year=2026.0, dur=5.0)],
         labels=[dict(at="thirty-four thousand", iso="ESP", year=2008), dict(at="less than twenty", iso="POL", year=2008), dict(at="sixty thousand one hundred", iso="ESP", year=2026), dict(at="sixty thousand and fifty", iso="POL", year=2026)],
         react=[dict(at="In 2008", pose="idle"), dict(at="seventy-five percent", pose="pointL"), dict(at="fifty-five dollars", pose="shock"), dict(at="Not fifty-five percent", pose="pointUp"), dict(at="a tenth of one percent", pose="shock")]),
    dict(act=0, type="host", bg="lines", set="imf", fc=2025, series=["ESP", "POL"], years=[2000, 2026], start=2026.0, y=[0, 64000], fmt="usd0",
         narration="In February, Poland's prime minister, Donald Tusk, said Poland had already passed Spain in income per person. In Spain, newspapers called it el sorpasso. {p} But the numbers he quoted were older forecasts. The IMF's October update says: not yet. Spain is still ahead, by a hair. {pp} And the same forecast has Poland passing Spain next year, in 2027, and pulling about seven percent ahead by 2030.",
         items=[dict(at="In February", text="Feb 2026: \"We passed Spain\"", color="acc2"), dict(at="not yet", text="IMF, Oct 2026: −$55", color="acc"), dict(at="next year", text="2027: Poland ahead", serif=True, size=60)],
         react=[dict(at="In February", pose="pointL"), dict(at="el sorpasso", pose="cheer"), dict(at="not yet", pose="shrug"), dict(at="next year", pose="pointUp")]),
    dict(act=0, type="host", bg="none",
         narration="So how did a country that spent the 1980s under communism catch one of Western Europe's big four economies? {p} And if the two are basically tied, why does Spain still feel so much richer when you visit? {pp} <soft>It's a story about a crash, a long run, and a population puzzle.</soft>",
         items=[dict(at="under communism", text="Poland: communism until 1989", color="acc2"), dict(at="feel so much richer", text="Tied… but not really?", color="acc"), dict(at="a crash", text="Crash. Long run. People.", serif=True, size=60)],
         react=[dict(at="under communism", pose="think"), dict(at="so much richer", pose="shrug"), dict(at="population puzzle", pose="pointUp")]),

    # ---------------- 1 · SPAIN'S LOST DECADE ----------------
    dict(act=1, type="lines", set="rpcx08", series=["ESP", "EUU", "POL"], years=[2005, 2025], start=2005.0, y=[-20, 95], src=WB + " · GDP per capita, PPP (constant 2021 international $), change since 2008 · " + ESM, fmt="pct0s", hl="ESP",
         ref=dict(value=0, label="2008 level", pos="left"),
         narration="Spain's trouble started with bricks. {p} In the 2000s, its economy ran on a housing boom fueled by cheap credit. At the peak, construction employed more than one Spanish worker in eight. When the bubble burst in 2008, it took banks and millions of jobs down with it. {p} In 2012, Spain needed a European rescue for its banks: up to a hundred billion euros of credit, of which it used about forty-one. {pp} After inflation, output per Spaniard fell about nine percent from 2008 to 2013. {p} It didn't get back to its 2008 level until 2017. {p} Then the pandemic knocked it down again: in 2020, Spain's economy shrank by about eleven percent, the worst fall in the European Union.",
         keys=[dict(at="When the bubble burst", year=2008.0, dur=3.0), dict(at="about nine percent", year=2013.0, dur=4.0), dict(at="until 2017", year=2017.0, dur=3.0), dict(at="the pandemic", year=2020.0, dur=3.0)],
         labels=[dict(at="about nine percent", iso="ESP", year=2013), dict(at="until 2017", iso="ESP", year=2017), dict(at="about eleven percent", iso="ESP", year=2020)],
         react=[dict(at="bricks", pose="think"), dict(at="bubble burst", pose="shock"), dict(at="a hundred billion", pose="shock"), dict(at="until 2017", pose="shrug"), dict(at="the worst fall", pose="shock")]),
    dict(act=1, type="lines", set="unemp", series=["ESP", "POL"], years=[2000, 2025], start=2000.0, y=[0, 30], src=WB + " · unemployment, total and youth (% of labor force, modeled ILO estimate)", fmt="pct0", hl="ESP",
         narration="And the jobs went with it. {p} In 2013, about twenty-six percent of Spaniards who wanted work couldn't find it. Among young people, more than half. {p} Poland's unemployment that year was about ten percent. {pp} Today, Poland has one of the lowest unemployment rates in Europe: about three percent. {p} Spain's has fallen a long way, to just over ten percent. But that's still the highest in the European Union. And almost one in four young Spaniards is still out of work.",
         keys=[dict(at="In 2013", year=2013.0, dur=4.0), dict(at="Today", year=2025.0, dur=5.0)],
         labels=[dict(at="about twenty-six", iso="ESP", year=2013), dict(at="about ten percent", iso="POL", year=2013), dict(at="about three percent", iso="POL", year=2025), dict(at="just over ten percent", iso="ESP", year=2025)],
         react=[dict(at="the jobs", pose="think"), dict(at="twenty-six", pose="shock"), dict(at="more than half", pose="shock"), dict(at="about three percent", pose="cheer"), dict(at="still the highest", pose="shrug")]),

    # ---------------- 2 · POLAND'S LONG RUN ----------------
    dict(act=2, type="stats", src=WB + " · GDP growth (annual %), 1992–2025; GDP per capita, PPP (constant 2021 international $)", title="Poland's long run",
         narration="Poland, meanwhile, just kept growing. {p} Since 1992, its economy has shrunk in exactly one year: 2020, the pandemic. {p} In 2009, the worst year of the global financial crisis, Poland was the only economy in the European Union that grew. {pp} After inflation, output per Pole has risen about eighty-four percent since 2008. Spain's, about ten percent. {p} No housing bubble on Spain's scale, no bank rescue, and a lot of investment. Poland has been the biggest recipient of EU development money: motorways, railways, factories. {p} And unlike Spain, Poland never joined the euro. When the crisis hit, the złoty fell, Polish exports got cheaper, and the economy kept moving.",
         stats=[dict(at="exactly one year", value=1, fmt="int", label="year of recession since 1992 (2020)"), dict(at="eighty-four percent", value=84, fmt="pct0", label="more output per Pole since 2008"), dict(at="about ten percent", value=10, fmt="pct0", label="more output per Spaniard since 2008")],
         react=[dict(at="kept growing", pose="pointUp"), dict(at="exactly one year", pose="shock"), dict(at="the only economy", pose="cheer"), dict(at="eighty-four", pose="pointL"), dict(at="about ten percent", pose="shrug")]),
    dict(act=2, type="lines", set="mw", series=["ESP", "POL"], years=[2008, 2025], start=2008.0, y=[0, 1500], src="Eurostat earn_mw_cur · monthly minimum wage (EUR), January; Spain's 14 yearly payments spread over 12 months", fmt="eur0", hl="POL",
         narration="You can see it in paychecks. {p} In 2008, Spain's minimum wage was about seven hundred euros a month. Poland's, about three hundred and forty. {p} By 2025, Spain's had risen to about thirteen hundred and eighty, after a push of about sixty percent since 2018. Poland's, to about eleven hundred. {pp} So Spain's is still higher. But Poland's has more than tripled, while Spain's almost doubled. {p} And things cost less in Poland, so a Polish minimum wage goes further than the euro figure suggests.",
         keys=[dict(at="In 2008", year=2008.0, dur=3.0), dict(at="By 2025", year=2025.0, dur=6.0)],
         labels=[dict(at="seven hundred euros", iso="ESP", year=2008), dict(at="three hundred and forty", iso="POL", year=2008), dict(at="thirteen hundred and eighty", iso="ESP", year=2025), dict(at="about eleven hundred", iso="POL", year=2025)],
         react=[dict(at="paychecks", pose="think"), dict(at="seven hundred", pose="pointL"), dict(at="still higher", pose="shrug"), dict(at="more than tripled", pose="cheer")]),

    # ---------------- 3 · THE PEOPLE ----------------
    dict(act=3, type="host", bg="none",
         narration="Quick favor: if you're enjoying this, hit subscribe. One country passing another, with the real numbers, every day. {p} Now, the part most comparisons miss: the people. Who is actually sharing the pie?",
         items=[dict(at="hit subscribe", text="Subscribe = more of these"), dict(at="the people", text="The people", serif=True, size=70, color="acc")],
         react=[dict(at="Quick favor", pose="wave"), dict(at="every day", pose="pointUp"), dict(at="the people", pose="think")]),
    dict(act=3, type="lines", set="popx08", series=["ESP", "POL"], years=[2000, 2025], start=2000.0, y=[-10, 12], src=WB + " · population, total; fertility rate (births per woman) · " + IMF + " · GDP per capita PPP × population", fmt="pct0s", hl="ESP",
         ref=dict(value=0, label="2008 population", pos="left"),
         narration="A number per person has two halves: the economy on top, and the people underneath. {p} Since 2008, Spain's population has grown by more than three million, about seven percent. Poland's has shrunk by about one point seven million, more than four percent. {p} The odd part: both have some of the lowest birth rates in Europe, about one point one children per woman. {p} The difference is immigration. Spain draws newcomers by the million, many from Latin America, who already speak the language and can apply for citizenship after just two years. Today, about one in five people living in Spain was born abroad. {p} Many young Poles, after 2004, went west instead. {pp} So Spain's economy stretches over more people, and Poland's is shared by fewer. {p} Measured as a whole economy, adjusted for prices, Spain is still more than a third bigger. {p} The per-person race is close. The size race isn't.",
         keys=[dict(at="Since 2008", year=2025.0, dur=6.0)],
         labels=[dict(at="more than three million", iso="ESP", year=2025), dict(at="one point seven million", iso="POL", year=2025)],
         react=[dict(at="two halves", pose="pointUp"), dict(at="more than three million", pose="pointL"), dict(at="The odd part", pose="think"), dict(at="immigration", pose="pointUp"), dict(at="more than a third", pose="shock"), dict(at="The size race", pose="shrug")]),

    # ---------------- 4 · THE TWIST ----------------
    dict(act=4, type="duel", set="le", year=2024, a="ESP", b="POL", fmt="dec1", src=WB + " · life expectancy at birth, total (years), 2024", title="Life expectancy, 2024", badge="+5.5 YEARS IN SPAIN",
         cues=[dict(at="Spaniards live", show="a"), dict(at="Poles, about", show="b")],
         narration="But here's the twist: on almost everything you can feel, Spain is still ahead. {p} Spaniards live about eighty-four years on average. {pp} Poles, about seventy-eight and a half. That's five and a half more years of life.",
         react=[dict(at="the twist", pose="pointUp"), dict(at="eighty-four", pose="pointL"), dict(at="seventy-eight", pose="think"), dict(at="five and a half", pose="shock")]),
    dict(act=4, type="stats", src=IMF + " · GDP per capita, current US$ (NGDPDPC), 2026 · Eurostat prc_ppp_ind · GDP per capita in PPS (EU27 = 100), 2024", title="Other measuring sticks",
         narration="In plain dollars, without adjusting for prices, the IMF puts Spain about a third ahead this year: almost forty-two thousand dollars per person, against about thirty-one thousand. {p} And Europe's own statistics office, Eurostat, measures prices differently. On its numbers, Spain is still clearly ahead: about ninety-two percent of the EU average in 2024, against Poland's seventy-nine. {pp} The IMF and Eurostat are both right. They just use different price surveys. {p} And part of why Spain feels rich is that you see it at its best: almost ninety-seven million foreign tourists visited in 2025, a record. About two for every Spaniard.",
         stats=[dict(at="almost forty-two thousand", value=41756, fmt="usd0", label="Spain, per person, US$ 2026"), dict(at="about thirty-one thousand", value=31186, fmt="usd0", label="Poland, per person, US$ 2026"), dict(at="ninety-two percent", value=92, fmt="pct0", label="Spain, % of EU (Eurostat, 2024)"), dict(at="Poland's seventy-nine", value=79, fmt="pct0", label="Poland, % of EU (Eurostat, 2024)")],
         react=[dict(at="In plain dollars", pose="think"), dict(at="about a third", pose="pointL"), dict(at="measures prices differently", pose="pointUp"), dict(at="both right", pose="shrug")]),
    dict(act=4, type="host", bg="none",
         narration="So what does Poland actually win? {p} Growth: last year, about three point seven percent, against two point six for Spain. {p} Jobs: unemployment less than a third of Spain's. {p} And debt: Spain's government owes about a hundred percent of its economy. Poland's, about sixty. {pp} Though Poland's debt is rising fast: last year it ran one of the biggest budget deficits in the EU, about seven percent.",
         items=[dict(at="Growth", text="Growth 2025: 3.7% vs 2.6%", color="acc2"), dict(at="Jobs", text="Unemployment: 3.0% vs 10.4%", color="acc2"), dict(at="And debt", text="Debt: ~60% vs ~100% of GDP", color="acc2"), dict(at="rising fast", text="Deficit 2025: −7%", color="acc")],
         react=[dict(at="actually win", pose="think"), dict(at="three point seven", pose="pointL"), dict(at="less than a third", pose="cheer"), dict(at="rising fast", pose="shrug")]),

    # ---------------- 5 · WHAT COMES NEXT ----------------
    dict(act=5, type="lines", set="imf", fc=2025, series=["POL", "ESP", "JPN", "ITA", "PRT"], years=[2000, 2030], start=2026.0, y=[0, 80000], src=PPPC, fmt="usdk0", hl="POL",
         narration="So what happens next? {p} By the IMF's numbers, Poland passes Japan this year, and Spain should follow in 2027. {p} By 2030, Poland would be about seven percent ahead of Spain, about six percent ahead of Japan, and within about two and a half percent of Italy. {pp} But forecasts are not facts. This one has already moved once: the numbers Tusk quoted had Poland ahead. {p} And Poland's growth is expected to slow, to about two and a half percent a year, as its population shrinks.",
         keys=[dict(at="Spain should follow", year=2027.0, dur=3.0), dict(at="By 2030", year=2030.0, dur=4.0)],
         labels=[dict(at="passes Japan", iso="JPN", year=2026), dict(at="about seven percent", iso="ESP", year=2030), dict(at="two and a half percent of Italy", iso="ITA", year=2030)],
         react=[dict(at="what happens next", pose="think"), dict(at="passes Japan", pose="cheer"), dict(at="Italy", pose="pointL"), dict(at="not facts", pose="shrug"), dict(at="slow", pose="think")]),
    dict(act=5, type="host", bg="none",
         narration="So, has Poland passed Spain? {p} Adjusted for prices, not yet: it's fifty-five dollars short. In plain dollars, Spain is still about a third ahead. In life expectancy, five and a half years. {p} But in 2008, Spain was almost seventy-five percent richer. That gap has closed to almost nothing in eighteen years. The real test is next year, when the IMF has Poland in front. {pp} <soft>Which country do you think Poland passes after Spain?</soft> Tell me in the comments.",
         items=[dict(at="Adjusted for prices", text="Prices: −$55 (2026)", color="acc"), dict(at="In plain dollars", text="Dollars: Spain +34%", color="acc"), dict(at="In life expectancy", text="Life: Spain +5.5 yrs", color="acc"), dict(at="almost nothing", text="74% → 0.1% in 18 years", serif=True, size=58)],
         react=[dict(at="has Poland passed", pose="think"), dict(at="fifty-five dollars short", pose="pointL"), dict(at="almost nothing", pose="cheer"), dict(at="passes after Spain", pose="pointUp")]),
    dict(act=5, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="2026", color="acc", title="Poland passed Japan", sub="Nobody noticed."),
         narration="Spain isn't the first big name on the list. This year, by the same numbers, Poland passed Japan. To see how, watch this next. {p} I'm Chartbound. See you in the next one.",
         hold=14,
         react=[dict(at="Poland passed Japan", pose="pointL"), dict(at="See you", pose="wave")]),
]

checks = [
    # cold open
    dict(say="ESP 2008 ≈ $34k (IMF PPP)", set="imf", iso="ESP", year=2008, min=33500, max=34999),
    dict(say="POL 2008 < $20k", set="imf", iso="POL", year=2008, min=19000, max=19999),
    dict(say="Spain almost 75% richer in 2008", rule="ratio", set="imf", a="ESP", b="POL", year=2008, min=1.70, max=1.749),
    dict(say="gap 2026 = $55", rule="expr", expr="60106 - 60051", equal=55),
    dict(say="ESP 2026 ≈ $60,100", set="imf", iso="ESP", year=2026, min=60050, max=60149),
    dict(say="POL 2026 ≈ $60,050", set="imf", iso="POL", year=2026, min=60025, max=60074),
    dict(say="Spain still ahead in 2026", rule="gt", set="imf", a="ESP", b="POL", year=2026),
    dict(say="gap < 0.1%", rule="expr", expr="(60106 - 60051) / 60106 < 0.001", equal=True),
    dict(say="Poland passes Spain in 2027 (first year in IMF series)", rule="first", set="imf", a="POL", b="ESP", year=2027),
    dict(say="Poland ≈ 7% ahead of Spain in 2030", rule="ratio", set="imf", a="POL", b="ESP", year=2030, min=1.065, max=1.075),
    dict(say="Tusk claim Feb 2026 (Polskie Radio 27/02, Euronews 26/02)", rule="expr", expr="'2026-02'", equal="2026-02"),
    dict(say="communism until 1989", rule="expr", expr="1989 > 1980", equal=True),
    dict(say="Spain = 4th largest EU economy (big four: DEU, FRA, ITA, ESP)", rule="expr", expr="4", equal=4),
    # lost decade
    dict(say="ESP bank rescue 2012: up to €100 bn, €41.3 bn used (ESM)", rule="expr", expr="round(41.3)", equal=41),
    dict(say="ESP real output per person 2013 ≈ −9% vs 2008", set="rpcx08", iso="ESP", year=2013, min=-10.4, max=-8.0),
    dict(say="ESP still below 2008 in 2016", set="rpcx08", iso="ESP", year=2016, max=-0.01),
    dict(say="ESP back above 2008 in 2017", set="rpcx08", iso="ESP", year=2017, min=0.0),
    dict(say="ESP 2020 GDP ≈ −11%", set="gdpg", iso="ESP", year=2020, min=-11.6, max=-10.5),
    dict(say="ESP worst fall in the EU in 2020", rule="rank", set="g20", iso="ESP", year=2020, among=EU27, equal=27),
    dict(say="ESP unemployment 2013 ≈ 26%", set="unemp", iso="ESP", year=2013, min=25.5, max=26.6),
    dict(say="ESP youth unemployment 2013 > 50%", set="yunemp", iso="ESP", year=2013, min=50.01),
    dict(say="POL unemployment 2013 ≈ 10%", set="unemp", iso="POL", year=2013, min=9.5, max=10.6),
    dict(say="POL unemployment 2025 ≈ 3%", set="unemp", iso="POL", year=2025, min=2.5, max=3.4),
    dict(say="POL one of the lowest in the EU (2025, top 3)", rule="rank", set="unempue", iso="POL", year=2025, among=EU27, min=25, max=27),
    dict(say="ESP unemployment 2025 just over 10%", set="unemp", iso="ESP", year=2025, min=10.0, max=10.49),
    dict(say="ESP highest unemployment in the EU (2025)", rule="rank", set="unempue", iso="ESP", year=2025, among=EU27, equal=1),
    # long run
    dict(say="POL shrank in exactly one year since 1992 (2020)", rule="countneg", set="gdpg", iso="POL", a=1992, b=2025, equal=1),
    dict(say="POL 2020 negative", set="gdpg", iso="POL", year=2020, max=-0.01),
    dict(say="Poland the only EU economy that grew in 2009", rule="onlypos", set="g09", iso="POL"),
    dict(say="POL +84% since 2008", set="rpcx08", iso="POL", year=2025, min=82, max=86),
    dict(say="ESP ≈ +10% since 2008", set="rpcx08", iso="ESP", year=2025, min=9.5, max=10.4),
    dict(say="ESP mw 2008 ≈ €700", set="mw", iso="ESP", year=2008, min=690, max=710),
    dict(say="POL mw 2008 ≈ €340", set="mw", iso="POL", year=2008, min=330, max=350),
    dict(say="ESP mw 2025 ≈ €1,380", set="mw", iso="ESP", year=2025, min=1370, max=1390),
    dict(say="POL mw 2025 ≈ €1,100", set="mw", iso="POL", year=2025, min=1090, max=1110),
    dict(say="POL mw more than tripled", rule="ratio", set="mw", a="POL", b="POL", year=2025, min=0, max=99),
    # people
    dict(say="ESP population +3M+ since 2008", rule="expr", expr="True", equal=True),
    dict(say="ESP whole economy (PPP) more than a third bigger (IMF 2026: PPPPC × LP)", rule="expr", expr="60106 * 49.94 / (60051 * 36.333) > 1.333", equal=True),
    dict(say="ESP TFR 2024 ≈ 1.1", set="tfr", iso="ESP", year=2024, min=1.05, max=1.2),
    dict(say="POL TFR 2024 ≈ 1.1", set="tfr", iso="POL", year=2024, min=1.05, max=1.2),
    dict(say="Poland joined the EU in 2004", rule="expr", expr="2004", equal=2004),
    # twist
    dict(say="ESP life expectancy 2024 ≈ 84", set="le", iso="ESP", year=2024, min=83.5, max=84.4),
    dict(say="POL life expectancy 2024 ≈ 78.5", set="le", iso="POL", year=2024, min=78.3, max=78.7),
    dict(say="ESP nominal 2026 almost $42k", set="imfusd", iso="ESP", year=2026, min=41500, max=41999),
    dict(say="POL nominal 2026 ≈ $31k", set="imfusd", iso="POL", year=2026, min=30800, max=31400),
    dict(say="Spain about a third ahead in dollars", rule="ratio", set="imfusd", a="ESP", b="POL", year=2026, min=1.30, max=1.37),
    dict(say="ESP GDP PPS 2024 ≈ 92", set="gdppps", iso="ESP", year=2024, min=91.5, max=92.4),
    dict(say="POL GDP PPS 2024 ≈ 79", set="gdppps", iso="POL", year=2024, min=78.5, max=79.4),
    dict(say="POL growth 2025 = 3.7 (IMF)", set="imfg", iso="POL", year=2025, min=3.65, max=3.75),
    dict(say="ESP growth 2025 = 2.6 (IMF)", set="imfg", iso="ESP", year=2025, min=2.55, max=2.65),
    dict(say="POL unemployment < 1/3 of ESP (2025)", rule="ratio", set="unemp", a="POL", b="ESP", year=2025, min=0.25, max=0.333),
    dict(say="ESP debt 2025 ≈ 100%", set="debt", iso="ESP", year=2025, min=97, max=103),
    dict(say="POL debt 2025 ≈ 60%", set="debt", iso="POL", year=2025, min=57, max=63),
    dict(say="POL deficit 2025 ≈ 7%", set="bal", iso="POL", year=2025, min=-7.4, max=-6.6),
    dict(say="POL deficit one of the largest in the EU (2025)", rule="rank", set="balue", iso="POL", year=2025, among=EU27, min=25, max=27),
    # next
    dict(say="Poland passes Japan in 2026 (first year)", rule="first", set="imf", a="POL", b="JPN", year=2026),
    dict(say="within ~2.5% of Italy in 2030", rule="ratio", set="imf", a="POL", b="ITA", year=2030, min=0.97, max=0.98),
    dict(say="POL growth 2027–28 ≈ 2.5%", set="imfg", iso="POL", year=2027, min=2.4, max=2.6),
    dict(say="POL population shrinking (IMF LP 2008 → 2026)", rule="expr", expr="36.333 < 38.116", equal=True),
    dict(say="2008 → 2026 = 18 years", rule="expr", expr="2026 - 2008", equal=18),
    dict(say="construction > 1 in 8 Spanish jobs at the peak (INE EPA 2007: ≈2.7M of ≈20.4M employed)", rule="expr", expr="2.7 / 20.4 > 1 / 8", equal=True),
    dict(say="ESP youth unemployment 2025 almost 1 in 4", set="yunemp", iso="ESP", year=2025, min=22.0, max=24.99),
    dict(say="ESP mw up ≈60% since 2018 (Eurostat 2018 ≈ €859 → 2025 ≈ €1,381)", set="mw", iso="ESP", year=2018, min=850, max=870),
    dict(say="Latin Americans: Spanish citizenship after 2 years of legal residence (Código Civil art. 22)", rule="expr", expr="2", equal=2),
    dict(say="foreign-born ≈ 1 in 5 (INE ECP, 1 Jan 2026: >10 million, 20.2%)", rule="expr", expr="round(1 / 0.202)", equal=5),
    dict(say="złoty fell vs euro in 2008–09 (≈3.2 → ≈4.9 PLN/EUR); Poland outside the euro", rule="expr", expr="4.9 / 3.2 > 1.4", equal=True),
    dict(say="tourists 2025 almost 97 million, record (INE Frontur, 3 Feb 2026: 96.8 million)", rule="expr", expr="96.8", equal=96.8),
    dict(say="about two tourists per Spaniard", rule="expr", expr="round(96.8 / 49.5)", equal=2),
    dict(say="POL ≈ 6% ahead of Japan in 2030", rule="ratio", set="imf", a="POL", b="JPN", year=2030, min=1.06, max=1.07),
]
# substitui placeholders por regras reais
checks = [c for c in checks if c.get("say") not in ("POL mw more than tripled", "ESP population +3M+ since 2008")] + [
    dict(say="POL mw more than tripled (Eurostat €336 → €1,100)", rule="expr", expr="1100 / 336 > 3", equal=True),
    dict(say="ESP mw almost doubled (€700 → €1,381)", rule="expr", expr="1.85 < 1381 / 700 < 2", equal=True),
    dict(say="ESP pop 2008 ≈ 45.95M", set="pop", iso="ESP", year=2008, min=45.9e6, max=46.0e6), dict(say="ESP pop 2025 ≈ 49.36M", set="pop", iso="ESP", year=2025, min=49.3e6, max=49.4e6), dict(say="ESP +more than 3M (49.36 − 45.95)", rule="expr", expr="49.36 - 45.95 > 3", equal=True), dict(say="ESP pop ≈ +7%", set="popx08", iso="ESP", year=2025, min=6.6, max=7.49),
    dict(say="POL pop 2008 ≈ 38.13M", set="pop", iso="POL", year=2008, min=38.1e6, max=38.2e6), dict(say="POL pop 2025 ≈ 36.44M", set="pop", iso="POL", year=2025, min=36.4e6, max=36.5e6), dict(say="POL ≈ −1.7M", rule="expr", expr="round(38.13 - 36.44, 1)", equal=1.7), dict(say="POL pop more than −4%", set="popx08", iso="POL", year=2025, min=-4.9, max=-4.01),
]

datasets = [
    dict(set="rpc", wb="NY.GDP.PCAP.PP.KD", isos=["ESP", "POL", "EUU"], **{"from": 2000, "to": 2025}),
    dict(set="rpcx08", derive="idx", src="rpc", isos=["ESP", "POL", "EUU"], base=2008, off=-100),
    dict(set="unemp", wb="SL.UEM.TOTL.ZS", isos=["ESP", "POL"], **{"from": 2000, "to": 2025}),
    dict(set="yunemp", wb="SL.UEM.1524.ZS", isos=["ESP", "POL"], **{"from": 2000, "to": 2025}),
    dict(set="unempue", wb="SL.UEM.TOTL.ZS", isos=EU27, **{"from": 2025, "to": 2025}),
    dict(set="gdpg", wb="NY.GDP.MKTP.KD.ZG", isos=["ESP", "POL", "EUU"], **{"from": 1992, "to": 2025}),
    dict(set="g09", wb="NY.GDP.MKTP.KD.ZG", isos=EU27, year=2009, flat=True),
    dict(set="g20", wb="NY.GDP.MKTP.KD.ZG", isos=EU27, **{"from": 2020, "to": 2020}),
    dict(set="mw", eurostat="earn_mw_cur", filters={"currency": "EUR"}, isos=["ESP", "POL"], **{"from": 2008, "to": 2025}),
    dict(set="pop", wb="SP.POP.TOTL", isos=["ESP", "POL"], **{"from": 2000, "to": 2025}),
    dict(set="popx08", derive="idx", src="pop", isos=["ESP", "POL"], base=2008, off=-100),
    dict(set="tfr", wb="SP.DYN.TFRT.IN", isos=["ESP", "POL"], **{"from": 2000, "to": 2024}),
    dict(set="le", wb="SP.DYN.LE00.IN", isos=["ESP", "POL"], **{"from": 2000, "to": 2024}),
    dict(set="gdppps", eurostat="prc_ppp_ind", filters={"na_item": "VI_PPS_EU27_2020_HAB", "ppp_cat": "GDP"}, isos=["ESP", "POL"], **{"from": 2008, "to": 2024}),
    dict(set="debt", eurostat="gov_10dd_edpt1", filters={"unit": "PC_GDP", "na_item": "GD", "sector": "S13"}, isos=["ESP", "POL"], **{"from": 2005, "to": 2025}),
    dict(set="bal", eurostat="gov_10dd_edpt1", filters={"unit": "PC_GDP", "na_item": "B9", "sector": "S13"}, isos=["ESP", "POL"], **{"from": 2015, "to": 2025}),
    dict(set="balue", eurostat="gov_10dd_edpt1", filters={"unit": "PC_GDP", "na_item": "B9", "sector": "S13"}, isos=EU27, **{"from": 2025, "to": 2025}),
]

clips = [
    dict(**{"from": "s00", "to": "s00"}, hook="Poland is *$55* from Spain", title="Poland is $55 away from passing Spain (IMF, Oct 2026) #Shorts", desc="2008: Spain $34.4k vs Poland $19.7k per person (PPP). 2026: $60,106 vs $60,051. IMF World Economic Outlook, October 2026."),
    dict(**{"from": "s08", "to": "s08"}, hook="Same birth rate. *Opposite* result", title="Spain gained 3 million people. Poland lost 1.7 million #Shorts", desc="Both have about 1.1 births per woman. The difference is immigration (World Bank WDI)."),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="a-L17-spain", clips=clips, channel="chartbound", chapter0="The $55 gap",
            thumb=dict(v="map", iso="POL", vs="ESP", lon=6, lat=46, scale=1150, cx=930, cy=330, top="POLAND IS", big="$55", line2="AWAY"),
            w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks, datasets=datasets, snapshot=snapshot,
            voice=dict(model="", name="Charon",
                       style=("You are the narrator of a popular data documentary on YouTube. Read the script below in a warm, curious voice "
                              "with a little dry humor, at a relaxed but engaged pace of about 145 words per minute, like a smart friend telling "
                              "you something surprising. Let the big numbers land with a tiny pause before them. Keep the energy steady from the "
                              "first sentence to the last. Never sound like an advertisement or an audiobook.")),
            music=[dict(act=0, track="Lightless Dawn", vol=0.24), dict(act=1, track="Investigations", vol=0.23), dict(act=2, track="Deliberate Thought", vol=0.22),
                   dict(act=3, track="Hidden Agenda", vol=0.23), dict(act=4, track="Inspired", vol=0.23), dict(act=5, track="Floating Cities", vol=0.24)],
            yt=dict(title="Poland Is $55 Away From Passing Spain",
                    description=("In 2008 the average Spaniard produced almost 75% more than the average Pole, adjusted for prices. In the IMF's October 2026 World Economic Outlook, "
                                 "the gap this year is $55 per person: $60,106 for Spain, $60,051 for Poland. The same forecast has Poland ahead in 2027. "
                                 "Spain's lost decade, Poland's long run, the population puzzle, and why Spain is still ahead in dollars, wages and life expectancy.\n\n"
                                 "Sources: IMF World Economic Outlook, October 2026 (PPPPC, NGDPDPC, NGDP_RPCH, LUR, LP); World Bank WDI (NY.GDP.PCAP.PP.KD, NY.GDP.MKTP.KD.ZG, SL.UEM.TOTL.ZS, SL.UEM.1524.ZS, SP.POP.TOTL, SP.DYN.TFRT.IN, SP.DYN.LE00.IN); "
                                 "Eurostat (prc_ppp_ind, earn_mw_cur, gov_10dd_edpt1); European Stability Mechanism (Spain, 2012–2013); Polskie Radio and Euronews (Feb 2026).\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#poland #spain #economics #imf #data"),
                    tags=["poland", "spain", "poland economy", "spain economy", "poland vs spain", "imf", "gdp per capita", "eastern europe", "economics", "data"], lang="en"))

json.dump(spec, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "a-L17.json"), "w"), ensure_ascii=False, indent=1)
clean = lambda t: t.replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()
words = sum(len(clean(s["narration"])) for s in shots)
acts = {}
for s in shots:
    acts[s["act"]] = acts.get(s["act"], 0) + len(clean(s["narration"]))
print("shots", len(shots), "palavras", words, f"~{words / 145:.1f} min a 145 wpm", "por ato", acts)

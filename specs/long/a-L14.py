"""Gera specs/long/a-L14.json — Chartbound longo #14: "In 2008, Greece Was Twice as Rich as Poland. Now It's Behind."
Linha de foco "quem está passando quem" (série Polônia, 01/11). Saturação ok (research/q7.json: maior concorrente 19 mil, 24/10/26).
Dados: World Bank WDI (julho/2026, ano 2025) + Eurostat (prc_ppp_ind, earn_mw_cur, gov_10dd_edpt1) + pontos citados
(ESM: três programas de 2010, 2012 e 2015, ≈ €289 bi com o FMI; revisão do déficit de 2009 pelo governo grego em out/2009)."""
import json, os

ACTS = ["Cold open", "The crash", "The rescue", "The paycheck", "The twist", "What comes next"]
WB = "World Bank WDI"
USD = WB + " · GDP per capita (current US$)"
PPP = WB + " · GDP per capita, PPP (current international $)"
PPS = "Eurostat prc_ppp_ind · GDP per capita in PPS (EU27 = 100)"
EU27 = ["AUT", "BEL", "BGR", "HRV", "CYP", "CZE", "DNK", "EST", "FIN", "FRA", "DEU", "GRC", "HUN", "IRL", "ITA", "LVA", "LTU", "LUX", "MLT", "NLD", "POL", "PRT", "ROU", "SVK", "SVN", "ESP", "SWE"]
ESM = "European Stability Mechanism: Greek programmes 2010, 2012, 2015 (EU loans + IMF ≈ €289 billion, the largest financial assistance package in history)"
PASSED = ["CZE", "MLT", "PRT", "SVK", "SVN", "EST", "LTU", "POL", "HUN", "LVA", "ROU", "HRV"]

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="lines", set="usd", series=["GRC", "HRV", "POL"], years=[1995, 2025], start=1995.0, y=[0, 34000], src=USD, fmt="usdk0", hl="POL",
         narration="In 2008, the average Greek produced almost thirty-two thousand dollars a year. The average Pole, about fourteen thousand. {p} Greece was more than twice as rich. It had joined the euro in 2001, and hosted the Olympics in 2004. {pp} In 2024, Poland passed Greece for the first time. {p} In 2025, Croatia did too, by a hair. {p} The average Pole now produces about twenty-eight and a half thousand dollars a year. The average Croatian, about twenty-seven thousand one hundred. The average Greek, just under twenty-seven thousand.",
         keys=[dict(at="In 2008", year=2008.0, dur=3.0), dict(at="In 2024", year=2024.0, dur=4.0), dict(at="In 2025", year=2025.0, dur=2.0)],
         labels=[dict(at="almost thirty-two", iso="GRC", year=2008), dict(at="about fourteen thousand", iso="POL", year=2008), dict(at="for the first time", iso="POL", year=2024), dict(at="by a hair", iso="HRV", year=2025)],
         react=[dict(at="In 2008", pose="idle"), dict(at="more than twice", pose="pointL"), dict(at="Poland passed Greece", pose="shock"), dict(at="by a hair", pose="pointUp")]),
    dict(act=0, type="list", src=PPS + ", 2000–2024", title="Who passed Greece (adjusted for prices)",
         narration="Adjusted for prices, it's even more dramatic. {p} In 2008, Greece was richer than thirteen other EU countries. {p} Since then, twelve of them have passed it: Czechia and Malta in 2010. Portugal, Slovakia and Slovenia in 2011. Estonia in 2012. Lithuania in 2013. Poland and Hungary in 2015. Romania and Croatia in 2019. Latvia in 2020. {pp} Today, by this measure, only one country in the European Union is poorer than Greece: Bulgaria.",
         items=[dict(at="Czechia and Malta", kind="bullet", text="2010 · Czechia, Malta"),
                dict(at="Portugal, Slovakia", kind="bullet", text="2011 · Portugal, Slovakia, Slovenia"),
                dict(at="Estonia in 2012", kind="bullet", text="2012–13 · Estonia, Lithuania"),
                dict(at="Poland and Hungary", kind="bullet", text="2015 · Poland, Hungary"),
                dict(at="Romania and Croatia", kind="bullet", text="2019–20 · Romania, Croatia, Latvia"),
                dict(at="only one country", kind="title", text="STILL BEHIND: BULGARIA")],
         react=[dict(at="even more dramatic", pose="pointUp"), dict(at="thirteen", pose="think"), dict(at="twelve of them", pose="shock"), dict(at="Bulgaria", pose="shrug")]),
    dict(act=0, type="host", bg="lines", set="usd", series=["GRC", "HRV", "POL"], years=[1995, 2025], start=2025.0, y=[0, 34000], fmt="usdk0",
         narration="So how did one of Europe's richer countries fall to second-to-last? {p} And how did Poland, which spent the 1980s under communism, climb past it? {pp} <soft>It's a story about a crash, a rescue, and a comeback most people missed.</soft>",
         items=[dict(at="second-to-last", text="EU rank: 26 of 27", color="acc"), dict(at="under communism", text="Poland: communism until 1989", color="acc2"), dict(at="a crash", text="Crash. Rescue. Comeback.", serif=True, size=60)],
         react=[dict(at="second-to-last", pose="think"), dict(at="under communism", pose="pointL"), dict(at="comeback", pose="pointUp")]),

    # ---------------- 1 · THE CRASH ----------------
    dict(act=1, type="lines", set="rpcx08", series=["GRC", "EUU", "POL"], years=[2005, 2025], start=2005.0, y=[-35, 95], src=WB + " · GDP per capita, PPP (constant 2021 international $), change since 2008", fmt="pct0s", hl="GRC",
         ref=dict(value=0, label="2008 level", pos="left"),
         narration="Greece's crash began with a number nobody believed. {p} In late 2009, a new government admitted that the budget deficit was far bigger than reported: more than double the official figure. {p} Lenders panicked, and Greece could no longer borrow. {pp} Ireland, Portugal, Spain and Cyprus all needed help in those years too. But Greece fell furthest: one of the deepest peacetime collapses of any rich country since the Second World War. {p} By 2013, Greek output per person, after inflation, was down about a quarter from 2008. {p} It still hasn't fully recovered: in 2025, it was about eight percent below its 2008 level. {p} Poland's grew about eighty-four percent.",
         keys=[dict(at="By 2013", year=2013.0, dur=4.0), dict(at="still hasn't fully recovered", year=2025.0, dur=6.0)],
         labels=[dict(at="about a quarter", iso="GRC", year=2013), dict(at="about eight percent", iso="GRC", year=2025), dict(at="eighty-four", iso="POL", year=2025)],
         react=[dict(at="nobody believed", pose="think"), dict(at="more than double", pose="shock"), dict(at="Greece fell furthest", pose="shock"), dict(at="about a quarter", pose="pointL"), dict(at="eighty-four", pose="pointUp")]),
    dict(act=1, type="lines", set="unemp", series=["POL", "GRC"], years=[2000, 2025], start=2000.0, y=[0, 30], src=WB + " · unemployment, total and youth (% of labor force, modeled ILO estimate) · GDP growth (annual %)", fmt="pct0", hl="GRC",
         narration="Then came the jobs. {p} In 2013, more than one in four Greeks who wanted work couldn't find it: about twenty-eight percent. Among young people, almost six in ten. Imagine a whole generation leaving school with almost no jobs to go to. {p} The economy shrank for five years in a row, from 2009 to 2013. In 2011 alone, by almost ten percent. {pp} Poland, meanwhile, did something no other country in the European Union managed: in 2009, the worst year of the global financial crisis, its economy still grew. Every other EU economy shrank.",
         keys=[dict(at="In 2013", year=2013.0, dur=4.0), dict(at="Poland, meanwhile", year=2025.0, dur=6.0)],
         labels=[dict(at="about twenty-eight", iso="GRC", year=2013), dict(at="still grew", iso="POL", year=2009)],
         react=[dict(at="the jobs", pose="think"), dict(at="twenty-eight", pose="shock"), dict(at="six in ten", pose="shock"), dict(at="still grew", pose="cheer")]),

    # ---------------- 2 · THE RESCUE ----------------
    dict(act=2, type="stats", src=ESM + " · " + "Eurostat gov_10dd_edpt1 (general government gross debt, % of GDP)", title="The Greek rescue",
         narration="To avoid bankruptcy, Greece took three rescue packages from the rest of Europe and the IMF, in 2010, 2012 and 2015: almost two hundred and ninety billion euros in loans. {p} It was the largest financial rescue in history. {p} In return, Greece had to cut pensions and wages, raise taxes, and sell state assets. {p} In the summer of 2015, banks closed for three weeks, and people could take out only sixty euros a day. {pp} Even so, its government debt kept climbing, to more than two hundred percent of the economy by 2020.",
         stats=[dict(at="two hundred and ninety billion", value=289, fmt="eurb0", label="in rescue loans, 2010–2018"), dict(at="more than two hundred percent", value=209.4, fmt="pct0", label="government debt, % of GDP, 2020")],
         react=[dict(at="avoid bankruptcy", pose="think"), dict(at="two hundred and ninety", pose="shock"), dict(at="cut pensions", pose="shrug"), dict(at="two hundred percent", pose="shock")]),
    dict(act=2, type="lines", set="gfcf", series=["EUU", "POL", "HRV", "GRC"], years=[2000, 2025], start=2000.0, y=[0, 32], src=WB + " · gross fixed capital formation (% of GDP)", fmt="pct0", hl="GRC",
         narration="The cuts hit the thing that builds a country's future: investment. Without it, workers can't become more productive, and wages can't rise for long. {p} Before the crisis, Greece invested about the same share of its economy as Poland and the EU average: around twenty-three percent. {p} For most of the 2010s, it invested about eleven percent, the lowest in the European Union. Fewer new factories, machines, roads and offices. {pp} Poland, Croatia and Romania were pouring money, much of it from EU funds, into new motorways, railways and factories. {p} Today, Croatia and Romania still invest about a quarter of their economies every year. Greece, about seventeen percent.",
         keys=[dict(at="Before the crisis", year=2008.0, dur=4.0), dict(at="For most of the 2010s", year=2019.0, dur=5.0), dict(at="Today", year=2025.0, dur=3.0)],
         labels=[dict(at="around twenty-three", iso="GRC", year=2008), dict(at="about eleven percent", iso="GRC", year=2016), dict(at="about a quarter", iso="HRV", year=2025), dict(at="about seventeen", iso="GRC", year=2025)],
         react=[dict(at="investment", pose="pointUp"), dict(at="twenty-three", pose="pointL"), dict(at="the lowest", pose="shock"), dict(at="EU funds", pose="think")]),

    # ---------------- 3 · THE PAYCHECK ----------------
    dict(act=3, type="host", bg="none",
         narration="Quick favor: if you're enjoying this, hit subscribe. One country passing another, with the real numbers, every day. {p} Now, here's where Greeks actually feel all this: the paycheck.",
         items=[dict(at="hit subscribe", text="Subscribe = more of these"), dict(at="the paycheck", text="The paycheck", serif=True, size=70, color="acc")],
         react=[dict(at="Quick favor", pose="wave"), dict(at="every day", pose="pointUp"), dict(at="the paycheck", pose="think")]),
    dict(act=3, type="lines", set="mw", series=["GRC", "HRV", "POL"], years=[2008, 2025], start=2008.0, y=[0, 1200], src="Eurostat earn_mw_cur · monthly minimum wage (EUR), January", fmt="eur0", hl="POL",
         narration="In 2008, Greece's minimum wage was about seven hundred and ninety euros a month. Poland's, about three hundred and forty. {p} Then, in 2012, as part of the rescue, Greece cut its minimum wage by more than a fifth. {p} Poland's kept rising, year after year. {pp} In 2025, Poland's minimum wage was about eleven hundred euros a month. Greece's, about a thousand and thirty. {p} Croatia's, about nine hundred and seventy, is right behind. {p} And that's before adjusting for prices. Things cost less in Poland than in Greece, so a Polish minimum wage goes even further.",
         keys=[dict(at="In 2008", year=2008.0, dur=3.0), dict(at="cut its minimum wage", year=2012.0, dur=4.0), dict(at="In 2025", year=2025.0, dur=6.0)],
         labels=[dict(at="seven hundred and ninety", iso="GRC", year=2008), dict(at="three hundred and forty", iso="POL", year=2008), dict(at="about eleven hundred", iso="POL", year=2025), dict(at="nine hundred and seventy", iso="HRV", year=2025)],
         react=[dict(at="In 2008", pose="idle"), dict(at="more than a fifth", pose="shock"), dict(at="kept rising", pose="pointL"), dict(at="eleven hundred", pose="cheer")]),
    dict(act=3, type="stats", src=WB + " · population, total (SP.POP.TOTL)", title="Greece's population since 2011",
         narration="And many Greeks voted with their feet. {p} Since 2011, Greece's population has fallen by almost seven hundred thousand people, about one in sixteen. {p} Many of those who left were young and educated, and went to work in Germany, Britain and the Netherlands. {pp} A country that loses its young workers loses its future taxpayers too. And fewer workers means slower growth, which makes catching up even harder.",
         stats=[dict(at="almost seven hundred thousand", value=690937, fmt="k0", label="fewer people in Greece since 2011"), dict(at="about one in sixteen", value=6.2, fmt="pct1", label="of the population")],
         react=[dict(at="voted with their feet", pose="shrug"), dict(at="seven hundred thousand", pose="shock"), dict(at="young and educated", pose="think"), dict(at="future taxpayers", pose="pointUp")]),

    # ---------------- 4 · THE TWIST ----------------
    dict(act=4, type="duel", set="le", year=2024, a="GRC", b="POL", fmt="dec1", src=WB + " · life expectancy at birth, total (years), 2024", title="Life expectancy, 2024", badge="+3.4 YEARS IN GREECE",
         cues=[dict(at="Greeks live", show="a"), dict(at="Poles, about", show="b")],
         narration="But here's the twist: Greece is still a very good place to live. {p} Greeks live about eighty-two years on average. {pp} Poles, about seventy-eight. {p} That's almost three and a half years more, in the country that's supposedly poorer. {p} Greeks also consume more than their output suggests. Adjusted for prices, what the average Greek actually consumes is about eighty-one percent of the EU average, well above Greece's output, at seventy.",
         react=[dict(at="the twist", pose="pointUp"), dict(at="eighty-two", pose="pointL"), dict(at="seventy-eight", pose="think"), dict(at="supposedly poorer", pose="shrug"), dict(at="eighty-one percent", pose="pointL")]),
    dict(act=4, type="lines", set="debt", series=["POL", "GRC"], years=[2005, 2025], start=2005.0, y=[0, 220], src="Eurostat gov_10dd_edpt1 · government debt and budget balance (% of GDP) · " + WB + " · GDP growth (annual %)", fmt="pct0", hl="GRC",
         narration="And Greece's comeback has quietly begun. {p} Since 2021, the Greek economy has grown faster than the EU average every single year. {p} Its government now runs a budget surplus: in 2025, about two percent of the economy. Poland ran a deficit of about seven percent, one of the largest in the EU. {pp} And Greek debt is falling: from more than two hundred percent of the economy in 2020, to about a hundred and forty-five percent in 2025. Still the highest in the EU, but down by more than sixty points in five years.",
         keys=[dict(at="more than two hundred percent", year=2020.0, dur=4.0), dict(at="a hundred and forty-five", year=2025.0, dur=5.0)],
         labels=[dict(at="more than two hundred percent", iso="GRC", year=2020), dict(at="a hundred and forty-five", iso="GRC", year=2025)],
         react=[dict(at="quietly begun", pose="pointUp"), dict(at="every single year", pose="cheer"), dict(at="budget surplus", pose="pointL"), dict(at="about seven percent", pose="shock"), dict(at="sixty points", pose="cheer")]),
    dict(act=4, type="host", bg="none",
         narration="So Greece isn't collapsing anymore. It's recovering. {p} The problem is that its neighbors are recovering faster. {pp} In 2025, Poland grew about three and a half percent. Greece, about two.",
         items=[dict(at="isn't collapsing", text="Greece: recovering", color="acc2"), dict(at="recovering faster", text="Neighbors: faster", color="acc"), dict(at="about three and a half", text="2025: Poland +3.6% · Greece +2.1%", serif=True, size=54)],
         react=[dict(at="isn't collapsing", pose="idle"), dict(at="recovering faster", pose="shrug"), dict(at="three and a half", pose="pointL")]),

    # ---------------- 5 · WHAT COMES NEXT ----------------
    dict(act=5, type="lines", set="ppp", series=["GRC", "ROU", "BGR"], years=[2000, 2025], start=2000.0, y=[0, 56000], src=PPP + " · " + PPS, fmt="usdk0", hl="BGR",
         narration="So who's next? {p} Adjusted for prices, Bulgaria is the only EU country still behind Greece. And by the World Bank's measure, it's now within about two percent. {p} In 2000, Greece produced almost three times as much per person as Bulgaria, at those prices. {pp} If Bulgaria keeps growing faster, Greece could soon be last in the European Union. Romania already passed it, back in 2019. {p} And Bulgaria just joined the euro, in January 2026: the same club Greece joined twenty-five years earlier.",
         keys=[dict(at="In 2000", year=2000.0, dur=3.0), dict(at="If Bulgaria keeps", year=2025.0, dur=6.0)],
         labels=[dict(at="within about two percent", iso="BGR", year=2025), dict(at="almost three times", iso="GRC", year=2000), dict(at="back in 2019", iso="ROU", year=2019)],
         react=[dict(at="who's next", pose="think"), dict(at="two percent", pose="shock"), dict(at="three times", pose="pointL"), dict(at="last in the European Union", pose="shock")]),
    dict(act=5, type="host", bg="none",
         narration="So is Poland really richer than Greece now? {p} In dollars, yes, since 2024. Adjusted for prices, yes, since 2015. {p} In how long people live, Greece is still clearly ahead. {p} But the bigger story isn't Greece falling. It's Eastern Europe rising. {p} Twenty years ago, these countries were the EU's poor relatives. Today, they're passing the old South, one by one. Portugal and Greece have already been passed. Others may be next. {pp} <soft>Which country do you think Poland passes next?</soft> Tell me in the comments.",
         items=[dict(at="In dollars, yes", text="Dollars: Poland ✓ (2024)", color="acc2"), dict(at="Adjusted for prices", text="Prices: Poland ✓ (2015)", color="acc2"), dict(at="Greece is still clearly ahead", text="Life expectancy: Greece ✓", color="acc"), dict(at="one by one", text="East passing South", serif=True, size=62)],
         react=[dict(at="really richer", pose="think"), dict(at="since 2024", pose="pointL"), dict(at="clearly ahead", pose="shrug"), dict(at="Eastern Europe rising", pose="cheer"), dict(at="passes next", pose="pointUp")]),
    dict(act=5, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="2025", color="acc", title="Poland passed Portugal too", sub="Again."),
         narration="Greece wasn't the only one. Poland passed Portugal too. To see how, watch this next. {p} I'm Chartbound. See you in the next one.",
         hold=14,
         react=[dict(at="Poland passed Portugal", pose="pointL"), dict(at="See you", pose="wave")]),
]

checks = [
    dict(say="GRC 2008 almost $32k", set="usd", iso="GRC", year=2008, min=31000, max=31999),
    dict(say="POL 2008 ≈ $14k", set="usd", iso="POL", year=2008, min=13500, max=14500),
    dict(say="Greece more than twice as rich (2008, US$)", rule="ratio", set="usd", a="GRC", b="POL", year=2008, min=2.0, max=2.4),
    dict(say="Poland passed Greece in 2024 — first time in the series", rule="first", set="usd", a="POL", b="GRC", year=2024),
    dict(say="Croatia passed Greece in 2025 (first time)", rule="first", set="usd", a="HRV", b="GRC", year=2025),
    dict(say="Croatia ahead by a hair (<1%)", rule="ratio", set="usd", a="HRV", b="GRC", year=2025, min=1.0, max=1.01),
    dict(say="POL 2025 ≈ $28.5k", set="usd", iso="POL", year=2025, min=28200, max=28700),
    dict(say="HRV 2025 ≈ $27.1k", set="usd", iso="HRV", year=2025, min=27050, max=27150),
    dict(say="GRC 2025 just under $27k", set="usd", iso="GRC", year=2025, min=26800, max=26999),
    dict(say="euro 2001, Olympics 2004", rule="expr", expr="[2001, 2004]", equal=[2001, 2004]),
    dict(say="13 EU countries below Greece in 2008 (PPS)", rule="rank", set="gdppps", iso="GRC", year=2008, among=EU27, equal=14),
    dict(say="Greece 26th of 27 in 2024 (PPS) — second-to-last", rule="rank", set="gdppps", iso="GRC", year=2024, among=EU27, equal=26),
    dict(say="Bulgaria still behind Greece (PPS 2024)", rule="gt", set="gdppps", a="GRC", b="BGR", year=2024),
] + [dict(say=f"{iso} ahead of Greece since {y} (PPS)", rule="since", set="gdppps", a=iso, b="GRC", year=y) for iso, y in
     [("CZE", 2010), ("MLT", 2010), ("PRT", 2011), ("SVK", 2011), ("SVN", 2011), ("EST", 2012), ("LTU", 2013), ("POL", 2015), ("HUN", 2015), ("LVA", 2020), ("ROU", 2019), ("HRV", 2019)]] + [
    dict(say="Poland in communism in the 1980s (1989 transition)", rule="expr", expr="1989 > 1980", equal=True),
    dict(say="deficit 2009 revised to more than double (Oct 2009: ~6% → 12.5%; later 15.4%)", rule="expr", expr="12.5 / 6.0 > 2", equal=True),
    dict(say="GRC real output per person 2013 down about a quarter vs 2008", set="rpcx08", iso="GRC", year=2013, min=-28, max=-23),
    dict(say="GRC 2025 about 8% below 2008", set="rpcx08", iso="GRC", year=2025, min=-9.5, max=-7),
    dict(say="POL +84% since 2008", set="rpcx08", iso="POL", year=2025, min=82, max=86),
    dict(say="Greece fell furthest (real output per person 2013 vs 2008) among GRC/IRL/PRT/ESP/CYP", rule="rank", set="rpcx08", iso="GRC", year=2013, among=["GRC", "IRL", "PRT", "ESP", "CYP"], equal=5),
    dict(say="Ireland 2010, Portugal 2011, Spain 2012, Cyprus 2013 programmes", rule="expr", expr="[2010, 2011, 2012, 2013]", equal=[2010, 2011, 2012, 2013]),
    dict(say="prices lower in Poland than Greece (US$/PPP 2025)", rule="expr", expr="28419.6 / 54262.4 < 26948.0 / 45263.6", equal=True),
    dict(say="GRC AIC 2024 ≈ 81 (PPS)", set="aic", iso="GRC", year=2024, min=80.5, max=81.4),
    dict(say="GRC GDP PPS 2024 = 70", set="gdppps", iso="GRC", year=2024, min=69.5, max=70.4),
    dict(say="Bulgaria euro 1 Jan 2026; Greece 2001 → 25 years", rule="expr", expr="2026 - 2001", equal=25),
    dict(say="GRC unemployment 2013 ≈ 28%", set="unemp", iso="GRC", year=2013, min=27.0, max=28.4),
    dict(say="GRC youth unemployment 2013 almost 60%", set="yunemp", iso="GRC", year=2013, min=55, max=59.99),
    dict(say="GRC shrank five years in a row 2009–2013", rule="countneg", set="gdpg", iso="GRC", a=2009, b=2013, equal=5),
    dict(say="GRC 2011 almost −10%", set="gdpg", iso="GRC", year=2011, min=-10.0, max=-9.0),
    dict(say="Poland the only EU economy that grew in 2009", rule="onlypos", set="g09", iso="POL"),
    dict(say="rescue ≈ €289 bn (ESM)", rule="expr", expr="round(141.8 + 61.9 + 52.9 + 32.1)", equal=289),
    dict(say="2015: banks closed 29 Jun–20 Jul (3 weeks), €60/day ATM limit (Bank of Greece / Greek government decree)", rule="expr", expr="[21, 60]", equal=[21, 60]),
    dict(say="GRC debt 2020 > 200%", set="debt", iso="GRC", year=2020, min=200),
    dict(say="GRC/POL/EU gfcf ≈ 23% in 2008", rule="expr", expr="all(22.5 <= v <= 23.5 for v in [23.3, 23.2, 23.0])", equal=True),
    dict(say="GRC gfcf 2016 ≈ 11%", set="gfcf", iso="GRC", year=2016, min=10.5, max=11.9),
    dict(say="GRC gfcf lowest in the EU (2016)", rule="rank", set="gfcf", iso="GRC", year=2016, among=EU27, equal=27),
    dict(say="HRV gfcf 2025 ≈ a quarter", set="gfcf", iso="HRV", year=2025, min=24, max=27),
    dict(say="ROU gfcf 2025 ≈ a quarter", set="gfcf", iso="ROU", year=2025, min=24, max=27),
    dict(say="GRC gfcf 2025 ≈ 17%", set="gfcf", iso="GRC", year=2025, min=16.5, max=17.4),
    dict(say="GRC mw 2008 ≈ €790", set="mw", iso="GRC", year=2008, min=780, max=800),
    dict(say="POL mw 2008 ≈ €340", set="mw", iso="POL", year=2008, min=330, max=350),
    dict(say="GRC mw cut more than a fifth (2011 €877 → 2012 €684)", set="mw", iso="GRC", year=2012, min=680, max=690),
    dict(say="cut = 22%", rule="expr", expr="round(1 - 684 / 877, 2)", equal=0.22),
    dict(say="POL mw 2025 ≈ €1,100", set="mw", iso="POL", year=2025, min=1090, max=1110),
    dict(say="GRC mw 2025 ≈ €1,030", set="mw", iso="GRC", year=2025, min=1020, max=1035),
    dict(say="HRV mw 2025 ≈ €970", set="mw", iso="HRV", year=2025, min=960, max=980),
    dict(say="GRC pop 2011 → 2025 almost −700k", rule="expr", expr="11104899 - 10413962", equal=690937),
    dict(say="≈ one in sixteen", rule="expr", expr="round(11104899 / 690937)", equal=16),
    dict(say="GRC life expectancy 2024 ≈ 82", set="le", iso="GRC", year=2024, min=81.5, max=82.4),
    dict(say="POL life expectancy 2024 ≈ 78", set="le", iso="POL", year=2024, min=78.0, max=78.6),
    dict(say="almost 3.5 years more", rule="expr", expr="round(81.8 - 78.4, 1)", equal=3.4),
] + [dict(say=f"GRC grew faster than the EU in {y}", rule="gt", set="gdpg", a="GRC", b="EUU", year=y) for y in range(2021, 2026)] + [
    dict(say="GRC surplus 2025 ≈ 2%", set="bal", iso="GRC", year=2025, min=1.6, max=2.4),
    dict(say="POL deficit 2025 ≈ 7%", set="bal", iso="POL", year=2025, min=-7.4, max=-6.6),
    dict(say="POL deficit one of the largest in the EU (2025)", rule="rank", set="balue", iso="POL", year=2025, among=EU27, min=25, max=27),
    dict(say="GRC debt 2025 ≈ 145%", set="debt", iso="GRC", year=2025, min=143, max=147),
    dict(say="GRC debt highest in the EU (2025)", rule="rank", set="debtue", iso="GRC", year=2025, among=EU27, equal=1),
    dict(say="down by more than 60 points 2020→2025", rule="expr", expr="209.4 - 145.4 > 60", equal=True),
    dict(say="POL growth 2025 ≈ 3.5%", set="gdpg", iso="POL", year=2025, min=3.3, max=3.8),
    dict(say="GRC growth 2025 ≈ 2%", set="gdpg", iso="GRC", year=2025, min=1.8, max=2.3),
    dict(say="BGR within about 2% of GRC (PPP 2025)", rule="ratio", set="ppp", a="BGR", b="GRC", year=2025, min=0.975, max=0.995),
    dict(say="GRC almost 3× BGR in 2000 (PPP)", rule="ratio", set="ppp", a="GRC", b="BGR", year=2000, min=2.8, max=2.99),
    dict(say="Poland ahead in dollars since 2024", rule="since", set="usd", a="POL", b="GRC", year=2024),
]

datasets = [
    dict(set="usd", wb="NY.GDP.PCAP.CD", isos=["GRC", "POL", "HRV", "ROU", "HUN", "BGR", "EUU"], **{"from": 1995, "to": 2025}),
    dict(set="ppp", wb="NY.GDP.PCAP.PP.CD", isos=["GRC", "POL", "HRV", "ROU", "BGR", "ESP", "EUU"], **{"from": 1995, "to": 2025}),
    dict(set="rpc", wb="NY.GDP.PCAP.PP.KD", isos=["GRC", "POL", "EUU", "IRL", "PRT", "ESP", "CYP"], **{"from": 2000, "to": 2025}),
    dict(set="rpcx08", derive="idx", src="rpc", isos=["GRC", "POL", "EUU", "IRL", "PRT", "ESP", "CYP"], base=2008, off=-100),
    dict(set="aic", eurostat="prc_ppp_ind", filters={"na_item": "VI_PPS_EU27_2020_HAB", "ppp_cat": "A01"}, isos=["GRC"], **{"from": 2008, "to": 2024}),
    dict(set="gdppps", eurostat="prc_ppp_ind", filters={"na_item": "VI_PPS_EU27_2020_HAB", "ppp_cat": "GDP"}, isos=EU27, **{"from": 2000, "to": 2024}),
    dict(set="unemp", wb="SL.UEM.TOTL.ZS", isos=["GRC", "POL"], **{"from": 2000, "to": 2025}),
    dict(set="yunemp", wb="SL.UEM.1524.ZS", isos=["GRC", "POL"], **{"from": 2000, "to": 2025}),
    dict(set="gdpg", wb="NY.GDP.MKTP.KD.ZG", isos=["GRC", "POL", "EUU"], **{"from": 2005, "to": 2025}),
    dict(set="g09", wb="NY.GDP.MKTP.KD.ZG", isos=EU27, year=2009, flat=True),
    dict(set="gfcf", wb="NE.GDI.FTOT.ZS", isos=sorted(set(EU27 + ["EUU"])), **{"from": 2000, "to": 2025}),
    dict(set="debt", eurostat="gov_10dd_edpt1", filters={"unit": "PC_GDP", "na_item": "GD", "sector": "S13"}, isos=["GRC", "POL"], **{"from": 2005, "to": 2025}),
    dict(set="debtue", eurostat="gov_10dd_edpt1", filters={"unit": "PC_GDP", "na_item": "GD", "sector": "S13"}, isos=EU27, **{"from": 2025, "to": 2025}),
    dict(set="bal", eurostat="gov_10dd_edpt1", filters={"unit": "PC_GDP", "na_item": "B9", "sector": "S13"}, isos=["GRC", "POL"], **{"from": 2015, "to": 2025}),
    dict(set="balue", eurostat="gov_10dd_edpt1", filters={"unit": "PC_GDP", "na_item": "B9", "sector": "S13"}, isos=EU27, **{"from": 2025, "to": 2025}),
    dict(set="mw", eurostat="earn_mw_cur", filters={"currency": "EUR"}, isos=["GRC", "POL", "HRV"], **{"from": 2008, "to": 2025}),
    dict(set="le", wb="SP.DYN.LE00.IN", isos=["GRC", "POL"], **{"from": 2000, "to": 2024}),
]
snapshot = []

clips = [
    dict(**{"from": "s00", "to": "s00"}, hook="Poland just passed *Greece*", title="Greece was twice as rich as Poland in 2008. Not anymore #Shorts", desc="2008: $31.7k vs $14.0k per person. 2024: Poland passed Greece. 2025: Croatia too (World Bank)."),
    dict(**{"from": "s01", "to": "s01"}, hook="12 countries *passed Greece*", title="12 EU countries passed Greece since 2008 #Shorts", desc="Adjusted for prices (Eurostat PPS), only Bulgaria is still behind Greece in the EU."),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="a-L14-greece", clips=clips, channel="chartbound", chapter0="The flip",
            thumb=dict(v="map", iso="POL", vs="GRC", lon=21, lat=46, scale=1500, cx=930, cy=330, top="POLAND", big="PASSED", line2="GREECE"),
            w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks, datasets=datasets, snapshot=snapshot,
            voice=dict(model="", name="Charon",
                       style=("You are the narrator of a popular data documentary on YouTube. Read the script below in a warm, curious voice "
                              "with a little dry humor, at a relaxed but engaged pace of about 145 words per minute, like a smart friend telling "
                              "you something surprising. Let the big numbers land with a tiny pause before them. Keep the energy steady from the "
                              "first sentence to the last. Never sound like an advertisement or an audiobook.")),
            music=[dict(act=0, track="Lightless Dawn", vol=0.24), dict(act=1, track="Investigations", vol=0.23), dict(act=2, track="Deliberate Thought", vol=0.22),
                   dict(act=3, track="Hidden Agenda", vol=0.23), dict(act=4, track="Inspired", vol=0.23), dict(act=5, track="Floating Cities", vol=0.24)],
            yt=dict(title="In 2008, Greece Was Twice as Rich as Poland. Now It's Behind.",
                    description=("In 2008 the average Greek produced more than twice as much as the average Pole, in dollars. In 2024 Poland passed Greece, and in 2025 Croatia did too. "
                                 "Adjusted for prices, 12 of the 13 EU countries that were poorer than Greece in 2008 have passed it; only Bulgaria is still behind. "
                                 "The crash, the €289 billion rescue, the paycheck, and the twist: Greeks still live longer, run a budget surplus and are growing again.\n\n"
                                 "Sources: World Bank WDI (NY.GDP.PCAP.CD, NY.GDP.PCAP.PP.CD, NY.GDP.PCAP.PP.KD, NY.GDP.MKTP.KD.ZG, NE.GDI.FTOT.ZS, SL.UEM.TOTL.ZS, SL.UEM.1524.ZS, SP.POP.TOTL, SP.DYN.LE00.IN); "
                                 "Eurostat (prc_ppp_ind, earn_mw_cur, gov_10dd_edpt1); European Stability Mechanism (Greek programmes 2010–2018).\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#poland #greece #croatia #economics #data"),
                    tags=["poland", "greece", "poland economy", "greece economy", "croatia", "eastern europe", "gdp per capita", "minimum wage", "economics", "data"], lang="en"))

json.dump(spec, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "a-L14.json"), "w"), ensure_ascii=False, indent=1)
clean = lambda t: t.replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()
words = sum(len(clean(s["narration"])) for s in shots)
acts = {}
for s in shots:
    acts[s["act"]] = acts.get(s["act"], 0) + len(clean(s["narration"]))
print("shots", len(shots), "palavras", words, f"~{words / 145:.1f} min a 145 wpm", "por ato", acts)

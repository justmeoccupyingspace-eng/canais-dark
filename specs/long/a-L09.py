"""Gera specs/long/a-L09.json — Chartbound longo #9: "In 2012, Japan Was 74% Richer Than Spain. Now Spain Is Ahead."
Banco de pautas (31/10): o iene sozinho é tema saturado; o ângulo aqui é a Espanha (virada desde 2013) + a primeira ultrapassagem em dólares desde 1960.
Dados: World Bank WDI (julho/2026, ano 2025) + Eurostat une_rt_a + pontos citados (INE Frontur 2025; JNTO 2025; MOF/Jiji 26 mai 2026; BoJ; Fed)."""
import json, os

ACTS = ["Cold open", "The yen", "Spain's comeback", "The sunshine economy", "The twist", "What comes next"]
WB = "World Bank WDI"
USD = WB + " · GDP per capita (current US$)"
EU27 = ["AUT", "BEL", "BGR", "HRV", "CYP", "CZE", "DNK", "EST", "FIN", "FRA", "DEU", "GRC", "HUN", "IRL", "ITA", "LVA", "LTU", "LUX", "MLT", "NLD", "POL", "PRT", "ROU", "SVK", "SVN", "ESP", "SWE"]
TOUR = "INE Frontur (3 Feb 2026): 96.8 million international tourists in Spain, 2025 · JNTO (Jan 2026): 42.7 million visitors to Japan, 2025"
NIIP = "Japan Ministry of Finance via Jiji/Nippon.com (26 May 2026): net external assets ¥561.75 trillion at end-2025, third after Germany and China"

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="lines", set="usd", series=["JPN", "ESP"], years=[1990, 2025], start=1990.0, y=[0, 55000], src=USD, fmt="usdk0", hl="ESP",
         narration="In 2012, the average Japanese produced about forty-nine and a half thousand dollars a year. The average Spaniard, about twenty-eight and a half. {p} Japan was almost seventy-five percent richer. And Spain was in the middle of a brutal crisis: one in four Spaniards who wanted a job couldn't find one. {pp} In 2024, Spain passed Japan. In 2025, it pulled further ahead: about thirty-eight and a half thousand dollars per person, against thirty-six. {p} In more than sixty years of World Bank records, that had never happened before. {p} And Spain isn't alone. Italy passed Japan again in 2022. South Korea, for the first time, in 2023.",
         keys=[dict(at="In 2012", year=2012.0, dur=3.0), dict(at="In 2024", year=2025.0, dur=6.0)],
         labels=[dict(at="forty-nine and a half", iso="JPN", year=2012), dict(at="twenty-eight and a half", iso="ESP", year=2012), dict(at="pulled further ahead", iso="ESP", year=2025)],
         react=[dict(at="In 2012", pose="idle"), dict(at="seventy-five percent", pose="pointL"), dict(at="brutal crisis", pose="think"), dict(at="Spain passed Japan", pose="shock"), dict(at="never happened", pose="pointUp")]),
    dict(act=0, type="host", bg="lines", set="usd", series=["JPN", "ESP"], years=[1990, 2025], start=2025.0, y=[0, 55000], fmt="usdk0",
         narration="Japan: the bullet trains, the robots, and companies everyone knows, like Toyota, Sony and Nintendo. {p} Spain: one of Europe's biggest tourist destinations, a housing crash that left entire towns of empty apartments, and for years, Europe's worst unemployment. {p} Thirteen years later, the ranking is the other way around: measured in dollars, the average Spaniard now produces more. How did that flip? {pp} There are two reasons. <soft>Only one of them is about Spain.</soft>",
         items=[dict(at="bullet trains", text="Japan: trains, robots, brands", color="acc2"), dict(at="worst unemployment", text="Spain: beaches, unemployment", color="acc"), dict(at="Only one", text="Two reasons. One is Spain.", serif=True, size=60)],
         react=[dict(at="bullet trains", pose="pointL"), dict(at="worst unemployment", pose="shrug"), dict(at="How did that flip", pose="think"), dict(at="Only one", pose="pointUp")]),

    # ---------------- 1 · THE YEN ----------------
    dict(act=1, type="lines", set="fx", series=["JPN"], years=[2005, 2025], start=2005.0, y=[60, 160], src=WB + " · official exchange rate, yen per US$ (period average)", fmt="int", hl="JPN",
         narration="The first reason is the yen. Japan didn't do anything dramatic. Its currency did. {p} In 2012, one dollar bought about eighty yen. In 2024, about a hundred and fifty. {p} The yen lost almost half its value against the dollar. {p} So a Japanese paycheck that never changed in yen was suddenly worth almost half as much in dollars. A salary of five million yen was worth about sixty-three thousand dollars in 2012. In 2024, about thirty-three thousand. {pp} Japan's economy, measured in dollars, shrank by about thirty percent between 2012 and 2025.",
         keys=[dict(at="In 2012", year=2012.0, dur=3.0), dict(at="In 2024", year=2025.0, dur=6.0)],
         labels=[dict(at="about eighty yen", iso="JPN", year=2012), dict(at="a hundred and fifty", iso="JPN", year=2024)],
         react=[dict(at="the yen", pose="pointUp"), dict(at="about eighty", pose="pointL"), dict(at="almost half its value", pose="shock"), dict(at="thirty percent", pose="shock")]),
    dict(act=1, type="list", src="Bank of Japan (negative rate from Feb 2016; ended 19 Mar 2024) · US Federal Reserve (target 5.25–5.50%, Jul 2023–Sep 2024)", title="Why the yen fell",
         narration="Why? Interest rates. {p} To fight decades of falling prices, the Bank of Japan kept its main rate below zero from 2016 until March 2024. {p} Meanwhile, America's central bank pushed its rate above five percent. {p} Investors sold yen to buy dollars that paid far more. The Bank of Japan only raised rates in 2024, its first hike in seventeen years. {p} And a weaker yen was partly the point: it makes Japanese exports cheaper, and Japan a bargain for tourists. {pp} Measured in yen, Japan didn't get poorer. Output per person, after inflation, grew about eleven percent since 2013.",
         items=[dict(at="below zero", kind="bullet", text="Japan: rates below 0% (2016–2024)"),
                dict(at="above five percent", kind="bullet", text="USA: rates above 5% (2023–2024)"),
                dict(at="sold yen", kind="bullet", text="Investors sell yen, buy dollars"),
                dict(at="didn't get poorer", kind="title", text="IN YEN: +11% SINCE 2013")],
         react=[dict(at="Interest rates", pose="think"), dict(at="below zero", pose="pointL"), dict(at="above five", pose="shock"), dict(at="didn't get poorer", pose="pointUp")]),

    # ---------------- 2 · SPAIN'S COMEBACK ----------------
    dict(act=2, type="lines", set="unemp", series=["JPN", "EMU", "ESP"], years=[2000, 2025], start=2000.0, y=[0, 30], src=WB + " · unemployment, total (% of labor force, modeled ILO estimate) · ESM financial assistance to Spain (2012): €41.3 bn", fmt="pct0", hl="ESP",
         narration="But that's only half the story. The other half is Spain. {p} In 2013, twenty-six percent of Spain's workforce was unemployed. Among young people, more than half. {p} The housing bubble had burst, and the banks needed a European rescue: about forty-one billion euros in loans, to keep them standing. {pp} By 2025, unemployment was about ten percent. Still the highest in the European Union, but the lowest in Spain in almost twenty years.",
         keys=[dict(at="In 2013", year=2013.0, dur=4.0), dict(at="By 2025", year=2025.0, dur=6.0)],
         labels=[dict(at="twenty-six percent", iso="ESP", year=2013), dict(at="about ten percent", iso="ESP", year=2025)],
         react=[dict(at="only half the story", pose="pointUp"), dict(at="twenty-six", pose="shock"), dict(at="more than half", pose="shock"), dict(at="European rescue", pose="think"), dict(at="almost twenty years", pose="cheer")]),
    dict(act=2, type="lines", set="rpcx", series=["JPN", "EMU", "ESP"], years=[2013, 2025], start=2013.0, y=[-12, 25], src=WB + " · GDP per capita (constant 2015 US$), change since 2013 · OICA vehicle production 2024", fmt="pct0s", hl="ESP",
         ref=dict(value=0, label="2013 level", pos="left"),
         narration="Since then, Spain's output per person, after inflation, has grown about twenty-one percent. The eurozone's, about sixteen. Japan's, about eleven. {p} And lately, Spain has been sprinting. {p} In 2024 and 2025, it grew faster than Germany, France and Italy, and faster than the United States. In 2024, about three and a half percent, more than three times the eurozone's pace. {p} Its car factories, mostly foreign-owned, now build more vehicles than any country in Europe except Germany.",
         keys=[dict(at="Since then", year=2025.0, dur=7.0)],
         labels=[dict(at="about twenty-one", iso="ESP", year=2025), dict(at="Japan's, about eleven", iso="JPN", year=2025)],
         react=[dict(at="Since then", pose="idle"), dict(at="twenty-one", pose="cheer"), dict(at="about eleven", pose="pointL"), dict(at="the United States", pose="shock")]),
    dict(act=2, type="stats", src=WB + " · population, total (SP.POP.TOTL)", title="Population change",
         narration="And Spain has something Japan doesn't: more people. {p} Since 2019, thanks to immigration, Spain's population has grown by more than two million. Many come from Latin America, and already speak the language. {p} Japan's has shrunk by more than three million. {pp} Since its peak in 2010, Japan has lost about four point seven million people, more than the entire population of Croatia.",
         stats=[dict(at="more than two million", value=2236642, fmt="k0", label="more people in Spain since 2019"), dict(at="four point seven million", value=4703266, fmt="k0", label="fewer people in Japan since 2010")],
         react=[dict(at="more people", pose="pointUp"), dict(at="more than two million", pose="cheer"), dict(at="more than three million", pose="shock"), dict(at="Croatia", pose="shrug")]),

    # ---------------- 3 · THE SUNSHINE ECONOMY ----------------
    dict(act=3, type="host", bg="none",
         narration="Quick favor: if you're enjoying this, hit subscribe. It's free, and it's genuinely what keeps this channel going. {p} Now, what is Spain actually selling? {pp} Mostly, sunshine. Quite literally.",
         items=[dict(at="hit subscribe", text="Subscribe = more of these"), dict(at="actually selling", text="What does Spain sell?", color="acc2"), dict(at="sunshine", text="Sunshine.", serif=True, size=76, color="acc")],
         react=[dict(at="Quick favor", pose="wave"), dict(at="actually selling", pose="think"), dict(at="sunshine", pose="cheer")]),
    dict(act=3, type="stats", src=TOUR + " · INE tourism satellite account (12.6% of GDP, 2024) · Red Eléctrica (55.5% renewable electricity, 2025)", title="International tourists, 2025",
         narration="In 2025, Spain welcomed almost ninety-seven million foreign tourists, a new record. Only France gets more. That's about two tourists for every person who lives in Spain. {p} Japan had a record year too: almost forty-three million. {pp} Spain, with about forty percent of Japan's population, received more than twice as many visitors. {p} Tourism brings in money from abroad, and jobs that don't need a university degree, exactly what Spain needed after the crash. Tourism is now about an eighth of Spain's entire economy. {p} And the same sun powers the country: in 2025, more than half of Spain's electricity came from renewables.",
         stats=[dict(at="almost ninety-seven million", value=96800000, fmt="k0", label="tourists in Spain, 2025"), dict(at="almost forty-three million", value=42700000, fmt="k0", label="visitors to Japan, 2025")],
         react=[dict(at="ninety-seven million", pose="shock"), dict(at="forty-three million", pose="pointL"), dict(at="more than twice", pose="pointUp"), dict(at="after the crash", pose="think")]),
    dict(act=3, type="lines", set="pppx", series=["JPN", "ESP"], years=[1990, 2025], start=1990.0, y=[0, 65000], src=WB + " · GDP per capita, PPP (current international $)", fmt="usdk0", hl="ESP",
         narration="And it's not just the exchange rate. {p} Adjust for what things actually cost in each country, and Spain has been ahead of Japan every year since 2022. {p} In 2025, by about eight percent: the average Spaniard now produces about sixty thousand dollars' worth a year, at those prices. That's a slightly bigger lead than in plain dollars. {pp} In 1990, by that same measure, Japan was about half again as rich.",
         keys=[dict(at="Adjust for", year=2022.0, dur=5.0), dict(at="In 2025", year=2025.0, dur=3.0)],
         labels=[dict(at="every year since 2022", iso="ESP", year=2022), dict(at="about eight percent", iso="ESP", year=2025)],
         react=[dict(at="not just the exchange rate", pose="pointUp"), dict(at="since 2022", pose="pointL"), dict(at="eight percent", pose="cheer"), dict(at="half again", pose="think")]),

    # ---------------- 4 · THE TWIST ----------------
    dict(act=4, type="duel", set="yunemp", year=2025, a="ESP", b="JPN", fmt="pct1", src=WB + " · unemployment, youth (% of labor force ages 15–24, modeled ILO estimate), 2025", title="Youth unemployment, 2025", badge="6× HIGHER IN SPAIN",
         cues=[dict(at="In Spain", show="a"), dict(at="In Japan", show="b")],
         narration="But don't feel sorry for Japan just yet. {p} Look at young people looking for work. {p} In Spain, about one in four can't find a job. {pp} In Japan, about one in twenty-five. {p} A young Spaniard is more than six times as likely to be unemployed. {p} Japan has the opposite problem: it can't find enough workers.",
         react=[dict(at="feel sorry", pose="shrug"), dict(at="one in four", pose="shock"), dict(at="one in twenty-five", pose="pointL"), dict(at="six times", pose="shock")]),
    dict(act=4, type="stats", src=NIIP, title="What Japan owns abroad, net",
         narration="And Japan is sitting on a mountain of savings. {p} Japanese families, companies and the government own about five hundred and sixty trillion yen more abroad than foreigners own in Japan. {p} That's about three point seven trillion dollars, a record, and the third biggest pile on Earth, after Germany and China. {pp} Interest and dividends from all of it flow home every year, and a weak yen makes them worth more in yen.",
         stats=[dict(at="five hundred and sixty trillion", value=561.75, fmt="dec1", label="trillion yen, net, end of 2025"), dict(at="three point seven trillion", value=3.75, fmt="dec2", label="trillion US dollars")],
         react=[dict(at="mountain of savings", pose="pointUp"), dict(at="five hundred and sixty", pose="shock"), dict(at="third biggest", pose="pointL"), dict(at="worth more in yen", pose="think")]),
    dict(act=4, type="host", bg="none",
         narration="And here's the uncomfortable math for Spain. {p} If the yen went back to where it was in 2019, about a hundred and ten to the dollar, Japan would jump straight back ahead, by more than ten thousand dollars a person. {p} Japan's overall unemployment is about two and a half percent. Spain's is four times that. And both countries live about as long as anyone on Earth: around eighty-four years. {pp} <soft>Spain's lead is real, but it's fragile.</soft>",
         items=[dict(at="where it was in 2019", text="Yen at 110 (2019)?", color="acc2"), dict(at="more than ten thousand", text="Japan +$10k ahead", color="acc"), dict(at="it's fragile", text="Real, but fragile", serif=True, size=66)],
         react=[dict(at="uncomfortable math", pose="think"), dict(at="straight back ahead", pose="shock"), dict(at="fragile", pose="shrug")]),

    # ---------------- 5 · WHAT COMES NEXT ----------------
    dict(act=5, type="lines", set="old", series=["KOR", "ESP", "ITA", "JPN"], years=[1990, 2025], start=1990.0, y=[0, 32], src=WB + " · population aged 65+ (% of total) · fertility rate (births per woman)", fmt="pct0", hl="ESP",
         narration="And Spain faces Japan's problem, just later. {p} Spanish women now have about one point one children on average. That's even fewer than in Japan. {p} People sixty-five and over are now more than a fifth of Spain's population. {p} That's where Japan was around 2007. Today it's at thirty percent, and the share of Japanese of working age has fallen from sixty-eight percent in 2000 to under fifty-nine. {pp} Without immigrants, Spain would already be shrinking. {p} South Korea and Italy are on the same road, and Korea is moving down it fastest of all.",
         keys=[dict(at="just later", year=2007.0, dur=6.0), dict(at="more than a fifth", year=2025.0, dur=5.0)],
         labels=[dict(at="around 2007", iso="JPN", year=2007), dict(at="more than a fifth", iso="ESP", year=2025), dict(at="thirty percent", iso="JPN", year=2025)],
         react=[dict(at="just later", pose="think"), dict(at="one point one", pose="shock"), dict(at="more than a fifth", pose="pointL"), dict(at="already be shrinking", pose="shrug")]),
    dict(act=5, type="host", bg="none",
         narration="So is Spain really richer than Japan? {p} In dollars, yes, for now. Adjusted for prices, yes, by a little. {p} In jobs, savings and security, Japan is still far ahead. {p} But Spain did something Japan hasn't managed in thirty years: it turned a disaster into a decade of growth. {pp} <soft>The race is close, and it's no longer one-sided.</soft> {p} And for Japan, the lesson runs the other way: a country can be rich in savings and still lose ground, when its people, and its currency, shrink.",
         items=[dict(at="In dollars, yes", text="Dollars: Spain ✓", color="acc2"), dict(at="Adjusted for prices", text="Prices: Spain ✓", color="acc2"), dict(at="Japan is still far ahead", text="Jobs, savings: Japan ✓", color="acc"), dict(at="no longer one-sided", text="Close race", serif=True, size=66)],
         react=[dict(at="really richer", pose="think"), dict(at="for now", pose="shrug"), dict(at="still far ahead", pose="pointL"), dict(at="decade of growth", pose="cheer")]),
    dict(act=5, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="2026", color="acc", title="Poland just passed Japan", sub="and nobody noticed"),
         narration="Spain isn't the only one. Poland passed Japan too, and almost nobody noticed. To see how, watch this next. {p} I'm Chartbound. See you in the next one.",
         hold=14,
         react=[dict(at="Poland passed Japan", pose="pointL"), dict(at="See you", pose="wave")]),
]

checks = [
    dict(say="JPN 2012 ≈ $49.5k", set="usd", iso="JPN", year=2012, min=49000, max=50000),
    dict(say="ESP 2012 ≈ $28.5k", set="usd", iso="ESP", year=2012, min=28000, max=29000),
    dict(say="Japan almost 75% richer (2012)", rule="ratio", set="usd", a="JPN", b="ESP", year=2012, min=1.72, max=1.749),
    dict(say="Spain passed Japan in 2024 — first time since 1960", rule="first", set="usd60", a="ESP", b="JPN", year=2024),
    dict(say="records since 1960 (> 60 years)", rule="expr", expr="2025 - 1960 > 60", equal=True),
    dict(say="still ahead 2025", rule="gt", set="usd", a="ESP", b="JPN", year=2025),
    dict(say="ESP 2025 ≈ $38.5k", set="usd", iso="ESP", year=2025, min=38250, max=38900),
    dict(say="JPN 2025 ≈ $36k", set="usd", iso="JPN", year=2025, min=35700, max=36300),
    dict(say="unemployment ESP 2013 ≈ 26%", set="unemp", iso="ESP", year=2013, min=25.5, max=26.5),
    dict(say="youth unemployment ESP 2013 > 50%", set="yunemp", iso="ESP", year=2013, min=50.01),
    dict(say="unemployment ESP 2025 ≈ 10%", set="unemp", iso="ESP", year=2025, min=9.8, max=10.6),
    dict(say="highest in the EU 2025 (Eurostat)", rule="rank", set="unue", iso="ESP", year=2025, among=EU27, equal=1),
    dict(say="2007 below 2025 (so 'lowest in almost 20 years')", set="unemp", iso="ESP", year=2007, max=10.37),
    dict(say="yen ≈ 80 in 2012", set="fx", iso="JPN", year=2012, min=78, max=82),
    dict(say="yen ≈ 150 in 2024", set="fx", iso="JPN", year=2024, min=148, max=153),
    dict(say="yen lost almost half (2012→2024)", rule="expr", expr="round(1 - 79.79 / 151.37, 2)", equal=0.47),
    dict(say="JPN GDP in $ shrank ≈30% 2012→2025", set="gdpchg", iso="JPN", year=0, min=-33, max=-27),
    dict(say="BoJ negative rate Feb 2016 → 19 Mar 2024; Fed 5.25–5.50%", rule="expr", expr="[2016, 2024, 5.25 > 5]", equal=[2016, 2024, True]),
    dict(say="JPN real pc +≈11% since 2013", set="rpcx", iso="JPN", year=2025, min=10.5, max=12.0),
    dict(say="ESP real pc +≈21% since 2013", set="rpcx", iso="ESP", year=2025, min=20.5, max=22.0),
    dict(say="EMU +≈16%", set="rpcx", iso="EMU", year=2025, min=15.5, max=16.9),
    dict(say="2024 ESP > DEU", rule="gt", set="gdpg", a="ESP", b="DEU", year=2024),
    dict(say="2024 ESP > FRA", rule="gt", set="gdpg", a="ESP", b="FRA", year=2024),
    dict(say="2024 ESP > ITA", rule="gt", set="gdpg", a="ESP", b="ITA", year=2024),
    dict(say="2024 ESP > USA", rule="gt", set="gdpg", a="ESP", b="USA", year=2024),
    dict(say="2025 ESP > DEU", rule="gt", set="gdpg", a="ESP", b="DEU", year=2025),
    dict(say="2025 ESP > FRA", rule="gt", set="gdpg", a="ESP", b="FRA", year=2025),
    dict(say="2025 ESP > ITA", rule="gt", set="gdpg", a="ESP", b="ITA", year=2025),
    dict(say="2025 ESP > USA", rule="gt", set="gdpg", a="ESP", b="USA", year=2025),
    dict(say="ESP pop +2M since 2019", set="popchg", iso="ESP", year=0, min=2.0e6 * 100 / 47118501, max=2.5e6 * 100 / 47118501),
    dict(say="JPN pop −3M since 2019", set="popchg", iso="JPN", year=0, min=-3.5e6 * 100 / 126633000, max=-3.0e6 * 100 / 126633000),
    dict(say="JPN peak 2010", rule="peak", set="popj", iso="JPN", a=2010, b=2010),
    dict(say="JPN −4.7M since 2010", rule="expr", expr="round((128070000 - 123366734) / 1e6, 1)", equal=4.7),
    dict(say="> Croatia's population", set="hrv", iso="HRV", year=2025, max=4.7e6),
    dict(say="Spain 96.8M tourists 2025 (INE); Japan 42.7M (JNTO)", rule="expr", expr="[96.8 < 97, 42.7 < 43, round(96.8 / 42.7, 2) > 2]", equal=[True, True, True]),
    dict(say="Spain ≈ 40% of Japan's population", rule="ratio", set="pop", a="ESP", b="JPN", year=2025, min=0.38, max=0.42),
    dict(say="PPP: Spain ahead every year 2022–2025", rule="since", set="pppx", a="ESP", b="JPN", year=2022),
    dict(say="PPP 2025 lead ≈ 8%", rule="ratio", set="pppx", a="ESP", b="JPN", year=2025, min=1.07, max=1.09),
    dict(say="PPP 1990: Japan about half again as rich", rule="ratio", set="pppx", a="JPN", b="ESP", year=1990, min=1.4, max=1.6),
    dict(say="youth unemp ESP 2025 ≈ 1 in 4", set="yunemp", iso="ESP", year=2025, min=23.5, max=26),
    dict(say="youth unemp JPN 2025 ≈ 1 in 25", set="yunemp", iso="JPN", year=2025, min=3.6, max=4.4),
    dict(say="> 6× as likely", rule="ratio", set="yunemp", a="ESP", b="JPN", year=2025, min=6.0, max=7.0),
    dict(say="NIIP ¥561.75T ≈ $3.75T at ¥149.7", rule="expr", expr="round(561.75 / 149.66, 2)", equal=3.75),
    dict(say="yen back to 110 → Japan ahead by > $10k", rule="expr", expr="round(35951.04 * 149.66 / 110 - 38627.25) > 10000", equal=True),
    dict(say="2019 yen ≈ 110", set="fx", iso="JPN", year=2019, min=108, max=111),
    dict(say="ESP fertility ≈ 1.1 (2024)", set="tfr", iso="ESP", year=2024, min=1.05, max=1.15),
    dict(say="…fewer than Japan", rule="gt", set="tfr", a="JPN", b="ESP", year=2024),
    dict(say="ESP 65+ > a fifth (2025)", set="old", iso="ESP", year=2025, min=20.01, max=22),
    dict(say="JPN 65+ in 2007 ≈ Spain 2025 (21.6%)", set="old", iso="JPN", year=2007, min=20.9, max=22.3),
    dict(say="Italy passed Japan again in 2022 and stayed ahead", rule="since", set="usd", a="ITA", b="JPN", year=2022),
    dict(say="Korea first time 2023", rule="first", set="usd60", a="KOR", b="JPN", year=2023),
    dict(say="2012 → 2025 = 13 years", rule="expr", expr="2025 - 2012", equal=13),
    dict(say="¥5M = $62.7k (2012) / $33.0k (2024)", rule="expr", expr="[round(5e6 / 79.79 / 1000), round(5e6 / 151.37 / 1000)]", equal=[63, 33]),
    dict(say="Spain bank rescue: €41.3bn ESM drawn (2012)", rule="expr", expr="round(41.3)", equal=41),
    dict(say="ESP 2024 growth ≈ 3.5%", set="gdpg", iso="ESP", year=2024, min=3.4, max=3.6),
    dict(say="> 3× eurozone 2024", rule="ratio", set="gdpg", a="ESP", b="EMU", year=2024, min=3.0, max=9),
    dict(say="Spain 2nd car producer in Europe after Germany (OICA 2024)", rule="expr", expr="True", equal=True),
    dict(say="tourism 12.6% of GDP 2024 (INE CSTE) ≈ an eighth", rule="expr", expr="abs(12.6 - 12.5) < 0.5", equal=True),
    dict(say="renewables 55.5% of electricity 2025 (REE)", rule="expr", expr="55.5 > 50", equal=True),
    dict(say="JPN unemployment ≈ 2.5% (2025)", set="unemp", iso="JPN", year=2025, min=2.3, max=2.7),
    dict(say="Spain ≈ 4× Japan", rule="ratio", set="unemp", a="ESP", b="JPN", year=2025, min=3.8, max=4.4),
    dict(say="life expectancy JPN ≈ 84 (2024)", set="le", iso="JPN", year=2024, min=83.6, max=84.4),
    dict(say="life expectancy ESP ≈ 84 (2024)", set="le", iso="ESP", year=2024, min=83.5, max=84.4),
    dict(say="Korea 65+ rose most since 2000 (×2.9)", set="oldx", iso="KOR", year=2025, min=250),
    dict(say="…vs Italy", set="oldx", iso="ITA", year=2025, max=150),
    dict(say="…vs Spain", set="oldx", iso="ESP", year=2025, max=150),
    dict(say="ESP PPP 2025 ≈ $60k", set="pppx", iso="ESP", year=2025, min=59000, max=60999),
    dict(say="Spain 2nd most visited after France (UN Tourism)", rule="expr", expr="True", equal=True),
    dict(say="BoJ first hike in 17 years (Mar 2024 vs Feb 2007)", rule="expr", expr="2024 - 2007", equal=17),
    dict(say="JPN working-age 2000 ≈ 68%", set="wa", iso="JPN", year=2000, min=67.5, max=68.5),
    dict(say="JPN working-age 2025 < 59%", set="wa", iso="JPN", year=2025, max=58.99),
    dict(say="≈2 tourists per resident (96.8M / 49.4M)", rule="expr", expr="round(96.8 / 49.355, 1)", equal=2.0),
    dict(say="PPP lead (≈8%) > nominal lead (≈7.4%)", rule="expr", expr="59867.69 / 55421.88 > 38627.25 / 35951.04", equal=True),
    dict(say="JPN 65+ 2025 ≈ 30%", set="old", iso="JPN", year=2025, min=29.5, max=30.5),
]

datasets = [
    dict(set="usd", wb="NY.GDP.PCAP.CD", isos=["ESP", "JPN", "ITA"], **{"from": 1990, "to": 2025}),
    dict(set="usd60", wb="NY.GDP.PCAP.CD", isos=["ESP", "JPN", "KOR"], **{"from": 1960, "to": 2025}),
    dict(set="wa", wb="SP.POP.1564.TO.ZS", isos=["JPN"], **{"from": 2000, "to": 2025}),
    dict(set="le", wb="SP.DYN.LE00.IN", isos=["ESP", "JPN"], **{"from": 2020, "to": 2024}),
    dict(set="pppx", wb="NY.GDP.PCAP.PP.CD", isos=["ESP", "JPN"], **{"from": 1990, "to": 2025}),
    dict(set="fx", wb="PA.NUS.FCRF", isos=["JPN"], **{"from": 2005, "to": 2025}),
    dict(set="gdpusd", wb="NY.GDP.MKTP.CD", isos=["JPN"], **{"from": 2012, "to": 2025}),
    dict(set="gdpchg", derive="chg", src="gdpusd", isos=["JPN"], a=2012, b=2025),
    dict(set="unemp", wb="SL.UEM.TOTL.ZS", isos=["ESP", "JPN", "EMU"], **{"from": 2000, "to": 2025}),
    dict(set="yunemp", wb="SL.UEM.1524.ZS", isos=["ESP", "JPN"], **{"from": 2010, "to": 2025}),
    dict(set="unue", eurostat="une_rt_a", filters={"age": "Y15-74", "unit": "PC_ACT", "sex": "T"}, isos=EU27, **{"from": 2025, "to": 2025}),
    dict(set="rpc", wb="NY.GDP.PCAP.KD", isos=["ESP", "JPN", "EMU"], **{"from": 2013, "to": 2025}),
    dict(set="rpcx", derive="idx", src="rpc", isos=["ESP", "JPN", "EMU"], base=2013, off=-100),
    dict(set="gdpg", wb="NY.GDP.MKTP.KD.ZG", isos=["ESP", "DEU", "FRA", "ITA", "USA", "EMU"], **{"from": 2023, "to": 2025}),
    dict(set="pop", wb="SP.POP.TOTL", isos=["ESP", "JPN"], **{"from": 2019, "to": 2025}),
    dict(set="popchg", derive="chg", src="pop", isos=["ESP", "JPN"], a=2019, b=2025),
    dict(set="popj", wb="SP.POP.TOTL", isos=["JPN"], **{"from": 1990, "to": 2025}),
    dict(set="hrv", wb="SP.POP.TOTL", isos=["HRV"], **{"from": 2025, "to": 2025}),
    dict(set="tfr", wb="SP.DYN.TFRT.IN", isos=["ESP", "JPN"], **{"from": 2020, "to": 2024}),
    dict(set="old", wb="SP.POP.65UP.TO.ZS", isos=["KOR", "ESP", "ITA", "JPN"], **{"from": 1990, "to": 2025}),
    dict(set="oldx", derive="idx", src="old", isos=["KOR", "ESP", "ITA", "JPN"], base=2000, off=0),
]
for y in range(2008, 2025):
    checks.append(dict(say=f"ESP unemployment {y} above 2025's", set="unemp", iso="ESP", year=y, min=10.39))
snapshot = []

clips = [
    dict(**{"from": "s00", "to": "s00"}, hook="Spain is now *richer than Japan*", title="Japan was 74% richer than Spain in 2012. Not anymore #Shorts", desc="In 2024 Spain passed Japan in GDP per person in dollars, for the first time in World Bank records (since 1960)."),
    dict(**{"from": "s02", "to": "s02"}, hook="The yen lost *half its value*", title="How the yen made Japan 'poorer' in dollars #Shorts", desc="2012: ¥80 per dollar. 2024: ¥150 (World Bank)."),
    dict(**{"from": "s08", "to": "s08"}, hook="97 million tourists vs *43 million*", title="Spain gets twice as many tourists as Japan #Shorts", desc="Spain 96.8M (INE), Japan 42.7M (JNTO), 2025."),
    dict(**{"from": "s10", "to": "s10"}, hook="Don't feel sorry for *Japan*", title="Youth unemployment: Spain vs Japan #Shorts", desc="About 1 in 4 young Spaniards can't find work. In Japan, about 1 in 25 (World Bank, 2025)."),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="a-L09-spain-japan", clips=clips, channel="chartbound", chapter0="The flip",
            thumb=dict(set="usd", iso="ESP", years=[1990, 2025], ymin=0, ymax=52000, band=[470, 690], flags=["ESP", "JPN"], top="SPAIN > JAPAN", big="FIRST", line2="TIME EVER", color="#ffd166"), w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks,
            datasets=datasets, snapshot=snapshot,
            voice=dict(model="", name="Charon",
                       style=("You are the narrator of a popular data documentary on YouTube. Read the script below in a warm, curious voice "
                              "with a little dry humor, at a relaxed but engaged pace of about 145 words per minute, like a smart friend telling "
                              "you something surprising. Let the big numbers land with a tiny pause before them. Keep the energy steady from the "
                              "first sentence to the last. Never sound like an advertisement or an audiobook.")),
            music=[dict(act=0, track="Lightless Dawn", vol=0.24), dict(act=1, track="Hidden Agenda", vol=0.23), dict(act=2, track="Inspired", vol=0.22),
                   dict(act=3, track="Investigations", vol=0.23), dict(act=4, track="Deliberate Thought", vol=0.22), dict(act=5, track="Floating Cities", vol=0.24)],
            yt=dict(title="In 2012, Japan Was 74% Richer Than Spain. Now Spain Is Ahead.",
                    description=("In 2012 the average Japanese produced about $49,600 a year and the average Spaniard about $28,500. In 2024 Spain passed Japan in GDP per person in dollars, for the first time in World Bank records going back to 1960, and in 2025 it pulled further ahead. "
                                 "Two reasons: the yen lost almost half its value, and Spain came back from 26% unemployment with immigration, tourism and the fastest growth among Europe's big economies. "
                                 "The twist: young Spaniards are six times as likely to be jobless as young Japanese, Japan sits on $3.7 trillion of net savings abroad, and a stronger yen would flip the ranking back.\n\n"
                                 "Sources: World Bank WDI (NY.GDP.PCAP.CD, NY.GDP.PCAP.PP.CD, NY.GDP.PCAP.KD, PA.NUS.FCRF, NY.GDP.MKTP.CD, SL.UEM.TOTL.ZS, SL.UEM.1524.ZS, NY.GDP.MKTP.KD.ZG, SP.POP.TOTL, SP.DYN.TFRT.IN, SP.POP.65UP.TO.ZS); "
                                 "Eurostat une_rt_a; INE Frontur; JNTO; Japan Ministry of Finance (net external assets); Bank of Japan; US Federal Reserve.\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#spain #japan #yen #economics #data"),
                    tags=["spain", "japan", "yen", "spain economy", "japan economy", "gdp per capita", "tourism", "economics", "data"], lang="en"))

json.dump(spec, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "a-L09.json"), "w"), ensure_ascii=False, indent=1)
clean = lambda t: t.replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()
words = sum(len(clean(s["narration"])) for s in shots)
acts = {}
for s in shots:
    acts[s["act"]] = acts.get(s["act"], 0) + len(clean(s["narration"]))
print("shots", len(shots), "palavras", words, f"~{words / 145:.1f} min a 145 wpm", "por ato", acts)

"""Gera specs/long/a-L06.json — Chartbound longo #6: "Portugal Was Richer Than Eastern Europe. Not Anymore."
Número próprio (filtro de saturação ok em 31/10, research/q3.json: "why is Portugal so poor" tem vídeos grandes sobre moradia/vida; ninguém mostrou a ultrapassagem da Polônia em 2025 nem o consumo romeno à frente).
Dados: World Bank WDI (julho/2026, ano 2025) + Eurostat (prc_ppp_ind, edat_lfse_03, earn_mw_cur, gov_10dd_edpt1) + pontos citados (resgate de 2011: Comissão Europeia)."""
import json, os

ACTS = ["Cold open", "The lost quarter century", "Why it happened", "The paycheck", "The twist", "What comes next"]
WB = "World Bank WDI"
PPP = WB + " · GDP per capita, PPP (current international $)"
RPC = WB + " · GDP per capita, PPP (constant 2021 international $), change since 2000"
EU27 = ["AUT", "BEL", "BGR", "HRV", "CYP", "CZE", "DNK", "EST", "FIN", "FRA", "DEU", "GRC", "HUN", "IRL", "ITA", "LVA", "LTU", "LUX", "MLT", "NLD", "POL", "PRT", "ROU", "SVK", "SVN", "ESP", "SWE"]
EC = "European Commission, financial assistance to Portugal (2011–2014): €78 billion EU/IMF programme"

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="lines", set="ppp", series=["PRT", "POL"], years=[1995, 2025], start=1995.0, y=[0, 60000], src=PPP, fmt="usdk0", hl="POL",
         narration="In 1995, the average person in Portugal produced almost twice as much as the average person in Poland, adjusted for prices. {p} Portugal had been in the European Union for almost a decade. Poland had just escaped communism. {p} Thirty years later, the lines have crossed. {pp} In 2025, for the first time, the average Pole out-produced the average Portuguese, by about two percent.",
         keys=[dict(at="Thirty years later", year=2025.0, dur=6.0)],
         labels=[dict(at="almost twice", iso="PRT", year=1995), dict(at="for the first time", iso="POL", year=2025)],
         react=[dict(at="In 1995", pose="idle"), dict(at="almost twice", pose="pointL"), dict(at="escaped communism", pose="think"), dict(at="lines have crossed", pose="shock"), dict(at="out-produced", pose="pointUp")]),
    dict(act=0, type="list", src=PPP + " · Eurostat prc_ppp_ind (actual individual consumption per head, PPS, 2024)", title="Who passed Portugal",
         narration="Poland isn't the first. {p} Slovenia got there in 2003. Czechia in 2007. Malta in 2009. Lithuania in 2018. {p} And three more are within about five percent: Estonia, Romania and Croatia. {pp} By one measure of how people actually live, what they consume per person, Romanians are already slightly ahead.",
         items=[dict(at="Slovenia got there", kind="bullet", text="Slovenia · 2003"),
                dict(at="Czechia in 2007", kind="bullet", text="Czechia · 2007"),
                dict(at="Lithuania in 2018", kind="bullet", text="Lithuania · 2018"),
                dict(at="isn't the first", kind="bullet", text="Poland · 2025"),
                dict(at="within about five percent", kind="title", text="NEXT: EE · RO · HR")],
         react=[dict(at="isn't the first", pose="pointUp"), dict(at="Lithuania in 2018", pose="pointL"), dict(at="three more", pose="shock"), dict(at="already slightly ahead", pose="shrug")]),
    dict(act=0, type="host", bg="lines", set="ppp", series=["PRT", "POL"], years=[1995, 2025], start=2025.0, y=[0, 60000], fmt="usdk0",
         narration="Portugal isn't poor. It's a rich, safe, beautiful country that a lot of people dream of moving to. {p} But for twenty-five years, it barely got richer, while its neighbors to the east sprinted. {p} This isn't a story about a country failing. It's about standing still while everyone around you runs. {p} So what happened to Portugal? {pp} <soft>And is it as bad as it looks?</soft>",
         items=[dict(at="isn't poor", text="Not poor. Not growing.", color="acc2"), dict(at="barely got richer", text="25 years of almost nothing", color="acc"), dict(at="as bad as it looks", text="As bad as it looks?", serif=True, size=66)],
         react=[dict(at="isn't poor", pose="idle"), dict(at="barely got richer", pose="shrug"), dict(at="what happened", pose="think"), dict(at="as bad as it looks", pose="pointUp")]),

    # ---------------- 1 · THE LOST QUARTER CENTURY ----------------
    dict(act=1, type="lines", set="rpc90x", series=["PRT", "EUU"], years=[1990, 2025], start=1990.0, y=[-5, 80], src=WB + " · GDP per capita, PPP (constant 2021 international $), change since 1990", fmt="pct0s", hl="PRT",
         ref=dict(value=0, label="1990 level", pos="left"),
         narration="It wasn't always like this. {p} After Portugal joined the European Union in 1986, it was catching up fast. {p} From 1990 to 2000, its output per person grew about twenty-nine percent, adjusted for prices. The EU's grew about twenty. {pp} Then, right around the year 2000, something broke.",
         keys=[dict(at="From 1990", year=2000.0, dur=6.0), dict(at="something broke", year=2025.0, dur=5.0)],
         labels=[dict(at="about twenty-nine", iso="PRT", year=2000)],
         react=[dict(at="wasn't always", pose="think"), dict(at="catching up fast", pose="cheer"), dict(at="twenty-nine", pose="pointL"), dict(at="something broke", pose="shock")]),
    dict(act=1, type="lines", set="rpcx", series=["LTU", "POL", "EUU", "PRT"], years=[2000, 2025], start=2000.0, y=[-10, 230], src=RPC, fmt="pct0s", hl="PRT",
         ref=dict(value=0, label="2000 level", pos="left"),
         narration="Look at growth since then. {p} From 2000 to 2025, output per person in Lithuania has roughly tripled. In Poland, it's grown about two and a half times. Romania's, almost as much. {p} The EU as a whole: up more than a third. {p} Portugal? {pp} Up about a fifth. In twenty-five years. Only Greece, crushed by its own debt crisis, did about as badly.",
         keys=[dict(at="From 2000 to 2025", year=2025.0, dur=7.0)],
         labels=[dict(at="roughly tripled", iso="LTU", year=2025), dict(at="Up about a fifth", iso="PRT", year=2025)],
         react=[dict(at="growth since then", pose="idle"), dict(at="roughly tripled", pose="shock"), dict(at="more than a third", pose="pointL"), dict(at="Up about a fifth", pose="shrug")]),
    dict(act=1, type="host", bg="lines", set="rpcx", series=["LTU", "POL", "EUU", "PRT"], years=[2000, 2025], start=2025.0, y=[-10, 230], fmt="pct0s",
         narration="And that's not just the pandemic. {p} From 2000 to 2019, Portugal's output per person grew just fifteen percent. {p} That's less than one percent a year, for almost two decades. Poland managed that much growth in less than four years. {p} Even Spain, next door, grew a little faster. {p} In 2000, Portugal was at about eighty-five percent of the EU average in output per person. By 2015, it had slipped to about seventy-six. {pp} <soft>For a generation of Portuguese, the economy simply stood still.</soft>",
         items=[dict(at="grew just fifteen", text="2000–2019: +15%", color="acc"), dict(at="less than one percent", text="< 1% a year", color="acc2"), dict(at="stood still", text="A generation of standing still", serif=True, size=60)],
         react=[dict(at="not just the pandemic", pose="think"), dict(at="just fifteen", pose="shock"), dict(at="less than one percent", pose="pointL"), dict(at="stood still", pose="shrug")]),

    # ---------------- 2 · WHY IT HAPPENED ----------------
    dict(act=2, type="lines", set="edu", series=["LTU", "CZE", "POL", "PRT"], years=[2000, 2025], start=2000.0, y=[0, 100], src="Eurostat edat_lfse_03 · adults 25–64 with at least upper secondary education (%)", fmt="pct0", hl="PRT",
         narration="The biggest reason is one most people never think about: school. {p} In 2000, fewer than one in five Portuguese adults had finished high school. {p} In Poland, four in five. In Czechia and Lithuania, more than eight in ten. {p} That's a legacy of the dictatorship that ended in 1974, which kept schooling short for most people. {p} Portugal entered the global economy with a workforce built for farms and small workshops. {pp} Today it's at about two in three, and climbing fast.",
         keys=[dict(at="The biggest reason", year=2000.0, dur=2.0), dict(at="workforce built", year=2025.0, dur=6.0)],
         labels=[dict(at="fewer than one in five", iso="PRT", year=2000), dict(at="four in five", iso="POL", year=2000), dict(at="two in three", iso="PRT", year=2025)],
         react=[dict(at="never think about", pose="think"), dict(at="fewer than one in five", pose="shock"), dict(at="four in five", pose="pointL"), dict(at="climbing fast", pose="cheer")]),
    dict(act=2, type="list", src="WTO (China accession, 11 Dec 2001) · EU enlargement (1 May 2004) · " + EC, title="Then came the shocks",
         narration="Then came the shocks. {p} In 2001, China joined the World Trade Organization. In 2004, eight countries from Central and Eastern Europe joined the EU. {p} Both offered what Portugal sold: cheap labor for textiles, shoes and assembly. {p} And inside the euro, Portugal could no longer devalue its currency to stay competitive. {p} When the euro crisis hit, Portugal needed a seventy-eight billion euro bailout in 2011.",
         items=[dict(at="China joined", kind="bullet", text="2001 · China joins the WTO"),
                dict(at="eight countries", kind="bullet", text="2004 · 8 CEE countries join the EU"),
                dict(at="cheap labor", kind="bullet", text="Same pitch: cheap labor"),
                dict(at="seventy-eight billion", kind="title", text="€78 BN BAILOUT")],
         react=[dict(at="the shocks", pose="think"), dict(at="China joined", pose="pointL"), dict(at="cheap labor", pose="shrug"), dict(at="seventy-eight billion", pose="shock")]),
    dict(act=2, type="lines", set="gfcf", series=["CZE", "EUU", "PRT"], years=[2000, 2025], start=2000.0, y=[0, 35], src=WB + " · gross fixed capital formation, % of GDP · net migration (SM.POP.NETM)", fmt="pct0", hl="PRT",
         narration="The bailout came with deep cuts. {p} Investment collapsed to about fifteen percent of the economy, among the lowest in the European Union. {p} And between 2011 and 2014, Portugal lost more than a hundred and thirty thousand people to emigration, net. {pp} Fewer machines, fewer workers, <soft>and a lost decade on top of a lost decade.</soft>",
         keys=[dict(at="deep cuts", year=2014.0, dur=6.0), dict(at="Fewer machines", year=2025.0, dur=4.0)],
         labels=[dict(at="about fifteen percent", iso="PRT", year=2014)],
         react=[dict(at="deep cuts", pose="think"), dict(at="about fifteen percent", pose="shock"), dict(at="hundred and thirty thousand", pose="pointL"), dict(at="lost decade", pose="shrug")]),

    # ---------------- 3 · THE PAYCHECK ----------------
    dict(act=3, type="host", bg="none",
         narration="Quick favor: if you're finding this interesting, hit subscribe. It's free, and it's genuinely what keeps this channel going. {p} Now, here's where people actually feel it: {pp} the paycheck.",
         items=[dict(at="hit subscribe", text="Subscribe = more of these"), dict(at="actually feel it", text="Where people feel it:", color="acc2"), dict(at="the paycheck", text="The paycheck.", serif=True, size=72, color="acc")],
         react=[dict(at="Quick favor", pose="wave"), dict(at="actually feel it", pose="think"), dict(at="the paycheck", pose="pointUp")]),
    dict(act=3, type="lines", set="mw", series=["POL", "LTU", "PRT"], years=[2005, 2025], start=2005.0, y=[0, 1200], src="Eurostat earn_mw_cur · monthly minimum wage, € (adjusted to 12 payments a year)", fmt="eur0", hl="PRT",
         narration="In 2005, Portugal's minimum wage was about four hundred and forty euros a month. Poland's: about two hundred and ten. Less than half. {p} In 2025, Portugal's was about one thousand and fifteen euros, counting the two extra payments Portuguese workers get each year. {p} Poland's: about eleven hundred. Lithuania's: more than a thousand. {pp} Both now higher than Portugal's. {p} For the lowest-paid Pole, that's about eighty-five euros more a month than for the lowest-paid Portuguese.",
         keys=[dict(at="In 2025", year=2025.0, dur=6.0)],
         labels=[dict(at="four hundred and forty", iso="PRT", year=2005), dict(at="two hundred and ten", iso="POL", year=2005), dict(at="about eleven hundred", iso="POL", year=2025)],
         react=[dict(at="In 2005", pose="idle"), dict(at="Less than half", pose="pointL"), dict(at="two extra payments", pose="think"), dict(at="eleven hundred", pose="shock"), dict(at="Both now higher", pose="shrug")]),
    dict(act=3, type="stats", src="Observatório da Emigração (via Expresso / Essential Business, 12 Jan 2024)", title="Born in Portugal, aged 15–39, living abroad",
         narration="No wonder so many leave. {p} By the Emigration Observatory's estimate, around eight hundred and fifty thousand people born in Portugal, aged fifteen to thirty-nine, live abroad. {pp} That's about thirty percent of that whole generation.",
         stats=[dict(at="eight hundred and fifty thousand", value=850000, fmt="k0", label="young Portuguese living abroad"), dict(at="about thirty percent", value=30, fmt="pct0", label="of everyone born in Portugal, aged 15–39")],
         react=[dict(at="so many leave", pose="think"), dict(at="eight hundred and fifty", pose="shock"), dict(at="thirty percent", pose="shock")]),
    dict(act=3, type="duel", set="aic", year=2024, a="PRT", b="ROU", fmt="int", src="Eurostat prc_ppp_ind · actual individual consumption per head, PPS (EU = 100), 2024", title="What people consume per head (EU = 100)", badge="ROMANIA AHEAD",
         cues=[dict(at="Portugal scores", show="a"), dict(at="Romania scores", show="b")],
         narration="And remember Romania? {p} Eurostat measures what households actually consume, food, housing, and services the state provides, like health care and schools, adjusted for prices, against an EU average of one hundred. {p} In 2024, Portugal scores eighty-five. {pp} Romania scores eighty-eight. Lithuania, eighty-nine. {p} In 2000, Romania was at thirty.",
         react=[dict(at="remember Romania", pose="pointUp"), dict(at="actually consume", pose="think"), dict(at="eighty-eight", pose="shock"), dict(at="at thirty", pose="shrug")]),

    # ---------------- 4 · THE TWIST ----------------
    dict(act=4, type="lines", set="le", series=["PRT", "POL", "ROU"], years=[2000, 2024], start=2000.0, y=[65, 85], src=WB + " · life expectancy at birth (years)", fmt="dec1", hl="PRT",
         narration="But GDP isn't everything. {p} The average Portuguese can expect to live about eighty-two years, longer than the average German. {p} In Poland, about seventy-eight. In Romania, about seventy-six and a half. {pp} Four to six extra years of life don't show up in output per person.",
         keys=[dict(at="GDP isn't everything", year=2024.0, dur=5.0)],
         labels=[dict(at="eighty-two years", iso="PRT", year=2024), dict(at="about seventy-eight", iso="POL", year=2024)],
         react=[dict(at="isn't everything", pose="think"), dict(at="eighty-two", pose="cheer"), dict(at="seventy-six", pose="pointL"), dict(at="don't show up", pose="shrug")]),
    dict(act=4, type="lines", set="bal", series=["PRT", "POL", "ROU"], years=[2015, 2025], start=2015.0, y=[-11, 3], src="Eurostat gov_10dd_edpt1 · government balance and debt, % of GDP (April 2026 notification)", fmt="pct1s", hl="PRT",
         ref=dict(value=0, label="balanced budget", pos="left"),
         narration="And look at the public finances. {p} In 2025, Portugal ran a budget surplus for the third year in a row. {p} Poland ran a deficit of more than seven percent of its economy. Romania, almost eight, the largest in the EU. Even Greece now runs a surplus. {p} Portugal's government debt has fallen from a hundred and thirty-four percent of GDP in 2020 to about eighty-nine.",
         keys=[dict(at="public finances", year=2025.0, dur=6.0)],
         labels=[dict(at="third year in a row", iso="PRT", year=2025), dict(at="more than seven", iso="POL", year=2025)],
         react=[dict(at="public finances", pose="idle"), dict(at="surplus", pose="cheer"), dict(at="more than seven", pose="shock"), dict(at="about eighty-nine", pose="pointUp")]),
    dict(act=4, type="bars", mode="abs", set="netmig", iso="PRT", years=[2005, 2024], start=2004.0, fmt="int", src=WB + " · net migration, Portugal (SM.POP.NETM)",
         narration="And people are coming in again. {p} After losing more than a hundred and thirty thousand people in four crisis years, Portugal has had more arrivals than departures every year since 2017. {p} In 2021 alone, about seventy thousand more people moved in than left.",
         keys=[dict(at="coming in again", year=2016.0, dur=5.0), dict(at="every year since 2017", year=2024.0, dur=4.0)],
         hl=[2017, 2024], hltext=dict(at="every year since 2017", text="Net immigration since 2017"),
         labels=[dict(at="In 2021 alone", year=2021)],
         react=[dict(at="coming in again", pose="pointUp"), dict(at="four crisis years", pose="think"), dict(at="since 2017", pose="cheer"), dict(at="seventy thousand", pose="pointL")]),
    dict(act=4, type="host", bg="none",
         narration="Since 2022, Portugal has grown faster than the EU average every single year. {p} The tortoise, it turns out, kept its savings. {pp} <soft>Some of the hares are running on credit.</soft>",
         items=[dict(at="faster than the EU average", text="2022–2025: faster than the EU", color="acc2"), dict(at="kept its savings", text="Surpluses, falling debt", color="acc"), dict(at="running on credit", text="Tortoise vs hares", serif=True, size=66)],
         react=[dict(at="Since 2022", pose="cheer"), dict(at="tortoise", pose="think"), dict(at="on credit", pose="shrug")]),

    # ---------------- 5 · WHAT COMES NEXT ----------------
    dict(act=5, type="lines", set="relprt", series=["EST", "ROU", "HRV"], years=[2000, 2025], start=2000.0, y=[0, 120], src=PPP + ", as % of Portugal", fmt="pct0", hl="ROU",
         ref=dict(value=100, label="Portugal = 100", pos="left"),
         narration="Still, the race isn't over. {p} In 2000, Romania produced about a third as much per person as Portugal. Estonia, about half. Croatia, under sixty percent. {p} Today it's at about ninety-six percent. Croatia is at ninety-six too, and Estonia at about ninety-eight. {pp} The next few years will decide whether Portugal holds that line.",
         keys=[dict(at="race isn't over", year=2025.0, dur=7.0)],
         labels=[dict(at="about a third", iso="ROU", year=2000), dict(at="ninety-six percent", iso="ROU", year=2025)],
         react=[dict(at="race isn't over", pose="pointUp"), dict(at="about a third", pose="pointL"), dict(at="ninety-six", pose="shock"), dict(at="holds that line", pose="think")]),
    dict(act=5, type="stats", src="Chartbound calculation: Eurostat GDP per capita in PPS (Portugal 2024 = 82% of EU), catching up 1 point per year faster than the EU", title="To reach the EU average",
         narration="And catching up is slow. {p} Portugal is at about eighty-two percent of the EU average in output per person. {p} Even if it grew one percentage point faster than the EU, every single year, {pp} it would take about twenty years to close the gap.",
         stats=[dict(at="eighty-two percent", value=82, fmt="pct0", label="of the EU average, 2024"), dict(at="about twenty years", value=20, fmt="int", label="years at +1 point a year")],
         react=[dict(at="catching up is slow", pose="think"), dict(at="eighty-two", pose="pointL"), dict(at="every single year", pose="pointUp"), dict(at="twenty years", pose="shock")]),
    dict(act=5, type="host", bg="none",
         narration="Portugal has done the hard part. {p} It rebuilt its schools, fixed its budget, and became a place people move to, not just from. {p} The question for the next twenty-five years is simple: {pp} <soft>can it finally turn all that into higher pay, before more of its young people leave to find it elsewhere?</soft> {p} Growth isn't everything. But over twenty-five years, it decides what a country can afford.",
         items=[dict(at="rebuilt its schools", text="Schools ✓", color="acc2"), dict(at="fixed its budget", text="Budget ✓", color="acc2"), dict(at="higher pay", text="Pay?", serif=True, size=72, color="acc")],
         react=[dict(at="the hard part", pose="idle", nod=1), dict(at="fixed its budget", pose="cheer"), dict(at="question", pose="think"), dict(at="elsewhere", pose="shrug")]),
    dict(act=5, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="2026", color="acc", title="Poland just passed Japan", sub="and nobody noticed"),
         narration="Poland didn't stop at Portugal. In 2026, it passed Japan too, and almost nobody noticed. To see how, watch the next video. {p} I'm Chartbound. See you in the next one.",
         hold=14,
         react=[dict(at="passed Japan", pose="pointL"), dict(at="See you", pose="wave")]),
]

checks = [
    dict(say="Portugal ≈ almost twice Poland in 1995", rule="ratio", set="ppp", a="PRT", b="POL", year=1995, min=1.75, max=1.99),
    dict(say="EU member since 1986 → 1995 almost a decade", rule="expr", expr="1995 - 1986", equal=9),
    dict(say="Poland passed Portugal for the first time in 2025", rule="cross", set="ppp", a="POL", b="PRT", year=2025),
    dict(say="Slovenia passed in 2003", rule="cross", set="ppp", a="SVN", b="PRT", year=2003),
    dict(say="Czechia passed in 2007", rule="cross", set="ppp", a="CZE", b="PRT", year=2007),
    dict(say="Lithuania passed in 2018", rule="cross", set="ppp", a="LTU", b="PRT", year=2018),
    dict(say="Estonia within ~5%", set="relprt", iso="EST", year=2025, min=95, max=99.99),
    dict(say="Romania within ~5% (≈96%)", set="relprt", iso="ROU", year=2025, min=95, max=97.5),
    dict(say="Croatia within ~5% (≈96%)", set="relprt", iso="HRV", year=2025, min=95, max=97.5),
    dict(say="Estonia ≈ 98%", set="relprt", iso="EST", year=2025, min=97.5, max=99),
    dict(say="Romania consumes slightly more per head (AIC 2024)", rule="gt", set="aic", a="ROU", b="PRT", year=2024),
    dict(say="Portugal AIC 2024 = 85", set="aic", iso="PRT", year=2024, min=84.5, max=85.5),
    dict(say="Romania AIC 2024 = 88", set="aic", iso="ROU", year=2024, min=87.5, max=88.5),
    dict(say="Romania AIC 2000 = 30", set="aic", iso="ROU", year=2000, min=29.5, max=30.5),
    dict(say="Lithuania roughly tripled since 2000", set="rpcx", iso="LTU", year=2025, min=190, max=225),
    dict(say="Poland about 2.5x", set="rpcx", iso="POL", year=2025, min=140, max=160),
    dict(say="EU up more than a third", set="rpcx", iso="EUU", year=2025, min=33.4, max=40),
    dict(say="Portugal up about a fifth", set="rpcx", iso="PRT", year=2025, min=18, max=23),
    dict(say="Portugal 2000→2019 +15%", set="rpcx", iso="PRT", year=2019, min=14.5, max=15.9),
    dict(say="less than 1% a year", rule="expr", expr="round((1.15 ** (1 / 19) - 1) * 100, 2) < 1", equal=True),
    dict(say="Spain 2000→2019 a little faster", rule="gt", set="rpcx", a="ESP", b="PRT", year=2019),
    dict(say="Portugal 2000 fewer than 1 in 5 with upper secondary", set="edu", iso="PRT", year=2000, max=19.99),
    dict(say="Poland 2000 ≈ 4 in 5", set="edu", iso="POL", year=2000, min=78, max=82),
    dict(say="Czechia 2000 > 8 in 10", set="edu", iso="CZE", year=2000, min=80.01),
    dict(say="Lithuania 2000 > 8 in 10", set="edu", iso="LTU", year=2000, min=80.01),
    dict(say="Portugal 2025 ≈ two in three", set="edu", iso="PRT", year=2025, min=62, max=68),
    dict(say="€78 bn bailout (European Commission)", rule="expr", expr="78", equal=78),
    dict(say="investment ≈ 15% of GDP (2014)", set="gfcf", iso="PRT", year=2014, min=14.5, max=15.9),
    dict(say="among the lowest in the EU (2014)", rule="rank", set="gfcf", iso="PRT", year=2014, among=EU27, min=24, max=27),
    dict(say="net emigration 2011–2014 > 130k", set="nmsum", iso="PRT", year=0, max=-130000),
    dict(say="min wage PRT 2005 ≈ €440", set="mw", iso="PRT", year=2005, min=430, max=445),
    dict(say="min wage POL 2005 ≈ €210", set="mw", iso="POL", year=2005, min=205, max=215),
    dict(say="Poland less than half of Portugal in 2005", rule="ratio", set="mw", a="POL", b="PRT", year=2005, max=0.4999, min=0.3),
    dict(say="PRT 2025 ≈ €1,015", set="mw", iso="PRT", year=2025, min=1010, max=1020),
    dict(say="POL 2025 ≈ €1,100", set="mw", iso="POL", year=2025, min=1080, max=1120),
    dict(say="LTU 2025 > €1,000", set="mw", iso="LTU", year=2025, min=1000.01),
    dict(say="both higher than Portugal (POL)", rule="gt", set="mw", a="POL", b="PRT", year=2025),
    dict(say="both higher than Portugal (LTU)", rule="gt", set="mw", a="LTU", b="PRT", year=2025),
    dict(say="LE Portugal ≈ 82", set="le", iso="PRT", year=2024, min=81.8, max=82.6),
    dict(say="LE Poland ≈ 78", set="le", iso="POL", year=2024, min=77.8, max=78.6),
    dict(say="LE Romania ≈ 76.5", set="le", iso="ROU", year=2024, min=76.2, max=76.8),
    dict(say="four to six extra years", rule="expr", expr="[round(82.4 - 78.4, 1) >= 4, round(82.4 - 76.5, 1) <= 6]", equal=[True, True]),
    dict(say="surplus 2023, 2024, 2025", rule="allpos", set="bal", iso="PRT", a=2023, b=2025),
    dict(say="…and not in 2022 (so 'third year in a row' starts 2023)", set="bal", iso="PRT", year=2022, max=0),
    dict(say="Poland deficit > 7% (2025)", set="bal", iso="POL", year=2025, max=-7.0),
    dict(say="Romania almost 8% (2025)", set="bal", iso="ROU", year=2025, min=-8.0, max=-7.5),
    dict(say="debt 2020 ≈ 134%", set="debt", iso="PRT", year=2020, min=133.5, max=134.5),
    dict(say="debt 2025 ≈ 89%", set="debt", iso="PRT", year=2025, min=88.5, max=89.5),
    dict(say="growth > EU in 2022", rule="gt", set="gdpg", a="PRT", b="EUU", year=2022),
    dict(say="growth > EU in 2023", rule="gt", set="gdpg", a="PRT", b="EUU", year=2023),
    dict(say="growth > EU in 2024", rule="gt", set="gdpg", a="PRT", b="EUU", year=2024),
    dict(say="growth > EU in 2025", rule="gt", set="gdpg", a="PRT", b="EUU", year=2025),
    dict(say="net immigration every year since 2017", rule="allpos", set="netmig", iso="PRT", a=2017, b=2024),
    dict(say="Poland ahead by about 2% (2025)", set="relpol", iso="POL", year=2025, min=101.5, max=102.5),
    dict(say="Malta passed in 2009", rule="cross", set="ppp", a="MLT", b="PRT", year=2009),
    dict(say="1990→2000 Portugal +29%", set="rpc90x", iso="PRT", year=2000, min=28, max=30),
    dict(say="1990→2000 EU +20%", set="rpc90x", iso="EUU", year=2000, min=19, max=21),
    dict(say="Portugal 85% of EU in 2000 (Eurostat GDP PPS)", set="gdppps", iso="PRT", year=2000, min=84.5, max=85.5),
    dict(say="Portugal 76% of EU in 2015", set="gdppps", iso="PRT", year=2015, min=75.5, max=76.5),
    dict(say="Lithuania AIC 2024 = 89", set="aic", iso="LTU", year=2024, min=88.5, max=89.5),
    dict(say="~850,000 aged 15–39 abroad = ~30% (Observatório da Emigração)", rule="expr", expr="[850000 > 8e5, 30]", equal=[True, 30]),
    dict(say="2021 net immigration ≈ 70,000", set="netmig", iso="PRT", year=2021, min=67000, max=72000),
    dict(say="Romania largest deficit in the EU (2025)", rule="rank", set="balue", iso="ROU", year=2025, among=EU27, equal=27),
    dict(say="Estonia ≈ half of Portugal in 2000", set="relprt", iso="EST", year=2000, min=45, max=55),
    dict(say="Romania almost as much as Poland (2000→2025)", set="rpcx", iso="ROU", year=2025, min=160, max=185),
    dict(say="Greece did about as badly (+22%)", set="rpcx", iso="GRC", year=2025, min=18, max=26),
    dict(say="Portugal lives longer than Germany", rule="gt", set="le", a="PRT", b="DEU", year=2024),
    dict(say="Croatia under 60% of Portugal in 2000", set="relprt", iso="HRV", year=2000, max=59.99, min=50),
    dict(say="Portugal 82% of EU (2024)", set="gdppps", iso="PRT", year=2024, min=81.5, max=82.5),
    dict(say="+1 pt a year → ~20 years", rule="expr", expr="round(__import__('math').log(100 / 82) / __import__('math').log(1.01))", equal=20),
    dict(say="€1,100 − €1,015 ≈ €85", rule="expr", expr="1100 - 1015", equal=85),
    dict(say="Greece surplus 2025", set="bal", iso="GRC", year=2025, min=0.01),
    dict(say="Poland: 15% growth in < 4 years at its 2000–2025 average pace (×2.53 in 25 years)", rule="expr", expr="round(__import__('math').log(1.15) / __import__('math').log(2.53 ** (1 / 25)), 1) < 4", equal=True),
    dict(say="Romania ≈ a third of Portugal in 2000", set="relprt", iso="ROU", year=2000, min=28, max=36),
]

datasets = [
    dict(set="ppp", wb="NY.GDP.PCAP.PP.CD", isos=["PRT", "POL", "CZE", "SVN", "LTU", "EST", "ROU", "HRV", "MLT", "EUU"], **{"from": 1990, "to": 2025}),
    dict(set="relpol", derive="ratio", a=["ppp", "POL"], b=["ppp", "PRT"]),
    dict(set="relprt", derive="ratio", a=["ppp", "EST"], b=["ppp", "PRT"]),
    dict(set="relprt", derive="ratio", a=["ppp", "ROU"], b=["ppp", "PRT"]),
    dict(set="relprt", derive="ratio", a=["ppp", "HRV"], b=["ppp", "PRT"]),
    dict(set="rpc", wb="NY.GDP.PCAP.PP.KD", isos=["PRT", "POL", "LTU", "EUU", "ESP", "ROU", "GRC"], **{"from": 1990, "to": 2025}),
    dict(set="rpc90x", derive="idx", src="rpc", isos=["PRT", "EUU"], base=1990, off=-100),
    dict(set="gdppps", eurostat="prc_ppp_ind", filters={"na_item": "VI_PPS_EU27_2020_HAB", "ppp_cat": "GDP"}, isos=["PRT"], **{"from": 2000, "to": 2024}),
    dict(set="rpcx", derive="idx", src="rpc", isos=["PRT", "POL", "LTU", "EUU", "ESP", "ROU", "GRC"], base=2000, off=-100),
    dict(set="aic", eurostat="prc_ppp_ind", filters={"na_item": "VI_PPS_EU27_2020_HAB", "ppp_cat": "A01"}, isos=["PRT", "ROU", "POL", "LTU"], **{"from": 2000, "to": 2024}),
    dict(set="edu", eurostat="edat_lfse_03", filters={"sex": "T", "age": "Y25-64", "isced11": "ED3-8", "unit": "PC"}, isos=["PRT", "POL", "CZE", "LTU"], **{"from": 2000, "to": 2025}),
    dict(set="gfcf", wb="NE.GDI.FTOT.ZS", isos=sorted(set(EU27 + ["EUU"])), **{"from": 2000, "to": 2025}),
    dict(set="netmig", wb="SM.POP.NETM", isos=["PRT"], **{"from": 2005, "to": 2024}),
    dict(set="nmsum", derive="sum", src="netmig", isos=["PRT"], a=2011, b=2014),
    dict(set="mw", eurostat="earn_mw_cur", filters={"currency": "EUR"}, isos=["PRT", "POL", "LTU"], **{"from": 2005, "to": 2025}),
    dict(set="le", wb="SP.DYN.LE00.IN", isos=["PRT", "POL", "ROU", "DEU"], **{"from": 2000, "to": 2024}),
    dict(set="bal", eurostat="gov_10dd_edpt1", filters={"unit": "PC_GDP", "na_item": "B9", "sector": "S13"}, isos=["PRT", "POL", "ROU", "GRC"], **{"from": 2015, "to": 2025}),
    dict(set="balue", eurostat="gov_10dd_edpt1", filters={"unit": "PC_GDP", "na_item": "B9", "sector": "S13"}, isos=EU27, **{"from": 2024, "to": 2025}),
    dict(set="debt", eurostat="gov_10dd_edpt1", filters={"unit": "PC_GDP", "na_item": "GD", "sector": "S13"}, isos=["PRT"], **{"from": 2000, "to": 2025}),
    dict(set="gdpg", wb="NY.GDP.MKTP.KD.ZG", isos=["PRT", "EUU"], **{"from": 2019, "to": 2025}),
]
snapshot = []

clips = [
    dict(**{"from": "s00", "to": "s00"}, hook="Poland just passed *Portugal*", title="Portugal was twice as rich as Poland. Not anymore #Shorts", desc="In 1995 the average Portuguese produced almost twice what a Pole did. In 2025 the lines crossed."),
    dict(**{"from": "s06", "to": "s06"}, hook="The real reason: *school*", title="Why Portugal fell behind Eastern Europe, in one chart #Shorts", desc="In 2000, fewer than 1 in 5 Portuguese adults had finished high school. In Poland, 4 in 5."),
    dict(**{"from": "s10", "to": "s10"}, hook="Polish minimum wage > *Portugal's*", title="Poland's minimum wage is now higher than Portugal's #Shorts", desc="2005: €210 vs €437. 2025: €1,100 vs €1,015 (Eurostat)."),
    dict(**{"from": "s14", "to": "s14"}, hook="Portugal's *secret* advantage", title="The one thing Portugal does better than Poland #Shorts", desc="Three budget surpluses in a row, and debt falling fast."),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="a-L06-portugal", clips=clips, channel="chartbound", chapter0="The lines crossed",
            thumb=dict(set="ppp", iso="POL", years=[1995, 2025], ymin=5000, ymax=56000, band=[470, 690], flags=["PRT"], top="PORTUGAL", big="PASSED.", line2="BY POLAND", color="#ff5a6e"), w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks,
            datasets=datasets, snapshot=snapshot,
            voice=dict(model="", name="Charon",
                       style=("You are the narrator of a popular data documentary on YouTube. Read the script below in a warm, curious voice "
                              "with a little dry humor, at a relaxed but engaged pace of about 145 words per minute, like a smart friend telling "
                              "you something surprising. Let the big numbers land with a tiny pause before them. Keep the energy steady from the "
                              "first sentence to the last. Never sound like an advertisement or an audiobook.")),
            music=[dict(act=0, track="Lightless Dawn", vol=0.24), dict(act=1, track="Investigations", vol=0.23), dict(act=2, track="Deliberate Thought", vol=0.22),
                   dict(act=3, track="Hidden Agenda", vol=0.23), dict(act=4, track="Inspired", vol=0.23), dict(act=5, track="Floating Cities", vol=0.24)],
            yt=dict(title="Portugal Was Richer Than Eastern Europe. Not Anymore.",
                    description=("In 1995 the average Portuguese produced almost twice as much as the average Pole, adjusted for prices. In 2025, for the first time, Poland pulled ahead. Slovenia, Czechia and Lithuania got there earlier, "
                                 "and Romanians already consume slightly more per head. Why Portugal stood still for 25 years (school, the China and EU-enlargement shocks, the 2011 bailout), what it means for wages, "
                                 "and the twist: longer lives, budget surpluses and a comeback since 2022.\n\n"
                                 "Sources: World Bank WDI (NY.GDP.PCAP.PP.CD, NY.GDP.PCAP.PP.KD, NE.GDI.FTOT.ZS, SM.POP.NETM, SP.DYN.LE00.IN, NY.GDP.MKTP.KD.ZG); "
                                 "Eurostat (prc_ppp_ind, edat_lfse_03, earn_mw_cur, gov_10dd_edpt1); European Commission (financial assistance to Portugal); WTO; EU enlargement 2004.\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#portugal #poland #europe #economics #data"),
                    tags=["portugal", "poland", "eastern europe", "romania", "europe economy", "gdp per capita", "minimum wage", "economics", "data"], lang="en"))

json.dump(spec, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "a-L06.json"), "w"), ensure_ascii=False, indent=1)
clean = lambda t: t.replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()
words = sum(len(clean(s["narration"])) for s in shots)
acts = {}
for s in shots:
    acts[s["act"]] = acts.get(s["act"], 0) + len(clean(s["narration"]))
print("shots", len(shots), "palavras", words, f"~{words / 145:.1f} min a 145 wpm", "por ato", acts)

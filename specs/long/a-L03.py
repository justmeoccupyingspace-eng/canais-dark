"""Gera specs/long/a-L03.json — Chartbound longo #3: "Ireland Is the Richest Country in Europe. It Isn't."
Dados: World Bank (API), Eurostat prc_ppp_ind (AIC e PIB per capita em PPS, UE=100) + pontos citados (CSO, Fiscal Council, ESRI) em snapshot."""
import json, os

ACTS = ["Cold open", "Leprechaun economics", "How profits move", "The real number", "How the Irish live", "The catch"]
EU27 = ["AUT", "BEL", "BGR", "HRV", "CYP", "CZE", "DNK", "EST", "FIN", "FRA", "DEU", "GRC", "HUN", "IRL", "ITA", "LVA", "LTU", "LUX", "MLT", "NLD", "POL", "PRT", "ROU", "SVK", "SVN", "ESP", "SWE"]
EU = EU27 + ["EU"]
WBG = "World Bank · GDP per capita (current US$)"
CSO = "CSO Ireland, Annual National Accounts 2025 (2 Jul 2026)"
ESTAT = "Eurostat prc_ppp_ind · volume indices per capita in PPS (EU27 = 100)"

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="lines", set="gdppc", series=["IRL", "USA", "DEU"], years=[1990, 2024], start=1990.0, src=WBG, fmt="usdk", hl="IRL",
         narration="On paper, Ireland is one of the richest countries on Earth. {p} In 2024, its economy produced about a hundred and thirteen thousand dollars per person. {p} That's more than the United States. {p} It's double Germany. {p} In the whole European Union, only tiny Luxembourg ranks higher.",
         keys=[dict(at="On paper", year=2024.0, dur=6.0)],
         labels=[dict(at="per person", iso="IRL", year=2024), dict(at="United States", iso="USA", year=2024), dict(at="double Germany", iso="DEU", year=2024)],
         react=[dict(at="On paper", pose="pointL"), dict(at="United States", pose="shock"), dict(at="double Germany", pose="idle", nod=1), dict(at="Luxembourg", pose="shrug")]),
    dict(act=0, type="host", bg="lines", set="gdppc", series=["IRL", "USA", "DEU"], years=[1990, 2024], start=2024.0, fmt="usdk",
         narration="But walk around Dublin and ask people if they feel richer than Americans. {pp} You'll get a laugh. {p} Prices are the third highest in the EU. And the average Irish household doesn't live twice as well as a German one. {p} So which is it? {p} Is Ireland rich? <soft>Or is something strange going on with the number?</soft>",
         items=[dict(at="richer than Americans", text="Richer than Americans?"), dict(at="a laugh", text="…not quite.", color="acc"), dict(at="strange going on", text="What's wrong with the number?", serif=True, size=66)],
         react=[dict(at="walk around Dublin", pose="think"), dict(at="a laugh", pose="cheer"), dict(at="So which", pose="shrug"), dict(at="strange", pose="pointL")]),

    # ---------------- 1 · LEPRECHAUN ECONOMICS ----------------
    dict(act=1, type="lines", set="gdppc", series=["IRL", "EUU"], years=[1990, 2014], start=1990.0, src=WBG + " · EU/IMF programme for Ireland (Nov 2010)", fmt="usdk", hl="IRL",
         narration="Ireland wasn't always the rich kid. {p} In 1990, it was poorer than the average EU country. {p} Then came the Celtic Tiger. Foreign tech and drug companies poured in, and through the late nineties, the economy often grew close to ten percent a year. {p} By 2007, Irish GDP per person was about eighty percent above the EU average. {pp} Then the housing bubble burst. The banks collapsed, and in 2010, Ireland needed an eighty-five billion euro rescue from the EU and the IMF.",
         keys=[dict(at="Celtic Tiger", year=2000.0, dur=4.0), dict(at="By 2007", year=2007.0, dur=2.5), dict(at="housing bubble", year=2010.0, dur=2.5)],
         labels=[dict(at="poorer than", iso="IRL", year=1990), dict(at="poorer than", iso="EUU", year=1990, delay=0.5), dict(at="By 2007", iso="IRL", year=2007)],
         kicker=dict(at="eighty-five billion", text="2010 · €85 billion rescue"),
         react=[dict(at="rich kid", pose="shrug"), dict(at="Celtic Tiger", pose="cheer"), dict(at="eighty percent", pose="pointL"), dict(at="banks collapsed", pose="shock")]),
    dict(act=1, type="bars", set="gdpg", iso="IRL", years=[1996, 2024], start=1995.0, src="World Bank · GDP growth (annual %) · CSO (12 Jul 2016)",
         narration="Ireland recovered. And then came the moment the number broke. {p} In 2015, according to the official statistics, Ireland's economy grew by almost twenty-five percent. {p} In one year. {pp} Rich countries don't do that. A good year is two or three percent.",
         keys=[dict(at="Ireland recovered", year=2015.0, dur=4.5)],
         hl=[2015, 2015], hltext=dict(at="almost twenty-five", text="2015: +24.6%"),
         react=[dict(at="number broke", pose="think"), dict(at="almost twenty-five", pose="shock"), dict(at="two or three", pose="shrug")]),
    dict(act=1, type="list", src="Irish Fiscal Advisory Council via Irish Examiner (8 Sep 2016) · Paul Krugman (Jul 2016)", title="What happened in 2015",
         narration="No one in Ireland got twenty-five percent richer. {p} What happened was on paper. A handful of giant multinationals, above all Apple, moved their intellectual property onto Irish books: patents, designs, the rights to their brands. {p} Ireland's capital stock jumped by about three hundred billion euros, in a single year. {p} The economist Paul Krugman gave it a name. {pp} Leprechaun economics.",
         items=[dict(at="giant multinationals", kind="bullet", text="multinationals move IP to Ireland"),
                dict(at="three hundred billion", kind="bullet", text="capital stock: +€300 billion in one year"),
                dict(at="Leprechaun economics", kind="title", text="“LEPRECHAUN ECONOMICS”")],
         react=[dict(at="No one", pose="shrug"), dict(at="above all Apple", pose="pointL"), dict(at="three hundred billion", pose="shock"), dict(at="Leprechaun", pose="cheer")]),

    # ---------------- 2 · HOW PROFITS MOVE ----------------
    dict(act=2, type="cards", n=1, src="Irish corporation tax 12.5% (since 2003); 15% for groups over €750m (Pillar Two, 2024)",
         cards=[dict(t="Low tax", s="12.5% for decades"), dict(t="Paper profits", s="booked in Ireland"), dict(t="Real jobs", s="but far fewer")],
         narration="Why Ireland? {p} For decades, its corporate tax rate was twelve and a half percent, one of the lowest in the rich world. {p} Since 2024, the biggest companies pay fifteen, under a global minimum tax deal. {p} Still low. {p} So companies route their profits through Ireland, often from sales made everywhere else.",
         stat=dict(at="twelve and a half", value=12.5, fmt="pct1", label="Irish corporate tax rate"),
         chips=[dict(at="fifteen", text="15% for big groups since 2024")],
         react=[dict(at="Why Ireland", pose="think"), dict(at="twelve and a half", pose="pointL"), dict(at="Still low", pose="shrug")]),
    dict(act=2, type="cards", n=2, src="CSO; Fiscal Council (2025) · contract manufacturing in national accounts",
         cards=[dict(t="Low tax", s="12.5% for decades"), dict(t="Paper profits", s="booked in Ireland"), dict(t="Real jobs", s="but far fewer")],
         narration="And once the profits are booked in Ireland, they show up in Irish GDP. {p} A phone designed in California and assembled in China can count as an Irish export, because an Irish subsidiary owns the rights. {p} The money passes through, gets counted, {pp} and then most of it leaves again, as profits paid back to foreign owners. {p} Economists call this profit shifting, and by most estimates, Ireland is one of the biggest destinations for it in the world.",
         chips=[dict(at="designed in California", text="designed in the US"), dict(at="assembled in China", text="made in China"), dict(at="Irish export", text="= Irish export (on paper)")],
         react=[dict(at="show up", pose="pointL"), dict(at="Irish export", pose="shock"), dict(at="leaves again", pose="shrug")]),
    dict(act=2, type="list", src="Irish Budget 2015 (Oct 2014) · Reuters (3 Jan 2019): Google, Dutch filings for 2017", title="The Double Irish",
         narration="For years, the most famous trick had a name straight out of a spy novel: the Double Irish. {p} A company set up two Irish subsidiaries, one of them run from a tax haven like Bermuda, and passed its profits between them, often through the Netherlands. {p} Google used it to move billions through Ireland and on to Bermuda. {p} Ireland shut the Double Irish to newcomers in 2015, and closed it completely by 2020.",
         items=[dict(at="two Irish subsidiaries", kind="bullet", text="2 Irish companies, 1 “run” from Bermuda"),
                dict(at="through the Netherlands", kind="bullet", text="profits routed via the Netherlands"),
                dict(at="Google used it", kind="bullet", text="2017 · Google: €19.9B to Bermuda via a Dutch shell"),
                dict(at="shut the Double Irish", kind="strike", text="closed: 2015 for newcomers · 2020 for all")],
         react=[dict(at="spy novel", pose="cheer"), dict(at="Bermuda", pose="pointL"), dict(at="Google", pose="shock"), dict(at="closed it completely", pose="idle", nod=1)]),
    dict(act=2, type="stats", src="European Commission decision (30 Aug 2016) · EU Court of Justice, C-465/20 P (10 Sep 2024)", title="Apple vs the EU",
         narration="And then there's Apple. {p} In 2016, the European Commission found that Apple's main Irish company had paid an effective tax rate as low as zero point zero zero five percent, in 2014. {p} It ordered Ireland to collect thirteen billion euros in back taxes. {p} Ireland fought that order in court for eight years. {pp} It didn't want the money. {p} In 2024, the EU's top court said: take it anyway.",
         stats=[dict(at="zero point zero zero five", value=0.005, fmt="pct3", label="Apple's effective tax rate in Ireland, 2014"), dict(at="thirteen billion", value=13, fmt="eurb", label="back taxes ordered (2016)")],
         react=[dict(at="Apple", pose="pointL"), dict(at="zero point zero zero five", pose="shock"), dict(at="didn't want", pose="shrug"), dict(at="take it anyway", pose="cheer")]),
    dict(act=2, type="stats", src="Revenue / Irish Times (6 Jan 2026) · Irish Fiscal Advisory Council (2025)", title="Who pays Ireland's corporate tax",
         narration="To be clear, Ireland does collect real money from this. {p} In 2025, corporate tax brought in thirty-four point seven billion euros, almost a third of all tax revenue. {p} But it's incredibly concentrated. Just ten company groups paid fifty-six percent of it.",
         stats=[dict(at="thirty-four point seven", value=34.7, fmt="eurb", label="corporate tax, 2025"), dict(at="fifty-six percent", value=56, fmt="pct0", label="paid by just 10 groups (2023)")],
         react=[dict(at="real money", pose="cheer"), dict(at="almost a third", pose="pointUp"), dict(at="fifty-six", pose="shock")]),

    # ---------------- 3 · THE REAL NUMBER ----------------
    dict(act=3, type="host", bg="none",
         narration="By 2017, even Ireland's own statisticians had had enough. {p} GDP had stopped describing the Irish economy. {p} So the Central Statistics Office invented a new number, just for Ireland. {pp} They call it modified gross national income, or GNI star. {p} It's not perfect, but Ireland's own government now uses it to measure things like the national debt.",
         items=[dict(at="had had enough", text="GDP stopped making sense"), dict(at="invented a new number", text="So Ireland invented a new one:"), dict(at="GNI star", text="GNI*", serif=True, size=110, color="acc")],
         react=[dict(at="had had enough", pose="shrug"), dict(at="invented", pose="pointUp"), dict(at="GNI star", pose="cheer")]),
    dict(act=3, type="stack", src=CSO, title="Ireland, 2025: GDP vs GNI*", sub="€ billion, current prices",
         total=602.4, segs=[dict(at="Three hundred thirty-four", value=334.0, text="€334B", label="GNI*: what stays in Ireland", color="acc"),
                            dict(at="two hundred sixty-eight", value=268.4, text="€268B", label="profits, depreciation of foreign IP…", color="warm", ghost=True)],
         narration="GNI star strips out the profits that leave the country, and the paper value of all that foreign-owned intellectual property wearing out. {p} In 2025, Ireland's GDP was six hundred and two billion euros. {p} GNI star? Three hundred thirty-four billion. {p} About two hundred sixty-eight billion euros, roughly forty-five percent of the economy, {pp} either leaves the country or only exists on paper.",
         react=[dict(at="strips out", pose="pointL"), dict(at="six hundred and two", pose="idle"), dict(at="Three hundred thirty-four", pose="shock"), dict(at="only exists on paper", pose="shrug")]),
    dict(act=3, type="duel", src=CSO + " · population April 2025: 5,458,600 (CSO)", title="Per person, 2025",
         left=dict(label="GDP", value=110358, color="warm"), right=dict(label="GNI*", value=61188, color="acc2"), fmt="eurk",
         cues=[dict(at="GDP says", show="a"), dict(at="GNI star says", show="b")],
         narration="Per person, that's a huge difference. {p} GDP says about a hundred and ten thousand euros per Irish resident. {p} GNI star says about sixty-one thousand. {pp} Still a rich country. {p} Just not the richest. {p} In most rich countries, GDP and national income are within a few percent of each other. In Ireland, the gap is close to half.",
         badge="−45%",
         react=[dict(at="huge difference", pose="think"), dict(at="a hundred and ten", pose="pointL"), dict(at="sixty-one", pose="idle"), dict(at="Just not", pose="shrug")]),

    # ---------------- 4 · HOW THE IRISH LIVE ----------------
    dict(act=4, type="lines", set="gdpidx", series=["IRL", "LUX", "DEU"], years=[2000, 2024], start=2000.0, src=ESTAT + " · GDP", fmt="int", hl="IRL",
         ref=dict(value=100, label="EU average = 100", pos="left"),
         narration="But even GNI star measures income, not living standards. {p} For that, Europe's statisticians have a better measure: actual individual consumption. {p} It counts everything households actually use: food, rent, cars, holidays, and public services like health and schools. {p} First, here's GDP per person, adjusted for prices. Ireland is more than twice the EU average. Only Luxembourg is higher.",
         keys=[dict(at="For that", year=2024.0, dur=12.0)],
         labels=[dict(at="more than twice", iso="IRL", year=2024)],
         react=[dict(at="not living standards", pose="think"), dict(at="actual individual consumption", pose="pointUp"), dict(at="more than twice", pose="pointL")]),
    dict(act=4, type="lines", set="aic", series=["IRL", "LUX", "DEU"], years=[2000, 2024], start=2000.0, src=ESTAT + " · actual individual consumption", fmt="int", hl="IRL",
         ref=dict(value=100, label="EU average = 100", pos="left"),
         narration="Now, here's what people actually consume. {pp} Ireland drops to ninety-nine. {p} Just below the EU average. {p} Below Germany, below France, below Belgium. {p} Back in 2006, at the height of the Celtic Tiger boom, it was a hundred and seventeen. {p} Today, the country with the second highest GDP per person in the EU ranks tenth for how its people actually live.",
         keys=[dict(at="Now, here's", year=2024.0, dur=5.0)],
         labels=[dict(at="Ireland drops", iso="IRL", year=2024), dict(at="Below Germany", iso="DEU", year=2024), dict(at="Back in 2006", iso="IRL", year=2006)],
         react=[dict(at="actually consume", pose="pointL"), dict(at="Ireland drops", pose="shock"), dict(at="ranks tenth", pose="shrug")]),
    dict(act=4, type="host", bg="none",
         narration="That doesn't mean Irish people are poor. {p} Wages are high, and the multinationals do employ hundreds of thousands of people. {p} But the headline number is mostly about where giant companies keep their accounts. {pp} <soft>Not about how much richer the Irish are than everyone else.</soft>",
         items=[dict(at="are poor", text="Not poor."), dict(at="Wages are high", text="High wages, real jobs", color="acc2"), dict(at="where giant companies", text="GDP ≈ where companies keep their books", serif=True, size=56, color="acc")],
         react=[dict(at="are poor", pose="idle"), dict(at="Wages are high", pose="cheer"), dict(at="where giant companies", pose="pointUp")]),

    # ---------------- 5 · THE CATCH ----------------
    dict(act=5, type="list", src="CSO goods exports 2025 · Euronews (4 May 2026) · CSO quarterly national accounts Q1–Q2 2026", title="The catch",
         narration="And that makes Ireland's official numbers wildly unstable. {p} In 2025, GDP grew twelve percent, while the domestic economy grew about five. {p} Pharmaceuticals drove it: exports of weight-loss drug ingredients, many rushed to the US ahead of new American tariffs. Exports to America jumped fifty-two percent. {p} Then, in early 2026, GDP fell about seven percent in three months, {p} and jumped ten percent in the next three. {pp} Meanwhile, the domestic economy just kept growing at a normal pace.",
         items=[dict(at="grew twelve percent", kind="bullet", text="2025 · GDP +12.3%"),
                dict(at="about five", kind="bullet", text="domestic economy (MDD) +4.9%"),
                dict(at="weight-loss drug", kind="bullet", text="pharma exports: +41%"),
                dict(at="fifty-two percent", kind="bullet", text="exports to the US: +52%"),
                dict(at="fell about seven", kind="bullet", text="Q1 2026 · GDP ≈ −7%"),
                dict(at="jumped ten", kind="bullet", text="Q2 2026 · GDP +10.2%")],
         react=[dict(at="wildly unstable", pose="think"), dict(at="twelve percent", pose="pointL"), dict(at="weight-loss", pose="shock"), dict(at="fell about seven", pose="shock"), dict(at="normal pace", pose="shrug")]),
    dict(act=5, type="host", bg="none",
         narration="Ireland's government knows the corporate tax money could vanish if a few companies change their plans. {p} So it has started putting billions into two savings funds, instead of spending all of it. {p} Because in an economy where ten companies pay more than half the corporate tax, {pp} <soft>the leprechaun can always leave.</soft>",
         items=[dict(at="could vanish", text="Windfalls can vanish"), dict(at="savings funds", text="→ billions into savings funds", color="acc2"), dict(at="the leprechaun", text="The leprechaun can leave.", serif=True, size=66, color="acc")],
         react=[dict(at="could vanish", pose="think"), dict(at="savings funds", pose="pointUp"), dict(at="leprechaun", pose="shrug")]),
    dict(act=5, type="host", bg="lines", set="aic", series=["IRL", "LUX", "DEU"], years=[2000, 2024], start=2024.0, fmt="int",
         narration="So, is Ireland the richest country in Europe? {p} By GDP, almost: second only to Luxembourg. {p} By what people actually consume, it's ninety-nine. Average. {pp} The truth is somewhere in between: a genuinely prosperous country, {p} with a giant corporate tax machine bolted on top.",
         items=[dict(at="By GDP", text="GDP: #2 in the EU"), dict(at="ninety-nine", text="Consumption: 99 = average", color="acc2"), dict(at="bolted on top", text="Prosperous + a tax machine on top", serif=True, size=56, color="acc")],
         react=[dict(at="richest country", pose="think"), dict(at="Luxembourg", pose="pointUp"), dict(at="Average", pose="shrug"), dict(at="bolted on top", pose="cheer")]),
    dict(act=5, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="0.72", color="acc", title="South Korea's scariest number", sub="and why it just went up"),
         narration="If you want to see a country where the scariest number is real, watch our story on South Korea's birth rate. {p} I'm Chartbound. See you in the next one.",
         hold=14,
         react=[dict(at="South Korea's birth rate", pose="pointL"), dict(at="See you", pose="wave")]),
]

checks = [
    dict(say="about $113k per person (2024)", set="gdppc", iso="IRL", year=2024, approx=113000, tol=0.01),
    dict(say="more than the United States", rule="gt", set="gdppc", a="IRL", b="USA", year=2024),
    dict(say="double Germany (~$56k)", set="gdppc", iso="DEU", year=2024, approx=56450, tol=0.01),
    dict(say="only Luxembourg higher in the EU (GDP per capita, PPS)", rule="rank", set="gdpidx", iso="IRL", year=2024, among=EU27, equal=2),
    dict(say="prices third highest in the EU", rule="rank", set="pli", iso="IRL", year=2024, among=EU27, equal=3),
    dict(say="double Germany (ratio)", rule="ratio", set="gdppc", a="IRL", b="DEU", year=2024, min=1.95, max=2.1),
    dict(say="1990: poorer than EU average", rule="gt", set="gdppc", a="EUU", b="IRL", year=1990),
    dict(say="late 90s close to 10% a year (1997)", set="gdpg", iso="IRL", year=1997, min=9),
    dict(say="late 90s close to 10% a year (1999)", set="gdpg", iso="IRL", year=1999, min=9),
    dict(say="late 90s close to 10% a year (2000)", set="gdpg", iso="IRL", year=2000, min=9),
    dict(say="2007 about 80% above EU", rule="ratio", set="gdppc", a="IRL", b="EUU", year=2007, min=1.75, max=1.85),
    dict(say="2016 → 2024 = eight years", rule="expr", expr="2024 - 2016", equal=8),
    dict(say="almost 25% growth in 2015", set="gdpg", iso="IRL", year=2015, approx=24.6, tol=0.02),
    dict(say="more than twice the EU average (GDP, PPS)", set="gdpidx", iso="IRL", year=2024, min=200),
    dict(say="AIC ninety-nine", set="aic", iso="IRL", year=2024, approx=99, tol=0.006),
    dict(say="below Germany", rule="gt", set="aic", a="DEU", b="IRL", year=2024),
    dict(say="below France", rule="gt", set="aic", a="FRA", b="IRL", year=2024),
    dict(say="below Belgium", rule="gt", set="aic", a="BEL", b="IRL", year=2024),
    dict(say="AIC 117 in 2006", set="aic", iso="IRL", year=2006, approx=117, tol=0.005),
    dict(say="ranks tenth (AIC 2024)", rule="rank", set="aic", iso="IRL", year=2024, among=EU27, equal=10),
    dict(say="GDP €602.4bn − GNI* €334.0bn = €268bn, ~45%", rule="expr", expr="[round(602.4 - 334.0), round((602.4 - 334.0) / 602.4 * 100)]", equal=[268, 45]),
    dict(say="per person €110k vs €61k (pop 5,458,600)", rule="expr", expr="[round(602.4e9 / 5458600 / 1000), round(334.0e9 / 5458600 / 1000)]", equal=[110, 61]),
    dict(say="badge −45%", rule="expr", expr="round((1 - 334.0 / 602.4) * 100)", equal=45),
    dict(say="corporate tax almost a third of €107.4bn", rule="expr", expr="0.3 < 34.7 / 107.4 < 0.334", equal=True),
]
datasets = [
    dict(set="gdppc", wb="NY.GDP.PCAP.CD", isos=["IRL", "USA", "DEU", "LUX", "CHE", "NOR", "EUU"], **{"from": 1990, "to": 2024}),
    dict(set="gdpg", wb="NY.GDP.MKTP.KD.ZG", isos=["IRL"], **{"from": 1990, "to": 2024}),
    dict(set="pop", wb="SP.POP.TOTL", isos=["IRL"], **{"from": 2020, "to": 2024}),
    dict(set="aic", eurostat="prc_ppp_ind", filters={"na_item": "VI_PPS_EU27_2020_HAB", "ppp_cat": "A01"}, isos=EU, **{"from": 2000, "to": 2025}),
    dict(set="gdpidx", eurostat="prc_ppp_ind", filters={"na_item": "VI_PPS_EU27_2020_HAB", "ppp_cat": "GDP"}, isos=EU, **{"from": 2000, "to": 2025}),
    dict(set="pli", eurostat="prc_ppp_ind", filters={"na_item": "PLI_EU27_2020", "ppp_cat": "A01"}, isos=EU, **{"from": 2015, "to": 2025}),
]
snapshot = []

clips = [
    dict(**{"from": "s00", "to": "s01"}, hook="Ireland is 'richer' than America. *It isn't.*", title="Ireland is richer than the US on paper. Here's the catch #Shorts", desc="$113,000 of output per person, more than the US. So why doesn't it feel like it?"),
    dict(**{"from": "s03", "to": "s04"}, hook="Ireland's economy grew *25%* in one year. How?", title="Ireland's economy 'grew' 25% in one year #Shorts", desc="2015: the year Paul Krugman called it leprechaun economics."),
    dict(**{"from": "s08", "to": "s08"}, hook="Apple paid *0.005%* tax in Ireland", title="Apple's tax rate in Ireland was 0.005% #Shorts", desc="And Ireland fought for 8 years NOT to collect €13 billion."),
    dict(**{"from": "s11", "to": "s12"}, hook="*45%* of Ireland's GDP doesn't stay in Ireland", title="Almost half of Ireland's GDP isn't really Irish #Shorts", desc="GDP vs GNI*: €110k vs €61k per person."),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="a-L03-ireland", clips=clips, channel="chartbound", chapter0="Richer than America?",
            thumb=dict(set="gdppc", iso="IRL", years=[1990, 2024], flags=["IRL"], top="IRELAND", big="$113K", line2="EACH?!", color="#3ddc84"), w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks,
            datasets=datasets, snapshot=snapshot,
            voice=dict(model="", name="Charon",
                       style=("You are the narrator of a popular data documentary on YouTube. Read the script below in a warm, curious voice "
                              "with a little dry humor, at a relaxed but engaged pace of about 145 words per minute, like a smart friend telling "
                              "you something surprising. Let the big numbers land with a tiny pause before them. Keep the energy steady from the "
                              "first sentence to the last. Never sound like an advertisement or an audiobook.")),
            music=[dict(act=0, track="Hidden Agenda", vol=0.24), dict(act=1, track="Investigations", vol=0.23), dict(act=2, track="Deliberate Thought", vol=0.22),
                   dict(act=3, track="Floating Cities", vol=0.23), dict(act=4, track="Lightless Dawn", vol=0.25), dict(act=5, track="Inspired", vol=0.23)],
            yt=dict(title="Ireland Is the Richest Country in Europe. It Isn't.",
                    description=("On paper, Ireland produces more per person than the United States. In 2015 its economy \"grew\" 26% in a year. "
                                 "What leprechaun economics is, how multinational profits inflate Irish GDP, the number Ireland invented to fix it (GNI*), "
                                 "and how the Irish actually live compared with the rest of Europe.\n\n"
                                 "Sources: World Bank WDI (NY.GDP.PCAP.CD, NY.GDP.MKTP.KD.ZG, SP.POP.TOTL); Eurostat prc_ppp_ind (AIC and GDP per capita in PPS); "
                                 "CSO Ireland Annual National Accounts 2025; Irish Fiscal Advisory Council (2025); Revenue/Irish Times (Jan 2026); Irish Examiner (Sep 2016).\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#ireland #gdp #economics #data #tax"),
                    tags=["ireland", "gdp", "leprechaun economics", "gni star", "corporate tax", "economics", "data"], lang="en"))

json.dump(spec, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "a-L03.json"), "w"), ensure_ascii=False, indent=1)
words = sum(len(s["narration"].replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()) for s in shots)
print("shots", len(shots), "palavras", words, f"~{words / 145:.1f} min a 145 wpm")

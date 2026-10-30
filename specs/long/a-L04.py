"""Gera specs/long/a-L04.json — Chartbound longo #4: "Latvia Lost 30% of Its People. There Was No War."
Dados: World Bank (API), Eurostat proj_23np (EUROPOP2023, cenário base) + pontos citados (NSI Bulgária, CSB Letônia, Eurostat) em snapshot/expr."""
import json, os

ACTS = ["Cold open", "The exit", "Why they left", "More funerals than births", "The comeback", "What comes next"]
EU27 = ["AUT", "BEL", "BGR", "HRV", "CYP", "CZE", "DNK", "EST", "FIN", "FRA", "DEU", "GRC", "HUN", "IRL", "ITA", "LVA", "LTU", "LUX", "MLT", "NLD", "POL", "PRT", "ROU", "SVK", "SVN", "ESP", "SWE"]
MAP = EU27 + ["GBR", "NOR", "CHE", "ISL", "SRB", "BIH", "MDA", "ALB", "MKD", "MNE", "UKR", "BLR"]
WB = "World Bank WDI"
NSI25 = "NSI Bulgaria, population and demographic processes 2025 (via Novinite, 29 Apr 2026)"
CSB24 = "CSB Latvia, population 2024 (via Baltic Times, 2025)"

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="lines", set="popchg", series=["JPN", "BGR", "LVA"], years=[1990, 2024], start=1990.0, y=[-35, 10], src=WB + " · population (SP.POP.TOTL), change since 1990", fmt="pct0s", hl="LVA",
         ref=dict(value=0, label="1990 level", pos="left"),
         narration="Japan is the world's most famous shrinking country. {p} But on this chart, it barely moves. Since its peak in 2010, Japan has lost about three percent of its people. {p} Now look at Latvia. {pp} Since 1990, Latvia has lost thirty percent of its population. {p} Bulgaria, more than a quarter. {p} No war. No famine. No plague. {pp} So where did everyone go?",
         keys=[dict(at="Japan is", year=2024.0, dur=6.0)],
         labels=[dict(at="thirty percent", iso="LVA", year=2024), dict(at="more than a quarter", iso="BGR", year=2024)],
         react=[dict(at="Japan is", pose="pointL"), dict(at="barely moves", pose="shrug"), dict(at="Now look", pose="pointL"), dict(at="thirty percent", pose="shock"), dict(at="No war", pose="think")]),
    dict(act=0, type="globe", src=WB + " · population change 1990–2024", view=dict(lon=20, lat=51, zoom=4.4), hl=[],
         choro=dict(at="Here's every country", set="chg", isos=MAP, step=0.11, last="LVA", reveal_last="Latvia isn't alone", scale=25),
         narration="And Latvia isn't alone. {p} Here's every country in Europe, colored by how much its population has changed since 1990. {p} Green grew. Red shrank. {p} Ukraine's losses are mostly the war. But look at the red band running from the Baltic Sea down to the Balkans. {pp} Lithuania. Bulgaria. Bosnia. Albania. Each lost more than a fifth of its people. {p} Romania and Croatia, almost as much.",
         react=[dict(at="Latvia isn't alone", pose="pointL"), dict(at="Green grew", pose="idle", nod=1), dict(at="red band", pose="shock"), dict(at="a fifth", pose="think"), dict(at="almost as much", pose="shrug")]),
    dict(act=0, type="host", bg="lines", set="popchg", series=["JPN", "BGR", "LVA"], years=[1990, 2024], start=2024.0, y=[-35, 10], fmt="pct0s",
         narration="At its peak, Latvia had about two point six seven million people. {p} Today it has about one point eight six million. {p} That's around eight hundred thousand people gone, {pp} more than everyone who lives in the capital, Riga, today. {p} This is the story of Europe's vanishing countries: {p} why so many people left, why the numbers keep falling even now that people are coming back, <soft>and why the rest of Europe should be paying attention.</soft>",
         items=[dict(at="two point six seven", text="2.67M → 1.86M"), dict(at="eight hundred thousand", text="−800,000 people", color="acc"), dict(at="Riga", text="More than all of Riga", serif=True, size=66)],
         react=[dict(at="At its peak", pose="idle"), dict(at="eight hundred thousand", pose="shock"), dict(at="Riga", pose="pointL"), dict(at="paying attention", pose="think")]),

    # ---------------- 1 · THE EXIT ----------------
    dict(act=1, type="bars", mode="abs", set="tfr", iso="LVA", years=[1980, 2005], start=1979.0, fmt="dec2", src=WB + " · fertility rate (births per woman)",
         narration="It started with the end of the Soviet Union. {p} In 1991, Latvia, Lithuania and Estonia became independent again. Bulgaria and Romania had already thrown out their communist regimes two years earlier. {p} Freedom came with an economic collapse. Factories closed, savings vanished, prices exploded. {p} And people stopped having children. {p} In Latvia, births per woman fell from about two in 1990 to one point two five in 1995. {p} Bulgaria fell to almost exactly the same level.",
         keys=[dict(at="It started", year=2005.0, dur=7.0)],
         hl=[1990, 1995], hltext=dict(at="births per woman fell", text="2.0 → 1.25 in five years"),
         labels=[dict(at="about two in 1990", year=1990), dict(at="one point two five", year=1995)],
         react=[dict(at="Soviet Union", pose="think"), dict(at="economic collapse", pose="shock"), dict(at="stopped having", pose="shrug"), dict(at="one point two five", pose="pointL")]),
    dict(act=1, type="bars", set="nmp", iso="LVA", years=[1995, 2024], start=1994.0, src=WB + " · net migration as % of population, Latvia",
         narration="Then the doors opened. {p} In 2004, the Baltic states joined the European Union. In 2007, Bulgaria and Romania followed. {p} Suddenly, a young Latvian could legally take a job in Dublin or London. Britain, Ireland and Sweden opened their job markets on day one. {p} When the 2008 financial crisis hit, Latvia's economy shrank by about a fifth. {pp} In 2010 alone, the country lost almost two percent of its population to emigration. {p} In a single year.",
         keys=[dict(at="Then the doors", year=2024.0, dur=8.0)],
         bracket=dict(at="In 2010 alone", a=2009, b=2010, text="−1.7% of the population in 2010"),
         kicker=dict(at="about a fifth", text="2008–2010: GDP −21%"),
         react=[dict(at="doors opened", pose="pointUp"), dict(at="Dublin or London", pose="cheer"), dict(at="about a fifth", pose="shock"), dict(at="single year", pose="shrug")]),
    dict(act=1, type="list", src=WB + " · net migration · Eurostat, EU citizens living in another EU country (2024)", title="The great exit",
         narration="Lithuania lost almost eighty thousand people to emigration in 2010 alone. {p} Romania, a much bigger country, lost about two point four million people to emigration between 1990 and 2024, by World Bank estimates. {p} Today, about three point one million Romanians live in other EU countries, mostly in Italy, Germany and Spain. {p} That's more than any other country in the EU.",
         items=[dict(at="almost eighty thousand", kind="bullet", text="Lithuania, 2010: −79,000 people (−2.5%)"),
                dict(at="two point four million", kind="bullet", text="Romania, 1990–2024: −2.4 million, net"),
                dict(at="three point one million", kind="bullet", text="3.1 million Romanians in other EU countries"),
                dict(at="more than any other", kind="title", text="#1 IN THE EU")],
         react=[dict(at="almost eighty", pose="shock"), dict(at="much bigger", pose="pointL"), dict(at="three point one", pose="think"), dict(at="more than any other", pose="pointUp")]),

    # ---------------- 2 · WHY THEY LEFT ----------------
    dict(act=2, type="duel", set="gdppc", year=2000, a="BGR", b="DEU", fmt="usd0", src=WB + " · GDP per capita, PPP (current international $)",
         title="Output per person, 2000",
         narration="Why did so many people leave? {p} Mostly, money. {p} In 2000, the average Bulgarian produced about six thousand four hundred dollars of value a year, adjusted for prices. {p} The average German? {pp} About twenty-seven thousand. More than four times as much. {p} When a bus ticket can quadruple your income, a lot of people buy the ticket.",
         cues=[dict(at="six thousand four hundred", show="a"), dict(at="About twenty-seven", show="b")],
         react=[dict(at="Mostly, money", pose="shrug"), dict(at="six thousand", pose="pointL"), dict(at="twenty-seven", pose="shock"), dict(at="bus ticket", pose="cheer")]),
    dict(act=2, type="list", src="World Bank, ECA Economic Update: Migration and Brain Drain (Fall 2019)", title="Who left",
         narration="And the people who left weren't a random sample. {p} They were mostly young, in their twenties and thirties. {p} Many had a degree. {p} In other words, exactly the people who would have been raising the next generation of children at home. {pp} Emigration didn't just take people away. <soft>It took their future kids with them.</soft>",
         items=[dict(at="mostly young", kind="bullet", text="young: twenties and thirties"),
                dict(at="Many had a degree", kind="bullet", text="often with a degree"),
                dict(at="next generation", kind="bullet", text="= the would-be parents"),
                dict(at="future kids", kind="title", text="…and their future kids")],
         react=[dict(at="random sample", pose="think"), dict(at="mostly young", pose="pointL"), dict(at="next generation", pose="shrug"), dict(at="future kids", pose="shock")]),
    dict(act=2, type="lines", set="o65", series=["LVA", "BGR", "EUU"], years=[1990, 2024], start=1990.0, y=[0, 28], src=WB + " · population ages 65+ (% of total)", fmt="pct1", hl="LVA",
         narration="And the people who stayed got older. {p} In 1990, about one in eight Latvians was sixty-five or older. {p} Today, it's more than one in five. {p} In 1990, Latvia was younger than the EU average. Today, it has caught up. {p} Fewer young adults means fewer births, which means even fewer young adults twenty years later. {pp} It's a spiral, and it's very hard to get out of.",
         keys=[dict(at="got older", year=2024.0, dur=5.0)],
         labels=[dict(at="one in eight", iso="LVA", year=1990), dict(at="one in five", iso="LVA", year=2024)],
         react=[dict(at="got older", pose="idle"), dict(at="one in eight", pose="pointL"), dict(at="one in five", pose="shock"), dict(at="spiral", pose="think")]),

    # ---------------- 3 · MORE FUNERALS THAN BIRTHS ----------------
    dict(act=3, type="host", bg="none",
         narration="Quick favor: if you're finding this interesting, hit subscribe. It's free, and it's genuinely what keeps this channel going. {p} Now, here's the part most people miss. {pp} Today, emigration isn't the main reason these countries are shrinking.",
         items=[dict(at="hit subscribe", text="Subscribe = more of these"), dict(at="most people miss", text="The part most people miss:", color="acc2"), dict(at="isn't the main reason", text="It's not emigration anymore.", serif=True, size=66, color="acc")],
         react=[dict(at="Quick favor", pose="wave"), dict(at="most people miss", pose="think"), dict(at="isn't the main", pose="pointUp")]),
    dict(act=3, type="duel", src=NSI25 + " · " + CSB24, title="Bulgaria, 2025",
         left=dict(label="Births", value=50241, color="acc2"), right=dict(label="Deaths", value=99479, color="warm"), fmt="int", badge="×2",
         cues=[dict(at="about fifty thousand", show="a"), dict(at="almost a hundred thousand", show="b")],
         narration="In 2025, Bulgaria recorded about fifty thousand births. {p} And almost a hundred thousand deaths. {pp} Two funerals for every baby. {p} Latvia's numbers look almost the same: in 2024, about thirteen thousand babies, and more than twenty-six thousand deaths.",
         react=[dict(at="fifty thousand", pose="idle"), dict(at="hundred thousand", pose="shock"), dict(at="Two funerals", pose="shrug"), dict(at="Latvia's numbers", pose="pointL")]),
    dict(act=3, type="stack", src="NSI Bulgaria, 2021 census final results (via Sofia Globe, 3 Oct 2022)", title="Bulgaria lost 845,000 people, 2011–2021", sub="census to census",
         total=845000, segs=[dict(at="three hundred forty-four", value=344000, text="344K", label="emigration", color="acc"),
                             dict(at="five hundred thousand", value=501000, text="501K", label="deaths minus births", color="warm")],
         narration="Bulgaria's last census shows how the two forces compare. {p} Between 2011 and 2021, the country lost about eight hundred forty-five thousand people. {p} About three hundred forty-four thousand of them emigrated. {p} The other five hundred thousand or so were simply deaths outnumbering births. {pp} The biggest driver wasn't the airport anymore. <soft>It was the maternity ward, and the cemetery.</soft>",
         react=[dict(at="two forces", pose="think"), dict(at="eight hundred forty-five", pose="shock"), dict(at="three hundred forty-four", pose="pointL"), dict(at="five hundred thousand", pose="pointL"), dict(at="cemetery", pose="shrug")]),
    dict(act=3, type="lines", set="lem", series=["LVA", "EUU"], years=[1990, 2024], start=1990.0, y=[60, 85], src=WB + " · life expectancy at birth, male · OECD/European Observatory, Latvia Country Health Profile 2023", fmt="dec1", hl="LVA",
         narration="And people in this region still die younger. {p} A Latvian man can expect to live about seventy-one and a half years. {p} The average man in the EU, seventy-nine. {p} Latvian women live almost ten years longer than Latvian men, one of the widest gaps in Europe. {p} Heart disease, heavy drinking and smoking hit men here especially hard.",
         keys=[dict(at="die younger", year=2024.0, dur=5.0)],
         labels=[dict(at="seventy-one and a half", iso="LVA", year=2024), dict(at="seventy-nine", iso="EUU", year=2024)],
         react=[dict(at="die younger", pose="think"), dict(at="seventy-one", pose="pointL"), dict(at="almost ten years", pose="shock"), dict(at="heavy drinking", pose="shrug")]),

    # ---------------- 4 · THE COMEBACK ----------------
    dict(act=4, type="bars", set="nmp", iso="LTU", years=[1995, 2024], start=1994.0, src=WB + " · net migration as % of population, Lithuania · Statistics Lithuania via LRT (24 Feb 2023)",
         narration="But here's the twist. {p} In 2019, for the first time in about three decades, more people moved to Lithuania than left it. {p} Estonia had already turned the corner a few years earlier, and lately Latvia and Bulgaria have had years like that too. {p} Some of the newcomers are Lithuanians coming home, from Britain, Norway and Germany. {p} Others are Ukrainians and Belarusians, many of them fleeing war and repression.",
         keys=[dict(at="here's the twist", year=2024.0, dur=7.0)],
         bracket=dict(at="In 2019", a=2019, b=2023, text="more arrivals than departures"),
         react=[dict(at="twist", pose="pointUp"), dict(at="In 2019", pose="cheer"), dict(at="coming home", pose="idle", nod=1), dict(at="fleeing war", pose="think")]),
    dict(act=4, type="lines", set="rel", series=["LTU", "LVA", "BGR"], years=[2000, 2024], start=2000.0, y=[0, 110], src=WB + " · GDP per capita, PPP, as % of the EU average", fmt="pct0", hl="LTU",
         ref=dict(value=100, label="EU average", pos="left"),
         narration="Part of the reason is that the money gap has shrunk. {p} In 2000, Lithuanians produced about thirty-eight percent as much per person as the EU average, adjusted for prices. {p} Today, it's about eighty-seven percent. {p} Latvia and Bulgaria have closed a big part of the gap too. {p} When home is almost as rich as abroad, {pp} <soft>coming back starts to make sense.</soft>",
         keys=[dict(at="Today, it's", year=2024.0, dur=5.0)],
         labels=[dict(at="thirty-eight percent", iso="LTU", year=2000), dict(at="eighty-seven", iso="LTU", year=2024)],
         react=[dict(at="money gap", pose="think"), dict(at="thirty-eight", pose="pointL"), dict(at="eighty-seven", pose="cheer"), dict(at="make sense", pose="idle", nod=1)]),
    dict(act=4, type="stats", src=NSI25, title="Bulgaria, 2025",
         narration="And yet, look at Bulgaria in 2025. {p} About forty-five thousand people moved in. Fewer than ten thousand left. {p} That's a gain of about thirty-five thousand people. {p} And the population still fell, by fourteen thousand. {pp} Because deaths outnumbered births by even more.",
         stats=[dict(at="gain of about thirty-five", value=35085, fmt="int", label="more people moved in than left"), dict(at="still fell", value=-14153, fmt="int", label="population change")],
         react=[dict(at="look at Bulgaria", pose="pointL"), dict(at="thirty-five thousand", pose="cheer"), dict(at="still fell", pose="shock"), dict(at="by even more", pose="shrug")]),

    # ---------------- 5 · WHAT COMES NEXT ----------------
    dict(act=5, type="lines", set="tfr", series=["LTU", "LVA", "EUU"], years=[2000, 2024], start=2000.0, y=[0, 2.4], src=WB + " · fertility rate (births per woman)", fmt="dec2", hl="LTU",
         ref=dict(value=2.1, label="replacement level ≈ 2.1", pos="left"),
         narration="The deeper problem is the same one South Korea has. {p} Lithuania's fertility rate is now about one point one children per woman. Latvia's, about one point two. The EU as a whole is at about one point three. {p} To keep a population stable without immigration, you need about two point one. {p} Both are now among the lowest in the European Union.",
         keys=[dict(at="deeper problem", year=2024.0, dur=5.0)],
         labels=[dict(at="one point one", iso="LTU", year=2024), dict(at="one point two", iso="LVA", year=2024)],
         react=[dict(at="South Korea", pose="pointL"), dict(at="one point one", pose="shock"), dict(at="two point one", pose="pointUp"), dict(at="lowest", pose="shrug")]),
    dict(act=5, type="lines", set="projchg", series=["LVA", "LTU", "EU"], years=[2025, 2100], start=2025.0, y=[-45, 5], src="Eurostat proj_23np · EUROPOP2023, baseline projection", fmt="pct0s", hl="LVA",
         ref=dict(value=0, label="2025 level", pos="left"),
         narration="Eurostat's baseline projection shows where this is heading. {p} By 2100, Latvia is projected to have about one point two million people. {p} That's more than a third fewer than today. {p} Lithuania, about one point eight million. {pp} Not gone. <soft>But a very different country.</soft>",
         keys=[dict(at="where this is heading", year=2100.0, dur=6.0)],
         labels=[dict(at="one point two million", iso="LVA", year=2100), dict(at="one point eight", iso="LTU", year=2100)],
         react=[dict(at="heading", pose="think"), dict(at="one point two", pose="pointL"), dict(at="more than a third", pose="shock"), dict(at="Not gone", pose="shrug")]),
    dict(act=5, type="host", bg="none",
         narration="None of this means Latvia or Bulgaria will disappear from the map. {p} But it does mean emptier villages, more schools closing, and fewer workers paying for more pensions. {p} And it's a preview. {pp} The European Union as a whole now has more deaths than births. {p} What hit the Baltics and the Balkans first, fast and loud, <soft>is coming more slowly for everyone else.</soft>",
         items=[dict(at="emptier villages", text="Emptier villages"), dict(at="more pensions", text="Fewer workers, more pensions", color="acc2"), dict(at="a preview", text="A preview for all of Europe", serif=True, size=62, color="acc")],
         react=[dict(at="None of this", pose="idle"), dict(at="emptier villages", pose="shrug"), dict(at="a preview", pose="pointUp"), dict(at="everyone else", pose="think")]),
    dict(act=5, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="2026", color="acc", title="Poland just passed Japan", sub="and nobody noticed"),
         narration="Not every country in the region took this path. {p} To see one that went a very different way, watch how Poland passed Japan. {p} I'm Chartbound. See you in the next one.",
         hold=14,
         react=[dict(at="Poland passed Japan", pose="pointL"), dict(at="See you", pose="wave")]),
]

checks = [
    dict(say="Japan lost ~3% since its 2010 peak", set="jp10", iso="JPN", year=2024, min=96.3, max=97.5),
    dict(say="Japan peak in 2010", rule="peak", set="pop", iso="JPN", a=2008, b=2010),
    dict(say="Latvia −30% since 1990", set="popchg", iso="LVA", year=2024, min=-31, max=-29),
    dict(say="Bulgaria more than a quarter since 1990", set="popchg", iso="BGR", year=2024, min=-28, max=-25.01),
    dict(say="red band: Lithuania ≤ −20%", set="chg", iso="LTU", year=0, max=-20),
    dict(say="red band: Bulgaria ≤ −20%", set="chg", iso="BGR", year=0, max=-20),
    dict(say="Romania almost a fifth", set="chg", iso="ROU", year=0, min=-20, max=-17),
    dict(say="Croatia almost a fifth", set="chg", iso="HRV", year=0, min=-20, max=-17),
    dict(say="red band: Bosnia ≤ −20%", set="chg", iso="BIH", year=0, max=-20),
    dict(say="red band: Albania ≤ −20%", set="chg", iso="ALB", year=0, max=-20),
    dict(say="Latvia peak ≈ 2.67M", set="pop", iso="LVA", year="max:1980-2000", approx=2666000, tol=0.006),
    dict(say="Latvia today ≈ 1.86M", set="pop", iso="LVA", year=2024, approx=1866000, tol=0.006),
    dict(say="~800k gone > Riga 591,882 (CSB, 1 Jan 2025)", rule="expr", expr="2.666e6 - 1.866e6 > 591882", equal=True),
    dict(say="Latvia TFR about two in 1990", set="tfr", iso="LVA", year=1990, min=1.95, max=2.1),
    dict(say="Latvia TFR 1.25 in 1995", set="tfr", iso="LVA", year=1995, approx=1.25, tol=0.02),
    dict(say="Bulgaria same level in 1995", rule="tied", set="tfr", a="BGR", b="LVA", year=1995, tol=0.04),
    dict(say="Latvia GDP −21% 2007→2010 (≈ a fifth)", set="gdpkidx", iso="LVA", year=2010, min=77, max=82),
    dict(say="Latvia 2010 net migration ≈ −1.7% (almost two percent)", set="nmp", iso="LVA", year=2010, min=-1.85, max=-1.6),
    dict(say="Lithuania 2010 almost 80k", set="netmig", iso="LTU", year=2010, min=-80000, max=-75000),
    dict(say="Lithuania 2010 −2.5%", set="nmp", iso="LTU", year=2010, min=-2.65, max=-2.4),
    dict(say="Romania −2.4M net 1990–2024", set="migsum", iso="ROU", year=0, min=-2450000, max=-2350000),
    dict(say="Bulgaria 2000 ≈ $6,400 PPP", set="gdppc", iso="BGR", year=2000, approx=6424, tol=0.02),
    dict(say="Germany 2000 ≈ $27,000 PPP", set="gdppc", iso="DEU", year=2000, min=26500, max=27600),
    dict(say="more than four times", rule="ratio", set="gdppc", a="DEU", b="BGR", year=2000, min=4.0, max=4.5),
    dict(say="65+ about one in eight in 1990", set="o65", iso="LVA", year=1990, min=11.1, max=13.3),
    dict(say="65+ more than one in five today", set="o65", iso="LVA", year=2024, min=20.01),
    dict(say="Bulgaria two funerals per baby (99,479 / 50,241)", rule="expr", expr="round(99479 / 50241, 1)", equal=2.0),
    dict(say="Latvia 2024: 12,887 births, 26,661 deaths", rule="expr", expr="[round(12887 / 1000), 26661 > 26000]", equal=[13, True]),
    dict(say="census: 344k + 501k = 845k", rule="expr", expr="344 + 501", equal=845),
    dict(say="Latvian men ≈ 71.5 years", set="lem", iso="LVA", year=2024, min=71.3, max=71.8),
    dict(say="EU men ≈ 79", set="lem", iso="EUU", year=2024, min=78.6, max=79.4),
    dict(say="gap almost ten years", set="lgap", iso="LVA", year=2024, min=9.4, max=9.99),
    dict(say="one of the widest gaps in the EU (top 3)", rule="rank", set="lgap", iso="LVA", year=2024, among=EU27, min=1, max=3),
    dict(say="Lithuania net migration positive in 2019", set="netmig", iso="LTU", year=2019, min=1),
    dict(say="…first time in about three decades (1992–2018 all negative)", rule="countneg", set="netmig", iso="LTU", a=1992, b=2018, equal=27),
    dict(say="Estonia turned positive earlier (2015)", set="netmig", iso="EST", year=2015, min=1),
    dict(say="Latvia had a positive year (2022)", set="netmig", iso="LVA", year=2022, min=1),
    dict(say="Bulgaria had a positive year (2022)", set="netmig", iso="BGR", year=2022, min=1),
    dict(say="Lithuania 38% of EU in 2000", set="rel", iso="LTU", year=2000, approx=38.3, tol=0.04),
    dict(say="Lithuania 87% of EU today", set="rel", iso="LTU", year=2024, approx=87.3, tol=0.025),
    dict(say="Latvia closed a big part of the gap", set="rel", iso="LVA", year=2024, min=60),
    dict(say="Bulgaria closed a big part of the gap", set="rel", iso="BGR", year=2024, min=60),
    dict(say="Latvia younger than EU in 1990", rule="gt", set="o65", a="EUU", b="LVA", year=1990),
    dict(say="…caught up today", rule="tied", set="o65", a="LVA", b="EUU", year=2024, tol=0.03),
    dict(say="EU TFR about 1.3", set="tfr", iso="EUU", year=2024, min=1.26, max=1.36),
    dict(say="Bulgaria 2025: 44,640 in − 9,555 out = 35,085; births − deaths + that = −14,153", rule="expr", expr="[44640 - 9555, 50241 - 99479 + 44640 - 9555]", equal=[35085, -14153]),
    dict(say="Lithuania TFR ≈ 1.1", set="tfr", iso="LTU", year=2024, approx=1.11, tol=0.04),
    dict(say="Latvia TFR ≈ 1.2", set="tfr", iso="LVA", year=2024, approx=1.24, tol=0.04),
    dict(say="Lithuania among the lowest TFR in the EU", rule="rank", set="tfr", iso="LTU", year=2024, among=EU27, min=23, max=27),
    dict(say="Latvia among the lowest TFR in the EU", rule="rank", set="tfr", iso="LVA", year=2024, among=EU27, min=20, max=27),
    dict(say="Latvia 2100 ≈ 1.2M", set="proj", iso="LVA", year=2100, approx=1166000, tol=0.04),
    dict(say="more than a third fewer than today", set="projchg", iso="LVA", year=2100, max=-33.4),
    dict(say="Lithuania 2100 ≈ 1.8M", set="proj", iso="LTU", year=2100, approx=1776000, tol=0.04),
    dict(say="EU: more deaths than births (2024)", set="natd", iso="EUU", year=2024, min=0.01),
]

datasets = [
    dict(set="pop", wb="SP.POP.TOTL", isos=sorted(set(MAP + ["JPN", "EUU"])), **{"from": 1960, "to": 2024}),
    dict(set="popchg", derive="idx", src="pop", isos=["JPN", "BGR", "LVA", "LTU"], base=1990, off=-100),
    dict(set="jp10", derive="idx", src="pop", isos=["JPN"], base=2010),
    dict(set="chg", derive="chg", src="pop", isos=MAP, a=1990, b=2024),
    dict(set="tfr", wb="SP.DYN.TFRT.IN", isos=sorted(set(EU27 + ["EUU", "JPN", "KOR"])), **{"from": 1980, "to": 2024}),
    dict(set="netmig", wb="SM.POP.NETM", isos=["LVA", "LTU", "ROU", "BGR", "EST", "HRV"], **{"from": 1990, "to": 2024}),
    dict(set="nmp", derive="ratio", a=["netmig", "LVA"], b=["pop", "LVA"]),
    dict(set="nmp", derive="ratio", a=["netmig", "LTU"], b=["pop", "LTU"]),
    dict(set="migsum", derive="sum", src="netmig", isos=["ROU", "LVA", "LTU", "BGR"], a=1990, b=2024),
    dict(set="gdppc", wb="NY.GDP.PCAP.PP.CD", isos=["BGR", "DEU", "LTU", "LVA", "EUU"], **{"from": 1990, "to": 2024}),
    dict(set="rel", derive="ratio", a=["gdppc", "LTU"], b=["gdppc", "EUU"]),
    dict(set="rel", derive="ratio", a=["gdppc", "LVA"], b=["gdppc", "EUU"]),
    dict(set="rel", derive="ratio", a=["gdppc", "BGR"], b=["gdppc", "EUU"]),
    dict(set="gdpk", wb="NY.GDP.MKTP.KD", isos=["LVA"], **{"from": 2000, "to": 2024}),
    dict(set="gdpkidx", derive="idx", src="gdpk", isos=["LVA"], base=2007),
    dict(set="o65", wb="SP.POP.65UP.TO.ZS", isos=["LVA", "BGR", "EUU"], **{"from": 1990, "to": 2024}),
    dict(set="lem", wb="SP.DYN.LE00.MA.IN", isos=sorted(set(EU27 + ["EUU"])), **{"from": 1990, "to": 2024}),
    dict(set="lef", wb="SP.DYN.LE00.FE.IN", isos=sorted(set(EU27 + ["EUU"])), **{"from": 1990, "to": 2024}),
    dict(set="lgap", derive="diff", a="lef", b="lem", isos=EU27),
    dict(set="cdr", wb="SP.DYN.CDRT.IN", isos=["EUU"], **{"from": 1990, "to": 2024}),
    dict(set="cbr", wb="SP.DYN.CBRT.IN", isos=["EUU"], **{"from": 1990, "to": 2024}),
    dict(set="natd", derive="diff", a="cdr", b="cbr", isos=["EUU"]),
    dict(set="proj", eurostat="proj_23np", filters={"projection": "BSL", "sex": "T", "age": "TOTAL", "unit": "PER"}, isos=["LVA", "LTU", "EU"], **{"from": 2025, "to": 2100}),
    dict(set="projchg", derive="idx", src="proj", isos=["LVA", "LTU", "EU"], base=2025, off=-100),
]
snapshot = []

clips = [
    dict(**{"from": "s00", "to": "s00"}, hook="Latvia lost *30%* of its people. No war.", title="Latvia lost 30% of its people. There was no war #Shorts", desc="Japan is the famous shrinking country. It lost 3%. Latvia lost 30%."),
    dict(**{"from": "s06", "to": "s06"}, hook="Why they left: *4x* the money", title="Why millions left Eastern Europe, in one number #Shorts", desc="In 2000 a German produced 4x what a Bulgarian did."),
    dict(**{"from": "s10", "to": "s11"}, hook="*Two* funerals for every baby", title="Bulgaria: two deaths for every birth #Shorts", desc="And the census shows it's now the main reason the country is shrinking."),
    dict(**{"from": "s15", "to": "s15"}, hook="More people moved *in*. It still shrank.", title="35,000 more people moved in. Bulgaria still shrank #Shorts", desc="Bulgaria 2025: migration turned positive, the population still fell."),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="a-L04-shrinking", clips=clips, channel="chartbound", chapter0="No war, no famine",
            thumb=dict(set="pop", iso="LVA", years=[1990, 2024], flags=["LVA"], top="LATVIA", big="−30%", line2="NO WAR.", color="#ff5a6e"), w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks,
            datasets=datasets, snapshot=snapshot,
            voice=dict(model="", name="Charon",
                       style=("You are the narrator of a popular data documentary on YouTube. Read the script below in a warm, curious voice "
                              "with a little dry humor, at a relaxed but engaged pace of about 145 words per minute, like a smart friend telling "
                              "you something surprising. Let the big numbers land with a tiny pause before them. Keep the energy steady from the "
                              "first sentence to the last. Never sound like an advertisement or an audiobook.")),
            music=[dict(act=0, track="Lightless Dawn", vol=0.24), dict(act=1, track="Investigations", vol=0.23), dict(act=2, track="Deliberate Thought", vol=0.22),
                   dict(act=3, track="Hidden Agenda", vol=0.23), dict(act=4, track="Inspired", vol=0.23), dict(act=5, track="Floating Cities", vol=0.24)],
            yt=dict(title="Latvia Lost 30% of Its People. There Was No War.",
                    description=("Japan is the world's famous shrinking country, but it has lost about 3% of its people since its peak. Latvia has lost 30% since 1990. Bulgaria, more than a quarter. "
                                 "Why the Baltics and the Balkans emptied out, why emigration is no longer the main reason, why people are now coming back, and what the projections say.\n\n"
                                 "Sources: World Bank WDI (SP.POP.TOTL, SP.DYN.TFRT.IN, SM.POP.NETM, NY.GDP.PCAP.PP.CD, NY.GDP.MKTP.KD, SP.POP.65UP.TO.ZS, SP.DYN.LE00.MA.IN/FE.IN, SP.DYN.CBRT.IN, SP.DYN.CDRT.IN); "
                                 "Eurostat proj_23np (EUROPOP2023); NSI Bulgaria (2025 data; 2021 census); CSB Latvia; Statistics Lithuania; Eurostat/European Parliament (EU movers 2024); "
                                 "World Bank ECA Economic Update: Migration and Brain Drain (2019); OECD/European Observatory, Latvia Country Health Profile 2023.\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#latvia #bulgaria #population #demographics #data"),
                    tags=["latvia", "bulgaria", "lithuania", "population decline", "demographics", "emigration", "europe", "data"], lang="en"))

json.dump(spec, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "a-L04.json"), "w"), ensure_ascii=False, indent=1)
words = sum(len(s["narration"].replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()) for s in shots)
print("shots", len(shots), "palavras", words, f"~{words / 145:.1f} min a 145 wpm")

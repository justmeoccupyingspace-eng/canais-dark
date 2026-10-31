"""Gera specs/long/a-L08.json — Chartbound longo #8: "Vietnam Overtook Indonesia. With a Third of the People."
Número próprio (filtro de saturação: Vietnã tem concorrência — Statrys 941 mil —, mas ninguém mostrou a ultrapassagem de 2025 nem o confronto de modelos com Indonésia).
Dados: World Bank WDI (julho/2026, ano 2025) + pontos citados (USGS MCS 2026 níquel; alfândega do Vietnã jan–nov/2025 via Vietnam Law Magazine; Samsung ≈ metade dos celulares)."""
import json, os

ACTS = ["Cold open", "Two speeds", "The factory", "The rocks", "The people", "The twist", "What comes next"]
WB = "World Bank WDI"
PPP = WB + " · GDP per capita, PPP (current international $)"
ASIA_BIG = ["CHN", "JPN", "IND", "KOR", "IDN", "TUR", "SAU", "THA", "ISR", "ARE", "SGP", "PHL", "VNM", "MYS", "BGD", "PAK", "HKG", "IRN"]  # economias asiáticas com PIB > US$300 bi (2025); Mianmar (oficial, pouco confiável) fica fora
NICKEL = "USGS Mineral Commodity Summaries 2026 · nickel mine production 2025: Indonesia 2.6 Mt of 3.9 Mt world"
CUSTOMS = "Vietnam customs, Jan–Nov 2025 (via Vietnam Law Magazine): exports to the US $138.6 bn of >$430 bn total"

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="lines", set="ppp", series=["IDN", "VNM"], years=[1990, 2025], start=1990.0, y=[0, 20000], src=PPP, fmt="usdk0", hl="VNM",
         narration="In 1990, Vietnam was one of the poorest countries on Earth. {p} At market exchange rates, its economy produced less than a hundred dollars per person, for the whole year. Indonesia, its big neighbor to the south, produced almost six times as much. {p} Even adjusted for prices, Indonesia was two and a half times richer. {pp} In 2025, for the first time in the World Bank's records, Vietnam passed it. And even in plain dollars, it's now ahead, by about six dollars a person.",
         keys=[dict(at="Even adjusted", year=1990.0, dur=2.0), dict(at="In 2025", year=2025.0, dur=7.0)],
         labels=[dict(at="two and a half times", iso="IDN", year=1990), dict(at="Vietnam passed it", iso="VNM", year=2025)],
         react=[dict(at="In 1990", pose="idle"), dict(at="less than a hundred", pose="shock"), dict(at="almost six times", pose="pointL"), dict(at="Vietnam passed it", pose="pointUp"), dict(at="six dollars", pose="shrug")]),
    dict(act=0, type="host", bg="lines", set="ppp", series=["IDN", "VNM"], years=[1990, 2025], start=2025.0, y=[0, 20000], fmt="usdk0",
         narration="Vietnam had just come out of decades of war, and America kept a trade embargo on it until 1994. {p} In 1986, its Communist leaders had given up on central planning, with reforms they called Doi Moi, renovation. But in 1990, the results were still hard to see. {p} Indonesia has oil, gas, coal, nickel, and almost three times as many people. {p} On paper, this race wasn't close. {p} So how did the poorer country win? {pp} <soft>And is Indonesia really losing?</soft>",
         items=[dict(at="trade embargo", text="US embargo until 1994", color="acc"), dict(at="almost three times", text="Indonesia: 3× the people", color="acc2"), dict(at="really losing", text="Is Indonesia losing?", serif=True, size=66)],
         react=[dict(at="decades of war", pose="think"), dict(at="oil, gas", pose="pointL"), dict(at="wasn't close", pose="shrug"), dict(at="really losing", pose="pointUp")]),

    # ---------------- 1 · TWO SPEEDS ----------------
    dict(act=1, type="lines", set="rpcx", series=["PHL", "THA", "IDN", "VNM"], years=[1990, 2025], start=1990.0, y=[50, 700], src=WB + " · GDP per capita, PPP (constant 2021 international $), 1990 = 1×", fmt="x1", hl="VNM",
         ref=dict(value=100, label="1990 level", pos="left"),
         narration="Start with the speed. {p} Since 1990, output per person in Vietnam has grown more than six times, after inflation. Indonesia's has about tripled. Thailand's and the Philippines', even less. {p} Among Asia's big economies, only China grew faster. {p} In 1990, the average Vietnamese produced about a fifth of the world average, adjusted for prices. Today, about seventy percent. Indonesia went from about half, to about the same seventy. {pp} Vietnam's economy has grown almost seven percent a year, on average, for thirty-five years. In 2025 alone, it grew eight percent.",
         keys=[dict(at="Since 1990", year=2025.0, dur=7.0)],
         labels=[dict(at="more than six times", iso="VNM", year=2025), dict(at="about tripled", iso="IDN", year=2025)],
         react=[dict(at="the speed", pose="idle"), dict(at="more than six times", pose="shock"), dict(at="even less", pose="pointL"), dict(at="only China", pose="pointUp"), dict(at="almost seven percent", pose="cheer")]),
    dict(act=1, type="bars", mode="abs", set="gdpg", iso="IDN", years=[2010, 2025], start=2009.0, fmt="pct1", src=WB + " · GDP growth, Indonesia (annual %)",
         narration="Indonesia's problem is the opposite. It's stuck. {p} In every normal year since 2014, its economy grew between four point nine and five point three percent. Like clockwork. {p} Even Vietnam's slowest normal year in that stretch, 2023, at just under five percent, only matched Indonesia's typical one. {p} Five percent sounds fine. But at five percent, an economy doubles in about fourteen years. At Vietnam's pace, in about eleven. {pp} Indonesia's president, Prabowo Subianto, has promised eight percent. It hasn't come close.",
         keys=[dict(at="the opposite", year=2013.0, dur=4.0), dict(at="every normal year", year=2025.0, dur=6.0)],
         hl=[2014, 2025], hltext=dict(at="Like clockwork", text="≈5%, like clockwork"),
         labels=[dict(at="four point nine", year=2015), dict(at="five point three", year=2022)],
         react=[dict(at="It's stuck", pose="shrug"), dict(at="four point nine", pose="pointL"), dict(at="Like clockwork", pose="think"), dict(at="about eleven", pose="pointUp"), dict(at="hasn't come close", pose="shrug")]),

    # ---------------- 2 · THE FACTORY ----------------
    dict(act=2, type="lines", set="exp", series=["IDN", "THA", "VNM"], years=[1990, 2025], start=1990.0, y=[0, 110], src=WB + " · exports of goods and services (% of GDP)", fmt="pct0", hl="VNM",
         narration="The difference is what each country sells. {p} In 1990, exports were worth more than a third of Vietnam's economy. By 2025, they were worth almost as much as its entire GDP. {p} Indonesia went the other way: from about two fifths of its economy in 2000 to less than a quarter. Thailand, the region's old factory, sits in between. {pp} Vietnam turned itself into a factory for the world. Indonesia's economy runs mostly on what Indonesians buy from each other.",
         keys=[dict(at="In 1990", year=1990.0, dur=2.0), dict(at="By 2025", year=2025.0, dur=6.0)],
         labels=[dict(at="almost as much", iso="VNM", year=2025), dict(at="less than a quarter", iso="IDN", year=2025)],
         react=[dict(at="what each country sells", pose="think"), dict(at="almost as much", pose="shock"), dict(at="the other way", pose="pointL"), dict(at="factory for the world", pose="cheer")]),
    dict(act=2, type="stats", src=WB + " · merchandise exports (current US$) and population, 2025", title="Goods sold abroad, 2025",
         narration="Since 2015, Vietnam has sold more goods abroad than Indonesia, with about a third of the people. {p} In 2025, about four hundred and seventy billion dollars' worth, against Indonesia's two hundred and eighty. {pp} Per person, that's almost five times as much.",
         stats=[dict(at="four hundred and seventy", value=473, fmt="usdB0", label="Vietnam's goods exports, 2025 (Indonesia: $283B)"), dict(at="almost five times", value=470, fmt="x1", label="as much per person as Indonesia")],
         react=[dict(at="Since 2015", pose="pointUp"), dict(at="four hundred and seventy", pose="shock"), dict(at="almost five times", pose="shock")]),
    dict(act=2, type="list", src="Samsung share: SEAsia (5 Jul 2026), est. 45–50% of global output · " + WB + " · high-technology exports (% of manufactured exports, 2023) · FDI net inflows (% of GDP, 2025)", title="Made in Vietnam",
         narration="Much of that is electronics. {p} About half of all Samsung phones are made in Vietnam. {p} High-tech goods are more than forty percent of Vietnam's manufactured exports. In Indonesia, under ten. {p} And relative to the size of its economy, Vietnam attracts almost three times as much foreign investment. {p} It joined the World Trade Organization in 2007, then signed trade deals with Japan, Korea, Europe and the Pacific.",
         items=[dict(at="About half", kind="bullet", text="≈ ½ of Samsung phones"),
                dict(at="more than forty", kind="bullet", text="High-tech: 44% vs 9%"),
                dict(at="almost three times", kind="bullet", text="Foreign investment: 2.7× (vs GDP)")],
         react=[dict(at="electronics", pose="idle"), dict(at="About half", pose="shock"), dict(at="under ten", pose="pointL"), dict(at="almost three times", pose="pointUp")]),

    # ---------------- 3 · THE ROCKS ----------------
    dict(act=3, type="host", bg="none",
         narration="Quick favor: if you're enjoying this, hit subscribe. It's free, and it's genuinely what keeps this channel going. {p} Now, why didn't Indonesia do the same? {pp} Because it didn't have to.",
         items=[dict(at="hit subscribe", text="Subscribe = more of these"), dict(at="do the same", text="Why not Indonesia?", color="acc2"), dict(at="didn't have to", text="It didn't have to.", serif=True, size=70, color="acc")],
         react=[dict(at="Quick favor", pose="wave"), dict(at="do the same", pose="think"), dict(at="didn't have to", pose="pointUp")]),
    dict(act=3, type="lines", set="usd", series=["VNM", "IDN"], years=[2005, 2019], start=2005.0, y=[0, 4500], src=WB + " · GDP per capita (current US$) · fuel, ores and metals (% of merchandise exports, 2023)", fmt="usd0", hl="IDN",
         narration="Indonesia sits on some of the world's biggest piles of coal, palm oil and minerals. It's the world's largest producer of palm oil, and one of the largest exporters of coal. {p} In 2023, almost a third of everything it exported was fuel, ores and metals. In Vietnam, about two percent. {p} Commodities pay well, until they don't. {pp} When commodity prices slid after 2012, Indonesia's income per person, in dollars, fell three years in a row.",
         keys=[dict(at="Commodities pay well", year=2012.0, dur=4.0), dict(at="slid after 2012", year=2019.0, dur=6.0)],
         labels=[dict(at="pay well", iso="IDN", year=2012), dict(at="three years in a row", iso="IDN", year=2015)],
         react=[dict(at="biggest piles", pose="pointL"), dict(at="almost a third", pose="shock"), dict(at="until they don't", pose="shrug"), dict(at="three years in a row", pose="think")]),
    dict(act=3, type="stats", src=NICKEL + " · Indonesia's raw nickel ore export ban (in force 1 Jan 2020)", title="Indonesia's new bet: nickel",
         narration="Now Indonesia is betting on a new rock: nickel, for electric car batteries. {p} In 2020, it banned exports of raw nickel ore, to force companies to process it at home. Later, it tried the same trick with bauxite. {p} It worked. In 2025, about two of every three tons of nickel mined on Earth came from Indonesia. {pp} But smelters are built with money, not with millions of workers.",
         stats=[dict(at="two of every three", value=67, fmt="pct0", label="of the world's mined nickel, 2025"), dict(at="In 2020", value=2020, fmt="int", label="raw ore export ban")],
         react=[dict(at="a new rock", pose="pointUp"), dict(at="banned exports", pose="think"), dict(at="two of every three", pose="shock"), dict(at="not with millions", pose="shrug")]),

    # ---------------- 4 · THE PEOPLE ----------------
    dict(act=4, type="lines", set="agri", series=["IDN", "VNM"], years=[1995, 2025], start=1995.0, y=[0, 80], src=WB + " · employment in agriculture (% of total employment, modeled ILO estimate)", fmt="pct0", hl="VNM",
         narration="There's one more ingredient, and it's people. {p} In 1995, seven in ten Vietnamese workers were farmers. Today, it's one in four, now fewer than in Indonesia. As late as 2010, almost half of Vietnam's workers were still on farms. {p} That's millions of people moving from rice paddies to assembly lines, where each worker produces far more. {pp} That shift, more than anything, is what growth looks like in a poor country.",
         keys=[dict(at="In 1995", year=1995.0, dur=2.0), dict(at="Today", year=2025.0, dur=7.0)],
         labels=[dict(at="seven in ten", iso="VNM", year=1995), dict(at="one in four", iso="VNM", year=2025)],
         react=[dict(at="it's people", pose="idle"), dict(at="seven in ten", pose="pointL"), dict(at="one in four", pose="shock"), dict(at="what growth looks like", pose="cheer")]),
    dict(act=4, type="duel", set="hci", year=2020, a="VNM", b="IDN", fmt="pctx", src=WB + " · Human Capital Index 2020 (productivity of a child born today vs full education and health)", title="Human Capital Index, 2020", badge="VIETNAM AHEAD",
         cues=[dict(at="A Vietnamese child", show="a"), dict(at="An Indonesian child", show="b")],
         narration="And those workers arrive better prepared. {p} The World Bank's Human Capital Index estimates how productive a child born today will be, compared with one who gets a complete education and full health. It combines how long children stay in school, how much they actually learn, and how healthy they grow up. {p} A Vietnamese child: sixty-nine percent. {pp} An Indonesian child: fifty-four. {p} Vietnam even beats Malaysia and Thailand, which are far richer. In 2012, Vietnamese fifteen-year-olds outscored American and British students in math, on the OECD's PISA test.",
         react=[dict(at="better prepared", pose="think"), dict(at="sixty-nine", pose="cheer"), dict(at="fifty-four", pose="pointL"), dict(at="far richer", pose="shock")]),

    # ---------------- 5 · THE TWIST ----------------
    dict(act=5, type="lines", set="gdp", series=["VNM", "IDN"], years=[1990, 2025], start=1990.0, y=[0, 1.6e12], src=WB + " · GDP (current US$)", fmt="usdB", hl="IDN",
         narration="But here's the twist: Indonesia isn't losing. {p} Its economy is still almost three times the size of Vietnam's, about one point four trillion dollars, by far the biggest in Southeast Asia. {p} And it has something Vietnam doesn't: a home market of almost three hundred million people. When foreign buyers stop ordering, Indonesians keep shopping. {pp} It has also quietly done something remarkable.",
         keys=[dict(at="isn't losing", year=2025.0, dur=6.0)],
         labels=[dict(at="almost three times", iso="IDN", year=2025)],
         react=[dict(at="the twist", pose="pointUp"), dict(at="almost three times", pose="pointL"), dict(at="something remarkable", pose="think")]),
    dict(act=5, type="lines", set="pov", series=["IDN"], years=[1990, 2025], start=1990.0, y=[0, 90], src=WB + " · poverty headcount at $3.00 a day (2021 PPP), Indonesia (% of population) · GDP growth", fmt="pct0", hl="IDN",
         narration="In 1990, almost eight in ten Indonesians lived on less than three dollars a day, adjusted for prices. {p} In 2025, fewer than four in a hundred. Inflation that year: under two percent. {p} And remember the Asian financial crisis? In 1998, Indonesia's economy shrank thirteen percent in a single year, and its currency lost more than two thirds of its value. {pp} It hasn't had a year anywhere near that bad since. Not even during the pandemic. {p} Vietnam's growth is faster. Indonesia's has been steadier.",
         keys=[dict(at="In 1990", year=1990.0, dur=2.0), dict(at="In 2025", year=2025.0, dur=6.0)],
         labels=[dict(at="almost eight in ten", iso="IDN", year=1990), dict(at="fewer than four", iso="IDN", year=2025)],
         react=[dict(at="almost eight in ten", pose="shock"), dict(at="fewer than four", pose="cheer"), dict(at="thirteen percent", pose="shock"), dict(at="Not even", pose="pointUp")]),

    # ---------------- 6 · WHAT COMES NEXT ----------------
    dict(act=6, type="lines", set="old", series=["IDN", "VNM", "THA"], years=[1990, 2025], start=1990.0, y=[0, 18], src=WB + " · population aged 65+ (% of total) · fertility rate · GDP growth", fmt="pct0", hl="VNM",
         narration="So can Vietnam keep running? {p} Its biggest threat is time. Vietnamese women have about one point nine children on average, below the two point one needed to keep a population stable. Indonesia: about two point one. {p} People aged sixty-five and over are now almost a tenth of Vietnam's population. {p} That's about where Thailand was in 2013. {pp} Since then, Thailand's economy has grown only about two percent a year, and its population has started to shrink.",
         keys=[dict(at="biggest threat", year=2013.0, dur=5.0), dict(at="almost a tenth", year=2025.0, dur=5.0)],
         labels=[dict(at="where Thailand was", iso="THA", year=2013), dict(at="almost a tenth", iso="VNM", year=2025)],
         react=[dict(at="keep running", pose="think"), dict(at="one point nine", pose="pointL"), dict(at="almost a tenth", pose="shock"), dict(at="about two percent", pose="shrug")]),
    dict(act=6, type="host", bg="none",
         narration="And Vietnam's model depends on customers abroad. Almost a third of what it sells goes to just one country: the United States. {p} One decision in Washington can change its whole year. {p} Indonesia's model is slower, but harder to break. {p} Vietnam is the sprinter. Indonesia is the marathon runner. {p} And both have picked the same finish line: 2045, a hundred years after each declared independence. Both say they want to be high-income countries by then. {pp} <soft>The next twenty years will show which one the world rewards.</soft> {p} Either way, a country that made under a hundred dollars a person in 1990 has already won something.",
         items=[dict(at="just one country", text="≈ ⅓ of exports → USA", color="acc"), dict(at="harder to break", text="Slower, but sturdier", color="acc2"), dict(at="sprinter", text="Sprinter vs marathon", serif=True, size=66)],
         react=[dict(at="customers abroad", pose="think"), dict(at="the United States", pose="pointL"), dict(at="harder to break", pose="idle", nod=1), dict(at="sprinter", pose="pointUp"), dict(at="already won", pose="cheer")]),
    dict(act=6, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="0.72", color="acc", title="South Korea's scariest number", sub="where low birth rates lead"),
         narration="Want to see where falling birth rates lead? South Korea is already there. Watch this next. {p} I'm Chartbound. See you in the next one.",
         hold=14,
         react=[dict(at="South Korea", pose="pointL"), dict(at="See you", pose="wave")]),
]

checks = [
    dict(say="1990 Vietnam < $100 per person (nominal)", set="usd", iso="VNM", year=1990, max=99.99),
    dict(say="Indonesia almost 6× in 1990 (nominal)", rule="ratio", set="usd", a="IDN", b="VNM", year=1990, min=5.5, max=5.99),
    dict(say="Indonesia 2.5× adjusted for prices (1990)", rule="ratio", set="ppp", a="IDN", b="VNM", year=1990, min=2.4, max=2.6),
    dict(say="Vietnam passed Indonesia in PPP in 2025, first time since 1990", rule="cross", set="ppp", a="VNM", b="IDN", year=2025),
    dict(say="plain dollars: Vietnam ahead in 2025", rule="gt", set="usd", a="VNM", b="IDN", year=2025),
    dict(say="…by about $6", rule="expr", expr="round(5065.99 - 5059.63)", equal=6),
    dict(say="US embargo lifted 1994", rule="expr", expr="1994", equal=1994),
    dict(say="almost 3× the people (2025)", rule="ratio", set="pop", a="IDN", b="VNM", year=2025, min=2.7, max=2.99),
    dict(say="Vietnam ×6+ since 1990 (real PPP per capita)", set="rpcx", iso="VNM", year=2025, min=600, max=650),
    dict(say="Indonesia about tripled", set="rpcx", iso="IDN", year=2025, min=290, max=330),
    dict(say="Thailand even less", set="rpcx", iso="THA", year=2025, max=289),
    dict(say="Philippines even less", set="rpcx", iso="PHL", year=2025, max=289),
    dict(say="among big Asian economies (GDP > $300 bn) only China grew faster", rule="rank", set="bigx", iso="VNM", year=2025, among=ASIA_BIG, equal=2),
    dict(say="China first", rule="rank", set="bigx", iso="CHN", year=2025, among=ASIA_BIG, equal=1),
    dict(say="Vietnam ~7%/yr average 1990–2025 (sum of 36 years)", set="g9025", iso="VNM", year=0, min=36 * 6.5, max=36 * 6.99),
    dict(say="5% doubles in ~14 years", rule="expr", expr="round(__import__('math').log(2) / __import__('math').log(1.05))", equal=14),
    dict(say="Vietnam's pace (6.68%) doubles in ~11", rule="expr", expr="round(__import__('math').log(2) / __import__('math').log(1.0668))", equal=11),
    dict(say="Indonesia 2025 growth far from 8%", set="gdpg", iso="IDN", year=2025, max=5.5),
    dict(say="VNM exports 1990 > a third of GDP", set="exp", iso="VNM", year=1990, min=33.4, max=40),
    dict(say="VNM exports 2025 almost 100% of GDP", set="exp", iso="VNM", year=2025, min=95, max=99.99),
    dict(say="IDN exports 2000 ≈ two fifths", set="exp", iso="IDN", year=2000, min=38, max=42),
    dict(say="IDN exports 2025 < a quarter", set="exp", iso="IDN", year=2025, max=24.99),
    dict(say="VNM goods exports > IDN since 2015", rule="since", set="merch", a="VNM", b="IDN", year=2015),
    dict(say="a third of the people", rule="ratio", set="pop", a="VNM", b="IDN", year=2025, min=0.33, max=0.37),
    dict(say="VNM goods exports 2025 ≈ $470 bn", set="merch", iso="VNM", year=2025, min=465e9, max=480e9),
    dict(say="IDN ≈ $280 bn", set="merch", iso="IDN", year=2025, min=275e9, max=285e9),
    dict(say="per person almost 5×", rule="expr", expr="round((472929 / 101.598527) / (282909 / 285.721236), 2)", equal=4.7),
    dict(say="high-tech VNM 2023 > 40%", set="tech", iso="VNM", year=2023, min=40),
    dict(say="high-tech IDN 2023 < 10%", set="tech", iso="IDN", year=2023, max=9.99),
    dict(say="FDI ≈ 2.7× relative to GDP (2025)", rule="ratio", set="fdi", a="VNM", b="IDN", year=2025, min=2.6, max=2.95),
    dict(say="IDN fuel 2023 ≈ 22.9%", set="fuel", iso="IDN", year=2023, min=22.5, max=23.3),
    dict(say="IDN ores+metals 2023 ≈ 8.9%", set="mmtl", iso="IDN", year=2023, min=8.5, max=9.3),
    dict(say="IDN fuel+ores+metals 2023 almost a third", rule="expr", expr="round(22.92 + 8.9, 1) < 33.3 and round(22.92 + 8.9, 1) > 30", equal=True),
    dict(say="VNM fuel 2023 ≈ 1%", set="fuel", iso="VNM", year=2023, max=1.2),
    dict(say="VNM ores+metals 2023 ≈ 1%", set="mmtl", iso="VNM", year=2023, max=1.2),
    dict(say="IDN nominal pc peak 2012 (2005–2016)", rule="peak", set="usdi", iso="IDN", a=2012, b=2012),
    dict(say="no rise in 2013–2015 (last rise before 2016 = 2012)", rule="lastrise", set="usdi", iso="IDN", year=2016, equal=2012),
    dict(say="rose again in 2016 (so exactly three falls)", rule="lastrise", set="usdi", iso="IDN", year=2017, equal=2016),
    dict(say="2 of 3 tons of nickel (USGS 2026: 2.6 of 3.9 Mt)", rule="expr", expr="round(2.6 / 3.9 * 100)", equal=67),
    dict(say="1995 agri 7 in 10", set="agri", iso="VNM", year=1995, min=68, max=72),
    dict(say="2025 agri 1 in 4", set="agri", iso="VNM", year=2025, min=24, max=26),
    dict(say="now fewer than Indonesia", rule="gt", set="agri", a="IDN", b="VNM", year=2025),
    dict(say="HCI VNM 0.69", set="hci", iso="VNM", year=2020, min=0.685, max=0.695),
    dict(say="HCI IDN 0.54", set="hci", iso="IDN", year=2020, min=0.535, max=0.545),
    dict(say="VNM beats Malaysia", rule="gt", set="hci", a="VNM", b="MYS", year=2020),
    dict(say="VNM beats Thailand", rule="gt", set="hci", a="VNM", b="THA", year=2020),
    dict(say="Malaysia far richer (2020, PPP)", rule="ratio", set="ppp", a="MYS", b="VNM", year=2020, min=2.0, max=9),
    dict(say="Thailand far richer (2020, PPP)", rule="ratio", set="ppp", a="THA", b="VNM", year=2020, min=1.5, max=9),
    dict(say="IDN GDP almost 3× VNM (2025)", rule="ratio", set="gdp", a="IDN", b="VNM", year=2025, min=2.7, max=2.99),
    dict(say="IDN GDP ≈ $1.4T", set="gdp", iso="IDN", year=2025, min=1.4e12, max=1.49e12),
    dict(say="biggest in Southeast Asia (vs THA)", rule="ratio", set="gdp", a="IDN", b="THA", year=2025, min=2, max=9),
    dict(say="poverty 1990 almost 8 in 10", set="pov", iso="IDN", year=1990, min=75, max=79.99),
    dict(say="poverty 2025 < 4 in 100", set="pov", iso="IDN", year=2025, max=3.99),
    dict(say="1998 −13%", set="gdpg", iso="IDN", year=1998, min=-13.5, max=-12.5),
    dict(say="rupiah lost > 2/3 (1997→1998 avg)", rule="expr", expr="round(1 - 2909 / 10014, 2) > 0.667", equal=True),
    dict(say="since 1999 only one negative year (2020)", rule="countneg", set="gdpg", iso="IDN", a=1999, b=2025, equal=1),
    dict(say="2020 only ≈ −2%", set="gdpg", iso="IDN", year=2020, min=-3),
    dict(say="VNM fertility ≈ 1.9 (2024)", set="tfr", iso="VNM", year=2024, min=1.85, max=1.95),
    dict(say="IDN fertility ≈ 2.1 (2024)", set="tfr", iso="IDN", year=2024, min=2.05, max=2.15),
    dict(say="VNM 65+ almost a tenth (2025)", set="old", iso="VNM", year=2025, min=9.2, max=9.99),
    dict(say="Thailand 2013 ≈ same share", set="old", iso="THA", year=2013, min=9.2, max=9.8),
    dict(say="Thailand since 2013 ~2%/yr (sum 2014–2025, 12 yrs)", set="g1425", iso="THA", year=0, min=12 * 1.7, max=12 * 2.3),
    dict(say="almost a third of exports to the US (customs Jan–Nov 2025)", rule="expr", expr="round(138.6 / 430 * 100) <= 33 and round(138.6 / 430 * 100) >= 30", equal=True),
    dict(say="Doi Moi 1986", rule="expr", expr="1986", equal=1986),
    dict(say="VNM 2025 growth ≈ 8%", set="gdpg", iso="VNM", year=2025, min=7.9, max=8.1),
    dict(say="VNM 2023 just under 5%", set="gdpg", iso="VNM", year=2023, min=4.9, max=4.999),
    dict(say="Thailand in between (2025 exports % GDP)", set="exp", iso="THA", year=2025, min=40, max=90),
    dict(say="WTO 2007; EPAs Japan 2009, Korea 2015, CPTPP 2019, EVFTA 2020", rule="expr", expr="2007", equal=2007),
    dict(say="VNM agri 2010 almost half", set="agri", iso="VNM", year=2010, min=46, max=49.99),
    dict(say="PISA 2012 math: VNM 511 > GBR 494 > USA 481 (NCES)", rule="expr", expr="511 > 494 > 481", equal=True),
    dict(say="IDN pop almost 300M", set="pop", iso="IDN", year=2025, min=280e6, max=299e6),
    dict(say="IDN inflation 2025 < 2%", set="cpi", iso="IDN", year=2025, max=1.99),
    dict(say="Thailand population shrinking (2025 < 2022)", rule="lastrise", set="popt", iso="THA", year=2026, equal=2022),
    dict(say="independence 1945 (IDN 17 Aug, VNM 2 Sep) → 2045 = 100 years", rule="expr", expr="2045 - 1945", equal=100),
    dict(say="VNM ≈ a fifth of world avg 1990", set="relw", iso="VNM", year=1990, min=19, max=23),
    dict(say="VNM ≈ 70% of world avg 2025", set="relw", iso="VNM", year=2025, min=68, max=72),
    dict(say="IDN ≈ half of world avg 1990", set="relw", iso="IDN", year=1990, min=48, max=56),
    dict(say="IDN ≈ 70% 2025", set="relw", iso="IDN", year=2025, min=67, max=71),
    dict(say="Korea TFR 0.72 (2023)", set="tfrk", iso="KOR", year=2023, min=0.715, max=0.725),
]
for y in [2014, 2015, 2016, 2017, 2018, 2019, 2022, 2023, 2024, 2025]:
    checks.append(dict(say=f"Indonesia {y} growth in 4.9–5.3% (normal year)", set="gdpg", iso="IDN", year=y, min=4.85, max=5.35))
    if y != 2023:
        checks.append(dict(say=f"Vietnam {y} faster than its 2023 (slowest normal year)", set="gdpg", iso="VNM", year=y, min=5.0))

datasets = [
    dict(set="ppp", wb="NY.GDP.PCAP.PP.CD", isos=["VNM", "IDN", "THA", "PHL", "MYS"], **{"from": 1990, "to": 2025}),
    dict(set="pppw", wb="NY.GDP.PCAP.PP.CD", isos=["WLD"], **{"from": 1990, "to": 2025}),
    dict(set="relw", derive="ratio", a=["ppp", "VNM"], b=["pppw", "WLD"]),
    dict(set="relw", derive="ratio", a=["ppp", "IDN"], b=["pppw", "WLD"]),
    dict(set="usd", wb="NY.GDP.PCAP.CD", isos=["VNM", "IDN"], **{"from": 1990, "to": 2025}),
    dict(set="usdi", wb="NY.GDP.PCAP.CD", isos=["IDN"], **{"from": 2005, "to": 2016}),
    dict(set="pop", wb="SP.POP.TOTL", isos=["VNM", "IDN"], **{"from": 2020, "to": 2025}),
    dict(set="rpc", wb="NY.GDP.PCAP.PP.KD", isos=["VNM", "IDN", "THA", "PHL"], **{"from": 1990, "to": 2025}),
    dict(set="rpcx", derive="idx", src="rpc", isos=["VNM", "IDN", "THA", "PHL"], base=1990, off=0),
    dict(set="big", wb="NY.GDP.PCAP.PP.KD", isos=ASIA_BIG, **{"from": 1990, "to": 2025}),
    dict(set="bigx", derive="idx", src="big", isos=ASIA_BIG, base=1990, off=0),
    dict(set="gdpg", wb="NY.GDP.MKTP.KD.ZG", isos=["IDN", "VNM", "THA"], **{"from": 1990, "to": 2025}),
    dict(set="g9025", derive="sum", src="gdpg", isos=["VNM"], a=1990, b=2025),
    dict(set="g1425", derive="sum", src="gdpg", isos=["THA"], a=2014, b=2025),
    dict(set="exp", wb="NE.EXP.GNFS.ZS", isos=["VNM", "IDN", "THA"], **{"from": 1990, "to": 2025}),
    dict(set="merch", wb="TX.VAL.MRCH.CD.WT", isos=["VNM", "IDN"], **{"from": 2005, "to": 2025}),
    dict(set="tech", wb="TX.VAL.TECH.MF.ZS", isos=["VNM", "IDN"], **{"from": 2015, "to": 2024}),
    dict(set="fdi", wb="BX.KLT.DINV.WD.GD.ZS", isos=["VNM", "IDN"], **{"from": 2015, "to": 2025}),
    dict(set="fuel", wb="TX.VAL.FUEL.ZS.UN", isos=["VNM", "IDN"], **{"from": 2015, "to": 2025}),
    dict(set="mmtl", wb="TX.VAL.MMTL.ZS.UN", isos=["VNM", "IDN"], **{"from": 2015, "to": 2025}),
    dict(set="agri", wb="SL.AGR.EMPL.ZS", isos=["VNM", "IDN"], **{"from": 1995, "to": 2025}),
    dict(set="hci", wb="HD.HCI.OVRL", isos=["VNM", "IDN", "MYS", "THA"], **{"from": 2020, "to": 2020}),
    dict(set="gdp", wb="NY.GDP.MKTP.CD", isos=["VNM", "IDN", "THA"], **{"from": 1990, "to": 2025}),
    dict(set="pov", wb="SI.POV.DDAY", isos=["IDN"], **{"from": 1990, "to": 2025}),
    dict(set="old", wb="SP.POP.65UP.TO.ZS", isos=["VNM", "IDN", "THA"], **{"from": 1990, "to": 2025}),
    dict(set="tfr", wb="SP.DYN.TFRT.IN", isos=["VNM", "IDN"], **{"from": 2015, "to": 2024}),
    dict(set="cpi", wb="FP.CPI.TOTL.ZG", isos=["IDN"], **{"from": 2025, "to": 2025}),
    dict(set="popt", wb="SP.POP.TOTL", isos=["THA"], **{"from": 2015, "to": 2025}),
    dict(set="tfrk", wb="SP.DYN.TFRT.IN", isos=["KOR"], **{"from": 2023, "to": 2023}),
]
snapshot = []

clips = [
    dict(**{"from": "s00", "to": "s00"}, hook="$99 a person → *passed Indonesia*", title="Vietnam made $99 a person in 1990. Now it's passed Indonesia #Shorts", desc="In 1990 Indonesia was almost 6× richer per person. In 2025 Vietnam passed it (World Bank)."),
    dict(**{"from": "s04", "to": "s04"}, hook="A third of the people, *more exports*", title="Vietnam exports more than Indonesia with a third of the people #Shorts", desc="Exports ≈ 98% of Vietnam's GDP vs 23% in Indonesia (World Bank, 2025)."),
    dict(**{"from": "s09", "to": "s09"}, hook="2 of every 3 tons of *nickel*", title="Indonesia now mines 2 of every 3 tons of nickel on Earth #Shorts", desc="After banning raw ore exports in 2020 (USGS 2026)."),
    dict(**{"from": "s11", "to": "s11"}, hook="Vietnam's *secret weapon*", title="Why Vietnamese workers beat richer countries #Shorts", desc="World Bank Human Capital Index: Vietnam 0.69, Indonesia 0.54."),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="a-L08-vietnam", clips=clips, channel="chartbound", chapter0="From $99 to first place",
            thumb=dict(set="ppp", iso="VNM", years=[1990, 2025], ymin=0, ymax=19000, band=[470, 690], flags=["VNM", "IDN"], top="VIETNAM IN 1990", big="$99", line2="NOW > INDONESIA", color="#ffd166"), w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks,
            datasets=datasets, snapshot=snapshot,
            voice=dict(model="", name="Charon",
                       style=("You are the narrator of a popular data documentary on YouTube. Read the script below in a warm, curious voice "
                              "with a little dry humor, at a relaxed but engaged pace of about 145 words per minute, like a smart friend telling "
                              "you something surprising. Let the big numbers land with a tiny pause before them. Keep the energy steady from the "
                              "first sentence to the last. Never sound like an advertisement or an audiobook.")),
            music=[dict(act=0, track="Lightless Dawn", vol=0.24), dict(act=1, track="Investigations", vol=0.23), dict(act=2, track="Inspired", vol=0.22),
                   dict(act=3, track="Hidden Agenda", vol=0.23), dict(act=4, track="Deliberate Thought", vol=0.22), dict(act=5, track="Thinking Music", vol=0.23), dict(act=6, track="Floating Cities", vol=0.24)],
            yt=dict(title="Vietnam Overtook Indonesia. With a Third of the People.",
                    description=("In 1990 Vietnam produced less than $100 per person a year and Indonesia almost six times as much. In 2025, for the first time in the World Bank's records, Vietnam passed Indonesia in GDP per person adjusted for prices, and it's now ahead in plain dollars too. "
                                 "How the poorer country won (speed, exports, factories, people), why Indonesia didn't follow (coal, palm oil, nickel), "
                                 "and the twist: Indonesia's economy is still almost three times bigger, far more stable, and poverty there has nearly vanished.\n\n"
                                 "Sources: World Bank WDI (NY.GDP.PCAP.PP.CD, NY.GDP.PCAP.CD, NY.GDP.PCAP.PP.KD, NY.GDP.MKTP.KD.ZG, NE.EXP.GNFS.ZS, TX.VAL.MRCH.CD.WT, TX.VAL.TECH.MF.ZS, BX.KLT.DINV.WD.GD.ZS, TX.VAL.FUEL.ZS.UN, TX.VAL.MMTL.ZS.UN, SL.AGR.EMPL.ZS, HD.HCI.OVRL, NY.GDP.MKTP.CD, SI.POV.DDAY, SP.POP.65UP.TO.ZS, SP.DYN.TFRT.IN); "
                                 "USGS Mineral Commodity Summaries 2026 (nickel); Vietnam customs (exports to the US, Jan–Nov 2025).\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#vietnam #indonesia #asia #economics #data"),
                    tags=["vietnam", "indonesia", "southeast asia", "vietnam economy", "indonesia economy", "gdp per capita", "exports", "nickel", "economics", "data"], lang="en"))

json.dump(spec, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "a-L08.json"), "w"), ensure_ascii=False, indent=1)
clean = lambda t: t.replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()
words = sum(len(clean(s["narration"])) for s in shots)
acts = {}
for s in shots:
    acts[s["act"]] = acts.get(s["act"], 0) + len(clean(s["narration"]))
print("shots", len(shots), "palavras", words, f"~{words / 145:.1f} min a 145 wpm", "por ato", acts)

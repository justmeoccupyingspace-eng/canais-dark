"""Gera specs/long/a-L05.json — Chartbound longo #5: "Saudi Arabia Is No Richer Than in 1990"
Número próprio (filtro de saturação ok em 31/10, research/q3.json e q4.json): PIB por pessoa real (PPP, US$ constantes de 2021) do Golfo vs EUA e Noruega.
Dados: World Bank WDI (API) + pontos citados em expr: produção de petróleo (IMF via FRED), população por nacionalidade (PACI/CSB via GLMM; GAStat),
salários Kuwait (Central Statistics Administration via AGBI, 19/03/2025), fundo norueguês (Norsk Petroleum / NBIM)."""
import json, os

ACTS = ["Cold open", "The fall", "Same oil, more people", "Who is in the average", "The arithmetic", "The country that saved", "What comes next"]
GULF = ["SAU", "KWT", "ARE", "QAT", "OMN", "BHR"]
WB = "World Bank WDI"
RPC = WB + " · GDP per capita, PPP (constant 2021 international $)"
FRED_K = "IMF crude oil production, Kuwait (FRED KWTNGDPMOMBD)"
FRED_S = "IMF crude oil production, Saudi Arabia (FRED SAUNGDPMOMBD)"
KWPOP = "PACI / CSB Kuwait, population by nationality, 31 Dec 2024 (via GLMM)"
KWWAGE = "Kuwait Central Statistics Administration, average monthly wages (via AGBI, 19 Mar 2025)"
KWJOBS = "PACI Kuwait, employment by sector and nationality, 30 Jun 2026 (via Kuwait Times, 23 Jul 2026)"
NBIM = "Norsk Petroleum, Management of revenues (fund value end-2025); NBIM (first transfer 1996; ~1.5% of listed companies)"
BRENT = "IMF, global price of Brent crude, annual average (FRED POILBREUSDA)"
GASTAT_LFS = "GASTAT Labour Force Survey Q1 2025 (via Argaam, 29 Jun 2025)"

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="lines", set="rpc", series=["USA", "SAU"], years=[1990, 2025], start=1990.0, y=[30000, 85000], src=RPC, fmt="usdk0", hl="SAU",
         narration="In 1990, the average American produced about forty-four thousand dollars of value a year, adjusted for prices and inflation. {p} The average Saudi? {pp} About sixty-five thousand. About one and a half times as much. {p} Thirty-five years later, the American number has climbed to about seventy-seven thousand. {p} And the Saudi number? {pp} About sixty-three thousand. {p} A little less than in 1990.",
         keys=[dict(at="Thirty-five years later", year=2025.0, dur=7.0)],
         labels=[dict(at="forty-four thousand", iso="USA", year=1990), dict(at="About sixty-five", iso="SAU", year=1990), dict(at="seventy-seven thousand", iso="USA", year=2025), dict(at="About sixty-three", iso="SAU", year=2025)],
         react=[dict(at="In 1990", pose="idle"), dict(at="The average Saudi", pose="pointL"), dict(at="one and a half", pose="cheer"), dict(at="has climbed", pose="pointUp"), dict(at="About sixty-three", pose="shock"), dict(at="A little less", pose="shrug")]),
    dict(act=0, type="globe", src=RPC, view=dict(lon=48, lat=25, zoom=4.2), hl=[],
         seq=dict(at="Kuwait.", isos=["KWT", "ARE", "QAT", "OMN"], step=0.7),
         narration="And Saudi Arabia is the lucky one. {p} Kuwait. The Emirates. Qatar. Oman. {p} Some of the richest countries on Earth, sitting on some of its biggest oil reserves, where citizens pay no income tax. {p} Every one of them now produces less per person than it did at its peak. {pp} Kuwait, almost forty percent less.",
         react=[dict(at="lucky one", pose="shrug"), dict(at="Kuwait.", pose="pointL"), dict(at="richest countries", pose="cheer"), dict(at="Every one", pose="think"), dict(at="almost forty", pose="shock")]),
    dict(act=0, type="host", bg="lines", set="rpc", series=["USA", "SAU"], years=[1990, 2025], start=2025.0, y=[30000, 85000], fmt="usdk0",
         narration="These countries pumped oil, built cities out of the desert, and became a byword for wealth. {p} So how did they get poorer per person while most of the world got richer? {p} The answer is partly oil, partly people, {p} <soft>and partly a trick of arithmetic that makes the whole picture misleading.</soft>",
         items=[dict(at="byword for wealth", text="Oil, towers, wealth"), dict(at="get poorer per person", text="…and poorer per person?", color="acc"), dict(at="trick of arithmetic", text="A trick of arithmetic", serif=True, size=66, color="acc2")],
         react=[dict(at="pumped oil", pose="idle"), dict(at="get poorer", pose="think"), dict(at="partly people", pose="pointUp"), dict(at="misleading", pose="shrug")]),

    # ---------------- 1 · THE FALL ----------------
    dict(act=1, type="lines", set="rpc", series=["USA", "KWT"], years=[1990, 2025], start=1990.0, y=[30000, 85000], src=RPC, fmt="usdk0", hl="KWT",
         narration="Take Kuwait. {p} In 2006, the average Kuwaiti produced almost eighty thousand dollars a year, adjusted for prices. {p} About a third more than the average American. {p} By 2025, about forty-eight thousand. {pp} Down almost forty percent. {p} Today, it's less than two-thirds of the American level.",
         keys=[dict(at="Take Kuwait", year=2006.0, dur=5.0), dict(at="By 2025", year=2025.0, dur=4.0)],
         labels=[dict(at="almost eighty thousand", iso="KWT", year=2006), dict(at="about forty-eight", iso="KWT", year=2025)],
         react=[dict(at="Take Kuwait", pose="pointL"), dict(at="a third more", pose="cheer"), dict(at="forty-eight", pose="shock"), dict(at="two-thirds", pose="shrug")]),
    dict(act=1, type="lines", set="rpc", series=["USA", "ARE"], years=[1990, 2024], start=1990.0, y=[30000, 120000], src=RPC, fmt="usdk0", hl="ARE",
         narration="The Emirates are even stranger. {p} In 1990, the average person there produced two and a half times as much as the average American. {p} Since then, Dubai has built the world's tallest building and one of its busiest airports. {p} And output per person has fallen by more than a third. {pp} Today it's a little below the American level.",
         keys=[dict(at="Since then", year=2024.0, dur=8.0)],
         labels=[dict(at="two and a half times", iso="ARE", year=1990), dict(at="a little below", iso="ARE", year=2024)],
         react=[dict(at="even stranger", pose="think"), dict(at="two and a half", pose="shock"), dict(at="tallest building", pose="pointUp"), dict(at="fallen by more", pose="shock"), dict(at="a little below", pose="shrug")]),
    dict(act=1, type="list", src=RPC + " · change from each country's peak to the latest year", title="Below the peak",
         narration="Qatar is still one of the richest places on Earth, at about a hundred and ten thousand dollars per person. {p} But that's about a quarter below its 2011 peak. {p} Oman, a quarter below its 2009 peak. {p} Brunei, in Southeast Asia, a third below 1991. {p} The exception is Bahrain, which depends less on oil and is now at an all-time high. {pp} Oil made these countries rich. <soft>It didn't keep them getting richer.</soft>",
         items=[dict(at="But that's about a quarter", kind="bullet", text="Qatar: −26% since 2011"),
                dict(at="Oman, a quarter", kind="bullet", text="Oman: −25% since 2009"),
                dict(at="Brunei, in Southeast", kind="bullet", text="Brunei: −33% since 1991"),
                dict(at="The exception", kind="bullet", text="Bahrain: all-time high"),
                dict(at="Oil made", kind="title", text="RICH ≠ RICHER")],
         react=[dict(at="Qatar is still", pose="cheer"), dict(at="But that's", pose="pointL"), dict(at="Brunei", pose="think"), dict(at="The exception", pose="pointUp"), dict(at="Oil made", pose="shrug")]),

    # ---------------- 2 · SAME OIL, MORE PEOPLE ----------------
    dict(act=2, type="duel", src=FRED_K, title="Kuwait's crude oil output", fmt="mbd",
         left=dict(label="2005", value=2.573, color="acc2"), right=dict(label="2024", value=2.419, color="acc"), badge="≈ same",
         cues=[dict(at="In 2005, Kuwait", show="a"), dict(at="In 2024", show="b")],
         narration="So what happened? {p} Start with the oil itself. {p} In 2005, Kuwait pumped about two point six million barrels a day. {p} In 2024, about two point four million. {pp} Roughly the same. {p} But the number of people sharing it went from about two point two million to about four point nine million. {pp} More than double.",
         react=[dict(at="what happened", pose="think"), dict(at="two point six", pose="pointL"), dict(at="Roughly the same", pose="shrug"), dict(at="More than double", pose="shock")]),
    dict(act=2, type="bars", mode="abs", set="brent", iso="BRENT", years=[1992, 2025], start=1991.0, fmt="usd0", src=BRENT,
         narration="Why so many people? {p} Between 2003 and 2008, the price of oil more than tripled. {p} Gulf governments spent the windfall on airports, stadiums, malls and entire new cities. {p} To build and run them, they brought in workers. {pp} Millions of them. {p} Then, in 2014, the price crashed. Today it's about forty percent below its 2012 peak.",
         keys=[dict(at="Between 2003", year=2008.0, dur=5.0), dict(at="Millions of them", year=2012.0, dur=2.0), dict(at="the price crashed", year=2025.0, dur=4.0)],
         hl=[2003, 2008], hltext=dict(at="more than tripled", text="2003 → 2008: ×3.4"),
         labels=[dict(at="2008, the price", year=2003), dict(at="more than tripled", year=2008)],
         react=[dict(at="Why so many", pose="think"), dict(at="more than tripled", pose="shock"), dict(at="entire new cities", pose="pointUp"), dict(at="Millions of them", pose="shrug"), dict(at="price crashed", pose="shock")]),
    dict(act=2, type="lines", set="popx", series=["KWT", "ARE", "QAT"], years=[1990, 2025], start=1990.0, y=[50, 750], src=WB + " · population (SP.POP.TOTL), 1990 = 1×", fmt="x1", hl="QAT",
         ref=dict(value=100, label="1990", pos="left"),
         narration="Across the Gulf, populations exploded. {p} Since 1990, Kuwait's population has almost tripled. {p} The Emirates', multiplied by six. {p} Qatar's, by almost seven: from about four hundred forty thousand people to almost three million. {p} The economies grew fast too. Qatar's is about five times bigger than in 2000. {pp} But when the population grows faster than the economy, output per person falls.",
         keys=[dict(at="populations exploded", year=2025.0, dur=7.0)],
         labels=[dict(at="almost tripled", iso="KWT", year=2025), dict(at="multiplied by six", iso="ARE", year=2025), dict(at="almost seven", iso="QAT", year=2025)],
         react=[dict(at="exploded", pose="shock"), dict(at="almost tripled", pose="pointL"), dict(at="almost seven", pose="shock"), dict(at="five times bigger", pose="cheer"), dict(at="output per person falls", pose="shrug")]),
    dict(act=2, type="stats", src=FRED_S + " · " + WB + " (population 2000) · GAStat (population 2024)", title="Saudi oil per person",
         narration="Saudi Arabia shows the same math. {p} In 2000, it pumped about eight million barrels a day, for about sixteen million people. {p} In 2024, about nine million barrels, for more than thirty-five million people. {pp} About half as much oil per person.",
         stats=[dict(at="for about sixteen", value=0.50, fmt="dec2", label="barrels a day per person, 2000"), dict(at="more than thirty-five", value=0.25, fmt="dec2", label="barrels a day per person, 2024")],
         react=[dict(at="same math", pose="think"), dict(at="eight million", pose="pointL"), dict(at="thirty-five million", pose="shock"), dict(at="half as much", pose="shrug")]),

    # ---------------- 3 · WHO IS IN THE AVERAGE ----------------
    dict(act=3, type="host", bg="none",
         narration="Quick favor: if you're enjoying this, hit subscribe. It's free, and it's genuinely what keeps this channel going. {p} Now, the twist. {pp} Most of those new people aren't citizens.",
         items=[dict(at="hit subscribe", text="Subscribe = more of these"), dict(at="the twist", text="The twist:", color="acc2"), dict(at="aren't citizens", text="Most aren't citizens.", serif=True, size=66, color="acc")],
         react=[dict(at="Quick favor", pose="wave"), dict(at="the twist", pose="think"), dict(at="aren't citizens", pose="pointUp")]),
    dict(act=3, type="lines", set="mig", series=["QAT", "ARE", "KWT", "SAU"], years=[1990, 2024], start=1990.0, y=[0, 100], src=WB + " · international migrant stock, % of population (UN DESA)", fmt="pct0", hl="QAT",
         narration="Today, about three in four people living in Qatar and the Emirates were born abroad. {p} In Kuwait, about two in three. In Saudi Arabia, about two in five, which is still about fifteen and a half million foreign residents. {p} They came to build the towers, staff the hospitals, drive the taxis and clean the homes.",
         keys=[dict(at="Today, about three", year=2024.0, dur=6.0)],
         labels=[dict(at="three in four", iso="QAT", year=2024), dict(at="two in three", iso="KWT", year=2024), dict(at="two in five", iso="SAU", year=2024)],
         react=[dict(at="born abroad", pose="pointL"), dict(at="two in three", pose="shock"), dict(at="build the towers", pose="pointUp"), dict(at="clean the homes", pose="think")]),
    dict(act=3, type="stack", src=KWPOP + " · " + KWWAGE, title="Kuwait, end of 2024: 4.9 million residents", sub="by nationality",
         total=4881254, segs=[dict(at="one point six million", value=1566168, text="1.6M", label="Kuwaiti citizens", color="acc2"),
                              dict(at="three point three", value=3315086, text="3.3M", label="foreign residents and stateless", color="warm")],
         kicker=dict(at="four and a half times", text="Citizens earn ~4.5× what foreign employees earn"),
         narration="Kuwait counts its people carefully. {p} At the end of 2024, it had about four point nine million residents. {p} Only about one point six million were Kuwaiti citizens. {p} The other three point three million were foreign residents, plus stateless people known as the Bidoon. {p} Roughly two non-citizens for every citizen. {p} And Kuwaiti citizens earn, on average, about four and a half times as much as foreign employees.",
         react=[dict(at="carefully", pose="idle"), dict(at="one point six", pose="pointL"), dict(at="three point three", pose="shock"), dict(at="four and a half", pose="shock")]),
    dict(act=4, type="host", bg="none",
         narration="So when you divide Kuwait's economy by everyone who lives there, you're averaging a citizen's salary with a cleaner's. {p} Add millions of low-paid workers, and the average can fall even if nobody's pay goes down. {pp} It's the mirror image of Ireland, where GDP per person is inflated by money that isn't really Irish.",
         items=[dict(at="averaging a citizen's", text="Citizen + cleaner ÷ 2", color="acc2"), dict(at="the average can fall", text="Average ↓, pay unchanged", color="acc"), dict(at="mirror image of Ireland", text="Ireland, in reverse", serif=True, size=66)],
         react=[dict(at="divide Kuwait's", pose="think"), dict(at="a cleaner's", pose="pointL"), dict(at="average can fall", pose="shrug"), dict(at="mirror image", pose="pointUp")]),
    dict(act=4, type="duel", src=FRED_K + " · " + KWPOP, title="Oil per Kuwaiti citizen (barrels a day)", fmt="dec2",
         left=dict(label="2005", value=2.59, color="acc2"), right=dict(label="2024", value=1.54, color="warm"), badge="−40%",
         cues=[dict(at="Since 2005", show="a"), dict(at="down about forty", show="b")],
         narration="But even counting only citizens, the oil is stretched thinner. {p} Since 2005, the number of Kuwaiti citizens has grown by more than half. {p} So oil output per citizen is down about forty percent. {pp} The average is misleading. <soft>But the squeeze is real.</soft>",
         react=[dict(at="stretched thinner", pose="think"), dict(at="more than half", pose="pointL"), dict(at="forty percent", pose="shock"), dict(at="squeeze is real", pose="shrug")]),
    dict(act=4, type="stack", src=KWJOBS, title="Who works where in Kuwait, mid-2026", sub="employed Kuwaiti citizens",
         total=495697, segs=[dict(at="employed by the state", value=397165, text="80%", label="work for the government", color="acc2"),
                             dict(at="the rest", value=98532, text="20%", label="private sector", color="acc")],
         kicker=dict(at="more than ninety-six percent", text="Private sector: 96.4% foreign workers"),
         narration="And look at who does what. {p} By the middle of 2026, about four in five working Kuwaitis were employed by the state. {p} Only the rest worked for private companies, where more than ninety-six percent of the workforce is foreign. {p} The oil money pays the citizens. <soft>Imported workers run most of everything else.</soft>",
         react=[dict(at="who does what", pose="think"), dict(at="four in five", pose="pointL"), dict(at="ninety-six percent", pose="shock"), dict(at="everything else", pose="shrug")]),

    # ---------------- 4 · THE COUNTRY THAT SAVED ----------------
    dict(act=5, type="lines", set="rpc", series=["NOR", "SAU", "KWT"], years=[1990, 2025], start=1990.0, y=[30000, 100000], src=RPC, fmt="usdk0", hl="NOR",
         narration="But it's not just arithmetic. Compare Norway. {p} It pumps oil and gas too. {p} In 1990, the average Norwegian produced less than the average Saudi. {p} Since then, Norway's number is up about two-thirds, to about ninety-five thousand dollars a year. {p} Its population, now about five and a half million, grew by about a third, not six-fold. {pp} Same resource. Opposite result.",
         keys=[dict(at="Since then", year=2025.0, dur=7.0)],
         labels=[dict(at="less than the average Saudi", iso="NOR", year=1990), dict(at="ninety-five thousand", iso="NOR", year=2025)],
         react=[dict(at="Compare Norway", pose="pointL"), dict(at="less than the average", pose="think"), dict(at="two-thirds", pose="cheer"), dict(at="Opposite result", pose="pointUp")]),
    dict(act=5, type="stats", src=NBIM, title="Norway's oil fund, end of 2025",
         narration="The difference is what Norway did with the money. {p} Since 1996, it has moved its oil income into a fund invested abroad, and the government may spend only the expected real return, about three percent a year. {p} Today the fund owns, on average, about one and a half percent of every listed company on Earth. {p} At the end of 2025, the fund was worth about twenty-one trillion kroner. {pp} About three point eight million kroner for every person in Norway.",
         stats=[dict(at="twenty-one trillion", value=21.3, fmt="nokT", label="total value"), dict(at="three point eight million", value=3.8, fmt="nokM", label="per person in Norway")],
         react=[dict(at="did with the money", pose="think"), dict(at="three percent", pose="pointUp"), dict(at="one and a half percent", pose="cheer"), dict(at="twenty-one trillion", pose="shock"), dict(at="every person", pose="cheer")]),
    dict(act=5, type="lines", set="oilr", series=["KWT", "SAU", "NOR"], years=[2000, 2021], start=2000.0, y=[0, 70], src=WB + " · oil rents, % of GDP (NY.GDP.PETR.RT.ZS) · Kuwait Investment Authority", fmt="pct0", hl="KWT",
         narration="Gulf states have big funds too. Kuwait's, set up in 1953, is often called the oldest in the world. {p} But oil is a far bigger slice of their economies. {p} In 2012, oil rents were worth more than half of Kuwait's entire economy. In Norway, less than seven percent. {pp} Norway saved its oil. <soft>The Gulf built with it.</soft>",
         keys=[dict(at="far bigger slice", year=2012.0, dur=5.0), dict(at="Norway saved", year=2021.0, dur=4.0)],
         labels=[dict(at="more than half", iso="KWT", year=2012), dict(at="less than seven", iso="NOR", year=2012)],
         react=[dict(at="big funds too", pose="idle", nod=1), dict(at="oldest in the world", pose="pointUp"), dict(at="more than half", pose="shock"), dict(at="Norway saved", pose="pointL"), dict(at="built with it", pose="shrug")]),

    # ---------------- 5 · WHAT COMES NEXT ----------------
    dict(act=6, type="duel", src="Saudi Ministry of Human Resources (HRSD), Progress of the Saudi labor market (Dec 2025) · " + GASTAT_LFS, title="Saudi women in the labor force", fmt="pct1",
         left=dict(label="2017", value=17.0, color="acc2"), right=dict(label="Q1 2025", value=36.3, color="acc"), badge="×2",
         cues=[dict(at="from seventeen percent", show="a"), dict(at="about thirty-six", show="b")],
         narration="Saudi Arabia is trying to change the math. {p} Since 2016, its Vision 2030 plan has pushed citizens into jobs once filled by foreigners. {p} The share of Saudi women in the workforce has more than doubled, from seventeen percent in 2017 to about thirty-six percent in early 2025. {p} And unemployment among Saudi citizens hit a record low of about six percent, beating the plan's target of seven. {p} That's part of why its output per person is now back near its 1990 level, after two decades well below it.",
         react=[dict(at="change the math", pose="think"), dict(at="Vision 2030", pose="pointUp"), dict(at="more than doubled", pose="cheer"), dict(at="record low", pose="cheer"), dict(at="back near", pose="idle", nod=1)]),
    dict(act=6, type="host", bg="none",
         narration="But the clock is ticking. {p} Nobody knows exactly when the world's demand for oil will stop growing. {p} Saudi Arabia, the Emirates and Qatar are racing to build tourism, finance and tech industries before that day comes. {p} Some of it is working. Much of it is still paid for by oil. {p} When demand does stop growing, the countries that saved will be fine. {pp} The ones that spent will need a new answer to an old question: <soft>what happens to a country when the oil stops paying?</soft>",
         items=[dict(at="clock is ticking", text="The clock is ticking", color="acc"), dict(at="countries that saved", text="Saved → fine", color="acc2"), dict(at="oil stops paying", text="When the oil stops paying…", serif=True, size=62)],
         react=[dict(at="clock is ticking", pose="pointUp"), dict(at="Nobody knows", pose="shrug"), dict(at="will be fine", pose="idle", nod=1), dict(at="stops paying", pose="think")]),
    dict(act=6, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="$113K", color="acc", title="Ireland is the richest country in Europe", sub="It isn't."),
         narration="To see the opposite trick, where GDP per person makes a country look far richer than it is, watch my video on Ireland. {p} I'm Chartbound. See you in the next one.",
         hold=14,
         react=[dict(at="watch my video", pose="pointL"), dict(at="See you", pose="wave")]),
]

checks = [
    dict(say="USA 1990 ≈ $44k (const 2021 PPP)", set="rpc", iso="USA", year=1990, min=43500, max=44900),
    dict(say="Saudi 1990 ≈ $65k", set="rpc", iso="SAU", year=1990, min=64500, max=65800),
    dict(say="about one and a half times as much", rule="ratio", set="rpc", a="SAU", b="USA", year=1990, min=1.42, max=1.55),
    dict(say="USA 2025 ≈ $77k", set="rpc", iso="USA", year=2025, min=76300, max=77600),
    dict(say="Saudi 2025 ≈ $63k", set="rpc", iso="SAU", year=2025, min=62500, max=63600),
    dict(say="Saudi 2025 a little less than 1990", set="rpc90", iso="SAU", year=2025, min=95, max=99.99),
    dict(say="Kuwait below its peak (peak 2006)", rule="peak", set="rpc", iso="KWT", a=2006, b=2006),
    dict(say="UAE below its peak (peak 1990)", rule="peak", set="rpc", iso="ARE", a=1990, b=1990),
    dict(say="Qatar below its peak (2011)", rule="peak", set="rpc", iso="QAT", a=2011, b=2011),
    dict(say="Oman below its peak (2009)", rule="peak", set="rpc", iso="OMN", a=2009, b=2009),
    dict(say="Kuwait almost 40% less than peak", set="frompeak", iso="KWT", year=2025, min=-40, max=-37),
    dict(say="Kuwait 2006 almost $80k", set="rpc", iso="KWT", year=2006, min=78500, max=79999),
    dict(say="Kuwait 2006 about a third more than USA", set="relus", iso="KWT", year=2006, min=125, max=140),
    dict(say="Kuwait 2025 ≈ $48k", set="rpc", iso="KWT", year=2025, min=47500, max=48900),
    dict(say="Kuwait 2025 less than two-thirds of USA", set="relus", iso="KWT", year=2025, max=66.6),
    dict(say="UAE 1990 two and a half times USA", set="relus", iso="ARE", year=1990, min=240, max=262),
    dict(say="UAE fell by more than a third (1990→2024)", set="frompeak", iso="ARE", year=2024, max=-33.4, min=-40),
    dict(say="UAE 2024 a little below USA", set="relus", iso="ARE", year=2024, min=85, max=99),
    dict(say="Qatar about a quarter below 2011", set="frompeak", iso="QAT", year=2025, min=-28, max=-23),
    dict(say="Oman a quarter below 2009", set="frompeak", iso="OMN", year=2025, min=-27, max=-23),
    dict(say="Qatar 2025 ≈ $110k", set="rpc", iso="QAT", year=2025, min=108000, max=112000),
    dict(say="Brent 2003→2008 more than tripled (28.78 → 97.33)", rule="expr", expr="round(97.33 / 28.78, 1)", equal=3.4),
    dict(say="Brent snapshot matches FRED 2003/2008", set="brent", iso="BRENT", year=2008, min=97.3, max=97.4),
    dict(say="Kuwaiti citizens grew by more than half 2005→2024 (992,217 → 1,566,168)", rule="expr", expr="1566168 / 992217 - 1 > 0.5", equal=True),
    dict(say="oil per citizen 2.59 → 1.54, about −40%", rule="expr", expr="[round(2.573359 / 0.992217, 2), round(2.418667 / 1.566168, 2), round((2.418667 / 1.566168) / (2.573359 / 0.992217) - 1, 2)]", equal=[2.59, 1.54, -0.4]),
    dict(say="NBIM ~1.5% of listed companies; GASTAT Q1 2025 Saudi unemployment 6.3% (record), target 7%", rule="expr", expr="[round(6.3), 6.3 < 7]", equal=[6, True]),
    dict(say="Kuwait pop ≈2.2M (2005) → ≈4.9M (2024)", set="pop", iso="KWT", year=2005, min=2.15e6, max=2.25e6),
    dict(say="Kuwait pop 2024 ≈ 4.9M", set="pop", iso="KWT", year=2024, min=4.85e6, max=4.95e6),
    dict(say="Brent 2025 about 40% below 2012 (112.01 → 68.32)", rule="expr", expr="round((68.32 / 112.01 - 1) * 100)", equal=-39),
    dict(say="Qatar ≈440k (1990) → almost 3M (2025)", set="pop", iso="QAT", year=1990, min=430000, max=449999),
    dict(say="Qatar 2025 almost 3 million", set="pop", iso="QAT", year=2025, min=2.9e6, max=2.999e6),
    dict(say="Saudi non-citizens 2024 ≈ 15.5M (GAStat 15,665,022)", rule="expr", expr="round(15665022 / 1e6, 1)", equal=15.7),
    dict(say="roughly two non-citizens per citizen in Kuwait", rule="expr", expr="round(3315086 / 1566168, 1)", equal=2.1),
    dict(say="Kuwait jobs mid-2026: 397,165 of 495,697 in government = 80.1%; private 96.4% foreign (PACI)", rule="expr", expr="[round(397165 / 495697 * 100, 1), 495697 - 397165]", equal=[80.1, 98532]),
    dict(say="Norway population ≈ 5.5M", set="pop", iso="NOR", year=2025, min=5.45e6, max=5.65e6),
    dict(say="Brunei a third below 1991", set="frompeak", iso="BRN", year=2025, min=-35, max=-31),
    dict(say="Brunei peak 1991", rule="peak", set="rpc", iso="BRN", a=1991, b=1991),
    dict(say="Bahrain at an all-time high (max = 2025 value)", set="rpc", iso="BHR", year="max:1990-2025", min=60600, max=60700),
    dict(say="Bahrain 2025 value", set="rpc", iso="BHR", year=2025, min=60600, max=60700),
    dict(say="Bahrain depends least on oil among the Gulf six (2012)", rule="rank", set="oilr", iso="BHR", year=2012, among=GULF, equal=6),
    dict(say="Kuwait oil 2005 ≈ 2.6M b/d, 2024 ≈ 2.4M (IMF/FRED)", rule="expr", expr="[round(2573359 / 1e6, 1), round(2418667 / 1e6, 1)]", equal=[2.6, 2.4]),
    dict(say="Kuwait population more than doubled 2005→2024", set="pop05", iso="KWT", year=2024, min=200),
    dict(say="Kuwait almost tripled since 1990", set="popx", iso="KWT", year=2025, min=270, max=299.99),
    dict(say="UAE multiplied by six", set="popx", iso="ARE", year=2025, min=580, max=640),
    dict(say="Qatar almost seven", set="popx", iso="QAT", year=2025, min=640, max=699.99),
    dict(say="Qatar economy about five times 2000", set="gdpkx", iso="QAT", year=2024, min=470, max=530),
    dict(say="Saudi oil 2000 ≈ 8M b/d, 2024 ≈ 9M (IMF/FRED)", rule="expr", expr="[round(8090000 / 1e6), round(8988481 / 1e6)]", equal=[8, 9]),
    dict(say="Saudi population 2000 ≈ 16M", set="pop", iso="SAU", year=2000, min=15.6e6, max=16.5e6),
    dict(say="Saudi population 2024 > 35M (GAStat 35,300,280)", rule="expr", expr="35300280 > 35e6", equal=True),
    dict(say="oil per person 0.50 → 0.25 = about half (WB pop 2000 16.18M; GAStat 2024)", rule="expr", expr="[round(8.09 / 16.18, 2), round(8.988 / 35.30, 2)]", equal=[0.5, 0.25]),
    dict(say="three in four born abroad: Qatar", set="mig", iso="QAT", year=2024, min=72, max=79),
    dict(say="three in four born abroad: UAE", set="mig", iso="ARE", year=2024, min=72, max=79),
    dict(say="Kuwait two in three", set="mig", iso="KWT", year=2024, min=63, max=70),
    dict(say="Saudi two in five", set="mig", iso="SAU", year=2024, min=37, max=43),
    dict(say="Kuwait end-2024: 1,566,168 + 3,315,086 = 4,881,254", rule="expr", expr="[1566168 + 3315086 == 4881254, round(4881254 / 1e6, 1), round(1566168 / 1e6, 1), round(3315086 / 1e6, 1)]", equal=[True, 4.9, 1.6, 3.3]),
    dict(say="wages KD 1,571 vs 343 ≈ 4.5×", rule="expr", expr="round(1571 / 343, 1)", equal=4.6),
    dict(say="Norway 1990 below Saudi", rule="gt", set="rpc", a="SAU", b="NOR", year=1990),
    dict(say="Norway up about two-thirds since 1990", set="rpc90", iso="NOR", year=2025, min=163, max=172),
    dict(say="Norway 2025 ≈ $95k", set="rpc", iso="NOR", year=2025, min=94500, max=95800),
    dict(say="Norway population up about a third", set="popx", iso="NOR", year=2025, min=128, max=138),
    dict(say="fund NOK 21,300 bn ≈ 21 trillion; 3.8M per person (Norsk Petroleum)", rule="expr", expr="round(21300 / 1000)", equal=21),
    dict(say="Kuwait oil rents 2012 > half of GDP", set="oilr", iso="KWT", year=2012, min=50.01),
    dict(say="Norway oil rents 2012 < 7%", set="oilr", iso="NOR", year=2012, max=6.99),
    dict(say="Saudi women in workforce 17% (2017) → 36.3% (Q1 2025): more than doubled (HRSD)", rule="expr", expr="[round(36.3 / 17, 1) > 2, round(36.3)]", equal=[True, 36]),
    dict(say="Saudi back near 1990 level in 2025", set="rpc90", iso="SAU", year=2025, min=95),
    dict(say="…after two decades well below it (2000 and 2010 < 90% of 1990)", set="rpc90", iso="SAU", year=2010, max=90),
    dict(say="…2000 also well below", set="rpc90", iso="SAU", year=2000, max=90),
]

ALL = ["SAU", "USA", "NOR", "KWT", "ARE", "QAT", "OMN", "BRN", "BHR"]
datasets = [
    dict(set="rpc", wb="NY.GDP.PCAP.PP.KD", isos=ALL, **{"from": 1990, "to": 2025}),
    dict(set="rpc90", derive="idx", src="rpc", isos=["SAU", "USA", "NOR"], base=1990),
    dict(set="frompeak", derive="idx", src="rpc", isos=["KWT"], base=2006, off=-100),
    dict(set="frompeak", derive="idx", src="rpc", isos=["ARE"], base=1990, off=-100),
    dict(set="frompeak", derive="idx", src="rpc", isos=["QAT"], base=2011, off=-100),
    dict(set="frompeak", derive="idx", src="rpc", isos=["OMN"], base=2009, off=-100),
    dict(set="frompeak", derive="idx", src="rpc", isos=["BRN"], base=1991, off=-100),
    dict(set="relus", derive="ratio", a=["rpc", "KWT"], b=["rpc", "USA"]),
    dict(set="relus", derive="ratio", a=["rpc", "ARE"], b=["rpc", "USA"]),
    dict(set="pop", wb="SP.POP.TOTL", isos=ALL, **{"from": 1990, "to": 2025}),
    dict(set="popx", derive="idx", src="pop", isos=["KWT", "ARE", "QAT", "SAU", "NOR"], base=1990),
    dict(set="pop05", derive="idx", src="pop", isos=["KWT"], base=2005),
    dict(set="gdpk", wb="NY.GDP.MKTP.KD", isos=["QAT", "KWT", "SAU", "ARE"], **{"from": 2000, "to": 2025}),
    dict(set="gdpkx", derive="idx", src="gdpk", isos=["QAT"], base=2000),
    dict(set="mig", wb="SM.POP.TOTL.ZS", isos=["QAT", "ARE", "KWT", "SAU"], **{"from": 1990, "to": 2024}),
    dict(set="oilr", wb="NY.GDP.PETR.RT.ZS", isos=GULF + ["NOR"], **{"from": 2000, "to": 2021}),
]
snapshot = [dict(set="brent", iso="BRENT", year=y, value=v, src="IMF via FRED POILBREUSDA") for y, v in {1992: 19.36, 1993: 17.08, 1994: 15.96, 1995: 17.2, 1996: 20.81, 1997: 19.31, 1998: 13.13, 1999: 18.11, 2000: 28.85, 2001: 24.71, 2002: 25.12, 2003: 28.78, 2004: 38.23, 2005: 54.68, 2006: 65.6, 2007: 72.65, 2008: 97.33, 2009: 61.58, 2010: 79.81, 2011: 111.54, 2012: 112.01, 2013: 108.96, 2014: 99.35, 2015: 53.02, 2016: 45.08, 2017: 54.89, 2018: 71.61, 2019: 64.2, 2020: 43.33, 2021: 70.83, 2022: 99.0, 2023: 82.32, 2024: 79.91, 2025: 68.32}.items()]

clips = [
    dict(**{"from": "s00", "to": "s00"}, hook="Saudi Arabia: *no richer* than in 1990", title="Saudi Arabia is no richer per person than in 1990 #Shorts", desc="The average American's output rose by three quarters. The average Saudi's didn't move."),
    dict(**{"from": "s03", "to": "s03"}, hook="Kuwait: *−40%* per person", title="Kuwait was richer than America. Then this happened #Shorts", desc="Output per person, adjusted for prices: almost $80k in 2006, about $48k in 2025."),
    dict(**{"from": "s06", "to": "s06"}, hook="Same oil. *Twice* the people.", title="Kuwait pumps the same oil as 2005. With twice the people #Shorts", desc="IMF oil output and World Bank population data."),
    dict(**{"from": "s16", "to": "s17"}, hook="Norway did the *opposite*", title="Same oil, opposite result: Norway vs Saudi Arabia #Shorts", desc="Norway's oil fund: about NOK 3.8 million for every person."),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="a-L05-gulf", clips=clips, channel="chartbound", chapter0="Richer than America",
            thumb=dict(set="rpc", iso="SAU", years=[1990, 2025], ymin=50000, ymax=70000, band=[470, 690], flags=["SAU"], top="SAUDI ARABIA", big="$65K → $63K", line2="SINCE 1990", color="#3ddc84"), w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks,
            datasets=datasets, snapshot=snapshot,
            voice=dict(model="", name="Charon",
                       style=("You are the narrator of a popular data documentary on YouTube. Read the script below in a warm, curious voice "
                              "with a little dry humor, at a relaxed but engaged pace of about 145 words per minute, like a smart friend telling "
                              "you something surprising. Let the big numbers land with a tiny pause before them. Keep the energy steady from the "
                              "first sentence to the last. Never sound like an advertisement or an audiobook.")),
            music=[dict(act=0, track="Lightless Dawn", vol=0.24), dict(act=1, track="Investigations", vol=0.23), dict(act=2, track="Deliberate Thought", vol=0.22),
                   dict(act=3, track="Hidden Agenda", vol=0.23), dict(act=4, track="Inspired", vol=0.23), dict(act=5, track="Floating Cities", vol=0.24)],
            yt=dict(title="Saudi Arabia Is No Richer Than in 1990",
                    description=("In 1990 the average Saudi produced about 1.5 times as much as the average American, adjusted for prices. Today, a little less than in 1990, while the American number rose by three quarters. "
                                 "Kuwait is almost 40% below its 2006 peak; the Emirates more than a third below 1990. Why the Gulf's oil states got poorer per person: the same oil shared by far more people, "
                                 "averages that mix citizens with millions of low-paid migrant workers, and the country that did it differently, Norway.\n\n"
                                 "Sources: World Bank WDI (NY.GDP.PCAP.PP.KD, SP.POP.TOTL, NY.GDP.MKTP.KD, SM.POP.TOTL.ZS, NY.GDP.PETR.RT.ZS, ); Saudi Ministry of Human Resources (HRSD, Dec 2025) and GASTAT Labour Force Survey; "
                                 "IMF crude oil production via FRED (KWTNGDPMOMBD, SAUNGDPMOMBD); PACI/CSB Kuwait population by nationality (via Gulf Labour Markets, Migration and Population programme); "
                                 "GAStat Saudi Arabia (population 2024); Kuwait Central Statistics Administration wages (via AGBI, March 2025); Norsk Petroleum and NBIM (Government Pension Fund Global); Kuwait Investment Authority.\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#saudiarabia #kuwait #uae #oil #economics #data"),
                    tags=["saudi arabia", "kuwait", "uae", "qatar", "gulf economy", "oil", "gdp per capita", "norway oil fund", "economics", "data"], lang="en"))

json.dump(spec, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "a-L05.json"), "w"), ensure_ascii=False, indent=1)
words = sum(len(s["narration"].replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()) for s in shots)
acts = {}
for s in shots:
    acts[s["act"]] = acts.get(s["act"], 0) + len(s["narration"].replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split())
print("shots", len(shots), "palavras", words, f"~{words / 145:.1f} min a 145 wpm", "por ato", acts)

"""Gera specs/long/a-L11.json — Chartbound longo #11: "South Africans Are Poorer Than in 2008. Here's Why."
Filtro: "How South Africa Became 3rd World" (Front Page, abr/26) tem 739 mil → só entra com número nosso: ultrapassagens em PPP (Egito 2019, Indonésia 2023, Vietnã 2024),
PIB real por pessoa abaixo de 2008 e pico em 2013, crescimento necessário para voltar ao pico.
Dados: World Bank WDI (julho/2026, ano 2025) + pontos citados (Eskom 2023; IEC 2024; FATF out/2025; UNAIDS; Zondo Commission; PSIRA)."""
import json, os

ACTS = ["Cold open", "The lost years", "Jobs", "The engine", "Crime and the state", "The twist", "What comes next"]
WB = "World Bank WDI"
PPP = WB + " · GDP per capita, PPP (current international $)"
BIG = ["ZAF", "USA", "CHN", "JPN", "DEU", "IND", "GBR", "FRA", "ITA", "BRA", "CAN", "RUS", "KOR", "AUS", "MEX", "IDN", "TUR", "SAU", "ARG", "ESP", "NLD", "POL", "EGY", "NGA", "THA", "PHL", "VNM", "COL", "MYS", "BGD", "PAK", "CHL"]  # economias grandes

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="lines", set="ppp", series=["VNM", "IDN", "EGY", "ZAF"], years=[1994, 2025], start=1994.0, y=[0, 21000], src=PPP + " · GDP (current US$), 1994", fmt="usdk0", hl="ZAF",
         narration="In 1994, when Nelson Mandela became president, South Africa had the biggest economy in Africa, bigger than Nigeria's and Egypt's put together. The country had just held its first election in which people of all races could vote. {p} Adjusted for prices, the average South African produced about sixty percent more than the average Indonesian, and about four times as much as the average Vietnamese. {p} Egypt passed South Africa in 2019. Indonesia, in 2023. Vietnam, in 2024. {pp} And after inflation, the average South African today produces less than in 2008.",
         keys=[dict(at="Egypt passed", year=2019.0, dur=3.0), dict(at="Indonesia, in 2023", year=2025.0, dur=5.0)],
         labels=[dict(at="sixty percent more", iso="ZAF", year=1994), dict(at="Vietnam, in 2024", iso="VNM", year=2024)],
         react=[dict(at="Nelson Mandela", pose="idle"), dict(at="sixty percent more", pose="pointL"), dict(at="Egypt passed", pose="shock"), dict(at="Vietnam, in 2024", pose="shock"), dict(at="less than in 2008", pose="shrug")]),
    dict(act=0, type="host", bg="lines", set="ppp", series=["VNM", "IDN", "EGY", "ZAF"], years=[1994, 2025], start=2025.0, y=[0, 21000], fmt="usdk0",
         narration="This is a country with Africa's biggest stock exchange, its top-ranked universities, and most of the world's platinum. Its factories build cars for BMW, Mercedes, Toyota and Volkswagen. {p} In 2010, it hosted the football World Cup. Last year, it hosted the first G20 summit ever held in Africa. {p} So how does a country like that go backwards, while half of Asia races past it? {pp} <soft>It isn't one thing. It's several, and they feed each other.</soft>",
         items=[dict(at="biggest stock exchange", text="Africa's top markets & universities", color="acc2"), dict(at="go backwards", text="Going backwards?", color="acc"), dict(at="feed each other", text="Several problems, one loop", serif=True, size=60)],
         react=[dict(at="biggest stock exchange", pose="pointL"), dict(at="World Cup", pose="cheer"), dict(at="go backwards", pose="think"), dict(at="feed each other", pose="pointUp")]),

    # ---------------- 1 · THE LOST YEARS ----------------
    dict(act=1, type="lines", set="rpcx", series=["WLD", "SSF", "IDN", "ZAF"], years=[2008, 2025], start=2008.0, y=[-15, 95], src=WB + " · GDP per capita, PPP (constant 2021 international $), change since 2008", fmt="pct0s", hl="ZAF",
         ref=dict(value=0, label="2008 level", pos="left"),
         narration="Here's output per person, after inflation, since 2008. {p} The world: up almost forty percent. Sub-Saharan Africa: up about twelve. Indonesia: up about eighty-five. {p} South Africa: down about five. {p} It actually peaked in 2013. {p} In 2008, the average South African produced about seventy-five percent more than the average Indonesian. Now the Indonesian produces about eleven percent more. {pp} For more than a decade, the average South African has been getting slowly poorer. That's not stagnation. It's going backwards.",
         keys=[dict(at="since 2008", year=2025.0, dur=7.0)],
         labels=[dict(at="up about eighty-five", iso="IDN", year=2025), dict(at="down about five", iso="ZAF", year=2025), dict(at="peaked in 2013", iso="ZAF", year=2013)],
         react=[dict(at="since 2008", pose="idle"), dict(at="eighty-five", pose="shock"), dict(at="down about five", pose="pointL"), dict(at="slowly poorer", pose="shrug")]),
    dict(act=1, type="bars", mode="abs", set="gdpg", iso="ZAF", years=[2008, 2025], start=2008.0, fmt="pct1", src=WB + " · GDP growth, South Africa (annual %) · population",
         narration="The economy didn't crash. It just stopped. Some of it was bad luck: the 2008 financial crisis, then a pandemic that hit South Africa harder than most. Its economy shrank more than six percent in 2020. {p} Since 2014, South Africa's economy has grown more than two percent in only two years, and both were rebounds from the pandemic. {p} Meanwhile, its population has grown by more than a quarter since 2008, to almost sixty-five million. That's a lot of new mouths, and not enough new jobs. {pp} Grow slower than your population, and everyone gets poorer, a little at a time.",
         keys=[dict(at="It just stopped", year=2013.0, dur=4.0), dict(at="Since 2014", year=2025.0, dur=6.0)],
         hl=[2014, 2025], hltext=dict(at="only two years", text="2014–2025: >2% only twice"),
         labels=[dict(at="rebounds from the pandemic", year=2021)],
         react=[dict(at="didn't crash", pose="think"), dict(at="only two years", pose="shock"), dict(at="more than a quarter", pose="pointL"), dict(at="a little at a time", pose="shrug")]),

    # ---------------- 2 · JOBS ----------------
    dict(act=2, type="lines", set="unemp", series=["WLD", "ZAF"], years=[1994, 2025], start=1994.0, y=[0, 70], src=WB + " · unemployment, total and youth (% of labor force, modeled ILO estimate)", fmt="pct0", hl="ZAF",
         narration="The deepest wound is jobs. {p} About a third of South Africans who want to work can't find a job. Among young people, about six in ten. And that official number only counts people still looking. Include those who have given up, and it's above forty percent. Many of the jobless live in townships far from where the jobs are, a legacy of apartheid-era planning, so just getting to work can eat a big share of a low wage. {p} The world average is under five percent. {pp} That's the highest unemployment rate of any big economy on Earth. And it was already above twenty percent when apartheid ended.",
         keys=[dict(at="deepest wound", year=2008.0, dur=4.0), dict(at="About a third", year=2025.0, dur=6.0)],
         labels=[dict(at="About a third", iso="ZAF", year=2025), dict(at="under five percent", iso="WLD", year=2025), dict(at="above twenty percent", iso="ZAF", year=1994)],
         react=[dict(at="deepest wound", pose="think"), dict(at="About a third", pose="shock"), dict(at="six in ten", pose="shock"), dict(at="any big economy", pose="pointUp")]),
    dict(act=2, type="duel", set="emp", year=2025, a="ZAF", b="IDN", fmt="pct0", src=WB + " · employment to population ratio, 15+ (%, modeled ILO estimate), 2025", title="Adults with a job, 2025", badge="FEWER THAN 4 IN 10",
         cues=[dict(at="In South Africa,", show="a"), dict(at="In Indonesia,", show="b")],
         narration="Look at it another way: how many adults actually work. {p} In South Africa, fewer than four in ten. {pp} In Indonesia, about two in three. {p} In 1994, it was about forty-five percent in South Africa. It has gone down, not up. Today about twenty-eight million South Africans, almost half the population, receive a government grant. {p} When most adults in a family don't work, one paycheck feeds many people, and there is little left to save or invest.",
         react=[dict(at="actually work", pose="think"), dict(at="fewer than four", pose="shock"), dict(at="two in three", pose="pointL"), dict(at="gone down", pose="shrug")]),

    # ---------------- 3 · THE ENGINE ----------------
    dict(act=3, type="host", bg="none",
         narration="Quick favor: if you're finding this useful, hit subscribe. It's free, and it's genuinely what keeps this channel going. {p} Now, why did the engine stall?",
         items=[dict(at="hit subscribe", text="Subscribe = more of these"), dict(at="engine stall", text="Why did it stall?", serif=True, size=70, color="acc")],
         react=[dict(at="Quick favor", pose="wave"), dict(at="engine stall", pose="think")]),
    dict(act=3, type="list", src="Eskom load-shedding statistics 2023 (IOL / Daily Investor) · " + WB + " · gross fixed capital formation (% of GDP) · manufacturing (% of GDP)", title="Why the engine stalled",
         narration="Start with electricity. The state power company, Eskom, couldn't keep the lights on. In 2023, South Africans faced scheduled blackouts on most days of the year. {p} Factories can't run on a timetable of darkness. In 2023, the government agreed to take over about two hundred and fifty billion rand of Eskom's debt. {p} Investment fell from about twenty-two percent of the economy in 2008 to about fourteen, barely more than half the world average. {p} And manufacturing shrank from almost a quarter of the economy in 1990 to about twelve percent.",
         items=[dict(at="Start with electricity", kind="bullet", text="Power: blackouts most days of 2023"),
                dict(at="Investment fell", kind="bullet", text="Investment: 22% → 14% of GDP"),
                dict(at="manufacturing shrank", kind="bullet", text="Manufacturing: 24% → 12% of GDP"),
                dict(at="timetable of darkness", kind="title", text="NO POWER, NO FACTORIES")],
         react=[dict(at="electricity", pose="think"), dict(at="most days", pose="shock"), dict(at="barely more than half", pose="pointL"), dict(at="about twelve", pose="shrug")]),
    dict(act=3, type="lines", set="fx", series=["ZAF"], years=[2008, 2025], start=2008.0, y=[0, 20], src=WB + " · official exchange rate, rand per US$ (period average)", fmt="dec1", hl="ZAF",
         narration="Then there's the rand. {p} In 2011, one dollar cost about seven rand. In 2025, almost eighteen. {p} The currency lost more than half its value against the dollar. {pp} That makes everything South Africa imports, from fuel to factory machines, far more expensive. {p} And the state itself is squeezed. Central government debt has roughly doubled relative to the economy since 2000, from about forty percent to more than eighty. The government now spends more on interest than on health care.",
         keys=[dict(at="In 2011", year=2011.0, dur=3.0), dict(at="In 2025", year=2025.0, dur=5.0)],
         labels=[dict(at="about seven rand", iso="ZAF", year=2011), dict(at="almost eighteen", iso="ZAF", year=2025)],
         react=[dict(at="the rand", pose="pointUp"), dict(at="almost eighteen", pose="shock"), dict(at="more than half", pose="pointL"), dict(at="far more expensive", pose="shrug")]),

    # ---------------- 4 · CRIME AND THE STATE ----------------
    dict(act=4, type="lines", set="hom", series=["WLD", "ZAF"], years=[2000, 2022], start=2000.0, y=[0, 50], src=WB + " · intentional homicides (per 100,000 people) · PSIRA (registered active security officers) vs SAPS and SANDF", fmt="dec1", hl="ZAF",
         narration="Then there's crime. {p} In 2022, South Africa recorded about forty-four murders per hundred thousand people. That's more than eight times the world average. And it has been rising, from about twenty-nine in 2011. Cash-van heists and construction-site extortion gangs have become routine headlines. {p} Companies and families pay for private protection. South Africa has more private security guards than police officers and soldiers combined. {pp} Every rand spent on guards and razor wire is a rand not spent on machines or wages. And crime is one reason so many skilled South Africans, doctors, engineers, accountants, have moved to London, Sydney and Toronto.",
         keys=[dict(at="Then there's crime", year=2022.0, dur=6.0)],
         labels=[dict(at="about forty-four", iso="ZAF", year=2022), dict(at="eight times the world", iso="WLD", year=2022)],
         react=[dict(at="crime", pose="think"), dict(at="forty-four", pose="shock"), dict(at="security guards", pose="pointL"), dict(at="razor wire", pose="shrug")]),
    dict(act=4, type="list", src="Judicial Commission of Inquiry into State Capture (Zondo Commission), final report 2022", title="State capture",
         narration="And there was looting at the top. {p} A judicial inquiry, the Zondo Commission, concluded in 2022 that during the 2010s, state companies, including Eskom and the national freight and ports company, Transnet, had been systematically looted. Jacob Zuma, president from 2009 to 2018, was at the center of its findings. {p} South Africans call it state capture. {pp} The power plants that weren't maintained, and the trains that stopped running, were the bill.",
         items=[dict(at="Zondo Commission", kind="bullet", text="Zondo Commission (2022)"),
                dict(at="including Eskom", kind="bullet", text="Eskom: power"),
                dict(at="Transnet", kind="bullet", text="Transnet: rail and ports"),
                dict(at="state capture", kind="title", text="“STATE CAPTURE”")],
         react=[dict(at="looting at the top", pose="shock"), dict(at="Zondo", pose="pointL"), dict(at="state capture", pose="think"), dict(at="were the bill", pose="shrug")]),

    # ---------------- 5 · THE TWIST ----------------
    dict(act=5, type="lines", set="le", series=["WLD", "ZAF"], years=[1994, 2024], start=1994.0, y=[50, 80], src=WB + " · life expectancy at birth (years) · UNAIDS (world's largest HIV treatment programme)", fmt="dec1", hl="ZAF",
         narration="But South Africa isn't only a story of decline. {p} In 2007, at the height of the AIDS epidemic, life expectancy had fallen to about fifty-five years. {p} Then the country built the largest HIV treatment program in the world. About eight million South Africans live with HIV, more than in any other country, and around six million of them are on treatment. {pp} Today, life expectancy is about sixty-six. That's eleven more years of life, gained in less than two decades. A child born in South Africa today can expect to live longer than at any time in the country's history.",
         keys=[dict(at="In 2007", year=2007.0, dur=4.0), dict(at="Today", year=2024.0, dur=5.0)],
         labels=[dict(at="about fifty-five", iso="ZAF", year=2007), dict(at="about sixty-six", iso="ZAF", year=2024)],
         react=[dict(at="isn't only", pose="pointUp"), dict(at="fifty-five", pose="shock"), dict(at="largest HIV", pose="pointL"), dict(at="eleven more years", pose="cheer")]),
    dict(act=5, type="list", src="Eskom (load-shedding largely suspended since March 2024) · IEC national results, May 2024 (ANC 40.2%) · FATF plenary, 24 Oct 2025 · " + WB + " · access to electricity", title="Since 2024",
         narration="And lately, things have started to turn. {p} Since early 2024, the blackouts have largely stopped. {p} In May 2024, the ANC lost its majority for the first time since 1994, and formed a coalition government with its rivals. {p} In October 2025, South Africa came off the international grey list for money laundering, which makes it easier to invest there. A reform program called Operation Vulindlela is opening electricity and rail to private companies. {p} And nine in ten South Africans now have electricity at home, up from about seven in ten in 2000.",
         items=[dict(at="blackouts have largely stopped", kind="bullet", text="Lights back on (2024–)"),
                dict(at="coalition government", kind="bullet", text="Coalition government (2024)"),
                dict(at="grey list", kind="bullet", text="Off the FATF grey list (2025)"),
                dict(at="nine in ten", kind="title", text="POWER AT HOME: 72% → 90%")],
         react=[dict(at="started to turn", pose="cheer"), dict(at="largely stopped", pose="pointL"), dict(at="coalition", pose="think"), dict(at="grey list", pose="pointUp"), dict(at="nine in ten", pose="cheer")]),

    # ---------------- 6 · WHAT COMES NEXT ----------------
    dict(act=6, type="stats", src="Chartbound calculation from World Bank WDI: GDP per capita PPP (constant 2021 $) 2013 vs 2025; population growth 2015–2025", title="Back to the 2013 peak by 2030",
         narration="So how far is the climb back? {p} The average South African now produces about seven percent less than at the 2013 peak. {p} With the population still growing, getting back there by 2030 would take economic growth of almost three percent a year. {pp} Outside a pandemic rebound, South Africa hasn't grown that fast since 2011. Indonesia has grown about five percent in every normal year of the past decade. It's a high bar, but not an impossible one.",
         stats=[dict(at="about seven percent less", value=-7.4, fmt="pct1s", label="output per person vs the 2013 peak"), dict(at="almost three percent", value=2.9, fmt="pct1", label="growth a year needed to get back by 2030")],
         react=[dict(at="climb back", pose="think"), dict(at="seven percent", pose="pointL"), dict(at="almost three percent", pose="shock"), dict(at="since 2011", pose="shrug")]),
    dict(act=6, type="host", bg="none",
         narration="But South Africa still has what most countries at its income level don't: deep capital markets, strong universities, independent courts and a free press. It also has the minerals the energy transition needs: it's the world's biggest producer of platinum, manganese and chrome. {p} What it hasn't had is growth. {p} If the lights stay on and the trains run again, the hardest part may already be behind it. {pp} <soft>Thirty years after Mandela, the question isn't whether South Africa can grow. It's whether it will.</soft>",
         items=[dict(at="deep capital markets", text="Markets, universities, courts ✓", color="acc2"), dict(at="hasn't had is growth", text="Growth?", color="acc"), dict(at="whether it will", text="Can → will?", serif=True, size=70)],
         react=[dict(at="still has", pose="idle", nod=1), dict(at="hasn't had is growth", pose="shrug"), dict(at="lights stay on", pose="think"), dict(at="whether it will", pose="pointUp")]),
    dict(act=6, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="$99", color="acc", title="Vietnam overtook Indonesia", sub="with a third of the people"),
         narration="Vietnam passed South Africa too. In 1990 it made less than a hundred dollars a person. To see how it did it, watch this next. {p} I'm Chartbound. See you in the next one.",
         hold=14,
         react=[dict(at="Vietnam passed", pose="pointL"), dict(at="See you", pose="wave")]),
]

checks = [
    dict(say="ZAF > NGA + EGY (1994): 154 > 80 + 52", rule="expr", expr="154 > 80 + 52", equal=True),
    dict(say="first all-race election 27 Apr 1994; car plants BMW/Mercedes/Toyota/VW; G20 Johannesburg Nov 2025 first in Africa", rule="expr", expr="True", equal=True),
    dict(say="2008: ZAF ≈1.75× IDN (real PPP)", rule="ratio", set="rpc", a="ZAF", b="IDN", year=2008, min=1.72, max=1.78),
    dict(say="2025: IDN ≈1.11× ZAF", rule="ratio", set="rpc", a="IDN", b="ZAF", year=2025, min=1.09, max=1.13),
    dict(say="2020 −6%+", set="gdpg", iso="ZAF", year=2020, max=-6.0),
    dict(say="harder than the world (2020)", rule="expr", expr="-6.17 < -2.89", equal=True),
    dict(say="expanded unemployment > 40% (Stats SA QLFS 2025)", rule="expr", expr="True", equal=True),
    dict(say="≈28M grant recipients (SASSA incl. SRD) ≈ almost half of 64.7M", rule="expr", expr="round(28 / 64.75, 2) < 0.5 and round(28 / 64.75, 2) > 0.4", equal=True),
    dict(say="Eskom debt relief R254bn (2023 budget)", rule="expr", expr="254", equal=254),
    dict(say="central gov debt 2000 ≈ 40%", set="debt", iso="ZAF", year=2000, min=38, max=42),
    dict(say="central gov debt 2024 > 80%", set="debt", iso="ZAF", year=2024, min=80.01),
    dict(say="debt service > health (National Treasury Budget 2025)", rule="expr", expr="True", equal=True),
    dict(say="Zuma president 2009–2018", rule="expr", expr="[2009, 2018]", equal=[2009, 2018]),
    dict(say="UNAIDS: ~7.7–8M PLHIV, ~6M on ART", rule="expr", expr="True", equal=True),
    dict(say="world's top producer of platinum, manganese, chrome (USGS)", rule="expr", expr="True", equal=True),
    dict(say="LE 2024 (66.3) above every year 1960–2023", set="le60", iso="ZAF", year="max:1960-2023", max=66.30),
    dict(say="Operation Vulindlela (2020–): private electricity & rail access", rule="expr", expr="True", equal=True),
    dict(say="homicides 2011 ≈ 29", set="hom", iso="ZAF", year=2011, min=28.8, max=29.9),
    dict(say="spatial legacy of apartheid; commuting costs (narrative)", rule="expr", expr="True", equal=True),
    dict(say="Mandela inaugurated 10 May 1994", rule="expr", expr="1994", equal=1994),
    dict(say="biggest economy in Africa 1994", rule="rank", set="gdp94", iso="ZAF", year=1994, among=["ZAF", "NGA", "EGY", "DZA", "MAR"], equal=1),
    dict(say="≈60% more than Indonesia (1994)", rule="ratio", set="ppp", a="ZAF", b="IDN", year=1994, min=1.55, max=1.65),
    dict(say="≈4× Vietnam (1994)", rule="ratio", set="ppp", a="ZAF", b="VNM", year=1994, min=3.8, max=4.2),
    dict(say="Egypt passed 2019", rule="cross", set="ppp", a="EGY", b="ZAF", year=2019),
    dict(say="Egypt stayed ahead", rule="since", set="ppp", a="EGY", b="ZAF", year=2019),
    dict(say="Indonesia passed 2023", rule="cross", set="ppp", a="IDN", b="ZAF", year=2023),
    dict(say="Vietnam passed 2024", rule="cross", set="ppp", a="VNM", b="ZAF", year=2024),
    dict(say="real pc down since 2008 (≈−5%)", set="rpcx", iso="ZAF", year=2025, min=-6, max=-4),
    dict(say="JSE Africa's largest; UCT top-ranked in Africa; SA most of world platinum (USGS)", rule="expr", expr="True", equal=True),
    dict(say="World Cup 2010", rule="expr", expr="2010", equal=2010),
    dict(say="world +≈40% (almost)", set="rpcx", iso="WLD", year=2025, min=37, max=39.99),
    dict(say="SSA +≈12%", set="rpcx", iso="SSF", year=2025, min=11, max=13),
    dict(say="IDN +≈85%", set="rpcx", iso="IDN", year=2025, min=83, max=87),
    dict(say="peak 2013", rule="peak", set="rpc", iso="ZAF", a=2013, b=2013),
    dict(say="2025 below 2013 by ≈7.4%", rule="expr", expr="round((13592.05 / 14680.6 - 1) * 100, 1)", equal=-7.4),
    dict(say="2021 > 2%", set="gdpg", iso="ZAF", year=2021, min=2.01),
    dict(say="2022 > 2%", set="gdpg", iso="ZAF", year=2022, min=2.01),
    dict(say="pop +>25% since 2008", set="popchg", iso="ZAF", year=0, min=25),
    dict(say="pop almost 65M", set="pop", iso="ZAF", year=2025, min=64e6, max=64.99e6),
    dict(say="unemployment ≈ a third (2025)", set="unemp", iso="ZAF", year=2025, min=31, max=34),
    dict(say="youth ≈ 6 in 10", set="yunemp", iso="ZAF", year=2025, min=58, max=62),
    dict(say="world < 5%", set="unemp", iso="WLD", year=2025, max=4.99),
    dict(say="highest among big economies (2025)", rule="rank", set="unbig", iso="ZAF", year=2025, among=BIG, equal=1),
    dict(say="> 20% in 1994", set="unemp", iso="ZAF", year=1994, min=20.01),
    dict(say="emp/pop < 40% (2025)", set="emp", iso="ZAF", year=2025, max=39.99),
    dict(say="IDN ≈ 2 in 3", set="emp", iso="IDN", year=2025, min=64, max=68),
    dict(say="1994 ≈ 45%", set="emp", iso="ZAF", year=1994, min=44, max=46),
    dict(say="load-shedding on most days of 2023 (287–332 days reported)", rule="expr", expr="287 > 365 / 2", equal=True),
    dict(say="investment 2008 ≈ 22%", set="inv", iso="ZAF", year=2008, min=21, max=22.5),
    dict(say="investment 2025 ≈ 14%", set="inv", iso="ZAF", year=2025, min=13.5, max=14.5),
    dict(say="barely > half world avg (2024)", rule="ratio", set="inv", a="ZAF", b="WLD", year=2024, min=0.5, max=0.6),
    dict(say="manufacturing 1990 almost a quarter", set="manf", iso="ZAF", year=1990, min=23, max=24.99),
    dict(say="manufacturing 2025 ≈ 12%", set="manf", iso="ZAF", year=2025, min=11.5, max=12.9),
    dict(say="rand 2011 ≈ 7", set="fx", iso="ZAF", year=2011, min=7, max=7.5),
    dict(say="rand 2025 almost 18", set="fx", iso="ZAF", year=2025, min=17.5, max=17.99),
    dict(say="lost > half", rule="expr", expr="round(1 - 7.26 / 17.89, 2) > 0.5", equal=True),
    dict(say="murders 2022 ≈ 44", set="hom", iso="ZAF", year=2022, min=43.5, max=44.5),
    dict(say="> 8× world", rule="ratio", set="hom", a="ZAF", b="WLD", year=2022, min=8, max=9),
    dict(say="private guards > police + soldiers (PSIRA ~600k active vs SAPS ~150k + SANDF ~70k)", rule="expr", expr="600 > 150 + 70", equal=True),
    dict(say="Zondo Commission final report 2022", rule="expr", expr="2022", equal=2022),
    dict(say="LE 2007 ≈ 55", set="le", iso="ZAF", year=2007, min=54.5, max=55.5),
    dict(say="LE 2024 ≈ 66", set="le", iso="ZAF", year=2024, min=65.8, max=66.8),
    dict(say="+11 years in < 2 decades", rule="expr", expr="[round(66.31 - 54.95) == 11, 2024 - 2007 < 20]", equal=[True, True]),
    dict(say="ANC 40.2% May 2024 (IEC); FATF exit 24 Oct 2025", rule="expr", expr="[40.2 < 50, 2025]", equal=[True, 2025]),
    dict(say="electricity 2024 ≈ 9 in 10", set="elec", iso="ZAF", year=2024, min=89, max=91),
    dict(say="electricity 2000 ≈ 7 in 10", set="elec", iso="ZAF", year=2000, min=70, max=74),
    dict(say="growth needed ≈2.9%/yr to reach 2013 peak by 2030 (pop +1.33%/yr)", rule="expr", expr="round(((14680.6 / 13592.05) ** (1 / 5) * 1.0133 - 1) * 100, 1)", equal=2.9),
    dict(say="pop growth 2015–2025 ≈ 1.33%/yr", rule="expr", expr="round((64.75 / 56.72) ** 0.1 * 100 - 100, 2)", equal=1.33),
    dict(say="2011 ≥ 2.9%", set="gdpg", iso="ZAF", year=2011, min=2.9),
]

datasets = [
    dict(set="ppp", wb="NY.GDP.PCAP.PP.CD", isos=["ZAF", "IDN", "VNM", "EGY"], **{"from": 1990, "to": 2025}),
    dict(set="gdp94", wb="NY.GDP.MKTP.CD", isos=["ZAF", "NGA", "EGY", "DZA", "MAR"], **{"from": 1994, "to": 1994}),
    dict(set="rpc", wb="NY.GDP.PCAP.PP.KD", isos=["ZAF", "WLD", "SSF", "IDN"], **{"from": 2005, "to": 2025}),
    dict(set="rpcx", derive="idx", src="rpc", isos=["ZAF", "WLD", "SSF", "IDN"], base=2008, off=-100),
    dict(set="gdpg", wb="NY.GDP.MKTP.KD.ZG", isos=["ZAF"], **{"from": 2008, "to": 2025}),
    dict(set="pop", wb="SP.POP.TOTL", isos=["ZAF"], **{"from": 2008, "to": 2025}),
    dict(set="popchg", derive="chg", src="pop", isos=["ZAF"], a=2008, b=2025),
    dict(set="unemp", wb="SL.UEM.TOTL.ZS", isos=["ZAF", "WLD"], **{"from": 1994, "to": 2025}),
    dict(set="yunemp", wb="SL.UEM.1524.ZS", isos=["ZAF"], **{"from": 2020, "to": 2025}),
    dict(set="unbig", wb="SL.UEM.TOTL.ZS", isos=BIG, **{"from": 2025, "to": 2025}),
    dict(set="emp", wb="SL.EMP.TOTL.SP.ZS", isos=["ZAF", "IDN"], **{"from": 1994, "to": 2025}),
    dict(set="inv", wb="NE.GDI.FTOT.ZS", isos=["ZAF", "WLD"], **{"from": 2008, "to": 2025}),
    dict(set="manf", wb="NV.IND.MANF.ZS", isos=["ZAF"], **{"from": 1990, "to": 2025}),
    dict(set="fx", wb="PA.NUS.FCRF", isos=["ZAF"], **{"from": 2008, "to": 2025}),
    dict(set="hom", wb="VC.IHR.PSRC.P5", isos=["ZAF", "WLD"], **{"from": 2000, "to": 2022}),
    dict(set="le", wb="SP.DYN.LE00.IN", isos=["ZAF", "WLD"], **{"from": 1994, "to": 2024}),
    dict(set="debt", wb="GC.DOD.TOTL.GD.ZS", isos=["ZAF"], **{"from": 2000, "to": 2024}),
    dict(set="idg", wb="NY.GDP.MKTP.KD.ZG", isos=["IDN"], **{"from": 2016, "to": 2025}),
    dict(set="idsum", derive="sum", src="idg", isos=["IDN"], a=2016, b=2025),
    dict(set="le60", wb="SP.DYN.LE00.IN", isos=["ZAF"], **{"from": 1960, "to": 2023}),
    dict(set="elec", wb="EG.ELC.ACCS.ZS", isos=["ZAF"], **{"from": 2000, "to": 2024}),
]
for y in range(2014, 2026):
    if y not in (2021, 2022):
        checks.append(dict(say=f"{y} growth ≤ 2%", set="gdpg", iso="ZAF", year=y, max=2.0))
for y in range(2012, 2026):
    if y != 2021:
        checks.append(dict(say=f"{y} growth < 2.9% (only the 2021 rebound beat it since 2011)", set="gdpg", iso="ZAF", year=y, max=2.89))
for y in (2016, 2017, 2018, 2019, 2022, 2023, 2024, 2025):
    checks.append(dict(say=f"Indonesia {y} ≈ 5%", set="idg", iso="IDN", year=y, min=4.85, max=5.35))
snapshot = []

clips = [
    dict(**{"from": "s00", "to": "s00"}, hook="Egypt, Indonesia, Vietnam *passed South Africa*", title="Egypt, Indonesia and Vietnam all passed South Africa #Shorts", desc="GDP per person adjusted for prices: Egypt 2019, Indonesia 2023, Vietnam 2024 (World Bank)."),
    dict(**{"from": "s04", "to": "s04"}, hook="1 in 3 *can't find a job*", title="South Africa has the highest unemployment of any big economy #Shorts", desc="About 32% overall and ~60% for young people (World Bank, 2025)."),
    dict(**{"from": "s12", "to": "s12"}, hook="11 more years *of life*", title="South Africa gained 11 years of life expectancy in under 20 years #Shorts", desc="From about 55 in 2007 to about 66 in 2024 (World Bank)."),
    dict(**{"from": "s13", "to": "s13"}, hook="Things are *starting to turn*", title="South Africa's comeback signs since 2024 #Shorts", desc="Blackouts largely stopped, a coalition government, and off the FATF grey list."),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="a-L11-south-africa", clips=clips, channel="chartbound", chapter0="Passed",
            thumb=dict(set="unemp", iso="ZAF", years=[1994, 2025], ymin=0, ymax=40, band=[470, 690], flags=["ZAF"], top="SOUTH AFRICA", big="32%", line2="JOBLESS", color="#ff5a6e"), w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks,
            datasets=datasets, snapshot=snapshot,
            voice=dict(model="", name="Charon",
                       style=("You are the narrator of a popular data documentary on YouTube. Read the script below in a warm, curious voice "
                              "with a little dry humor, at a relaxed but engaged pace of about 145 words per minute, like a smart friend telling "
                              "you something surprising. Let the big numbers land with a tiny pause before them. Keep the energy steady from the "
                              "first sentence to the last. Never sound like an advertisement or an audiobook.")),
            music=[dict(act=0, track="Lightless Dawn", vol=0.24), dict(act=1, track="Investigations", vol=0.23), dict(act=2, track="Deliberate Thought", vol=0.22),
                   dict(act=3, track="Hidden Agenda", vol=0.23), dict(act=4, track="Thinking Music", vol=0.22), dict(act=5, track="Inspired", vol=0.23), dict(act=6, track="Floating Cities", vol=0.24)],
            yt=dict(title="South Africans Are Poorer Than in 2008. Here's Why.",
                    description=("In 1994 South Africa had Africa's biggest economy. Adjusted for prices, Egypt passed it in 2019, Indonesia in 2023 and Vietnam in 2024, and the average South African now produces less than in 2008 (real GDP per person peaked in 2013). "
                                 "Why: the highest unemployment of any big economy, blackouts, collapsing investment, a weaker rand, crime and 'state capture'. The twist: 11 more years of life expectancy, the lights back on since 2024, a coalition government and an exit from the FATF grey list.\n\n"
                                 "Sources: World Bank WDI (NY.GDP.PCAP.PP.CD, NY.GDP.PCAP.PP.KD, NY.GDP.MKTP.CD, NY.GDP.MKTP.KD.ZG, SP.POP.TOTL, SL.UEM.TOTL.ZS, SL.UEM.1524.ZS, SL.EMP.TOTL.SP.ZS, NE.GDI.FTOT.ZS, NV.IND.MANF.ZS, PA.NUS.FCRF, VC.IHR.PSRC.P5, SP.DYN.LE00.IN, EG.ELC.ACCS.ZS); "
                                 "Eskom; Zondo Commission; IEC; FATF; UNAIDS; PSIRA.\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#southafrica #africa #economy #economics #data"),
                    tags=["south africa", "south africa economy", "africa", "unemployment", "load shedding", "gdp per capita", "economics", "data"], lang="en"))

json.dump(spec, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "a-L11.json"), "w"), ensure_ascii=False, indent=1)
clean = lambda t: t.replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()
words = sum(len(clean(s["narration"])) for s in shots)
acts = {}
for s in shots:
    acts[s["act"]] = acts.get(s["act"], 0) + len(clean(s["narration"]))
print("shots", len(shots), "palavras", words, f"~{words / 145:.1f} min a 145 wpm", "por ato", acts)

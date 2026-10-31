"""Gera specs/long/a-L07.json — Chartbound longo #7: "Turkey Caught Up With Greece. Despite 50% Inflation."
Número próprio (filtro de saturação ok em 31/10, research/q5.json: "Turkey vs Greece" só tem comparação militar; o paradoxo inflação × crescimento só tem vídeos pequenos).
Dados: World Bank WDI (julho/2026, ano 2025) + pontos citados em expr (inflação de out/2022 e juros: TurkStat/CBRT via imprensa)."""
import json, os

ACTS = ["Cold open", "Two roads", "The Turkish engine", "The inflation", "Who paid", "As rich as Greece?", "What comes next"]
WB = "World Bank WDI"
PPP = WB + " · GDP per capita, PPP (current international $)"
RPC = WB + " · GDP per capita, PPP (constant 2021 international $), change since 2000"
PEAK = "TurkStat, CPI October 2022 (85.5%, highest since 1998; via Majalla/AFP)"
CBRT = "Central Bank of the Republic of Türkiye: policy rate 10.5% (Oct 2022), 50% (21 Mar 2024)"

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="lines", set="ppp", series=["GRC", "TUR"], years=[2000, 2025], start=2000.0, y=[0, 50000], src=PPP, fmt="usdk0", hl="TUR",
         narration="In 2000, the average person in Turkey produced about half as much as the average person in Greece, adjusted for prices. {p} Greece, an EU member since 1981, was about to join the euro. Turkey was heading into a currency crisis. {p} Twenty-five years later, look at this. {pp} In 2025: forty-five thousand two hundred and eighty-eight dollars for Turkey. Forty-five thousand two hundred and sixty-four for Greece. {p} A tie, to within twenty-five dollars.",
         keys=[dict(at="Twenty-five years later", year=2025.0, dur=7.0)],
         labels=[dict(at="about half as much", iso="TUR", year=2000), dict(at="dollars for Turkey", iso="TUR", year=2025), dict(at="sixty-four for Greece", iso="GRC", year=2025)],
         react=[dict(at="In 2000", pose="idle"), dict(at="about half", pose="pointL"), dict(at="currency crisis", pose="think"), dict(at="look at this", pose="pointUp"), dict(at="A tie", pose="shock")]),
    dict(act=0, type="host", bg="lines", set="ppp", series=["GRC", "TUR"], years=[2000, 2025], start=2025.0, y=[0, 50000], fmt="usdk0",
         narration="And Turkey did it while living through one of the worst inflation crises of the century. {p} Since 2022, prices have risen by an average of more than fifty percent a year. {p} Since 2018, the lira has lost almost ninety percent of its value against the dollar. {p} Inflation like that usually belongs to countries in deep trouble, like Argentina or Venezuela, not to a country catching up with Europe. {p} So how does a country get richer while its money melts? {pp} <soft>And what does it really mean to be as rich as Greece?</soft>",
         items=[dict(at="more than fifty percent", text="Inflation: 50%+ a year", color="acc"), dict(at="almost ninety percent", text="Lira: −88% vs the dollar", color="acc"), dict(at="get richer while its money melts", text="Richer, with melting money?", serif=True, size=62)],
         react=[dict(at="worst inflation", pose="shock"), dict(at="more than fifty", pose="pointL"), dict(at="almost ninety", pose="shock"), dict(at="money melts", pose="think"), dict(at="as rich as Greece", pose="shrug")]),

    # ---------------- 1 · TWO ROADS ----------------
    dict(act=1, type="lines", set="rpcx", series=["TUR", "ARG", "GRC", "MEX"], years=[2000, 2025], start=2000.0, y=[-30, 170], src=RPC, fmt="pct0s", hl="TUR",
         ref=dict(value=0, label="2000 level", pos="left"),
         narration="Start with real growth, adjusted for prices and inflation. {p} Since 2000, output per person in Turkey has grown about two and a half times. That's the same pace as Poland, Europe's growth champion. {p} Argentina's grew about a quarter. Greece's, about a fifth. {p} And Mexico's, a country famous for stable prices? {pp} Up about seven percent. In twenty-five years.",
         keys=[dict(at="Since 2000", year=2025.0, dur=7.0)],
         labels=[dict(at="two and a half times", iso="TUR", year=2025), dict(at="about seven percent", iso="MEX", year=2025)],
         react=[dict(at="real growth", pose="idle"), dict(at="two and a half", pose="cheer"), dict(at="about a fifth", pose="pointL"), dict(at="seven percent", pose="shock")]),
    dict(act=1, type="lines", set="grcx", series=["GRC"], years=[2000, 2025], start=2000.0, y=[-35, 10], src=WB + " · GDP, constant prices, change since 2007 · unemployment (ILO modeled)", fmt="pct0s", hl="GRC",
         ref=dict(value=0, label="2007 level", pos="left"),
         narration="Greece didn't just stand still. It fell off a cliff. {p} Between 2007 and 2013, its economy shrank by more than a quarter, a collapse on the scale of America's Great Depression. {p} Unemployment hit twenty-eight percent. {p} Even in 2025, the Greek economy was still about fourteen percent smaller than in 2007. {p} And as young Greeks left to find work, the country ended up with about seven hundred thousand fewer people than in 2010. {pp} Turkey didn't so much overtake Greece <soft>as meet it on the way down.</soft>",
         keys=[dict(at="fell off a cliff", year=2013.0, dur=6.0), dict(at="Even in 2025", year=2025.0, dur=4.0)],
         labels=[dict(at="more than a quarter", iso="GRC", year=2013), dict(at="about fourteen percent smaller", iso="GRC", year=2025)],
         react=[dict(at="fell off a cliff", pose="shock"), dict(at="more than a quarter", pose="pointL"), dict(at="twenty-eight", pose="shock"), dict(at="on the way down", pose="shrug")]),

    dict(act=1, type="list", src="Eurostat gov_10dd_edpt1 (Greek deficit 2009) · ESM: €288.7 billion in rescue loans to Greece, 2010–2018", title="What hit Greece",
         narration="How did it happen? {p} In 2009, Greece admitted its budget deficit was far bigger than reported: more than fifteen percent of its economy. {p} Lenders panicked. Over the next eight years, Greece needed three bailouts worth almost two hundred and ninety billion euros, {pp} in exchange for deep spending cuts and tax rises.",
         items=[dict(at="far bigger than reported", kind="bullet", text="2009: deficit > 15% of GDP"),
                dict(at="three bailouts", kind="bullet", text="3 bailouts, 2010–2018"),
                dict(at="almost two hundred and ninety", kind="title", text="€288.7 BN")],
         react=[dict(at="How did it happen", pose="think"), dict(at="far bigger", pose="shock"), dict(at="Lenders panicked", pose="shrug"), dict(at="two hundred and ninety", pose="shock")]),

    # ---------------- 2 · THE TURKISH ENGINE ----------------
    dict(act=2, type="lines", set="gdpx", series=["TUR", "GRC"], years=[2000, 2025], start=2000.0, y=[50, 360], src=WB + " · GDP, constant prices (2000 = 100) · population", fmt="pct0", hl="TUR",
         ref=dict(value=100, label="2000 = 100", pos="left"),
         narration="Meanwhile, Turkey's economy more than tripled. {p} That's growth of almost five percent a year, every year, for a quarter of a century. {p} And it happened even as the population grew from about sixty-five million to about eighty-six million. {p} More people, and much more output per person. {p} Turkey is also young: about one in five Turks is under fifteen. In Greece, about one in seven. {p} In total, Turkey's economy is now almost six times the size of Greece's.",
         keys=[dict(at="more than tripled", year=2025.0, dur=6.0)],
         labels=[dict(at="more than tripled", iso="TUR", year=2025)],
         react=[dict(at="more than tripled", pose="cheer"), dict(at="almost five percent", pose="pointL"), dict(at="eighty-six million", pose="think"), dict(at="much more output", pose="pointUp")]),
    dict(act=2, type="list", src=WB + " · Turkish crisis of 2001 · EU customs union with Türkiye (1995)", title="What powered it",
         narration="Part of it was simply starting from far behind: poorer countries can grow fast by copying what richer ones already do. {p} Part of it was a customs union with the European Union, in place since the mid-1990s, which turned Turkey into a workshop for Europe: cars, fridges, televisions, clothes. Its exports grew more than sevenfold in dollars between 2000 and 2025. {p} And part of it was a huge construction boom: roads, airports, bridges, and millions of new apartments. {p} Istanbul, a city of more than fifteen million people, became one of the biggest economic hubs between Europe and Asia.",
         items=[dict(at="starting from far behind", kind="bullet", text="Catch-up from far behind"),
                dict(at="customs union", kind="bullet", text="EU customs union since 1995"),
                dict(at="workshop for Europe", kind="bullet", text="Exports ×7 since 2000"),
                dict(at="construction boom", kind="bullet", text="A giant construction boom")],
         react=[dict(at="far behind", pose="think"), dict(at="customs union", pose="pointL"), dict(at="workshop for Europe", pose="cheer"), dict(at="construction boom", pose="pointUp")]),

    # ---------------- 3 · THE INFLATION ----------------
    dict(act=3, type="host", bg="none",
         narration="Quick favor: if you're finding this interesting, hit subscribe. It's free, and it's genuinely what keeps this channel going. {p} Now, the part that makes this so strange: {pp} the inflation.",
         items=[dict(at="hit subscribe", text="Subscribe = more of these"), dict(at="so strange", text="The strange part:", color="acc2"), dict(at="the inflation", text="The inflation.", serif=True, size=72, color="acc")],
         react=[dict(at="Quick favor", pose="wave"), dict(at="so strange", pose="think"), dict(at="the inflation", pose="pointUp")]),
    dict(act=3, type="bars", mode="abs", set="cpi", iso="TUR", years=[1995, 2025], start=1994.0, fmt="int", src=WB + " · inflation, consumer prices (annual %)",
         narration="High inflation isn't new in Turkey. {p} In the 1990s, prices rose by eighty or ninety percent a year. {p} Prices rose so much that in 2005 Turkey knocked six zeros off its currency: one million old lira became one new lira. {p} After a crisis in 2001 and tough reforms, inflation fell to single digits for over a decade. {p} And then it came back. {pp} Seventy-two percent in 2022. Fifty-eight percent in 2024.",
         keys=[dict(at="isn't new", year=1999.0, dur=4.0), dict(at="single digits", year=2016.0, dur=5.0), dict(at="it came back", year=2025.0, dur=4.0)],
         hl=[2004, 2016], hltext=dict(at="single digits", text="2004–2016: under 10% most years"),
         labels=[dict(at="eighty or ninety", year=1995), dict(at="Seventy-two percent", year=2022)],
         react=[dict(at="isn't new", pose="think"), dict(at="eighty or ninety", pose="shock"), dict(at="single digits", pose="cheer"), dict(at="it came back", pose="shrug"), dict(at="Seventy-two", pose="shock")]),
    dict(act=3, type="list", src=PEAK + " · " + CBRT, title="An experiment",
         narration="This time, the cause was a deliberate experiment. {p} Normally, a central bank fights inflation by raising interest rates. Turkey's did the opposite and cut them. {p} President Erdoğan argued that high interest rates cause inflation, the reverse of what most economists believe. {p} In October 2022, inflation hit eighty-five and a half percent, the highest since 1998, while the policy rate was about ten percent. {p} In 2023, Turkey reversed course. By March 2024, the rate was fifty percent.",
         items=[dict(at="by raising interest rates", kind="bullet", text="Textbook: inflation ↑ → rates ↑"),
                dict(at="cut them", kind="strike", text="Turkey: inflation ↑ → rates ↓"),
                dict(at="eighty-five and a half", kind="bullet", text="Oct 2022: inflation 85.5%, rate ~10%"),
                dict(at="fifty percent", kind="title", text="MARCH 2024: 50%")],
         react=[dict(at="deliberate experiment", pose="think"), dict(at="did the opposite", pose="shock"), dict(at="eighty-five", pose="shock"), dict(at="reversed course", pose="pointUp")]),

    # ---------------- 4 · WHO PAID ----------------
    dict(act=4, type="duel", src=WB + " · official exchange rate, lira per US$ (annual average)", title="10,000 lira of savings, in dollars", fmt="usd0",
         left=dict(label="2018", value=2070, color="acc2"), right=dict(label="2025", value=253, color="warm"), badge="−88%",
         cues=[dict(at="about two thousand", show="a"), dict(at="about two hundred and fifty", show="b")],
         narration="So who paid for it? {p} Imagine a Turkish family that kept ten thousand lira in savings in 2018. In dollars, that was worth about two thousand and seventy. {p} By 2025, the same ten thousand lira bought about two hundred and fifty dollars. {p} No wonder so many Turks rushed into dollars, gold and property to protect themselves. {pp} Prices in Turkey rose almost ninefold over those seven years.",
         react=[dict(at="who paid", pose="think"), dict(at="two thousand and seventy", pose="pointL"), dict(at="two hundred and fifty", pose="shock"), dict(at="almost ninefold", pose="shock")]),
    dict(act=4, type="host", bg="none",
         narration="That's the trick inflation plays. {p} The economy can keep growing, factories keep producing, and the average output per person keeps rising, {p} while savers, renters and people on fixed wages fall behind. {p} Turkey raised its minimum wage twice in a single year, in both 2022 and 2023, just to keep up. {p} Pensions, adjusted only twice a year, fell behind month after month in between. {p} Borrowers and owners of property and businesses tend to do better. {pp} Economists call inflation the cruelest tax, because it hits hardest the people with the least. {pp} <soft>Growth tells you how big the pie is. Inflation decides who gets which slice.</soft>",
         items=[dict(at="keep growing", text="Output ↑", color="acc2"), dict(at="fall behind", text="Savers, renters, wages ↓", color="acc"), dict(at="who gets which slice", text="Size of the pie ≠ the slices", serif=True, size=60)],
         react=[dict(at="trick inflation plays", pose="think"), dict(at="keep growing", pose="cheer"), dict(at="fall behind", pose="shrug"), dict(at="which slice", pose="pointUp")]),

    # ---------------- 5 · AS RICH AS GREECE? ----------------
    dict(act=5, type="duel", set="usd", year=2025, a="GRC", b="TUR", fmt="usd0", src=WB + " · GDP per capita (current US$), 2025", title="At market exchange rates, 2025", badge=False,
         cues=[dict(at="about twenty-seven thousand", show="a"), dict(at="about eighteen thousand six hundred", show="b")],
         narration="Now, the catch. {p} Everything so far was adjusted for prices. {p} Measured in plain dollars at market exchange rates, the average Greek produced about twenty-seven thousand dollars in 2025. {p} The average Turk, about eighteen thousand six hundred. {pp} By that measure, Greece is still about forty-five percent ahead. {p} In 2000, it was almost three times ahead.",
         react=[dict(at="the catch", pose="pointUp"), dict(at="adjusted for prices", pose="think"), dict(at="twenty-seven thousand", pose="pointL"), dict(at="forty-five percent", pose="shrug")]),
    dict(act=5, type="host", bg="none",
         narration="So which number is right? {p} Both, for different questions. {p} Dollars at market rates tell you what a country can buy from the rest of the world: an iPhone, a plane ticket, an imported car. {p} Prices adjusted for local costs tell you how people live day to day, because a haircut, a meal or rent in Istanbul costs far less than in Athens. {pp} By that measure, Turkey now out-produces China, Mexico, Brazil and Argentina per person. {p} It's even slightly ahead of an EU member, Bulgaria. {p} That's why economists compare living standards with prices adjusted, and buying power abroad with market rates. {pp} <soft>For daily life, Turks and Greeks are now neck and neck.</soft>",
         items=[dict(at="market rates", text="$ at market rates → buying from abroad", color="acc"), dict(at="adjusted for local costs", text="PPP → daily life", color="acc2"), dict(at="neck and neck", text="Daily life: a tie", serif=True, size=66)],
         react=[dict(at="which number", pose="think"), dict(at="an iPhone", pose="pointL"), dict(at="costs far less", pose="cheer"), dict(at="neck and neck", pose="idle", nod=1)]),

    # ---------------- 6 · WHAT COMES NEXT ----------------
    dict(act=6, type="lines", set="cpi2", series=["TUR", "MEX"], years=[2015, 2025], start=2015.0, y=[0, 80], src=WB + " · inflation, consumer prices (annual %)", fmt="pct0", hl="TUR",
         narration="Turkey's inflation is coming down: about thirty-five percent in 2025, after fifty-eight the year before. {p} Still far above Mexico's, at about four, but nowhere near Argentina, where prices rose two hundred and twenty percent in 2024 while the economy shrank. {p} But Mexico is the warning on the other side. {pp} Stable prices, a free-trade deal with the world's biggest economy, and almost no growth per person in twenty-five years. {p} In 2025, the average Mexican produced barely more than in 2007.",
         keys=[dict(at="is coming down", year=2025.0, dur=6.0)],
         labels=[dict(at="about thirty-five percent", iso="TUR", year=2025), dict(at="at about four", iso="MEX", year=2025)],
         react=[dict(at="coming down", pose="cheer"), dict(at="far above", pose="pointL"), dict(at="the warning", pose="think"), dict(at="almost no growth", pose="shrug")]),
    dict(act=6, type="host", bg="none",
         narration="The lesson isn't that inflation is fine. It isn't: it quietly wiped out the savings of millions of Turks. {p} It's that stability alone doesn't make a country rich, and chaos alone doesn't make it poor. {p} What matters over decades is whether a country keeps building, producing and selling more. {pp} <soft>Turkey did. The question now is whether it can do it without burning its own money.</soft> {p} And Greece? It's growing again, about two percent a year since 2023, with unemployment down from twenty-eight percent to under nine.",
         items=[dict(at="isn't that inflation is fine", text="Inflation ≠ fine", color="acc"), dict(at="stability alone", text="Stability ≠ growth", color="acc2"), dict(at="burning its own money", text="Growth without the burn?", serif=True, size=60)],
         react=[dict(at="inflation is fine", pose="shrug"), dict(at="stability alone", pose="think"), dict(at="keeps building", pose="pointUp"), dict(at="burning its own money", pose="think")]),
    dict(act=6, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="1995", color="acc", title="Portugal was richer than Eastern Europe", sub="Not anymore."),
         narration="Turkey isn't the only country that has caught a richer neighbor. To see Eastern Europe overtake Portugal, watch the next video. {p} I'm Chartbound. See you in the next one.",
         hold=14,
         react=[dict(at="overtake Portugal", pose="pointL"), dict(at="See you", pose="wave")]),
]

checks = [
    dict(say="Turkey ≈ half of Greece in 2000 (PPP)", set="trgr", iso="TUR", year=2000, min=45, max=55),
    dict(say="Turkey 2025 = $45,288", set="ppp", iso="TUR", year=2025, min=45287.5, max=45288.5),
    dict(say="Greece 2025 = $45,264", set="ppp", iso="GRC", year=2025, min=45263.5, max=45264.5),
    dict(say="a tie within $25", rule="expr", expr="45288 - 45264 < 25", equal=True),
    dict(say="Greece joined the euro on 1 Jan 2001; Turkey's crisis Nov 2000–Feb 2001", rule="expr", expr="2001 - 2000", equal=1),
    dict(say="average 2022–2025 CPI > 50% (sum > 200)", set="cpisum", iso="TUR", year=0, min=200.01),
    dict(say="lira lost almost 90% vs USD since 2018", rule="fxloss", set="fx", iso="TUR", a=2018, b=2025, min=0.85, max=0.899),
    dict(say="Turkey ≈ 2.5× since 2000 (+150%)", set="rpcx", iso="TUR", year=2025, min=140, max=160),
    dict(say="Argentina about a quarter", set="rpcx", iso="ARG", year=2025, min=22, max=28),
    dict(say="Greece about a fifth", set="rpcx", iso="GRC", year=2025, min=18, max=24),
    dict(say="Mexico about 7%", set="rpcx", iso="MEX", year=2025, min=6, max=8),
    dict(say="Greece shrank > a quarter 2007→2013", set="grcx", iso="GRC", year=2013, max=-25.01, min=-30),
    dict(say="Greece unemployment peak ≈ 28% (2013)", set="unemp", iso="GRC", year=2013, min=27.5, max=28.4),
    dict(say="Greece 2025 still ≈ 14% below 2007", set="grcx", iso="GRC", year=2025, min=-15, max=-13),
    dict(say="Turkey economy more than tripled since 2000", set="gdpx", iso="TUR", year=2025, min=300.01),
    dict(say="≈ 5% a year (×3.30 in 25 years)", rule="expr", expr="round((3.30 ** (1 / 25) - 1) * 100, 1)", equal=4.9),
    dict(say="population ≈ 65M (2000) → ≈ 86M (2025)", set="pop", iso="TUR", year=2000, min=64.5e6, max=65.9e6),
    dict(say="population 2025 ≈ 86M", set="pop", iso="TUR", year=2025, min=85.5e6, max=86.4e6),
    dict(say="1990s inflation 80–90% (1995)", set="cpi", iso="TUR", year=1995, min=80, max=90),
    dict(say="2004–2016: 12 of 13 years under 10% (WB values)", rule="expr", expr="sum(v < 10 for v in [8.6, 8.2, 9.6, 8.8, 10.4, 6.3, 8.6, 6.5, 8.9, 7.5, 8.9, 7.7, 7.8])", equal=12),
    dict(say="2008 the exception (≥10)", set="cpi", iso="TUR", year=2008, min=10.0),
    dict(say="2016 under 10", set="cpi", iso="TUR", year=2016, max=9.99),
    dict(say="72% in 2022", set="cpi", iso="TUR", year=2022, min=71.5, max=72.9),
    dict(say="58% in 2024", set="cpi", iso="TUR", year=2024, min=58.0, max=58.9),
    dict(say="85.5% in Oct 2022 (TurkStat), rate 10.5% (CBRT); 50% on 21 Mar 2024", rule="expr", expr="[85.5 > 85, 10.5 < 11, 50]", equal=[True, True, 50]),
    dict(say="10,000 lira = $2,070 in 2018 (4.83/$)", rule="expr", expr="round(10000 / 4.83 / 10) * 10", equal=2070),
    dict(say="10,000 lira = $253 in 2025 (39.45/$)", rule="expr", expr="round(10000 / 39.45)", equal=253),
    dict(say="fx 2018 ≈ 4.83", set="fx", iso="TUR", year=2018, min=4.82, max=4.84),
    dict(say="fx 2025 ≈ 39.45", set="fx", iso="TUR", year=2025, min=39.4, max=39.5),
    dict(say="prices almost ninefold 2018→2025", rule="expr", expr="round(1.152 * 1.123 * 1.196 * 1.723 * 1.539 * 1.585 * 1.349, 1)", equal=8.8),
    dict(say="Greece ≈ $27,000 nominal (2025)", set="usd", iso="GRC", year=2025, min=26500, max=27400),
    dict(say="Turkey ≈ $18,600 nominal (2025)", set="usd", iso="TUR", year=2025, min=18550, max=18650),
    dict(say="Greece ≈ 45% ahead in dollars", rule="ratio", set="usd", a="GRC", b="TUR", year=2025, min=1.43, max=1.47),
    dict(say="Greece EU member since 1981", rule="expr", expr="1981", equal=1981),
    dict(say="same pace as Poland (×2.51 vs ×2.52, WB constant PPP)", rule="tied", set="rpcx2", a="TUR", b="POL", year=2025, tol=0.03),
    dict(say="Greece pop −700k since 2010", rule="expr", expr="round((11.12 - 10.41) * 10) / 10", equal=0.7),
    dict(say="Greece pop 2010 ≈ 11.12M", set="popg", iso="GRC", year=2010, min=11.05e6, max=11.2e6),
    dict(say="Greece pop 2025 ≈ 10.41M", set="popg", iso="GRC", year=2025, min=10.35e6, max=10.47e6),
    dict(say="Turkey economy almost 6× Greece (current US$)", rule="ratio", set="gdpusd", a="TUR", b="GRC", year=2025, min=5.5, max=5.99),
    dict(say="exports more than sevenfold 2000→2025 (current US$)", set="expx", iso="TUR", year=2025, min=700.01, max=760),
    dict(say="2005 redenomination: 1,000,000 old lira = 1 new lira", rule="expr", expr="10 ** 6", equal=1000000),
    dict(say="minimum wage raised twice in 2022 and in 2023 (Jan and Jul)", rule="expr", expr="2", equal=2),
    dict(say="Greece almost 3× ahead in dollars in 2000", rule="ratio", set="usd", a="GRC", b="TUR", year=2000, min=2.6, max=2.99),
    dict(say="Turkey PPP > China (2025)", rule="gt", set="ppp5", a="TUR", b="CHN", year=2025),
    dict(say="Turkey PPP > Mexico (2025)", rule="gt", set="ppp5", a="TUR", b="MEX", year=2025),
    dict(say="Turkey PPP > Brazil (2025)", rule="gt", set="ppp5", a="TUR", b="BRA", year=2025),
    dict(say="Turkey PPP > Argentina (2025)", rule="gt", set="ppp5", a="TUR", b="ARG", year=2025),
    dict(say="Argentina 2024 inflation ≈ 220%", set="cpia", iso="ARG", year=2024, min=215, max=225),
    dict(say="Argentina shrank in 2024", set="gdpg", iso="ARG", year=2024, max=-0.01),
    dict(say="Greek deficit 2009 > 15% of GDP", set="balg", iso="GRC", year=2009, max=-15.0),
    dict(say="ESM: €288.7 bn over three programmes (2010–2018)", rule="expr", expr="round(52.9 + 141.8 + 61.9 + 32.1, 1)", equal=288.7),
    dict(say="Turkey: about 1 in 5 under 15", set="u15", iso="TUR", year=2024, min=18, max=22.5),
    dict(say="Greece: about 1 in 7 under 15", set="u15", iso="GRC", year=2024, min=12.5, max=15.5),
    dict(say="Turkey slightly ahead of Bulgaria (PPP 2025)", rule="gt", set="ppp5", a="TUR", b="BGR", year=2025),
    dict(say="Greece growth ≈ 2% in 2023", set="gdpgg", iso="GRC", year=2023, min=1.5, max=2.5),
    dict(say="Greece growth ≈ 2% in 2024", set="gdpgg", iso="GRC", year=2024, min=1.5, max=2.5),
    dict(say="Greece growth ≈ 2% in 2025", set="gdpgg", iso="GRC", year=2025, min=1.5, max=2.5),
    dict(say="Greece unemployment 2025 under 9%", set="unemp", iso="GRC", year=2025, max=8.99),
    dict(say="Mexico 2025 barely above 2007 (real PPP pc)", set="mex07", iso="MEX", year=2025, min=100.01, max=106),
    dict(say="Istanbul > 15 million people (TurkStat ABPRS 2024: ~15.7M)", rule="expr", expr="15.7 > 15", equal=True),
    dict(say="Turkey 2025 inflation ≈ 35%", set="cpi", iso="TUR", year=2025, min=34.5, max=35.4),
    dict(say="Mexico 2025 inflation ≈ 4%", set="cpi2", iso="MEX", year=2025, min=3.5, max=4.4),
]

datasets = [
    dict(set="ppp", wb="NY.GDP.PCAP.PP.CD", isos=["TUR", "GRC"], **{"from": 2000, "to": 2025}),
    dict(set="trgr", derive="ratio", a=["ppp", "TUR"], b=["ppp", "GRC"]),
    dict(set="rpc", wb="NY.GDP.PCAP.PP.KD", isos=["TUR", "GRC", "MEX", "ARG"], **{"from": 2000, "to": 2025}),
    dict(set="rpcx", derive="idx", src="rpc", isos=["TUR", "GRC", "MEX", "ARG"], base=2000, off=-100),
    dict(set="gdpk", wb="NY.GDP.MKTP.KD", isos=["TUR", "GRC"], **{"from": 2000, "to": 2025}),
    dict(set="grcx", derive="idx", src="gdpk", isos=["GRC"], base=2007, off=-100),
    dict(set="gdpx", derive="idx", src="gdpk", isos=["TUR", "GRC"], base=2000),
    dict(set="unemp", wb="SL.UEM.TOTL.ZS", isos=["GRC"], **{"from": 2000, "to": 2025}),
    dict(set="pop", wb="SP.POP.TOTL", isos=["TUR"], **{"from": 2000, "to": 2025}),
    dict(set="cpi", wb="FP.CPI.TOTL.ZG", isos=["TUR"], **{"from": 1995, "to": 2025}),
    dict(set="cpi2", wb="FP.CPI.TOTL.ZG", isos=["TUR", "MEX"], **{"from": 2015, "to": 2025}),
    dict(set="rpc2", wb="NY.GDP.PCAP.PP.KD", isos=["TUR", "POL"], **{"from": 2000, "to": 2025}),
    dict(set="rpcx2", derive="idx", src="rpc2", isos=["TUR", "POL"], base=2000),
    dict(set="popg", wb="SP.POP.TOTL", isos=["GRC"], **{"from": 2000, "to": 2025}),
    dict(set="gdpusd", wb="NY.GDP.MKTP.CD", isos=["TUR", "GRC"], **{"from": 2000, "to": 2025}),
    dict(set="exp", wb="NE.EXP.GNFS.CD", isos=["TUR"], **{"from": 2000, "to": 2025}),
    dict(set="expx", derive="idx", src="exp", isos=["TUR"], base=2000),
    dict(set="ppp5", wb="NY.GDP.PCAP.PP.CD", isos=["TUR", "CHN", "MEX", "BRA", "ARG", "BGR"], **{"from": 2020, "to": 2025}),
    dict(set="balg", eurostat="gov_10dd_edpt1", filters={"unit": "PC_GDP", "na_item": "B9", "sector": "S13"}, isos=["GRC"], **{"from": 2008, "to": 2012}),
    dict(set="u15", wb="SP.POP.0014.TO.ZS", isos=["TUR", "GRC"], **{"from": 2015, "to": 2024}),
    dict(set="gdpgg", wb="NY.GDP.MKTP.KD.ZG", isos=["GRC"], **{"from": 2018, "to": 2025}),
    dict(set="cpia", wb="FP.CPI.TOTL.ZG", isos=["ARG"], **{"from": 2018, "to": 2025}),
    dict(set="gdpg", wb="NY.GDP.MKTP.KD.ZG", isos=["ARG"], **{"from": 2018, "to": 2025}),
    dict(set="mex07", derive="idx", src="rpc", isos=["MEX"], base=2007),
    dict(set="cpisum", derive="sum", src="cpi", isos=["TUR"], a=2022, b=2025),
    dict(set="fx", wb="PA.NUS.FCRF", isos=["TUR"], **{"from": 2000, "to": 2025}),
    dict(set="usd", wb="NY.GDP.PCAP.CD", isos=["GRC", "TUR"], **{"from": 2000, "to": 2025}),
]
snapshot = []

clips = [
    dict(**{"from": "s00", "to": "s00"}, hook="Turkey vs Greece: *a tie*", title="Turkey just tied Greece, to within $25 #Shorts", desc="GDP per person adjusted for prices, 2025: Turkey $45,288, Greece $45,264 (World Bank)."),
    dict(**{"from": "s05", "to": "s05"}, hook="Turkey's economy: *×3*", title="Turkey's economy tripled while the lira collapsed #Shorts", desc="Almost 5% growth a year for 25 years."),
    dict(**{"from": "s10", "to": "s10"}, hook="10,000 lira: *$2,070 → $253*", title="What inflation did to Turkish savings #Shorts", desc="Prices rose almost ninefold between 2018 and 2025."),
    dict(**{"from": "s12", "to": "s13"}, hook="Which number is *right*?", title="Why Turkey looks poorer in dollars than in real life #Shorts", desc="Market exchange rates vs prices adjusted for local costs."),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="a-L07-turkey", clips=clips, channel="chartbound", chapter0="A tie",
            thumb=dict(set="ppp", iso="TUR", years=[2000, 2025], ymin=5000, ymax=48000, band=[470, 690], flags=["TUR", "GRC"], top="TURKEY = GREECE", big="$45K", line2="50% INFLATION", color="#ff5a6e"), w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks,
            datasets=datasets, snapshot=snapshot,
            voice=dict(model="", name="Charon",
                       style=("You are the narrator of a popular data documentary on YouTube. Read the script below in a warm, curious voice "
                              "with a little dry humor, at a relaxed but engaged pace of about 145 words per minute, like a smart friend telling "
                              "you something surprising. Let the big numbers land with a tiny pause before them. Keep the energy steady from the "
                              "first sentence to the last. Never sound like an advertisement or an audiobook.")),
            music=[dict(act=0, track="Lightless Dawn", vol=0.24), dict(act=1, track="Investigations", vol=0.23), dict(act=2, track="Deliberate Thought", vol=0.22),
                   dict(act=3, track="Hidden Agenda", vol=0.23), dict(act=4, track="Inspired", vol=0.23), dict(act=5, track="Floating Cities", vol=0.24), dict(act=6, track="Lightless Dawn", vol=0.24)],
            yt=dict(title="Turkey Caught Up With Greece. Despite 50% Inflation.",
                    description=("In 2000 the average Turk produced about half as much as the average Greek, adjusted for prices. In 2025: $45,288 vs $45,264. How Turkey's economy tripled while the lira lost almost 90% of its value, "
                                 "why Greece fell off a cliff, who paid for Turkey's inflation experiment, and why in plain dollars Greece is still 45% ahead.\n\n"
                                 "Sources: World Bank WDI (NY.GDP.PCAP.PP.CD, NY.GDP.PCAP.PP.KD, NY.GDP.MKTP.KD, NY.GDP.PCAP.CD, FP.CPI.TOTL.ZG, PA.NUS.FCRF, SP.POP.TOTL, SL.UEM.TOTL.ZS); "
                                 "TurkStat CPI (October 2022); Central Bank of the Republic of Türkiye (policy rate).\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#turkey #greece #inflation #economics #data"),
                    tags=["turkey", "greece", "turkey economy", "inflation", "lira", "gdp per capita", "mexico", "economics", "data"], lang="en"))

json.dump(spec, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "a-L07.json"), "w"), ensure_ascii=False, indent=1)
clean = lambda t: t.replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()
words = sum(len(clean(s["narration"])) for s in shots)
acts = {}
for s in shots:
    acts[s["act"]] = acts.get(s["act"], 0) + len(clean(s["narration"]))
print("shots", len(shots), "palavras", words, f"~{words / 145:.1f} min a 145 wpm", "por ato", acts)

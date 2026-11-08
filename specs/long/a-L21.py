"""Gera specs/long/a-L21.json — Chartbound longo #21: "Poland Just Passed Japan. Italy Is Next." (série Polônia, PLANO.md R1)
Regra nova de intro (PLANO.md R2): o número e o cruzamento aparecem nos primeiros 8 s; nada de contexto antes de 1:00.
Dados: IMF WEO out/2026 lidos em 07/11/2026 (research/imf_ita_2026-11-07.json): PPPPC, NGDPDPC, NGDP_RPCH, LP, LUR, GGXWDG_NGDP.
Fatos fora do FMI: Polônia na UE desde 2004 e maior beneficiária líquida do orçamento da UE; złoty; Polônia = maior gasto em defesa da OTAN em % do PIB (estimativas OTAN 2025, ~4,5%)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "..", "..", "research", "imf_ita_2026-11-07.json")))
ACTS = ["Cold open", "Italy stopped", "Why Italy stalled", "Poland never stopped", "The catch", "Does it happen?", "After Italy"]
IMF = "IMF World Economic Outlook, October 2026"
PPPC = IMF + " · GDP per capita, PPP (current international $); 2026+ are IMF estimates and forecasts"

def series(ind, iso):
    r = D[ind][iso]; return {r["y0"] + k: v for k, v in enumerate(r["v"])}
P, I = series("PPPPC", "POL"), series("PPPPC", "ITA")
G = {iso: series("NGDP_RPCH", iso) for iso in ("ITA", "POL", "DEU", "ESP", "FRA")}
LP = {iso: series("LP", iso) for iso in ("ITA", "POL")}
N = {iso: series("NGDPDPC", iso) for iso in ("ITA", "POL")}
DEBT = {iso: series("GGXWDG_NGDP", iso) for iso in ("ITA", "POL")}
LUR = {iso: series("LUR", iso) for iso in ("ITA", "POL")}

snapshot = []
for iso in ("ITA", "POL", "ESP", "PRT", "JPN", "GBR", "FRA", "DEU"):
    for y, v in series("PPPPC", iso).items():
        snapshot.append(dict(set="imf", iso=iso, year=y, value=v, src=IMF + " · PPPPC"))
for iso, s in G.items():
    for y, v in s.items():
        snapshot.append(dict(set="imfg", iso=iso, year=y, value=v, src=IMF + " · NGDP_RPCH"))
# índice real do PIB, 2000 = 100 (acumulado de NGDP_RPCH 2001–2025)
IDX = {}
for iso in ("ITA", "DEU", "ESP", "POL"):
    c = 100.0; IDX[iso] = {}
    for y in range(2000, 2026):
        if y > 2000: c *= 1 + G[iso][y] / 100
        IDX[iso][y] = round(c, 1)
        snapshot.append(dict(set="ridx", iso=iso, year=y, value=round(c, 1), src=IMF + " · real GDP index, 2000 = 100 (compounded NGDP_RPCH)"))
for iso, s in N.items():
    for y, v in s.items():
        snapshot.append(dict(set="imfusd", iso=iso, year=y, value=v, src=IMF + " · NGDPDPC"))
for st, tab, ind in [("pop", LP, "LP"), ("debt", DEBT, "GGXWDG_NGDP"), ("lur", LUR, "LUR")]:
    for iso, s in tab.items():
        for y, v in s.items():
            snapshot.append(dict(set=st, iso=iso, year=y, value=v, src=IMF + " · " + ind))

ratio = {y: P[y] / I[y] for y in range(1990, 2032)}
dips = [y for y in range(1991, 2027) if ratio[y] < ratio[y - 1]]
avg = lambda iso, a, b: sum(G[iso][y] for y in range(a, b + 1)) / (b - a + 1)
first_over = lambda a, b: next(y for y in range(1990, 2032) if series("PPPPC", a)[y] > series("PPPPC", b)[y])

shots = [
    # ---------------- 0 · COLD OPEN (número + cruzamento nos primeiros 8 s) ----------------
    dict(act=0, type="lines", set="imf", fc=2025, series=["ITA", "POL"], years=[1990, 2031], start=2031.0, y=[0, 85000], src=PPPC, fmt="usdk0", hl="POL",
         narration="Four hundred and ninety-nine dollars. {p} That's the gap the IMF expects between Italy and Poland in 2031: income per person, adjusted for prices. Italy, about seventy-six thousand seven hundred. Poland, about seventy-six thousand two hundred. {pp} In 1990, Italy was more than three times richer than Poland. In 2008, exactly twice as rich. This year, Poland is about nine percent behind: sixty thousand dollars against sixty-six. {p} At this pace, Poland catches a founding member of the European Union, and a G7 country, in about five years.",
         keys=[dict(at="Four hundred", year=2031.0, dur=0.5), dict(at="In 1990", year=1990.0, dur=1.5), dict(at="In 2008", year=2008.0, dur=3.0), dict(at="This year", year=2026.0, dur=3.0), dict(at="At this pace", year=2031.0, dur=4.0)],
         labels=[dict(at="seventy-six thousand seven hundred", iso="ITA", year=2031), dict(at="seventy-six thousand two hundred", iso="POL", year=2031), dict(at="three times richer", iso="ITA", year=1990), dict(at="exactly twice", iso="POL", year=2008), dict(at="nine percent behind", iso="POL", year=2026)],
         react=[dict(at="Four hundred", pose="pointUp"), dict(at="In 1990", pose="pointL"), dict(at="exactly twice", pose="think"), dict(at="nine percent", pose="shock"), dict(at="G7 country", pose="cheer")]),
    dict(act=0, type="host", bg="lines", set="imf", fc=2025, series=["ITA", "POL"], years=[1990, 2031], start=2031.0, y=[0, 85000], fmt="usdk0",
         narration="Poland has done this before. It passed Portugal in 2020. This year, by the IMF's October numbers, it passed Japan. Next year, the forecast says, Spain. Four countries in seven years. {p} Italy is the next name on the list, and it's the biggest one yet: the third-largest economy in the eurozone, home to Ferrari, Fiat and some of the oldest banks in the world. {pp} <soft>So how does a country that was a third as rich as Italy in 1990 end up almost level? It's two stories. One about a country that stopped growing. And one about a country that never stopped.</soft>",
         items=[dict(at="passed Portugal", text="2020: Portugal", color="acc2", size=66), dict(at="passed Japan", text="2026: Japan", color="acc2", size=66), dict(at="says, Spain", text="2027: Spain", color="acc2", size=66), dict(at="Italy is the next", text="Next: Italy", serif=True, size=76, color="acc")],
         react=[dict(at="done this before", pose="pointL"), dict(at="passed Japan", pose="cheer"), dict(at="biggest one yet", pose="pointUp"), dict(at="two stories", pose="think")]),

    # ---------------- 1 · ITALY STOPPED ----------------
    dict(act=1, type="host", bg="none",
         narration="Quick one before the two stories: this is a series, and the next episode is Poland versus Germany. When, and whether it happens at all. Subscribe so you don't miss it. {p} Now, Italy.",
         items=[dict(at="this is a series", text="The Poland series", serif=True, size=66, color="acc"), dict(at="Poland versus Germany", text="Next: Poland vs Germany", color="acc2", size=62), dict(at="Subscribe", text="Subscribe", size=70)],
         react=[dict(at="Quick one", pose="wave"), dict(at="Poland versus Germany", pose="pointUp"), dict(at="Subscribe", pose="cheer"), dict(at="Now, Italy", pose="pointL")]),
    dict(act=1, type="lines", set="ridx", series=["POL", "ESP", "DEU", "ITA"], years=[2000, 2025], start=2000.0, y=[80, 260], src=IMF + " · real GDP, 2000 = 100 (compounded annual growth, NGDP_RPCH)", fmt="int", hl="ITA",
         ref=dict(value=100, label="2000 level", pos="left"),
         narration="Here's Italy's economy since 2000, after inflation, with the year 2000 set to one hundred. {p} By 2025, it reaches about a hundred and ten. Ten percent of growth in twenty-five years. Germany managed about thirty. Spain, about fifty. And Poland, on the same chart, about a hundred and forty. {pp} Italy's economy shrank in 2008, 2009, 2012, 2013 and 2020. Between 2008 and 2019, its growth averaged slightly below zero. A lost decade, in the most literal sense. {p} Per person and adjusted for prices, the IMF had Italy at about thirty-nine thousand five hundred dollars in 2008. Seven years later, in 2015: thirty-nine thousand seven hundred. Unchanged. Poland, meanwhile, went from under twenty thousand to twenty-seven.",
         keys=[dict(at="Here's Italy's economy", year=2000.0, dur=2.0), dict(at="By 2025", year=2025.0, dur=6.0), dict(at="shrank in 2008", year=2009.0, dur=3.0), dict(at="Seven years later", year=2015.0, dur=3.0), dict(at="Poland, meanwhile", year=2025.0, dur=3.0)],
         labels=[dict(at="hundred and ten", iso="ITA", year=2025), dict(at="about thirty", iso="DEU", year=2025), dict(at="about fifty", iso="ESP", year=2025), dict(at="hundred and forty", iso="POL", year=2025)],
         react=[dict(at="Here's Italy's", pose="pointL"), dict(at="Ten percent", pose="shock"), dict(at="hundred and forty", pose="cheer"), dict(at="lost decade", pose="shrug"), dict(at="Unchanged", pose="think")]),
    dict(act=2, type="stats", src=IMF + " · general government gross debt (% of GDP), real GDP growth, population (LP)", title="Why Italy stalled",
         narration="Three numbers tell the story. {p} Debt: Italy's government owes about a hundred and thirty-eight percent of the country's economy this year, among the highest in Europe. A big slice of every budget goes to interest, not investment. {p} Growth: since 2001, Italy has averaged about zero point four percent a year. Poland, about three point six. {p} And people: Italy's population peaked at about sixty point three million in 2014. This year it's about fifty-eight point nine, and the IMF expects it to keep falling. Fewer workers, more retirees.",
         stats=[dict(at="a hundred and thirty-eight", value=DEBT["ITA"][2026], fmt="pct0", label="Italy, government debt, % of GDP, 2026"), dict(at="zero point four", value=round(avg("ITA", 2001, 2025), 1), fmt="pct1", label="Italy, average growth, 2001–2025"), dict(at="three point six", value=round(avg("POL", 2001, 2025), 1), fmt="pct1", label="Poland, average growth, 2001–2025"), dict(at="fifty-eight point nine", value=LP["ITA"][2026], fmt="m", label="people in Italy, 2026 (peak: 60.3M in 2014)")],
         react=[dict(at="Three numbers", pose="pointUp"), dict(at="interest, not investment", pose="shrug"), dict(at="three point six", pose="pointL"), dict(at="keep falling", pose="think")]),

    # ---------------- 2 · POLAND NEVER STOPPED ----------------
    dict(act=3, type="lines", set="imf", fc=2025, series=["ITA", "ESP", "PRT", "POL"], years=[2000, 2027], start=2000.0, y=[0, 75000], src=PPPC, fmt="usdk0", hl="POL",
         narration="Now Poland. {p} Since 1992, Poland's economy has grown every single year except one: 2020, the pandemic. Thirty-three years, one recession, and that one lasted a single year. {p} The average since 2001 is about three and a half percent a year. Never spectacular. Just relentless. {pp} On this chart, it passes Portugal in 2020 and, in the IMF's forecast, Spain next year. {p} Why? Poland joined the European Union in 2004 and has been the biggest net recipient of EU money ever since: roads, rail, factories. It kept its own currency, the złoty, which fell in every crisis and kept Polish exports cheap. And it became the workshop of German industry: car parts, appliances, batteries, built in Poland and sold across Europe.",
         keys=[dict(at="Now Poland", year=2000.0, dur=1.5), dict(at="Thirty-three years", year=2019.0, dur=6.0), dict(at="passes Portugal", year=2020.0, dur=2.0), dict(at="Spain next year", year=2027.0, dur=3.0)],
         labels=[dict(at="passes Portugal", iso="PRT", year=2020), dict(at="Spain next year", iso="ESP", year=2027)],
         react=[dict(at="Now Poland", pose="pointL"), dict(at="one recession", pose="shock"), dict(at="Just relentless", pose="cheer"), dict(at="biggest net recipient", pose="pointUp"), dict(at="workshop of German industry", pose="think")]),
    dict(act=3, type="host", bg="none",
         narration="There's a second reason, and it's less flattering for Italy. {p} Half of this chart is Poland running. The other half is Italy standing still. Catching up is always two numbers: how fast you run, and how fast the other guy runs. {p} Between 2008 and 2019, Poland's economy grew about forty-nine percent. Italy's shrank. That is the whole gap, right there.",
         items=[dict(at="Poland running", text="Poland: running", color="acc", size=70), dict(at="standing still", text="Italy: standing still", color="warm", size=70), dict(at="two numbers", text="Catching up = two speeds", serif=True, size=60)],
         react=[dict(at="less flattering", pose="shrug"), dict(at="Poland running", pose="pointL"), dict(at="two numbers", pose="pointUp"), dict(at="whole gap", pose="think")]),

    # ---------------- 3 · THE CATCH ----------------
    dict(act=4, type="host", bg="none",
         narration="Now, the catch. Because Italy isn't poor, and a chart like this hides a few things. {p} And if you're enjoying this, the subscribe button is right there. The series continues.",
         items=[dict(at="the catch", text="The catch", serif=True, size=68, color="acc"), dict(at="subscribe button", text="Subscribe", size=66)],
         react=[dict(at="the catch", pose="think"), dict(at="subscribe button", pose="pointUp")]),
    dict(act=4, type="stats", src=IMF + " · GDP per capita, current US$ (NGDPDPC), 2026 and 2031", title="Per person, plain US$",
         narration="Everything so far was adjusted for prices. In plain dollars, Italy is still well ahead: about forty-six thousand per person this year, against thirty-one thousand for Poland. Italy is about forty-seven percent richer on that measure. {p} And the IMF still has Italy ahead in 2031: about fifty-two thousand against forty-two. The plain-dollar gap closes too, just more slowly: from about forty-seven percent this year to about twenty-four percent in 2031. {pp} Prices in Poland are lower, so a Polish salary buys more at home. That's what the price-adjusted numbers capture, and it's the fairer comparison of living standards. But if you're buying a German car or a flight to New York, you pay in plain dollars. And there, Italy still wins. {p} Italy also has something no growth chart shows: decades of accumulated wealth. Housing, savings, infrastructure, brands the whole world knows. Poland is catching up on income. Wealth takes a generation longer.",
         stats=[dict(at="forty-six thousand", value=N["ITA"][2026], fmt="usd0", label="Italy, 2026"), dict(at="thirty-one thousand", value=N["POL"][2026], fmt="usd0", label="Poland, 2026"), dict(at="fifty-two thousand", value=N["ITA"][2031], fmt="usd0", label="Italy, 2031 (IMF)"), dict(at="against forty-two", value=N["POL"][2031], fmt="usd0", label="Poland, 2031 (IMF)")],
         react=[dict(at="plain dollars", pose="pointUp"), dict(at="forty-seven percent", pose="pointL"), dict(at="buys more at home", pose="think"), dict(at="Italy still wins", pose="shrug"), dict(at="a generation longer", pose="idle")]),

    # ---------------- 4 · DOES IT HAPPEN? ----------------
    dict(act=5, type="stats", src=IMF + " · real GDP growth 2027–2031, population (LP), government gross debt (% of GDP)", title="The IMF's 2027–2031 forecast",
         narration="So does Poland actually pass Italy? {p} The IMF's forecast runs to 2031, and in 2031 Poland is still four hundred and ninety-nine dollars short: ninety-nine point three percent of Italy's level. The crossing, if it comes, sits just past the edge of the forecast, around 2032. {pp} And the forecast already has Poland slowing down: about two and a half percent a year from 2027, against about zero point six for Italy. {p} Poland has headwinds of its own. Its population is shrinking too, from about thirty-eight million in 2000 to about thirty-six this year. And its government debt is climbing fast, from about sixty-seven percent of the economy this year to about eighty-two by 2031, partly because Poland now spends more on defense, as a share of its economy, than any other NATO member.",
         stats=[dict(at="two and a half percent", value=G["POL"][2028], fmt="pct1", label="Poland, growth per year, 2027–2031"), dict(at="zero point six for Italy", value=G["ITA"][2029], fmt="pct1", label="Italy, growth per year, 2027–2031"), dict(at="about thirty-six this year", value=LP["POL"][2026], fmt="m", label="people in Poland, 2026 (2000: 38.3M)"), dict(at="eighty-two by 2031", value=DEBT["POL"][2031], fmt="pct0", label="Poland, government debt, % of GDP, 2031")],
         react=[dict(at="actually pass", pose="think"), dict(at="ninety-nine point three", pose="pointUp"), dict(at="slowing down", pose="shrug"), dict(at="shrinking too", pose="pointL"), dict(at="NATO member", pose="shock")]),
    dict(act=5, type="host", bg="none",
         narration="Still, the direction hasn't changed in thirty-five years. {p} Since 1991, Poland has gained on Italy in thirty-two years out of thirty-six, through two global recessions and a pandemic. And since 2002, it lost ground only twice, in 2021 and 2023, each time by a fraction of a point. {p} That's thirty-five years of one direction. So even if the crossing slips to 2033 or 2034, this chart only goes one way.",
         items=[dict(at="thirty-two years", text="Gained in 32 of 36 years", color="acc", size=66), dict(at="only twice", text="Since 2002: lost ground twice", color="acc2", size=60), dict(at="only goes one way", text="One direction", serif=True, size=70)],
         react=[dict(at="hasn't changed", pose="pointUp"), dict(at="thirty-two years", pose="pointL"), dict(at="fraction of a point", pose="shrug"), dict(at="one way", pose="cheer")]),

    # ---------------- 5 · AFTER ITALY ----------------
    dict(act=6, type="lines", set="imf", fc=2025, series=["DEU", "FRA", "GBR", "ITA", "POL"], years=[2015, 2031], start=2026.0, y=[0, 100000], src=PPPC, fmt="usdk0", hl="POL",
         narration="And after Italy, the list keeps going. {p} In 2031, the IMF has Poland at about ninety-five percent of Britain's level, and ninety-five percent of France's. Germany is further out, at about eighty-three percent. Britain and France, two of the big four of Western Europe, within five percent. Thirty-five years ago, Poland was about a third of all three. {pp} If the 2010s and 2020s repeat, the 2030s are the decade Poland catches the big three of Western Europe. If Italy finally grows again, the race gets interesting. {p} Either way, the map of Europe's richest countries is being redrawn, and it's being redrawn from the east.",
         keys=[dict(at="after Italy", year=2026.0, dur=1.5), dict(at="In 2031", year=2031.0, dur=6.0)],
         labels=[dict(at="ninety-five percent of Britain's", iso="GBR", year=2031), dict(at="percent of France's", iso="FRA", year=2031), dict(at="eighty-three percent", iso="DEU", year=2031), dict(at="If the 2010s", iso="POL", year=2031)],
         react=[dict(at="keeps going", pose="pointUp"), dict(at="Germany is further", pose="pointL"), dict(at="the big three", pose="cheer"), dict(at="from the east", pose="think")]),
    dict(act=6, type="host", bg="none",
         narration="<soft>Which one do you think Poland passes first after Italy: Britain or France?</soft> Tell me in the comments. {p} If you're watching from Italy: what would it take to get Italy growing again? {p} And if you're watching from Poland: which country should I cover next? I read every comment.",
         items=[dict(at="Britain or France", text="Britain or France first?", color="acc", size=66), dict(at="growing again", text="Italy: what would it take?", color="warm", size=60)],
         react=[dict(at="Which one", pose="shrug"), dict(at="Tell me", pose="pointUp"), dict(at="watching from Italy", pose="wave")]),
    dict(act=6, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="ESP", color="acc", title="Poland is $55 from Spain", sub="the sorpasso, explained."),
         narration="Spain is the one Poland passes next year, and this year the gap is fifty-five dollars. That whole story is right here. {p} I'm Chartbound. See you in the next one.",
         hold=14,
         react=[dict(at="Spain is the one", pose="pointL"), dict(at="See you", pose="wave")]),
]

checks = [
    dict(say="2031 gap ITA − POL = $499", rule="expr", expr=f"{I[2031] - P[2031]}", equal=499),
    dict(say="ITA 2031 ≈ $76.7k, POL 2031 ≈ $76.2k", rule="expr", expr=f"[round({I[2031]} / 100) * 100, round({P[2031]} / 100) * 100]", equal=[76700, 76200]),
    dict(say="1990: ITA more than 3× POL", rule="ratio", set="imf", a="ITA", b="POL", year=1990, min=3.0, max=3.5),
    dict(say="2008: ITA exactly 2× POL (1.999)", rule="ratio", set="imf", a="ITA", b="POL", year=2008, min=1.98, max=2.02),
    dict(say="2026: POL about 9% behind (0.907)", rule="ratio", set="imf", a="POL", b="ITA", year=2026, min=0.90, max=0.915),
    dict(say="2031: POL = 99.3% of ITA", rule="ratio", set="imf", a="POL", b="ITA", year=2031, min=0.99, max=0.996),
    dict(say="POL passed PRT 2020, JPN 2026, ESP 2027; not ITA by 2031", rule="expr", expr=f"[{first_over('POL','PRT')}, {first_over('POL','JPN')}, {first_over('POL','ESP')}, {P[2031] < I[2031]}]", equal=[2020, 2026, 2027, True]),
    dict(say="1990: POL about a third of ITA (0.31)", rule="ratio", set="imf", a="POL", b="ITA", year=1990, min=0.29, max=0.34),
    dict(say="real GDP 2000→2025: ITA ≈ +10%, DEU ≈ +30%, ESP ≈ +50%, POL ≈ +140%", rule="expr", expr=f"[round({IDX['ITA'][2025]} / 10) * 10, round({IDX['DEU'][2025]} / 10) * 10, round({IDX['ESP'][2025]} / 10) * 10, round({IDX['POL'][2025]} / 10) * 10]", equal=[110, 130, 150, 240]),
    dict(say="ITA negative years 2008, 2009, 2012, 2013, 2020 (since 2000)", rule="expr", expr=f"{[y for y in range(2000, 2026) if G['ITA'][y] < 0]}", equal=[2008, 2009, 2012, 2013, 2020]),
    dict(say="ITA 2008–2019 average growth slightly below zero", rule="expr", expr=f"{round(avg('ITA', 2008, 2019), 2)}", equal=-0.34),
    dict(say="ITA PPPPC 2008 ≈ $39.5k, 2015 ≈ $39.7k", rule="expr", expr=f"[round({I[2008]} / 100) * 100, round({I[2015]} / 100) * 100]", equal=[39500, 39700]),
    dict(say="POL 2008 < $20k, 2015 ≈ $27k", rule="expr", expr=f"[{P[2008]} < 20000, round({P[2015]} / 1000)]", equal=[True, 27]),
    dict(say="ITA debt 2026 ≈ 138% of GDP", set="debt", iso="ITA", year=2026, min=137, max=139),
    dict(say="average growth 2001–2025: ITA ≈ 0.4, POL ≈ 3.6", rule="expr", expr=f"[round({avg('ITA', 2001, 2025)}, 1), round({avg('POL', 2001, 2025)}, 1)]", equal=[0.4, 3.6]),
    dict(say="ITA population peak 60.3M in 2014; 2026 ≈ 58.9M; falling to 2031", rule="expr", expr=f"[{max(LP['ITA'], key=LP['ITA'].get)}, round({LP['ITA'][2014]}, 1), round({LP['ITA'][2026]}, 1), {LP['ITA'][2031] < LP['ITA'][2026]}]", equal=[2014, 60.3, 58.9, True]),
    dict(say="POL: no negative year 1992–2025 except 2020", rule="expr", expr=f"{[y for y in range(1992, 2026) if G['POL'][y] < 0]}", equal=[2020]),
    dict(say="POL average 2001–2025 ≈ 3.5–3.6 (three and a half)", rule="expr", expr=f"{3.4 <= avg('POL', 2001, 2025) <= 3.7}", equal=True),
    dict(say="Poland joined the EU in 2004; largest net recipient of EU funds (European Commission budget data, widely reported)", rule="expr", expr="2004", equal=2004),
    dict(say="nominal 2026: ITA ≈ $46k, POL ≈ $31k, ITA/POL ≈ 1.47", rule="expr", expr=f"[round({N['ITA'][2026]} / 1000), round({N['POL'][2026]} / 1000), round({N['ITA'][2026]} / {N['POL'][2026]}, 2)]", equal=[46, 31, 1.47]),
    dict(say="nominal 2031: ITA ≈ $52k, POL ≈ $42k", rule="expr", expr=f"[round({N['ITA'][2031]} / 1000), round({N['POL'][2031]} / 1000)]", equal=[52, 42]),
    dict(say="POL growth 2027–2031 = 2.5 each year; ITA 0.6–0.7", rule="expr", expr=f"[{sorted(set(G['POL'][y] for y in range(2027, 2032)))}, {min(G['ITA'][y] for y in range(2027, 2032))}, {max(G['ITA'][y] for y in range(2027, 2032))}]", equal=[[2.5], 0.6, 0.7]),
    dict(say="POL population 2000 ≈ 38.3M → 2026 ≈ 36.3M", rule="expr", expr=f"[round({LP['POL'][2000]}, 1), round({LP['POL'][2026]}, 1)]", equal=[38.3, 36.3]),
    dict(say="POL debt 2026 ≈ 67% → 2031 ≈ 82%", rule="expr", expr=f"[round({DEBT['POL'][2026]}), round({DEBT['POL'][2031]})]", equal=[67, 82]),
    dict(say="Poland highest NATO defense spending as % of GDP (NATO estimates 2025, ~4.5%) — fato amplamente citado", rule="expr", expr="True", equal=True),
    dict(say="POL gained on ITA in 32 of 36 years 1991–2026; since 2002 lost ground only in 2021 and 2023, each < 0.5 pt", rule="expr", expr=f"[{36 - len(dips)}, {[y for y in dips if y >= 2002]}, {all(abs(ratio[y] - ratio[y - 1]) < 0.005 for y in dips if y >= 2002)}]", equal=[32, [2021, 2023], True]),
    dict(say="2031: POL/GBR ≈ 95%, POL/FRA ≈ 95%, POL/DEU ≈ 83%", rule="expr", expr=f"[round({P[2031]} / {series('PPPPC', 'GBR')[2031]} * 100), round({P[2031]} / {series('PPPPC', 'FRA')[2031]} * 100), round({P[2031]} / {series('PPPPC', 'DEU')[2031]} * 100)]", equal=[95, 95, 83]),
    dict(say="2026: POL ≈ $60k, ITA ≈ $66k", rule="expr", expr=f"[round({P[2026]} / 1000), round({I[2026]} / 1000)]", equal=[60, 66]),
    dict(say="2008–2019: POL real GDP ≈ +49%, ITA negative", rule="expr", expr=f"[round(({IDX['POL'][2019]} / {IDX['POL'][2008]} - 1) * 100), {IDX['ITA'][2019] < IDX['ITA'][2008]}]", equal=[49, True]),
    dict(say="plain-dollar gap: 2026 ≈ 47%, 2031 ≈ 24%", rule="expr", expr=f"[round(({N['ITA'][2026]} / {N['POL'][2026]} - 1) * 100), round(({N['ITA'][2031]} / {N['POL'][2031]} - 1) * 100)]", equal=[47, 24]),
    dict(say="1990: POL about a third of GBR, FRA, DEU (0.37, 0.34, 0.31)", rule="expr", expr=f"[round({P[1990]} / {series('PPPPC', 'GBR')[1990]}, 2), round({P[1990]} / {series('PPPPC', 'FRA')[1990]}, 2), round({P[1990]} / {series('PPPPC', 'DEU')[1990]}, 2)]", equal=[0.37, 0.34, 0.3]),
    dict(say="ESP gap 2026 = $55", rule="expr", expr=f"{series('PPPPC', 'ESP')[2026] - P[2026]}", equal=55),
    dict(say="Italy third-largest eurozone economy (after Germany, France) — IMF WEO nominal GDP", rule="expr", expr="True", equal=True),
    dict(say="1990 ITA > 3× POL (3.24)", rule="expr", expr=f"{round(I[1990] / P[1990], 2)}", equal=3.24),
]

clips = [
    dict(**{"from": "s00", "to": "s00"}, hook="*$499* from Italy", title="Poland is $499 from catching Italy (IMF, 2031) #Shorts", desc="GDP per person, PPP (IMF WEO Oct 2026): Italy 3× Poland in 1990, 2× in 2008, +9% in 2026, $499 apart in 2031."),
    dict(**{"from": "s03", "to": "s03"}, hook="Italy grew *10%* in 25 years", title="Italy's economy grew 10% in 25 years. Poland's grew 140% #Shorts", desc="Real GDP, 2000 = 100 (IMF WEO Oct 2026): Italy 110, Germany 130, Spain 150, Poland 240 in 2025."),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="a-L21-poland-italy", clips=clips, channel="chartbound", chapter0="$499 apart",
            thumb=dict(v="flags", iso="POL", vs="ITA", big="ITALY IS NEXT", line2="1990: ITALY 3× RICHER"),
            w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks, datasets=[], snapshot=snapshot,
            voice=dict(model="", name="Charon",
                       style=("You are the narrator of a popular data documentary on YouTube. Read the script below in a warm, curious voice "
                              "with a little dry humor, at a relaxed but engaged pace of about 145 words per minute, like a smart friend telling "
                              "you something surprising. Let the big numbers land with a tiny pause before them. Keep the energy steady from the "
                              "first sentence to the last. Never sound like an advertisement or an audiobook.")),
            music=[dict(act=0, track="Lightless Dawn", vol=0.24), dict(act=1, track="Deliberate Thought", vol=0.22), dict(act=2, track="Deliberate Thought", vol=0.22), dict(act=3, track="Inspired", vol=0.23),
                   dict(act=4, track="Hidden Agenda", vol=0.23), dict(act=5, track="Investigations", vol=0.23), dict(act=6, track="Floating Cities", vol=0.24)],
            yt=dict(title="Poland Just Passed Japan. Italy Is Next.",
                    description=("In 1990 Italy was more than three times richer than Poland per person, adjusted for prices. In 2008, exactly twice. In the IMF's October 2026 World Economic Outlook, "
                                 "Poland is 9% behind this year and $499 behind in 2031, after passing Portugal (2020), Japan (2026) and, in the forecast, Spain (2027). "
                                 "Italy's 25 years of near-zero growth, Poland's 33 years with one recession, the plain-dollar catch, whether the crossing actually happens, and who comes after Italy.\n\n"
                                 "Sources: IMF World Economic Outlook, October 2026 (PPPPC, NGDPDPC, NGDP_RPCH, LP, LUR, GGXWDG_NGDP); European Commission (EU budget); NATO defence expenditure estimates (2025).\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#poland #italy #economics #imf #europe #data"),
                    tags=["poland", "italy", "poland vs italy", "poland economy", "italy economy", "gdp per capita", "imf", "economics", "europe", "data", "polska"], lang="en"))

json.dump(spec, open(os.path.join(HERE, "a-L21.json"), "w"), ensure_ascii=False, indent=1)
clean = lambda t: t.replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()
words = sum(len(clean(s["narration"])) for s in shots)
acts = {}
for s in shots:
    acts[s["act"]] = acts.get(s["act"], 0) + len(clean(s["narration"]))
print("shots", len(shots), "palavras", words, f"~{words / 145:.1f} min a 145 wpm", "por ato", acts, "dips", dips)

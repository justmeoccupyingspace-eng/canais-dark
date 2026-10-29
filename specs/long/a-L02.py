"""Gera specs/long/a-L02.json — Chartbound longo #2: "South Korea's Scariest Number Just Went Up".
Mesmas convenções do a-L01 ({p}, {pp}, <soft>, cues "at"). Dados: World Bank (API) + pontos citados (KOSTAT etc.) em snapshot."""
import json, os

ACTS = ["Cold open", "Stop at two", "Why no babies", "The math", "The rebound", "Is it enough?"]
TFR = "World Bank · fertility rate, births per woman (2025: Statistics Korea)"
KOSTAT = "Statistics Korea (KOSTAT), via Reuters / Korea Times"

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="bars", mode="abs", set="births", iso="KOR", years=[1960, 2025], start=1969.0, fmt="k0", src="World Bank (birth rate × population) · Statistics Korea (2025)",
         narration="In 1970, about a million babies were born in South Korea. {p} In 2023? {pp} About two hundred and thirty thousand.",
         keys=[dict(at="In 2023?", year=2023.0, dur=3.2)],
         labels=[dict(at="a million", year=1970), dict(at="two hundred", year=2023)],
         react=[dict(at="a million", pose="pointL"), dict(at="two hundred", pose="shock")]),
    dict(act=0, type="lines", set="tfr", series=["KOR"], years=[1960, 2025], start=2023.0, src=TFR, fmt="dec2", y=[0, 6.5],
         narration="That year, the average Korean woman was expected to have zero point seven two children in her lifetime. {p} The lowest of any country on Earth. {pp} To keep a population stable, you need about two point one.",
         labels=[dict(at="zero point seven two", iso="KOR", year=2023)],
         refs=[dict(at="two point one", value=2.1, label="2.1 = population stays flat")],
         push=dict(at="lowest of any"),
         react=[dict(at="zero point seven two", pose="shock"), dict(at="two point one", pose="pointL")]),
    dict(act=0, type="host", bg="lines", set="tfr", series=["KOR"], years=[1960, 2025], start=2023.0, fmt="dec2", y=[0, 6.5],
         narration="So Korea was having about a third of the babies it needs just to stay the same size. {p} And then, last year, something nobody expected happened. {pp} The number went up. {p} Is Korea's baby crisis over? <soft>To answer that, you need to see the scariest chart in economics.</soft>",
         items=[dict(at="a third", text="0.72 ≈ a third of 2.1"), dict(at="went up", text="Then it went up.", color="acc"), dict(at="crisis over", text="Crisis over?", serif=True, size=72)],
         react=[dict(at="a third", pose="shrug"), dict(at="nobody expected", pose="think", lean=1), dict(at="went up", pose="shock"), dict(at="scariest chart", pose="pointL")]),

    # ---------------- 1 · STOP AT TWO ----------------
    dict(act=1, type="globe", src="World Bank · fertility rate; GDP per capita (current US$)",
         narration="Korea's story actually starts with too many babies. {p} In 1960, the average woman had about six children, {p} and South Korea was one of the poorest countries on Earth, poorer than most of Africa at the time. {p} The government decided families were simply too big.",
         view=dict(lon=127.8, lat=36.4, zoom=9.0), hl=["KOR"],
         stats=[dict(at="about six", set="tfr", iso="KOR", year=1960, fmt="dec1", label="children per woman, 1960", until="one of the poorest"),
                dict(at="one of the poorest", set="gdppc", iso="KOR", year=1960, fmt="usd0", label="GDP per person, 1960")],
         react=[dict(at="too many babies", pose="shrug"), dict(at="about six", pose="shock"), dict(at="poorest", pose="idle", nod=1)]),
    dict(act=1, type="list", src="Population Reference Bureau · Korean family-planning posters, 1974 and 1980s",
         title="The campaign",
         narration="In 1962, Seoul launched one of the most successful family-planning campaigns in history. {p} The posters of the seventies said: sons or daughters, have two, and raise them well. {p} By the eighties, the message was blunter: even two children are too many for our crowded country.",
         items=[dict(at="In 1962", kind="bullet", text="1962 · national family planning"),
                dict(at="sons or daughters", kind="quote", text="“Sons or daughters, have two and raise them well.”", sub="poster, 1974"),
                dict(at="even two", kind="quote", text="“Even two children are too many.”", sub="poster, 1980s")],
         react=[dict(at="In 1962", pose="pointL"), dict(at="sons or daughters", pose="idle"), dict(at="even two", pose="shock")]),
    dict(act=1, type="lines", set="tfr", series=["KOR"], years=[1960, 2025], start=1960.0, src=TFR, fmt="dec2", y=[0, 6.5], wm="tr",
         ref=dict(value=2.1, label="2.1 = population stays flat"),
         narration="It worked. {p} Too well. {p} By 1984, fertility was down to one point seven four, below replacement. {p} And it never came back. {p} One point five by the year 2000. {p} Below one in 2018. {p} Zero point seven two in 2023.",
         keys=[dict(at="It worked", year=1984.0, dur=4.5), dict(at="never came back", year=2000.0, dur=2.5), dict(at="Below one", year=2018.0, dur=2.0), dict(at="Zero point seven", year=2023.0, dur=1.5)],
         labels=[dict(at="one point seven four", iso="KOR", year=1984), dict(at="One point five", iso="KOR", year=2000), dict(at="Below one", iso="KOR", year=2018), dict(at="Zero point seven", iso="KOR", year=2023)],
         react=[dict(at="Too well", pose="shrug"), dict(at="never came back", pose="pointL"), dict(at="Zero point seven", pose="shock")]),
    dict(act=1, type="host", bg="lines", set="tfr", series=["KOR"], years=[1960, 2025], start=2023.0, fmt="dec2", y=[0, 6.5],
         narration="For decades, Korea told families to have fewer children. {p} Since 2006, it has been paying them to have more. {p} For almost twenty years, the line didn't care.",
         items=[dict(at="fewer children", text="1962–1990s: have fewer"), dict(at="paying them", text="2006–: please, have more", color="acc"), dict(at="didn't care", text="The line didn't care.", serif=True, size=70)],
         react=[dict(at="fewer children", pose="pointUp"), dict(at="paying them", pose="cheer"), dict(at="didn't care", pose="shrug")]),

    # ---------------- 2 · WHY NO BABIES ----------------
    dict(act=2, type="cards", n=1, src=KOSTAT + " · marriages 2022, births outside marriage 2023",
         cards=[dict(t="Marriage", s="almost all babies"), dict(t="Money", s="the race to compete"), dict(t="Time", s="work and home")],
         narration="So why aren't Koreans having kids? {p} Start with marriage. In Korea, more than ninety-five percent of babies are born to married couples. {p} And marriage is collapsing. In 2022, about a hundred and ninety-two thousand couples got married, {p} forty-two percent fewer than a decade earlier.",
         stat=dict(at="a hundred and ninety-two", value=192500, fmt="int", label="marriages in 2022 · −42% in ten years"),
         chips=[dict(at="ninety-five percent", text="95%+ of births: married parents")],
         react=[dict(at="why aren't", pose="think"), dict(at="collapsing", pose="shock"), dict(at="forty-two percent", pose="idle", nod=1)]),
    dict(act=2, type="cards", n=2, src="Statistics Korea, private education survey 2024 · World Bank exchange rate",
         cards=[dict(t="Marriage", s="almost all babies"), dict(t="Money", s="the race to compete"), dict(t="Time", s="work and home")],
         narration="Then there's the cost of raising a child to compete. {p} Korean parents spend a fortune on after-school cram academies, called hagwons. {p} In 2024, private education spending hit a record twenty-nine point two trillion won. {p} That's more than twenty billion dollars, for a shrinking number of students.",
         stat=dict(at="twenty-nine point two", value=29.2, fmt="krwT", label="private tutoring, 2024 · record"),
         chips=[dict(at="hagwons", text="학원 · hagwon")],
         react=[dict(at="fortune", pose="shrug"), dict(at="twenty-nine point two", pose="shock")]),
    dict(act=2, type="hbars", n=3, src="OECD · average annual hours worked per worker, 2025",
         cards=[dict(t="Marriage", s="almost all babies"), dict(t="Money", s="the race to compete"), dict(t="Time", s="work and home")],
         narration="And then there's time. {p} Koreans work about eighteen hundred and thirty hours a year, among the longest in the rich world, {p} and at home, most of the second shift still falls on women. {p} For a lot of young Korean women, it feels like a choice between a career and a child. {p} More and more, they choose the career.",
         bars=[dict(at="eighteen hundred", iso="KOR", value=1833, label="South Korea"), dict(at="among the longest", iso="DEU", value=1332, label="Germany")],
         kicker=dict(at="career and a child", text="career or child"),
         react=[dict(at="time", pose="think"), dict(at="second shift", pose="shrug"), dict(at="choose the career", pose="idle", nod=1)]),
    dict(act=2, type="globe", src="Statistics Korea · regional fertility 2023",
         narration="Seoul is where all of this peaks. {p} About half of all South Koreans live in the greater Seoul area, {p} and in 2023, Seoul's fertility rate was zero point five five. {pp} The capital is where Korea's future gets very, very small.",
         view=dict(lon=127.0, lat=37.4, zoom=22.0), hl=[], hl2=["KOR"],
         cities=[dict(at="Seoul is", name="Seoul", lon=126.98, lat=37.57)],
         stats=[dict(at="zero point five five", value=0.55, fmt="dec2", label="Seoul · births per woman, 2023")],
         react=[dict(at="Seoul is", pose="pointL"), dict(at="zero point five five", pose="shock")]),

    # ---------------- 3 · THE MATH ----------------
    dict(act=3, type="people", tfr=0.72, src="Generation ratio ≈ fertility ÷ 2",
         narration="Here's why demographers call this the scariest chart in economics. {p} Take a hundred Korean adults. At zero point seven two, they have about thirty-six children between them. {p} Those thirty-six have about thirteen. {pp} In two generations, a hundred becomes thirteen.",
         gens=[dict(at="a hundred Korean", n=100, label="adults"), dict(at="thirty-six children", n=36, label="children"), dict(at="about thirteen", n=13, label="grandchildren")],
         push=dict(at="a hundred becomes"),
         react=[dict(at="scariest", pose="think"), dict(at="thirty-six", pose="pointL"), dict(at="a hundred becomes", pose="shock")]),
    dict(act=3, type="duel", src=KOSTAT + " · 2025",
         title="South Korea, 2025",
         left=dict(label="Deaths", value=363389, color="warm"), right=dict(label="Births", value=254457, color="acc2"), fmt="int",
         narration="And it's not a forecast. It's already happening. {p} Since 2020, more Koreans have died every year than were born. {p} In 2025: about three hundred and sixty-three thousand deaths, {p} and two hundred and fifty-four thousand births.",
         cues=[dict(at="three hundred and sixty-three", show="a"), dict(at="two hundred and fifty-four", show="b")],
         badge="−109,000",
         react=[dict(at="already happening", pose="idle", lean=1), dict(at="deaths", pose="shock"), dict(at="births", pose="idle")]),
    dict(act=3, type="lines", set="pop", series=["KOR"], years=[1960, 2072], start=1960.0, fc=2024, src="World Bank (to 2024) · Statistics Korea projection (2072)", fmt="mil", y=[0, 60e6],
         narration="The official projection? {p} Fifty-one point seven million people today. {p} Thirty-six point two million by 2072. {p} And almost half of them would be sixty-five or older.",
         keys=[dict(at="The official", year=2024.0, dur=3.0), dict(at="Thirty-six point two", year=2072.0, dur=2.5)],
         labels=[dict(at="Fifty-one point seven", iso="KOR", year=2024), dict(at="Thirty-six point two", iso="KOR", year=2072)],
         kicker=dict(at="almost half", text="2072: 47.7% aged 65+"),
         react=[dict(at="Fifty-one", pose="pointL"), dict(at="Thirty-six point two", pose="shock"), dict(at="almost half", pose="idle", nod=1)]),
    dict(act=3, type="host", bg="none",
         narration="Think about what that means. {p} Fewer workers paying into pensions. Fewer soldiers. Fewer customers. {p} Schools closing, nursing homes opening. {pp} <soft>A whole country slowly turning into a retirement home.</soft>",
         items=[dict(at="Fewer workers", text="Fewer workers"), dict(at="Fewer soldiers", text="Fewer soldiers"), dict(at="Fewer customers", text="Fewer customers"), dict(at="retirement home", text="A country-sized retirement home", serif=True, size=60, color="acc")],
         react=[dict(at="Think about", pose="think"), dict(at="Schools closing", pose="shrug"), dict(at="retirement home", pose="idle", lean=1)]),

    # ---------------- 4 · THE REBOUND ----------------
    dict(act=4, type="lines", set="tfr", series=["KOR"], years=[2010, 2025], start=2023.0, src=TFR, fmt="dec2", y=[0.6, 1.4],
         narration="And then, the twist. {p} In 2024, Korea's fertility rate went up for the first time in nine years, to zero point seven five. {p} In 2025, it rose again, to zero point eight. {p} Births jumped almost seven percent, the biggest increase since 2007.",
         keys=[dict(at="In 2024", year=2024.0, dur=1.6), dict(at="rose again", year=2025.0, dur=1.6)],
         labels=[dict(at="zero point seven five", iso="KOR", year=2024), dict(at="zero point eight", iso="KOR", year=2025)],
         kicker=dict(at="almost seven", text="births +6.8% in 2025"),
         push=dict(at="the twist"),
         react=[dict(at="the twist", pose="shock"), dict(at="rose again", pose="cheer"), dict(at="almost seven", pose="cheer")]),
    dict(act=4, type="bars", mode="abs", set="births", iso="KOR", years=[1985, 2025], start=2025.0, fmt="k0", src="World Bank (birth rate × population) · KOSTAT marriages",
         narration="Why? {p} Partly weddings. Marriages delayed by the pandemic came back, up fifteen percent in 2024 and another eight percent in 2025. {p} And partly timing: Koreans born in the early nineties, a much bigger generation than the ones after it, {p} are now in their early thirties, the peak age for having a first child.",
         hl=[1991, 1996], hltext=dict(at="early nineties", text="born 1991–96"),
         chips=[dict(at="fifteen percent", text="marriages +14.8% (2024)"), dict(at="eight percent", text="+8.1% (2025)")],
         react=[dict(at="weddings", pose="cheer"), dict(at="early nineties", pose="pointL"), dict(at="peak age", pose="idle", nod=1)]),
    dict(act=4, type="list", src="Korean presidential office (June 2024) · Booyoung Group (Feb 2024) · World Bank exchange rate",
         title="All hands on deck",
         narration="And the country is now throwing everything at it. {p} In 2024, the president declared a national demographic emergency. {p} One construction company started paying employees a hundred million won for every baby. {p} That's about seventy thousand dollars.",
         items=[dict(at="demographic emergency", kind="bullet", text="2024 · “national demographic emergency”"),
                dict(at="a hundred million won", kind="bullet", text="₩100,000,000 per baby"),
                dict(at="seventy thousand", kind="title", text="≈ $70,000")],
         react=[dict(at="everything", pose="cheer"), dict(at="a hundred million", pose="shock"), dict(at="seventy thousand", pose="pointL")]),

    # ---------------- 5 · IS IT ENOUGH? ----------------
    dict(act=5, type="people", tfr=0.8, src="Generation ratio ≈ fertility ÷ 2",
         narration="So, is it over? {p} Run the math again at zero point eight. {p} A hundred adults have about forty children. Those forty have sixteen. {pp} Better than thirteen. {p} Still a country that shrinks by more than half, every single generation.",
         gens=[dict(at="A hundred adults", n=100, label="adults"), dict(at="forty children", n=40, label="children"), dict(at="have sixteen", n=16, label="grandchildren")],
         react=[dict(at="is it over", pose="think"), dict(at="Better than", pose="shrug"), dict(at="more than half", pose="idle", nod=1)]),
    dict(act=5, type="lines", set="tfr", series=["KOR", "JPN", "CHN", "ITA", "USA"], years=[1990, 2025], start=1990.0, src=TFR, fmt="dec2", y=[0.5, 2.8], hl="KOR",
         ref=dict(value=2.1, label="2.1"),
         narration="And Korea isn't alone. {p} Japan is at one point one five. {p} China, around one. Italy, one point one eight. {p} Even the United States is down to about one point six.",
         keys=[dict(at="Korea isn't alone", year=2024.0, dur=4.0)],
         labels=[dict(at="Japan is", iso="JPN", year=2024), dict(at="China", iso="CHN", year=2024), dict(at="Italy", iso="ITA", year=2024), dict(at="United States", iso="USA", year=2024)],
         react=[dict(at="isn't alone", pose="pointL"), dict(at="United States", pose="shock")]),
    dict(act=5, type="host", bg="lines", set="tfr", series=["KOR", "JPN", "CHN", "ITA", "USA"], years=[1990, 2025], start=2025.0, fmt="dec2", y=[0.5, 2.8],
         narration="Korea isn't an outlier. {p} It's a preview. {p} Most of the rich world is on the same line, just a few years behind. {pp} The question isn't whether other countries will face Korea's math. {p} It's whether anyone figures out how to beat it first.",
         items=[dict(at="outlier", text="Not an outlier."), dict(at="preview", text="A preview.", color="acc"), dict(at="beat it first", text="Who solves it first?", serif=True, size=70)],
         react=[dict(at="outlier", pose="idle"), dict(at="preview", pose="pointUp"), dict(at="beat it first", pose="think", lean=1)]),
    dict(act=5, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="101%", color="acc", title="Poland just passed Japan", sub="the other side of the same math"),
         narration="If you want to see what happens when a country runs this race from the other direction, watch our story on how Poland just passed Japan. {p} I'm Chartbound. See you in the next one.",
         hold=14,
         react=[dict(at="Poland just passed", pose="pointL"), dict(at="See you", pose="wave")]),
]

checks = [
    dict(say="about a million babies in 1970", set="births", iso="KOR", year=1970, approx=1.0e6, tol=0.08),
    dict(say="about 230 thousand in 2023", set="births", iso="KOR", year=2023, approx=230000, tol=0.06),
    dict(say="zero point seven two (2023)", set="tfr", iso="KOR", year=2023, approx=0.72, tol=0.01),
    dict(say="about six children in 1960", set="tfr", iso="KOR", year=1960, approx=6.0, tol=0.07),
    dict(say="one of the poorest countries (1960)", set="gdppc", iso="KOR", year=1960, max=300),
    dict(say="one point seven four by 1984", set="tfr", iso="KOR", year=1984, approx=1.74, tol=0.02),
    dict(say="one point five by 2000", set="tfr", iso="KOR", year=2000, approx=1.5, tol=0.04),
    dict(say="below one in 2018", set="tfr", iso="KOR", year=2018, max=0.999),
    dict(say="2024 zero point seven five", set="tfr", iso="KOR", year=2024, approx=0.75, tol=0.01),
    dict(say="first rise in nine years (last rise 2015)", rule="lastrise", set="tfr", iso="KOR", year=2024, equal=2015),
    dict(say="early-90s generation much bigger", rule="avgratio", set="births", iso="KOR", a1=1991, b1=1996, a2=2002, b2=2010, min=1.3),
    dict(say="29.2 trillion won > 20 billion dollars", rule="conv", set="fx", iso="KOR", year=2024, local=29.2e12, min=20e9, max=23e9),
    dict(say="100 million won ≈ 70 thousand dollars", rule="conv", set="fx", iso="KOR", year=2024, local=1e8, min=66000, max=76000),
    dict(say="Japan one point one five", set="tfr", iso="JPN", year=2024, approx=1.15, tol=0.01),
    dict(say="China around one", set="tfr", iso="CHN", year=2024, approx=1.0, tol=0.08),
    dict(say="Italy one point one eight", set="tfr", iso="ITA", year=2024, approx=1.18, tol=0.01),
    dict(say="US about one point six", set="tfr", iso="USA", year=2024, approx=1.6, tol=0.03),
    dict(say="51.7 million today", set="pop", iso="KOR", year=2024, approx=51.7e6, tol=0.01),
]

datasets = [
    dict(set="tfr", wb="SP.DYN.TFRT.IN", isos=["KOR", "JPN", "CHN", "ITA", "USA"], **{"from": 1960, "to": 2024}),
    dict(set="cbr", wb="SP.DYN.CBRT.IN", isos=["KOR"], **{"from": 1960, "to": 2024}),
    dict(set="pop", wb="SP.POP.TOTL", isos=["KOR"], **{"from": 1960, "to": 2024}),
    dict(set="births", derive="mul", a=["cbr", "KOR"], b=["pop", "KOR"], k=0.001, iso="KOR"),
    dict(set="gdppc", wb="NY.GDP.PCAP.CD", isos=["KOR"], **{"from": 1960, "to": 1965}),
    dict(set="fx", wb="PA.NUS.FCRF", isos=["KOR"], **{"from": 2020, "to": 2024}),
]
snapshot = [
    dict(set="tfr", iso="KOR", year=2025, value=0.80, src="Statistics Korea, 2025 births (Feb/Aug 2026)"),
    dict(set="births", iso="KOR", year=2025, value=254457, src="Statistics Korea 2025 (Reuters, 25/02/2026)"),
    dict(set="pop", iso="KOR", year=2072, value=36.2e6, src="Statistics Korea population projection, Dec 2023 (medium)"),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="a-L02-korea", channel="chartbound", chapter0="The lowest number on Earth", w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks,
            datasets=datasets, snapshot=snapshot,
            voice=dict(model="", name="Charon",
                       style=("You are the narrator of a popular data documentary on YouTube. Read the script below in a warm, curious voice "
                              "with a little dry humor, at a relaxed but engaged pace of about 145 words per minute, like a smart friend telling "
                              "you something surprising. Let the big numbers land with a tiny pause before them. Keep the energy steady from the "
                              "first sentence to the last. Never sound like an advertisement or an audiobook.")),
            music=[dict(act=0, track="Hidden Agenda", vol=0.24), dict(act=1, track="Investigations", vol=0.23), dict(act=2, track="Deliberate Thought", vol=0.22),
                   dict(act=3, track="Lightless Dawn", vol=0.26), dict(act=4, track="Reawakening", vol=0.23), dict(act=5, track="Lasting Hope", vol=0.24)],
            yt=dict(title="South Korea's Scariest Number Just Went Up",
                    description=("South Korea's fertility rate hit 0.72 in 2023, the lowest on Earth. Then, for the first time in nine years, it went up. "
                                 "How Korea went from six children per woman to under one, why young Koreans stopped having kids, the math that makes demographers panic, "
                                 "and whether the rebound is real.\n\n"
                                 "Sources: World Bank WDI (SP.DYN.TFRT.IN, SP.DYN.CBRT.IN, SP.POP.TOTL, NY.GDP.PCAP.CD, PA.NUS.FCRF); Statistics Korea (births and deaths 2025, marriages, "
                                 "regional fertility 2023, private education survey 2024, population projections Dec 2023); Population Reference Bureau (family planning history); "
                                 "OECD hours worked (2025).\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#southkorea #birthrate #demographics #economics #data"),
                    tags=["south korea", "birth rate", "fertility rate", "demographics", "population", "economics", "data"], lang="en"))

json.dump(spec, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "a-L02.json"), "w"), ensure_ascii=False, indent=1)
words = sum(len(s["narration"].replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()) for s in shots)
print("shots", len(shots), "palavras", words, f"~{words / 145:.1f} min a 145 wpm")

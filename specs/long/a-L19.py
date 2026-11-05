"""Gera specs/long/a-L19.json — Chartbound longo #19: "Taiwan Just Passed America"
Linha de foco "quem passou quem" (FMI out/2026: 2026 é o 1º ano da série, desde 1990, com TWN > USA em PIB por pessoa em PPP).
Dados: IMF WEO out/2026 (research/imf_twn_2026-11-05.json e research/imf_kor_2026-11-04.json). O Banco Mundial não cobre Taiwan,
por isso tudo vem do FMI; fatos citados: TSMC fundada em 1987 com apoio do governo (ITRI); distância mínima do Estreito ≈ 130 km."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "..", "..", "research")
TW = json.load(open(os.path.join(R, "imf_twn_2026-11-05.json")))
KR = json.load(open(os.path.join(R, "imf_kor_2026-11-04.json")))
ACTS = ["Cold open", "The chip island", "The long climb", "The catch", "The risks", "What comes next"]
IMF = "IMF World Economic Outlook, October 2026"
PPPC = IMF + " · GDP per capita, PPP (current international $); 2026+ are IMF estimates and forecasts"

snapshot = []
series = dict(TW["PPPPC_1990_2031"])
series["KOR"] = KR["PPPPC_1990_2031"]["KOR"]
for iso, row in series.items():
    for k, v in enumerate(row):
        snapshot.append(dict(set="imf", iso=iso, year=1990 + k, value=v, src=IMF + " · PPPPC"))
sel = TW["PPPPC_select"]
for iso in ("CHE", "SGP", "NLD", "DNK", "DEU"):
    for y, v in zip(sel["years"], sel[iso]):
        snapshot.append(dict(set="imf", iso=iso, year=y, value=v, src=IMF + " · PPPPC"))
for st, key in [("imfusd", "NGDPDPC"), ("imfg", "NGDP_RPCH"), ("imflp", "LP_millions"), ("ca", "BCA_NGDPD"), ("lur", "LUR"), ("debt", "GGXWDG_NGDP"), ("cpi", "PCPIPCH")]:
    tab = TW[key]
    for iso in ("TWN", "USA", "KOR", "JPN"):
        if iso in tab:
            for y, v in zip(tab["years"], tab[iso]):
                snapshot.append(dict(set=st, iso=iso, year=y, value=v, src=IMF + " · " + key))

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="lines", set="imf", fc=2025, series=["USA", "TWN"], years=[1990, 2026], start=1990.0, y=[0, 112000], src=PPPC, fmt="usd0", hl="TWN",
         narration="In 1990, the average person in Taiwan produced about nine and a half thousand dollars a year, adjusted for prices. The average American, about twenty-three thousand eight hundred. {p} Taiwan was at about forty percent of the American level. {pp} Last year, by the IMF's newest numbers, the gap was eleven dollars. {p} This year, it flips, and not by a little. {p} Taiwan: about a hundred and three thousand seven hundred dollars per person. The United States: about ninety-five thousand two hundred. {p} For the first time, the average person in Taiwan produces more than the average American: about nine percent more.",
         keys=[dict(at="In 1990", year=1990.0, dur=2.0), dict(at="Last year", year=2025.0, dur=5.0), dict(at="This year, it flips", year=2026.0, dur=3.0)],
         labels=[dict(at="nine and a half thousand", iso="TWN", year=1990), dict(at="twenty-three thousand eight hundred", iso="USA", year=1990), dict(at="a hundred and three thousand", iso="TWN", year=2026)],
         react=[dict(at="In 1990", pose="idle"), dict(at="forty percent", pose="pointL"), dict(at="eleven dollars", pose="shock"), dict(at="it flips", pose="cheer"), dict(at="nine percent more", pose="pointUp")]),
    dict(act=0, type="host", bg="lines", set="imf", fc=2025, series=["USA", "TWN"], years=[1990, 2026], start=2026.0, y=[0, 112000], fmt="usd0",
         narration="That's an island of about twenty-three million people, fewer than Texas, passing a country of almost three hundred and forty-three million. {p} Taiwan passed Japan back in 2010, and the Netherlands and Denmark last year. America is the biggest name yet. {p} And America isn't just any rich country. It's the largest economy on Earth, and for most of the last century, it set the standard for what being rich looks like. {pp} And the reason fits in one word: chips. <soft>So how did Taiwan do it, and why doesn't it feel richer than America?</soft>",
         items=[dict(at="twenty-three million", text="23 million vs 343 million", color="acc2", size=68), dict(at="back in 2010", text="Japan: 2010 · NL, DK: 2025", size=62), dict(at="one word: chips", text="One word: chips", serif=True, size=66, color="acc")],
         react=[dict(at="twenty-three million", pose="pointL"), dict(at="back in 2010", pose="think"), dict(at="chips", pose="pointUp"), dict(at="feel richer", pose="shrug")]),

    # ---------------- 1 · THE CHIP ISLAND ----------------
    dict(act=1, type="stats", src=IMF + " · real GDP growth (annual %), 2024–2026", title="Real growth, Taiwan",
         narration="Look at how fast Taiwan has been growing. {p} About five percent in 2024. Almost nine percent in 2025. And the IMF expects almost eleven percent this year. {p} For a rich economy, that's extraordinary. America is growing a little over two percent a year. Japan, under one percent. South Korea, about three. {pp} Most of that boom comes from one industry.",
         stats=[dict(at="About five percent", value=5.3, fmt="pct1", label="2024"), dict(at="Almost nine percent", value=8.8, fmt="pct1", label="2025"), dict(at="almost eleven percent", value=10.7, fmt="pct1", label="2026 (IMF forecast)"), dict(at="a little over two percent", value=2.3, fmt="pct1", label="United States, 2026")],
         react=[dict(at="how fast", pose="pointUp"), dict(at="Almost nine", pose="shock"), dict(at="almost eleven", pose="shock"), dict(at="one industry", pose="think")]),
    dict(act=1, type="host", bg="none",
         narration="Taiwan's biggest company, TSMC, makes most of the world's most advanced computer chips: the kind inside new phones, and inside the servers that run artificial intelligence. {p} When the world started buying AI servers by the hundreds of thousands, much of that money flowed to Taiwan, for the chips and for the servers themselves, many of them built by Taiwanese companies. {p} Think about that for a second. One company, mostly on one island, sits in the middle of a huge share of the world's phones, laptops and AI systems. That's why Taiwan's exports have been surging, and its factories running flat out. {pp} The result: this year, Taiwan expects to sell the world far more than it buys. Its current account surplus is about twenty-two percent of its whole economy. America runs a deficit of about four percent.",
         items=[dict(at="TSMC", text="TSMC: the world's chip factory", color="acc", size=62), dict(at="AI servers", text="AI boom → Taiwan", color="acc2", size=66), dict(at="twenty-two percent", text="Surplus: 22% of GDP", size=66), dict(at="deficit of about four", text="USA: −4%", color="warm", size=66)],
         react=[dict(at="TSMC", pose="pointUp"), dict(at="artificial intelligence", pose="think"), dict(at="flowed to Taiwan", pose="cheer"), dict(at="twenty-two percent", pose="shock")]),

    # ---------------- 2 · THE LONG CLIMB ----------------
    dict(act=2, type="lines", set="imf", fc=2025, series=["USA", "TWN", "JPN", "KOR"], years=[1990, 2026], start=1990.0, y=[0, 112000], src=PPPC, fmt="usdk0", hl="TWN",
         narration="But this wasn't luck. It was a forty-year climb. {p} In the 1960s and 70s, Taiwan made plastics, textiles, shoes and toys for the world. {p} In 1987, with help from the government, an engineer named Morris Chang founded TSMC, with a new idea: a company that would only manufacture chips that other companies designed. {pp} That idea turned out to be one of the most valuable in modern industry. Instead of every company building its own very expensive factory, they could design the chips and let TSMC make them. Apple, Nvidia and AMD all rely on it today. {p} Taiwan passed Japan in 2010, right after the global financial crisis. It's been ahead of South Korea the whole time, and this year it's almost fifty percent ahead.",
         keys=[dict(at="forty-year climb", year=1990.0, dur=2.0), dict(at="passed Japan in 2010", year=2010.0, dur=4.0), dict(at="this year it's almost", year=2026.0, dur=5.0)],
         labels=[dict(at="passed Japan in 2010", iso="JPN", year=2010), dict(at="almost fifty percent", iso="KOR", year=2026)],
         react=[dict(at="wasn't luck", pose="pointUp"), dict(at="toys", pose="think"), dict(at="Morris Chang", pose="pointL"), dict(at="most valuable", pose="cheer"), dict(at="almost fifty percent", pose="shock")]),
    dict(act=2, type="host", bg="none",
         narration="There's also a quieter reason Taiwan's number per person jumps so fast: there are fewer persons. {p} Taiwan's population peaked around 2020, at about twenty-three and a half million, and it's already shrinking. America's keeps growing. {p} In 1990, Taiwan had about twenty point four million people. It grew for three decades, and now the IMF has it shrinking every year. {p} So Taiwan's growing economy is shared by fewer people every year.",
         items=[dict(at="fewer persons", text="Fewer people to share it", color="acc2", size=66), dict(at="peaked around 2020", text="Peak: ~2020, 23.6 million", size=62), dict(at="America's keeps growing", text="USA: still growing", color="acc", size=66)],
         react=[dict(at="quieter reason", pose="think"), dict(at="peaked", pose="pointL"), dict(at="fewer people", pose="shrug")]),

    # ---------------- 3 · THE CATCH ----------------
    dict(act=3, type="host", bg="none",
         narration="Quick favor: if you're enjoying this, hit subscribe. It takes one second, and it really helps a small channel like this one. One country passing another, with the real numbers, every day. {p} Now the catch, because there's always a catch, and this one is big.",
         items=[dict(at="hit subscribe", text="Subscribe = more of these"), dict(at="the catch", text="The catch", serif=True, size=70, color="acc")],
         react=[dict(at="Quick favor", pose="wave"), dict(at="every day", pose="pointUp"), dict(at="the catch", pose="think")]),
    dict(act=3, type="stats", src=IMF + " · GDP per capita, current US$ (NGDPDPC), 2026", title="In plain dollars, 2026",
         narration="Everything so far is adjusted for prices. Rent, food, transport and haircuts cost far less in Taipei than in New York or San Francisco, so a dollar goes much further. A meal, a train ride, a month's rent: all much cheaper in Taiwan. {p} In plain dollars, without that adjustment, the picture is completely different. {p} The IMF puts the average American at about ninety-five thousand dollars this year. The average Taiwanese, about forty-four thousand. {pp} By that measure, America is still more than twice as rich per person. {p} Both numbers are real. They just answer different questions. One asks how much you can actually buy where you live. The other asks what your income is worth in dollars, on world markets. {p} So if you're a Taiwanese tourist in New York, it doesn't feel like you're from the richer country. At home, though, your money stretches a lot further.",
         stats=[dict(at="about ninety-five thousand", value=95212, fmt="usd0", label="United States, per person, US$"), dict(at="about forty-four thousand", value=43951, fmt="usd0", label="Taiwan, per person, US$")],
         react=[dict(at="adjusted for prices", pose="pointUp"), dict(at="much further", pose="think"), dict(at="ninety-five thousand", pose="pointL"), dict(at="more than twice", pose="shock"), dict(at="stretches", pose="shrug")]),

    # ---------------- 4 · THE RISKS ----------------
    dict(act=4, type="stats", src=IMF + " · general government gross debt (% of GDP) · unemployment rate · inflation, 2026", title="Taiwan vs America, 2026",
         narration="On some measures, Taiwan's position is enviable. {p} Its government owes about twenty-one percent of the economy. America's government owes about a hundred and twenty-seven percent. {p} Unemployment in Taiwan is about three and a half percent. Inflation, about two. {p} In America, unemployment is a bit over four percent, and the IMF expects inflation of about three and a half.",
         stats=[dict(at="about twenty-one percent", value=21.1, fmt="pct0", label="Taiwan, government debt % of GDP"), dict(at="a hundred and twenty-seven", value=126.8, fmt="pct0", label="United States"), dict(at="three and a half percent", value=3.4, fmt="pct1", label="Taiwan, unemployment"), dict(at="Inflation, about two", value=2.0, fmt="pct1", label="Taiwan, inflation")],
         react=[dict(at="enviable", pose="cheer"), dict(at="twenty-one percent", pose="pointL"), dict(at="a hundred and twenty-seven", pose="shock"), dict(at="three and a half", pose="pointUp")]),
    dict(act=4, type="host", bg="none",
         narration="But there are real risks, too. {p} First, concentration. So much of Taiwan's growth now depends on one industry, and on a few giant customers. If the AI spending boom slows, Taiwan feels it first. And big customers are already asking TSMC to build more factories outside Taiwan: in Arizona, in Japan, and in Germany. {p} Second, people. Taiwan has one of the lowest birth rates in the world, and the IMF expects its population to keep shrinking, to about twenty-two point eight million by 2030. {p} And third, geography. At its narrowest, the Taiwan Strait is only about a hundred and thirty kilometers wide, and the island's political future is one of the biggest questions in global politics. Investors watch that very closely, and so do the governments that depend on its chips.",
         items=[dict(at="concentration", text="1 · One industry", color="acc", size=68), dict(at="Second, people", text="2 · A shrinking population", color="acc", size=68), dict(at="third, geography", text="3 · Geography", color="acc", size=68)],
         react=[dict(at="real risks", pose="think"), dict(at="slows", pose="shrug"), dict(at="lowest birth rates", pose="shock"), dict(at="geography", pose="pointL")]),

    # ---------------- 5 · WHAT COMES NEXT ----------------
    dict(act=5, type="lines", set="imf", fc=2025, series=["USA", "TWN"], years=[2000, 2030], start=2026.0, y=[0, 140000], src=PPPC, fmt="usdk0", hl="TWN",
         narration="So what comes next? {p} If the IMF is right, the gap keeps growing. By 2030, Taiwan would be about eighteen percent ahead of America, adjusted for prices. {p} Next year, it would pass Switzerland too. Singapore, by the way, is still far ahead of everyone here, at almost a hundred and seventy-seven thousand dollars. {pp} But the same forecast has Taiwan's growth slowing sharply after this year's boom: to about four percent in 2027, and about three in 2028. Booms built on one product rarely last at full speed.",
         keys=[dict(at="the gap keeps growing", year=2030.0, dur=5.0)],
         labels=[dict(at="about eighteen percent", iso="TWN", year=2030), dict(at="slowing sharply", iso="USA", year=2030)],
         react=[dict(at="what comes next", pose="think"), dict(at="eighteen percent", pose="cheer"), dict(at="Switzerland", pose="pointUp"), dict(at="rarely last", pose="shrug")]),
    dict(act=5, type="host", bg="none",
         narration="So, is Taiwan richer than America now? {p} Adjusted for prices, yes, for the first time, this year. In plain dollars, no: America is still more than twice as rich per person. {p} But in 1990, Taiwan produced about forty percent of what America did per person. Closing that gap in one generation, on an island of twenty-three million people, is one of the great economic stories of our time. {pp} <soft>Which country do you think passes America next?</soft> Tell me in the comments.",
         items=[dict(at="Adjusted for prices, yes", text="Prices: Taiwan ✓ (2026)", color="acc2", size=68), dict(at="In plain dollars, no", text="Dollars: USA ×2.2", color="acc", size=68), dict(at="one generation", text="40% → 109% in 36 years", serif=True, size=56)],
         react=[dict(at="richer than America", pose="think"), dict(at="for the first time", pose="cheer"), dict(at="more than twice", pose="shrug"), dict(at="passes America next", pose="pointUp")]),
    dict(act=5, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="2026", color="acc", title="South Korea passed Britain", sub="and France, too."),
         narration="Taiwan isn't the only Asian economy passing old giants this year. South Korea just passed Britain and France. To see how, watch this next. {p} I'm Chartbound. See you in the next one.",
         hold=14,
         react=[dict(at="South Korea just passed", pose="pointL"), dict(at="See you", pose="wave")]),
]

checks = [
    dict(say="TWN 1990 ≈ $9.5k", set="imf", iso="TWN", year=1990, min=9400, max=9600),
    dict(say="USA 1990 ≈ $23.8k", set="imf", iso="USA", year=1990, min=23750, max=23899),
    dict(say="TWN ≈ 40% of USA (1990)", rule="ratio", set="imf", a="TWN", b="USA", year=1990, min=0.39, max=0.41),
    dict(say="2025 gap = $11", rule="expr", expr="90267 - 90256", equal=11),
    dict(say="TWN 2026 ≈ $103.7k", set="imf", iso="TWN", year=2026, min=103650, max=103799),
    dict(say="USA 2026 ≈ $95.2k", set="imf", iso="USA", year=2026, min=95150, max=95299),
    dict(say="first year TWN > USA = 2026", rule="first", set="imf", a="TWN", b="USA", year=2026),
    dict(say="≈ 9% more (2026)", rule="ratio", set="imf", a="TWN", b="USA", year=2026, min=1.085, max=1.095),
    dict(say="TWN pop ≈ 23 million; USA almost 343 million (IMF LP 2026)", rule="expr", expr="[round(23.198), round(342.838)]", equal=[23, 343]),
    dict(say="first year TWN > JPN = 2010", rule="first", set="imf", a="TWN", b="JPN", year=2010),
    dict(say="TWN passed NLD in 2025", rule="first", set="imf", a="TWN", b="NLD", year=2025),
    dict(say="TWN passed DNK in 2025", rule="first", set="imf", a="TWN", b="DNK", year=2025),
    dict(say="growth 2024 ≈ 5% (5.3)", set="imfg", iso="TWN", year=2024, min=5.0, max=5.5),
    dict(say="growth 2025 almost 9% (8.8)", set="imfg", iso="TWN", year=2025, min=8.5, max=8.99),
    dict(say="growth 2026 almost 11% (10.7)", set="imfg", iso="TWN", year=2026, min=10.5, max=10.99),
    dict(say="USA growth a little over 2% (2.3)", set="imfg", iso="USA", year=2026, min=2.1, max=2.5),
    dict(say="current account TWN 2026 ≈ 22% of GDP", set="ca", iso="TWN", year=2026, min=21.5, max=22.5),
    dict(say="USA deficit ≈ 4% (3.9)", set="ca", iso="USA", year=2026, min=-4.2, max=-3.6),
    dict(say="TSMC founded 1987 (with government/ITRI support), founder Morris Chang", rule="expr", expr="1987", equal=1987),
    dict(say="TWN ahead of KOR every year 1990–2026", rule="since", set="imf", a="TWN", b="KOR", year=1990),
    dict(say="TWN almost 50% ahead of KOR (2026)", rule="ratio", set="imf", a="TWN", b="KOR", year=2026, min=1.45, max=1.499),
    dict(say="TWN population peaked ~2020 (23.561M) and shrinking (23.299 → 23.198 → 22.8)", rule="expr", expr="23.561 > 23.299 > 23.198 > 22.8", equal=True),
    dict(say="USA population growing (331.3 → 341.9 → 342.8 → 346.6)", rule="expr", expr="331.307 < 341.89 < 342.838 < 346.631", equal=True),
    dict(say="USA nominal ≈ $95k (2026)", set="imfusd", iso="USA", year=2026, min=95000, max=95499),
    dict(say="TWN nominal ≈ $44k (2026)", set="imfusd", iso="TWN", year=2026, min=43700, max=44200),
    dict(say="USA more than twice (nominal 2026)", rule="ratio", set="imfusd", a="USA", b="TWN", year=2026, min=2.0, max=2.3),
    dict(say="TWN debt ≈ 21%", set="debt", iso="TWN", year=2026, min=20.5, max=21.5),
    dict(say="USA debt ≈ 127%", set="debt", iso="USA", year=2026, min=126, max=127.5),
    dict(say="TWN unemployment ≈ 3.5% (3.4)", set="lur", iso="TWN", year=2026, min=3.3, max=3.6),
    dict(say="TWN inflation ≈ 2%", set="cpi", iso="TWN", year=2026, min=1.8, max=2.2),
    dict(say="TWN population 2030 ≈ 22.8M (IMF)", set="imflp", iso="TWN", year=2030, min=22.75, max=22.85),
    dict(say="Taiwan Strait ≈ 130 km at narrowest", rule="expr", expr="130", equal=130),
    dict(say="TWN ≈ 18% ahead of USA in 2030", rule="ratio", set="imf", a="TWN", b="USA", year=2030, min=1.17, max=1.185),
    dict(say="TWN passes CHE in 2027", rule="first", set="imf", a="TWN", b="CHE", year=2027),
    dict(say="SGP 2026 almost $177k", set="imf", iso="SGP", year=2026, min=176500, max=176999),
    dict(say="JPN growth under 1%, KOR about 3% (2026)", rule="expr", expr="[0.7 < 1, round(3.3)]", equal=[True, 3]),
    dict(say="USA unemployment a bit over 4% (4.2), inflation ≈ 3.5 (3.6)", rule="expr", expr="[4 < 4.2 < 4.5, round(3.6 * 2) / 2]", equal=[True, 3.5]),
    dict(say="TWN pop 1990 ≈ 20.4M", set="imflp", iso="TWN", year=1990, min=20.35, max=20.45),
    dict(say="TWN growth 2027 ≈ 4% (4.3), 2028 ≈ 3% (3.2)", rule="expr", expr="[round(4.3), round(3.2)]", equal=[4, 3]),
    dict(say="1990 → 2026 = 36 years; 40% → 109%", rule="expr", expr="[2026 - 1990, round(9534 / 23848 * 100), round(103743 / 95212 * 100)]", equal=[36, 40, 109]),
    dict(say="USA ×2.2 in dollars", rule="expr", expr="round(95212 / 43951, 1)", equal=2.2),
]

clips = [
    dict(**{"from": "s00", "to": "s00"}, hook="Taiwan just passed *America*", title="Taiwan just passed the United States (IMF, 2026) #Shorts", desc="GDP per person, PPP: 1990 Taiwan $9.5k vs US $23.8k. 2026: Taiwan $103.7k vs US $95.2k (IMF WEO Oct 2026)."),
    dict(**{"from": "s03", "to": "s03"}, hook="One company changed *Taiwan*", title="Taiwan grew 9% and 11% in two years. Here's why #Shorts", desc="IMF: real growth 8.8% in 2025 and 10.7% expected in 2026; current account surplus ~22% of GDP."),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="a-L19-taiwan", clips=clips, channel="chartbound", chapter0="The flip",
            thumb=dict(v="flags", iso="TWN", vs="USA", big="TAIWAN > USA", line2="FIRST TIME EVER (IMF, 2026)"),
            w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks, datasets=[], snapshot=snapshot,
            voice=dict(model="", name="Charon",
                       style=("You are the narrator of a popular data documentary on YouTube. Read the script below in a warm, curious voice "
                              "with a little dry humor, at a relaxed but engaged pace of about 145 words per minute, like a smart friend telling "
                              "you something surprising. Let the big numbers land with a tiny pause before them. Keep the energy steady from the "
                              "first sentence to the last. Never sound like an advertisement or an audiobook.")),
            music=[dict(act=0, track="Lightless Dawn", vol=0.24), dict(act=1, track="Investigations", vol=0.23), dict(act=2, track="Deliberate Thought", vol=0.22),
                   dict(act=3, track="Hidden Agenda", vol=0.23), dict(act=4, track="Inspired", vol=0.23), dict(act=5, track="Floating Cities", vol=0.24)],
            yt=dict(title="Taiwan Just Passed America",
                    description=("In 1990 the average person in Taiwan produced about 40% as much as the average American, adjusted for prices. In the IMF's October 2026 World Economic Outlook, "
                                 "2026 is the first year Taiwan is ahead: $103,743 per person against $95,212 for the United States. The chip boom, the forty-year climb, the shrinking population, "
                                 "why America is still more than twice as rich in plain dollars, and the risks.\n\n"
                                 "Sources: IMF World Economic Outlook, October 2026 (PPPPC, NGDPDPC, NGDP_RPCH, LP, BCA_NGDPD, LUR, GGXWDG_NGDP, PCPIPCH).\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#taiwan #usa #economics #imf #chips #data"),
                    tags=["taiwan", "taiwan economy", "taiwan vs usa", "tsmc", "semiconductors", "gdp per capita", "imf", "economics", "data", "ai boom"], lang="en"))

json.dump(spec, open(os.path.join(HERE, "a-L19.json"), "w"), ensure_ascii=False, indent=1)
clean = lambda t: t.replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()
words = sum(len(clean(s["narration"])) for s in shots)
acts = {}
for s in shots:
    acts[s["act"]] = acts.get(s["act"], 0) + len(clean(s["narration"]))
print("shots", len(shots), "palavras", words, f"~{words / 145:.1f} min a 145 wpm", "por ato", acts)

"""Gera specs/long/a-L31.json — Chartbound longo #31: "Japan Was Twice as Rich as Italy. Now Italy Is 30% Ahead." (série "quem passou quem"; Japão, o público que mais rende)
Medida principal: PIB per capita em dólares correntes (NGDPDPC, câmbio de mercado), dita na tela e na narração; ato 3 mostra o ajustado por preços (PPPPC),
em que a Itália já estava à frente em 1990. Achado central: 2012→2024 PIB real JPN +9,2% e ITA +9,0%, mas em dólares JPN −32% e ITA +16% (câmbio).
Dados: IMF WEO out/2026 (research/imf_ita_2026-11-07.json: JPN, ITA, ESP, PRT, POL completos 1990–2031).
Fora do FMI (documentado): câmbio médio anual JPY/USD ≈ 80 (2012) → ≈ 151 (2024), iene perdeu ~47%; EUR/USD ≈ 1,29 → ≈ 1,08, euro perdeu ~16% (Fed H.10 / BCE)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "..", "..", "research", "imf_ita_2026-11-07.json")))
ACTS = ["Cold open", "Four lines", "Same growth, opposite dollars", "Adjusted for prices", "Where Japan wins", "Who's next", "Your guess"]
IMF = "IMF World Economic Outlook, October 2026"


def series(ind, iso):
    r = D[ind][iso]
    return {r["y0"] + k: v for k, v in enumerate(r["v"])}


C5 = ("JPN", "ITA", "ESP", "PRT", "POL")
N = {c: series("NGDPDPC", c) for c in C5}
PP = {c: series("PPPPC", c) for c in ("JPN", "ITA")}
GR = {c: series("NGDP_RPCH", c) for c in ("JPN", "ITA")}
LUR = {c: series("LUR", c) for c in ("JPN", "ITA")}
DEBT = {c: series("GGXWDG_NGDP", c) for c in ("JPN", "ITA")}
CPI = {c: series("PCPIPCH", c) for c in ("JPN", "ITA")}
J, I, E, PR, P = N["JPN"], N["ITA"], N["ESP"], N["PRT"], N["POL"]


def grow(iso, a, b):
    c = 1.0
    for y in range(a + 1, b + 1):
        c *= 1 + GR[iso][y] / 100
    return c


snapshot = []
for c, s in N.items():
    for y, v in s.items():
        snapshot.append(dict(set="imfusd", iso=c, year=y, value=v, src=IMF + " · NGDPDPC"))
for c, s in PP.items():
    for y, v in s.items():
        snapshot.append(dict(set="imf", iso=c, year=y, value=v, src=IMF + " · PPPPC"))
for st, tab, ind in [("imfg", GR, "NGDP_RPCH"), ("lur", LUR, "LUR"), ("debt", DEBT, "GGXWDG_NGDP"), ("cpi", CPI, "PCPIPCH")]:
    for c, s in tab.items():
        for y, v in s.items():
            snapshot.append(dict(set=st, iso=c, year=y, value=v, src=IMF + " · " + ind))

USDSRC = IMF + " · GDP per capita, current US$ at market exchange rates (NGDPDPC); 2026+ are IMF estimates and forecasts"
PPPSRC = IMF + " · GDP per capita, PPP, current international $ (PPPPC); 2026+ are IMF estimates and forecasts"
USD2 = dict(set="imfusd", fc=2025, series=["JPN", "ITA"], years=[1990, 2031], y=[0, 55000], src=USDSRC, fmt="usd0", hl="ITA")

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="lines", start=1995.0, **USD2,
         narration="Twice as rich. {p} In 1995, the average Japanese person produced more than twice as much as the average Italian, in plain dollars at market exchange rates. About forty-five thousand dollars a year, against about twenty-one thousand. {pp} In 2022, Italy passed Japan, by about a hundred and thirty dollars. {p} This year, in the IMF's numbers, Italy is about thirty percent ahead.",
         keys=[dict(at="Twice as rich", year=1995.0, dur=0.5), dict(at="In 2022", year=2022.0, dur=2.5), dict(at="This year", year=2026.0, dur=2.5)],
         labels=[dict(at="About forty-five thousand", iso="JPN", year=1995), dict(at="about twenty-one thousand", iso="ITA", year=1995), dict(at="In 2022", iso="ITA", year=2022), dict(at="thirty percent ahead", iso="ITA", year=2026)],
         react=[dict(at="Twice as rich", pose="shock"), dict(at="plain dollars", pose="pointUp"), dict(at="Italy passed Japan", pose="shock"), dict(at="thirty percent ahead", pose="think")]),
    dict(act=0, type="host", bg="lines", start=2031.0, **{k: v for k, v in USD2.items() if k != "src"},
         narration="And Italy isn't alone. Spain passed Japan in 2024. In the IMF's forecast, Portugal passes it in 2029. {p} These are not the economies people usually call fast. Italy's economy has grown about ten percent in twenty-five years. {pp} <soft>So this isn't really a story about Southern Europe. It's a story about what happened to Japan's money.</soft>",
         items=[dict(at="Spain passed Japan", text="2024: Spain > Japan", color="acc2", size=58), dict(at="Portugal passes it", text="2029: Portugal > Japan?", color="warm", size=58), dict(at="about ten percent", text="Italy: +10% since 2000", serif=True, size=60, color="acc")],
         react=[dict(at="isn't alone", pose="pointL"), dict(at="Portugal", pose="shock"), dict(at="not the economies", pose="think"), dict(at="Japan's money", pose="pointUp")]),

    # ---------------- 1 · FOUR LINES ----------------
    dict(act=1, type="host", bg="none",
         narration="Quick one before the chart: this channel is a series about who's passing whom. Subscribe so you don't miss the next one. {p} Now, four lines.",
         items=[dict(at="who's passing whom", text="Who passed whom", serif=True, size=66, color="acc"), dict(at="Subscribe", text="Subscribe", size=70)],
         react=[dict(at="Quick one", pose="wave"), dict(at="Subscribe", pose="cheer"), dict(at="four lines", pose="pointL")]),
    dict(act=1, type="lines", set="imfusd", fc=2025, series=["JPN", "ITA", "ESP", "PRT"], years=[1990, 2031], start=1995.0, y=[0, 55000], src=USDSRC, fmt="usdk0", hl="JPN",
         narration="Here's Japan against Italy, Spain and Portugal, in plain dollars per person. {p} In 1995, Japan was more than twice as rich as Italy, almost three times as rich as Spain, and almost four times as rich as Portugal. {pp} Japan peaked in 2012. Then its line goes down, while the other three keep climbing. Italy crosses in 2022. Spain in 2024. And Portugal, in the forecast, in 2029.",
         keys=[dict(at="Here's Japan", year=1995.0, dur=1.5), dict(at="Japan peaked in 2012", year=2012.0, dur=2.0), dict(at="Italy crosses", year=2022.0, dur=1.5), dict(at="Spain in 2024", year=2024.0, dur=1.5), dict(at="in 2029", year=2029.0, dur=2.5)],
         react=[dict(at="Here's Japan", pose="pointL"), dict(at="almost four times", pose="shock"), dict(at="goes down", pose="think"), dict(at="Italy crosses", pose="pointUp"), dict(at="in 2029", pose="shock")]),

    # ---------------- 2 · SAME GROWTH, OPPOSITE DOLLARS ----------------
    dict(act=2, type="stats", src=IMF + " · real GDP growth (NGDP_RPCH, compounded) and GDP per capita in current US$ (NGDPDPC), 2012–2024", title="2012 to 2024",
         narration="Here's the strangest part. From 2012 to 2024, after inflation, Japan's economy grew about nine percent. Italy's grew about nine percent too. Almost exactly the same. {pp} But in dollars per person, Japan's number fell by almost a third. Italy's rose by about sixteen percent. {p} Same growth. Opposite dollars. The difference is mostly the currency: the yen lost almost half its value against the dollar. The euro lost much less.",
         stats=[dict(at="Japan's economy grew about nine percent", value=round((grow("JPN", 2012, 2024) - 1) * 100), fmt="pct0", label="Japan, real growth 2012–2024"), dict(at="Italy's grew about nine percent too", value=round((grow("ITA", 2012, 2024) - 1) * 100), fmt="pct0", label="Italy, real growth 2012–2024"), dict(at="fell by almost a third", value=round((J[2024] / J[2012] - 1) * 100), fmt="pct0", label="Japan, US$ per person 2012→2024"), dict(at="rose by about sixteen percent", value=round((I[2024] / I[2012] - 1) * 100), fmt="pct0", label="Italy, US$ per person 2012→2024")],
         react=[dict(at="strangest part", pose="think"), dict(at="Almost exactly the same", pose="shock"), dict(at="almost a third", pose="shock"), dict(at="Opposite dollars", pose="pointUp")]),

    # ---------------- 3 · ADJUSTED FOR PRICES ----------------
    dict(act=3, type="lines", set="imf", fc=2025, series=["JPN", "ITA"], years=[1990, 2031], start=1990.0, y=[0, 80000], src=PPPSRC, fmt="usdk0", hl="ITA",
         narration="Now adjust for what money actually buys at home, and the picture changes again. {p} On this measure, Italy was already ahead of Japan in 1990. Japan pulled slightly ahead for a few years, from 2014 to 2017. {pp} Since 2018, Italy has been ahead every year, and this year by about eleven percent. {p} So the old idea of Japan as far richer than Italy was mostly an exchange-rate story.",
         keys=[dict(at="Now adjust", year=1990.0, dur=1.5), dict(at="from 2014 to 2017", year=2016.0, dur=2.0), dict(at="Since 2018", year=2018.0, dur=1.5), dict(at="eleven percent", year=2026.0, dur=2.5)],
         labels=[dict(at="already ahead of Japan in 1990", iso="ITA", year=1990), dict(at="eleven percent", iso="ITA", year=2026)],
         react=[dict(at="Now adjust", pose="pointUp"), dict(at="already ahead", pose="shock"), dict(at="a few years", pose="think"), dict(at="exchange-rate story", pose="pointL")]),

    # ---------------- 4 · WHERE JAPAN WINS ----------------
    dict(act=4, type="host", bg="none",
         narration="And if you're enjoying this, the subscribe button is right there. {p} Now, to be fair to Japan.",
         items=[dict(at="subscribe button", text="Subscribe", size=66), dict(at="fair to Japan", text="Where Japan wins", serif=True, size=66, color="acc")],
         react=[dict(at="subscribe button", pose="pointUp"), dict(at="fair to Japan", pose="cheer")]),
    dict(act=4, type="duel", set="lur", year=2026, a="JPN", b="ITA", fmt="dec1", src=IMF + " · unemployment rate (% of labor force), 2026 estimate", title="Unemployment, 2026", badge="LOWER IN JAPAN",
         cues=[dict(at="two point five", show="a"), dict(at="five point six", show="b")],
         narration="Unemployment this year: about two point five percent in Japan, {pp} five point six in Italy. And when prices jumped in 2022, inflation was about two and a half percent in Japan, and almost nine in Italy. {p} Both carry heavy government debt: about two hundred percent of the economy in Japan, about a hundred and thirty-eight in Italy.",
         react=[dict(at="Unemployment", pose="pointUp"), dict(at="almost nine", pose="shock"), dict(at="heavy government debt", pose="think")]),

    # ---------------- 5 · WHO'S NEXT ----------------
    dict(act=5, type="lines", set="imfusd", fc=2025, series=["JPN", "PRT", "POL"], years=[2010, 2031], start=2020.0, y=[0, 55000], src=USDSRC, fmt="usdk0", hl="JPN",
         narration="So who's next? {p} This year, the average Portuguese person produces about ninety-eight percent of what the average Japanese person does, in plain dollars. In the IMF's forecast, Portugal passes Japan in 2029. {pp} And right behind it, Poland: eighty-eight percent this year, and ninety-nine percent in 2031. That one has its own episode on the channel. {p} In 1995, all of these countries together looked poor next to Japan.",
         keys=[dict(at="who's next", year=2020.0, dur=1.0), dict(at="ninety-eight percent", year=2026.0, dur=2.0), dict(at="in 2029", year=2029.0, dur=2.0), dict(at="ninety-nine percent in 2031", year=2031.0, dur=2.5)],
         labels=[dict(at="in 2029", iso="PRT", year=2029), dict(at="ninety-nine percent in 2031", iso="POL", year=2031)],
         react=[dict(at="who's next", pose="think"), dict(at="Portugal passes", pose="shock"), dict(at="Poland", pose="pointUp"), dict(at="looked poor", pose="shrug")]),

    # ---------------- 6 · YOUR GUESS ----------------
    dict(act=6, type="host", bg="none",
         narration="<soft>So, what's your guess?</soft> {pp} Does the yen bounce back and put Japan ahead again, {p} or is this the new normal? {pp} Tell me in the comments. {pp} If you're watching from Japan or Italy: {p} does this match what you see? {pp} I read every comment.",
         items=[dict(at="your guess", text="Bounce back or new normal?", color="acc", size=60), dict(at="Japan or Italy", text="Japan, Italy: does it match?", color="warm", size=54)],
         react=[dict(at="your guess", pose="shrug"), dict(at="Tell me", pose="pointUp"), dict(at="Japan or Italy", pose="wave")]),
    dict(act=6, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="JPN", color="acc", title="Poland passed Japan", sub="the one nobody noticed."),
         narration="And if you missed it, {p} this is the episode where Poland passed Japan, adjusted for prices. {pp} It's right here. {pp} I'm Chartbound. {p} See you in the next one.",
         hold=14,
         react=[dict(at="if you missed it", pose="pointL"), dict(at="See you", pose="wave")]),
]

checks = [
    dict(say="1995: JPN/ITA 2.17 (more than twice); JPN ≈ 45k, ITA ≈ 21k (20,723)", rule="expr", expr=f"[round({J[1995]} / {I[1995]}, 2), round({J[1995]} / 1000), round({I[1995]} / 1000)]", equal=[2.17, 45, 21]),
    dict(say="ITA passed JPN in 2022 by ≈130; ahead every year 2022–2031; 2021 still behind", rule="expr", expr=f"[round({I[2022]} - {J[2022]}), {all(I[y] > J[y] for y in range(2022, 2032))}, {I[2021] < J[2021]}]", equal=[130, True, True]),
    dict(say="2026: ITA ≈ 30% ahead (29.6)", rule="expr", expr=f"round(({I[2026]} / {J[2026]} - 1) * 100)", equal=30),
    dict(say="ESP passed JPN 2024 (2023 behind; ahead 2024–2031)", rule="expr", expr=f"[{E[2023] < J[2023]}, {all(E[y] > J[y] for y in range(2024, 2032))}]", equal=[True, True]),
    dict(say="PRT passes JPN 2029 (2028 behind; ahead 2029–2031)", rule="expr", expr=f"[{PR[2028] < J[2028]}, {all(PR[y] > J[y] for y in range(2029, 2032))}]", equal=[True, True]),
    dict(say="ITA real growth 2000→2025 ≈ +10% (twenty-five years)", rule="expr", expr=f"round(({grow('ITA', 2000, 2025)} - 1) * 100)", equal=10),
    dict(say="1995: JPN/ESP 2.9 (almost three), JPN/PRT 3.8 (almost four)", rule="expr", expr=f"[round({J[1995]} / {E[1995]}, 1), round({J[1995]} / {PR[1995]}, 1)]", equal=[2.9, 3.8]),
    dict(say="JPN USD peak 2012", rule="expr", expr=f"{max(J, key=J.get)}", equal=2012),
    dict(say="2012→2024 real: JPN +9%, ITA +9%; USD: JPN −32% (almost a third), ITA +16%", rule="expr", expr=f"[round(({grow('JPN', 2012, 2024)} - 1) * 100), round(({grow('ITA', 2012, 2024)} - 1) * 100), round(({J[2024]} / {J[2012]} - 1) * 100), round(({I[2024]} / {I[2012]} - 1) * 100)]", equal=[9, 9, -32, 16]),
    dict(say="PPP: ITA > JPN in 1990; JPN ahead exactly 2014–2017 (1990–2031); ITA ahead 2018–2031; 2026 ITA +11%", rule="expr", expr=f"[{PP['ITA'][1990] > PP['JPN'][1990]}, {[y for y in range(1990, 2032) if PP['JPN'][y] > PP['ITA'][y]]}, round(({PP['ITA'][2026]} / {PP['JPN'][2026]} - 1) * 100)]", equal=[True, [2014, 2015, 2016, 2017], 11]),
    dict(say="unemployment 2026 JPN 2.5, ITA 5.6; CPI 2022 JPN 2.5, ITA 8.7 (almost nine); debt 2026 JPN ≈ 199 (about two hundred), ITA ≈ 138", rule="expr", expr=f"[{LUR['JPN'][2026]}, {LUR['ITA'][2026]}, {CPI['JPN'][2022]}, {CPI['ITA'][2022]}, round({DEBT['JPN'][2026]}), round({DEBT['ITA'][2026]})]", equal=[2.5, 5.6, 2.5, 8.7, 199, 138]),
    dict(say="2026: PRT/JPN 98%, POL/JPN 88%; 2031 POL/JPN 99%", rule="expr", expr=f"[round({PR[2026]} / {J[2026]} * 100), round({P[2026]} / {J[2026]} * 100), round({P[2031]} / {J[2031]} * 100)]", equal=[98, 88, 99]),
    dict(say="1995: JPN > ITA, ESP, PRT, POL (all looked poor next to Japan)", rule="expr", expr=f"{J[1995] > max(I[1995], E[1995], PR[1995], P[1995])}", equal=True),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="a-L31-japan-italy-usd", clips=[], channel="chartbound", chapter0="Twice as rich",
            thumb=dict(v="flags", iso="ITA", vs="JPN", sym=">", big="+30%", line2="IN DOLLARS"),
            w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks, datasets=[], snapshot=snapshot,
            voice=dict(model="", name="Charon",
                       style=("You are the narrator of a popular data documentary on YouTube. Read the script below in a warm, curious voice "
                              "with a little dry humor, at a relaxed but engaged pace of about 145 words per minute, like a smart friend telling "
                              "you something surprising. Let the big numbers land with a tiny pause before them. Keep the energy steady from the "
                              "first sentence to the last. Never sound like an advertisement or an audiobook.")),
            music=[dict(act=0, track="Lightless Dawn", vol=0.24), dict(act=1, track="Deliberate Thought", vol=0.22), dict(act=2, track="Hidden Agenda", vol=0.23), dict(act=3, track="Inspired", vol=0.23),
                   dict(act=4, track="Investigations", vol=0.23), dict(act=5, track="Deliberate Thought", vol=0.22), dict(act=6, track="Floating Cities", vol=0.24)],
            yt=dict(title="Japan Was Twice as Rich as Italy. Now Italy Is 30% Ahead.",
                    description=("Income per person in plain US dollars, at market exchange rates (IMF World Economic Outlook, October 2026): in 1995 the average Japanese person produced 2.2× as much as the average Italian. "
                                 "Italy passed Japan in 2022; this year it's ~30% ahead. Spain passed Japan in 2024, and in the IMF's forecast Portugal passes it in 2029. "
                                 "The strangest part: from 2012 to 2024 both economies grew ~9% after inflation, yet Japan's dollar income per person fell ~32% and Italy's rose ~16% — the yen. "
                                 "Adjusted for prices, Italy was already ahead in 1990. Plus where Japan still wins (unemployment, inflation) and who's next (Portugal, Poland).\n\n"
                                 "Sources: IMF World Economic Outlook, October 2026 (NGDPDPC, PPPPC, NGDP_RPCH, LUR, GGXWDG_NGDP, PCPIPCH). 2026+ figures are IMF estimates and forecasts.\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#japan #italy #yen #economics #imf #data"),
                    tags=["japan", "italy", "japan vs italy", "yen", "weak yen", "japan economy", "italy economy", "spain", "portugal", "gdp per capita", "imf", "economics", "日本", "italia"], lang="en"))

json.dump(spec, open(os.path.join(HERE, "a-L31.json"), "w"), ensure_ascii=False, indent=1)
clean = lambda t: t.replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()
words = sum(len(clean(s["narration"])) for s in shots)
acts = {}
for s in shots:
    acts[s["act"]] = acts.get(s["act"], 0) + len(clean(s["narration"]))
print("shots", len(shots), "palavras", words, f"~{words / 145:.1f} min a 145 wpm", "por ato", acts)

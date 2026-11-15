"""Gera specs/long/a-L30.json — Chartbound longo #30: "Estonia Was 46% Richer Than Poland. Then It Stalled." (série Polônia, formato "passou")
Medida principal: PIB per capita ajustado por preços (PPPPC), como no resto da série; o ato 3 mostra os dólares correntes (NGDPDPC), em que a Estônia ainda lidera.
Dados: IMF WEO out/2026 (research/imf_v4_2026-11-13.json: POL, EST; research/imf_ltu_2026-11-10.json: LTU).
Fora do FMI (documentado): Estônia adotou o euro em 1/1/2011; quase todos os serviços públicos são online (e-Estonia)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "..", "..", "research")
D = json.load(open(os.path.join(R, "imf_v4_2026-11-13.json")))
LT = json.load(open(os.path.join(R, "imf_ltu_2026-11-10.json")))
ACTS = ["Cold open", "The tiger years", "The crash", "Plain dollars", "The Baltic race", "The pass", "Your guess"]
IMF = "IMF World Economic Outlook, October 2026"


def ser(src, ind, iso):
    r = src[ind][iso]
    return {r["y0"] + k: v for k, v in enumerate(r["v"])}


PP = {"POL": ser(D, "PPPPC", "POL"), "EST": ser(D, "PPPPC", "EST"), "LTU": ser(LT, "PPPPC", "LTU")}
N = {"POL": ser(D, "NGDPDPC", "POL"), "EST": ser(D, "NGDPDPC", "EST")}
GR = {"POL": ser(D, "NGDP_RPCH", "POL"), "EST": ser(D, "NGDP_RPCH", "EST"), "LTU": ser(LT, "NGDP_RPCH", "LTU")}
LP = {"POL": ser(D, "LP", "POL"), "EST": ser(D, "LP", "EST")}
P, E, L = PP["POL"], PP["EST"], PP["LTU"]


def grow(iso, a, b):
    c = 1.0
    for y in range(a + 1, b + 1):
        c *= 1 + GR[iso][y] / 100
    return c


snapshot = []
for iso, s in PP.items():
    for y, v in s.items():
        snapshot.append(dict(set="imf", iso=iso, year=y, value=v, src=IMF + " · PPPPC"))
for iso, s in N.items():
    for y, v in s.items():
        snapshot.append(dict(set="imfusd", iso=iso, year=y, value=v, src=IMF + " · NGDPDPC"))
for iso, s in GR.items():
    for y, v in s.items():
        snapshot.append(dict(set="imfg", iso=iso, year=y, value=v, src=IMF + " · NGDP_RPCH"))
for iso, s in LP.items():
    for y, v in s.items():
        snapshot.append(dict(set="pop", iso=iso, year=y, value=v, src=IMF + " · LP"))
for y in range(1995, 2032):
    snapshot.append(dict(set="rat", iso="EST", year=y, value=round(E[y] / P[y] * 100, 2), src=IMF + " · Estonia's GDP per capita (PPP) as % of Poland's"))

PPPSRC = IMF + " · GDP per capita, PPP, current international $ (PPPPC); 2026+ are IMF estimates and forecasts"
USDSRC = IMF + " · GDP per capita, current US$ at market exchange rates (NGDPDPC); 2026+ are IMF estimates and forecasts"
PPP2 = dict(set="imf", fc=2025, series=["EST", "POL"], years=[1995, 2031], y=[0, 80000], src=PPPSRC, fmt="usd0", hl="POL")
RATCH = dict(set="rat", fc=2025, series=["EST"], years=[1995, 2031], y=[60, 160], src=IMF + " · Estonia's GDP per capita (PPP) as % of Poland's; 2026+ are IMF estimates and forecasts", fmt="pct0", hl="EST", ref=dict(value=100, label="Poland = 100%", pos="left"))

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="lines", start=2007.0, **PPP2,
         narration="Forty-six percent. {p} In 2007, the average Estonian was forty-six percent richer than the average Pole, on income adjusted for prices. About twenty-seven thousand dollars a person, against eighteen and a half thousand. {pp} In 2023, Poland passed. This year, in the IMF's numbers, Poland is about twelve percent ahead. {p} And by 2031, in the IMF's forecast, about fifteen.",
         keys=[dict(at="Forty-six percent", year=2007.0, dur=0.5), dict(at="In 2023", year=2023.0, dur=2.5), dict(at="This year", year=2026.0, dur=1.5), dict(at="by 2031", year=2031.0, dur=2.5)],
         labels=[dict(at="About twenty-seven thousand", iso="EST", year=2007), dict(at="eighteen and a half thousand", iso="POL", year=2007), dict(at="In 2023", iso="POL", year=2023), dict(at="twelve percent ahead", iso="POL", year=2026)],
         react=[dict(at="Forty-six percent", pose="shock"), dict(at="In 2007", pose="pointL"), dict(at="Poland passed", pose="cheer"), dict(at="by 2031", pose="pointUp")]),
    dict(act=0, type="host", bg="lines", start=2031.0, **{k: v for k, v in PPP2.items() if k != "src"},
         narration="Estonia was the star of Eastern Europe. One of the fastest-growing economies in Europe in the 2000s, the euro since 2011, and a government that moved almost every public service online. {p} If you'd asked in 2007 which country would be richer in 2026, almost nobody would have said Poland. {pp} <soft>So what happened? A crash, a long stall, and a neighbor that never slowed down.</soft>",
         items=[dict(at="the star of Eastern Europe", text="The Baltic tiger", serif=True, size=66, color="acc2"), dict(at="the euro since 2011", text="Euro since 2011", color="acc", size=60), dict(at="never slowed down", text="Poland: 1 down year since 1992", color="warm", size=54)],
         react=[dict(at="the star", pose="pointL"), dict(at="almost every public service online", pose="think"), dict(at="almost nobody", pose="shrug"), dict(at="never slowed down", pose="pointUp")]),

    # ---------------- 1 · THE TIGER YEARS ----------------
    dict(act=1, type="host", bg="none",
         narration="Quick one before the chart: this is a series about who's passing whom, and Poland keeps showing up. Subscribe so you don't miss the next one. {p} Now, the tiger years.",
         items=[dict(at="who's passing whom", text="Who passed whom", serif=True, size=66, color="acc"), dict(at="Subscribe", text="Subscribe", size=70)],
         react=[dict(at="Quick one", pose="wave"), dict(at="Subscribe", pose="cheer"), dict(at="the tiger years", pose="pointL")]),
    dict(act=1, type="lines", start=1995.0, **RATCH,
         narration="Here's Estonia as a share of Poland, adjusted for prices. {p} 1995: about even, a hundred and three percent. Then Estonia took off. A hundred and nine percent in 2000. And in 2007, a hundred and forty-six. {pp} Between 2000 and 2007, Estonia's economy grew almost seventy percent after inflation. Poland's grew about thirty. {p} Then came 2008.",
         keys=[dict(at="1995", year=1995.0, dur=1.5), dict(at="A hundred and nine percent", year=2000.0, dur=1.5), dict(at="And in 2007", year=2007.0, dur=2.0), dict(at="Then came 2008", year=2008.0, dur=1.5)],
         labels=[dict(at="1995", iso="EST", year=1995), dict(at="A hundred and nine percent", iso="EST", year=2000), dict(at="And in 2007", iso="EST", year=2007)],
         react=[dict(at="about even", pose="pointL"), dict(at="took off", pose="shock"), dict(at="almost seventy percent", pose="pointUp"), dict(at="Then came 2008", pose="think")]),

    # ---------------- 2 · THE CRASH ----------------
    dict(act=2, type="bars", mode="abs", set="imfg", iso="EST", years=[2000, 2030], start=2005.0, fmt="pct1", src=IMF + " · real GDP growth, Estonia (annual %); 2026+ are IMF estimates and forecasts",
         narration="Here's Estonia's economy, year by year, after inflation. {p} In 2008, it shrank about five percent. In 2009, it shrank fourteen and a half percent, one of the deepest drops in Europe in that recession. In the same year, Poland grew two point six percent. {pp} Estonia recovered, then slowed again: it shrank about three percent in 2023, and barely grew in 2024. {p} Poland's economy has shrunk in only one year since 1991: 2020.",
         keys=[dict(at="In 2008", year=2008.0, dur=1.5), dict(at="In 2009", year=2009.0, dur=2.0), dict(at="Estonia recovered", year=2011.0, dur=2.0), dict(at="three percent in 2023", year=2023.0, dur=1.5), dict(at="barely grew in 2024", year=2024.0, dur=1.5)],
         react=[dict(at="In 2008", pose="think"), dict(at="fourteen and a half", pose="shock"), dict(at="Poland grew", pose="pointUp"), dict(at="slowed again", pose="shrug"), dict(at="since 1991", pose="cheer")]),
    dict(act=2, type="stats", src=IMF + " · real GDP growth (NGDP_RPCH, compounded), population (LP)", title="The long stall",
         narration="Put it together. From 2007 to 2025, after inflation, Estonia's economy grew about twenty-one percent. Poland's grew about eighty-four. {p} That's the whole story of this chart: not a Polish miracle in one year, but eighteen years of Poland growing four times as much. {pp} And Estonia is small: about one point four million people. Poland has twenty-seven times as many.",
         stats=[dict(at="about twenty-one percent", value=round((grow("EST", 2007, 2025) - 1) * 100), fmt="pct0", label="Estonia, real growth 2007–2025"), dict(at="about eighty-four", value=round((grow("POL", 2007, 2025) - 1) * 100), fmt="pct0", label="Poland, real growth 2007–2025"), dict(at="one point four million", value=round(LP["EST"][2026], 1), fmt="dec1", label="million people in Estonia, 2026"), dict(at="twenty-seven times", value=round(LP["POL"][2026] / LP["EST"][2026]), fmt="dec0", label="Poland's population ÷ Estonia's")],
         react=[dict(at="Put it together", pose="pointUp"), dict(at="about eighty-four", pose="cheer"), dict(at="four times as much", pose="shock"), dict(at="Estonia is small", pose="think")]),

    # ---------------- 3 · PLAIN DOLLARS ----------------
    dict(act=3, type="lines", set="imfusd", fc=2025, series=["EST", "POL"], years=[1995, 2031], start=2015.0, y=[0, 50000], src=USDSRC, fmt="usd0", hl="POL",
         narration="To be fair to Estonia: in plain dollars, at market exchange rates, it's still ahead. {p} This year, about thirty-seven thousand three hundred dollars per person, against thirty-one thousand two hundred in Poland. That's twenty percent. {pp} Prices in Estonia are higher, so the same money buys less there. Adjust for that, and Poland is ahead. But in plain dollars, the IMF still has Estonia about thirteen percent ahead in 2031.",
         keys=[dict(at="To be fair", year=2015.0, dur=1.5), dict(at="This year", year=2026.0, dur=2.5), dict(at="in 2031", year=2031.0, dur=2.5)],
         labels=[dict(at="thirty-seven thousand three hundred", iso="EST", year=2026), dict(at="thirty-one thousand two hundred", iso="POL", year=2026), dict(at="in 2031", iso="EST", year=2031)],
         react=[dict(at="To be fair", pose="think"), dict(at="twenty percent", pose="pointUp"), dict(at="Prices in Estonia are higher", pose="shrug"), dict(at="thirteen percent", pose="pointL")]),

    # ---------------- 4 · THE BALTIC RACE ----------------
    dict(act=4, type="host", bg="none",
         narration="And if you're enjoying the series, the subscribe button is right there. {p} Now, the neighbor that never slowed down.",
         items=[dict(at="subscribe button", text="Subscribe", size=66), dict(at="never slowed down", text="The Baltic race", serif=True, size=66, color="acc")],
         react=[dict(at="subscribe button", pose="pointUp"), dict(at="never slowed down", pose="pointL")]),
    dict(act=4, type="lines", set="imf", fc=2025, series=["EST", "LTU", "POL"], years=[2000, 2031], start=2007.0, y=[0, 80000], src=PPPSRC, fmt="usd0", hl="POL",
         narration="Lithuania. In 2007, the average Lithuanian was about nineteen percent behind the average Estonian, adjusted for prices. {p} In 2020, Lithuania passed Estonia. Three years later, Poland did too. {pp} This year, Lithuania is about fourteen percent ahead of Estonia, and still about two percent ahead of Poland. Which is a whole other episode, and it's already on the channel. {p} Estonia went from first in this race to third.",
         keys=[dict(at="In 2007", year=2007.0, dur=1.5), dict(at="In 2020", year=2020.0, dur=1.5), dict(at="Three years later", year=2023.0, dur=1.5), dict(at="This year", year=2026.0, dur=3.0)],
         labels=[dict(at="In 2007", iso="EST", year=2007), dict(at="In 2020", iso="LTU", year=2020), dict(at="Three years later", iso="POL", year=2023), dict(at="still about two percent", iso="LTU", year=2026)],
         react=[dict(at="Lithuania", pose="pointL"), dict(at="passed Estonia", pose="shock"), dict(at="Poland did too", pose="cheer"), dict(at="from first", pose="think")]),

    # ---------------- 5 · THE PASS ----------------
    dict(act=5, type="stats", src=PPPSRC, title="The pass, adjusted for prices",
         narration="So here's the pass, in the IMF's numbers. {p} In 2022, Estonia was still ahead, by about seven hundred dollars per person. {p} In 2023, Poland passed it, and finished the year about eighteen hundred dollars ahead. {pp} This year, the gap is about six thousand four hundred. And by 2031, in the IMF's forecast, about ten thousand.",
         stats=[dict(at="still ahead", value=E[2022], fmt="usd0", label="Estonia, 2022"), dict(at="about seven hundred", value=P[2022], fmt="usd0", label="Poland, 2022"), dict(at="eighteen hundred dollars ahead", value=P[2023] - E[2023], fmt="usd0", label="Poland ahead, 2023"), dict(at="about ten thousand", value=P[2031] - E[2031], fmt="usd0", label="Poland ahead, 2031 (IMF)")],
         react=[dict(at="here's the pass", pose="pointUp"), dict(at="still ahead", pose="think"), dict(at="Poland passed it", pose="cheer"), dict(at="about ten thousand", pose="shock")]),

    # ---------------- 6 · YOUR GUESS ----------------
    dict(act=6, type="host", bg="none",
         narration="<soft>So, what's your guess?</soft> {pp} Does Estonia come back, the way it did after 2009, {p} or has Poland left it behind for good? {pp} Tell me in the comments. {pp} If you're watching from Estonia: {p} does the stall feel real where you are? {pp} I read every comment.",
         items=[dict(at="your guess", text="Comeback or for good?", color="acc", size=66), dict(at="watching from Estonia", text="Estonia: does it match?", color="warm", size=58)],
         react=[dict(at="your guess", pose="shrug"), dict(at="Tell me", pose="pointUp"), dict(at="watching from Estonia", pose="wave")]),
    dict(act=6, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="JPN", color="acc", title="Poland passed Japan", sub="the one nobody noticed."),
         narration="And if you missed it, {p} this is the episode where Poland passed Japan. {pp} It's right here. {pp} I'm Chartbound. {p} See you in the next one.",
         hold=14,
         react=[dict(at="if you missed it", pose="pointL"), dict(at="See you", pose="wave")]),
]

checks = [
    dict(say="2007: EST 146% of POL; EST ≈ 27k (27,125), POL ≈ 18.5k (18,563)", rule="expr", expr=f"[round({E[2007]} / {P[2007]} * 100), round({E[2007]} / 1000), round({P[2007]} / 500) * 500]", equal=[146, 27, 18500]),
    dict(say="POL passed EST in 2023 (only crossing 1996–2031: 2023)", rule="expr", expr=f"{[y for y in range(1996, 2032) if (P[y] > E[y]) != (P[y - 1] > E[y - 1])]}", equal=[2023]),
    dict(say="2026: POL ≈ 12% ahead (11.9); 2031 ≈ 15% (15.4)", rule="expr", expr=f"[round(({P[2026]} / {E[2026]} - 1) * 100), round(({P[2031]} / {E[2031]} - 1) * 100)]", equal=[12, 15]),
    dict(say="EST/POL: 1995 103%, 2000 109%, 2007 146%", rule="expr", expr=f"[round({E[1995]} / {P[1995]} * 100), round({E[2000]} / {P[2000]} * 100), round({E[2007]} / {P[2007]} * 100)]", equal=[103, 109, 146]),
    dict(say="real 2000→2007: EST +68% (almost seventy), POL +31% (about thirty)", rule="expr", expr=f"[round(({grow('EST', 2000, 2007)} - 1) * 100), round(({grow('POL', 2000, 2007)} - 1) * 100)]", equal=[68, 31]),
    dict(say="EST growth 2008 −5.1 (shrank about five), 2009 −14.6 (fourteen and a half); POL 2009 +2.6", rule="expr", expr=f"[{GR['EST'][2008]}, {GR['EST'][2009]}, {GR['POL'][2009]}]", equal=[-5.1, -14.6, 2.6]),
    dict(say="EST 2023 −2.9 (shrank about three), 2024 0.1 (barely grew)", rule="expr", expr=f"[{GR['EST'][2023]}, {GR['EST'][2024]}]", equal=[-2.9, 0.1]),
    dict(say="POL: no negative year 1992–2031 except 2020", rule="expr", expr=f"{[y for y in range(1992, 2032) if GR['POL'][y] < 0]}", equal=[2020]),
    dict(say="real 2007→2025: EST +21%, POL +84%; ratio 4×", rule="expr", expr=f"[round(({grow('EST', 2007, 2025)} - 1) * 100), round(({grow('POL', 2007, 2025)} - 1) * 100), round(({grow('POL', 2007, 2025)} - 1) / ({grow('EST', 2007, 2025)} - 1))]", equal=[21, 84, 4]),
    dict(say="EST pop 2026 1.4M; POL/EST ≈ 27", rule="expr", expr=f"[round({LP['EST'][2026]}, 1), round({LP['POL'][2026]} / {LP['EST'][2026]})]", equal=[1.4, 27]),
    dict(say="USD 2026: EST ≈ 37,300, POL ≈ 31,200, EST +20%; 2031 EST +13%", rule="expr", expr=f"[round({N['EST'][2026]} / 100) * 100, round({N['POL'][2026]} / 100) * 100, round(({N['EST'][2026]} / {N['POL'][2026]} - 1) * 100), round(({N['EST'][2031]} / {N['POL'][2031]} - 1) * 100)]", equal=[37300, 31200, 20, 13]),
    dict(say="LTU 2007 ≈ 19% behind EST; LTU passed EST 2020; LTU 2026 +14% vs EST, +2% vs POL", rule="expr", expr=f"[round((1 - {L[2007]} / {E[2007]}) * 100), {L[2019] < E[2019]}, {L[2020] > E[2020]}, round(({L[2026]} / {E[2026]} - 1) * 100), round(({L[2026]} / {P[2026]} - 1) * 100)]", equal=[19, True, True, 14, 2]),
    dict(say="2022: EST 47970, POL 47245, gap ≈ 700; 2023: POL 49328, EST 47554, gap ≈ 1,800", rule="expr", expr=f"[{E[2022]}, {P[2022]}, round(({E[2022]} - {P[2022]}) / 100) * 100, {P[2023]}, {E[2023]}, round(({P[2023]} - {E[2023]}) / 100) * 100]", equal=[47970, 47245, 700, 49328, 47554, 1800]),
    dict(say="2026 gap ≈ 6,400; 2031 ≈ 10,000", rule="expr", expr=f"[round(({P[2026]} - {E[2026]}) / 100) * 100, round(({P[2031]} - {E[2031]}) / 1000) * 1000]", equal=[6400, 10000]),
    dict(say="EST 2000–2007 média ≈ 7,7%/ano ('one of the fastest-growing in Europe'; NÃO a mais rápida do Báltico: LTU cresceu mais)", rule="expr", expr=f"round(({grow('EST', 2000, 2007)} ** (1 / 7) - 1) * 100, 1)", equal=7.7),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="a-L30-poland-estonia", clips=[], channel="chartbound", chapter0="46%",
            thumb=dict(v="flags", iso="EST", vs="POL", sym="vs", big="2007: +46%", line2="2026: BEHIND"),
            w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks, datasets=[], snapshot=snapshot,
            voice=dict(model="", name="Charon",
                       style=("You are the narrator of a popular data documentary on YouTube. Read the script below in a warm, curious voice "
                              "with a little dry humor, at a relaxed but engaged pace of about 145 words per minute, like a smart friend telling "
                              "you something surprising. Let the big numbers land with a tiny pause before them. Keep the energy steady from the "
                              "first sentence to the last. Never sound like an advertisement or an audiobook.")),
            music=[dict(act=0, track="Lightless Dawn", vol=0.24), dict(act=1, track="Deliberate Thought", vol=0.22), dict(act=2, track="Hidden Agenda", vol=0.23), dict(act=3, track="Inspired", vol=0.23),
                   dict(act=4, track="Investigations", vol=0.23), dict(act=5, track="Deliberate Thought", vol=0.22), dict(act=6, track="Floating Cities", vol=0.24)],
            yt=dict(title="Estonia Was 46% Richer Than Poland. Then It Stalled.",
                    description=("Income per person adjusted for prices (IMF World Economic Outlook, October 2026): in 2007 the average Estonian was 46% ahead of the average Pole. "
                                 "In 2023 Poland passed; this year it's ~12% ahead, ~15% by 2031 in the IMF's forecast. Estonia's boom (+68% real growth 2000–2007), the 2009 crash (−14.6%), "
                                 "the 2023 recession, 2007–2025 real growth of ~21% vs ~84% for Poland, why Estonia is still ~20% ahead in plain dollars, and the Baltic race: Lithuania passed Estonia in 2020.\n\n"
                                 "Sources: IMF World Economic Outlook, October 2026 (PPPPC, NGDPDPC, NGDP_RPCH, LP). 2026+ figures are IMF estimates and forecasts.\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#poland #estonia #baltics #economics #imf #europe #data"),
                    tags=["poland", "estonia", "poland vs estonia", "baltic tiger", "lithuania", "baltics", "estonia economy", "poland economy", "gdp per capita", "imf", "economics", "polska", "eesti"], lang="en"))

json.dump(spec, open(os.path.join(HERE, "a-L30.json"), "w"), ensure_ascii=False, indent=1)
clean = lambda t: t.replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()
words = sum(len(clean(s["narration"])) for s in shots)
acts = {}
for s in shots:
    acts[s["act"]] = acts.get(s["act"], 0) + len(clean(s["narration"]))
print("shots", len(shots), "palavras", words, f"~{words / 145:.1f} min a 145 wpm", "por ato", acts)

"""Gera specs/long/a-L29.json — Chartbound longo #29: "Japan Was 16 Times Richer Than Poland. Now It's 14% Ahead." (série Polônia; sequência do hit XGmxZPO8lx8)
O hit mostrou a Polônia passando o Japão em PIB per capita ajustado por preços (PPPPC, 2026). Este episódio faz a pergunta seguinte: e em dólares
correntes (NGDPDPC, câmbio de mercado)? Medida dita na tela e na narração.
Dados: IMF WEO out/2026 (research/imf_ita_2026-11-07.json: POL, JPN completos 1990–2031; research/imf_twn_2026-11-05.json: KOR, TWN, USA em anos
selecionados, NGDPDPC). Inferência documentada: entre 2012 e 2024 o PIB real do Japão cresceu ~9% enquanto o PIB per capita em dólares caiu ~32% → câmbio."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "..", "..", "research", "imf_ita_2026-11-07.json")))
T = json.load(open(os.path.join(HERE, "..", "..", "research", "imf_twn_2026-11-05.json")))["NGDPDPC"]
ACTS = ["Cold open", "Sixteen times", "Japan's lost dollars", "Already passed", "Where Japan wins", "The pass", "Your guess"]
IMF = "IMF World Economic Outlook, October 2026"


def series(ind, iso):
    r = D[ind][iso]
    return {r["y0"] + k: v for k, v in enumerate(r["v"])}


N = {iso: series("NGDPDPC", iso) for iso in ("POL", "JPN")}
PP = {iso: series("PPPPC", iso) for iso in ("POL", "JPN")}
GR = {iso: series("NGDP_RPCH", iso) for iso in ("POL", "JPN")}
LP = {iso: series("LP", iso) for iso in ("POL", "JPN")}
LUR = {iso: series("LUR", iso) for iso in ("POL", "JPN")}
CPI = {iso: series("PCPIPCH", iso) for iso in ("POL", "JPN")}
DEBT = {iso: series("GGXWDG_NGDP", iso) for iso in ("POL", "JPN")}
P, J = N["POL"], N["JPN"]
TW = {iso: dict(zip(T["years"], T[iso])) for iso in ("TWN", "USA", "KOR", "JPN")}


def grow(iso, a, b):
    c = 1.0
    for y in range(a + 1, b + 1):
        c *= 1 + GR[iso][y] / 100
    return c


snapshot = []
for iso in ("POL", "JPN"):
    for y, v in N[iso].items():
        snapshot.append(dict(set="imfusd", iso=iso, year=y, value=v, src=IMF + " · NGDPDPC"))
    for y, v in PP[iso].items():
        snapshot.append(dict(set="imf", iso=iso, year=y, value=v, src=IMF + " · PPPPC"))
    for y, v in GR[iso].items():
        snapshot.append(dict(set="imfg", iso=iso, year=y, value=v, src=IMF + " · NGDP_RPCH"))
    for st, tab, ind in [("pop", LP, "LP"), ("debt", DEBT, "GGXWDG_NGDP"), ("lur", LUR, "LUR"), ("cpi", CPI, "PCPIPCH")]:
        for y, v in tab[iso].items():
            snapshot.append(dict(set=st, iso=iso, year=y, value=v, src=IMF + " · " + ind))
for y in range(1990, 2032):
    snapshot.append(dict(set="rat", iso="POL", year=y, value=round(P[y] / J[y] * 100, 2), src=IMF + " · Poland's GDP per capita (current US$) as % of Japan's"))

USDSRC = IMF + " · GDP per capita, current US$ at market exchange rates (NGDPDPC); 2026+ are IMF estimates and forecasts"
USD2 = dict(set="imfusd", fc=2025, series=["JPN", "POL"], years=[1990, 2031], y=[0, 55000], src=USDSRC, fmt="usd0", hl="POL")  # usd0: com usdk0, 1990 mostrava "$2k" para os US$ 1.634 narrados
RATCH = dict(set="rat", fc=2025, series=["POL"], years=[1990, 2031], y=[0, 110], src=IMF + " · Poland's GDP per capita in current US$, as % of Japan's; 2026+ are IMF estimates and forecasts", fmt="pct0", hl="POL", ref=dict(value=100, label="Japan = 100%", pos="left"))

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="lines", start=1990.0, **USD2,
         narration="Sixteen times. {p} In 1990, the average Japanese person produced sixteen times as much as the average Pole, in plain dollars: about twenty-six thousand four hundred dollars a year, against one thousand six hundred. {pp} This year, in the IMF's numbers: about thirty-five thousand four hundred in Japan, thirty-one thousand two hundred in Poland. Japan is about fourteen percent ahead. {p} And by 2031, in the IMF's forecast, the gap is two hundred and fifty-six dollars.",
         keys=[dict(at="Sixteen times", year=1990.0, dur=0.5), dict(at="This year", year=2026.0, dur=3.0), dict(at="fourteen percent ahead", year=2026.0, dur=1.0), dict(at="by 2031", year=2031.0, dur=2.5)],
         labels=[dict(at="twenty-six thousand four hundred", iso="JPN", year=1990), dict(at="against one thousand six hundred", iso="POL", year=1990), dict(at="thirty-five thousand four hundred", iso="JPN", year=2026), dict(at="thirty-one thousand two hundred", iso="POL", year=2026), dict(at="two hundred and fifty-six", iso="POL", year=2031)],
         react=[dict(at="Sixteen times", pose="shock"), dict(at="plain dollars", pose="pointUp"), dict(at="This year", pose="pointL"), dict(at="fourteen percent", pose="think"), dict(at="two hundred and fifty-six", pose="shock")]),
    dict(act=0, type="host", bg="lines", start=2031.0, **{k: v for k, v in USD2.items() if k != "src"},
         narration="This year, on income adjusted for prices, the IMF's numbers put Poland ahead of Japan. That was one of the biggest stories on this channel. But adjusted for prices isn't the money people see on a payslip converted into dollars. {p} So here's the plain money: market exchange rates, no adjustment. {pp} <soft>And the surprising part of this chart isn't Poland. It's Japan. In plain dollars, the average Japanese person produces less this year than in 1995.</soft>",
         items=[dict(at="adjusted for prices", text="2026: Poland > Japan (PPP)", color="acc", size=58), dict(at="plain money", text="Plain dollars", serif=True, size=66, color="acc2"), dict(at="less this year than in 1995", text="Japan: $44,960 → $35,400", color="warm", size=58)],
         react=[dict(at="This year", pose="pointL"), dict(at="biggest stories", pose="cheer"), dict(at="plain money", pose="pointUp"), dict(at="It's Japan", pose="shock")]),

    # ---------------- 1 · SIXTEEN TIMES ----------------
    dict(act=1, type="host", bg="none",
         narration="Quick one before the chart: this channel is a series about who's passing whom. Subscribe so you don't miss the next one. {p} Now, the long view.",
         items=[dict(at="who's passing whom", text="Who passed whom", serif=True, size=66, color="acc"), dict(at="Subscribe", text="Subscribe", size=70)],
         react=[dict(at="Quick one", pose="wave"), dict(at="Subscribe", pose="cheer"), dict(at="the long view", pose="pointL")]),
    dict(act=1, type="lines", start=1990.0, **RATCH,
         narration="Here's Poland as a share of Japan, in plain dollars. {p} 1990: six percent. In 1990, the average Japanese person produced more than the average American. Poland was coming out of communism. {p} By 2004, when Poland joined the European Union, it was at seventeen percent. 2012: twenty-six. {pp} Then the line turns almost straight up. Fifty-three percent in 2022. Seventy-four in 2024. Eighty-eight this year. That's thirty-five points in four years. Poland didn't suddenly get that much faster. Something happened to Japan.",
         keys=[dict(at="1990: six percent", year=1990.0, dur=1.5), dict(at="By 2004", year=2004.0, dur=1.5), dict(at="2012: twenty-six", year=2012.0, dur=1.5), dict(at="Fifty-three percent in 2022", year=2022.0, dur=1.0), dict(at="Seventy-four in 2024", year=2024.0, dur=1.0), dict(at="Eighty-eight this year", year=2026.0, dur=2.5)],
         labels=[dict(at="1990: six percent", iso="POL", year=1990), dict(at="By 2004", iso="POL", year=2004), dict(at="2012: twenty-six", iso="POL", year=2012), dict(at="Fifty-three percent in 2022", iso="POL", year=2022), dict(at="Eighty-eight this year", iso="POL", year=2026)],
         react=[dict(at="six percent", pose="shock"), dict(at="the average American", pose="think"), dict(at="almost straight up", pose="shock"), dict(at="thirty-five points", pose="pointUp"), dict(at="Something happened to Japan", pose="think")]),

    # ---------------- 2 · JAPAN'S LOST DOLLARS ----------------
    dict(act=2, type="lines", set="imfusd", fc=2025, series=["JPN"], years=[1990, 2031], start=1995.0, y=[0, 55000], src=USDSRC, fmt="usd0", hl="JPN",
         narration="Here's Japan alone, in plain dollars per person. {p} 1995: about forty-five thousand. Then thirty years of going sideways. The peak came in 2012, at almost fifty thousand. {pp} And then, from 2012 to 2024, it fell by almost a third, to about thirty-four thousand. {p} Did Japan's economy collapse? No. After inflation, it grew about nine percent over those twelve years. Slowly, but it grew. What collapsed was the value of the yen in dollars. Same work, same output, fewer dollars.",
         keys=[dict(at="1995", year=1995.0, dur=1.5), dict(at="going sideways", year=2005.0, dur=2.0), dict(at="The peak came in 2012", year=2012.0, dur=2.0), dict(at="fell by almost a third", year=2024.0, dur=2.5)],
         labels=[dict(at="1995", iso="JPN", year=1995), dict(at="The peak came in 2012", iso="JPN", year=2012), dict(at="about thirty-four thousand", iso="JPN", year=2024)],
         react=[dict(at="Japan alone", pose="pointL"), dict(at="going sideways", pose="shrug"), dict(at="almost a third", pose="shock"), dict(at="Did Japan's economy collapse", pose="think"), dict(at="fewer dollars", pose="pointUp")]),
    dict(act=2, type="stats", src=IMF + " · real GDP growth (NGDP_RPCH, compounded), population (LP)", title="Slow growth, fewer people",
         narration="Underneath the yen, there's a slower story too. Since 1995, after inflation, Japan's economy has grown about twenty-five percent. Poland's has more than tripled. {p} And Japan's population peaked in 2011, at about a hundred and twenty-eight million. This year it's about a hundred and twenty-three, and the IMF has a hundred and nineteen by 2031. {pp} The IMF expects Japan to grow well under one percent a year until 2031.",
         stats=[dict(at="about twenty-five percent", value=round((grow("JPN", 1995, 2025) - 1) * 100), fmt="pct0", label="Japan, real growth 1995–2025"), dict(at="more than tripled", value=round(grow("POL", 1995, 2025), 1), fmt="dec1", label="Poland, 2025 vs 1995 (×)"), dict(at="a hundred and twenty-three", value=round(LP["JPN"][2026], 1), fmt="dec1", label="million people in Japan, 2026 (2011: 127.8)"), dict(at="well under one percent", value=GR["JPN"][2028], fmt="pct1", label="Japan, IMF growth forecast 2028")],
         react=[dict(at="slower story", pose="think"), dict(at="more than tripled", pose="cheer"), dict(at="peaked in 2011", pose="pointL"), dict(at="well under one percent", pose="shrug")]),

    # ---------------- 3 · ALREADY PASSED ----------------
    dict(act=3, type="stats", src=IMF + " · NGDPDPC (current US$), selected years", title="Already ahead of Japan",
         narration="Poland isn't the first to close in on Japan in plain dollars. Two of Japan's neighbors already passed it. {p} In 2020, the average South Korean and the average Taiwanese both produced less than the average Japanese person. By 2024, both were ahead. {pp} This year, in the IMF's numbers: South Korea about forty-three and a half thousand dollars per person, Taiwan about forty-four thousand, Japan about thirty-five thousand four hundred. {p} In 1990, Japan was more than three times as rich as Taiwan, in plain dollars, and almost four times as rich as South Korea.",
         stats=[dict(at="South Korea about forty-three and a half thousand", value=TW["KOR"][2026], fmt="usd0", label="South Korea, 2026"), dict(at="Taiwan about forty-four thousand", value=TW["TWN"][2026], fmt="usd0", label="Taiwan, 2026"), dict(at="Japan about thirty-five thousand four hundred", value=TW["JPN"][2026], fmt="usd0", label="Japan, 2026"), dict(at="more than three times", value=round(TW["JPN"][1990] / TW["TWN"][1990], 1), fmt="dec1", label="Japan ÷ Taiwan, 1990 (×)")],
         react=[dict(at="isn't the first", pose="think"), dict(at="already passed", pose="shock"), dict(at="both were ahead", pose="pointUp"), dict(at="more than three times", pose="shock")]),

    # ---------------- 4 · WHERE JAPAN WINS ----------------
    dict(act=4, type="host", bg="none",
         narration="And if you're enjoying this, the subscribe button is right there. {p} Now, to be fair to Japan: where it still wins.",
         items=[dict(at="subscribe button", text="Subscribe", size=66), dict(at="still wins", text="Where Japan wins", serif=True, size=66, color="acc")],
         react=[dict(at="subscribe button", pose="pointUp"), dict(at="still wins", pose="cheer")]),
    dict(act=4, type="duel", set="lur", year=2026, a="JPN", b="POL", fmt="dec1", src=IMF + " · unemployment rate (% of labor force), 2026 estimate", title="Unemployment, 2026", badge="LOWER IN JAPAN",
         cues=[dict(at="two point five", show="a"), dict(at="three point two", show="b")],
         narration="Unemployment this year: about two point five percent in Japan, {pp} three point two in Poland. And inflation: in 2022, prices rose two and a half percent in Japan, and more than fourteen percent in Poland. {p} Where Poland wins is debt: about sixty-seven percent of the economy in Poland, about two hundred percent in Japan, one of the highest in the world.",
         react=[dict(at="Unemployment", pose="pointUp"), dict(at="more than fourteen", pose="shock"), dict(at="Where Poland wins", pose="cheer"), dict(at="two hundred percent", pose="shock")]),

    # ---------------- 5 · THE PASS ----------------
    dict(act=5, type="lines", start=2019.0, **{**USD2, "years": [2010, 2031]},
         narration="So, does Poland pass Japan in plain dollars too? {p} In the IMF's forecast: next year, Japan about thirty-six thousand six hundred dollars per person, Poland about thirty-three thousand three hundred. 2030: forty thousand seven hundred against thirty-nine thousand five hundred. {pp} And 2031: forty-one thousand nine hundred and fifty-three in Japan, forty-one thousand six hundred and ninety-seven in Poland. Two hundred and fifty-six dollars apart. Ninety-nine percent. {p} That's not a pass. It's a coin flip, and it depends on the yen as much as on Poland.",
         keys=[dict(at="does Poland pass Japan", year=2026.0, dur=1.5), dict(at="next year", year=2027.0, dur=1.5), dict(at="2030", year=2030.0, dur=1.5), dict(at="And 2031", year=2031.0, dur=3.0)],
         labels=[dict(at="next year", iso="POL", year=2027), dict(at="forty-one thousand nine hundred and fifty-three", iso="JPN", year=2031), dict(at="forty-one thousand six hundred and ninety-seven", iso="POL", year=2031)],
         react=[dict(at="does Poland pass", pose="think"), dict(at="next year", pose="pointL"), dict(at="Two hundred and fifty-six", pose="shock"), dict(at="coin flip", pose="shrug")]),
    dict(act=5, type="host", bg="none",
         narration="Think about what that means. In 1990, the average Pole produced six percent of what the average Japanese person did. Today, the average Pole produces about eighty-eight percent of what the average Japanese person does, in the same dollars. {p} And adjusted for what money buys at home, Poland is already ahead. {pp} Japan isn't poor. But in plain money, the gap that defined the last thirty-five years is almost gone.",
         items=[dict(at="In 1990", text="1990: 6%", color="warm", size=62), dict(at="eighty-eight percent", text="2026: 88%", serif=True, size=64, color="acc"), dict(at="already ahead", text="PPP: Poland ahead", color="acc2", size=58)],
         react=[dict(at="Think about", pose="think"), dict(at="six percent", pose="shrug"), dict(at="already ahead", pose="cheer"), dict(at="almost gone", pose="pointUp")]),

    # ---------------- 6 · YOUR GUESS ----------------
    dict(act=6, type="host", bg="none",
         narration="<soft>So, your guess: does Poland pass Japan in plain dollars by 2031, or does the yen bounce back first?</soft> Tell me in the comments. {p} If you're watching from Japan: does this match what you see in your own wallet? {p} If you're in Poland: did you ever expect to be this close? {p} I read every comment.",
         items=[dict(at="your guess", text="2031: pass or not?", color="acc", size=66), dict(at="watching from Japan", text="Japan: does it match?", color="warm", size=58)],
         react=[dict(at="your guess", pose="shrug"), dict(at="Tell me", pose="pointUp"), dict(at="watching from Japan", pose="wave")]),
    dict(act=6, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="JPN", color="acc", title="Poland passed Japan", sub="adjusted for prices."),
         narration="And if you missed it, here's the episode where Poland passed Japan, adjusted for prices. It's right here. {p} I'm Chartbound. See you in the next one.",
         hold=14,
         react=[dict(at="if you missed it", pose="pointL"), dict(at="See you", pose="wave")]),
]

R = {y: P[y] / J[y] for y in range(1990, 2032)}
checks = [
    dict(say="1990: JPN 26399 (≈26,400), POL 1634 (≈1,600), 16×", rule="expr", expr=f"[round({J[1990]} / 100) * 100, round({P[1990]} / 100) * 100, round({J[1990]} / {P[1990]})]", equal=[26400, 1600, 16]),
    dict(say="2026: JPN ≈ 35,400, POL ≈ 31,200, Japan +14% (13.5)", rule="expr", expr=f"[round({J[2026]} / 100) * 100, round({P[2026]} / 100) * 100, round(({J[2026]} / {P[2026]} - 1) * 100)]", equal=[35400, 31200, 14]),
    dict(say="2031: JPN 41953, POL 41697, gap 256, 99%", rule="expr", expr=f"[{J[2031]}, {P[2031]}, {J[2031] - P[2031]}, round({R[2031]} * 100)]", equal=[41953, 41697, 256, 99]),
    dict(say="PPP: POL > JPN in 2026 (first year)", rule="expr", expr=f"[{PP['POL'][2026] > PP['JPN'][2026]}, {PP['POL'][2025] < PP['JPN'][2025]}]", equal=[True, True]),
    dict(say="JPN USD 2026 (35,400) < 1995 (44,960)", rule="expr", expr=f"[{J[2026] < J[1995]}, {J[1995]}]", equal=[True, 44960]),
    dict(say="1990 JPN > USA (26,399 vs 23,848)", rule="expr", expr=f"{TW['JPN'][1990] > TW['USA'][1990]}", equal=True),
    dict(say="POL/JPN: 1990 6%, 2004 17%, 2012 26%, 2022 53%, 2024 74%, 2026 88% (+35 in 4 years)", rule="expr", expr=f"[round({R[1990]} * 100), round({R[2004]} * 100), round({R[2012]} * 100), round({R[2022]} * 100), round({R[2024]} * 100), round({R[2026]} * 100), round({R[2026]} * 100) - round({R[2022]} * 100)]", equal=[6, 17, 26, 53, 74, 88, 35]),
    dict(say="JPN USD 1995 ≈ 45k; peak 2012 49,657 (almost fifty); 2024 ≈ 34k; fall 2012→2024 −32% (almost a third)", rule="expr", expr=f"[round({J[1995]} / 1000), {max(J, key=J.get)}, round({J[2024]} / 1000), round(({J[2024]} / {J[2012]} - 1) * 100)]", equal=[45, 2012, 34, -32]),
    dict(say="JPN real growth 2012→2024 +9%", rule="expr", expr=f"round(({grow('JPN', 2012, 2024)} - 1) * 100)", equal=9),
    dict(say="real 1995→2025: JPN +25%, POL ×3.1 (more than tripled)", rule="expr", expr=f"[round(({grow('JPN', 1995, 2025)} - 1) * 100), round({grow('POL', 1995, 2025)}, 1)]", equal=[25, 3.1]),
    dict(say="JPN population peak 2011 ≈ 128 (127.8); 2026 ≈ 123 (122.7); 2031 ≈ 119", rule="expr", expr=f"[{max(LP['JPN'], key=LP['JPN'].get)}, round({max(LP['JPN'].values())}, 1), round({LP['JPN'][2026]}), round({LP['JPN'][2031]})]", equal=[2011, 127.8, 123, 119]),
    dict(say="JPN growth 2027–2031 all < 1 (well under one)", rule="expr", expr=f"{all(GR['JPN'][y] < 1 for y in range(2027, 2032))}", equal=True),
    dict(say="KOR, TWN < JPN in 2020; > JPN in 2024", rule="expr", expr=f"[{TW['KOR'][2020] < TW['JPN'][2020]}, {TW['TWN'][2020] < TW['JPN'][2020]}, {TW['KOR'][2024] > TW['JPN'][2024]}, {TW['TWN'][2024] > TW['JPN'][2024]}]", equal=[True, True, True, True]),
    dict(say="2026: KOR ≈ 43.5k, TWN ≈ 44k, JPN ≈ 35.4k (twn file = ita file)", rule="expr", expr=f"[round({TW['KOR'][2026]} / 500) * 500, round({TW['TWN'][2026]} / 1000), round({TW['JPN'][2026]} / 100) * 100, {TW['JPN'][2026] == J[2026]}]", equal=[43500, 44, 35400, True]),
    dict(say="1990: JPN/TWN 3.2 (more than three), JPN/KOR 3.9 (almost four)", rule="expr", expr=f"[round({TW['JPN'][1990]} / {TW['TWN'][1990]}, 1), round({TW['JPN'][1990]} / {TW['KOR'][1990]}, 1)]", equal=[3.2, 3.9]),
    dict(say="unemployment 2026: JPN 2.5, POL 3.2; inflation 2022 JPN 2.5, POL 14.4; debt 2026 POL ≈ 67, JPN ≈ 199 (about two hundred)", rule="expr", expr=f"[{LUR['JPN'][2026]}, {LUR['POL'][2026]}, {CPI['JPN'][2022]}, {CPI['POL'][2022]}, round({DEBT['POL'][2026]}), round({DEBT['JPN'][2026]})]", equal=[2.5, 3.2, 2.5, 14.4, 67, 199]),
    dict(say="2027: JPN ≈ 36,600, POL ≈ 33,300; 2030: JPN ≈ 40,700, POL ≈ 39,500", rule="expr", expr=f"[round({J[2027]} / 100) * 100, round({P[2027]} / 100) * 100, round({J[2030]} / 100) * 100, round({P[2030]} / 100) * 100]", equal=[36600, 33300, 40700, 39500]),
    dict(say="POL still behind JPN every year 2026–2031 (not a pass)", rule="expr", expr=f"{all(P[y] < J[y] for y in range(2026, 2032))}", equal=True),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="a-L29-poland-japan-usd", clips=[], channel="chartbound", chapter0="16 times",
            thumb=dict(v="flags", iso="JPN", vs="POL", sym="vs", big="16× → 1.1×", line2="PLAIN DOLLARS"),
            w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks, datasets=[], snapshot=snapshot,
            voice=dict(model="", name="Charon",
                       style=("You are the narrator of a popular data documentary on YouTube. Read the script below in a warm, curious voice "
                              "with a little dry humor, at a relaxed but engaged pace of about 145 words per minute, like a smart friend telling "
                              "you something surprising. Let the big numbers land with a tiny pause before them. Keep the energy steady from the "
                              "first sentence to the last. Never sound like an advertisement or an audiobook.")),
            music=[dict(act=0, track="Lightless Dawn", vol=0.24), dict(act=1, track="Deliberate Thought", vol=0.22), dict(act=2, track="Hidden Agenda", vol=0.23), dict(act=3, track="Inspired", vol=0.23),
                   dict(act=4, track="Investigations", vol=0.23), dict(act=5, track="Deliberate Thought", vol=0.22), dict(act=6, track="Floating Cities", vol=0.24)],
            yt=dict(title="Japan Was 16 Times Richer Than Poland. Now It's 14% Ahead.",
                    description=("Income per person in plain US dollars, at market exchange rates (IMF World Economic Outlook, October 2026): in 1990 the average Japanese person produced 16× as much as the average Pole "
                                 "($26,399 vs $1,634). In 2026: $35,400 vs $31,186 — Japan ~14% ahead — and in the IMF's 2031 forecast the gap is $256. "
                                 "Why Japan's dollar income is lower than in 1995 (peak 2012, −32% by 2024 while the real economy grew ~9%: the yen), slow growth and a shrinking population, "
                                 "South Korea and Taiwan already ahead of Japan in plain dollars, and where Japan still wins (unemployment, inflation) and loses (debt ~200% of GDP).\n"
                                 "Adjusted for prices (PPP), Poland already passed Japan in 2026 — that's the previous episode.\n\n"
                                 "Sources: IMF World Economic Outlook, October 2026 (NGDPDPC, PPPPC, NGDP_RPCH, LP, LUR, GGXWDG_NGDP, PCPIPCH). 2026+ figures are IMF estimates and forecasts.\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#poland #japan #yen #economics #imf #data"),
                    tags=["poland", "japan", "poland vs japan", "japan economy", "yen", "weak yen", "poland economy", "gdp per capita", "imf", "economics", "polska", "japonia", "日本"], lang="en"))

json.dump(spec, open(os.path.join(HERE, "a-L29.json"), "w"), ensure_ascii=False, indent=1)
clean = lambda t: t.replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()
words = sum(len(clean(s["narration"])) for s in shots)
acts = {}
for s in shots:
    acts[s["act"]] = acts.get(s["act"], 0) + len(clean(s["narration"]))
print("shots", len(shots), "palavras", words, f"~{words / 145:.1f} min a 145 wpm", "por ato", acts)

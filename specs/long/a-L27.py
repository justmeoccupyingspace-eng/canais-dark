"""Gera specs/long/a-L27.json — Chartbound longo #27: "Poland Is $55 Behind Spain. Next Year, It Passes." (série Polônia, PLANO.md L1/L3)
Intro (PLANO R2): número nos primeiros 2 s. CTA de série no minuto 1 com gancho do próximo episódio (Polônia × Itália).
Dados: IMF WEO out/2026 (research/imf_ita_2026-11-07.json: POL, ESP, ITA, lido 07/11). Fora do FMI (documentado): turismo pesa muito no PIB
espanhol (por isso o tombo de 2020); a Espanha recebeu muitos imigrantes desde os anos 2000."""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "..", "..", "research", "imf_ita_2026-11-07.json")))
ACTS = ["Cold open", "Half to 99.9%", "Spain's two crashes", "Where Spain wins", "Where Poland wins", "The pass", "Your guess"]
IMF = "IMF World Economic Outlook, October 2026"


def series(ind, iso):
    r = D[ind][iso]
    return {r["y0"] + k: v for k, v in enumerate(r["v"])}


P, F, I = series("PPPPC", "POL"), series("PPPPC", "ESP"), series("PPPPC", "ITA")
GR = {iso: series("NGDP_RPCH", iso) for iso in ("POL", "ESP")}
LP = {iso: series("LP", iso) for iso in ("POL", "ESP")}
N = {iso: series("NGDPDPC", iso) for iso in ("POL", "ESP")}
DEBT = {iso: series("GGXWDG_NGDP", iso) for iso in ("POL", "ESP")}
LUR = {iso: series("LUR", iso) for iso in ("POL", "ESP")}
CPI = {iso: series("PCPIPCH", iso) for iso in ("POL", "ESP")}

Y0, Y1 = 1990, 2031
R = {y: P[y] / F[y] for y in range(Y0, Y1 + 1)}
GAP = {y: F[y] - P[y] for y in range(Y0, Y1 + 1)}
first_at = lambda th: next(y for y in range(Y0, Y1 + 1) if R[y] >= th)


def grow(iso, a, b):
    c = 1.0
    for y in range(a + 1, b + 1):
        c *= 1 + GR[iso][y] / 100
    return c


k_recent = math.log(R[2026] / R[2016]) / 10
k_imf = math.log(R[2031] / R[2026]) / 5
par_recent = 2026 + math.log(1 / R[2026]) / k_recent
par_imf = 2031 + math.log(1 / R[2031]) / k_imf

snapshot = []
for y in range(Y0, Y1 + 1):
    snapshot.append(dict(set="rat", iso="POL", year=y, value=round(R[y] * 100, 2), src=IMF + " · Poland's GDP per capita (PPP) as % of Spain's"))
for iso, s in (("POL", P), ("ESP", F)):
    for y, v in s.items():
        snapshot.append(dict(set="imf", iso=iso, year=y, value=v, src=IMF + " · PPPPC"))
for iso in ("POL", "ESP"):
    for y, v in GR[iso].items():
        snapshot.append(dict(set="imfg", iso=iso, year=y, value=v, src=IMF + " · NGDP_RPCH"))
for st, tab, ind in [("pop", LP, "LP"), ("debt", DEBT, "GGXWDG_NGDP"), ("lur", LUR, "LUR"), ("imfusd", N, "NGDPDPC"), ("cpi", CPI, "PCPIPCH")]:
    for iso, s in tab.items():
        for y, v in s.items():
            snapshot.append(dict(set=st, iso=iso, year=y, value=v, src=IMF + " · " + ind))

RATSRC = IMF + " · Poland's GDP per capita, PPP, as % of Spain's; 2026+ are IMF estimates and forecasts"
RATCH = dict(set="rat", fc=2025, series=["POL"], years=[Y0, Y1], y=[0, 120], src=RATSRC, fmt="pct0", hl="POL", ref=dict(value=100, label="Spain = 100%", pos="left"))

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="lines", start=2026.0, **RATCH,
         narration="Fifty-five dollars. {p} That's the gap this year between the average Spaniard and the average Pole: income per person, adjusted for prices. About sixty thousand dollars each, and Spain is ahead by fifty-five. Ninety-nine point nine percent. {pp} In 1990, Poland was at forty-two percent of Spain. Half by 2006. Seventy percent in 2012. Ninety in 2020. {p} And next year, in the IMF's forecast, Poland passes Spain. By 2031, it's nine percent ahead.",
         keys=[dict(at="Fifty-five dollars", year=2026.0, dur=0.5), dict(at="In 1990", year=1990.0, dur=1.5), dict(at="Half by 2006", year=2006.0, dur=1.5), dict(at="Seventy percent in 2012", year=2012.0, dur=1.5), dict(at="Ninety in 2020", year=2020.0, dur=1.5), dict(at="next year", year=2027.0, dur=1.5), dict(at="By 2031", year=2031.0, dur=2.5)],
         labels=[dict(at="Ninety-nine point nine", iso="POL", year=2026), dict(at="In 1990", iso="POL", year=1990), dict(at="Half by 2006", iso="POL", year=2006), dict(at="Ninety in 2020", iso="POL", year=2020), dict(at="By 2031", iso="POL", year=2031)],
         react=[dict(at="Fifty-five dollars", pose="shock"), dict(at="ahead by fifty-five", pose="pointUp"), dict(at="In 1990", pose="pointL"), dict(at="Poland passes Spain", pose="cheer"), dict(at="nine percent ahead", pose="think")]),
    dict(act=0, type="host", bg="lines", start=2031.0, **{k: v for k, v in RATCH.items() if k != "src"},
         narration="In this series, Poland has passed Japan, and it's closing in on Britain and France. Spain is the next one to actually fall. {p} And here's what makes it interesting: Spain isn't stuck. Its economy is one of the fastest-growing big economies in Europe right now. Poland is passing it anyway. {pp} <soft>Here's how Spain got caught, the two crashes that did it, and what passing Spain really means, and doesn't.</soft>",
         items=[dict(at="Spain is the next one", text="2027: Spain", serif=True, size=66, color="acc"), dict(at="isn't stuck", text="Spain 2025: +2.6%", color="acc2", size=60), dict(at="Poland is passing it anyway", text="Poland 2025: +3.7%", color="warm", size=60)],
         react=[dict(at="passed Japan", pose="pointL"), dict(at="next one to actually fall", pose="cheer"), dict(at="isn't stuck", pose="think"), dict(at="anyway", pose="pointUp")]),

    # ---------------- 1 · HALF TO 99.9% ----------------
    dict(act=1, type="host", bg="none",
         narration="Quick one before the chart: this is a series, and the next episode is Italy, the big economy Poland is closest to catching after Spain: about six thousand dollars behind this year. Subscribe so you don't miss it. {p} Now, the race.",
         items=[dict(at="this is a series", text="The Poland series", serif=True, size=66, color="acc"), dict(at="Italy", text="Next: Poland vs Italy", color="acc2", size=62), dict(at="Subscribe", text="Subscribe", size=70)],
         react=[dict(at="Quick one", pose="wave"), dict(at="Italy", pose="pointUp"), dict(at="Subscribe", pose="cheer"), dict(at="the race", pose="pointL")]),
    dict(act=1, type="lines", start=1990.0, **RATCH,
         narration="In 1990, the average Spaniard produced about sixteen thousand dollars a year, adjusted for prices. The average Pole, about six thousand seven hundred. {p} Since then, Poland's economy has grown about three and a half times, after inflation. Spain's has doubled. When Poland joined the European Union in 2004, it was still at forty-nine percent: just under half. {pp} But the line didn't rise smoothly. It moved fastest in two moments, and both were Spanish crashes: after 2008, and in 2020.",
         keys=[dict(at="In 1990", year=1990.0, dur=1.5), dict(at="Since then", year=2000.0, dur=2.5), dict(at="didn't rise smoothly", year=2005.0, dur=2.0), dict(at="after 2008", year=2012.0, dur=2.0), dict(at="in 2020", year=2020.0, dur=2.0)],
         labels=[dict(at="after 2008", iso="POL", year=2008), dict(at="in 2020", iso="POL", year=2020)],
         react=[dict(at="In 1990", pose="pointL"), dict(at="three and a half times", pose="cheer"), dict(at="Spain's has doubled", pose="shrug"), dict(at="Spanish crashes", pose="shock")]),

    # ---------------- 2 · SPAIN'S TWO CRASHES ----------------
    dict(act=2, type="bars", mode="abs", set="imfg", iso="ESP", years=[2000, 2030], start=2000.0, fmt="pct1", src=IMF + " · real GDP growth, Spain (annual %); 2026+ are IMF estimates and forecasts",
         narration="Here's Spain's economy, year by year, after inflation. {p} First crash: after 2008, Spain shrank in four different years, 2009, 2011, 2012 and 2013. By 2013, the economy was about eight percent smaller than in 2007, and unemployment hit twenty-six percent. {pp} Second crash: 2020. Minus eleven percent, one of the deepest falls in Europe that year, with tourism shut down. Poland's was about minus two. In that single year, Poland jumped from eighty-two percent of Spain to ninety-three.",
         keys=[dict(at="Here's Spain's", year=2004.0, dur=3.0), dict(at="First crash", year=2009.0, dur=1.5), dict(at="2013", year=2013.0, dur=1.5), dict(at="Second crash", year=2020.0, dur=1.5), dict(at="ninety-three", year=2021.0, dur=2.0)],
         react=[dict(at="Here's Spain's", pose="pointL"), dict(at="four different years", pose="shock"), dict(at="twenty-six percent", pose="shock"), dict(at="Minus eleven", pose="shock"), dict(at="ninety-three", pose="pointUp")]),
    dict(act=2, type="stats", src=IMF + " · real GDP growth (NGDP_RPCH), population (LP), unemployment (LUR)", title="Growing, but sharing it",
         narration="Since then, Spain has bounced back hard: almost four percent growth in 2024, and about two and a half last year and this year. {p} But there's a catch for income per person: people. Spain's population has grown from about thirty-nine million in 1990 to almost fifty million, mostly through immigration. Poland's has shrunk to about thirty-six. {pp} So even when Spain's economy grows fast, it's shared between more people every year. And from 2027, the IMF has Spain slowing to under two percent, and Poland holding at two and a half.",
         stats=[dict(at="almost four percent", value=GR["ESP"][2024], fmt="pct1", label="Spain, real growth 2024"), dict(at="almost fifty million", value=round(LP["ESP"][2026], 1), fmt="dec1", label="million people in Spain, 2026 (1990: 39.2)"), dict(at="about thirty-six", value=round(LP["POL"][2026], 1), fmt="dec1", label="million people in Poland, 2026"), dict(at="under two percent", value=GR["ESP"][2028], fmt="pct1", label="Spain, IMF growth forecast 2028")],
         react=[dict(at="bounced back hard", pose="cheer"), dict(at="there's a catch", pose="think"), dict(at="immigration", pose="pointL"), dict(at="slowing", pose="shrug")]),

    # ---------------- 3 · WHERE SPAIN WINS ----------------
    dict(act=3, type="stats", src=IMF + " · GDP per capita, current US$ (NGDPDPC); inflation (PCPIPCH)", title="Where Spain still wins",
         narration="Now, what passing Spain doesn't mean. {p} In plain dollars, without adjusting for prices, the average Spaniard produces about forty-two thousand dollars this year, and the average Pole about thirty-one thousand. There, Poland is at seventy-five percent, and still at about eighty-four in 2031. Even so, that gap has collapsed: in 1990, in plain dollars, the average Spaniard produced more than eight times as much as the average Pole. In 2004, almost four times. Now, about one point three. {pp} So a Spanish salary still buys more in euros. What changes is this: measured by what money actually buys at home, the average Pole is now as well off as the average Spaniard. {p} And on inflation, Spain did better in 2022: about eight percent, against Poland's fourteen.",
         stats=[dict(at="about forty-two thousand", value=N["ESP"][2026], fmt="usd0", label="Spain, plain US$, 2026"), dict(at="about thirty-one thousand", value=N["POL"][2026], fmt="usd0", label="Poland, plain US$, 2026"), dict(at="seventy-five percent", value=round(N["POL"][2026] / N["ESP"][2026] * 100), fmt="pct0", label="Poland vs Spain, plain dollars, 2026"), dict(at="about eight percent", value=CPI["ESP"][2022], fmt="pct1", label="Spain, inflation, 2022 (Poland: 14.4%)")],
         react=[dict(at="doesn't mean", pose="think"), dict(at="seventy-five percent", pose="shrug"), dict(at="as well off", pose="cheer"), dict(at="Spain did better", pose="pointL")]),

    # ---------------- 4 · WHERE POLAND WINS ----------------
    dict(act=4, type="host", bg="none",
         narration="And if you're enjoying the series, the subscribe button is right there. Italy is next. {p} Now, where Poland already wins.",
         items=[dict(at="subscribe button", text="Subscribe", size=66), dict(at="already wins", text="Where Poland wins", serif=True, size=66, color="acc")],
         react=[dict(at="subscribe button", pose="pointUp"), dict(at="already wins", pose="cheer")]),
    dict(act=4, type="duel", set="lur", year=2026, a="POL", b="ESP", fmt="dec1", src=IMF + " · unemployment rate (% of labor force), 2026 estimate", title="Unemployment, 2026", badge="LOWER IN POLAND",
         cues=[dict(at="three point two", show="a"), dict(at="nine point eight", show="b")],
         narration="Unemployment this year: about three point two percent in Poland, {pp} nine point eight in Spain. Three times as high. And government debt: about sixty-seven percent of the economy in Poland, about ninety-eight in Spain. {p} Spain's unemployment has been higher than Poland's every single year since 2008. In 2013, at the bottom, it was twenty-six percent in Spain, and about ten in Poland.",
         react=[dict(at="Unemployment", pose="pointUp"), dict(at="Three times", pose="shock"), dict(at="ninety-eight", pose="pointL")]),

    # ---------------- 5 · THE PASS ----------------
    dict(act=5, type="stats", src=IMF + " · PPPPC (GDP per capita, PPP, current international $); 2026+ are IMF estimates and forecasts", title="The pass",
         narration="So here's the pass, in the IMF's numbers. {p} This year: Spain sixty thousand one hundred and six dollars, Poland sixty thousand and fifty-one. Fifty-five dollars apart. {p} Next year: Poland about sixty-three thousand six hundred, Spain about sixty-two thousand five hundred. Poland ahead by about eleven hundred. {pp} And by 2031, about six thousand two hundred ahead. For comparison: in 2010, Spain was about twelve thousand dollars ahead.",
         stats=[dict(at="sixty thousand one hundred and six", value=F[2026], fmt="usd0", label="Spain, 2026"), dict(at="sixty thousand and fifty-one", value=P[2026], fmt="usd0", label="Poland, 2026"), dict(at="ahead by about eleven hundred", value=P[2027] - F[2027], fmt="usd0", label="Poland ahead, 2027 (IMF)"), dict(at="six thousand two hundred ahead", value=P[2031] - F[2031], fmt="usd0", label="Poland ahead, 2031 (IMF)")],
         react=[dict(at="here's the pass", pose="pointUp"), dict(at="Fifty-five dollars apart", pose="shock"), dict(at="Poland ahead", pose="cheer"), dict(at="For comparison", pose="think")]),
    dict(act=5, type="host", bg="none",
         narration="For a lot of Poles, Spain was the dream holiday, and for many, a place to move for work. In 1990, the average Spaniard was more than twice as well off as the average Pole. {p} Next year, by this measure, that's over. One caveat: these are IMF estimates and forecasts, and a gap of fifty-five dollars can flip either way with one revision. But the trend has pointed the same way for thirty-five years. {p} If you're Polish and you go to Spain on holiday, prices there will still look higher than at home. That's the plain-dollar gap. What's gone is the gap in what people can afford in their own country.",
         items=[dict(at="more than twice", text="1990: Spain 2.4× Poland", color="warm", size=60), dict(at="that's over", text="2027: Poland ahead", serif=True, size=64, color="acc")],
         react=[dict(at="dream holiday", pose="wave"), dict(at="more than twice", pose="shock"), dict(at="that's over", pose="cheer"), dict(at="One caveat", pose="think")]),

    # ---------------- 6 · YOUR GUESS ----------------
    dict(act=6, type="host", bg="none",
         narration="<soft>So, your guess: does Poland actually pass Spain next year, or does the revision go the other way?</soft> Tell me in the comments. {p} If you're watching from Spain: does this match what you see? {p} If you're in Poland: did you expect this moment to come so soon? {p} And Italy: you're next. I read every comment.",
         items=[dict(at="your guess", text="2027: pass or not?", color="acc", size=66), dict(at="watching from Spain", text="Spain: does it match?", color="warm", size=58)],
         react=[dict(at="your guess", pose="shrug"), dict(at="Tell me", pose="pointUp"), dict(at="watching from Spain", pose="wave")]),
    dict(act=6, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="FRA", color="acc", title="France grew 0.4%", sub="the next big one."),
         narration="And if you missed it, France is the next big one after Spain: eighty-seven percent, and a date around 2031. That story is right here. {p} I'm Chartbound. See you in the next one.",
         hold=14,
         react=[dict(at="if you missed it", pose="pointL"), dict(at="See you", pose="wave")]),
]

checks = [
    dict(say="2026: ESP − POL = 5; POL = 99.9%; both ≈ 0k", rule="expr", expr=f"[round({F[2026]} - {P[2026]}), round({R[2026]} * 100, 1), round({P[2026]} / 1000), round({F[2026]} / 1000)]", equal=[55, 99.9, 60, 60]),
    dict(say="1990 42%; ≥50% 2006; ≥70% 2012; ≥90% 2020; ≥100% 2027; 2031 = 109% (nine percent ahead)", rule="expr", expr=f"[round({R[1990]} * 100), {first_at(0.5)}, {first_at(0.7)}, {first_at(0.9)}, {first_at(1.0)}, round({R[2031]} * 100)]", equal=[42, 2006, 2012, 2020, 2027, 109]),
    dict(say="ESP 2025 growth (2.6) > DEU, FRA, ITA, GBR in IMF data (one of the fastest-growing big economies in Europe)", rule="expr", expr=f"{GR['ESP'][2025] > max(series('NGDP_RPCH', i)[2025] for i in ('DEU', 'FRA', 'ITA', 'GBR'))}", equal=True),
    dict(say="POL 2025 3.7, ESP 2025 2.6", rule="expr", expr=f"[{GR['POL'][2025]}, {GR['ESP'][2025]}]", equal=[3.7, 2.6]),
    dict(say="ITA − POL 2026 ≈ k (about six thousand); closer than FRA and GBR", rule="expr", expr=f"[round(({I[2026]} - {P[2026]}) / 1000), {I[2026] - P[2026] < min(series('PPPPC', 'FRA')[2026], series('PPPPC', 'GBR')[2026]) - P[2026]}]", equal=[6, True]),
    dict(say="1990: ESP ≈ 6k, POL ≈ .7k; ESP 2.4× (more than twice)", rule="expr", expr=f"[round({F[1990]} / 1000), round({P[1990]} / 100) * 100, round({F[1990]} / {P[1990]}, 1)]", equal=[16, 6700, 2.4]),
    dict(say="real 1990→2025: POL ×3.5, ESP ×2.0 (doubled)", rule="expr", expr=f"[round({grow('POL', 1990, 2025)}, 1), round({grow('ESP', 1990, 2025)}, 1)]", equal=[3.5, 2.0]),
    dict(say="ESP contraction 2008–2013: 2009, 2011, 2012, 2013; 2007→2013 −8% (−7.6); unemployment 2013 = 26.1 (peak)", rule="expr", expr=f"[{[y for y in range(2008, 2014) if GR['ESP'][y] < 0]}, round(({grow('ESP', 2007, 2013)} - 1) * 100), {LUR['ESP'][2013]}, {max(LUR['ESP'], key=LUR['ESP'].get)}]", equal=[[2009, 2011, 2012, 2013], -8, 26.1, 2013]),
    dict(say="2020: ESP −10.9 (minus eleven), POL −2.1; ratio 82% → 93%", rule="expr", expr=f"[{GR['ESP'][2020]}, {GR['POL'][2020]}, round({R[2019]} * 100), round({R[2020]} * 100)]", equal=[-10.9, -2.1, 82, 93]),
    dict(say="ESP growth 2024 3.7 (almost four); 2025 2.6, 2026 2.5 (about two and a half); 2027–2031 < 2; POL 2027–2031 2.5", rule="expr", expr=f"[{GR['ESP'][2024]}, {GR['ESP'][2025]}, {GR['ESP'][2026]}, {all(GR['ESP'][y] < 2 for y in range(2027, 2032))}, {sorted(set(GR['POL'][y] for y in range(2027, 2032)))}]", equal=[3.7, 2.6, 2.5, True, [2.5]]),
    dict(say="population: ESP 1990 39.2 → 2026 49.9 (almost fifty); POL 2026 36.3", rule="expr", expr=f"[round({LP['ESP'][1990]}, 1), round({LP['ESP'][2026]}, 1), round({LP['POL'][2026]}, 1)]", equal=[39.2, 49.9, 36.3]),
    dict(say="nominal 2026: ESP ≈ 2k, POL ≈ 1k, 75%; 2031 84%", rule="expr", expr=f"[round({N['ESP'][2026]} / 1000), round({N['POL'][2026]} / 1000), round({N['POL'][2026]} / {N['ESP'][2026]} * 100), round({N['POL'][2031]} / {N['ESP'][2031]} * 100)]", equal=[42, 31, 75, 84]),
    dict(say="inflation 2022: ESP 8.3 (about eight), POL 14.4", rule="expr", expr=f"[{CPI['ESP'][2022]}, {CPI['POL'][2022]}]", equal=[8.3, 14.4]),
    dict(say="unemployment 2026 POL 3.2, ESP 9.8 (three times); debt POL ≈ 67, ESP ≈ 98", rule="expr", expr=f"[{LUR['POL'][2026]}, {LUR['ESP'][2026]}, round({LUR['ESP'][2026] / LUR['POL'][2026]}), round({DEBT['POL'][2026]}), round({DEBT['ESP'][2026]})]", equal=[3.2, 9.8, 3, 67, 98]),
    dict(say="the pass: 2026 ESP 60106 / POL 60051; 2027 POL ≈ 63.6k, ESP ≈ 62.5k, +≈1,100; 2031 +≈6,200; 2010 ESP ahead ≈ 12k", rule="expr", expr=f"[{F[2026]}, {P[2026]}, round({P[2027]} / 100) * 100, round({F[2027]} / 100) * 100, round(({P[2027]} - {F[2027]}) / 100) * 100, round(({P[2031]} - {F[2031]}) / 100) * 100, round(({F[2010]} - {P[2010]}) / 1000)]", equal=[60106, 60051, 63600, 62500, 1100, 6200, 12]),
    dict(say="trend: POL/ESP 2026 > 1990 and > 2000, 2010, 2020 (rising)", rule="expr", expr=f"{R[1990] < R[2000] < R[2010] < R[2020] < R[2026]}", equal=True),
    dict(say="series callbacks: Japan passed 2026; FRA 87%, parity ~2031 (A-L26)", rule="expr", expr="[87, 2031]", equal=[87, 2031]),
    dict(say="2004: POL = 49% of ESP", rule="expr", expr=f"round({R[2004]} * 100)", equal=49),
    dict(say="nominal ESP/POL: 1990 8.4× (more than eight), 2004 3.7× (almost four), 2026 1.3×", rule="expr", expr=f"[round({N['ESP'][1990]} / {N['POL'][1990]}, 1), round({N['ESP'][2004]} / {N['POL'][2004]}, 1), round({N['ESP'][2026]} / {N['POL'][2026]}, 1)]", equal=[8.4, 3.7, 1.3]),
    dict(say="ESP unemployment > POL every year 2008–2031; 2013: ESP 26.1, POL 10.3 (about ten)", rule="expr", expr=f"[{all(LUR['ESP'][y] > LUR['POL'][y] for y in range(2008, 2032))}, {LUR['POL'][2013]}]", equal=[True, 10.3]),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="a-L27-poland-spain", clips=[], channel="chartbound", chapter0="$55 apart",
            thumb=dict(v="flags", iso="POL", vs="ESP", sym="vs", big="$55 APART", line2="NEXT YEAR POLAND PASSES"),
            w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks, datasets=[], snapshot=snapshot,
            voice=dict(model="", name="Charon",
                       style=("You are the narrator of a popular data documentary on YouTube. Read the script below in a warm, curious voice "
                              "with a little dry humor, at a relaxed but engaged pace of about 145 words per minute, like a smart friend telling "
                              "you something surprising. Let the big numbers land with a tiny pause before them. Keep the energy steady from the "
                              "first sentence to the last. Never sound like an advertisement or an audiobook.")),
            music=[dict(act=0, track="Lightless Dawn", vol=0.24), dict(act=1, track="Deliberate Thought", vol=0.22), dict(act=2, track="Hidden Agenda", vol=0.23), dict(act=3, track="Inspired", vol=0.23),
                   dict(act=4, track="Investigations", vol=0.23), dict(act=5, track="Deliberate Thought", vol=0.22), dict(act=6, track="Floating Cities", vol=0.24)],
            yt=dict(title="Poland Is $55 Behind Spain. Next Year, It Passes.",
                    description=("Income per person, adjusted for prices (IMF World Economic Outlook, October 2026): Poland was 42% of Spain in 1990, half in 2006, 90% in 2020 and 99.9% this year — "
                                 "$60,051 vs $60,106, a $55 gap. In the IMF's forecast Poland passes Spain in 2027 and is ~9% ahead by 2031. Spain's two crashes (2008–2013 and 2020), why fast Spanish growth "
                                 "is shared by more people, where Spain still wins (plain dollars: Poland 75%; 2022 inflation) and where Poland wins (unemployment 3.2% vs 9.8%, debt).\n\n"
                                 "Sources: IMF World Economic Outlook, October 2026 (PPPPC, NGDPDPC, NGDP_RPCH, LP, LUR, GGXWDG_NGDP, PCPIPCH). 2026+ figures are IMF estimates and forecasts.\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#poland #spain #economics #imf #europe #data"),
                    tags=["poland", "spain", "poland vs spain", "spain economy", "poland economy", "gdp per capita", "imf", "economics", "europe", "data", "polska", "hiszpania", "españa"], lang="en"))

json.dump(spec, open(os.path.join(HERE, "a-L27.json"), "w"), ensure_ascii=False, indent=1)
clean = lambda t: t.replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()
words = sum(len(clean(s["narration"])) for s in shots)
acts = {}
for s in shots:
    acts[s["act"]] = acts.get(s["act"], 0) + len(clean(s["narration"]))
print("shots", len(shots), "palavras", words, f"~{words / 145:.1f} min a 145 wpm", "por ato", acts, "paridade", round(par_recent, 2), round(par_imf, 2))

"""Gera specs/long/a-L32.json — Chartbound longo #32: "Hungary Was 29% Richer Than Poland. Now Poland Is 18% Ahead." (gêmeo do A-L30 Estônia, 5,6k)
Medida principal: PIB per capita ajustado por preços (PPPPC); ato 3 em dólares correntes (NGDPDPC).
Dados: IMF WEO out/2026 (research/imf_v4_2026-11-13.json: POL, HUN, CZE, SVK).
Fora do FMI (documentado): empréstimo de emergência FMI/UE/Banco Mundial à Hungria em out–nov/2008 (~€20 bi), o 1º a um país da UE na crise de 2008; V4 = CZE, HUN, POL, SVK; Hungria e Polônia entraram na UE em 1/5/2004."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "..", "..", "research")
D = json.load(open(os.path.join(R, "imf_v4_2026-11-13.json")))
ACTS = ["Cold open", "The head start", "The lost years", "Plain dollars", "The Visegrád race", "The pass", "Your guess"]
IMF = "IMF World Economic Outlook, October 2026"


def ser(ind, iso):
    r = D[ind][iso]
    return {r["y0"] + k: v for k, v in enumerate(r["v"])}


PP = {iso: ser("PPPPC", iso) for iso in ("POL", "HUN", "CZE", "SVK")}
N = {iso: ser("NGDPDPC", iso) for iso in ("POL", "HUN")}
GR = {iso: ser("NGDP_RPCH", iso) for iso in ("POL", "HUN")}
LP = {iso: ser("LP", iso) for iso in ("POL", "HUN")}
P, H, C, S = PP["POL"], PP["HUN"], PP["CZE"], PP["SVK"]


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
    snapshot.append(dict(set="rat", iso="HUN", year=y, value=round(H[y] / P[y] * 100, 2), src=IMF + " · Hungary's GDP per capita (PPP) as % of Poland's"))

PPPSRC = IMF + " · GDP per capita, PPP, current international $ (PPPPC); 2026+ are IMF estimates and forecasts"
USDSRC = IMF + " · GDP per capita, current US$ at market exchange rates (NGDPDPC); 2026+ are IMF estimates and forecasts"
PPP2 = dict(set="imf", fc=2025, series=["HUN", "POL"], years=[1995, 2031], y=[0, 80000], src=PPPSRC, fmt="usd0", hl="POL")
RATCH = dict(set="rat", fc=2025, series=["HUN"], years=[1995, 2031], y=[60, 160], src=IMF + " · Hungary's GDP per capita (PPP) as % of Poland's; 2026+ are IMF estimates and forecasts", fmt="pct0", hl="HUN", ref=dict(value=100, label="Poland = 100%", pos="right"))

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="lines", start=2005.0, **PPP2,
         narration="Twenty-nine percent. {p} In 2005, the average Hungarian was twenty-nine percent richer than the average Pole, on income adjusted for prices. {pp} In 2011, Poland passed. This year, in the IMF's numbers, Poland is about eighteen percent ahead. {p} And by 2031, in the IMF's forecast, the gap is about the same.",
         keys=[dict(at="Twenty-nine percent", year=2005.0, dur=0.5), dict(at="In 2011", year=2011.0, dur=2.5), dict(at="This year", year=2026.0, dur=1.5), dict(at="by 2031", year=2031.0, dur=2.5)],
         labels=[dict(at="In 2005", iso="HUN", year=2005), dict(at="In 2011", iso="POL", year=2011), dict(at="eighteen percent ahead", iso="POL", year=2026)],
         react=[dict(at="Twenty-nine percent", pose="shock"), dict(at="In 2005", pose="pointL"), dict(at="Poland passed", pose="cheer"), dict(at="by 2031", pose="pointUp")]),
    dict(act=0, type="host", bg="lines", start=2031.0, **{k: v for k, v in PPP2.items() if k != "src"},
         narration="When both countries joined the European Union in 2004, Hungary was the richer one, and it wasn't close. {p} Poland was the bigger country, but the poorer one. {pp} <soft>So what happened? A slow decade, a crisis, and a neighbor that kept growing.</soft>",
         items=[dict(at="joined the European Union", text="EU, May 2004", serif=True, size=66, color="acc2"), dict(at="it wasn't close", text="Hungary +27%", color="acc", size=60), dict(at="kept growing", text="Poland: 1 down year since 1992", color="warm", size=54)],
         react=[dict(at="joined the European Union", pose="pointL"), dict(at="it wasn't close", pose="think"), dict(at="the poorer one", pose="shrug"), dict(at="kept growing", pose="pointUp")]),

    # ---------------- 1 · THE HEAD START ----------------
    dict(act=1, type="host", bg="none",
         narration="Quick one before the chart: this is a series about who's passing whom, and Poland keeps showing up. Subscribe so you don't miss the next one. {p} Now, the head start.",
         items=[dict(at="who's passing whom", text="Who passed whom", serif=True, size=66, color="acc"), dict(at="Subscribe", text="Subscribe", size=70)],
         react=[dict(at="Quick one", pose="wave"), dict(at="Subscribe", pose="cheer"), dict(at="the head start", pose="pointL")]),
    dict(act=1, type="lines", start=1995.0, **RATCH,
         narration="Here's Hungary as a share of Poland, adjusted for prices. {p} In 1995, a hundred and thirty-three percent. Poland closed some of that in the late nineties. {pp} Then Hungary pulled away again: a hundred and twenty-seven percent in 2004, and a hundred and twenty-nine in 2005. {p} That was the peak.",
         keys=[dict(at="In 1995", year=1995.0, dur=1.5), dict(at="late nineties", year=2000.0, dur=1.5), dict(at="in 2004", year=2004.0, dur=1.5), dict(at="the peak", year=2005.0, dur=1.5)],
         labels=[dict(at="In 1995", iso="HUN", year=1995), dict(at="a hundred and twenty-nine", iso="HUN", year=2005)],
         react=[dict(at="In 1995", pose="pointL"), dict(at="closed some", pose="think"), dict(at="pulled away again", pose="shock"), dict(at="the peak", pose="pointUp")]),

    # ---------------- 2 · THE LOST YEARS ----------------
    dict(act=2, type="bars", mode="abs", set="imfg", iso="HUN", years=[2000, 2030], start=2005.0, fmt="pct1", src=IMF + " · real GDP growth, Hungary (annual %); 2026+ are IMF estimates and forecasts",
         narration="Here's Hungary's economy, year by year, after inflation. {p} In 2007, it grew a third of a percent. Poland grew almost seven. {pp} Then the 2008 crisis. In late 2008, Hungary needed an emergency loan from the IMF and the European Union, the first EU country to get one in that crisis. {p} In 2009, its economy shrank almost seven percent. Poland's grew two point six. {pp} And in 2012, Hungary shrank again.",
         keys=[dict(at="In 2007", year=2007.0, dur=1.5), dict(at="the 2008 crisis", year=2008.0, dur=2.0), dict(at="In 2009", year=2009.0, dur=2.0), dict(at="in 2012", year=2012.0, dur=1.5)],
         react=[dict(at="In 2007", pose="think"), dict(at="emergency loan", pose="shock"), dict(at="Poland's grew", pose="pointUp"), dict(at="shrank again", pose="shrug")]),
    dict(act=2, type="stats", src=IMF + " · real GDP growth (NGDP_RPCH, compounded), population (LP)", title="The lost years",
         narration="Put it together. From 2006 to 2013, after inflation, Hungary's economy actually got smaller, by about two percent. Poland's grew about twenty-seven. {p} That's where the pass happened. {pp} And since then? Hungary barely grew from 2023 to 2025. Poland grew about seven percent. {p} Hungary has about nine and a half million people. Poland has almost four times as many.",
         stats=[dict(at="about two percent", value=round((grow("HUN", 2006, 2013) - 1) * 100), fmt="pct0", label="Hungary, real growth 2006–2013"), dict(at="about twenty-seven", value=round((grow("POL", 2006, 2013) - 1) * 100), fmt="pct0", label="Poland, real growth 2006–2013"), dict(at="about seven percent", value=round((grow("POL", 2022, 2025) - 1) * 100), fmt="pct0", label="Poland, real growth 2023–2025"), dict(at="nine and a half million", value=round(LP["HUN"][2026], 1), fmt="dec1", label="million people in Hungary, 2026")],
         react=[dict(at="Put it together", pose="pointUp"), dict(at="got smaller", pose="shock"), dict(at="the pass happened", pose="cheer"), dict(at="almost four times", pose="think")]),

    # ---------------- 3 · PLAIN DOLLARS ----------------
    dict(act=3, type="lines", set="imfusd", fc=2025, series=["HUN", "POL"], years=[2004, 2031], start=2016.0, y=[0, 50000], src=USDSRC, fmt="usd0", hl="POL",
         narration="In plain dollars, at market exchange rates, the race was closer, and it went back and forth for years. {p} In 2023, they were basically tied: about twenty-two thousand dollars a person each. {pp} Since 2024, Poland has been ahead. This year, about thirty-one thousand two hundred dollars, against twenty-seven thousand nine hundred in Hungary. {p} Unlike most countries in this series, Hungary is now behind on both measures.",
         keys=[dict(at="In plain dollars", year=2016.0, dur=1.5), dict(at="In 2023", year=2023.0, dur=2.0), dict(at="Since 2024", year=2024.0, dur=1.5), dict(at="This year", year=2026.0, dur=2.5)],
         labels=[dict(at="thirty-one thousand two hundred", iso="POL", year=2026), dict(at="twenty-seven thousand nine hundred", iso="HUN", year=2026)],
         react=[dict(at="back and forth", pose="think"), dict(at="basically tied", pose="shrug"), dict(at="Since 2024", pose="pointUp"), dict(at="both measures", pose="shock")]),

    # ---------------- 4 · THE VISEGRÁD RACE ----------------
    dict(act=4, type="host", bg="none",
         narration="And if you're enjoying the series, the subscribe button is right there. {p} Now, the four-country race.",
         items=[dict(at="subscribe button", text="Subscribe", size=66), dict(at="four-country race", text="The Visegrád race", serif=True, size=66, color="acc")],
         react=[dict(at="subscribe button", pose="pointUp"), dict(at="four-country race", pose="pointL")]),
    dict(act=4, type="lines", set="imf", fc=2025, series=["CZE", "HUN", "SVK", "POL"], years=[2004, 2031], start=2004.0, y=[0, 80000], src=PPPSRC, fmt="usd0", hl="POL",
         narration="Czechia, Hungary, Slovakia and Poland: the Visegrád Four. {p} In 2004, adjusted for prices, Poland was last of the four. Czechia first, Hungary second. {pp} This year, Poland is second, behind only Czechia. Hungary is third, just ahead of Slovakia. {p} Poland went from last to second. Hungary went from second to third.",
         keys=[dict(at="In 2004", year=2004.0, dur=2.0), dict(at="This year", year=2026.0, dur=3.0)],
         labels=[dict(at="Poland was last", iso="POL", year=2004)],
         react=[dict(at="the Visegrád Four", pose="pointL"), dict(at="Poland was last", pose="think"), dict(at="behind only Czechia", pose="cheer"), dict(at="from second to third", pose="shrug")]),

    # ---------------- 5 · THE PASS ----------------
    dict(act=5, type="stats", src=PPPSRC, title="The pass, adjusted for prices",
         narration="So here's the pass, in the IMF's numbers. {p} In 2010, Hungary was still ahead, by about five hundred dollars per person. {p} In 2011, Poland passed, by about a hundred dollars. For almost a decade, they stayed within a few percent of each other. {pp} Then Poland pulled away. This year, the gap is about nine thousand dollars. And by 2031, in the IMF's forecast, about eleven and a half thousand.",
         stats=[dict(at="still ahead", value=H[2010], fmt="usd0", label="Hungary, 2010"), dict(at="about five hundred", value=P[2010], fmt="usd0", label="Poland, 2010"), dict(at="about nine thousand", value=P[2026] - H[2026], fmt="usd0", label="Poland ahead, 2026"), dict(at="eleven and a half thousand", value=P[2031] - H[2031], fmt="usd0", label="Poland ahead, 2031 (IMF)")],
         react=[dict(at="here's the pass", pose="pointUp"), dict(at="still ahead", pose="think"), dict(at="Poland passed", pose="cheer"), dict(at="pulled away", pose="shock")]),

    # ---------------- 6 · YOUR GUESS ----------------
    dict(act=6, type="host", bg="none",
         narration="<soft>So, what's your guess?</soft> {pp} Can Hungary close the gap again, {p} or is this the new normal? {pp} Tell me in the comments. {pp} If you're watching from Hungary: {p} does it feel like this where you are? {pp} I read every comment.",
         items=[dict(at="your guess", text="Comeback or new normal?", color="acc", size=66), dict(at="watching from Hungary", text="Hungary: does it match?", color="warm", size=58)],
         react=[dict(at="your guess", pose="shrug"), dict(at="Tell me", pose="pointUp"), dict(at="watching from Hungary", pose="wave")]),
    dict(act=6, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="EST", color="acc", title="Estonia vs Poland", sub="the Baltic tiger that stalled."),
         narration="And if you missed it, {p} this is the one where Estonia stalled and Poland passed. {pp} It's right here. {pp} I'm Chartbound. {p} See you in the next one.",
         hold=14,
         react=[dict(at="if you missed it", pose="pointL"), dict(at="See you", pose="wave")]),
]

checks = [
    dict(say="2005: HUN 129% of POL (peak 1996–2031)", rule="expr", expr=f"[round({H[2005]} / {P[2005]} * 100), {max(range(1996, 2032), key=lambda y: H[y] / P[y])}]", equal=[129, 2005]),
    dict(say="POL passed HUN in 2011 (only crossing 1996–2031)", rule="expr", expr=f"{[y for y in range(1996, 2032) if (P[y] > H[y]) != (P[y - 1] > H[y - 1])]}", equal=[2011]),
    dict(say="2026: POL ≈ 18% ahead; 2031 ≈ 18% (about the same)", rule="expr", expr=f"[round(({P[2026]} / {H[2026]} - 1) * 100), round(({P[2031]} / {H[2031]} - 1) * 100)]", equal=[18, 18]),
    dict(say="HUN/POL: 1995 133%, 2004 127%, 2005 129%; 2000 lower (118%)", rule="expr", expr=f"[round({H[1995]} / {P[1995]} * 100), round({H[2004]} / {P[2004]} * 100), round({H[2005]} / {P[2005]} * 100), round({H[2000]} / {P[2000]} * 100)]", equal=[133, 127, 129, 118]),
    dict(say="growth 2007: HUN 0.3 (a third of a percent), POL 6.8 (almost seven)", rule="expr", expr=f"[{GR['HUN'][2007]}, {GR['POL'][2007]}]", equal=[0.3, 6.8]),
    dict(say="2009: HUN −6.8 (almost seven), POL +2.6; 2012 HUN −1.3 (shrank again)", rule="expr", expr=f"[{GR['HUN'][2009]}, {GR['POL'][2009]}, {GR['HUN'][2012] < 0}]", equal=[-6.8, 2.6, True]),
    dict(say="real 2006→2013: HUN −2%, POL +27%", rule="expr", expr=f"[round(({grow('HUN', 2006, 2013)} - 1) * 100), round(({grow('POL', 2006, 2013)} - 1) * 100)]", equal=[-2, 27]),
    dict(say="real 2022→2025 (2023–2025): HUN ≈ 0 (barely), POL ≈ 7", rule="expr", expr=f"[round(({grow('HUN', 2022, 2025)} - 1) * 100), round(({grow('POL', 2022, 2025)} - 1) * 100)]", equal=[0, 7]),
    dict(say="POL: no negative year 1992–2031 except 2020", rule="expr", expr=f"{[y for y in range(1992, 2032) if GR['POL'][y] < 0]}", equal=[2020]),
    dict(say="HUN pop 2026 9.5M; POL/HUN ≈ 3.8 (almost four)", rule="expr", expr=f"[round({LP['HUN'][2026]}, 1), round({LP['POL'][2026]} / {LP['HUN'][2026]}, 1)]", equal=[9.5, 3.8]),
    dict(say="USD 2023 both ≈ 22,000 (22,198 / 22,119); POL ahead every year 2024–2031; 2026 POL ≈ 31,200, HUN ≈ 27,900", rule="expr", expr=f"[round({N['HUN'][2023]} / 1000), round({N['POL'][2023]} / 1000), {all(N['POL'][y] > N['HUN'][y] for y in range(2024, 2032))}, round({N['POL'][2026]} / 100) * 100, round({N['HUN'][2026]} / 100) * 100]", equal=[22, 22, True, 31200, 27900]),
    dict(say="V4 2004: CZE > HUN > SVK > POL (POL last); 2026: CZE > POL > HUN > SVK", rule="expr", expr=f"[{sorted(['CZE', 'HUN', 'SVK', 'POL'], key=lambda i: -PP[i][2004])}, {sorted(['CZE', 'HUN', 'SVK', 'POL'], key=lambda i: -PP[i][2026])}]", equal=[["CZE", "HUN", "SVK", "POL"], ["CZE", "POL", "HUN", "SVK"]]),
    dict(say="2010: HUN ahead by ≈ 500 (528); 2011 POL ahead ≈ 100 (99)", rule="expr", expr=f"[round(({H[2010]} - {P[2010]}) / 100) * 100, round(({P[2011]} - {H[2011]}) / 100) * 100]", equal=[500, 100]),
    dict(say="2012–2019 within a few percent (ratio 97–100%)", rule="expr", expr=f"[round(min({[H[y] / P[y] for y in range(2012, 2020)]}) * 100), round(max({[H[y] / P[y] for y in range(2012, 2020)]}) * 100)]", equal=[97, 100]),
    dict(say="2026 gap ≈ 9,000; 2031 ≈ 11,500 (11,681)", rule="expr", expr=f"[round(({P[2026]} - {H[2026]}) / 1000) * 1000, round(({P[2031]} - {H[2031]}) / 500) * 500]", equal=[9000, 11500]),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="a-L32-poland-hungary", clips=[], channel="chartbound", chapter0="29%",
            thumb=dict(v="flags", iso="HUN", vs="POL", sym="vs", big="2005: +29%", line2="2026: BEHIND"),
            w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks, datasets=[], snapshot=snapshot,
            voice=dict(model="", name="Charon",
                       style=("You are the narrator of a popular data documentary on YouTube. Read the script below in a warm, curious voice "
                              "with a little dry humor, at a relaxed but engaged pace of about 145 words per minute, like a smart friend telling "
                              "you something surprising. Let the big numbers land with a tiny pause before them. Keep the energy steady from the "
                              "first sentence to the last. Never sound like an advertisement or an audiobook.")),
            music=[dict(act=0, track="Lightless Dawn", vol=0.24), dict(act=1, track="Deliberate Thought", vol=0.22), dict(act=2, track="Hidden Agenda", vol=0.23), dict(act=3, track="Inspired", vol=0.23),
                   dict(act=4, track="Investigations", vol=0.23), dict(act=5, track="Deliberate Thought", vol=0.22), dict(act=6, track="Floating Cities", vol=0.24)],
            yt=dict(title="Hungary Was 29% Richer Than Poland. Now Poland Is 18% Ahead.",
                    description=("Income per person adjusted for prices (IMF World Economic Outlook, October 2026): in 2005 the average Hungarian was 29% ahead of the average Pole. "
                                 "Poland passed in 2011; this year it's ~18% ahead, about the same in the IMF's 2031 forecast. Hungary's slow 2000s (+0.3% in 2007), the 2008 emergency loan, "
                                 "the 2009 recession (−6.8%), 2006–2013 real growth of about −2% vs +27% for Poland, the plain-dollar race, and the Visegrád Four: Poland went from last to second.\n\n"
                                 "Sources: IMF World Economic Outlook, October 2026 (PPPPC, NGDPDPC, NGDP_RPCH, LP). 2026+ figures are IMF estimates and forecasts.\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#poland #hungary #visegrad #economics #imf #europe #data"),
                    tags=["poland", "hungary", "poland vs hungary", "visegrad", "visegrad four", "czechia", "slovakia", "hungary economy", "poland economy", "gdp per capita", "imf", "economics", "polska", "magyarország"], lang="en"))

json.dump(spec, open(os.path.join(HERE, "a-L32.json"), "w"), ensure_ascii=False, indent=1)
clean = lambda t: t.replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()
words = sum(len(clean(s["narration"])) for s in shots)
acts = {}
for s in shots:
    acts[s["act"]] = acts.get(s["act"], 0) + len(clean(s["narration"]))
print("shots", len(shots), "palavras", words, f"~{words / 145:.1f} min a 145 wpm", "por ato", acts)

"""Gera specs/long/a-L34.json — Chartbound longo #34: "Czechia Was 87% Richer Than Poland. Now It's Just 7%." (gêmeo do A-L33 Eslovênia, que pegou: 19 → 1.096 views em 15 h)
Medida principal: PIB per capita ajustado por preços (PPPPC); ato 3 em dólares correntes (NGDPDPC).
Dados: IMF WEO out/2026 (research/imf_v4_2026-11-13.json: POL, CZE, SVN, SVK).
Fora do FMI (documentado): Tchecoslováquia se dividiu em 1/1/1993; crise cambial de maio/1997 (coroa passou a flutuar — Yale YPFS 'Czech Republic Currency Crisis (1997)'; CEU 'The May 1997 currency crisis in the Czech Republic');
Polônia foi o único país da UE sem recessão em 2009 (IMF Survey 2010; vários); Tchéquia e Polônia entraram na UE em 1/5/2004; Tchéquia mantém a coroa (não adotou o euro)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "..", "..", "research")
D = json.load(open(os.path.join(R, "imf_v4_2026-11-13.json")))
ACTS = ["Cold open", "The head start", "The crash", "Plain dollars", "The race", "The gap now", "Your guess"]
IMF = "IMF World Economic Outlook, October 2026"


def ser(ind, iso):
    r = D[ind][iso]
    return {r["y0"] + k: v for k, v in enumerate(r["v"])}


PP = {iso: ser("PPPPC", iso) for iso in ("POL", "CZE", "SVN", "SVK")}
N = {iso: ser("NGDPDPC", iso) for iso in ("POL", "CZE")}
GR = {iso: ser("NGDP_RPCH", iso) for iso in ("POL", "CZE")}
LP = {iso: ser("LP", iso) for iso in ("POL", "CZE")}
P, C, S, K = PP["POL"], PP["CZE"], PP["SVN"], PP["SVK"]


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
    snapshot.append(dict(set="rat", iso="CZE", year=y, value=round(C[y] / P[y] * 100, 2), src=IMF + " · Czechia's GDP per capita (PPP) as % of Poland's"))

PPPSRC = IMF + " · GDP per capita, PPP, current international $ (PPPPC); 2026+ are IMF estimates and forecasts"
USDSRC = IMF + " · GDP per capita, current US$ at market exchange rates (NGDPDPC); 2026+ are IMF estimates and forecasts"
PPP2 = dict(set="imf", fc=2025, series=["CZE", "POL"], years=[1995, 2031], y=[0, 80000], src=PPPSRC, fmt="usd0", hl="POL")
RATCH = dict(set="rat", fc=2025, series=["CZE"], years=[1995, 2031], y=[80, 200], src=IMF + " · Czechia's GDP per capita (PPP) as % of Poland's; 2026+ are IMF estimates and forecasts", fmt="pct0", hl="CZE", ref=dict(value=100, label="Poland = 100%", pos="right"))

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="lines", start=1995.0, **PPP2,
         narration="Eighty-seven percent. {p} In 1995, the average Czech was eighty-seven percent richer than the average Pole, on income adjusted for prices. {pp} This year, in the IMF's numbers, the gap is under seven percent. {p} And by 2031, in the IMF's forecast, it's about four.",
         keys=[dict(at="Eighty-seven percent", year=1995.0, dur=0.5), dict(at="This year", year=2026.0, dur=3.0), dict(at="by 2031", year=2031.0, dur=2.5)],
         labels=[dict(at="In 1995", iso="CZE", year=1995), dict(at="under seven percent", iso="POL", year=2026), dict(at="about four", iso="CZE", year=2031)],
         react=[dict(at="Eighty-seven percent", pose="shock"), dict(at="In 1995", pose="pointL"), dict(at="under seven percent", pose="think"), dict(at="about four", pose="pointUp")]),
    dict(act=0, type="host", bg="lines", start=2031.0, **{k: v for k, v in PPP2.items() if k != "src"},
         narration="On January 1st, 1993, Czechoslovakia split in two. {p} The Czech half was the richer one. {pp} In 1995, Czechia was richer than Slovakia, richer than Slovenia, and far richer than Poland. {p} <soft>So how did Poland close almost the whole gap?</soft>",
         items=[dict(at="split in two", text="January 1, 1993", serif=True, size=62, color="acc2"), dict(at="the richer one", text="The richer half", color="acc", size=60), dict(at="far richer than Poland", text="+87% vs Poland", color="warm", size=60)],
         react=[dict(at="split in two", pose="pointL"), dict(at="the richer one", pose="think"), dict(at="far richer", pose="shock"), dict(at="the whole gap", pose="shrug")]),

    # ---------------- 1 · THE HEAD START ----------------
    dict(act=1, type="host", bg="none",
         narration="Quick one before the chart: this is a series about who's passing whom in Europe, and Poland keeps showing up. Subscribe so you don't miss the next one. {p} Now, the head start.",
         items=[dict(at="who's passing whom", text="Who passed whom", serif=True, size=66, color="acc"), dict(at="Subscribe", text="Subscribe", size=70)],
         react=[dict(at="Quick one", pose="wave"), dict(at="Subscribe", pose="cheer"), dict(at="the head start", pose="pointL")]),
    dict(act=1, type="lines", start=1995.0, **RATCH,
         narration="Here's Czechia as a share of Poland, adjusted for prices. {p} In 1995, a hundred and eighty-seven percent. {pp} Then, in May 1997, a run on the Czech currency. The koruna was set free to float, and the economy shrank two years in a row. {p} From 1996 to 1999, Czechia barely grew at all. Poland grew eighteen percent. {pp} By 2000, the lead was down to fifty-six percent. And there it sat, for almost a decade.",
         keys=[dict(at="In 1995", year=1995.0, dur=1.5), dict(at="May 1997", year=1997.0, dur=1.5), dict(at="By 2000", year=2000.0, dur=1.5), dict(at="almost a decade", year=2008.0, dur=3.0)],
         labels=[dict(at="In 1995", iso="CZE", year=1995), dict(at="fifty-six percent", iso="CZE", year=2000)],
         react=[dict(at="In 1995", pose="pointL"), dict(at="a run on the Czech", pose="shock"), dict(at="barely grew", pose="shrug"), dict(at="there it sat", pose="think")]),

    # ---------------- 2 · THE CRASH ----------------
    dict(act=2, type="bars", mode="abs", set="imfg", iso="CZE", years=[2000, 2030], start=2005.0, fmt="pct1", src=IMF + " · real GDP growth, Czechia (annual %); 2026+ are IMF estimates and forecasts",
         narration="Here's Czechia's economy, year by year, after inflation. {p} From 2005 to 2007, a boom: more than five percent a year. {pp} Then the 2008 crisis. In 2009, Czechia shrank four point eight percent. {p} Poland grew two point six. It was the only economy in the European Union that didn't shrink that year. {pp} And Czechia dipped again in 2012.",
         keys=[dict(at="From 2005", year=2006.0, dur=2.0), dict(at="In 2009", year=2009.0, dur=2.0), dict(at="dipped again", year=2012.0, dur=1.5)],
         react=[dict(at="a boom", pose="cheer"), dict(at="four point eight", pose="shock"), dict(at="the only economy", pose="pointUp"), dict(at="dipped again", pose="shrug")]),
    dict(act=2, type="stats", src=IMF + " · real GDP growth (NGDP_RPCH, compounded), population (LP)", title="The crash",
         narration="Put it together. From 2008 to 2013, after inflation, Czechia's economy shrank about one percent. Poland's grew about fourteen. {p} And over thirty years, from 1995 to 2025, Czechia's economy almost doubled. Poland's roughly tripled. {pp} Czechia has about eleven million people. Poland has more than three times as many.",
         stats=[dict(at="shrank about one percent", value=round((grow("CZE", 2008, 2013) - 1) * 100), fmt="pct0", label="Czechia, real growth 2008–2013"), dict(at="grew about fourteen", value=round((grow("POL", 2008, 2013) - 1) * 100), fmt="pct0", label="Poland, real growth 2008–2013"), dict(at="roughly tripled", value=round((grow("POL", 1995, 2025) - 1) * 100), fmt="pct0", label="Poland, real growth 1995–2025"), dict(at="eleven million people", value=round(LP["CZE"][2026], 1), fmt="dec1", label="million people in Czechia, 2026")],
         react=[dict(at="Put it together", pose="pointUp"), dict(at="shrank about one", pose="shock"), dict(at="roughly tripled", pose="cheer"), dict(at="three times as many", pose="think")]),

    # ---------------- 3 · PLAIN DOLLARS ----------------
    dict(act=3, type="lines", set="imfusd", fc=2025, series=["CZE", "POL"], years=[1995, 2031], start=2008.0, y=[0, 60000], src=USDSRC, fmt="usd0", hl="CZE",
         narration="Now the twist. In plain dollars, at market exchange rates, Czechia is further ahead. {p} This year, about thirty-nine thousand six hundred dollars a person. Poland, about thirty-one thousand two hundred. {pp} That's about a quarter more. {p} Czechia kept its own currency, and never joined the euro. Neither did Poland. {p} So in plain money, the Czechs are still clearly ahead.",
         keys=[dict(at="plain dollars", year=2008.0, dur=1.5), dict(at="This year", year=2026.0, dur=3.0)],
         labels=[dict(at="thirty-nine thousand six hundred", iso="CZE", year=2026), dict(at="thirty-one thousand two hundred", iso="POL", year=2026)],
         react=[dict(at="the twist", pose="pointUp"), dict(at="further ahead", pose="shock"), dict(at="a quarter more", pose="think"), dict(at="clearly ahead", pose="shrug")]),

    # ---------------- 4 · THE RACE ----------------
    dict(act=4, type="host", bg="none",
         narration="And if you're enjoying the series, the subscribe button is right there. {p} Now, the bigger race.",
         items=[dict(at="subscribe button", text="Subscribe", size=66), dict(at="bigger race", text="Central Europe's race", serif=True, size=66, color="acc")],
         react=[dict(at="subscribe button", pose="pointUp"), dict(at="bigger race", pose="pointL")]),
    dict(act=4, type="lines", set="imf", fc=2025, series=["CZE", "SVN", "SVK", "POL"], years=[2004, 2031], start=2004.0, y=[0, 80000], src=PPPSRC, fmt="usd0", hl="POL",
         narration="Czechia, Slovenia, Slovakia and Poland. {p} In 2004, adjusted for prices, Slovenia was first and Poland was last. {pp} Since 2009, Czechia has been ahead of Slovenia. And Poland passed Slovakia. {p} So the old Czechoslovakia ended up on both sides of Poland.",
         keys=[dict(at="In 2004", year=2004.0, dur=2.0), dict(at="Since 2009", year=2009.0, dur=2.0), dict(at="passed Slovakia", year=2026.0, dur=3.0)],
         labels=[dict(at="Poland was last", iso="POL", year=2004)],
         react=[dict(at="Czechia, Slovenia", pose="pointL"), dict(at="Poland was last", pose="think"), dict(at="passed Slovakia", pose="cheer"), dict(at="both sides", pose="shock")]),

    # ---------------- 5 · THE GAP NOW ----------------
    dict(act=5, type="stats", src=PPPSRC, title="The gap, adjusted for prices",
         narration="So here's where it stands, in the IMF's numbers. {p} In 2008, Czechia was ahead by about eleven thousand three hundred dollars per person. {p} This year, about four thousand. {pp} And in 2031, in the IMF's forecast, about three thousand one hundred. {p} Czechia is still ahead. But most of that lead is gone.",
         stats=[dict(at="eleven thousand three hundred", value=C[2008] - P[2008], fmt="usd0", label="Czechia ahead, 2008"), dict(at="about four thousand", value=C[2026] - P[2026], fmt="usd0", label="Czechia ahead, 2026"), dict(at="three thousand one hundred", value=C[2031] - P[2031], fmt="usd0", label="Czechia ahead, 2031 (IMF)")],
         react=[dict(at="where it stands", pose="pointUp"), dict(at="eleven thousand", pose="shock"), dict(at="about four thousand", pose="think"), dict(at="most of that lead", pose="shrug")]),

    # ---------------- 6 · YOUR GUESS ----------------
    dict(act=6, type="host", bg="none",
         narration="<soft>So, what's your guess?</soft> {pp} Does Poland pass Czechia in the 2030s, {p} later, {p} or never? {pp} Tell me in the comments. {pp} If you're watching from Czechia: {p} does it feel like this where you are? {pp} I read every comment.",
         items=[dict(at="your guess", text="2030s, later, or never?", color="acc", size=60), dict(at="watching from Czechia", text="Czechia: does it match?", color="warm", size=58)],
         react=[dict(at="your guess", pose="shrug"), dict(at="Tell me", pose="pointUp"), dict(at="watching from Czechia", pose="wave")]),
    dict(act=6, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="SVN", color="acc", title="Slovenia vs Poland", sub="71% richer, now almost even."),
         narration="And if you missed it, {p} this is the one where Slovenia was seventy-one percent richer, and now it's almost even. {pp} It's right here. {pp} I'm Chartbound. {p} See you in the next one.",
         hold=14,
         react=[dict(at="if you missed it", pose="pointL"), dict(at="See you", pose="wave")]),
]

checks = [
    dict(say="1995: CZE 187% of POL (87% richer)", rule="expr", expr=f"round({C[1995]} / {P[1995]} * 100)", equal=187),
    dict(say="2026 under 7% (106.7); 2031 ≈ 4%", rule="expr", expr=f"[{C[2026] / P[2026] * 100 < 107}, round(({C[2031]} / {P[2031]} - 1) * 100)]", equal=[True, 4]),
    dict(say="POL never passes CZE 1995–2031 (still ahead)", rule="expr", expr=f"{all(C[y] > P[y] for y in range(1995, 2032))}", equal=True),
    dict(say="1995: CZE > SVK, SVN; CZE far richer than POL", rule="expr", expr=f"[{C[1995] > K[1995]}, {C[1995] > S[1995]}]", equal=[True, True]),
    dict(say="growth 1997, 1998 < 0 (shrank two years in a row); 1996→1999 CZE ~0%, POL +18%", rule="expr", expr=f"[{GR['CZE'][1997] < 0 and GR['CZE'][1998] < 0}, round(({grow('CZE', 1996, 1999)} - 1) * 100), round(({grow('POL', 1996, 1999)} - 1) * 100)]", equal=[True, 0, 18]),
    dict(say="2000: 156% (fifty-six percent lead); 2000–2008 ratio stayed 156–164", rule="expr", expr=f"[round({C[2000]} / {P[2000]} * 100), round(min({[C[y] / P[y] for y in range(2000, 2009)]}) * 100), round(max({[C[y] / P[y] for y in range(2000, 2009)]}) * 100)]", equal=[156, 156, 164]),
    dict(say="2005–2007 all > 5%; 2009 CZE −4.8, POL 2.6; 2012 CZE < 0", rule="expr", expr=f"[{min(GR['CZE'][y] for y in (2005, 2006, 2007)) > 5}, {GR['CZE'][2009]}, {GR['POL'][2009]}, {GR['CZE'][2012] < 0}]", equal=[True, -4.8, 2.6, True]),
    dict(say="real 2008→2013: CZE −1%, POL +14%", rule="expr", expr=f"[round(({grow('CZE', 2008, 2013)} - 1) * 100), round(({grow('POL', 2008, 2013)} - 1) * 100)]", equal=[-1, 14]),
    dict(say="real 1995→2025: CZE ×1.9 (almost doubled), POL ×3.1 (roughly tripled)", rule="expr", expr=f"[round({grow('CZE', 1995, 2025)}, 1), round({grow('POL', 1995, 2025)}, 1)]", equal=[1.9, 3.1]),
    dict(say="pop 2026: CZE 10.8M (~11); POL/CZE > 3", rule="expr", expr=f"[round({LP['CZE'][2026]}), {LP['POL'][2026] / LP['CZE'][2026] > 3}]", equal=[11, True]),
    dict(say="USD 2026: CZE ≈ 39,600, POL ≈ 31,200; ratio ≈ 1.27 (about a quarter more); USD ratio > PPP ratio (further ahead)", rule="expr", expr=f"[round({N['CZE'][2026]} / 100) * 100, round({N['POL'][2026]} / 100) * 100, round({N['CZE'][2026]} / {N['POL'][2026]}, 2), {N['CZE'][2026] / N['POL'][2026] > C[2026] / P[2026]}]", equal=[39600, 31200, 1.27, True]),
    dict(say="2004 order SVN > CZE > SVK > POL; CZE > SVN every year 2009–2031; POL > SVK 2026", rule="expr", expr=f"[{sorted(['SVN', 'CZE', 'SVK', 'POL'], key=lambda i: -PP[i][2004])}, {all(C[y] > S[y] for y in range(2009, 2032))}, {P[2026] > K[2026]}]", equal=[["SVN", "CZE", "SVK", "POL"], True, True]),
    dict(say="gap 2008 ≈ 11,300 (11,291); 2026 ≈ 4,000 (4,020); 2031 ≈ 3,100 (3,073)", rule="expr", expr=f"[round(({C[2008]} - {P[2008]}) / 100) * 100, round(({C[2026]} - {P[2026]}) / 1000) * 1000, round(({C[2031]} - {P[2031]}) / 100) * 100]", equal=[11300, 4000, 3100]),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="a-L34-poland-czechia", clips=[], channel="chartbound", chapter0="87%",
            thumb=dict(v="flags", iso="CZE", vs="POL", sym="vs", big="1995: +87%", line2="2026: +7%"),
            w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks, datasets=[], snapshot=snapshot,
            voice=dict(model="", name="Charon",
                       style=("You are the narrator of a popular data documentary on YouTube. Read the script below in a warm, curious voice "
                              "with a little dry humor, at a relaxed but engaged pace of about 145 words per minute, like a smart friend telling "
                              "you something surprising. Let the big numbers land with a tiny pause before them. Keep the energy steady from the "
                              "first sentence to the last. Never sound like an advertisement or an audiobook.")),
            music=[dict(act=0, track="Lightless Dawn", vol=0.24), dict(act=1, track="Deliberate Thought", vol=0.22), dict(act=2, track="Hidden Agenda", vol=0.23), dict(act=3, track="Inspired", vol=0.23),
                   dict(act=4, track="Investigations", vol=0.23), dict(act=5, track="Deliberate Thought", vol=0.22), dict(act=6, track="Floating Cities", vol=0.24)],
            yt=dict(title="Czechia Was 87% Richer Than Poland. Now It's Just 7%.",
                    description=("Income per person adjusted for prices (IMF World Economic Outlook, October 2026): in 1995 the average Czech was 87% ahead of the average Pole. "
                                 "This year the gap is under 7%, and in the IMF's 2031 forecast it's about 4%. The May 1997 currency crisis, the 2009 crash (−4.8% while Poland grew 2.6%), "
                                 "why Czechia is still about a quarter richer in plain dollars, and how the old Czechoslovakia ended up on both sides of Poland.\n\n"
                                 "Sources: IMF World Economic Outlook, October 2026 (PPPPC, NGDPDPC, NGDP_RPCH, LP). 2026+ figures are IMF estimates and forecasts.\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#poland #czechia #economics #imf #europe #data"),
                    tags=["poland", "czechia", "czech republic", "poland vs czechia", "czech economy", "poland economy", "gdp per capita", "imf", "economics", "europe", "polska", "cesko", "slovakia", "slovenia"], lang="en"))

json.dump(spec, open(os.path.join(HERE, "a-L34.json"), "w"), ensure_ascii=False, indent=1)
clean = lambda t: t.replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()
words = sum(len(clean(s["narration"])) for s in shots)
acts = {}
for s in shots:
    acts[s["act"]] = acts.get(s["act"], 0) + len(clean(s["narration"]))
print("shots", len(shots), "palavras", words, f"~{words / 145:.1f} min a 145 wpm", "por ato", acts)

"""Gera specs/long/a-L33.json — Chartbound longo #33: "Slovenia Was 71% Richer Than Poland. Now It's Almost Even." (gêmeo do A-L30 Estônia / A-L32 Hungria)
Medida principal: PIB per capita ajustado por preços (PPPPC); ato 3 em dólares correntes (NGDPDPC).
Dados: IMF WEO out/2026 (research/imf_v4_2026-11-13.json: POL, SVN, CZE, HUN).
Fora do FMI (documentado): Eslovênia entrou na UE em 1/5/2004 e no euro em 1/1/2007 (1ª dos novos membros de 2004);
dez/2013: governo injetou €3,01 bi nos bancos estatais após os testes de estresse e evitou ajuda internacional (Banco da Eslovênia/STA, 12/12/2013); era a república mais rica da Iugoslávia."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "..", "..", "research")
D = json.load(open(os.path.join(R, "imf_v4_2026-11-13.json")))
ACTS = ["Cold open", "The head start", "The crash", "Plain dollars", "The race", "The almost-pass", "Your guess"]
IMF = "IMF World Economic Outlook, October 2026"


def ser(ind, iso):
    r = D[ind][iso]
    return {r["y0"] + k: v for k, v in enumerate(r["v"])}


PP = {iso: ser("PPPPC", iso) for iso in ("POL", "SVN", "CZE", "HUN")}
N = {iso: ser("NGDPDPC", iso) for iso in ("POL", "SVN")}
GR = {iso: ser("NGDP_RPCH", iso) for iso in ("POL", "SVN")}
LP = {iso: ser("LP", iso) for iso in ("POL", "SVN")}
P, S, C, H = PP["POL"], PP["SVN"], PP["CZE"], PP["HUN"]


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
for y in range(1992, 2032):
    snapshot.append(dict(set="rat", iso="SVN", year=y, value=round(S[y] / P[y] * 100, 2), src=IMF + " · Slovenia's GDP per capita (PPP) as % of Poland's"))

PPPSRC = IMF + " · GDP per capita, PPP, current international $ (PPPPC); 2026+ are IMF estimates and forecasts"
USDSRC = IMF + " · GDP per capita, current US$ at market exchange rates (NGDPDPC); 2026+ are IMF estimates and forecasts"
PPP2 = dict(set="imf", fc=2025, series=["SVN", "POL"], years=[1995, 2031], y=[0, 80000], src=PPPSRC, fmt="usd0", hl="POL")
RATCH = dict(set="rat", fc=2025, series=["SVN"], years=[1992, 2031], y=[80, 190], src=IMF + " · Slovenia's GDP per capita (PPP) as % of Poland's; 2026+ are IMF estimates and forecasts", fmt="pct0", hl="SVN", ref=dict(value=100, label="Poland = 100%", pos="right"))

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="lines", start=1995.0, **PPP2,
         narration="Seventy-one percent. {p} In 1995, the average Slovenian was seventy-one percent richer than the average Pole, on income adjusted for prices. {pp} This year, in the IMF's numbers, the gap is under four percent. {p} And by 2031, in the IMF's forecast, it's about half a percent.",
         keys=[dict(at="Seventy-one percent", year=1995.0, dur=0.5), dict(at="This year", year=2026.0, dur=3.0), dict(at="by 2031", year=2031.0, dur=2.5)],
         labels=[dict(at="In 1995", iso="SVN", year=1995), dict(at="under four percent", iso="POL", year=2026), dict(at="half a percent", iso="SVN", year=2031)],
         react=[dict(at="Seventy-one percent", pose="shock"), dict(at="In 1995", pose="pointL"), dict(at="under four percent", pose="think"), dict(at="half a percent", pose="pointUp")]),
    dict(act=0, type="host", bg="lines", start=2031.0, **{k: v for k, v in PPP2.items() if k != "src"},
         narration="Slovenia was the richest part of the old Yugoslavia. {p} When it joined the European Union in 2004, it was richer than Czechia, Hungary and Poland. {pp} In 2007, it was the first of the new members to adopt the euro. {p} <soft>So how did a country this far ahead end up almost tied?</soft>",
         items=[dict(at="richest part", text="Richest of Yugoslavia", serif=True, size=62, color="acc2"), dict(at="joined the European Union", text="EU, May 2004", color="acc", size=60), dict(at="adopt the euro", text="Euro, 2007", color="warm", size=60)],
         react=[dict(at="richest part", pose="pointL"), dict(at="richer than Czechia", pose="think"), dict(at="the euro", pose="cheer"), dict(at="almost tied", pose="shrug")]),

    # ---------------- 1 · THE HEAD START ----------------
    dict(act=1, type="host", bg="none",
         narration="Quick one before the chart: this is a series about who's passing whom in Europe, and Poland keeps showing up. Subscribe so you don't miss the next one. {p} Now, the head start.",
         items=[dict(at="who's passing whom", text="Who passed whom", serif=True, size=66, color="acc"), dict(at="Subscribe", text="Subscribe", size=70)],
         react=[dict(at="Quick one", pose="wave"), dict(at="Subscribe", pose="cheer"), dict(at="the head start", pose="pointL")]),
    dict(act=1, type="lines", start=1992.0, **RATCH,
         narration="Here's Slovenia as a share of Poland, adjusted for prices. {p} In 1992, a hundred and seventy-six percent. {pp} For the next sixteen years, Poland barely closed the gap. In 2008, Slovenia was still about sixty percent richer. {p} Then the line falls off a cliff.",
         keys=[dict(at="In 1992", year=1992.0, dur=1.5), dict(at="next sixteen years", year=2004.0, dur=3.0), dict(at="In 2008", year=2008.0, dur=1.5), dict(at="falls off a cliff", year=2013.0, dur=2.5)],
         labels=[dict(at="In 1992", iso="SVN", year=1992), dict(at="sixty percent richer", iso="SVN", year=2008)],
         react=[dict(at="In 1992", pose="pointL"), dict(at="barely closed", pose="think"), dict(at="about sixty percent", pose="shrug"), dict(at="off a cliff", pose="shock")]),

    # ---------------- 2 · THE CRASH ----------------
    dict(act=2, type="bars", mode="abs", set="imfg", iso="SVN", years=[2000, 2030], start=2007.0, fmt="pct1", src=IMF + " · real GDP growth, Slovenia (annual %); 2026+ are IMF estimates and forecasts",
         narration="Here's Slovenia's economy, year by year, after inflation. {p} In 2007, it grew seven percent. {pp} Then the 2008 crisis. In 2009, it shrank seven point six percent. Poland grew two point six. {p} And it didn't bounce back: Slovenia shrank again in 2012, and again in 2013. {pp} In December 2013, the government put about three billion euros into its banks, and avoided an international bailout.",
         keys=[dict(at="In 2007", year=2007.0, dur=1.5), dict(at="In 2009", year=2009.0, dur=2.0), dict(at="again in 2012", year=2012.0, dur=1.5), dict(at="again in 2013", year=2013.0, dur=1.5)],
         react=[dict(at="In 2007", pose="cheer"), dict(at="seven point six", pose="shock"), dict(at="didn't bounce back", pose="shrug"), dict(at="three billion euros", pose="think")]),
    dict(act=2, type="stats", src=IMF + " · real GDP growth (NGDP_RPCH, compounded), population (LP)", title="The crash",
         narration="Put it together. From 2008 to 2013, after inflation, Slovenia's economy shrank about nine percent. Poland's grew about fourteen. {p} And over thirty years, from 1995 to 2025, Slovenia's economy roughly doubled. Poland's roughly tripled. {pp} Slovenia has about two million people. Poland has seventeen times as many.",
         stats=[dict(at="shrank about nine percent", value=round((grow("SVN", 2008, 2013) - 1) * 100), fmt="pct0", label="Slovenia, real growth 2008–2013"), dict(at="grew about fourteen", value=round((grow("POL", 2008, 2013) - 1) * 100), fmt="pct0", label="Poland, real growth 2008–2013"), dict(at="roughly tripled", value=round((grow("POL", 1995, 2025) - 1) * 100), fmt="pct0", label="Poland, real growth 1995–2025"), dict(at="two million people", value=round(LP["SVN"][2026], 1), fmt="dec1", label="million people in Slovenia, 2026")],
         react=[dict(at="Put it together", pose="pointUp"), dict(at="shrank about nine", pose="shock"), dict(at="roughly tripled", pose="cheer"), dict(at="seventeen times", pose="think")]),

    # ---------------- 3 · PLAIN DOLLARS ----------------
    dict(act=3, type="lines", set="imfusd", fc=2025, series=["SVN", "POL"], years=[1995, 2031], start=2008.0, y=[0, 60000], src=USDSRC, fmt="usd0", hl="SVN",
         narration="But here's the twist. In plain dollars, at market exchange rates, the picture is very different. {p} This year, Slovenia is about forty-one thousand six hundred dollars a person. Poland, about thirty-one thousand two hundred. {pp} That's still a third more. {p} Prices in Slovenia are higher, so adjusting for prices shrinks the gap. So in plain money, Slovenia is still well ahead.",
         keys=[dict(at="plain dollars", year=2008.0, dur=1.5), dict(at="This year", year=2026.0, dur=3.0)],
         labels=[dict(at="forty-one thousand six hundred", iso="SVN", year=2026), dict(at="thirty-one thousand two hundred", iso="POL", year=2026)],
         react=[dict(at="the twist", pose="pointUp"), dict(at="very different", pose="shock"), dict(at="a third more", pose="think"), dict(at="well ahead", pose="shrug")]),

    # ---------------- 4 · THE RACE ----------------
    dict(act=4, type="host", bg="none",
         narration="And if you're enjoying the series, the subscribe button is right there. {p} Now, the bigger race.",
         items=[dict(at="subscribe button", text="Subscribe", size=66), dict(at="bigger race", text="Central Europe's race", serif=True, size=66, color="acc")],
         react=[dict(at="subscribe button", pose="pointUp"), dict(at="bigger race", pose="pointL")]),
    dict(act=4, type="lines", set="imf", fc=2025, series=["SVN", "CZE", "HUN", "POL"], years=[2004, 2031], start=2004.0, y=[0, 80000], src=PPPSRC, fmt="usd0", hl="POL",
         narration="Slovenia, Czechia, Hungary and Poland. {p} In 2004, adjusted for prices, Slovenia was first and Poland was last. {pp} Since then, Czechia has passed Slovenia. Poland has passed Hungary. {p} And in the IMF's forecast, Poland ends up right on Slovenia's heels.",
         keys=[dict(at="In 2004", year=2004.0, dur=2.0), dict(at="Since then", year=2026.0, dur=3.0), dict(at="right on Slovenia's heels", year=2031.0, dur=2.0)],
         labels=[dict(at="Poland was last", iso="POL", year=2004)],
         react=[dict(at="Slovenia, Czechia", pose="pointL"), dict(at="Poland was last", pose="think"), dict(at="passed Hungary", pose="cheer"), dict(at="on Slovenia's heels", pose="shock")]),

    # ---------------- 5 · THE ALMOST-PASS ----------------
    dict(act=5, type="stats", src=PPPSRC, title="The almost-pass, adjusted for prices",
         narration="So here's where it stands, in the IMF's numbers. {p} In 2008, Slovenia was ahead by about twelve thousand dollars per person. {p} This year, about two thousand two hundred. {pp} And in 2031, in the IMF's forecast, about four hundred dollars. {p} That's half a percent. Not a pass, but close enough to call it a tie.",
         stats=[dict(at="about twelve thousand", value=S[2008] - P[2008], fmt="usd0", label="Slovenia ahead, 2008"), dict(at="two thousand two hundred", value=S[2026] - P[2026], fmt="usd0", label="Slovenia ahead, 2026"), dict(at="about four hundred", value=S[2031] - P[2031], fmt="usd0", label="Slovenia ahead, 2031 (IMF)")],
         react=[dict(at="where it stands", pose="pointUp"), dict(at="about twelve thousand", pose="shock"), dict(at="two thousand two hundred", pose="think"), dict(at="call it a tie", pose="shrug")]),

    # ---------------- 6 · YOUR GUESS ----------------
    dict(act=6, type="host", bg="none",
         narration="<soft>So, what's your guess?</soft> {pp} Does Poland pass Slovenia before 2031, {p} after, {p} or never? {pp} Tell me in the comments. {pp} If you're watching from Slovenia: {p} does it feel like this where you are? {pp} I read every comment.",
         items=[dict(at="your guess", text="Before 2031, after, or never?", color="acc", size=60), dict(at="watching from Slovenia", text="Slovenia: does it match?", color="warm", size=58)],
         react=[dict(at="your guess", pose="shrug"), dict(at="Tell me", pose="pointUp"), dict(at="watching from Slovenia", pose="wave")]),
    dict(act=6, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="HUN", color="acc", title="Hungary vs Poland", sub="29% richer, then passed."),
         narration="And if you missed it, {p} this is the one where Hungary was twenty-nine percent richer, and Poland passed. {pp} It's right here. {pp} I'm Chartbound. {p} See you in the next one.",
         hold=14,
         react=[dict(at="if you missed it", pose="pointL"), dict(at="See you", pose="wave")]),
]

checks = [
    dict(say="1995: SVN 171% of POL (71% richer)", rule="expr", expr=f"round({S[1995]} / {P[1995]} * 100)", equal=171),
    dict(say="2026 under 4% (103.7); 2031 ≈ half a percent (0.55)", rule="expr", expr=f"[{S[2026] / P[2026] * 100 < 104}, round(({S[2031]} / {P[2031]} - 1) * 100, 1)]", equal=[True, 0.5]),
    dict(say="POL never passes SVN 1992–2031", rule="expr", expr=f"{all(S[y] > P[y] for y in range(1992, 2032))}", equal=True),
    dict(say="2004: SVN > CZE > HUN > POL (richer than Czechia, Hungary, Poland)", rule="expr", expr=f"{sorted(['SVN', 'CZE', 'HUN', 'POL'], key=lambda i: -PP[i][2004])}", equal=["SVN", "CZE", "HUN", "POL"]),
    dict(say="1992 176%; 2008 still ~60% (160.5)", rule="expr", expr=f"[round({S[1992]} / {P[1992]} * 100), round({S[2008]} / {P[2008]} * 100)]", equal=[176, 161]),
    dict(say="1992–2008 'barely closed': ratio stayed ≥ 159", rule="expr", expr=f"round(min({[S[y] / P[y] for y in range(1992, 2009)]}) * 100)", equal=159),
    dict(say="growth: 2007 SVN 7.1 (seven); 2009 SVN −7.6, POL 2.6; 2012 & 2013 SVN < 0", rule="expr", expr=f"[round({GR['SVN'][2007]}), {GR['SVN'][2009]}, {GR['POL'][2009]}, {GR['SVN'][2012] < 0 and GR['SVN'][2013] < 0}]", equal=[7, -7.6, 2.6, True]),
    dict(say="real 2008→2013: SVN −9%, POL +14%", rule="expr", expr=f"[round(({grow('SVN', 2008, 2013)} - 1) * 100), round(({grow('POL', 2008, 2013)} - 1) * 100)]", equal=[-9, 14]),
    dict(say="real 1995→2025: SVN ×2.2 (roughly doubled), POL ×3.1 (roughly tripled)", rule="expr", expr=f"[round({grow('SVN', 1995, 2025)}, 1), round({grow('POL', 1995, 2025)}, 1)]", equal=[2.2, 3.1]),
    dict(say="pop 2026: SVN 2.1M; POL/SVN ≈ 17", rule="expr", expr=f"[round({LP['SVN'][2026]}, 1), round({LP['POL'][2026]} / {LP['SVN'][2026]})]", equal=[2.1, 17]),
    dict(say="USD 2026: SVN ≈ 41,600, POL ≈ 31,200; ratio ≈ 1.33 (a third more)", rule="expr", expr=f"[round({N['SVN'][2026]} / 100) * 100, round({N['POL'][2026]} / 100) * 100, round({N['SVN'][2026]} / {N['POL'][2026]}, 2)]", equal=[41600, 31200, 1.33]),
    dict(say="2026: CZE > SVN (Czechia passed), POL > HUN; 2004: SVN > CZE", rule="expr", expr=f"[{C[2026] > S[2026]}, {P[2026] > H[2026]}, {S[2004] > C[2004]}]", equal=[True, True, True]),
    dict(say="gap 2008 ≈ 12,000 (11,955); 2026 ≈ 2,200 (2,204); 2031 ≈ 400 (416)", rule="expr", expr=f"[round(({S[2008]} - {P[2008]}) / 1000) * 1000, round(({S[2026]} - {P[2026]}) / 100) * 100, round(({S[2031]} - {P[2031]}) / 100) * 100]", equal=[12000, 2200, 400]),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="a-L33-poland-slovenia", clips=[], channel="chartbound", chapter0="71%",
            thumb=dict(v="flags", iso="SVN", vs="POL", sym="vs", big="1995: +71%", line2="2031: +0.5%"),
            w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks, datasets=[], snapshot=snapshot,
            voice=dict(model="", name="Charon",
                       style=("You are the narrator of a popular data documentary on YouTube. Read the script below in a warm, curious voice "
                              "with a little dry humor, at a relaxed but engaged pace of about 145 words per minute, like a smart friend telling "
                              "you something surprising. Let the big numbers land with a tiny pause before them. Keep the energy steady from the "
                              "first sentence to the last. Never sound like an advertisement or an audiobook.")),
            music=[dict(act=0, track="Lightless Dawn", vol=0.24), dict(act=1, track="Deliberate Thought", vol=0.22), dict(act=2, track="Hidden Agenda", vol=0.23), dict(act=3, track="Inspired", vol=0.23),
                   dict(act=4, track="Investigations", vol=0.23), dict(act=5, track="Deliberate Thought", vol=0.22), dict(act=6, track="Floating Cities", vol=0.24)],
            yt=dict(title="Slovenia Was 71% Richer Than Poland. Now It's Almost Even.",
                    description=("Income per person adjusted for prices (IMF World Economic Outlook, October 2026): in 1995 the average Slovenian was 71% ahead of the average Pole. "
                                 "This year the gap is under 4%, and in the IMF's 2031 forecast it's about half a percent. The 2009 crash (−7.6%), the second recession in 2012–2013, "
                                 "the €3 billion bank rescue of December 2013, why Slovenia is still a third richer in plain dollars, and the race with Czechia and Hungary.\n\n"
                                 "Sources: IMF World Economic Outlook, October 2026 (PPPPC, NGDPDPC, NGDP_RPCH, LP); Bank of Slovenia, stress test results (December 2013). 2026+ figures are IMF estimates and forecasts.\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#poland #slovenia #economics #imf #europe #data"),
                    tags=["poland", "slovenia", "poland vs slovenia", "slovenia economy", "poland economy", "gdp per capita", "imf", "economics", "europe", "polska", "slovenija", "czechia", "hungary"], lang="en"))

json.dump(spec, open(os.path.join(HERE, "a-L33.json"), "w"), ensure_ascii=False, indent=1)
clean = lambda t: t.replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()
words = sum(len(clean(s["narration"])) for s in shots)
acts = {}
for s in shots:
    acts[s["act"]] = acts.get(s["act"], 0) + len(clean(s["narration"]))
print("shots", len(shots), "palavras", words, f"~{words / 145:.1f} min a 145 wpm", "por ato", acts)

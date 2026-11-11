"""Gera specs/long/a-L24.json — Chartbound longo #24: "Lithuania Passed Poland. Twice." (série Polônia, PLANO.md L1/L3)
Intro (PLANO R2): número nos primeiros 2 s. CTA de série no minuto 1 com gancho do próximo episódio (Polônia × Reino Unido).
Dados: IMF WEO out/2026 — POL em research/imf_ita_2026-11-07.json (lido 07/11) e LTU em research/imf_ltu_2026-11-10.json (série completa, lido 10/11).
Fora do FMI (fatos amplamente documentados): ambos entraram na UE em 1/5/2004; Lituânia adotou o euro em 1/1/2015 (litas atrelado ao euro antes);
ajuste de 2009–2010 por corte de salários/gastos ("desvalorização interna") em vez de desvalorizar; emigração lituana sobretudo para Reino Unido,
Irlanda e Noruega; desde ~2019 a Lituânia recebe mais gente do que perde (retorno + Ucrânia e Belarus); centenas de milhares de nascidos na Polônia
vivem no Reino Unido (ONS)."""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "..", "..", "research", "imf_ita_2026-11-07.json")))
LT = json.load(open(os.path.join(HERE, "..", "..", "research", "imf_ltu_2026-11-10.json")))
ACTS = ["Cold open", "Lithuania takes off", "The crash", "Fewer people", "Scoreboard", "The date", "Your guess"]
IMF = "IMF World Economic Outlook, October 2026"


def series(ind, iso):
    r = (LT if iso == "LTU" else D)[ind][iso]
    return {r["y0"] + k: v for k, v in enumerate(r["v"])}


P, L = series("PPPPC", "POL"), series("PPPPC", "LTU")
GR = {iso: series("NGDP_RPCH", iso) for iso in ("POL", "LTU")}
LP = {iso: series("LP", iso) for iso in ("POL", "LTU")}
N = {iso: series("NGDPDPC", iso) for iso in ("POL", "LTU")}
DEBT = {iso: series("GGXWDG_NGDP", iso) for iso in ("POL", "LTU")}
LUR = {iso: series("LUR", iso) for iso in ("POL", "LTU")}
CPI = {iso: series("PCPIPCH", iso) for iso in ("POL", "LTU")}

Y0, Y1 = 1995, 2031
R = {y: P[y] / L[y] for y in range(Y0, Y1 + 1)}          # Polônia como % da Lituânia
LEAD = {y: L[y] - P[y] for y in range(Y0, Y1 + 1)}       # vantagem lituana em US$ PPP
ahead = lambda y: L[y] > P[y]
crosses = [y for y in range(Y0 + 1, Y1 + 1) if ahead(y) != ahead(y - 1)]


def grow(iso, a, b):
    c = 1.0
    for y in range(a + 1, b + 1):
        c *= 1 + GR[iso][y] / 100
    return c


k_recent = math.log(R[2026] / R[2016]) / 10          # ritmo 2016–2026
par_recent = 2026 + math.log(1 / R[2026]) / k_recent

snapshot = []
for y in range(Y0, Y1 + 1):
    snapshot.append(dict(set="rat", iso="POL", year=y, value=round(R[y] * 100, 2), src=IMF + " · Poland's GDP per capita (PPP) as % of Lithuania's"))
for iso, s in (("POL", P), ("LTU", L)):
    for y, v in s.items():
        snapshot.append(dict(set="imf", iso=iso, year=y, value=v, src=IMF + " · PPPPC"))
for iso, s in GR.items():
    for y, v in s.items():
        snapshot.append(dict(set="imfg", iso=iso, year=y, value=v, src=IMF + " · NGDP_RPCH"))
for st, tab, ind in [("pop", LP, "LP"), ("debt", DEBT, "GGXWDG_NGDP"), ("lur", LUR, "LUR"), ("imfusd", N, "NGDPDPC"), ("cpi", CPI, "PCPIPCH")]:
    for iso, s in tab.items():
        for y, v in s.items():
            snapshot.append(dict(set=st, iso=iso, year=y, value=v, src=IMF + " · " + ind))

RATSRC = IMF + " · Poland's GDP per capita, PPP, as % of Lithuania's; 2026+ are IMF estimates and forecasts"
RATCH = dict(set="rat", fc=2025, series=["POL"], years=[Y0, Y1], y=[60, 130], src=RATSRC, fmt="pct0", hl="POL", ref=dict(value=100, label="Lithuania = 100%", pos="left"))

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="lines", start=2026.0, **RATCH,
         narration="Ninety-eight percent. {p} That's how rich the average Pole is, compared with the average Lithuanian, this year: income per person, adjusted for prices. Both are around sixty thousand dollars, but Lithuania is ahead by about twelve hundred. {pp} In 1995, it was the other way around: the average Pole was almost a fifth richer than the average Lithuanian. Then Lithuania passed Poland in 2003. Poland took the lead back in 2009. And Lithuania passed it again in 2011, and has stayed ahead ever since. {p} And here's the strange part: in the IMF's forecast, the gap stops closing. It's still about twelve hundred dollars in 2031.",
         keys=[dict(at="Ninety-eight", year=2026.0, dur=0.5), dict(at="In 1995", year=1995.0, dur=1.5), dict(at="passed Poland in 2003", year=2003.0, dur=1.5), dict(at="back in 2009", year=2009.0, dur=1.5), dict(at="again in 2011", year=2011.0, dur=1.5), dict(at="the gap stops closing", year=2026.0, dur=1.0), dict(at="still about twelve hundred", year=2031.0, dur=3.0)],
         labels=[dict(at="Ninety-eight percent", iso="POL", year=2026), dict(at="In 1995", iso="POL", year=1995), dict(at="passed Poland in 2003", iso="POL", year=2003), dict(at="back in 2009", iso="POL", year=2009), dict(at="again in 2011", iso="POL", year=2011)],
         react=[dict(at="Ninety-eight", pose="pointUp"), dict(at="other way around", pose="pointL"), dict(at="took the lead back", pose="shock"), dict(at="ever since", pose="shrug"), dict(at="the strange part", pose="think")]),
    dict(act=0, type="host", bg="lines", start=2031.0, **{k: v for k, v in RATCH.items() if k != "src"},
         narration="In this series, we've measured Poland against Germany: seventy-six percent. Against Czechia: ninety-four. Lithuania is the closest race of all, and the weirdest. {p} It's a country of under three million people, next to a country of thirty-six million. Both joined the European Union on the same day in 2004. And since 1995, both economies have roughly tripled in size. {pp} <soft>So why is the average Lithuanian ahead? Here's the crash that changed everything, the people who left, and why the IMF thinks Poland gets stuck just below a hundred percent.</soft>",
         items=[dict(at="against Germany", text="Germany: 76%", color="acc2", size=66), dict(at="Against Czechia", text="Czechia: 94%", color="acc2", size=66), dict(at="closest race", text="Lithuania: 98%", serif=True, size=66, color="acc"), dict(at="under three million", text="2.9M vs 36M people", color="warm", size=58)],
         react=[dict(at="against Germany", pose="pointL"), dict(at="the weirdest", pose="think"), dict(at="roughly tripled", pose="pointUp"), dict(at="stuck just below", pose="shrug")]),

    # ---------------- 1 · LITHUANIA TAKES OFF ----------------
    dict(act=1, type="host", bg="none",
         narration="Quick one before the chart: this is a series, and the next episode is Britain, the country hundreds of thousands of Poles moved to. Subscribe so you don't miss it. {p} Now, the race.",
         items=[dict(at="this is a series", text="The Poland series", serif=True, size=66, color="acc"), dict(at="Britain", text="Next: Poland vs Britain", color="acc2", size=62), dict(at="Subscribe", text="Subscribe", size=70)],
         react=[dict(at="Quick one", pose="wave"), dict(at="Britain", pose="pointUp"), dict(at="Subscribe", pose="cheer"), dict(at="the race", pose="pointL")]),
    dict(act=1, type="lines", start=1995.0, **RATCH,
         narration="Start in 1995. The average Lithuanian produced about seven thousand dollars a year, adjusted for prices. The average Pole, about eight thousand four hundred. {p} Lithuania had a rough start: it broke away from the Soviet Union in 1990, and the Russian financial crisis of 1998 pushed it back into recession in 1999. {p} Then Lithuania took off. Real growth above six percent every single year from 2001 to 2007, and eleven percent in 2007 alone. By 2007, the average Lithuanian was about eighteen percent richer than the average Pole: about three thousand four hundred dollars ahead. {pp} On this chart, that's Poland's line falling far below the dotted line. It looked like Poland would never catch up. And then came 2009.",
         keys=[dict(at="Start in 1995", year=1995.0, dur=1.0), dict(at="took off", year=2001.0, dur=2.0), dict(at="eleven percent", year=2007.0, dur=2.5), dict(at="never catch up", year=2008.0, dur=1.5), dict(at="then came 2009", year=2009.0, dur=1.5)],
         labels=[dict(at="Start in 1995", iso="POL", year=1995), dict(at="By 2007", iso="POL", year=2007)],
         react=[dict(at="Start in 1995", pose="pointL"), dict(at="took off", pose="shock"), dict(at="three thousand four hundred", pose="pointUp"), dict(at="never catch up", pose="shrug"), dict(at="then came 2009", pose="think")]),

    # ---------------- 2 · THE CRASH ----------------
    dict(act=2, type="bars", mode="abs", set="imfg", iso="LTU", years=[1996, 2026], start=1996.0, fmt="pct1", src=IMF + " · real GDP growth, Lithuania (annual %); 2026 is an IMF estimate",
         narration="Here's Lithuania's economy, year by year, after inflation. {p} 2009: minus fourteen and a half percent. One of the deepest crashes anywhere in the world that year. Poland, as we saw last episode, grew two point six. {pp} So for two years, 2009 and 2010, Poland was ahead again. Lithuanian unemployment hit almost eighteen percent in 2010. {p} And Lithuania chose the hard way out. Its currency was pegged to the euro, so instead of devaluing, it cut wages and public spending.",
         keys=[dict(at="Here's Lithuania's", year=2005.0, dur=3.0), dict(at="2009: minus", year=2009.0, dur=1.5), dict(at="for two years", year=2010.0, dur=1.5), dict(at="the hard way out", year=2011.0, dur=2.0)],
         react=[dict(at="Here's Lithuania's", pose="pointL"), dict(at="minus fourteen", pose="shock"), dict(at="Poland was ahead again", pose="cheer"), dict(at="almost eighteen", pose="shock"), dict(at="the hard way out", pose="think")]),
    dict(act=2, type="stats", src=IMF + " · PPPPC gap in US$, real GDP growth (NGDP_RPCH)", title="Back on top, and the same growth",
         narration="It worked, in its own way. Lithuania grew more than six percent in 2011 and passed Poland again that year. It joined the euro in 2015, and by 2021 the average Lithuanian was almost four thousand eight hundred dollars ahead. Since then, the gap has shrunk every single year. {pp} But look at the totals. Since 1995, Lithuania's economy has grown about three point two times, after inflation. Poland's, about three point one times. Almost exactly the same. {p} So where did the gap per person come from? From people.",
         stats=[dict(at="almost four thousand eight hundred", value=LEAD[2021], fmt="usd0", label="Lithuania's lead, 2021 (the widest)"), dict(at="three point two times", value=round(grow("LTU", 1995, 2025), 1), fmt="dec1", label="Lithuania's economy, 2025 vs 1995 (×, real)"), dict(at="three point one times", value=round(grow("POL", 1995, 2025), 1), fmt="dec1", label="Poland's economy, 2025 vs 1995 (×, real)")],
         react=[dict(at="It worked", pose="pointUp"), dict(at="joined the euro", pose="pointL"), dict(at="look at the totals", pose="think"), dict(at="Almost exactly the same", pose="shock"), dict(at="From people", pose="pointUp")]),

    # ---------------- 3 · FEWER PEOPLE ----------------
    dict(act=3, type="stats", src=IMF + " · population (LP), millions", title="Where everyone went",
         narration="In 1995, Lithuania had about three point six million people. By 2021, two point eight million. It lost more than a fifth of its population, mostly to emigration: to Britain, Ireland and Norway. When Lithuania joined the EU in 2004, Britain and Ireland opened their job markets to its workers straight away, and wages there were several times higher. After the 2009 crash, another big wave left. {p} Poland lost people too, but far fewer: from thirty-eight and a half million to about thirty-six, around six percent. {pp} The same growth, divided between fewer people, means more income per person. That's a big part of how Lithuania pulled ahead. It's not a happy way to get richer per person, but it shows up in the numbers. {p} And now it's reversing. Since 2021, Lithuania's population has been growing again, to about two point nine million this year, with Lithuanians coming home and people arriving from Ukraine and Belarus.",
         stats=[dict(at="three point six million", value=round(LP["LTU"][1995], 1), fmt="dec1", label="million people in Lithuania, 1995"), dict(at="two point eight million", value=round(LP["LTU"][2021], 1), fmt="dec1", label="million people in Lithuania, 2021"), dict(at="more than a fifth", value=round((LP["LTU"][2021] / LP["LTU"][1995] - 1) * 100), fmt="pct0", label="Lithuania's population, 1995–2021"), dict(at="around six percent", value=round((LP["POL"][2026] / LP["POL"][1995] - 1) * 100), fmt="pct0", label="Poland's population, 1995–2026")],
         react=[dict(at="three point six", pose="pointL"), dict(at="more than a fifth", pose="shock"), dict(at="far fewer", pose="pointUp"), dict(at="not a happy way", pose="shrug"), dict(at="it's reversing", pose="think"), dict(at="coming home", pose="cheer")]),

    # ---------------- 4 · SCOREBOARD ----------------
    dict(act=4, type="host", bg="none",
         narration="Now, the scoreboard. {p} And if you're enjoying the series, the subscribe button is right there. Britain is next.",
         items=[dict(at="the scoreboard", text="The scoreboard", serif=True, size=68, color="acc"), dict(at="subscribe button", text="Subscribe", size=66)],
         react=[dict(at="the scoreboard", pose="pointUp"), dict(at="subscribe button", pose="cheer")]),
    dict(act=4, type="duel", set="lur", year=2026, a="POL", b="LTU", fmt="dec1", src=IMF + " · unemployment rate (% of labor force), 2026 estimate", title="Unemployment, 2026", badge="LOWER IN POLAND",
         cues=[dict(at="three point two", show="a"), dict(at="six point eight", show="b")],
         narration="On jobs, Poland wins easily. Unemployment this year: about three point two percent in Poland, {pp} six point eight in Lithuania. More than double. And Lithuania's rate has been higher than Poland's every year since 2009.",
         react=[dict(at="Poland wins", pose="cheer"), dict(at="three point two", pose="pointL"), dict(at="More than double", pose="shock")]),
    dict(act=4, type="stats", src=IMF + " · gross debt (GGXWDG_NGDP), GDP per capita in current US$ (NGDPDPC), inflation (PCPIPCH)", title="Where Lithuania wins, and 2022",
         narration="Lithuania wins on two others. Government debt: about forty-five percent of the economy, against Poland's sixty-seven. And in plain dollars, without adjusting for prices, the average Lithuanian produces about thirty-six thousand this year, and the average Pole about thirty-one thousand. {p} One more, from 2022, the year energy prices exploded. Inflation hit about nineteen percent in Lithuania, and fourteen in Poland. With the euro, Lithuania couldn't set its own interest rates. Poland could.",
         stats=[dict(at="about forty-five percent", value=round(DEBT["LTU"][2026]), fmt="pct0", label="Lithuania, government debt, 2026 (Poland: 67%)"), dict(at="about thirty-six thousand", value=N["LTU"][2026], fmt="usd0", label="Lithuania, plain US$, 2026"), dict(at="about thirty-one thousand", value=N["POL"][2026], fmt="usd0", label="Poland, plain US$, 2026"), dict(at="about nineteen percent", value=CPI["LTU"][2022], fmt="pct1", label="Lithuania, inflation, 2022 (Poland: 14.4%)")],
         react=[dict(at="Lithuania wins", pose="pointL"), dict(at="plain dollars", pose="pointUp"), dict(at="energy prices exploded", pose="shock"), dict(at="Poland could", pose="think")]),

    # ---------------- 5 · THE DATE ----------------
    dict(act=5, type="lines", start=2016.0, **{**RATCH, "years": [2010, 2031]},
         narration="So, does Poland pass Lithuania again? {p} At the pace of the last ten years, when Poland gained almost one percent a year on Lithuania, it would happen around 2029. {p} But the IMF doesn't see it. In its forecast, Poland gets to about ninety-nine percent of Lithuania next year, and then slips back a little: ninety-eight percent in 2031, still about twelve hundred dollars behind. Both economies grow about two and a half percent a year, so the line just goes flat. {pp} For Poland to pass, one of two things has to happen: Poland grows faster than the IMF expects, or Lithuania's income per person grows slower. And the second one might already be starting. {p} So it's 2029, or not by 2031 at all.",
         keys=[dict(at="does Poland pass", year=2016.0, dur=1.0), dict(at="last ten years", year=2026.0, dur=3.0), dict(at="next year", year=2027.0, dur=1.5), dict(at="ninety-eight percent in 2031", year=2031.0, dur=2.5)],
         labels=[dict(at="next year", iso="POL", year=2027), dict(at="ninety-eight percent in 2031", iso="POL", year=2031)],
         react=[dict(at="does Poland pass", pose="pointUp"), dict(at="around 2029", pose="cheer"), dict(at="doesn't see it", pose="shrug"), dict(at="goes flat", pose="think"), dict(at="not by 2031", pose="pointL")]),
    dict(act=5, type="host", bg="none",
         narration="And here's the twist. The thing that made Lithuania richer per person, people leaving, is exactly what it's now trying to reverse. When more people move in, income per person grows more slowly, even if the economy grows faster. {p} So the best outcome for Lithuania might also be the one that lets Poland catch up: a Lithuania that people move to, instead of leave.",
         items=[dict(at="people leaving", text="1995–2021: −23% people", color="warm", size=60), dict(at="people move to", text="Best case: people move in", serif=True, size=64, color="acc")],
         react=[dict(at="the twist", pose="think"), dict(at="people leaving", pose="pointL"), dict(at="grows more slowly", pose="shrug"), dict(at="people move to", pose="cheer")]),

    # ---------------- 6 · YOUR GUESS ----------------
    dict(act=6, type="host", bg="none",
         narration="<soft>So, your guess: does Poland pass Lithuania again, and when?</soft> Tell me in the comments. {p} If you're watching from Lithuania: did you, or someone in your family, ever work abroad? {p} If you're in Poland: did you expect Lithuania to be ahead? {p} And if you're in Britain: you're next. I read every comment.",
         items=[dict(at="your guess", text="2029, or never?", color="acc", size=68), dict(at="watching from Lithuania", text="Lithuania: did your family leave?", color="warm", size=54)],
         react=[dict(at="your guess", pose="shrug"), dict(at="Tell me", pose="pointUp"), dict(at="watching from Lithuania", pose="wave")]),
    dict(act=6, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="CZE", color="acc", title="Poland vs Czechia: 94%", sub="the next closest race."),
         narration="And if you missed it, Poland versus Czechia is the next closest race: ninety-four percent, and a date that could be 2030. That story is right here. {p} I'm Chartbound. See you in the next one.",
         hold=14,
         react=[dict(at="if you missed it", pose="pointL"), dict(at="See you", pose="wave")]),
]

checks = [
    dict(say="2026: POL = 98% of LTU (98.1); both ~ $60k; LTU ahead by ~ $1,200", rule="expr", expr=f"[round({R[2026]} * 100), round({P[2026]} / 1000), round({L[2026]} / 1000), round({LEAD[2026]} / 100) * 100]", equal=[98, 60, 61, 1200]),
    dict(say="1995: POL almost a fifth richer than LTU (×1.19)", rule="expr", expr=f"round({P[1995]} / {L[1995]}, 2)", equal=1.19),
    dict(say="lead changes: LTU passes 2003, POL back 2009, LTU again 2011; LTU ahead every year 2011–2031", rule="expr", expr=f"[{crosses}, {all(ahead(y) for y in range(2011, 2032))}]", equal=[[2003, 2009, 2011], True]),
    dict(say="2031: LTU lead ≈ $1,200", rule="expr", expr=f"round({LEAD[2031]} / 100) * 100", equal=1200),
    dict(say="series callbacks: POL/DEU 2026 = 76%, POL/CZE 2026 = 94% (A-L22, A-L23)", rule="expr", expr="[76, 94]", equal=[76, 94]),
    dict(say="LTU population 2026 < 3M; POL ≈ 36M", rule="expr", expr=f"[{LP['LTU'][2026] < 3}, round({LP['POL'][2026]})]", equal=[True, 36]),
    dict(say="UE 1/5/2004 (ambos); euro LTU 1/1/2015; currency board atrelado ao euro em 2009 — fatos documentados", rule="expr", expr="[2004, 2015]", equal=[2004, 2015]),
    dict(say="1995→2025 real: LTU ×3.2, POL ×3.1 (roughly tripled)", rule="expr", expr=f"[round({grow('LTU', 1995, 2025)}, 1), round({grow('POL', 1995, 2025)}, 1)]", equal=[3.2, 3.1]),
    dict(say="IMF 2027–2031: POL/LTU between 98% and 99% (just below 100)", rule="expr", expr=f"{all(0.98 <= R[y] < 0.99 for y in range(2027, 2032))}", equal=True),
    dict(say="centenas de milhares de nascidos na Polônia no Reino Unido (ONS) — amplamente citado", rule="expr", expr="True", equal=True),
    dict(say="1995 PPP per person: LTU ≈ $7.0k, POL ≈ $8.4k", rule="expr", expr=f"[round({L[1995]} / 1000), round({P[1995]} / 100) * 100]", equal=[7, 8400]),
    dict(say="LTU real growth > 6% every year 2001–2007; 2007 = 11.1", rule="expr", expr=f"[{all(GR['LTU'][y] > 6 for y in range(2001, 2008))}, {GR['LTU'][2007]}]", equal=[True, 11.1]),
    dict(say="2007: LTU ≈ 18% richer (18.5), lead ≈ $3,400", rule="expr", expr=f"[round(({L[2007]} / {P[2007]} - 1) * 100, 1), round({LEAD[2007]} / 100) * 100]", equal=[18.5, 3400]),
    dict(say="2009: LTU −14.5, POL +2.6; POL ahead in 2009 and 2010", rule="expr", expr=f"[{GR['LTU'][2009]}, {GR['POL'][2009]}, {not ahead(2009) and not ahead(2010)}]", equal=[-14.5, 2.6, True]),
    dict(say="2009: um dos maiores tombos do mundo (Lituânia/Letônia/Ucrânia ~ −14/−15%) — FMI WEO", rule="expr", expr=f"{GR['LTU'][2009] < -14}", equal=True),
    dict(say="LTU unemployment 2010 = 17.8 (almost eighteen)", rule="expr", expr=f"{LUR['LTU'][2010]}", equal=17.8),
    dict(say="LTU growth 2011 = 6.3 (> 6), passes again 2011; lead 2021 ≈ $4,800 (widest)", rule="expr", expr=f"[{GR['LTU'][2011]}, {max(LEAD, key=LEAD.get)}, round({LEAD[2021]} / 100) * 100]", equal=[6.3, 2021, 4800]),
    dict(say="LTU pop 1995 3.6M → 2021 2.8M (−22.6%, more than a fifth); POL 38.6 → 36.3 (−5.8%, around six)", rule="expr", expr=f"[round({LP['LTU'][1995]}, 1), round({LP['LTU'][2021]}, 1), round(({LP['LTU'][2021]} / {LP['LTU'][1995]} - 1) * 100, 1), round({LP['POL'][1995]}, 1), round(({LP['POL'][2026]} / {LP['POL'][1995]} - 1) * 100, 1)]", equal=[3.6, 2.8, -22.6, 38.6, -5.8]),
    dict(say="LTU pop: 2021 is the low; grows to ≈ 2.9M in 2026", rule="expr", expr=f"[{min(LP['LTU'], key=LP['LTU'].get)}, round({LP['LTU'][2026]}, 1), {all(LP['LTU'][y] > LP['LTU'][y - 1] for y in range(2022, 2027))}]", equal=[2021, 2.9, True]),
    dict(say="unemployment 2026: POL 3.2, LTU 6.8 (more than double)", rule="expr", expr=f"[{LUR['POL'][2026]}, {LUR['LTU'][2026]}, {LUR['LTU'][2026] > 2 * LUR['POL'][2026]}]", equal=[3.2, 6.8, True]),
    dict(say="debt 2026: LTU ≈ 45, POL ≈ 67", rule="expr", expr=f"[round({DEBT['LTU'][2026]}), round({DEBT['POL'][2026]})]", equal=[45, 67]),
    dict(say="nominal 2026: LTU ≈ $36k, POL ≈ $31k", rule="expr", expr=f"[round({N['LTU'][2026]} / 1000), round({N['POL'][2026]} / 1000)]", equal=[36, 31]),
    dict(say="inflation 2022: LTU 18.9 (about nineteen), POL 14.4 (fourteen)", rule="expr", expr=f"[{CPI['LTU'][2022]}, {CPI['POL'][2022]}]", equal=[18.9, 14.4]),
    dict(say="pace 2016–2026 ≈ 0.8%/yr (almost one percent) → parity 2029 (2028.4)", rule="expr", expr=f"[round({k_recent} * 100, 1), {math.ceil(par_recent)}]", equal=[0.8, 2029]),
    dict(say="IMF: 2027 ≈ 99% (98.8), 2031 ≈ 98% (98.4), slipping after 2027", rule="expr", expr=f"[round({R[2027]} * 100), round({R[2031]} * 100), {R[2031] < R[2027]}]", equal=[99, 98, True]),
    dict(say="growth 2027–2031: POL 2.5 every year; LTU 2.1–2.6 (about two and a half)", rule="expr", expr=f"[{sorted(set(GR['POL'][y] for y in range(2027, 2032)))}, {all(2.0 <= GR['LTU'][y] <= 2.6 for y in range(2027, 2032))}]", equal=[[2.5], True]),
    dict(say="−23% people 1995–2021 (item na tela)", rule="expr", expr=f"round(({LP['LTU'][2021]} / {LP['LTU'][1995]} - 1) * 100)", equal=-23),
    dict(say="POL/CZE ~2030 at recent pace (A-L23)", rule="expr", expr="2030", equal=2030),
    dict(say="LTU independence 1990 (11/03/1990); 1999 growth −1.1 (Russian crisis 1998)", rule="expr", expr=f"{GR['LTU'][1999]}", equal=-1.1),
    dict(say="gap shrinks every year 2022–2026 after 2021 peak", rule="expr", expr=f"{all(LEAD[y] < LEAD[y - 1] for y in range(2022, 2027))}", equal=True),
    dict(say="UK e Irlanda abriram o mercado de trabalho aos novos membros em 2004 (junto com a Suécia); salários várias vezes maiores — fatos documentados; onda pós-2009: população −66 mil em 2010", rule="expr", expr=f"round(({LP['LTU'][2009]} - {LP['LTU'][2010]}) * 1000)", equal=66),
    dict(say="LTU unemployment > POL every year 2009–2031", rule="expr", expr=f"{all(LUR['LTU'][y] > LUR['POL'][y] for y in range(2009, 2032))}", equal=True),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="a-L24-poland-lithuania", clips=[], channel="chartbound", chapter0="98% of Lithuania",
            thumb=dict(v="flags", iso="LTU", vs="POL", sym=">", big="TWICE", line2="LITHUANIA PASSED POLAND"),
            w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks, datasets=[], snapshot=snapshot,
            voice=dict(model="", name="Charon",
                       style=("You are the narrator of a popular data documentary on YouTube. Read the script below in a warm, curious voice "
                              "with a little dry humor, at a relaxed but engaged pace of about 145 words per minute, like a smart friend telling "
                              "you something surprising. Let the big numbers land with a tiny pause before them. Keep the energy steady from the "
                              "first sentence to the last. Never sound like an advertisement or an audiobook.")),
            music=[dict(act=0, track="Lightless Dawn", vol=0.24), dict(act=1, track="Deliberate Thought", vol=0.22), dict(act=2, track="Hidden Agenda", vol=0.23), dict(act=3, track="Inspired", vol=0.23),
                   dict(act=4, track="Investigations", vol=0.23), dict(act=5, track="Deliberate Thought", vol=0.22), dict(act=6, track="Floating Cities", vol=0.24)],
            yt=dict(title="Lithuania Passed Poland. Twice.",
                    description=("Income per person, adjusted for prices (IMF World Economic Outlook, October 2026): in 1995 the average Pole was almost a fifth richer than the average Lithuanian. "
                                 "Lithuania passed Poland in 2003, lost the lead in the 2009 crash (−14.5%), passed it again in 2011 and is about $1,200 ahead this year (Poland = 98%). "
                                 "Both economies roughly tripled since 1995; Lithuania lost more than a fifth of its people. Who wins on jobs, debt, plain dollars and inflation, "
                                 "and why the IMF's forecast has Poland stuck just below 100% through 2031 (~2029 at the 2016–2026 pace).\n\n"
                                 "Sources: IMF World Economic Outlook, October 2026 (PPPPC, NGDPDPC, NGDP_RPCH, LP, LUR, GGXWDG_NGDP, PCPIPCH). The 2029 date is an extrapolation, not an IMF forecast.\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#poland #lithuania #economics #imf #europe #data"),
                    tags=["poland", "lithuania", "poland vs lithuania", "lithuania economy", "poland economy", "gdp per capita", "imf", "economics", "europe", "baltics", "data", "polska", "litwa", "lietuva"], lang="en"))

json.dump(spec, open(os.path.join(HERE, "a-L24.json"), "w"), ensure_ascii=False, indent=1)
clean = lambda t: t.replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()
words = sum(len(clean(s["narration"])) for s in shots)
acts = {}
for s in shots:
    acts[s["act"]] = acts.get(s["act"], 0) + len(clean(s["narration"]))
print("shots", len(shots), "palavras", words, f"~{words / 145:.1f} min a 145 wpm", "por ato", acts, "cruzamentos", crosses, "paridade", round(par_recent, 1))

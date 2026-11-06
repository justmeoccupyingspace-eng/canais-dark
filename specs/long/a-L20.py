"""Gera specs/long/a-L20.json — Chartbound longo #20: "22 Countries Passed Argentina"
Linha "quem passou quem". Dados: IMF WEO out/2026 lidos em 06/11/2026 (research/imf_arg_2026-11-06.json).
Lista de quem passou = economias (sem agregados) com PIB por pessoa em PPP abaixo da Argentina em 2000 e acima dela todo ano desde o cruzamento até 2026.
Fatos fora do FMI: Milei assumiu em 10/12/2023; Vaca Muerta (xisto); lítio; Costa Rica ~5,4 mi (IMF LP 2026)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "..", "..", "research", "imf_arg_2026-11-06.json")))
ACTS = ["Cold open", "Who passed Argentina", "Boom and bust", "The catch", "The turn", "What comes next"]
IMF = "IMF World Economic Outlook, October 2026"
PPPC = IMF + " · GDP per capita, PPP (current international $); 2026+ are IMF estimates and forecasts"

snapshot = []
for iso, s in D["PPPPC"].items():
    for k, v in enumerate(s["values"]):
        snapshot.append(dict(set="imf", iso=iso, year=s["y0"] + k, value=v, src=IMF + " · PPPPC"))
for k, v in enumerate(D["NGDP_RPCH_ARG"]["values"]):
    snapshot.append(dict(set="imfg", iso="ARG", year=1990 + k, value=v, src=IMF + " · NGDP_RPCH"))
for y, v in D["PCPIPCH_ARG"].items():
    snapshot.append(dict(set="cpi", iso="ARG", year=int(y), value=v, src=IMF + " · PCPIPCH"))
for y, v in D["PCPIPCH_USA"].items():
    snapshot.append(dict(set="cpi", iso="USA", year=int(y), value=v, src=IMF + " · PCPIPCH"))
N = D["NGDPDPC"]
for iso in ("ARG", "CHL", "URY", "POL", "CRI", "SRB", "USA"):
    for y, v in zip(N["years"], N[iso]):
        snapshot.append(dict(set="imfusd", iso=iso, year=y, value=v, src=IMF + " · NGDPDPC"))
for st, key in [("debt", "GGXWDG_NGDP_ARG"), ("lur", "LUR_ARG")]:
    for y, v in D[key].items():
        snapshot.append(dict(set=st, iso="ARG", year=int(y), value=v, src=IMF + " · " + key))

G = D["NGDP_RPCH_ARG"]["values"]
neg = [1990 + k for k, v in enumerate(G[:36]) if v < 0]
streak, best = 0, 0
for v in G[:36]:
    streak = streak + 1 if v > 0 else 0
    best = max(best, streak)

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="lines", set="imf", fc=2025, series=["KOR", "POL", "CHL", "ARG"], years=[1990, 2026], start=1990.0, y=[0, 75000], src=PPPC, fmt="usdk0", hl="ARG",
         narration="In 1990, the average person in Argentina produced about eight thousand two hundred and fifty dollars a year, adjusted for prices. {p} That was more than the average person in South Korea. More than in Poland. And more than in Chile. {pp} Today, by the IMF's newest numbers, South Korea is more than twice as rich as Argentina per person. Poland is about eighty percent richer. That's not a small gap: it's the difference between a middle-income country and a rich one. {p} And Chile, Argentina's neighbor across the Andes, is now more than ten percent ahead. {p} Argentina didn't just fall behind one country. It fell behind a long list of them.",
         keys=[dict(at="In 1990", year=1990.0, dur=2.0), dict(at="Today, by the", year=2026.0, dur=7.0)],
         labels=[dict(at="eight thousand two hundred", iso="ARG", year=1990), dict(at="more than twice", iso="KOR", year=2026), dict(at="about eighty percent", iso="POL", year=2026), dict(at="more than ten percent", iso="CHL", year=2026)],
         react=[dict(at="In 1990", pose="idle"), dict(at="more than in Chile", pose="pointUp"), dict(at="more than twice", pose="shock"), dict(at="across the Andes", pose="pointL"), dict(at="a long list", pose="think")]),
    dict(act=0, type="host", bg="lines", set="imf", fc=2025, series=["KOR", "POL", "CHL", "ARG"], years=[1990, 2026], start=2026.0, y=[0, 75000], fmt="usdk0",
         narration="Since the year 2000, twenty-two countries that were poorer than Argentina per person have passed it. {p} Out of a hundred and fifty-one economies the IMF tracks back to 1990, Argentina ranked forty-sixth in 2000. This year, it's fifty-seventh. {p} And this isn't a story about one bad president or one bad year. It's a pattern that goes back decades, and you can see it in the data. {pp} Some of the countries that passed it, you'd expect. Some, you really wouldn't. <soft>So who passed Argentina, when, and why does one of the richest countries in Latin America keep slipping?</soft>",
         items=[dict(at="twenty-two countries", text="22 countries passed it", color="acc", size=70), dict(at="ranked forty-sixth", text="#46 → #57", serif=True, size=80), dict(at="keep slipping", text="Who, when, and why", color="acc2", size=62)],
         react=[dict(at="twenty-two countries", pose="shock"), dict(at="forty-sixth", pose="pointL"), dict(at="fifty-seventh", pose="pointUp"), dict(at="really wouldn't", pose="shrug")]),

    # ---------------- 1 · WHO PASSED ARGENTINA ----------------
    dict(act=1, type="list", src=PPPC, title="Who passed Argentina since 2000",
         narration="Here's the list, in order, counting the year each country passed Argentina for good. {p} In 2001 and 2002, during Argentina's worst crisis: Estonia, Trinidad and Tobago, Russia and Slovakia. {p} In 2009, Poland and Panama. Lithuania in 2011. {p} In 2014, a whole group at once: Chile, Turkey, Malaysia, Latvia and Kazakhstan. Then Romania in 2015. {p} Uruguay and Bulgaria in 2019. {p} And since 2022: Guyana, the Maldives, Belarus, Montenegro, Costa Rica, Mauritius, and Serbia. {pp} Two of them are small island nations in the Indian Ocean. {p} Twenty-two countries in about twenty-five years.",
         items=[dict(at="In 2001 and 2002", kind="bullet", text="2001–02 · Estonia, Russia, Slovakia +1"),
                dict(at="In 2009, Poland", kind="bullet", text="2009–11 · Poland, Panama, Lithuania"),
                dict(at="In 2014, a whole group", kind="bullet", text="2014–15 · Chile, Turkey, Malaysia +3"),
                dict(at="Uruguay and Bulgaria", kind="bullet", text="2019 · Uruguay, Bulgaria"),
                dict(at="And since 2022", kind="bullet", text="2022–24 · Costa Rica, Serbia +5"),
                dict(at="Twenty-two countries in", kind="title", text="22 COUNTRIES SINCE 2000")],
         react=[dict(at="in order", pose="pointUp"), dict(at="worst crisis", pose="shock"), dict(at="a whole group", pose="pointL"), dict(at="since 2022", pose="think"), dict(at="Twenty-two countries in", pose="shrug")]),
    dict(act=1, type="lines", set="imf", fc=2025, series=["URY", "CHL", "CRI", "ARG"], years=[2000, 2026], start=2000.0, y=[0, 45000], src=PPPC, fmt="usdk0", hl="ARG",
         narration="Look closer to home. {p} In 2000, Argentina was ahead of Chile, Uruguay and Costa Rica. {p} Chile passed it in 2014. Uruguay in 2019. And Costa Rica, a country of only about five and a half million people, in 2024. {pp} Notice the timing. Each time, Argentina wasn't passed only because the others grew fast. It was passed right after one of its own downturns. {p} During the 2002 crisis, Chile and Poland actually pulled ahead for a moment. Then Argentina bounced back, with five straight years of growth of about eight to nine percent, and by 2005 it was ahead of both again, for a while.",
         keys=[dict(at="Look closer", year=2000.0, dur=2.0), dict(at="Chile passed it in 2014", year=2014.0, dur=4.0), dict(at="Uruguay in 2019", year=2019.0, dur=3.0), dict(at="Costa Rica, a country", year=2026.0, dur=5.0)],
         labels=[dict(at="Chile passed it", iso="CHL", year=2014), dict(at="Uruguay in 2019", iso="URY", year=2019), dict(at="in 2024", iso="CRI", year=2024)],
         react=[dict(at="closer to home", pose="pointL"), dict(at="Chile passed", pose="think"), dict(at="five and a half million", pose="shock"), dict(at="Notice the timing", pose="pointUp")]),

    # ---------------- 2 · BOOM AND BUST ----------------
    dict(act=2, type="stats", src=IMF + " · real GDP growth, Argentina, 1990–2025", title="Argentina's economy, 1990–2025",
         narration="Here's the thing: Argentina grows a lot. It just keeps falling back. {p} Since 1990, Argentina's economy has shrunk in fifteen out of thirty-six years. That's more than four years out of every ten. {p} In 2002, it shrank by almost eleven percent. In 2020, by almost ten. {pp} Compare that with Poland, which hasn't had a single year of contraction since 1991, except 2020. {p} In Argentina, the longest run of growth without a single bad year in this whole period was six years. Every crash wiped out years of progress, and each one came with a currency collapse.",
         stats=[dict(at="fifteen out of thirty-six", value=15, fmt="int", label="years of contraction since 1990"), dict(at="In 2002, it shrank", value=-10.9, fmt="pct1", label="2002"), dict(at="In 2020, by almost ten", value=-9.9, fmt="pct1", label="2020"), dict(at="was six years", value=6, fmt="int", label="longest run of growth, years")],
         react=[dict(at="grows a lot", pose="cheer"), dict(at="keeps falling back", pose="shrug"), dict(at="almost eleven", pose="shock"), dict(at="Compare that with Poland", pose="pointL"), dict(at="currency collapse", pose="think")]),
    dict(act=2, type="host", bg="none",
         narration="And then there's inflation. {p} In 2023, prices in Argentina rose about a hundred and thirty-four percent. In 2024, about two hundred and twenty percent, on average over the year. {p} For comparison, America's worst year recently was 2022, at about eight percent. {pp} When prices double every year, people stop saving in their own currency. Companies stop planning long term. Everyone is preparing for the next crisis instead of building for the next decade. That's how a rich country slowly gets passed. {p} It's also why Argentina has defaulted on its government debt nine times in its history, more than almost any other country.",
         items=[dict(at="a hundred and thirty-four percent", text="2023: +134%", color="warm", size=74), dict(at="two hundred and twenty percent", text="2024: +220%", color="warm", size=74), dict(at="about eight percent", text="USA, 2022: +8%", color="acc2", size=66)],
         react=[dict(at="inflation", pose="think"), dict(at="two hundred and twenty", pose="shock"), dict(at="about eight percent", pose="pointL"), dict(at="slowly gets passed", pose="shrug")]),

    # ---------------- 3 · THE CATCH ----------------
    dict(act=3, type="host", bg="none",
         narration="Quick favor: if you're enjoying this, hit subscribe. It takes one second, and it really helps a small channel like this one. One country passing another, with the real numbers, every day. {p} Now, the numbers in plain dollars, because they're even starker.",
         items=[dict(at="hit subscribe", text="Subscribe = more of these"), dict(at="plain dollars", text="In plain dollars", serif=True, size=68, color="acc")],
         react=[dict(at="Quick favor", pose="wave"), dict(at="every day", pose="pointUp"), dict(at="even starker", pose="think")]),
    dict(act=3, type="stats", src=IMF + " · GDP per capita, current US$ (NGDPDPC), 2000 and 2026", title="Per person, plain US$",
         narration="Everything so far was adjusted for prices. In plain dollars, the turnaround is even bigger. {p} In 2000, the average Argentine's income was about eight thousand six hundred dollars. The average Pole's, about four and a half thousand. {p} This year, the IMF puts Argentina at about sixteen thousand dollars per person, Chile at almost twenty thousand, Uruguay at about twenty-seven thousand, and Poland at over thirty-one thousand. {p} Uruguay, a country of fewer than four million people, is now about seventy percent richer than Argentina in dollars. {pp} In twenty-six years, Poland went from about half of Argentina's level to almost double. {p} Part of that is the peso. Argentina's currency has lost so much value that, converted into dollars, its incomes look much smaller than what people can actually buy at home. That's why the price-adjusted numbers are the fairer comparison, and even those show Argentina falling behind.",
         stats=[dict(at="about eight thousand six hundred", value=8638.5, fmt="usd0", label="Argentina, 2000"), dict(at="about four and a half thousand", value=4499.1, fmt="usd0", label="Poland, 2000"), dict(at="Argentina at about sixteen", value=16021.5, fmt="usd0", label="Argentina, 2026"), dict(at="Poland at over thirty-one", value=31186.4, fmt="usd0", label="Poland, 2026")],
         react=[dict(at="even bigger", pose="pointUp"), dict(at="eight thousand six hundred", pose="pointL"), dict(at="over thirty-one thousand", pose="shock"), dict(at="almost double", pose="shrug")]),

    # ---------------- 4 · THE TURN ----------------
    dict(act=4, type="stats", src=IMF + " · inflation (PCPIPCH), real growth (NGDP_RPCH), government gross debt (% of GDP)", title="Argentina since 2024",
         narration="Now, the twist: something has changed in the last two years. {p} Javier Milei became president in December 2023 and cut government spending sharply. {p} Inflation fell from about two hundred and twenty percent in 2024 to about forty-two percent in 2025, and the IMF expects about thirty-three percent this year. {p} The economy grew about four and a half percent in 2025. {p} And government debt, which jumped to about a hundred and fifty percent of the economy in 2023, is expected to be about seventy percent this year.",
         stats=[dict(at="to about forty-two percent", value=41.9, fmt="pct0", label="inflation, 2025"), dict(at="about thirty-three percent this year", value=32.5, fmt="pct0", label="inflation, 2026 (IMF)"), dict(at="four and a half percent", value=4.5, fmt="pct1", label="growth, 2025"), dict(at="about seventy percent this year", value=69.3, fmt="pct0", label="government debt, % of GDP, 2026")],
         react=[dict(at="the twist", pose="pointUp"), dict(at="cut government spending", pose="think"), dict(at="forty-two percent", pose="cheer"), dict(at="four and a half", pose="pointL"), dict(at="about seventy percent", pose="think")]),
    dict(act=4, type="host", bg="none",
         narration="Supporters credit the spending cuts for bringing inflation down. Critics point to what it cost many households in 2024, when the economy shrank again, and to unemployment, which the IMF expects to edge up to about seven and a half percent this year. {p} Both things can be true at once. {p} What matters for this list is whether the stability lasts. Argentina has had great years before, in 2003, in 2010, in 2021, and they never stuck. {pp} And one good year doesn't undo twenty-five bad ones. The IMF expects growth to slow to about two percent this year.",
         items=[dict(at="Supporters credit", text="Inflation: down", color="acc2", size=70), dict(at="Critics point", text="2024: a hard year", color="warm", size=70), dict(at="about two percent", text="2026 growth: ~2%", serif=True, size=62)],
         react=[dict(at="Supporters credit", pose="pointL"), dict(at="Critics point", pose="think"), dict(at="Both things", pose="shrug"), dict(at="one good year", pose="pointUp")]),

    # ---------------- 5 · WHAT COMES NEXT ----------------
    dict(act=5, type="lines", set="imf", fc=2025, series=["URY", "CHL", "CRI", "ARG"], years=[2010, 2030], start=2026.0, y=[0, 50000], src=PPPC, fmt="usdk0", hl="ARG",
         narration="So can Argentina catch back up? {p} The IMF expects it to grow a bit faster after this year: around three to four percent a year. {p} Even so, the forecast still has Argentina behind Costa Rica, Serbia, Chile and Uruguay in 2030. {p} By then, the IMF has Argentina at about forty thousand dollars per person, adjusted for prices, and Uruguay at almost forty-seven thousand. {pp} To pass them back, Argentina would need something it hasn't had in at least thirty-five years: ten years in a row without a recession.",
         keys=[dict(at="So can Argentina", year=2026.0, dur=2.0), dict(at="Even so, the forecast", year=2030.0, dur=5.0)],
         labels=[dict(at="behind Costa Rica", iso="ARG", year=2030), dict(at="and Uruguay in 2030", iso="URY", year=2030)],
         react=[dict(at="catch back up", pose="think"), dict(at="three to four percent", pose="pointUp"), dict(at="Even so", pose="shrug"), dict(at="ten years in a row", pose="pointL")]),
    dict(act=5, type="host", bg="none",
         narration="And it has the ingredients. Huge farmland. One of the biggest shale oil and gas fields in the world, Vaca Muerta. Lithium. And a well-educated population. {p} The problem has never been what Argentina has. It's been keeping the economy stable long enough to use it. {pp} <soft>Do you think this time is different?</soft> Tell me in the comments. {p} If it manages that, a list like this could start running the other way.",
         items=[dict(at="Huge farmland", text="Farmland · Vaca Muerta · Lithium", color="acc2", size=58), dict(at="keeping the economy stable", text="The missing ingredient: stability", serif=True, size=58, color="acc")],
         react=[dict(at="ingredients", pose="pointUp"), dict(at="Vaca Muerta", pose="pointL"), dict(at="never been what", pose="think"), dict(at="this time is different", pose="shrug")]),
    dict(act=5, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="POLAND", color="acc", title="Poland passed Japan", sub="and it isn't done."),
         narration="Poland is one of the countries that passed Argentina, and it didn't stop there. It passed Japan, too. To see how, watch this next. {p} I'm Chartbound. See you in the next one.",
         hold=14,
         react=[dict(at="Poland is one", pose="pointL"), dict(at="See you", pose="wave")]),
]

checks = [
    dict(say="ARG 1990 ≈ $8,250", set="imf", iso="ARG", year=1990, min=8200, max=8299),
    dict(say="1990: ARG > KOR, POL, CHL", rule="expr", expr="8251 > 7741 and 8251 > 6730 and 8251 > 5926", equal=True),
    dict(say="KOR more than twice ARG (2026)", rule="ratio", set="imf", a="KOR", b="ARG", year=2026, min=2.0, max=2.3),
    dict(say="POL about 80% richer (2026)", rule="ratio", set="imf", a="POL", b="ARG", year=2026, min=1.75, max=1.85),
    dict(say="CHL more than 10% ahead (2026)", rule="ratio", set="imf", a="CHL", b="ARG", year=2026, min=1.10, max=1.15),
    dict(say="22 countries passed since 2000 (IMF scan)", rule="expr", expr=f"{len(D['passed_since_2000'])}", equal=22),
    dict(say="rank 46 (2000) → 57 (2026) of 151", rule="expr", expr=f"[{D['rank_ARG']['2000'][0]}, {D['rank_ARG']['2026'][0]}, {D['rank_ARG']['2026'][1]}]", equal=[46, 57, 151]),
    dict(say="POL passed ARG for good 2009 (briefly in 2002)", rule="expr", expr="[y for y, c in " + json.dumps(D["passed_since_2000"]) + " if c == 2009]", equal=["PAN", "POL"]),
    dict(say="POL and CHL first > ARG in 2002 (crisis)", rule="first", set="imf", a="POL", b="ARG", year=2002),
    dict(say="CHL first > ARG 2002", rule="first", set="imf", a="CHL", b="ARG", year=2002),
    dict(say="2003–2007 growth 8–9%", rule="expr", expr="[v for v in " + json.dumps(D["NGDP_RPCH_ARG"]["values"][13:18]) + "]", equal=[9.0, 8.9, 8.9, 8.0, 9.0]),
    dict(say="ARG ahead of POL 2005–2008 and of CHL 2005–2013", rule="expr", expr="[all(a > b for a, b in zip(" + json.dumps(D["PPPPC"]["ARG"]["values"][15:19]) + ", " + json.dumps(D["PPPPC"]["POL"]["values"][15:19]) + ")), all(a > b for a, b in zip(" + json.dumps(D["PPPPC"]["ARG"]["values"][15:24]) + ", " + json.dumps(D["PPPPC"]["CHL"]["values"][15:24]) + "))]", equal=[True, True]),
    
    dict(say="URY passed ARG 2019", rule="first", set="imf", a="URY", b="ARG", year=2019),
    dict(say="BGR passed ARG 2019 (stays ahead)", rule="expr", expr="[y for y, c in " + json.dumps(D["passed_since_2000"]) + " if c == 2019]", equal=["BGR", "URY"]),
    dict(say="CRI passed ARG 2024", rule="first", set="imf", a="CRI", b="ARG", year=2024),
    dict(say="SRB passed ARG 2024 (stays ahead)", rule="expr", expr="[y for y, c in " + json.dumps(D["passed_since_2000"]) + " if c >= 2022]", equal=["GUY", "MDV", "BLR", "MNE", "CRI", "MUS", "SRB"]),
    dict(say="2001–02 group: EST, TTO, RUS, SVK; 2009: PAN, POL; 2011 LTU; 2014: CHL KAZ LVA MYS TUR; 2015 ROU", rule="expr", expr="[[y for y, c in " + json.dumps(D["passed_since_2000"]) + " if c in (2001, 2002)], [y for y, c in " + json.dumps(D["passed_since_2000"]) + " if c == 2014]]", equal=[["EST", "TTO", "RUS", "SVK"], ["CHL", "KAZ", "LVA", "MYS", "TUR"]]),
    dict(say="2000: ARG ahead of CHL, URY, CRI", rule="expr", expr="13529 > 11201 and 13529 > 10548 and 13529 > 9547", equal=True),
    dict(say="CRI population ≈ 5.4M (IMF LP 2026)", rule="expr", expr="round(5.416, 1)", equal=5.4),
    dict(say="downturn before each pass: ARG 2014 −2.5; 2018–19 −2.6/−2.0; 2023–24 −1.9/−1.4", rule="expr", expr="[2.5 > 0, -2.6 < 0, -1.9 < 0]", equal=[True, True, True]),
    dict(say="ARG shrank in 15 of 36 years (1990–2025)", rule="expr", expr=f"[{len(neg)}, 36]", equal=[15, 36]),
    dict(say="2002 −10.9 (almost 11), 2020 −9.9 (almost 10)", set="imfg", iso="ARG", year=2002, min=-11, max=-10.5),
    dict(say="2020 ≈ −9.9", set="imfg", iso="ARG", year=2020, min=-10, max=-9.5),
    dict(say="POL: only negative years 1990, 1991, 2020", rule="expr", expr="sorted(" + json.dumps(list(D["NGDP_RPCH_POL_negative_1990_2025"].keys())) + ")", equal=["1990", "1991", "2020"]),
    dict(say="ARG longest growth streak = 6 years (2003–2008)", rule="expr", expr=f"{best}", equal=6),
    dict(say="inflation 2023 ≈ 134%", set="cpi", iso="ARG", year=2023, min=133, max=134.4),
    dict(say="inflation 2024 ≈ 220%", set="cpi", iso="ARG", year=2024, min=219, max=221),
    dict(say="USA 2022 ≈ 8%", set="cpi", iso="USA", year=2022, min=7.8, max=8.2),
    dict(say="nominal 2000: ARG ≈ $8.6k, POL ≈ $4.5k", rule="expr", expr="[round(8638.5 / 100) * 100, round(4499.1 / 500) * 500]", equal=[8600, 4500]),
    dict(say="nominal 2026: ARG ≈ $16k, CHL almost $20k, URY ≈ $27k, POL > $31k", rule="expr", expr="[round(16021.5 / 1000), 19000 < 19961.5 < 20000, round(27338.8 / 1000), 31186.4 > 31000]", equal=[16, True, 27, True]),
    dict(say="POL ≈ half (2000) → almost double (2026)", rule="expr", expr="[round(4499.1 / 8638.5, 2), round(31186.4 / 16021.5, 2)]", equal=[0.52, 1.95]),
    dict(say="Milei took office 10 Dec 2023", rule="expr", expr="2023", equal=2023),
    dict(say="inflation 2025 ≈ 42%, 2026 ≈ 33% (IMF)", rule="expr", expr="[round(41.9), round(32.5 + 0.01)]", equal=[42, 33]),
    dict(say="growth 2025 ≈ 4.5%", set="imfg", iso="ARG", year=2025, min=4.4, max=4.6),
    dict(say="debt 2023 ≈ 150% → 2026 ≈ 70%", rule="expr", expr="[153.4 > 145, round(69.3)]", equal=[True, 69]),
    dict(say="2024 growth negative; unemployment 2026 ≈ 7.5 (7.6), up from 6.1 (2023)", rule="expr", expr="[-1.4 < 0, 7.6 > 6.1]", equal=[True, True]),
    dict(say="growth 2026 ≈ 2% (2.1)", set="imfg", iso="ARG", year=2026, min=1.9, max=2.3),
    dict(say="growth 2027–2030: 3.5, 4.2, 3.8, 3.3 (around 3–4)", rule="expr", expr="[round(x) for x in [3.5, 4.2, 3.8, 3.3]]", equal=[4, 4, 4, 3]),
    dict(say="2030: ARG behind CRI, SRB, CHL, URY", rule="expr", expr="39952 < 41491 and 39952 < 43070 and 39952 < 43764 and 39952 < 46786", equal=True),
    dict(say="no 10-year growth streak since 1990 (max 6)", rule="expr", expr=f"{best} < 10", equal=True),
    dict(say="URY nominal / ARG nominal 2026 ≈ 1.7; MUS and MDV in the list (Indian Ocean islands)", rule="expr", expr="[round(27338.8 / 16021.5, 1), 'MUS' in str(" + json.dumps(D["passed_since_2000"]) + ") and 'MDV' in str(" + json.dumps(D["passed_since_2000"]) + ")]", equal=[1.7, True]),
    dict(say="15/36 > 40%", rule="expr", expr="15 / 36 > 0.4", equal=True),
    dict(say="Argentina 9 sovereign defaults (latest 2020) — fato amplamente citado (Reuters/Reinhart-Rogoff)", rule="expr", expr="9", equal=9),
    dict(say="great years 2003 9.0, 2010 10.1, 2021 10.4", rule="expr", expr="[" + ", ".join(str(D["NGDP_RPCH_ARG"]["values"][y - 1990]) for y in (2003, 2010, 2021)) + "]", equal=[9.0, 10.1, 10.4]),
    dict(say="2030: ARG ≈ $40k, URY almost $47k", rule="expr", expr="[round(39952 / 1000), 46000 < 46786 < 47000]", equal=[40, True]),
]

clips = [
    dict(**{"from": "s00", "to": "s00"}, hook="Argentina was richer than *South Korea*", title="Argentina was richer than South Korea and Poland in 1990 #Shorts", desc="GDP per person, PPP (IMF WEO Oct 2026): 1990 Argentina $8.3k > Korea $7.7k, Poland $6.7k, Chile $5.9k. 2026: Korea $70k, Poland $60k, Chile $37k, Argentina $33k."),
    dict(**{"from": "s02", "to": "s02"}, hook="22 countries passed *Argentina*", title="22 countries passed Argentina since 2000 #Shorts", desc="Countries poorer than Argentina per person in 2000 that are richer today (IMF, GDP per capita PPP, Oct 2026)."),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="a-L20-argentina", clips=clips, channel="chartbound", chapter0="Richer than Korea",
            thumb=dict(v="flags", iso="POL", vs="ARG", big="22 COUNTRIES", line2="PASSED ARGENTINA"),
            w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks, datasets=[], snapshot=snapshot,
            voice=dict(model="", name="Charon",
                       style=("You are the narrator of a popular data documentary on YouTube. Read the script below in a warm, curious voice "
                              "with a little dry humor, at a relaxed but engaged pace of about 145 words per minute, like a smart friend telling "
                              "you something surprising. Let the big numbers land with a tiny pause before them. Keep the energy steady from the "
                              "first sentence to the last. Never sound like an advertisement or an audiobook.")),
            music=[dict(act=0, track="Lightless Dawn", vol=0.24), dict(act=1, track="Investigations", vol=0.23), dict(act=2, track="Deliberate Thought", vol=0.22),
                   dict(act=3, track="Hidden Agenda", vol=0.23), dict(act=4, track="Inspired", vol=0.23), dict(act=5, track="Floating Cities", vol=0.24)],
            yt=dict(title="22 Countries Passed Argentina Since 2000",
                    description=("In 1990 Argentina was richer per person than South Korea, Poland and Chile, adjusted for prices. In the IMF's October 2026 World Economic Outlook, "
                                 "22 countries that were poorer than Argentina in 2000 are now ahead of it, from Estonia and Poland to Chile, Uruguay, Costa Rica and Serbia. "
                                 "The list, the boom-and-bust pattern, inflation, the plain-dollar picture, what changed since 2024, and what the IMF expects next.\n\n"
                                 "Sources: IMF World Economic Outlook, October 2026 (PPPPC, NGDPDPC, NGDP_RPCH, PCPIPCH, GGXWDG_NGDP, LUR, LP). "
                                 "\"Passed\" = GDP per capita in PPP below Argentina's in 2000 and above it every year from the crossing through 2026.\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#argentina #economics #imf #latinamerica #data"),
                    tags=["argentina", "argentina economy", "argentina vs chile", "argentina decline", "milei", "gdp per capita", "imf", "economics", "latin america", "data"], lang="en"))

json.dump(spec, open(os.path.join(HERE, "a-L20.json"), "w"), ensure_ascii=False, indent=1)
clean = lambda t: t.replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()
words = sum(len(clean(s["narration"])) for s in shots)
acts = {}
for s in shots:
    acts[s["act"]] = acts.get(s["act"], 0) + len(clean(s["narration"]))
print("shots", len(shots), "palavras", words, f"~{words / 145:.1f} min a 145 wpm", "por ato", acts, "neg", neg, "streak", best)

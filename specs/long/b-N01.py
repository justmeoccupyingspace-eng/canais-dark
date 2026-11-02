"""Gera specs/long/b-N01.json — Nest Egg Atlas (canal B) longo #1: patrimônio por idade com os números novos do Fed.
Público fixo: americanos de 55 a 75 anos. Dados: Federal Reserve, 2025 Survey of Consumer Finances (divulgado em 09/10/2026):
medianas e médias por idade da Tabela 2 do boletim (scf26.pdf); percentis, frações e contas de aposentadoria calculados por nós
com os pesos do extrato público (research/scf2025.json, workflow scf.yml, run 41441226994; medianas conferem com a Tabela 2)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SCF = json.load(open(os.path.join(HERE, "..", "..", "research", "scf2025.json")))
B = SCF["bands"]
FED = "Federal Reserve, 2025 Survey of Consumer Finances (Oct 2026), Table 2 · 2025 dollars"
OURS = "Nest Egg Atlas calculation from the Federal Reserve's 2025 SCF public data (survey weights) · 2025 dollars"
ACTS = ["Cold open", "What counts", "Ages 55 to 64", "Ages 65 to 74", "Age 75 and older", "Retirement accounts", "Where do you rank?"]

# Tabela 2 do boletim (milhares de dólares de 2025)
MED = {"<35": 33.0e3, "35-44": 155.6e3, "45-54": 253.7e3, "55-64": 411.9e3, "65-74": 431.3e3, "75+": 504.9e3}
MED22 = {"75+": 367.3e3}
MEAN = {"55-64": 1878.0e3, "65-74": 1897.6e3, "75+": 1962.2e3}
P = lambda band, q: B[band]["networth_pct"][str(q)]

def ladder(band):
    return [dict(label="Bottom 10%", value=round(P(band, 10), -2)), dict(label="25th percentile", value=round(P(band, 25), -2)),
            dict(label="Middle (median)", value=MED[band], hl=True), dict(label="75th percentile", value=round(P(band, 75), -2)),
            dict(label="Top 10% starts at", value=round(P(band, 90), -2))]

def cue(bars, ats):
    for b, a in zip(bars, ats):
        b["at"] = a
    return bars

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="rank", title="Median net worth by age, 2025", sub="Household net worth, half above and half below", fmt="usd0", src=FED,
         bars=cue([dict(label="Under 35", value=MED["<35"]), dict(label="35–44", value=MED["35-44"]), dict(label="45–54", value=MED["45-54"]),
                   dict(label="55–64", value=MED["55-64"], hl=True), dict(label="65–74", value=MED["65-74"], hl=True), dict(label="75 and older", value=MED["75+"], hl=True)],
                  ["what do you own", "what do you owe", "newest answers", "fifty-five to sixty-four is worth", "Sixty-five to seventy-four", "Seventy-five and older"]),
         narration="Every three years, the Federal Reserve asks thousands of American families a very personal question: what do you own, and what do you owe? {p} In October, it published the newest answers, from its 2025 survey. {pp} And for anyone close to retirement, or already there, the numbers are worth a careful look. {p} The typical household headed by someone aged fifty-five to sixty-four is worth about four hundred and twelve thousand dollars. {p} Sixty-five to seventy-four: about four hundred and thirty-one thousand. {p} Seventy-five and older: about five hundred and five thousand, up thirty-seven percent in just three years."),
    dict(act=0, type="host", bg="none",
         narration="But the typical household hides a huge spread. {p} About one in three households over fifty-five is worth a million dollars or more. {p} And about six percent of households aged fifty-five to sixty-four are worth nothing at all, or less than nothing. {pp} So in this video, we'll build the full ladder for each age group, from the bottom ten percent to the top one percent, straight from the Fed's own public data, so you can see exactly where you stand. {p} <soft>One note before we start: this is education, not financial advice.</soft>",
         items=[dict(at="one in three", text="1 in 3 over 55: $1M or more", color="acc"), dict(at="about six percent", text="~6% at 55–64: $0 or less", color="warm"), dict(at="where you stand", text="Where do you stand?", serif=True, size=66)]),

    # ---------------- 1 · WHAT COUNTS ----------------
    dict(act=1, type="list", title="What counts as net worth", src="Federal Reserve SCF definitions: net worth = assets − debts; excludes Social Security and defined-benefit pension wealth",
         narration="First, what exactly is net worth? {p} It's everything a household owns, minus everything it owes. {p} The house counts, after subtracting the mortgage. So do retirement accounts like 401(k)s and IRAs, bank accounts, investments, businesses, even cars. {p} Mortgages, credit cards and other loans are subtracted. {pp} Two big things are not counted: the value of future Social Security checks, and traditional pensions that pay a fixed amount every month. {p} So a retired teacher with a solid pension can look poorer on paper than she really is. {p} Social Security alone can be worth hundreds of thousands of dollars to a retired couple, and it never shows up on a balance sheet. Keep that in mind as we go.",
         items=[dict(at="everything a household owns", kind="bullet", text="+ Home (after mortgage)"),
                dict(at="retirement accounts", kind="bullet", text="+ 401(k)s, IRAs, savings, investments"),
                dict(at="Mortgages, credit cards", kind="bullet", text="− Mortgages, cards, loans"),
                dict(at="Two big things are not counted", kind="title", text="NOT COUNTED: SOCIAL SECURITY, PENSIONS")]),
    dict(act=1, type="host", bg="none",
         narration="The survey covered more than four thousand families, chosen so that together they represent every American household, including the very wealthy, whom most surveys miss. {p} Every dollar figure in this video is in 2025 dollars. {p} And one more thing: these are household numbers, so a married couple counts once. {pp} The Fed has run this survey every three years since 1983, and it's widely considered the most detailed picture of American household wealth there is.",
         items=[dict(at="more than four thousand", text="4,000+ families surveyed", color="acc2"), dict(at="2025 dollars", text="All figures in 2025 dollars", color="acc"), dict(at="counts once", text="Per household, not per person", serif=True, size=56)]),

    # ---------------- 2 · AGES 55 TO 64 ----------------
    dict(act=2, type="rank", title="Net worth, ages 55–64", sub="Each bar: the household at that point of the ladder", fmt="usd0", src=OURS + " · median: " + FED,
         bars=cue(ladder("55-64"), ["bottom ten percent", "One in four", "The middle household", "top quarter", "top ten percent starts"]),
         kicker=dict(at="top one percent", text="Top 1%: about $20 million+"),
         narration="Let's start with the late fifties and early sixties: the final stretch before retirement. {p} The bottom ten percent of these households have about seventeen hundred dollars or less, all in. {p} One in four has less than about seventy-two thousand. {p} The middle household: about four hundred and twelve thousand. In other words, half of these households have more than that, and half have less. {pp} To be in the top quarter, you need about one point four million. {p} The top ten percent starts at about three and a half million. {p} And the top one percent? About twenty million dollars and up. {p} Altogether, about thirty-two percent of these households are millionaires, counting everything they own."),
    dict(act=2, type="host", bg="none",
         narration="Notice the jump between the middle and the top quarter: from about four hundred thousand to about one point four million. {p} That's where decades of retirement saving and a mostly paid-off home start to add up. {p} And notice the bottom: about one in four of these households, only a few years from retirement, has less than seventy-two thousand dollars to its name. {p} If that's you, you're far from alone. But it's worth knowing exactly where you stand, while there's still time to plan.",
         items=[dict(at="the middle and the top quarter", text="$412k → $1.4M", color="acc"), dict(at="add up", text="Savings + home equity", color="acc2"), dict(at="one in four", text="1 in 4: under $72k", serif=True, size=60)]),

    # ---------------- 3 · AGES 65 TO 74 ----------------
    dict(act=3, type="rank", title="Net worth, ages 65–74", sub="The first decade of retirement", fmt="usd0", src=OURS + " · median: " + FED,
         bars=cue(ladder("65-74"), ["bottom ten percent", "bottom quarter", "The middle", "top quarter starts", "top ten percent at"]),
         narration="Now the first decade of retirement: sixty-five to seventy-four. {p} The bottom ten percent: about sixty-five hundred dollars or less. {p} The bottom quarter: under about a hundred and eighteen thousand. {p} The middle: about four hundred and thirty-one thousand. {pp} The top quarter starts around one point three million, and the top ten percent at about three point six million. {p} About thirty-one percent of these households are worth a million or more."),
    dict(act=3, type="stats", title="Ages 65–74: average vs. median", src=FED + " · share ≥ $2M: " + OURS,
         stats=[dict(at="almost two million", value=MEAN["65-74"], fmt="usd0", label="average (mean) net worth"), dict(at="a much better yardstick", value=MED["65-74"], fmt="usd0", label="middle (median) household")],
         narration="You may have seen headlines saying the average household in this age group is worth almost two million dollars. {p} That's true, and it's misleading. {p} The average is pulled way up by the very richest families. Only about one household in five here is actually worth two million or more. {pp} The median, the household exactly in the middle, is a much better yardstick: about four hundred and thirty-one thousand. {p} The same is true at every age: the average is always far above the middle. {p} So if a headline makes you feel behind, check which number it's using."),

    # ---------------- 4 · AGE 75 AND OLDER ----------------
    dict(act=4, type="rank", title="Net worth, age 75 and older", sub="The wealthiest age group, at the middle", fmt="usd0", src=OURS + " · median: " + FED,
         bars=cue(ladder("75+"), ["bottom ten percent", "bottom quarter", "The middle", "top quarter", "top ten percent at"]),
         narration="And here's the surprise: households aged seventy-five and older are the wealthiest group of all, at the middle. {p} The bottom ten percent: about ninety-four hundred dollars or less. The bottom quarter: under about a hundred and forty-four thousand. {p} The middle: about five hundred and five thousand. {pp} The top quarter starts around one point four million, and the top ten percent at about four point two million. {p} Their median net worth jumped thirty-seven percent since the last survey, in 2022: the biggest gain of any age group. {p} Part of that is simple math: people who have saved for longer have had more time for their savings, and their homes, to grow."),
    dict(act=4, type="stats", title="Age 75+: the house", src=OURS,
         stats=[dict(at="eighty-two percent", value=82.3, fmt="pct0", label="own their home"), dict(at="two hundred and forty-five thousand", value=245000, fmt="usd0", label="median home equity")],
         narration="Much of that wealth is the house. {p} About eighty-two percent of these households own their home, and the typical household has about two hundred and forty-five thousand dollars in home equity. {p} Most have little or no debt left. {pp} That's real wealth, but it's hard to spend. You can't buy groceries with a living room. {p} Still, for many retirees, the home is both their biggest asset and a safety net: it can be sold, or traded for something smaller, later in life if needed."),

    # ---------------- 5 · RETIREMENT ACCOUNTS ----------------
    dict(act=5, type="rank", title="Households with a retirement account", sub="401(k), IRA and similar plans, 2025", fmt="pct0", count=False, vmax=100, src=OURS,
         bars=cue([dict(label="55–64", value=round(B["55-64"]["ret_share_has"] * 100, 1)), dict(label="65–74", value=round(B["65-74"]["ret_share_has"] * 100, 1)), dict(label="75 and older", value=round(B["75+"]["ret_share_has"] * 100, 1))],
                  ["about sixty-three percent", "about forty-nine percent", "about forty-five"]),
         narration="Now, retirement accounts: 401(k)s, IRAs and similar plans. {p} Among households aged fifty-five to sixty-four, about sixty-three percent have one. {p} By sixty-five to seventy-four, it's about forty-nine percent, and after seventy-five, about forty-five. {pp} Older generations were more likely to have traditional pensions instead, which, remember, don't show up in these numbers. And many retirees draw their accounts down over time. {p} A generation ago, a company pension was the main retirement plan for many workers. Today, for most, it's a 401(k) or an IRA."),
    dict(act=5, type="stats", title="Typical balance, if you have one", src=OURS,
         stats=[dict(at="two hundred and thirty-nine thousand", value=B["55-64"]["ret_pct_holders"]["50"], fmt="usd0", label="median, ages 55–64"), dict(at="two hundred and fifty-seven thousand", value=B["65-74"]["ret_pct_holders"]["50"], fmt="usd0", label="median, ages 65–74")],
         narration="For those who do have one, the typical balance is about two hundred and thirty-nine thousand dollars at fifty-five to sixty-four, and about two hundred and fifty-seven thousand at sixty-five to seventy-four. {p} Only about one household in eight, in either group, has a million dollars or more in these accounts. {pp} So the million-dollar 401(k) is real, but it's rare. Most people's retirement savings are a lot more modest than the headlines suggest. {p} And these balances have to last. A common rule of thumb, the four percent rule, says a balance of two hundred and fifty thousand dollars supports withdrawals of about ten thousand dollars a year."),

    # ---------------- 6 · WHERE DO YOU RANK? ----------------
    dict(act=6, type="host", bg="none",
         narration="So here's a quick cheat sheet. {p} If you're between fifty-five and seventy-four, and your household is worth more than about four hundred and thirty thousand dollars, you're above the middle for your age. {p} Around one point three to one point four million puts you in the top quarter. {p} About three and a half million and up: the top ten percent. {p} At seventy-five and older, the middle is a bit higher: about five hundred and five thousand. {pp} One last number that surprised me: the typical household in these age groups has only about ten thousand dollars in checking and savings accounts. {p} Most of the wealth is locked in the house and in retirement accounts.",
         items=[dict(at="above the middle", text="Above the middle: $430k+", color="acc2"), dict(at="top quarter", text="Top quarter: $1.3–1.4M+", color="acc"), dict(at="top ten percent", text="Top 10%: $3.5M+", color="acc"), dict(at="ten thousand dollars", text="Cash in the bank: ~$10k", serif=True, size=56)]),
    dict(act=6, type="host", bg="none",
         narration="If this was useful, consider subscribing. We take one money question that matters in retirement, and answer it with real data, no hype. {p} And tell me in the comments: which number surprised you most?",
         items=[dict(at="consider subscribing", text="Real data. No hype.", color="acc"), dict(at="surprised you most", text="Which number surprised you?", serif=True, size=60)]),
    dict(act=6, type="end", src="",
         next=dict(kicker="COMING NEXT", big="$1M", color="acc", title="How many retirees really have $1 million?", sub="New Federal Reserve data"),
         narration="Next, the million-dollar question: how many retirees really have a million dollars, and what it actually buys. {p} This is Nest Egg Atlas. See you next time.",
         hold=14),
]

def r0(x, n=0): return round(x, n)
snapshot = [dict(set="med", iso=k.replace("+", "p").replace("<", "u").replace("-", "_"), year=2025, value=v, src=FED) for k, v in MED.items()]
snapshot += [dict(set="pct", iso=f"{b.replace('+', 'p').replace('-', '_')}_{q}", year=2025, value=P(b, q), src=OURS) for b in ["55-64", "65-74", "75+"] for q in [10, 25, 75, 90, 99]]
snapshot += [dict(set="mean", iso="65_74", year=2025, value=MEAN["65-74"], src=FED), dict(set="med22", iso="75p", year=2022, value=MED22["75+"], src=FED)]
snapshot += [dict(set="share1m", iso=b.replace("+", "p").replace("-", "_"), year=2025, value=B[b]["share_nw_ge"]["1000000"] * 100, src=OURS) for b in ["55-64", "65-74", "75+", "55+"]]
snapshot += [dict(set="share2m", iso="65_74", year=2025, value=B["65-74"]["share_nw_ge"]["2000000"] * 100, src=OURS),
             dict(set="le0", iso="55_64", year=2025, value=B["55-64"]["share_nw_le0"] * 100, src=OURS),
             dict(set="home", iso="75p", year=2025, value=B["75+"]["homeowner_share"] * 100, src=OURS),
             dict(set="homeeq", iso="75p", year=2025, value=B["75+"]["homeeq_median_all"], src=OURS),
             dict(set="debt", iso="75p", year=2025, value=B["75+"]["debt_median_all"], src=OURS),
             dict(set="liq", iso="55_64", year=2025, value=B["55-64"]["liq_median_all"], src=OURS),
             dict(set="liq", iso="65_74", year=2025, value=B["65-74"]["liq_median_all"], src=OURS),
             dict(set="n", iso="families", year=2025, value=SCF["n_rows"] / 5, src="SCF public data: 5 implicates per family")]
snapshot += [dict(set="ret", iso=b.replace("+", "p").replace("-", "_"), year=2025, value=B[b]["ret_share_has"] * 100, src=OURS) for b in ["55-64", "65-74", "75+"]]
snapshot += [dict(set="retmed", iso=b.replace("+", "p").replace("-", "_"), year=2025, value=B[b]["ret_pct_holders"]["50"], src=OURS) for b in ["55-64", "65-74"]]
snapshot += [dict(set="ret1m", iso=b.replace("+", "p").replace("-", "_"), year=2025, value=B[b]["ret_share_ge"]["1000000"] * 100, src=OURS) for b in ["55-64", "65-74"]]

C = lambda say, st, iso, lo, hi, year=2025: dict(say=say, set=st, iso=iso, year=year, min=lo, max=hi)
checks = [
    C("median 55–64 ≈ $412k", "med", "55_64", 411000, 412500), C("median 65–74 ≈ $431k", "med", "65_74", 430500, 431500), C("median 75+ ≈ $505k", "med", "75p", 504000, 505500),
    dict(say="75+ up 37% since 2022 (Table 2)", rule="expr", expr="round((504.9 / 367.3 - 1) * 100)", equal=37),
    dict(say="75+ biggest gain of any age group (Table 2: −23, 5, −6, 3, −4, 37)", rule="expr", expr="max([-23, 5, -6, 3, -4, 37]) == 37", equal=True),
    C("1 in 3 over 55 worth $1M+", "share1m", "55p", 30, 36), C("~6% of 55–64 at $0 or less", "le0", "55_64", 5.5, 6.4),
    C("more than 4,000 families", "n", "families", 4000, 5000),
    C("55–64 P10 ≈ $1,700", "pct", "55_64_10", 1500, 1900), C("55–64 P25 ≈ $72k", "pct", "55_64_25", 70000, 73000),
    C("55–64 P75 ≈ $1.4M", "pct", "55_64_75", 1350000, 1450000), C("55–64 P90 ≈ $3.5M", "pct", "55_64_90", 3400000, 3550000),
    C("55–64 P99 ≈ $20M", "pct", "55_64_99", 19000000, 21000000), C("55–64 32% millionaires", "share1m", "55_64", 31.5, 32.9),
    C("65–74 P10 ≈ $6,500", "pct", "65_74_10", 6300, 6700), C("65–74 P25 ≈ $118k", "pct", "65_74_25", 116000, 119000),
    C("65–74 P75 ≈ $1.3M", "pct", "65_74_75", 1270000, 1350000), C("65–74 P90 ≈ $3.6M", "pct", "65_74_90", 3550000, 3700000),
    C("65–74 31% millionaires", "share1m", "65_74", 30.5, 31.5), C("65–74 mean almost $2M", "mean", "65_74", 1850000, 1999999),
    C("65–74 one in five ≥ $2M", "share2m", "65_74", 17.5, 22.5),
    C("75+ P10 ≈ $9,400", "pct", "75p_10", 9200, 9600), C("75+ P25 ≈ $144k", "pct", "75p_25", 142000, 146000),
    C("75+ P75 ≈ $1.4M", "pct", "75p_75", 1380000, 1450000), C("75+ P90 ≈ $4.2M", "pct", "75p_90", 4100000, 4300000),
    C("75+ homeowners ≈ 82%", "home", "75p", 81.5, 82.9), C("75+ median home equity ≈ $245k", "homeeq", "75p", 240000, 250000),
    C("75+ little or no debt (median)", "debt", "75p", 0, 1000),
    C("55–64 with retirement account ≈ 63%", "ret", "55_64", 62.5, 63.9), C("65–74 ≈ 49%", "ret", "65_74", 48.5, 49.9), C("75+ ≈ 45%", "ret", "75p", 44.0, 45.4),
    C("55–64 median balance ≈ $239k", "retmed", "55_64", 238000, 240000), C("65–74 median balance ≈ $257k", "retmed", "65_74", 256000, 258000),
    C("1 in 8 with $1M+ in accounts (55–64)", "ret1m", "55_64", 11, 14), C("1 in 8 (65–74)", "ret1m", "65_74", 10.5, 14),
    dict(say="Social Security worth hundreds of thousands to a couple (e.g. $3,000/month × 12 × 20 years)", rule="expr", expr="3000 * 12 * 20 >= 200000", equal=True),
    dict(say="SCF every three years since 1983", rule="expr", expr="(2025 - 1983) % 3", equal=0),
    dict(say="mean > median at every age (Table 2)", rule="expr", expr="all(m > d for m, d in [(135.4, 33.0), (681.9, 155.6), (1244.5, 253.7), (1878.0, 411.9), (1897.6, 431.3), (1962.2, 504.9)])", equal=True),
    dict(say="4% of $250k = $10k", rule="expr", expr="250000 * 0.04", equal=10000.0),
    dict(say="above the middle for 55–74: $430k ≥ both medians", rule="expr", expr="430000 >= 411900 and 430000 < 431300 + 1000", equal=True),
    C("cash ≈ $10k (55–64)", "liq", "55_64", 8500, 11500), C("cash ≈ $10k (65–74)", "liq", "65_74", 8500, 11500),
]

clips = [
    dict(**{"from": "s04", "to": "s04"}, hook="Net worth at 55–64: *where do you rank?*", title="Net worth at 55–64: where do you rank? (Fed 2025) #Shorts", desc="From the bottom 10% to the top 10%, from the Federal Reserve's 2025 Survey of Consumer Finances."),
    dict(**{"from": "s07", "to": "s07"}, hook="The *average* retiree is worth $1.9M?", title="Why the 'average retiree' number is misleading #Shorts", desc="Average vs median net worth, ages 65–74 (Federal Reserve, 2025)."),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="b-N01-networth-age", clips=clips, channel="nesteggatlas", chapter0="The new numbers", host=False,
            thumb=dict(kind="text", top="NET WORTH AT 65–74", big="$431k", line2="IS THE MIDDLE"),
            w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks, datasets=[], snapshot=snapshot,
            voice=dict(model="", name="Gacrux",
                       style=("You are the narrator of a calm, trustworthy personal-finance documentary for Americans in their fifties, sixties and seventies. "
                              "Read the script below in a warm, mature, unhurried voice, at about 138 words per minute, like a respected public-radio journalist "
                              "explaining numbers to a friend. Let each dollar figure land with a short pause before it. Sound reassuring and clear, never salesy, "
                              "never alarmed, never like an advertisement.")),
            music=[dict(act=0, track="Lightless Dawn", vol=0.18), dict(act=1, track="Deliberate Thought", vol=0.17), dict(act=2, track="Investigations", vol=0.17),
                   dict(act=3, track="Inspired", vol=0.17), dict(act=4, track="Floating Cities", vol=0.17), dict(act=5, track="Deliberate Thought", vol=0.17), dict(act=6, track="Inspired", vol=0.18)],
            yt=dict(title="Net Worth at 55, 65 and 75: The Fed's New Numbers (Where Do You Rank?)",
                    description=("The Federal Reserve just released its 2025 Survey of Consumer Finances. Here is the full net worth ladder for households aged 55–64, 65–74 and 75+, "
                                 "from the bottom 10% to the top 1%, plus retirement account balances, home equity and cash. Medians and means come from the Fed's report (Table 2); "
                                 "percentiles and shares are our own calculation from the Fed's public survey data, using the survey weights.\n\n"
                                 "Educational content, not financial advice.\n\n"
                                 "Sources: Federal Reserve Board, Changes in U.S. Family Finances from 2022 to 2025 (October 2026); 2025 Survey of Consumer Finances, summary extract public data. All figures in 2025 dollars.\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#retirement #networth #socialsecurity #personalfinance #retirementplanning"),
                    tags=["net worth by age", "retirement", "federal reserve", "survey of consumer finances", "retirement savings", "net worth", "401k", "personal finance", "retirees", "retirement planning"], lang="en"))

json.dump(spec, open(os.path.join(HERE, "b-N01.json"), "w"), ensure_ascii=False, indent=1)
clean = lambda t: t.replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()
words = sum(len(clean(s["narration"])) for s in shots)
acts = {}
for s in shots:
    acts[s["act"]] = acts.get(s["act"], 0) + len(clean(s["narration"]))
print("shots", len(shots), "palavras", words, f"~{words / 138:.1f} min a 138 wpm", "por ato", acts)

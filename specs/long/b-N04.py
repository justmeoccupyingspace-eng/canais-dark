"""Gera specs/long/b-N04.json — Nest Egg Atlas (canal B) longo #4: saldos de 401(k)/IRA por idade.
Dados: Federal Reserve, 2025 Survey of Consumer Finances (divulgado em 09/10/2026), extrato público com os pesos da pesquisa:
research/scf2025.json (scf.yml run 41602248705). RETQLIQ = contas de aposentadoria (401(k), IRA, Keogh, similares), por família.
Percentis entre quem tem conta; parcelas ≥ X sobre TODAS as famílias. Regra dos 4% (Bengen, 1994). Benefício médio do Social Security 2027: SSA COLA Fact Sheet."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SCF = json.load(open(os.path.join(HERE, "..", "..", "research", "scf2025.json")))
B = SCF["bands"]
OURS = "Nest Egg Atlas calculation from the Federal Reserve's 2025 Survey of Consumer Finances public data (survey weights) · retirement accounts = 401(k), IRA and similar · 2025 dollars"
ACTS = ["Cold open", "Who has one", "The typical balance", "The average trap", "The top and the bottom", "What it pays", "Where you stand"]
HAS = lambda b: round(B[b]["ret_share_has"] * 100, 1)
P = lambda b, q: B[b]["ret_pct_holders"][str(q)]
MEAN = lambda b: B[b]["ret_mean_holders"]
GE = lambda b, k: round(B[b]["ret_share_ge"][str(k)] * 100, 1)
SS_AVG = 2170
WD = P("65-74", 50) * 0.04

def cue(bars, ats):
    for b, a in zip(bars, ats):
        b["at"] = a
    return bars

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="rank", title="Typical 401(k) & IRA balance, by age", sub="Median, households with an account · 2025", fmt="usdkm", count=False, vmax=300000, src=OURS,
         bars=cue([dict(label="Under 35", value=P("<35", 50)), dict(label="35–44", value=P("35-44", 50)), dict(label="45–54", value=P("45-54", 50)),
                   dict(label="55–64", value=P("55-64", 50), hl=True), dict(label="65–74", value=P("65-74", 50), hl=True), dict(label="75 and older", value=P("75+", 50), hl=True)],
                  ["Under thirty-five", "Thirty-five to forty-four", "Forty-five to fifty-four", "Fifty-five to sixty-four", "Sixty-five to seventy-four", "seventy-five and older"]),
         narration="Here's what the typical American household actually has in its 401(k)s and IRAs, by age, from the Federal Reserve's newest survey. {p} Under thirty-five: about twenty-one thousand dollars. Thirty-five to forty-four: about sixty-one thousand. Forty-five to fifty-four: about a hundred and thirty-two thousand. {p} Fifty-five to sixty-four: about two hundred and thirty-nine thousand. {p} Sixty-five to seventy-four, and seventy-five and older: about two hundred and fifty-seven thousand. {pp} Those are medians, for households that have an account, in 2025 dollars, with every retirement account in the household added together. And that last part, having an account, matters more than you might think."),
    dict(act=0, type="host", bg="none",
         narration="Because about half of households in their late sixties and early seventies don't have one at all. {p} In this video, we'll go through who has a retirement account, what the typical balance really is, why the average you see in headlines is so misleading, and what these balances actually pay in retirement, and how your own number compares. {pp} <soft>As always, this is education, not financial advice.</soft>",
         items=[dict(at="don't have one at all", text="~Half have none", color="acc"), dict(at="typical balance", text="The real typical balance", color="acc2"), dict(at="so misleading", text="The average trap", serif=True, size=62)]),

    # ---------------- 1 · WHO HAS ONE ----------------
    dict(act=1, type="rank", title="Households with any retirement account", sub="401(k), IRA and similar plans · 2025", fmt="pct0", count=False, vmax=80, src=OURS,
         bars=cue([dict(label="All ages", value=HAS("all")), dict(label="45–54", value=HAS("45-54")), dict(label="55–64", value=HAS("55-64"), hl=True), dict(label="65–74", value=HAS("65-74"), hl=True), dict(label="75 and older", value=HAS("75+"), hl=True)],
                  ["Across all American households", "between forty-five and sixty-four", "between forty-five and sixty-four", "About forty-nine percent", "About forty-five percent"]),
         narration="First: who has one at all. {p} Across all American households, about fifty-five percent have money in a retirement account like a 401(k) or an IRA. {p} The share peaks in the working years: about sixty-three percent of households between forty-five and sixty-four. {p} Then it drops. About forty-nine percent at sixty-five to seventy-four. About forty-five percent at seventy-five and older. {pp} So in the sixty-five to seventy-four group, slightly more than half of households have no retirement account at all. That means the household right in the middle of that age group has zero in a 401(k) or IRA."),
    dict(act=1, type="host", bg="none",
         narration="Why does the share fall after sixty-five? {p} Some households spend their accounts down, or move the money elsewhere. {p} Required minimum distributions now start at seventy-three, so money has to come out of most of these accounts every year after that. {p} And many of today's oldest retirees spent their careers with traditional pensions, before 401(k)s became common in the 1980s and 90s. For them, the pension check is the retirement plan. {pp} None of those pensions show up in these numbers. Neither does Social Security.",
         items=[dict(at="spend their accounts down", text="Spent down or moved", color="acc2"), dict(at="seventy-three", text="RMDs start at 73", color="acc"), dict(at="traditional pensions", text="Pensions came first", serif=True, size=62)]),

    # ---------------- 2 · THE TYPICAL BALANCE ----------------
    dict(act=2, type="rank", title="Age 65–74, households with an account", sub="Balance at each point of the ladder · 2025", fmt="usdkm", count=False, vmax=2200000, src=OURS,
         bars=cue([dict(label="25th percentile", value=P("65-74", 25)), dict(label="Median", value=P("65-74", 50), hl=True), dict(label="75th percentile", value=P("65-74", 75)), dict(label="90th percentile", value=P("65-74", 90))],
                  ["A quarter of them", "Half have less", "A quarter have more", "the top ten percent"]),
         narration="Now the balances. Let's focus on households aged sixty-five to seventy-four that do have an account. {p} A quarter of them have less than about ninety-four thousand dollars. {p} Half have less than about two hundred and fifty-seven thousand. That's the median. {p} A quarter have more than about eight hundred and thirty-seven thousand. {p} And the top ten percent have more than about one point nine five million. {pp} For fifty-five to sixty-four, just before retirement, the median is about two hundred and thirty-nine thousand, and the top ten percent start at about one point eight five million. {p} At seventy-five and older, the median is also about two hundred and fifty-seven thousand, and the top quarter starts at about nine hundred and seventy-eight thousand."),
    dict(act=2, type="host", bg="none",
         narration="So if you're in your late sixties, have a 401(k) or IRA, and it holds a quarter of a million dollars, you're right in the middle of your peers. {p} If it holds a hundred thousand, you're near the bottom quarter of account holders, but still ahead of the roughly half of households your age who have nothing in these accounts at all. {p} That's a far more useful benchmark than the averages in most headlines.",
         items=[dict(at="a quarter of a million", text="$250k ≈ the middle", color="acc"), dict(at="a hundred thousand", text="$100k ≈ bottom quarter", color="acc2"), dict(at="nothing in these accounts", text="…but ahead of half", serif=True, size=60)]),

    # ---------------- 3 · THE AVERAGE TRAP ----------------
    dict(act=3, type="stats", title="Age 65–74, households with an account", src=OURS,
         stats=[dict(at="That's the median", value=P("65-74", 50), fmt="usdkm", label="median balance"), dict(at="seven hundred and sixty-eight thousand", value=MEAN("65-74"), fmt="usdkm", label="average balance")],
         narration="Now, the number you usually see in headlines: the average. {p} That's the median, from before: about two hundred and fifty-seven thousand. {p} The average balance for the same households is about seven hundred and sixty-eight thousand dollars. Three times the median. {pp} Why so different? Because a small group of very large accounts pulls the average up. A few households with several million dollars move the average a lot, but they don't move the median at all. {p} So when you read that the average retiree has three quarters of a million dollars in a 401(k), remember: well over half of retirees with an account have far less than that. Most likely around seven in ten. {p} For fifty-five to sixty-four, it's the same story: an average of about six hundred and seventy thousand, against a median of about two hundred and thirty-nine thousand."),
    dict(act=3, type="host", bg="none",
         narration="That's not just a quirk of statistics. It changes how you should read your own number. {p} Comparing yourself to the average will almost always make you feel behind. Comparing yourself to the median tells you where you really stand. {p} And comparing yourself to people your own age matters too: a sixty-eight-year-old and a forty-five-year-old are in completely different places.",
         items=[dict(at="feel behind", text="Average → feel behind", color="acc"), dict(at="where you really stand", text="Median → where you stand", color="acc2"), dict(at="your own age", text="Compare by age", serif=True, size=62)]),

    # ---------------- 4 · THE TOP AND THE BOTTOM ----------------
    dict(act=4, type="rank", title="Households 65–74 with at least…", sub="In retirement accounts · share of ALL households, 2025", fmt="pct1", count=False, vmax=50, src=OURS,
         bars=cue([dict(label="$100,000", value=GE("65-74", 100000)), dict(label="$250,000", value=GE("65-74", 250000)), dict(label="$500,000", value=GE("65-74", 500000)), dict(label="$1 million", value=GE("65-74", 1000000), hl=True)],
                  ["at least a hundred thousand", "two hundred and fifty thousand", "half a million", "a million or more"]),
         narration="Here's another way to see it, counting every household, with or without an account. {p} Among households aged sixty-five to seventy-four, about thirty-six percent have at least a hundred thousand dollars in retirement accounts. {p} About one in four has at least two hundred and fifty thousand. {p} About eighteen percent, half a million. {p} And about eleven and a half percent, a million or more. Roughly one in nine. {pp} For fifty-five to sixty-four, the shares are a little higher: about forty percent have a hundred thousand or more, and about twelve percent a million. {p} Seventy-five and older: about thirty-one percent have a hundred thousand or more, and about eleven percent a million."),
    dict(act=4, type="host", bg="none",
         narration="And at the bottom: about half of all households aged sixty-five to seventy-four have nothing in these accounts. For most of them, retirement income comes from Social Security, sometimes a pension, home equity, and work. {p} That's why Social Security matters so much. For many retirees, the lifetime value of their checks is worth more than everything in their accounts, even though it never shows up on a balance sheet. And Social Security checks rise with inflation every year, which no savings account can promise.",
         items=[dict(at="have nothing", text="~Half: $0 in accounts", color="acc"), dict(at="Social Security, sometimes a pension", text="Social Security · pension · home", color="acc2"), dict(at="never shows up", text="Not on any balance sheet", serif=True, size=58)]),

    # ---------------- 5 · WHAT IT PAYS ----------------
    dict(act=5, type="stats", title="What the median balance pays", sub="Age 65–74 · 4% rule of thumb · before taxes", src="4% rule of thumb (Bengen, 1994): first-year withdrawal of 4% of savings · Social Security Administration, 2027 COLA Fact Sheet · illustration, not advice",
         stats=[dict(at="eight hundred and fifty-seven dollars a month", value=round(WD / 12), fmt="usd0", label="per month from $257k (4%)"), dict(at="two thousand one hundred and seventy dollars a month", value=SS_AVG, fmt="usd0", label="average Social Security check, 2027")],
         narration="So what does the median balance actually pay? {p} Using the common four percent rule of thumb, a balance of two hundred and fifty-seven thousand dollars supports a first-year withdrawal of about ten thousand two hundred and eighty dollars. That's about eight hundred and fifty-seven dollars a month, before taxes. {p} Compare that with Social Security. In 2027, the average retired worker's check is about two thousand one hundred and seventy dollars a month. {pp} So for the typical household with an account, Social Security pays about two and a half times more than the 401(k) does."),
    dict(act=5, type="host", bg="none",
         narration="Two more things to keep in mind. {p} First, money in traditional, pre-tax accounts is taxed as income when you take it out. Two hundred and fifty-seven thousand dollars in a traditional IRA is not two hundred and fifty-seven thousand dollars to spend. {p} Second, these are household numbers. A married couple counts once, with both spouses' accounts added together. So for a couple, the typical balance per person is even smaller. {p} And if your money is in a Roth IRA or a Roth 401(k), qualified withdrawals are tax-free, so the same balance goes further.",
         items=[dict(at="taxed as income", text="Pre-tax = taxed on the way out", color="acc"), dict(at="household numbers", text="Couples count once", color="acc2")]),

    # ---------------- 6 · WHERE YOU STAND ----------------
    dict(act=6, type="list", title="The ladder, age 65–74", src=OURS,
         narration="So here's the quick ladder for sixty-five to seventy-four. {p} Zero: about half of all households. {p} About ninety-four thousand: the bottom quarter of those with an account. {p} About two hundred and fifty-seven thousand: the middle. {p} About eight hundred and thirty-seven thousand: the top quarter. {p} About one point nine five million: the top ten percent. {pp} If you're somewhere between two rungs, you're in very normal company. Most people are. {p} Wherever you are on this ladder, remember that it leaves out Social Security, pensions and your home.",
         items=[dict(at="Zero: about half", kind="bullet", text="$0 · about half of households"),
                dict(at="About ninety-four thousand", kind="bullet", text="$94k · bottom quarter of holders"),
                dict(at="About two hundred and fifty-seven", kind="bullet", text="$257k · the middle"),
                dict(at="About eight hundred and thirty-seven", kind="bullet", text="$837k · top quarter"),
                dict(at="About one point nine five million", kind="bullet", text="$1.95M · top 10%"),
                dict(at="leaves out Social Security", kind="title", text="NOT COUNTED: SOCIAL SECURITY, PENSIONS, HOME")]),
    dict(act=6, type="host", bg="none",
         narration="Tell me in the comments: does your balance surprise you, compared with these numbers? {p} And if you're already retired, I'd like to know: was it a 401(k), an IRA, or a pension that did most of the work? {p} And if you know someone your age who's worried they're behind, send them this. The median might be a relief.",
         items=[dict(at="does your balance surprise you", text="Surprised?", serif=True, size=66), dict(at="did most of the work", text="401(k) · IRA · pension?", color="acc")]),
    dict(act=6, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="AGE 80", color="acc", title="Social Security at 62, 67 or 70?", sub="The break-even ages"),
         narration="For most retirees, the biggest piece is still Social Security. To see when it pays to claim, watch this next. {p} This is Nest Egg Atlas. See you next time.",
         hold=14),
]

snapshot = []
for b in ["all", "<35", "35-44", "45-54", "55-64", "65-74", "75+"]:
    k = b.replace("+", "p").replace("-", "_").replace("<", "u")
    snapshot += [dict(set="has", iso=k, year=2025, value=HAS(b), src=OURS)] + [dict(set=f"p{q}", iso=k, year=2025, value=P(b, q), src=OURS) for q in (25, 50, 75, 90)]
    snapshot += [dict(set="mean", iso=k, year=2025, value=MEAN(b), src=OURS)] + [dict(set=f"ge{kk}", iso=k, year=2025, value=GE(b, kk), src=OURS) for kk in (100000, 250000, 500000, 1000000)]

C = lambda say, st, iso, lo, hi: dict(say=say, set=st, iso=iso, year=2025, min=lo, max=hi)
checks = [
    C("<35 median ≈ $21k", "p50", "u35", 20500, 21499), C("35–44 ≈ $61k", "p50", "35_44", 60500, 61499), C("45–54 ≈ $132k", "p50", "45_54", 131500, 132499),
    C("55–64 ≈ $239k", "p50", "55_64", 238500, 239499), C("65–74 ≈ $257k", "p50", "65_74", 256500, 257499), C("75+ ≈ $257k", "p50", "75p", 256500, 257499),
    C("all: ≈ 55% have an account", "has", "all", 54.5, 55.4), C("45–54 ≈ 63%", "has", "45_54", 62.5, 63.4), C("55–64 ≈ 63%", "has", "55_64", 62.5, 63.4),
    C("65–74 ≈ 49% (slightly more than half have none)", "has", "65_74", 48.5, 49.9), C("75+ ≈ 45%", "has", "75p", 44.5, 45.4),
    C("65–74 p25 ≈ $94k", "p25", "65_74", 93500, 94999), C("65–74 p75 ≈ $837k", "p75", "65_74", 836500, 837499), C("65–74 p90 ≈ $1.95M", "p90", "65_74", 1.945e6, 1.955e6),
    C("55–64 p90 ≈ $1.85M", "p90", "55_64", 1.845e6, 1.855e6),
    dict(say="$100k near the bottom quarter (p25 $94k)", rule="expr", expr=f"{P('65-74', 25)} < 100000 < {P('65-74', 50)}", equal=True),
    C("65–74 mean ≈ $768k", "mean", "65_74", 767000, 768999),
    dict(say="mean ≈ 3× median", rule="expr", expr=f"round({MEAN('65-74')} / {P('65-74', 50)})", equal=3),
    dict(say="share of holders below the mean ≈ 70% (linear between p50 and p75)", rule="expr", expr=f"round(50 + 25 * ({MEAN('65-74')} - {P('65-74', 50)}) / ({P('65-74', 75)} - {P('65-74', 50)}))", equal=72),
    C("65–74 ≥$100k ≈ 36%", "ge100000", "65_74", 35.5, 36.4), C("≥$250k ≈ 1 in 4", "ge250000", "65_74", 24.5, 25.4), C("≥$500k ≈ 18%", "ge500000", "65_74", 17.5, 18.4),
    C("≥$1M ≈ 11.5%", "ge1000000", "65_74", 11.3, 11.7), C("55–64 ≥$100k ≈ 40%", "ge100000", "55_64", 39.0, 40.4), C("55–64 ≥$1M ≈ 12%", "ge1000000", "55_64", 11.8, 12.4),
    dict(say="4% of $257k ≈ $10,280; /12 ≈ $857", rule="expr", expr=f"[round({WD}), round({WD} / 12)]", equal=[10280, 857]),
    dict(say="SS 2,170 / 857 ≈ 2.5×", rule="expr", expr=f"round({SS_AVG} / ({WD} / 12), 1)", equal=2.5),
    dict(say="RMD age 73 (SECURE 2.0)", rule="expr", expr="73", equal=73),
    C("75+ p75 ≈ $978k", "p75", "75p", 977500, 978499), C("55–64 mean ≈ $670k", "mean", "55_64", 669500, 670999),
    C("75+ ≥$100k ≈ 31%", "ge100000", "75p", 30.5, 31.9), C("75+ ≥$1M ≈ 11%", "ge1000000", "75p", 10.5, 11.4),
]

clips = [
    dict(**{"from": "s00", "to": "s00"}, hook="The typical *401(k)* by age", title="The typical 401(k) & IRA balance by age (Fed 2025) #Shorts", desc="Median among households with an account: 55–64 ≈ $239k, 65–74 ≈ $257k (Federal Reserve 2025 SCF, our calculation)."),
    dict(**{"from": "s06", "to": "s06"}, hook="Why the *average* 401(k) lies", title="Average 401(k) at 65–74: $768k. Median: $257k #Shorts", desc="A few very large accounts pull the average up (Federal Reserve 2025 SCF, our calculation)."),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="b-N04-401k", clips=clips, channel="nesteggatlas", chapter0="The numbers", host=False,
            thumb=dict(kind="text", top="TYPICAL 401(k) AT 65–74", big="$257k", line2="NOT $768k", sticker="NEW FED DATA"),
            w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks, datasets=[], snapshot=snapshot,
            voice=dict(model="", name="Algieba",
                       style=("You are the narrator of a calm, trustworthy personal-finance documentary for Americans in their fifties, sixties and seventies. "
                              "Read the script below in a warm, mature, unhurried voice, at about 138 words per minute, like a respected public-radio journalist "
                              "explaining numbers to a friend. Let each dollar figure land with a short pause before it. Sound reassuring and clear, never salesy, "
                              "never alarmed, never like an advertisement.")),
            music=[dict(act=0, track="Lightless Dawn", vol=0.18), dict(act=1, track="Deliberate Thought", vol=0.17), dict(act=2, track="Investigations", vol=0.17),
                   dict(act=3, track="Inspired", vol=0.17), dict(act=4, track="Floating Cities", vol=0.17), dict(act=5, track="Deliberate Thought", vol=0.17), dict(act=6, track="Inspired", vol=0.18)],
            yt=dict(title="401(k) and IRA Balances at 55, 65 and 75: The Fed's New Numbers",
                    description=("What does the typical American household actually have in its 401(k)s and IRAs? Using the Federal Reserve's 2025 Survey of Consumer Finances, "
                                 "we calculate who has a retirement account by age, the median and the percentiles for households with one, why the average is three times the median, "
                                 "the share with $100k, $250k, $500k and $1 million, and what the median balance pays under the 4% rule compared with Social Security.\n\n"
                                 "Educational content, not financial advice.\n\n"
                                 "Sources: Federal Reserve Board, 2025 Survey of Consumer Finances, summary extract public data (our calculation with survey weights; 2025 dollars); "
                                 "Social Security Administration, 2027 COLA Fact Sheet; Bengen (1994), 4% rule of thumb.\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#401k #ira #retirement #retirementsavings #personalfinance"),
                    tags=["401k balance by age", "ira balance by age", "retirement savings by age", "average 401k", "median 401k", "federal reserve", "survey of consumer finances", "retirement", "4% rule", "personal finance"], lang="en"))

json.dump(spec, open(os.path.join(HERE, "b-N04.json"), "w"), ensure_ascii=False, indent=1)
clean = lambda t: t.replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()
words = sum(len(clean(s["narration"])) for s in shots)
acts = {}
for s in shots:
    acts[s["act"]] = acts.get(s["act"], 0) + len(clean(s["narration"]))
print("shots", len(shots), "palavras", words, f"~{words / 138:.1f} min a 138 wpm", "por ato", acts)

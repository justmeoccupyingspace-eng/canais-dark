"""Gera specs/long/b-N08.json — Nest Egg Atlas (canal B) longo: patrimônio líquido de quem tem 65–74 anos (topo 10%, mediana, base).
Dados: Federal Reserve, 2025 Survey of Consumer Finances (divulgado em 09/10/2026), extrato público com os pesos da pesquisa:
research/scf2025.json (scf.yml run 41602248705). NETWORTH do SCF = ativos − dívidas da família; NÃO inclui Social Security nem pensões de benefício definido.
Faixas por idade do chefe da família. 'mill' = famílias com patrimônio ≥ US$ 1 milhão. LIQ = contas de transação (corrente, poupança, money market).
q15: Retiree Math (17,7 mil inscritos) 416 mil views "How Wealthy Are You Compared to Most Retirees?"; American Finance (4 mil) 38 mil "Top 10% of American Retirees"."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SCF = json.load(open(os.path.join(HERE, "..", "..", "research", "scf2025.json")))
B = SCF["bands"]
OURS = "Nest Egg Atlas calculation from the Federal Reserve's 2025 Survey of Consumer Finances public data (survey weights) · households by age of head · 2025 dollars"
ACTS = ["Cold open", "What counts", "The ladder", "The millionaires", "By age", "The other end", "Where you stand"]
NW = lambda b, q: B[b]["networth_pct"][str(q)]
GE = lambda b, k: round(B[b]["share_nw_ge"][str(k)] * 100, 1)
M = B["65-74"]["mill"]
HH = B["65-74"]["weight_sum"]


def cue(bars, ats):
    for b, a in zip(bars, ats):
        b["at"] = a
    return bars


shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="rank", title="Net worth, households 65–74", sub="Where each group starts · 2025", fmt="usdkm", count=False, vmax=3800000, src=OURS,
         bars=cue([dict(label="Bottom 25% below", value=NW("65-74", 25)), dict(label="Median", value=NW("65-74", 50)), dict(label="Top 25% from", value=NW("65-74", 75)), dict(label="Top 10% from", value=NW("65-74", 90), hl=True)],
                  ["The bottom quarter", "The typical household", "To be in the top quarter", "to be in the top ten percent"]),
         narration="The Federal Reserve recently released its newest survey of American family finances, and it answers a question a lot of people quietly wonder about: how do I compare? {p} For households where the head is sixty-five to seventy-four, here's the ladder. {p} The bottom quarter has less than about a hundred and eighteen thousand dollars in net worth. {p} The typical household, right in the middle, has about four hundred and thirty-one thousand. {p} To be in the top quarter, you need about one point three million. {p} And to be in the top ten percent, about three point six million dollars. {pp} So the top ten percent starts at more than eight times what the typical household has."),
    dict(act=0, type="host", bg="none",
         narration="In this video, we'll look at what actually counts in that number, the full ladder from the bottom to the very top, how many retirees are millionaires and what their money is made of, how it changes with age, and the part of the picture that's easy to miss: the households at the bottom. {p} These are real survey numbers, not estimates from a calculator: about twenty-two million households in this age group, measured by the Federal Reserve. {pp} <soft>As always, this is education, not financial advice.</soft>",
         items=[dict(at="what actually counts", text="What counts", color="acc"), dict(at="how many retirees are millionaires", text="1 in 3 are millionaires?", color="acc2"), dict(at="the households at the bottom", text="The other end", serif=True, size=62)]),

    # ---------------- 1 · WHAT COUNTS ----------------
    dict(act=1, type="list", title="What counts in net worth", src="Federal Reserve, Survey of Consumer Finances: net worth = assets minus debts (excludes Social Security and defined-benefit pensions)",
         narration="First, what goes into that number. {p} Net worth is everything a household owns, minus everything it owes. {p} That includes the home: what it's worth, minus the mortgage. {p} Retirement accounts like 401(k)s and IRAs. {p} Savings, stocks, bonds, and any business. {p} Cars count too. Minus every debt: the mortgage, car loans, credit cards. {pp} And one thing is left out: the value of future Social Security checks and traditional pensions. For many retirees, those are worth a lot, and they don't show up here at all.",
         items=[dict(at="That includes the home", kind="bullet", text="+ Home, minus the mortgage"),
                dict(at="Retirement accounts like", kind="bullet", text="+ 401(k)s and IRAs"),
                dict(at="Savings, stocks, bonds", kind="bullet", text="+ Savings, stocks, a business"),
                dict(at="Minus every debt", kind="bullet", text="− Every debt"),
                dict(at="one thing is left out", kind="title", text="NOT COUNTED: SOCIAL SECURITY")]),
    dict(act=1, type="host", bg="none",
         narration="The home is a big part of it. About eighty percent of households in this age group own their home, and the median household has about two hundred and ten thousand dollars of home equity. {p} Take the home out, and the typical net worth drops from about four hundred and thirty-one thousand to about a hundred and forty thousand. {pp} In the middle of the ladder, the house does a lot of the work. Near the top, as we'll see, it's a much smaller share. {p} And for renters, there's no home equity at all, which is one reason the bottom of the ladder looks so different.",
         items=[dict(at="own their home", text="80% own their home", color="acc2"), dict(at="two hundred and ten thousand", text="Median home equity: $210k", color="acc"), dict(at="Take the home out", text="Without the home: $140k", serif=True, size=62)]),

    # ---------------- 2 · THE LADDER ----------------
    dict(act=2, type="rank", title="The full ladder, ages 65–74", sub="Net worth where each group starts · 2025", fmt="usdkm", count=False, vmax=7500000, src=OURS,
         bars=cue([dict(label="Bottom 10% below", value=NW("65-74", 10)), dict(label="Bottom 25% below", value=NW("65-74", 25)), dict(label="Median", value=NW("65-74", 50)),
                   dict(label="Top 25% from", value=NW("65-74", 75)), dict(label="Top 10% from", value=NW("65-74", 90)), dict(label="Top 5% from", value=NW("65-74", 95), hl=True)],
                  ["The bottom ten percent", "The bottom quarter", "The middle", "The top quarter starts", "The top ten percent, at", "the top five percent"]),
         narration="Here's the whole ladder. {p} The bottom ten percent: less than about sixty-five hundred dollars. {p} The bottom quarter: less than about a hundred and eighteen thousand. {p} The middle: about four hundred and thirty-one thousand. {p} The top quarter starts at about one point three million. {p} The top ten percent, at about three point six million. {p} And the top five percent, at about seven point one million. {pp} The very top one percent starts at about twenty and a half million dollars. {p} Between the start of the top five percent and the bottom ten percent, that's a difference of more than a thousand times."),
    dict(act=2, type="host", bg="none",
         narration="Notice how fast it climbs at the top. Going from the middle to the start of the top quarter means about three times more. From there to the top ten percent, almost three times again. {p} That's also why the average is so misleading. The average net worth for this age group is about one point nine million dollars. That's more than four times the median, because a relatively small number of very wealthy households pull it up. {pp} When you see an average in a headline, the typical household is usually far below it. Medians are the fairer way to compare.",
         items=[dict(at="about three times more", text="Median → top 25%: ×3", color="acc"), dict(at="almost three times again", text="Top 25% → top 10%: ×2.8", color="acc"), dict(at="one point nine million", text="Average: $1.9M (not typical)", color="warm", size=62)]),

    # ---------------- 3 · THE MILLIONAIRES ----------------
    dict(act=3, type="stats", title="Households 65–74 with at least…", src=OURS,
         stats=[dict(at="at least half a million", value=GE("65-74", 500000), fmt="pct0", label="$500,000"), dict(at="at least a million", value=GE("65-74", 1000000), fmt="pct0", label="$1 million"),
                dict(at="at least two million", value=GE("65-74", 2000000), fmt="pct0", label="$2 million"), dict(at="at least five million", value=GE("65-74", 5000000), fmt="pct0", label="$5 million")],
         narration="So how many retirees are millionaires? More than you might think. {p} About forty-five percent of households aged sixty-five to seventy-four have at least half a million dollars. {p} About thirty-one percent have at least a million. {p} About nineteen percent, at least two million. {p} And about eight percent, at least five million. {pp} That's roughly one in three households in this age group with a seven-figure net worth: about six point eight million households."),
    dict(act=3, type="host", bg="none",
         narration="So what does a typical millionaire household at this age look like? {p} Its median net worth is about two and a half million dollars. Almost all of them, ninety-eight percent, own their home, with about five hundred and seventy-five thousand dollars of equity. {p} The typical one has about six hundred and sixty thousand dollars in retirement accounts, and an income of about a hundred and forty thousand a year. {pp} But the home is usually only about a fifth of their net worth. Much more of their money is in financial assets: the typical one has about one point three million dollars in stocks, funds, savings and retirement accounts combined. {p} In other words, most millionaire retirees didn't get there through their house alone.",
         items=[dict(at="two and a half million", text="Median: $2.5M", color="acc"), dict(at="ninety-eight percent", text="98% own a home", color="acc2"), dict(at="six hundred and sixty thousand", text="Retirement accounts: $660k", size=62), dict(at="about a fifth", text="Home ≈ 1/5 of net worth", serif=True, size=60)]),

    # ---------------- 4 · BY AGE ----------------
    dict(act=4, type="rank", title="Median net worth by age", sub="Households by age of head · 2025", fmt="usdkm", count=False, vmax=560000, src=OURS,
         bars=cue([dict(label="55–64", value=NW("55-64", 50)), dict(label="65–74", value=NW("65-74", 50)), dict(label="75 and older", value=NW("75+", 50), hl=True)],
                  ["fifty-five to sixty-four has", "Sixty-five to seventy-four: about", "Seventy-five and older"]),
         narration="Here's something that surprises people: in this survey, net worth doesn't fall after retirement. It keeps rising. {p} The typical household aged fifty-five to sixty-four has about four hundred and eleven thousand. {p} Sixty-five to seventy-four: about four hundred and thirty-one thousand. {p} Seventy-five and older: about five hundred and four thousand. {pp} The top ten percent line rises too: from about three point five million, to about three point six, to about four point two million for households seventy-five and older."),
    dict(act=4, type="host", bg="none",
         narration="Part of that is the home. Older households have usually paid down more of their mortgage, and home values have risen. The median household's home equity goes from about a hundred and fifty-eight thousand at fifty-five to sixty-four, to about two hundred and forty-five thousand at seventy-five and older. {p} Part of it is who's in the group. People with more money tend to live longer, so the oldest group is a bit wealthier on average. {pp} And this is a snapshot of different generations in 2025, not one family followed over time. So compare yourself with your own age group, not with a single national number.",
         items=[dict(at="Part of that is the home", text="Home equity: $158k → $245k", color="acc"), dict(at="tend to live longer", text="Wealthier people live longer", color="acc2", size=62), dict(at="a snapshot", text="A 2025 snapshot", serif=True, size=62)]),

    # ---------------- 5 · THE OTHER END ----------------
    dict(act=5, type="stats", title="The other end of the ladder, ages 65–74", src=OURS,
         stats=[dict(at="a net worth of zero or less", value=round(B["65-74"]["share_nw_le0"] * 100, 1), fmt="pct1", label="zero or negative net worth"), dict(at="less than about sixty-five hundred", value=NW("65-74", 10), fmt="usd0", label="bottom 10% below"),
                dict(at="ten thousand dollars in checking", value=B["65-74"]["liq_median_all"], fmt="usd0", label="median in checking & savings")],
         narration="Now the other end. {p} About five percent of households in this age group have a net worth of zero or less: they owe as much as they own, or more. {p} The bottom ten percent has less than about sixty-five hundred dollars. {p} And the typical household has about ten thousand dollars in checking and savings accounts. {pp} For many of the households near the bottom, Social Security isn't one part of retirement income. It's most of it. That's why the size of that monthly check matters so much."),
    dict(act=5, type="host", bg="none",
         narration="And what about income? For households aged sixty-five to seventy-four, the median income in this survey is about seventy thousand dollars a year. To be in the top ten percent by income, it takes about two hundred and thirty-five thousand. {p} The bottom ten percent by income have about twenty thousand dollars a year or less. {p} Income and wealth don't always line up. Plenty of retirees have a modest income and a paid-off house worth a lot. And some have a high income and very little saved. {pp} Both numbers matter. Net worth is how long your money can last. Income is how comfortable each year feels.",
         items=[dict(at="median income", text="Median income: ~$70k", color="acc2"), dict(at="two hundred and thirty-five thousand", text="Top 10% income: $235k+", color="acc"), dict(at="Both numbers matter", text="Wealth ≠ income", serif=True, size=64)]),

    # ---------------- 6 · WHERE YOU STAND ----------------
    dict(act=6, type="list", title="Where do you stand? Ages 65–74", src=OURS,
         narration="So here's where the lines fall for households aged sixty-five to seventy-four. {p} Under about a hundred and eighteen thousand puts you in the bottom quarter. {p} Around four hundred and thirty thousand is the middle. {p} About one point three million puts you in the top quarter. {p} About three point six million, in the top ten percent. {p} And about twenty and a half million, in the top one percent. {pp} And remember: these numbers leave out Social Security and traditional pensions, which for many people are worth hundreds of thousands of dollars more. {p} And for households seventy-five and older, every line is a little higher: the middle is about five hundred thousand, and the top ten percent starts at about four point two million.",
         items=[dict(at="Under about a hundred and eighteen", kind="bullet", text="Bottom 25%: under $118k"),
                dict(at="Around four hundred and thirty", kind="bullet", text="Median: about $431k"),
                dict(at="puts you in the top quarter", kind="bullet", text="Top 25%: $1.3M+"),
                dict(at="in the top ten percent", kind="bullet", text="Top 10%: $3.6M+"),
                dict(at="in the top one percent", kind="bullet", text="Top 1%: $20.5M+")]),
    dict(act=6, type="host", bg="none",
         narration="Tell me in the comments: were you surprised by where the median is? {p} And if you know someone who's sure they're behind, send them this. They might be doing better than they think.",
         items=[dict(at="surprised", text="Surprised?", serif=True, size=70), dict(at="better than they think", text="Share it", color="acc")]),
    dict(act=6, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="$257k", color="acc", title="The typical 401(k) at 65–74", sub="Not $768k."),
         narration="Net worth is the big picture. If you want to see what's actually in the typical retirement account, watch this next. {p} This is Nest Egg Atlas. See you next time.",
         hold=14),
]

snapshot = []
for b in ("55-64", "65-74", "75+"):
    for q, v in B[b]["networth_pct"].items():
        snapshot.append(dict(set="nw", iso=b, year=int(q), value=v, src=OURS))

R = lambda x, n=0: round(x, n)
E = lambda say, expr, eq: dict(say=say, rule="expr", expr=expr, equal=eq)
checks = [
    E("SCF 2025 released 09/10/2026 (recently)", "2026", 2026),
    E("65–74: p25 ≈ $118k, p50 ≈ $431k, p75 ≈ $1.3M, p90 ≈ $3.6M", f"[{R(NW('65-74', 25) / 1000)}, {R(NW('65-74', 50) / 1000)}, {R(NW('65-74', 75) / 1e6, 1)}, {R(NW('65-74', 90) / 1e6, 1)}]", [118, 431, 1.3, 3.6]),
    E("p90 / p50 > 8", f"{NW('65-74', 90) / NW('65-74', 50)} > 8", True),
    E("SCF net worth excludes Social Security and DB pensions (Fed SCF definition)", "True", True),
    E("homeowner ≈ 80%; median home equity ≈ $210k; without home median ≈ $140k", f"[{R(B['65-74']['homeowner_share'] * 100)}, {R(B['65-74']['homeeq_median_all'] / 1000)}, {R(B['65-74']['nwx_pct']['50'] / 1000)}]", [80, 210, 140]),
    E("p10 ≈ $6.5k, p95 ≈ $7.1M, p99 ≈ $20.5M", f"[{R(NW('65-74', 10) / 100) * 100}, {R(NW('65-74', 95) / 1e6, 1)}, {R(NW('65-74', 99) / 1e6, 1)}]", [6500, 7.1, 20.5]),
    E("p75/p50 ≈ 3, p90/p75 ≈ 2.8 (almost 3)", f"[{R(NW('65-74', 75) / NW('65-74', 50), 1)}, {R(NW('65-74', 90) / NW('65-74', 75), 1)}]", [3.0, 2.8]),
    E("mean ≈ $1.9M, > 4× median", f"[{R(B['65-74']['networth_mean'] / 1e6, 1)}, {B['65-74']['networth_mean'] / NW('65-74', 50)} > 4]", [1.9, True]),
    E("≥$500k 45%, ≥$1M 31%, ≥$2M 19%, ≥$5M 8%", f"[{R(GE('65-74', 500000))}, {R(GE('65-74', 1000000))}, {R(GE('65-74', 2000000))}, {R(GE('65-74', 5000000))}]", [45, 31, 19, 8]),
    E("≈ 6.8M households ≥ $1M (weights)", f"{R(HH * B['65-74']['share_nw_ge']['1000000'] / 1e6, 1)}", 6.8),
    E("millionaires: median NW ≈ $2.5M, 98% own home, home equity ≈ $575k, retirement ≈ $660k, income ≈ $140k, home ≈ 1/5, fin ≈ $1.3M",
      f"[{R(M['nw_med'] / 1e6, 1)}, {R(M['home_share'] * 100)}, {R(M['homeeq_med'] / 1000)}, {R(M['ret_med'] / 10000) * 10}, {R(M['inc_med'] / 10000) * 10}, {R(M['home_pct_of_nw_med'], 1)}, {R(M['fin_med'] / 1e6, 1)}]", [2.5, 98, 575, 660, 140, 0.2, 1.3]),
    E("median 55–64 ≈ $411k, 65–74 ≈ $431k, 75+ ≈ $504k", f"[{R(NW('55-64', 50) / 1000)}, {R(NW('65-74', 50) / 1000)}, {R(NW('75+', 50) / 1000)}]", [411, 431, 504]),
    E("p90 by age ≈ 3.5M, 3.6M, 4.2M", f"[{R(NW('55-64', 90) / 1e6, 1)}, {R(NW('65-74', 90) / 1e6, 1)}, {R(NW('75+', 90) / 1e6, 1)}]", [3.5, 3.6, 4.2]),
    E("home equity 55–64 ≈ $158k → 75+ ≈ $245k", f"[{R(B['55-64']['homeeq_median_all'] / 1000)}, {R(B['75+']['homeeq_median_all'] / 1000)}]", [158, 245]),
    E("wealthier people live longer (Chetty et al., JAMA 2016) — fato citado", "True", True),
    E("≤0 net worth ≈ 5%; median checking & savings ≈ $10k", f"[{R(B['65-74']['share_nw_le0'] * 100)}, {R(B['65-74']['liq_median_all'])}]", [5, 10000]),
    E("income 65–74: median ≈ $70k, p90 ≈ $235k", f"[{R(B['65-74']['income_pct']['50'] / 1000)}, {R(B['65-74']['income_pct']['90'] / 1000)}]", [70, 235]),
    E("weighted households 65–74 ≈ 22M", f"{R(HH / 1e6)}", 22),
    E("p95 / p10 > 1000", f"{NW('65-74', 95) / NW('65-74', 10)} > 1000", True),
    E("income p10 ≈ $20k (under about 20k? 20,541 → 'less than about twenty thousand' ok)", f"{R(B['65-74']['income_pct']['10'] / 1000)}", 21),
    E("75+: median ≈ $500k (504k), p90 ≈ $4.2M", f"[{R(NW('75+', 50) / 100000) * 100}, {R(NW('75+', 90) / 1e6, 1)}]", [500, 4.2]),
    E("SS present value ≈ hundreds of thousands: $2,170 × 12 × 20 years undiscounted ≈ $520k", "round(2170 * 12 * 20 / 1000)", 521),
]

clips = [
    dict(**{"from": "s00", "to": "s00"}, hook="Top 10% net worth at *65–74*", title="The net worth that puts you in the top 10% at 65–74 (Fed 2025) #Shorts", desc="Households 65–74, Federal Reserve 2025 SCF (our calculation): bottom 25% under $118k, median $431k, top 25% from $1.3M, top 10% from $3.6M."),
    dict(**{"from": "s06", "to": "s06"}, hook="How many retirees are *millionaires*?", title="1 in 3 households aged 65–74 are millionaires #Shorts", desc="Share with net worth of at least $500k: 45%, $1M: 31%, $2M: 19%, $5M: 8% (Federal Reserve 2025 SCF, our calculation)."),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="b-N08-networth", clips=clips, channel="nesteggatlas", chapter0="The ladder", host=False,
            thumb=dict(kind="text", top="TOP 10% AT 65–74:", big="$3.6M", line2="MEDIAN: $431k", sticker="NEW FED DATA"),
            w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks, datasets=[], snapshot=snapshot,
            voice=dict(model="", name="Algieba",
                       style=("You are the narrator of a calm, trustworthy personal-finance documentary for Americans in their fifties, sixties and seventies. "
                              "Read the script below in a warm, mature, unhurried voice, at about 135 words per minute, like a respected public-radio journalist "
                              "explaining numbers to a friend. Take your time with every dollar figure and let it land with a short pause before it. "
                              "Read only the script, word for word. Sound reassuring and clear, never rushed, never salesy, never alarmed, never like an advertisement.")),
            music=[dict(act=0, track="Lightless Dawn", vol=0.18), dict(act=1, track="Deliberate Thought", vol=0.17), dict(act=2, track="Investigations", vol=0.17),
                   dict(act=3, track="Inspired", vol=0.17), dict(act=4, track="Floating Cities", vol=0.17), dict(act=5, track="Deliberate Thought", vol=0.17), dict(act=6, track="Inspired", vol=0.18)],
            yt=dict(title="What Net Worth Puts You in the Top 10% at 65–74? (New Fed Data)",
                    description=("How does your net worth compare with other households aged 65 to 74? Using the Federal Reserve's 2025 Survey of Consumer Finances, "
                                 "we calculate the full ladder (bottom 10%, bottom 25%, median, top 25%, top 10%, top 5%, top 1%), what counts in net worth, how many retirees are millionaires "
                                 "and what their money is made of, how net worth changes from 55 to 75+, and the households at the bottom.\n\n"
                                 "Net worth = assets minus debts, including home equity and retirement accounts; it does not include Social Security or traditional pensions.\n\n"
                                 "Educational content, not financial advice.\n\n"
                                 "Sources: Federal Reserve Board, 2025 Survey of Consumer Finances, summary extract public data (our calculation with survey weights; 2025 dollars).\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#networth #retirement #top10percent #personalfinance #retirementplanning"),
                    tags=["net worth by age", "net worth percentile", "top 10 percent net worth", "retiree net worth", "median net worth 65", "federal reserve", "survey of consumer finances", "retirement", "millionaire retirees", "personal finance"], lang="en"))

json.dump(spec, open(os.path.join(HERE, "b-N08.json"), "w"), ensure_ascii=False, indent=1)
clean = lambda t: t.replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()
words = sum(len(clean(s["narration"])) for s in shots)
acts = {}
for s in shots:
    acts[s["act"]] = acts.get(s["act"], 0) + len(clean(s["narration"]))
print("shots", len(shots), "palavras", words, f"~{words / 140:.1f} min a 140 wpm", "por ato", acts)

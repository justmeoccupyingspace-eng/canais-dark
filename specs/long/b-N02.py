"""Gera specs/long/b-N02.json — Nest Egg Atlas (canal B) longo #2: quantos aposentados têm de fato US$ 1 milhão.
Dados: Federal Reserve, 2025 Survey of Consumer Finances (divulgado em 09/10/2026), extrato público com os pesos da pesquisa:
research/scf2025.json (scf.yml run 41602248705). Todas as frações e medianas são cálculo nosso com os pesos; total de famílias = soma dos pesos."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SCF = json.load(open(os.path.join(HERE, "..", "..", "research", "scf2025.json")))
B = SCF["bands"]
OURS = "Nest Egg Atlas calculation from the Federal Reserve's 2025 Survey of Consumer Finances public data (survey weights) · 2025 dollars"
ACTS = ["Cold open", "What counts", "Counting everything", "Without the house", "The million-dollar 401(k)", "Who the millionaires are", "What $1 million buys"]
pc = lambda x: round(x * 100, 1)
S1 = lambda b: pc(B[b]["share_nw_ge"]["1000000"])
SX = lambda b: pc(B[b]["share_nwx_ge"]["1000000"])
SF = lambda b: pc(B[b]["share_fin_ge"]["1000000"])
SR = lambda b: pc(B[b]["ret_share_ge"]["1000000"])
M = B["65+"]["mill"]
HH65 = B["65+"]["weight_sum"]

def cue(bars, ats):
    for b, a in zip(bars, ats):
        b["at"] = a
    return bars

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="rank", title="Households 65+ with $1 million or more", sub="Depends on what you count · 2025", fmt="pct1", count=False, vmax=40, src=OURS,
         bars=cue([dict(label="Everything they own", value=S1("65+"), hl=True), dict(label="Not counting the house", value=SX("65+")),
                   dict(label="Savings & investments", value=SF("65+")), dict(label="In 401(k)s & IRAs", value=SR("65+"))],
                  ["counting everything", "leave out the house", "savings and investments", "retirement accounts alone"]),
         narration="There are about forty million American households headed by someone sixty-five or older. {p} How many of them have a million dollars? {pp} According to the Federal Reserve's newest survey, counting everything they own, about thirty-two percent. Roughly one in three. {p} But that number changes a lot depending on what you count. {p} If you leave out the house, it drops to about twenty-three percent. {p} Count only savings and investments, and it's about eighteen percent. {p} And in retirement accounts alone, like 401(k)s and IRAs, only about eleven percent."),
    dict(act=0, type="host", bg="none",
         narration="So is the million-dollar retiree common, or rare? {p} The honest answer is: both, depending on the question. {pp} In this video, we'll go through each definition, age group by age group, using the Fed's own public data. And at the end, we'll look at what a million dollars actually buys in retirement. {p} Why does this matter? Because millionaire headlines can make people feel behind, or falsely comfortable. Knowing which number you're looking at changes the whole picture. {p} <soft>As always, this is education, not financial advice.</soft>",
         items=[dict(at="common, or rare", text="Common or rare?", serif=True, size=66), dict(at="each definition", text="4 ways to count", color="acc"), dict(at="actually buys", text="What $1M buys", color="acc2")]),

    # ---------------- 1 · WHAT COUNTS ----------------
    dict(act=1, type="list", title="Four ways to count $1 million", src="Federal Reserve SCF definitions: net worth, financial assets, quasi-liquid retirement accounts, home equity",
         narration="First, the four ways to count. {p} One: net worth. Everything a household owns, including the home, minus everything it owes. {p} Two: net worth without the house. The same thing, but leaving out the equity in the home you live in. {p} Three: financial assets. Bank accounts, stocks, bonds, mutual funds and retirement accounts, but not real estate or businesses. {p} Four: retirement accounts only. 401(k)s, IRAs and similar plans. {pp} None of these include future Social Security checks or traditional pensions. So many retirees are better off than any of these numbers show.",
         items=[dict(at="One: net worth", kind="bullet", text="1 · Net worth (everything)"),
                dict(at="Two: net worth without", kind="bullet", text="2 · Net worth without the house"),
                dict(at="Three: financial assets", kind="bullet", text="3 · Savings & investments"),
                dict(at="Four: retirement accounts", kind="bullet", text="4 · 401(k)s & IRAs only"),
                dict(at="None of these include", kind="title", text="NOT COUNTED: SOCIAL SECURITY, PENSIONS")]),

    dict(act=1, type="host", bg="none",
         narration="Why does each definition matter? {p} Home equity is real wealth, but it's hard to spend without selling or borrowing against the house. {p} Financial assets can be spent, but there's a catch: money in a traditional 401(k) or IRA is taxed when you take it out. A million dollars in those accounts is not a million dollars after taxes. {pp} And retirement accounts are only one part of the picture for people who also have pensions, rental property or a small business.",
         items=[dict(at="Home equity is real wealth", text="House: real, but hard to spend", color="acc2"), dict(at="taxed when you take it out", text="401(k)/IRA: taxed on withdrawal", color="acc"), dict(at="only one part", text="One piece of the picture", serif=True, size=56)]),

    # ---------------- 2 · COUNTING EVERYTHING ----------------
    dict(act=2, type="rank", title="$1 million or more, counting everything", sub="Share of households, 2025", fmt="pct1", count=False, vmax=40, src=OURS,
         bars=cue([dict(label="All ages", value=S1("all")), dict(label="55–64", value=S1("55-64"), hl=True), dict(label="65–74", value=S1("65-74"), hl=True), dict(label="75 and older", value=S1("75+"), hl=True)],
                  ["all American households", "fifty-five to sixty-four", "sixty-five to seventy-four", "seventy-five and older"]),
         narration="Let's start with the broadest measure: net worth, counting everything. {p} Across all American households, about twenty-two percent are worth a million dollars or more. {p} Among households aged fifty-five to sixty-four, about thirty-two percent. {p} Sixty-five to seventy-four, about thirty-one percent. {p} And seventy-five and older, about thirty-four percent. {p} For comparison, between forty-five and fifty-four it's about twenty-four percent, and under thirty-five, less than two percent. {pp} In total, that's roughly thirteen million households headed by someone sixty-five or older. {p} That surprises a lot of people. But it makes sense: these households have had decades for their homes, savings and investments to grow. {p} Many bought their homes decades ago, when prices were far lower. A house bought in the 1990s can be worth several times that today."),
    dict(act=2, type="host", bg="none",
         narration="But a million dollars in net worth is not a million dollars in the bank. {p} For many of these households, a big piece of that million is the house they live in. You can't spend it without selling it, borrowing against it, or moving somewhere smaller. {pp} So let's take the house out.",
         items=[dict(at="not a million dollars in the bank", text="Net worth ≠ cash", color="acc"), dict(at="the house they live in", text="A big piece is the house", color="acc2"), dict(at="take the house out", text="Now, without the house", serif=True, size=60)]),

    # ---------------- 3 · WITHOUT THE HOUSE ----------------
    dict(act=3, type="rank", title="$1 million or more, without the house", sub="Net worth minus home equity · share of households, 2025", fmt="pct1", count=False, vmax=40, src=OURS,
         bars=cue([dict(label="55–64", value=SX("55-64"), hl=True), dict(label="65–74", value=SX("65-74"), hl=True), dict(label="75 and older", value=SX("75+"), hl=True)],
                  ["fifty-five to sixty-four", "sixty-five to seventy-four", "seventy-five and older"]),
         narration="Without home equity, the share of millionaire households drops to about twenty-five percent at fifty-five to sixty-four, about twenty-three percent at sixty-five to seventy-four, and about twenty-three percent at seventy-five and older. {p} Still close to one in four. Notice the house matters most for the oldest households, who've had the longest to pay it off. {pp} But look at the middle household instead of the top. {p} Without the house, the typical household aged sixty-five or older is worth about a hundred and sixty thousand dollars. {p} At fifty-five to sixty-four, about a hundred and fifty thousand."),
    dict(act=3, type="stats", title="Typical household, without the house", src=OURS,
         stats=[dict(at="a hundred and sixty thousand", value=B["65+"]["nwx_pct"]["50"], fmt="usdkm", label="median, age 65+"), dict(at="a million or more", value=SX("65+"), fmt="pct0", label="age 65+ with $1M+ without the house")],
         narration="So the picture splits in two. {p} A large group, about one in four, has a million or more even without counting the home. {p} And the household right in the middle has about a hundred and sixty thousand. {pp} That's the gap a single average number hides. If you're somewhere in between, you're in very normal company. {p} Savings and investments tell a similar story: about nineteen percent of households at fifty-five to sixty-four, seventeen percent at sixty-five to seventy-four, and twenty percent at seventy-five and older have a million or more in financial assets."),

    # ---------------- 4 · THE MILLION-DOLLAR 401(K) ----------------
    dict(act=4, type="rank", title="$1 million or more in retirement accounts", sub="401(k), IRA and similar plans · share of households, 2025", fmt="pct1", count=False, vmax=40, src=OURS,
         bars=cue([dict(label="All ages", value=SR("all")), dict(label="55–64", value=SR("55-64"), hl=True), dict(label="65–74", value=SR("65-74"), hl=True), dict(label="75 and older", value=SR("75+"), hl=True)],
                  ["Across all ages", "fifty-five to sixty-four", "sixty-five to seventy-four", "seventy-five and older"]),
         narration="Now the strictest test: a million dollars in retirement accounts alone. {p} Across all ages, only about seven percent of households have that much in 401(k)s and IRAs. {p} At fifty-five to sixty-four, about twelve percent. {p} Sixty-five to seventy-four, about eleven and a half. {p} Seventy-five and older, about eleven. {pp} So the million-dollar 401(k) is real, but it's about one household in nine, even among people at or near retirement."),
    dict(act=4, type="host", bg="none",
         narration="Why so few, when one in three is a millionaire overall? {p} Partly because 401(k)s only became common in the 1980s and 90s. Many of today's retirees spent part of their careers with traditional pensions instead. {p} And partly because much of their wealth sits elsewhere: in homes, businesses, and regular brokerage and bank accounts. {pp} That doesn't mean a 401(k) can't get you there. It means today's retirees, as a group, built their wealth in more than one place. For people now in their forties and fifties, who've had 401(k)s their whole careers, these numbers will probably look different.",
         items=[dict(at="Why so few", text="Why so few?", serif=True, size=66), dict(at="traditional pensions", text="Pensions came first", color="acc2"), dict(at="sits elsewhere", text="Homes · businesses · brokerage", color="acc")]),

    # ---------------- 5 · WHO THE MILLIONAIRES ARE ----------------
    dict(act=5, type="stats", title="The typical millionaire household, 65+", src=OURS,
         stats=[dict(at="two point seven million", value=M["nw_med"], fmt="usdkm", label="median net worth"), dict(at="six hundred thousand", value=M["homeeq_med"], fmt="usdkm", label="median home equity")],
         narration="So who are these millionaire households? {p} Among households aged sixty-five and older with a net worth of at least a million dollars, the one in the middle is worth about two point seven million. {p} About ninety-seven percent own their home, with about six hundred thousand dollars in home equity. {pp} For the typical one, the house is roughly a fifth of their wealth, not most of it."),
    dict(act=5, type="stats", title="Millionaire households 65+: where the money is", src=OURS,
         stats=[dict(at="five hundred and thirty-two thousand", value=M["ret_med"], fmt="usdkm", label="median in retirement accounts"), dict(at="a hundred and forty-three thousand", value=M["inc_med"], fmt="usdkm", label="median yearly income")],
         narration="Their typical retirement accounts hold about five hundred and thirty-two thousand dollars, and their typical financial assets, including those accounts, about one point three million. And only about thirty-five percent of these millionaires have a million or more in those accounts. {p} Their typical income is about a hundred and forty-three thousand dollars a year, from pensions, Social Security, investments and, for some, work. {pp} In other words, most millionaire retirees didn't get there with one giant 401(k). They got there with several pieces adding up. {p} Some in a 401(k) or IRA, some in a regular brokerage account, some in a business or rental property, plus Social Security, and often a pension. That's also why the averages in headlines can be so misleading."),

    # ---------------- 6 · WHAT $1 MILLION BUYS ----------------
    dict(act=6, type="stats", title="What $1 million buys, by the 4% rule", src="4% rule of thumb (Bengen, 1994): first-year withdrawal of 4% of savings, adjusted for inflation afterward · illustration, not advice",
         stats=[dict(at="forty thousand dollars", value=40000, fmt="usdkm", label="first-year withdrawal from $1M"), dict(at="about thirty-three hundred", value=3333, fmt="usd0", label="per month, before taxes")],
         narration="And what does a million dollars actually buy? {p} A common rule of thumb, the four percent rule, says you can withdraw about four percent in the first year, then adjust for inflation. {p} On a million dollars, that's about forty thousand dollars a year, or about thirty-three hundred a month, before taxes. {pp} Add Social Security on top, and for many households that's a comfortable retirement. {p} But it's a far cry from the image of a millionaire. A million dollars buys security, not luxury. {p} And remember, Social Security can add hundreds of thousands of dollars over a retirement, even though it's not counted in any of these numbers."),
    dict(act=6, type="host", bg="none",
         narration="So, how many retirees really have a million dollars? {p} Counting everything: about one in three. {p} Without the house: about one in four. {p} In retirement accounts alone: about one in nine. {pp} If you're not in any of those groups, you're in the majority. And if you are, now you know exactly how rare your position is. {p} Tell me in the comments: which way of counting do you think is the fairest?",
         items=[dict(at="Counting everything", text="Everything: ~1 in 3", color="acc"), dict(at="Without the house", text="Without the house: ~1 in 4", color="acc2"), dict(at="In retirement accounts alone", text="401(k)s & IRAs: ~1 in 9", color="acc"), dict(at="which way of counting", text="Which count is fairest?", serif=True, size=56)]),
    dict(act=6, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="$431k", color="acc", title="Net worth at 55, 65 and 75: where do you rank?", sub="The full ladder"),
         narration="To see the full net worth ladder for your age group, from the bottom ten percent to the top, watch this next. {p} This is Nest Egg Atlas. See you next time.",
         hold=14),
]

snapshot = []
for b in ["all", "55-64", "65-74", "75+", "65+"]:
    k = b.replace("+", "p").replace("-", "_")
    snapshot += [dict(set="s1", iso=k, year=2025, value=S1(b), src=OURS), dict(set="sr", iso=k, year=2025, value=SR(b), src=OURS)]
    if b != "all":
        snapshot += [dict(set="sx", iso=k, year=2025, value=SX(b), src=OURS), dict(set="sf", iso=k, year=2025, value=SF(b), src=OURS), dict(set="nwx50", iso=k, year=2025, value=B[b]["nwx_pct"]["50"], src=OURS)]
snapshot += [dict(set="s1", iso="45_54", year=2025, value=S1("45-54"), src=OURS), dict(set="s1", iso="u35", year=2025, value=S1("<35"), src=OURS)]
snapshot += [dict(set="hh", iso="65p", year=2025, value=HH65, src=OURS)] + [dict(set="mill", iso=k, year=2025, value=float(v), src=OURS) for k, v in M.items()]

C = lambda say, st, iso, lo, hi: dict(say=say, set=st, iso=iso, year=2025, min=lo, max=hi)
checks = [
    C("about 40 million households 65+", "hh", "65p", 38e6, 42e6),
    C("65+ millionaires ≈ 32% (everything)", "s1", "65p", 31.5, 32.9), C("65+ without house ≈ 23%", "sx", "65p", 22.5, 23.9),
    C("65+ savings & investments ≈ 18%", "sf", "65p", 17.5, 19.4), C("65+ retirement accounts ≈ 11%", "sr", "65p", 10.5, 11.9),
    C("all ages ≈ 22%", "s1", "all", 21.0, 22.4), C("55–64 ≈ 32%", "s1", "55_64", 31.5, 32.9), C("65–74 ≈ 31%", "s1", "65_74", 30.5, 31.4), C("75+ ≈ 34%", "s1", "75p", 33.0, 34.4),
    C("45–54 ≈ 24%", "s1", "45_54", 23.0, 24.4), C("under 35 < 2%", "s1", "u35", 0, 1.99),
    C("55–64 savings ≈ 19%", "sf", "55_64", 18.5, 19.4), C("65–74 savings ≈ 17%", "sf", "65_74", 16.5, 17.4), C("75+ savings ≈ 20%", "sf", "75p", 19.5, 20.4),
    C("millionaires 65+: financial assets ≈ $1.3M", "mill", "fin_med", 1.25e6, 1.35e6),
    dict(say="≈ 13 million households 65+ with $1M+", rule="expr", expr=f"round({HH65} * {S1('65+')} / 100 / 1e6)", equal=13),
    C("55–64 without house ≈ 25%", "sx", "55_64", 24.5, 25.9), C("65–74 without house ≈ 23%", "sx", "65_74", 22.5, 23.9), C("75+ without house ≈ 23%", "sx", "75p", 22.5, 23.4),
    C("median without house 65+ ≈ $160k", "nwx50", "65p", 155000, 165000), C("median without house 55–64 ≈ $150k", "nwx50", "55_64", 145000, 155000),
    C("all ages $1M in accounts ≈ 7%", "sr", "all", 6.5, 7.4), C("55–64 ≈ 12%", "sr", "55_64", 11.5, 12.9), C("65–74 ≈ 11.5%", "sr", "65_74", 11.2, 11.8), C("75+ ≈ 11%", "sr", "75p", 10.5, 11.4),
    dict(say="about one in nine (11–12%)", rule="expr", expr="round(100 / 11.3)", equal=9),
    C("millionaires 65+: median NW ≈ $2.7M", "mill", "nw_med", 2.65e6, 2.75e6), C("97% own home", "mill", "home_share", 0.965, 0.979),
    C("median home equity ≈ $600k", "mill", "homeeq_med", 590000, 610000), C("house ≈ a fifth of wealth (median share)", "mill", "home_pct_of_nw_med", 0.18, 0.25),
    C("median retirement accounts ≈ $532k", "mill", "ret_med", 530000, 534000), C("≈ 35% have $1M+ in accounts", "mill", "ret1m_share", 0.34, 0.36),
    C("median income ≈ $143k", "mill", "inc_med", 142000, 144000),
    dict(say="house matters most for 75+: drop everything→without house largest", rule="expr", expr=f"({S1('75+')} - {SX('75+')}) > ({S1('55-64')} - {SX('55-64')}) and ({S1('75+')} - {SX('75+')}) > ({S1('65-74')} - {SX('65-74')})", equal=True),
    dict(say="401(k) created by the Revenue Act of 1978, spread in the 1980s", rule="expr", expr="1978 < 1985", equal=True),
    dict(say="4% of $1M = $40k; /12 ≈ $3,333", rule="expr", expr="[1_000_000 * 0.04, round(40000 / 12)]", equal=[40000.0, 3333]),
]

clips = [
    dict(**{"from": "s00", "to": "s00"}, hook="How many retirees have *$1 million?*", title="How many retirees really have $1 million? It depends #Shorts", desc="Households 65+ (Federal Reserve, 2025 SCF): everything ~32%, without the house ~23%, savings ~18%, 401(k)/IRA ~11%."),
    dict(**{"from": "s08", "to": "s08"}, hook="The million-dollar 401(k) is *rare*", title="Only 1 in 9 retirees has $1M in a 401(k) or IRA #Shorts", desc="Federal Reserve 2025 Survey of Consumer Finances, our calculation with survey weights."),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="b-N02-million", clips=clips, channel="nesteggatlas", chapter0="The question", host=False,
            thumb=dict(kind="text", top="RETIREES WITH $1 MILLION", big="1 in 3", line2="OR 1 IN 9?", sticker="NEW FED DATA"),
            w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks, datasets=[], snapshot=snapshot,
            voice=dict(model="", name="Algieba",
                       style=("You are the narrator of a calm, trustworthy personal-finance documentary for Americans in their fifties, sixties and seventies. "
                              "Read the script below in a warm, mature, unhurried voice, at about 138 words per minute, like a respected public-radio journalist "
                              "explaining numbers to a friend. Let each dollar figure land with a short pause before it. Sound reassuring and clear, never salesy, "
                              "never alarmed, never like an advertisement.")),
            music=[dict(act=0, track="Lightless Dawn", vol=0.18), dict(act=1, track="Deliberate Thought", vol=0.17), dict(act=2, track="Investigations", vol=0.17),
                   dict(act=3, track="Inspired", vol=0.17), dict(act=4, track="Floating Cities", vol=0.17), dict(act=5, track="Deliberate Thought", vol=0.17), dict(act=6, track="Inspired", vol=0.18)],
            yt=dict(title="How Many Retirees Actually Have $1 Million? (New Fed Data)",
                    description=("How many American retirees really have a million dollars? It depends on what you count. Using the Federal Reserve's 2025 Survey of Consumer Finances, "
                                 "we calculate the share of households aged 55–64, 65–74 and 75+ with $1 million or more: counting everything, without the house, in savings and investments, "
                                 "and in 401(k)s and IRAs alone. Plus a profile of the typical millionaire retiree household and what $1 million buys under the 4% rule.\n\n"
                                 "Educational content, not financial advice.\n\n"
                                 "Sources: Federal Reserve Board, 2025 Survey of Consumer Finances, summary extract public data (our calculation with survey weights; all figures in 2025 dollars); "
                                 "Bengen (1994), 4% rule of thumb.\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#retirement #millionaire #401k #personalfinance #retirementplanning"),
                    tags=["retirement", "how many retirees have 1 million", "millionaire retirees", "federal reserve", "survey of consumer finances", "401k", "net worth", "4% rule", "retirement savings", "personal finance"], lang="en"))

json.dump(spec, open(os.path.join(HERE, "b-N02.json"), "w"), ensure_ascii=False, indent=1)
clean = lambda t: t.replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()
words = sum(len(clean(s["narration"])) for s in shots)
acts = {}
for s in shots:
    acts[s["act"]] = acts.get(s["act"], 0) + len(clean(s["narration"]))
print("shots", len(shots), "palavras", words, f"~{words / 138:.1f} min a 138 wpm", "por ato", acts)

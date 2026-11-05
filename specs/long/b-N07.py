"""Gera specs/long/b-N07.json — Nest Egg Atlas (canal B) longo: quanto o Social Security paga com salário de $40k, $60k e $100k.
Dados oficiais (lidos em 05/11/2026 no navegador): SSA OACT bend points 2027 ($1.340 / $8.077; ssa.gov/oact/cola/bendpoints.html),
AWI 2025 = 72.800,33 e AWI 1990 = 21.027,98 (ssa.gov/oact/cola/AWI.html), teto de contribuição 2027 = $192.300 (ssa.gov/oact/cola/cbb.html),
2027 COLA Fact Sheet (benefício médio do aposentado $2.170; máximo na FRA $4.188). Conta = fórmula do PIA aplicada por nós: carreira de 35 anos
com salário constante em termos de salário médio (ganhos indexados = salário de hoje), elegível em 2027 (62 anos em 2027, FRA 67).
Arredondamentos da SSA: AIME para baixo no dólar, PIA para baixo no centavo de 10, benefício reduzido/aumentado para baixo no dólar."""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
B1, B2, CAP, AWI25, AWI90, AVG, MAXFRA = 1340, 8077, 192300, 72800.33, 21027.98, 2170, 4188
SSA = "Social Security Administration, Office of the Chief Actuary: 2027 PIA bend points, national average wage index, contribution and benefit base"
OURS = "Nest Egg Atlas calculation with the SSA benefit formula (2027 bend points) · turning 62 in 2027 · 35-year career · salary in today's wages"
ACTS = ["Cold open", "The formula", "Working it out", "What it replaces", "Claiming age", "The 35-year rule", "Where you stand"]


def aime(salary, years=35):
    return math.floor(salary * years / 35 / 12)


def pia(salary, years=35):
    a = aime(salary, years)
    v = 0.9 * min(a, B1) + 0.32 * max(min(a, B2) - B1, 0) + 0.15 * max(a - B2, 0)
    return math.floor(round(v * 10, 6)) / 10


def at(salary, factor):
    return math.floor(pia(salary) * factor)


R = lambda s: round(pia(s) * 12 / s * 100, 1)


def cue(bars, ats):
    for b, a in zip(bars, ats):
        b["at"] = a
    return bars


shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="rank", title="Social Security at full retirement age", sub="Monthly check by career salary · turning 62 in 2027", fmt="usd0", count=False, vmax=3600, src=OURS,
         bars=cue([dict(label="$40,000 salary", value=pia(40000)), dict(label="$60,000 salary", value=pia(60000)), dict(label="$100,000 salary", value=pia(100000), hl=True)],
                  ["forty thousand dollars a year", "Sixty thousand a year", "A hundred thousand a year"]),
         narration="Here's what Social Security pays at three different salaries, using the official formula for people turning sixty-two in 2027. {p} Someone who earned forty thousand dollars a year: about eighteen hundred and forty-four dollars a month, at full retirement age. {p} Sixty thousand a year: about two thousand three hundred and seventy-seven. {p} A hundred thousand a year: about three thousand four hundred. {pp} Notice something. The hundred-thousand-dollar earner made two and a half times as much as the forty-thousand-dollar earner. But their check is less than twice as big. {p} That's not an accident. It's built into the formula, and once you see how it works, you can estimate your own check in about a minute."),
    dict(act=0, type="host", bg="none",
         narration="Social Security published the new numbers for 2027 last month: the formula's bend points, the national wage index, and the cost-of-living adjustment. {p} In this video, we'll go through how the formula works, what it pays at different salaries, how much your claiming age changes it, and the one rule that quietly lowers a lot of people's checks. {p} Every number comes from Social Security's own published figures, and you can plug in your own salary as we go. {pp} <soft>As always, this is education, not financial advice.</soft>",
         items=[dict(at="the new numbers for 2027", text="The 2027 formula", color="acc"), dict(at="different salaries", text="Salary → monthly check", color="acc2"), dict(at="quietly lowers", text="The 35-year rule", serif=True, size=62)]),

    # ---------------- 1 · THE FORMULA ----------------
    dict(act=1, type="list", title="The 2027 benefit formula", src=SSA,
         narration="Here's the formula itself. It starts with one number: your average monthly earnings over your thirty-five best years. Social Security calls it your AIME. {p} Then it pays you ninety percent of the first thirteen hundred and forty dollars of that monthly average. {p} Thirty-two percent of the part between thirteen hundred and forty and eight thousand and seventy-seven dollars. {p} And fifteen percent of anything above eight thousand and seventy-seven. {pp} The result is your full benefit at full retirement age, which is sixty-seven for anyone born in 1960 or later. Those two dollar amounts are called bend points, and they rise every year with average wages.",
         items=[dict(at="your thirty-five best years", kind="title", text="START: MONTHLY AVERAGE OF YOUR BEST 35 YEARS"),
                dict(at="ninety percent of the first", kind="bullet", text="90% of the first $1,340"),
                dict(at="Thirty-two percent of the part", kind="bullet", text="32% from $1,340 to $8,077"),
                dict(at="fifteen percent of anything above", kind="bullet", text="15% above $8,077"),
                dict(at="sixty-seven for anyone born", kind="bullet", text="= your benefit at 67 (born 1960+)")]),
    dict(act=1, type="host", bg="none",
         narration="Two details matter here. {p} First, your old earnings are adjusted for wage growth. A salary of twenty thousand dollars in 1990 counts like about sixty-nine thousand today, because average wages have risen that much since then. So the formula compares your career with today's pay, not with old prices. {p} Second, there's a cap. In 2027, earnings above a hundred and ninety-two thousand three hundred dollars aren't taxed for Social Security, and they don't count toward your benefit either.",
         items=[dict(at="twenty thousand dollars in 1990", text="$20k in 1990 ≈ $69k today", color="acc"), dict(at="there's a cap", text="2027 cap: $192,300", color="acc2")]),

    # ---------------- 2 · WORKING IT OUT ----------------
    dict(act=2, type="list", title="Example: $60,000 a year for 35 years", src=OURS,
         narration="Let's work one through. Take someone who earned sixty thousand dollars a year, in today's wages, for thirty-five years. {p} Their monthly average is five thousand dollars. {p} Ninety percent of the first thirteen hundred and forty is twelve hundred and six dollars. {p} The rest, thirty-six hundred and sixty dollars, falls in the thirty-two percent bracket. That adds eleven hundred and seventy-one dollars and twenty cents. {p} Nothing is above the second bend point, so that's it. {pp} Total: about two thousand three hundred and seventy-seven dollars a month, at sixty-seven.",
         items=[dict(at="Their monthly average", kind="bullet", text="$60,000 ÷ 12 = $5,000 a month"),
                dict(at="Ninety percent of the first", kind="bullet", text="90% × $1,340 = $1,206"),
                dict(at="The rest, thirty-six hundred", kind="bullet", text="32% × $3,660 = $1,171.20"),
                dict(at="Total: about", kind="title", text="= $2,377 A MONTH AT 67")]),
    dict(act=2, type="host", bg="none",
         narration="Do the same for forty thousand dollars a year: a monthly average of about three thousand three hundred and thirty-three, and a check of about eighteen hundred and forty-four. {p} And for a hundred thousand: a monthly average of about eight thousand three hundred and thirty-three. Only about two hundred and fifty-six dollars of that is above the second bend point, and it's paid at fifteen percent. The check comes to about thirty-four hundred dollars. {p} Above that second bend point, each extra dollar of monthly average earnings adds just fifteen cents to the check.",
         items=[dict(at="Do the same for forty thousand", text="$40k → $1,844", color="acc2"), dict(at="And for a hundred thousand", text="$100k → $3,400", color="acc"), dict(at="just fifteen cents", text="Above $8,077: 15¢ per $1", serif=True, size=60)]),

    # ---------------- 3 · WHAT IT REPLACES ----------------
    dict(act=3, type="rank", title="Share of salary Social Security replaces", sub="At full retirement age · 35-year career · 2027 formula", fmt="pct0", count=False, vmax=90, src=OURS,
         bars=cue([dict(label="$20,000", value=R(20000), hl=True), dict(label="$40,000", value=R(40000)), dict(label="$60,000", value=R(60000)), dict(label="$100,000", value=R(100000))],
                  ["At twenty thousand dollars a year", "At forty thousand, about fifty-five", "At sixty thousand, about forty-eight", "At a hundred thousand, about forty-one"]),
         narration="Now compare each check with the salary behind it. {p} At twenty thousand dollars a year, Social Security replaces about seventy-nine percent of your pay. {p} At forty thousand, about fifty-five percent. {p} At sixty thousand, about forty-eight percent. {p} At a hundred thousand, about forty-one percent. {pp} That's the design: Social Security replaces a much bigger share of a smaller paycheck. {p} Double a salary from forty to eighty thousand, and the check rises by only about fifty-eight percent, from about eighteen hundred and forty-four dollars to about twenty-nine hundred and ten."),
    dict(act=3, type="host", bg="none",
         narration="That's also why the famous thirty-five-hundred-dollar check is harder to reach than it sounds. {p} To get thirty-five hundred dollars a month at full retirement age, you'd need to have earned about a hundred and eight thousand dollars a year, in today's wages, for thirty-five years. {p} And the maximum benefit for someone retiring at full retirement age in 2027, after a whole career at or above the cap, is four thousand one hundred and eighty-eight dollars a month. {p} In other words, for lower earners Social Security does most of the work in retirement. For higher earners, it's more of a base layer, and savings, pensions and 401(k)s have to carry much more of the load.",
         items=[dict(at="thirty-five-hundred-dollar check", text="$3,500 a month?", serif=True, size=64), dict(at="a hundred and eight thousand", text="≈ $108k a year × 35 years", color="acc"), dict(at="four thousand one hundred and eighty-eight", text="2027 max at full age: $4,188", color="acc2")]),

    # ---------------- 4 · CLAIMING AGE ----------------
    dict(act=4, type="rank", title="$60,000 career: monthly check by claiming age", sub="2027 formula · full retirement age 67", fmt="usd0", count=False, vmax=3200, src=OURS,
         bars=cue([dict(label="Claim at 62", value=at(60000, 0.70)), dict(label="Claim at 67", value=pia(60000)), dict(label="Claim at 70", value=at(60000, 1.24), hl=True)],
                  ["Claim at sixty-two", "At sixty-seven, about two thousand", "Wait until seventy"]),
         narration="Those are the checks at sixty-seven. But you can claim as early as sixty-two, or as late as seventy. {p} Claim at sixty-two, and the check is cut by thirty percent, for life. For the sixty-thousand-dollar earner, that's about sixteen hundred and sixty-four dollars a month. {p} At sixty-seven, about two thousand three hundred and seventy-seven. {p} Wait until seventy, and you get eight percent more for every year past sixty-seven: twenty-four percent in total. About two thousand nine hundred and forty-seven. {pp} For the forty-thousand-dollar earner, that's about twelve hundred and ninety at sixty-two, and about twenty-two hundred and eighty-six at seventy. For the hundred-thousand-dollar earner, about twenty-three hundred and eighty, and about forty-two hundred and sixteen."),
    dict(act=4, type="host", bg="none",
         narration="If you're married, there's one more number. A spouse with a small work record can get up to half of the other spouse's full benefit, if they claim at their own full retirement age. {p} For the hundred-thousand-dollar earner, that's up to about seventeen hundred dollars a month for the spouse. {p} And when one spouse dies, the survivor keeps the larger of the two checks.",
         items=[dict(at="up to half", text="Spouse: up to 50%", color="acc"), dict(at="seventeen hundred dollars", text="$100k earner → up to $1,700", color="acc2"), dict(at="the survivor keeps", text="Survivor keeps the larger check", serif=True, size=58)]),

    # ---------------- 5 · THE 35-YEAR RULE ----------------
    dict(act=5, type="rank", title="$60,000 a year, different career lengths", sub="Monthly check at 67 · missing years count as zero", fmt="usd0", count=False, vmax=2600, src=OURS,
         bars=cue([dict(label="35 years", value=pia(60000, 35)), dict(label="30 years", value=pia(60000, 30)), dict(label="25 years", value=pia(60000, 25), hl=True)],
                  ["a full thirty-five years", "With only thirty years", "With twenty-five years"]),
         narration="Now, the rule that quietly lowers a lot of checks. {p} The formula always averages thirty-five years. If you worked fewer, the missing years count as zero. {p} Our sixty-thousand-dollar earner, with a full thirty-five years, gets about two thousand three hundred and seventy-seven a month. {p} With only thirty years of earnings, about two thousand one hundred and forty-eight. {p} With twenty-five years, about nineteen hundred and twenty. That's about four hundred and fifty-seven dollars a month less, for life. {pp} This is common for anyone who took years off to raise children, care for a parent, or go back to school."),
    dict(act=5, type="host", bg="none",
         narration="The good news: it works in reverse, too. If you have fewer than thirty-five years, every extra year you work replaces a zero, even a part-time year. And a strong year late in your career can replace a weak year from your twenties. {p} You can see every year of your record at ssa.gov, in your my Social Security account. Check it for missing years. If wages are missing, you can ask Social Security to fix them, but there are time limits, so it's worth checking now, not at sixty-two.",
         items=[dict(at="replaces a zero", text="Each extra year replaces a zero", color="acc"), dict(at="my Social Security account", text="Check your record: ssa.gov", color="acc2"), dict(at="time limits", text="Fix errors early", serif=True, size=62)]),

    # ---------------- 6 · WHERE YOU STAND ----------------
    dict(act=6, type="list", title="Quick estimate at 67 (2027 formula)", src=OURS,
         narration="So here's the quick ladder, at full retirement age, for a full thirty-five-year career. {p} Twenty thousand a year: about thirteen hundred and ten dollars a month. {p} Forty thousand: about eighteen hundred and forty-four. {p} Sixty thousand: about twenty-three hundred and seventy-seven. {p} Seventy-two thousand eight hundred, the national average wage for 2025: about twenty-seven hundred and eighteen. {p} A hundred thousand: about thirty-four hundred. {pp} For comparison, the average retired worker's check in 2027 is about two thousand one hundred and seventy dollars. These estimates are before taxes, and before the Medicare premium most people have taken out of their check. The real formula uses your exact earnings, year by year.",
         items=[dict(at="Twenty thousand a year", kind="bullet", text="$20k → about $1,310"),
                dict(at="Forty thousand: about", kind="bullet", text="$40k → about $1,844"),
                dict(at="Sixty thousand: about", kind="bullet", text="$60k → about $2,377"),
                dict(at="Seventy-two thousand eight hundred", kind="bullet", text="$72.8k (average wage) → about $2,718"),
                dict(at="A hundred thousand: about", kind="bullet", text="$100k → about $3,400"),
                dict(at="before taxes", kind="title", text="BEFORE TAXES AND MEDICARE · 35 YEARS · TODAY'S WAGES")]),
    dict(act=6, type="host", bg="none",
         narration="Tell me in the comments: is your estimate higher or lower than you expected? {p} And if you've already claimed, I'd like to know: at what age, and would you choose the same again? {p} And if you know someone in their fifties who has never looked at their Social Security record, send them this. Ten minutes on ssa.gov now can catch a costly mistake later.",
         items=[dict(at="higher or lower", text="Higher or lower?", serif=True, size=66), dict(at="at what age", text="62 · 67 · 70?", color="acc")]),
    dict(act=6, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="AGE 80", color="acc", title="Social Security at 62, 67 or 70?", sub="The break-even ages"),
         narration="Now that you know your number, the next question is when to claim it. To see the break-even ages, watch this next. {p} This is Nest Egg Atlas. See you next time.",
         hold=14),
]

snapshot = [dict(set="ssa", iso=k, year=2027, value=v, src=SSA) for k, v in [("bend1", B1), ("bend2", B2), ("cap", CAP), ("awi2025", AWI25), ("avg", AVG), ("maxfra", MAXFRA)]]
snapshot += [dict(set="pia", iso=f"s{s // 1000}k", year=2027, value=pia(s), src=OURS) for s in (20000, 40000, 60000, 72800, 80000, 100000)]

E = lambda say, expr, eq: dict(say=say, rule="expr", expr=expr, equal=eq)
checks = [
    E("bend points 2027 = $1,340 / $8,077 (SSA OACT)", "[1340, 8077]", [B1, B2]),
    E("$40k → AIME 3,333 → PIA 1,843.70 (≈ $1,844)", f"[{aime(40000)}, {pia(40000)}]", [3333, 1843.7]),
    E("$60k → AIME 5,000 → PIA 2,377.20", f"[{aime(60000)}, {pia(60000)}]", [5000, 2377.2]),
    E("$100k → AIME 8,333 → PIA 3,400.20 (≈ $3,400)", f"[{aime(100000)}, {pia(100000)}]", [8333, 3400.2]),
    E("100k/40k = 2.5×; check ratio < 2", f"[100000 / 40000, {pia(100000)} / {pia(40000)} < 2]", [2.5, True]),
    E("FRA 67 for born 1960+", "67", 67),
    E("$20k in 1990 indexed to AWI 2025 ≈ $69k", f"round(20000 * {AWI25} / {AWI90} / 1000)", 69),
    E("taxable max 2027 = $192,300", "192300", CAP),
    E("$60k: 0.9×1340 = 1206; 5000−1340 = 3660; ×0.32 = 1171.20", "[round(0.9 * 1340, 2), 5000 - 1340, round(0.32 * 3660, 2)]", [1206.0, 3660, 1171.2]),
    E("$100k: 8333 − 8077 = 256 above bend 2", f"{aime(100000)} - 8077", 256),
    E("replacement: 20k ≈ 79%, 40k ≈ 55%, 60k ≈ 48%, 100k ≈ 41%", f"[round({R(20000)}), round({R(40000)}), round({R(60000)}), round({R(100000)})]", [79, 55, 48, 41]),
    E("$80k → ≈ $2,910 (+58% vs $40k)", f"[round({pia(80000)}), round(({pia(80000)} / {pia(40000)} - 1) * 100)]", [2910, 58]),
    E("$3,500 at FRA needs ≈ $108k salary", f"[{pia(107000)} < 3500, {pia(108000)} >= 3500]", [True, True]),
    E("max at FRA 2027 = $4,188 (COLA fact sheet)", "4188", MAXFRA),
    E("$60k at 62 / 67 / 70 = 1,664 / 2,377 / 2,947", f"[{at(60000, 0.7)}, round({pia(60000)}), {at(60000, 1.24)}]", [1664, 2377, 2947]),
    E("$40k at 62 / 70 = 1,290 / 2,286", f"[{at(40000, 0.7)}, {at(40000, 1.24)}]", [1290, 2286]),
    E("$100k at 62 / 70 = 2,380 / 4,216", f"[{at(100000, 0.7)}, {at(100000, 1.24)}]", [2380, 4216]),
    E("spouse up to 50% of $3,400 ≈ $1,700", f"round({pia(100000)} / 2)", 1700),
    E("$60k for 30 / 25 years = 2,148 / 1,920; −$457", f"[round({pia(60000, 30)}), round({pia(60000, 25)}), round({pia(60000)} - {pia(60000, 25)})]", [2148, 1920, 457]),
    E("$20k → ≈ $1,310", f"round({pia(20000)})", 1310),
    E("AWI 2025 = 72,800.33 → ≈ $2,718", f"round({pia(72800.33)})", 2718),
    E("average retired worker 2027 = $2,170", "2170", AVG),
]

clips = [
    dict(**{"from": "s00", "to": "s00"}, hook="Social Security at *$40k, $60k, $100k*", title="Social Security at a $40k, $60k or $100k salary (2027 formula) #Shorts", desc="2027 SSA formula, turning 62 in 2027, 35-year career, full retirement age 67: $40k ≈ $1,844, $60k ≈ $2,377, $100k ≈ $3,400 a month. Education, not financial advice."),
    dict(**{"from": "s10", "to": "s10"}, hook="The rule that *shrinks* your check", title="Fewer than 35 years of work? Your Social Security drops #Shorts", desc="$60k a year: 35 years ≈ $2,377, 30 years ≈ $2,148, 25 years ≈ $1,920 a month (2027 SSA formula, our calculation)."),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="b-N07-ss-salary", clips=clips, channel="nesteggatlas", chapter0="Three salaries", host=False,
            thumb=dict(kind="text", top="ON A $60k SALARY:", big="$2,377", line2="A MONTH AT 67", sticker="SOCIAL SECURITY 2027"),
            w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks, datasets=[], snapshot=snapshot,
            voice=dict(model="", name="Algieba",
                       style=("You are the narrator of a calm, trustworthy personal-finance documentary for Americans in their fifties, sixties and seventies. "
                              "Read the script below in a warm, mature, unhurried voice, at about 135 words per minute, like a respected public-radio journalist "
                              "explaining numbers to a friend. Take your time with every dollar figure and let it land with a short pause before it. "
                              "Sound reassuring and clear, never rushed, never salesy, never alarmed, never like an advertisement.")),
            music=[dict(act=0, track="Lightless Dawn", vol=0.18), dict(act=1, track="Deliberate Thought", vol=0.17), dict(act=2, track="Investigations", vol=0.17),
                   dict(act=3, track="Inspired", vol=0.17), dict(act=4, track="Floating Cities", vol=0.17), dict(act=5, track="Deliberate Thought", vol=0.17), dict(act=6, track="Inspired", vol=0.18)],
            yt=dict(title="How Much Social Security on a $40k, $60k or $100k Salary? (2027 Formula)",
                    description=("What does Social Security actually pay at different salaries? Using the official 2027 benefit formula (bend points $1,340 and $8,077), "
                                 "we work out the monthly check at full retirement age for a 35-year career at $20k, $40k, $60k, the national average wage and $100k, "
                                 "how much of your pay it replaces, what changes if you claim at 62 or 70, spousal benefits, and the 35-year rule.\n\n"
                                 "Assumptions: turning 62 in 2027 (full retirement age 67), 35 years of earnings at the same level relative to national average wages "
                                 "(salary in today's wages), before taxes and Medicare premiums. Your own estimate: your my Social Security account at ssa.gov.\n\n"
                                 "Educational content, not financial advice.\n\n"
                                 "Sources: Social Security Administration, Office of the Chief Actuary — PIA formula bend points, national average wage index (2025: $72,800.33), "
                                 "contribution and benefit base ($192,300 in 2027); 2027 COLA Fact Sheet. Calculations: Nest Egg Atlas.\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#socialsecurity #retirement #retirementplanning #personalfinance #socialsecurity2027"),
                    tags=["social security", "how much social security will i get", "social security calculator", "social security benefit formula", "bend points 2027",
                          "social security by salary", "full retirement age", "35 years social security", "retirement planning", "personal finance"], lang="en"))

json.dump(spec, open(os.path.join(HERE, "b-N07.json"), "w"), ensure_ascii=False, indent=1)
clean = lambda t: t.replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()
words = sum(len(clean(s["narration"])) for s in shots)
acts = {}
for s in shots:
    acts[s["act"]] = acts.get(s["act"], 0) + len(clean(s["narration"]))
print("shots", len(shots), "palavras", words, f"~{words / 140:.1f} min a 140 wpm", "por ato", acts)

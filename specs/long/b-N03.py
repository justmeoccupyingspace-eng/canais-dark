"""Gera specs/long/b-N03.json — Nest Egg Atlas (canal B) longo #3: Social Security aos 62, 67 ou 70.
Dados oficiais da SSA, lidos em 03/11/2026:
- 2027 COLA Fact Sheet (ssa.gov/news/en/cola/factsheets/2027.html): COLA 3,6%; benefício médio do aposentado US$ 2.095 → 2.170;
  máximo na idade plena US$ 4.188; teste de rendimentos US$ 25.560/ano (US$ 1 retido a cada US$ 2).
- Annual Statistical Supplement 2026, tabela 6.B5.1 (idade na concessão, homens e mulheres, 1998–2025) → média ponderada nossa.
- Actuarial Life Table: tábua de período 2023 da área do Social Security, usada no Trustees Report 2026 (ssa.gov/oact/STATS/table4c6.html).
- Regras: redução 5/9 de 1% por mês nos 36 primeiros meses e 5/12 de 1% além disso; créditos de 2/3 de 1% por mês até 70 (nascidos em 1943+);
  idade plena 67 para nascidos em 1960+; viúvo(a) com limite mínimo de 82,5% do PIA quando o falecido pediu antes (RIB-LIM).
Contas de ponto de equilíbrio, totais e probabilidades = cálculo nosso (sem impostos, sem juros, mesmo COLA para todas as idades)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SSA = "Social Security Administration"
OURS = "Nest Egg Atlas calculation with " + SSA + " benefit formulas (full retirement age 67) · today's dollars, before taxes"
LT = SSA + " Office of the Chief Actuary, 2023 period life table (used in the 2026 Trustees Report) · Nest Egg Atlas calculation"
SUPP = SSA + ", Annual Statistical Supplement 2026, Table 6.B5.1 (retired-worker awards by age at entitlement) · men and women combined by Nest Egg Atlas"
COLA = SSA + ", 2027 COLA Fact Sheet (October 2026)"
ACTS = ["Cold open", "The rules", "What people actually do", "The break-even", "The odds", "The survivor", "So when?"]

PIA = 2000
F62, F70 = 1 - (36 * 5 / 9 + 24 * 5 / 12) / 100, 1 + 36 * (2 / 3) / 100  # 0.70 e 1.24
B62, B70 = round(PIA * F62), round(PIA * F70)
be = lambda fa, aa, fb, ab: (fb * ab - fa * aa) / (fb - fa)  # idade em que o total pago se iguala
BE6267, BE6270, BE6770 = be(F62, 62, 1.0, 67), be(F62, 62, F70, 70), be(1.0, 67, F70, 70)
tot = lambda monthly, start, upto: monthly * 12 * (upto - start)
T80 = {a: tot(b, a, 80) for a, b in [(62, B62), (67, PIA), (70, B70)]}
T90 = {a: tot(b, a, 90) for a, b in [(62, B62), (67, PIA), (70, B70)]}

# SSA 2023 period life table: número de vivos (de 100.000) por idade exata
LX_M = {62: 82563, 67: 76416, 78: 56024, 79: 53477, 80: 50785, 81: 47960, 82: 44998, 83: 41922}
LX_F = {62: 89767, 67: 85567, 78: 69387, 79: 67087, 80: 64606, 81: 61946, 82: 59099, 83: 56068}
EX62 = {"M": 20.29, "F": 23.08}
def lx(tab, age):
    a = int(age)
    return tab[a] - (age - a) * (tab[a] - tab[a + 1])
P_M = lx(LX_M, BE6270) / LX_M[62]
P_F = lx(LX_F, BE6270) / LX_F[62]
P_ANY = 1 - (1 - P_M) * (1 - P_F)
P67_M = lx(LX_M, BE6770) / LX_M[67]
P67_F = lx(LX_F, BE6770) / LX_F[67]

# Tabela 6.B5.1 (milhares de concessões; % aos 62; % aos 70+)
AW = {2008: dict(m=(1191, 42.6, 0.7, 63.6), f=(1077, 48.0, 2.4, 63.6)), 2024: dict(m=(1866, 22.0, 8.7, 65.3), f=(1847, 23.1, 10.0, 65.3))}
def comb(y, k):
    m, f = AW[y]["m"], AW[y]["f"]
    return (m[0] * m[k] + f[0] * f[k]) / (m[0] + f[0])
S62 = {y: comb(y, 1) for y in AW}
S70 = {y: comb(y, 2) for y in AW}

# viúvo(a): maior benefício do casal; se o falecido pediu cedo, mínimo de 82,5% do PIA
HI = 2800
SURV62, SURV70 = max(round(HI * F62), round(HI * 0.825)), round(HI * F70)

def cue(bars, ats):
    for b, a in zip(bars, ats):
        b["at"] = a
    return bars

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="rank", title="Monthly check, by claiming age", sub="Example: full benefit of $2,000 at 67 · today's dollars", fmt="usd0", count=False, vmax=2800, src=OURS,
         bars=cue([dict(label="Claim at 62", value=B62), dict(label="Claim at 67", value=PIA), dict(label="Claim at 70", value=B70, hl=True)],
                  ["claim at sixty-two", "full Social Security benefit", "wait until seventy"]),
         narration="Take someone whose full Social Security benefit, at sixty-seven, is two thousand dollars a month. {p} If they claim at sixty-two, the earliest age allowed, they get about fourteen hundred dollars a month, for life. {p} If they wait until seventy, they get about two thousand four hundred and eighty. {pp} That's about seventy-seven percent more every month, for waiting eight years. {p} But the early claimer collects eight years of checks first. So who comes out ahead? {p} Over a long retirement, the difference can be more than a hundred thousand dollars, in either direction. {p} It mostly comes down to one number: how long you live."),
    dict(act=0, type="host", bg="none",
         narration="In this video, we'll use Social Security's own numbers: its benefit rules, its new figures for 2027, its records of when Americans actually claim, and its life tables. {p} We'll calculate the break-even ages, the odds of reaching them, and the part most break-even math leaves out. {pp} <soft>As always, this is education, not financial advice. The benefit estimate in your own Social Security account is the number that counts.</soft>",
         items=[dict(at="Social Security's own numbers", text="SSA's own data", color="acc"), dict(at="break-even ages", text="Break-even ages", color="acc2"), dict(at="leaves out", text="+ the part most math misses", serif=True, size=56)]),

    # ---------------- 1 · THE RULES ----------------
    dict(act=1, type="list", title="The rules, if you were born in 1960 or later", src=SSA + ": early retirement reduction and delayed retirement credits",
         narration="First, the rules. {p} If you were born in 1960 or later, your full retirement age is sixty-seven. That's when you get one hundred percent of your benefit. {p} Claim earlier, and the check is cut for life: by five-ninths of one percent for each of the first thirty-six months early, and five-twelfths of one percent for each month before that. At sixty-two, that adds up to a thirty percent cut. {p} Wait past sixty-seven, and you earn delayed retirement credits: two-thirds of one percent a month, or eight percent a year. At seventy, that's twenty-four percent more. {pp} After seventy, there's nothing more to gain by waiting. {p} These rules are for your own retirement benefit. Spousal benefits follow slightly different ones.",
         items=[dict(at="full retirement age is sixty-seven", kind="bullet", text="Full retirement age: 67 → 100%"),
                dict(at="thirty percent cut", kind="bullet", text="At 62: −30%, for life"),
                dict(at="eight percent a year", kind="bullet", text="After 67: +8% a year"),
                dict(at="twenty-four percent more", kind="bullet", text="At 70: +24%"),
                dict(at="nothing more to gain", kind="title", text="AFTER 70: NO MORE CREDITS")]),
    dict(act=1, type="stats", title="Social Security in 2027", src=COLA,
         stats=[dict(at="three point six percent", value=3.6, fmt="pct1", label="cost-of-living adjustment"), dict(at="two thousand one hundred and seventy", value=2170, fmt="usd0", label="average retired worker, per month"),
                dict(at="four thousand one hundred and eighty-eight", value=4188, fmt="usd0", label="maximum at full retirement age")],
         narration="And every year, all of these checks rise with inflation. For 2027, the cost-of-living adjustment is three point six percent. {p} The average retired worker's check goes from about two thousand and ninety-five dollars a month to about two thousand one hundred and seventy: about seventy-five dollars more. {p} The maximum, for someone retiring at full retirement age, is four thousand one hundred and eighty-eight dollars a month."),

    # ---------------- 2 · WHAT PEOPLE ACTUALLY DO ----------------
    dict(act=2, type="rank", title="When new retirees start benefits", sub="Share of new retired-worker awards", fmt="pct1", count=False, vmax=50, src=SUPP,
         bars=cue([dict(label="At 62 · 2008", value=round(S62[2008], 1)), dict(label="At 62 · 2024", value=round(S62[2024], 1), hl=True),
                   dict(label="At 70+ · 2008", value=round(S70[2008], 1)), dict(label="At 70+ · 2024", value=round(S70[2024], 1), hl=True)],
                  ["In 2008, about forty-five", "By 2024", "only about one and a half", "more than nine percent"]),
         narration="So what do Americans actually choose? {p} Social Security publishes the age at which every new retiree starts benefits. {p} In 2008, about forty-five percent of new retired workers started at sixty-two, the earliest possible age. Almost half. {p} By 2024, the latest full year, that was down to about twenty-three percent. {pp} And at the other end: in 2008, only about one and a half percent waited until seventy or later. In 2024, more than nine percent. {p} The average starting age rose from about sixty-three and a half to about sixty-five and a quarter."),
    dict(act=2, type="host", bg="none",
         narration="Part of the reason is that the rules changed. Full retirement age used to be sixty-five. It rose step by step to sixty-seven, for people born in 1960 or later. Those born in 1960 are the first to reach it: they turn sixty-seven in 2027. {p} When full retirement age was sixty-five, claiming at sixty-two meant a twenty percent cut. Now it's thirty. {pp} People are also working longer. But almost one in four new retirees still claims at the very first chance. And for many of them, as we'll see, that's a reasonable choice.",
         items=[dict(at="used to be sixty-five", text="Full retirement age: 65 → 67", color="acc2"), dict(at="twenty percent cut", text="Cut at 62: 20% → 30%", color="acc"), dict(at="almost one in four", text="Still ~1 in 4 at 62", serif=True, size=58)]),

    # ---------------- 3 · THE BREAK-EVEN ----------------
    dict(act=3, type="rank", title="Break-even age", sub="Age at which the total paid is the same · our calculation", fmt="dec1", count=False, vmax=90, src=OURS,
         bars=cue([dict(label="62 vs 67", value=round(BE6267, 1)), dict(label="62 vs 70", value=round(BE6270, 1), hl=True), dict(label="67 vs 70", value=round(BE6770, 1))],
                  ["seventy-eight years and eight months", "eighty years and four months", "eighty-two and a half"]),
         narration="Now the break-even math. {p} Compare claiming at sixty-two with claiming at sixty-seven. The early claimer starts five years sooner, but with a check thirty percent smaller. The total paid catches up at about seventy-eight years and eight months. {p} Sixty-two versus seventy: about eighty years and four months. {p} Sixty-seven versus seventy: about eighty-two and a half. {pp} Live past those ages, and waiting paid more in total. Die before them, and claiming earlier did. {p} These ages are the same whatever your benefit is, because every check rises with the same cost-of-living adjustment. We left out taxes and investment returns, which can move them a little."),
    dict(act=3, type="rank", title="Total collected by age 90", sub="Example: $2,000 at 67 · today's dollars", fmt="usdkm", count=False, vmax=650000, src=OURS,
         bars=cue([dict(label="Claim at 62", value=T90[62]), dict(label="Claim at 67", value=T90[67]), dict(label="Claim at 70", value=T90[70], hl=True)],
                  ["four hundred and seventy thousand", "five hundred and fifty thousand", "five hundred and ninety-five thousand"]),
         narration="In dollars, with our example: by age eighty, the three choices are almost tied, at about three hundred thousand dollars each. {p} By ninety, the gap opens up. Claiming at sixty-two pays about four hundred and seventy thousand in total. At sixty-seven, about five hundred and fifty thousand. At seventy, about five hundred and ninety-five thousand. {pp} That's about a hundred and twenty-five thousand dollars more for the person who waited, if they make it to ninety."),

    # ---------------- 4 · THE ODDS ----------------
    dict(act=4, type="rank", title="Chance a 62-year-old lives past 80⅓", sub="The 62-vs-70 break-even · SSA period life table", fmt="pct0", count=False, vmax=100, src=LT,
         bars=cue([dict(label="Man", value=round(P_M * 100, 1)), dict(label="Woman", value=round(P_F * 100, 1)), dict(label="At least one of a couple", value=round(P_ANY * 100, 1), hl=True)],
                  ["sixty-two-year-old man", "sixty-two-year-old woman", "at least one of them"]),
         narration="So how likely are you to reach those ages? {p} Social Security's actuaries publish a life table, the one used in this year's trustees report. {p} By that table, a sixty-two-year-old man has about a sixty percent chance of living past eighty and a third, the break-even between sixty-two and seventy. A sixty-two-year-old woman, about seventy-one percent. {pp} For a married couple, both sixty-two, the chance that at least one of them gets there is about eighty-eight percent, treating their lifespans as independent. {p} On average, a man who reaches sixty-two lives to about eighty-two. A woman, to about eighty-five. {p} And for someone already sixty-seven, deciding whether to wait until seventy: the chance of living past eighty-two and a half is about fifty-seven percent for a man, and sixty-seven percent for a woman."),
    dict(act=4, type="host", bg="none",
         narration="Two warnings about these odds. {p} First, this is a period life table: it uses death rates from a single recent year. If health keeps improving, today's sixty-two-year-olds should live a little longer than this. {p} Second, averages aren't you. Your health, your family history and your income all shift the odds. Research has found that, on average, higher earners live several years longer than lower earners.",
         items=[dict(at="period life table", text="One year's death rates", color="acc2"), dict(at="averages aren't you", text="Averages aren't you", serif=True, size=62), dict(at="higher earners", text="Health · family · income", color="acc")]),

    # ---------------- 5 · THE SURVIVOR ----------------
    dict(act=5, type="stats", title="When the higher earner dies first", sub="Example: higher earner's full benefit $2,800 · survivor at full retirement age", src=SSA + ": survivor benefits; widow(er)'s limit of 82.5% of the deceased's full benefit when the deceased claimed early · our calculation",
         stats=[dict(at="two thousand three hundred and ten", value=SURV62, fmt="usd0", label="survivor's check if they claimed at 62"), dict(at="three thousand four hundred and seventy-two", value=SURV70, fmt="usd0", label="survivor's check if they waited to 70")],
         narration="There's one more piece most break-even math leaves out: the survivor. {p} When one spouse dies, the survivor keeps the larger of the two checks, not both. So for a married couple, the higher earner's claiming age can decide the widow's or widower's income for decades. {pp} Say the higher earner's full benefit is twenty-eight hundred dollars. If they claimed at sixty-two and die first, a survivor at full retirement age gets about two thousand three hundred and ten a month. That's thanks to a rule that guarantees at least eighty-two and a half percent of the full amount. {p} If they had waited until seventy, the survivor would get about three thousand four hundred and seventy-two. {p} That's more than eleven hundred dollars a month, for the rest of the survivor's life, and it rises with every cost-of-living adjustment. {p} And because women who reach sixty-two outlive men by about three years on average, in many couples the survivor is the wife. For her, the husband's claiming age may matter more than her own."),

    # ---------------- 6 · SO WHEN? ----------------
    dict(act=6, type="list", title="Good reasons people claim early", src=SSA + ": retirement earnings test, 2027 ($1 withheld for every $2 above $25,560 before full retirement age)",
         narration="That doesn't make seventy right for everyone. People have good reasons to claim earlier. {p} They need the income now, and have no savings to bridge the gap. {p} Their health, or their family history, points to a shorter life. {p} They're the lower earner in a couple, while the higher earner waits. {p} Or they simply value money more at sixty-two than at ninety. {pp} One trap to know: if you claim before full retirement age and keep working, Social Security holds back one dollar for every two you earn above twenty-five thousand five hundred and sixty dollars in 2027. That money isn't lost. Your check is recalculated at full retirement age. But it surprises many people.",
         items=[dict(at="need the income now", kind="bullet", text="Need the income, no bridge savings"),
                dict(at="Their health", kind="bullet", text="Health or family history"),
                dict(at="the lower earner", kind="bullet", text="Lower earner in a couple"),
                dict(at="value money more", kind="bullet", text="Money now > money at 90"),
                dict(at="One trap", kind="title", text="TRAP: EARNINGS TEST ($25,560)")]),
    dict(act=6, type="host", bg="none",
         narration="So, sixty-two, sixty-seven or seventy? {p} If you live past about eighty, waiting starts to win. Most sixty-two-year-olds will get there, and most couples will have at least one spouse who does. {p} Yet fewer than one in ten new retirees waits until seventy, and almost one in four starts at sixty-two. {pp} Tell me in the comments: when did you claim, or when do you plan to?",
         items=[dict(at="past about eighty", text="Past ~80: waiting wins", color="acc"), dict(at="most couples", text="Couples: ~88% odds", color="acc2"), dict(at="when did you claim", text="When did you claim?", serif=True, size=60)]),
    dict(act=6, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="1 in 3", color="acc", title="How many retirees really have $1 million?", sub="4 ways to count"),
         narration="Social Security is one piece. To see how many retirees have a million dollars on top of it, watch this next. {p} This is Nest Egg Atlas. See you next time.",
         hold=14),
]

snapshot = [dict(set="ssa", iso=k, year=2027, value=v, src=COLA) for k, v in [("cola", 3.6), ("avg_before", 2095), ("avg_after", 2170), ("max_fra", 4188), ("ret_test", 25560)]]
snapshot += [dict(set="aw", iso=f"s62_{y}", year=y, value=S62[y], src=SUPP) for y in AW] + [dict(set="aw", iso=f"s70_{y}", year=y, value=S70[y], src=SUPP) for y in AW]

E = lambda say, expr, equal: dict(say=say, rule="expr", expr=expr, equal=equal)
checks = [
    E("62 = −30% (36×5/9 + 24×5/12)", "round(36 * 5 / 9 + 24 * 5 / 12, 6)", 30.0),
    E("70 = +24% (36 × 2/3)", "round(36 * 2 / 3, 6)", 24.0),
    E("$2,000 → $1,400 at 62, $2,480 at 70", f"[{B62}, {B70}]", [1400, 2480]),
    E("≈ 77% more per month (2480/1400)", "round(2480 / 1400 - 1, 2)", 0.77),
    E("waiting eight years (62 → 70)", "70 - 62", 8),
    E("break-even 62 vs 67 ≈ 78 y 8 m", f"round({BE6267} * 12) == 78 * 12 + 8", True),
    E("break-even 62 vs 70 ≈ 80 y 4 m", f"round({BE6270} * 12) == 80 * 12 + 4", True),
    E("break-even 67 vs 70 = 82.5", f"round({BE6770}, 3)", 82.5),
    E("by 80 almost tied, ~$300k each", f"all(290000 <= v <= 315000 for v in {list(T80.values())})", True),
    E("by 90: ≈ $470k / $550k / $595k", f"[round({T90[62]} / 1e4), round({T90[67]} / 1e4), round({T90[70]} / 5e3)]", [47, 55, 119]),
    E("≈ $125k more if waited (90)", f"round(({T90[70]} - {T90[62]}) / 5e3) * 5", 125),
    dict(say="COLA 2027 = 3.6%", set="ssa", iso="cola", year=2027, min=3.6, max=3.6),
    dict(say="average retired worker $2,095 → $2,170", set="ssa", iso="avg_after", year=2027, min=2170, max=2170),
    dict(say="max at FRA $4,188", set="ssa", iso="max_fra", year=2027, min=4188, max=4188),
    dict(say="earnings test $25,560", set="ssa", iso="ret_test", year=2027, min=25560, max=25560),
    dict(say="2008: ≈ 45% at 62", set="aw", iso="s62_2008", year=2008, min=44.5, max=45.49),
    dict(say="2024: ≈ 23% at 62", set="aw", iso="s62_2024", year=2024, min=22.5, max=23.49),
    dict(say="2008: ≈ 1.5% at 70+", set="aw", iso="s70_2008", year=2008, min=1.25, max=1.74),
    dict(say="2024: more than 9% at 70+", set="aw", iso="s70_2024", year=2024, min=9.0, max=9.99),
    E("average age 63.6 → 65.3", "[63.6, 65.3]", [63.6, 65.3]),
    E("FRA 65 → 62 = −20% (36 × 5/9)", "round(36 * 5 / 9, 6)", 20.0),
    dict(say="almost one in four still at 62 (2024)", set="aw", iso="s62_2024", year=2024, min=21.0, max=24.99),
    E("man 62 → past 80⅓ ≈ 60%", f"round({P_M} * 100)", 60),
    E("woman 62 → past 80⅓ ≈ 71%", f"round({P_F} * 100)", 71),
    E("couple: at least one ≈ 88%", f"round({P_ANY} * 100)", 88),
    E("life expectancy at 62: man ≈ 82, woman ≈ 85", f"[round(62 + {EX62['M']}), round(62 + {EX62['F']})]", [82, 85]),
    E("survivor if claimed at 62 = max(70%, 82.5%) of $2,800", f"{SURV62}", 2310),
    E("survivor if waited to 70 = 124% of $2,800", f"{SURV70}", 3472),
    E("difference > $1,100/month", f"{SURV70} - {SURV62} > 1100", True),
    E("fewer than one in ten at 70+ (2024)", f"{S70[2024]} < 10", True),
    E("trustees report 2026 uses 2023 period table (SSA OACT)", "2023", 2023),
    E("over a long retirement > $100k either way (by 90: +$124,800)", f"{T90[70]} - {T90[62]} > 100000", True),
    E("born 1960 → turn 67 in 2027", "1960 + 67", 2027),
    E("avg +$75 (2,170 − 2,095)", "2170 - 2095", 75),
    E("age 67 → past 82.5: man ≈ 57%", f"round({P67_M} * 100)", 57),
    E("age 67 → past 82.5: woman ≈ 67%", f"round({P67_F} * 100)", 67),
    E("women at 62 outlive men by ≈ 3 years (23.08 − 20.29)", f"round({EX62['F']} - {EX62['M']})", 3),
]

clips = [
    dict(**{"from": "s00", "to": "s00"}, hook="Social Security: *62 or 70?*", title="Social Security at 62 vs 70: 77% more per month #Shorts", desc="Full benefit $2,000 at 67 → $1,400 at 62 or $2,480 at 70 (SSA rules, born 1960+)."),
    dict(**{"from": "s04", "to": "s04"}, hook="Almost half used to claim at *62*", title="Half of retirees claimed Social Security at 62. Now? #Shorts", desc="2008: ~45% of new retirees started at 62. 2024: ~23%. At 70+: 1.5% → 9% (SSA Annual Statistical Supplement 2026)."),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="b-N03-ssage", clips=clips, channel="nesteggatlas", chapter0="The choice", host=False,
            thumb=dict(kind="text", top="SOCIAL SECURITY: 62 OR 70?", big="AGE 80", line2="THE BREAK-EVEN", sticker="SSA DATA"),
            w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks, datasets=[], snapshot=snapshot,
            voice=dict(model="", name="Algieba",
                       style=("You are the narrator of a calm, trustworthy personal-finance documentary for Americans in their fifties, sixties and seventies. "
                              "Read the script below in a warm, mature, unhurried voice, at about 138 words per minute, like a respected public-radio journalist "
                              "explaining numbers to a friend. Let each dollar figure land with a short pause before it. Sound reassuring and clear, never salesy, "
                              "never alarmed, never like an advertisement.")),
            music=[dict(act=0, track="Lightless Dawn", vol=0.18), dict(act=1, track="Deliberate Thought", vol=0.17), dict(act=2, track="Investigations", vol=0.17),
                   dict(act=3, track="Inspired", vol=0.17), dict(act=4, track="Floating Cities", vol=0.17), dict(act=5, track="Deliberate Thought", vol=0.17), dict(act=6, track="Inspired", vol=0.18)],
            yt=dict(title="Social Security at 62, 67 or 70? The Break-Even Ages, From SSA's Own Data",
                    description=("When should you claim Social Security? Using the Social Security Administration's own rules and data, we calculate the break-even ages "
                                 "(62 vs 67, 62 vs 70, 67 vs 70), how much each choice pays by age 80 and 90, the odds of reaching those ages from SSA's life table, "
                                 "what new retirees actually choose (almost half claimed at 62 in 2008; about 23% in 2024), and the survivor rule most break-even math leaves out. "
                                 "Includes the 2027 COLA of 3.6%.\n\n"
                                 "Educational content, not financial advice. Check your own estimate in your Social Security account.\n\n"
                                 "Sources: Social Security Administration — 2027 COLA Fact Sheet; Annual Statistical Supplement 2026, Table 6.B5.1; Office of the Chief Actuary, 2023 period life table "
                                 "(2026 Trustees Report); early retirement reduction, delayed retirement credits, survivor benefits and the retirement earnings test. "
                                 "Break-even ages, totals and probabilities are our calculations (today's dollars, before taxes, no investment returns).\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#socialsecurity #retirement #retirementplanning #personalfinance #cola2027"),
                    tags=["social security", "social security at 62 vs 70", "when to claim social security", "social security break even", "2027 cola", "full retirement age", "survivor benefits", "retirement planning", "retirement", "personal finance"], lang="en"))

json.dump(spec, open(os.path.join(HERE, "b-N03.json"), "w"), ensure_ascii=False, indent=1)
clean = lambda t: t.replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()
words = sum(len(clean(s["narration"])) for s in shots)
acts = {}
for s in shots:
    acts[s["act"]] = acts.get(s["act"], 0) + len(clean(s["narration"]))
print("shots", len(shots), "palavras", words, f"~{words / 138:.1f} min a 138 wpm", "por ato", acts)
print("BE", round(BE6267, 3), round(BE6270, 3), round(BE6770, 3), "T80", T80, "T90", T90, "P", round(P_M, 3), round(P_F, 3), round(P_ANY, 3), "S62", S62, "S70", S70, "surv", SURV62, SURV70)

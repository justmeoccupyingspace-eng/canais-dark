"""Gera specs/long/b-L03.json — How It Ticks longo #3: "GPS Only Works Because of Einstein".
Fontes: GPS.gov (órbita ~20.200 km, 2 voltas/dia), Ashby (APS 'Matters of Gravity' / Living Reviews), Misra (GPS World, 2023),
Bahder (arXiv gr-qc/0306076). Todas as contas físicas conferidas em "checks" (regra expr)."""
import json, os

ACTS = ["Cold open", "Time is distance", "Clocks in orbit", "The 11-kilometer problem", "The fix", "Einstein in your pocket"]
C = 299792458

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="orbit", src="GPS.gov · constellation in medium Earth orbit, ~20,200 km",
         narration="Right now, about thirty satellites are flying twenty thousand kilometers above you. {p} Every one of them carries an atomic clock. {p} Your phone listens to those clocks to work out where you are. {pp} But there's a problem. Those clocks run fast.",
         sats=6, link=dict(at="Your phone listens"), tag=dict(at="run fast", text="+38 µs / day"),
         react=[dict(at="Right now", pose="pointUp"), dict(at="atomic clock", pose="pointL"), dict(at="run fast", pose="shock")]),
    dict(act=0, type="counter", src="Uncorrected relativistic clock offset × speed of light", title="GPS error if nobody fixed the clocks", unit="kilometers off, after one day",
         **{"from": 0, "to": 11}, dur=5.0, go=dict(at="every single day"),
         notes=[dict(at="Albert Einstein", text="the fix: relativity")],
         narration="Only by about thirty-eight millionths of a second a day. {p} Sounds like nothing. {p} But if nobody corrected it, GPS would drift by about eleven kilometers, every single day. {pp} The fix comes from Albert Einstein, and from two ideas most people think only matter near black holes. {p} It might be the most useful thing relativity has ever done. {p} Let's see how a few billionths of a second decide whether your map puts you on the right street.",
         react=[dict(at="thirty-eight millionths", pose="idle"), dict(at="eleven kilometers", pose="shock"), dict(at="Albert Einstein", pose="pointUp"), dict(at="black holes", pose="think")]),

    # ---------------- 1 · TIME IS DISTANCE ----------------
    dict(act=1, type="orbit", src="GPS signal: satellite ID + exact send time; range = travel time × speed of light",
         narration="First, how GPS actually works. {p} Each satellite constantly broadcasts a simple message: who it is, and exactly what time it sent the signal. {p} Your phone notes when the signal arrives. {p} The difference is how long the signal traveled. {p} And since radio waves move at the speed of light, travel time tells you distance.",
         sats=6, link=dict(at="Your phone notes"), msg=dict(at="who it is", text="“I'm satellite 17. It's 12:00:00.000000000”"),
         react=[dict(at="how GPS", pose="think"), dict(at="who it is", pose="pointL"), dict(at="travel time tells", pose="pointUp")]),
    dict(act=1, type="code", title="light, per nanosecond", src="c = 299,792,458 m/s",
         narration="The catch is how fast light is. {p} In one billionth of a second, a nanosecond, light travels about thirty centimeters. {p} So if your clock is off by just one millionth of a second, your position is off by about three hundred meters. {p} GPS is really a timing system that happens to tell you where you are.",
         lines=[dict(at="one billionth", **{"in": "299792458 * 1e-9   # meters in 1 ns", "out": "0.299792458", "note": "≈ 30 cm per nanosecond"}),
                dict(at="one millionth", **{"in": "299792458 * 1e-6   # meters in 1 µs", "out": "299.792458", "bad": True, "note": "≈ 300 m off"})],
         react=[dict(at="how fast", pose="think"), dict(at="thirty centimeters", pose="pointL"), dict(at="three hundred meters", pose="shock"), dict(at="timing system", pose="pointUp")]),
    dict(act=1, type="orbit", src="Trilateration: 3 ranges fix a point; the 4th satellite solves the receiver clock error",
         narration="With the distance to three satellites, your phone can pin down a single point. {p} But your phone has a cheap quartz clock, nowhere near an atomic one. {p} So it uses a fourth satellite to solve for the time as well. {p} Four satellites, four unknowns: where you are, in three dimensions, and what time it really is. {p} Usually your phone can see more than four, and uses the extras to sharpen the fix.",
         sats=6, link=dict(at="three satellites"), spheres=dict(at="pin down"), tag=dict(at="fourth satellite", text="4 satellites → x, y, z + time"),
         react=[dict(at="three satellites", pose="pointL"), dict(at="cheap quartz", pose="shrug"), dict(at="four unknowns", pose="pointUp")]),

    # ---------------- 2 · CLOCKS IN ORBIT ----------------
    dict(act=2, type="list", src="GPS.gov · satellite atomic clocks (cesium, rubidium)", title="The satellites",
         narration="So everything depends on the satellite clocks being perfect. {p} They're atomic clocks, cesium and rubidium, accurate to a few billionths of a second. {p} They orbit about twenty thousand kilometers up, going around the Earth twice a day, at almost fourteen thousand kilometers an hour. {p} And that's exactly where Einstein comes in. Twice.",
         items=[dict(at="cesium and rubidium", kind="bullet", text="atomic clocks: cesium + rubidium"),
                dict(at="twenty thousand kilometers", kind="bullet", text="~20,200 km up · 2 orbits a day"),
                dict(at="fourteen thousand", kind="bullet", text="~14,000 km/h"),
                dict(at="Twice", kind="title", text="EINSTEIN, TWICE")],
         react=[dict(at="perfect", pose="idle"), dict(at="atomic clocks", pose="pointL"), dict(at="fourteen thousand", pose="shock"), dict(at="Twice", pose="pointUp")]),
    dict(act=2, type="code", title="special relativity: speed slows time", src="Δt ≈ v²/2c² per second · v ≈ 3.87 km/s",
         narration="Effect number one: speed. {p} Einstein's special relativity says a moving clock ticks slower than one standing still. {p} At fourteen thousand kilometers an hour, the satellite clocks lose about seven millionths of a second every day, compared with clocks on the ground.",
         lines=[dict(at="Effect number one", **{"in": "v = 3874   # m/s, GPS orbit"}),
                dict(at="lose about seven", **{"in": "v**2 / (2 * c**2) * 86400 * 1e6", "out": "7.2", "bad": True, "note": "µs lost per day (moving clock ticks slower)"})],
         react=[dict(at="speed", pose="pointUp"), dict(at="ticks slower", pose="think"), dict(at="lose about seven", pose="pointL")]),
    dict(act=2, type="code", title="general relativity: gravity slows time", src="Δt ≈ GM(1/R⊕ − 1/r)/c² per second · r ≈ 26,560 km",
         narration="Effect number two: gravity. {p} Einstein's general relativity says clocks run slower deeper in a gravity well. {p} We're down here, deep in Earth's gravity. The satellites are far above it, where gravity is weaker. {p} So from our point of view, their clocks run faster, by about forty-five millionths of a second a day.",
         lines=[dict(at="Effect number two", **{"in": "GM = 3.986e14; R = 6.371e6; r = 2.656e7"}),
                dict(at="forty-five millionths", **{"in": "GM * (1/R - 1/r) / c**2 * 86400 * 1e6", "out": "45.7", "note": "µs gained per day (weaker gravity → faster clock)"})],
         react=[dict(at="gravity", pose="pointUp"), dict(at="gravity well", pose="think"), dict(at="run faster", pose="shock")]),
    dict(act=2, type="duel", src="Ashby (APS, 1997); Misra, GPS World (2023)", title="Satellite clock vs ground clock, per day",
         left=dict(label="speed (special)", value=-7, color="acc2"), right=dict(label="gravity (general)", value=45, color="warm"), fmt="usec", badge="NET +38 µs",
         cues=[dict(at="Minus seven", show="a"), dict(at="plus forty-five", show="b")],
         narration="Put them together. {p} Minus seven for speed, plus forty-five for gravity. {pp} The satellite clocks gain about thirty-eight millionths of a second every day. {p} The two effects fight each other, and gravity wins.",
         react=[dict(at="Put them together", pose="think"), dict(at="Minus seven", pose="pointL"), dict(at="thirty-eight", pose="shock"), dict(at="gravity wins", pose="cheer")]),

    dict(act=2, type="duel", src="Hafele & Keating, Science 177 (1972) · flights of October 1971", title="1971: four atomic clocks on airliners",
         left=dict(label="flying east", value=-59, color="acc2"), right=dict(label="flying west", value=273, color="warm"), fmt="nsec", badge="AS PREDICTED",
         cues=[dict(at="Flying east", show="a"), dict(at="Flying west", show="b")],
         narration="If that sounds too weird to be real, it was tested with plane tickets. {p} In 1971, two physicists, Joseph Hafele and Richard Keating, flew four atomic clocks around the world on ordinary passenger jets, then compared them with clocks left on the ground. {p} Flying east, the clocks lost about fifty-nine billionths of a second. {p} Flying west, they gained about two hundred seventy-three. {pp} Within the error bars of what Einstein's theories predicted.",
         react=[dict(at="plane tickets", pose="cheer"), dict(at="four atomic clocks", pose="pointL"), dict(at="Flying east", pose="think"), dict(at="Einstein's theories predicted", pose="pointUp")]),

    # ---------------- 3 · 11 KM ----------------
    dict(act=3, type="code", title="38 µs, in distance", src="c = 299,792,458 m/s",
         narration="Now turn that into distance. {p} Thirty-eight millionths of a second, times the speed of light, is about eleven thousand four hundred meters. {p} Eleven kilometers. {pp} After one day. {p} And the error doesn't reset. It keeps piling up: twenty-three kilometers after two days, about eighty after a week.",
         lines=[dict(at="Thirty-eight millionths", **{"in": "38e-6 * 299792458", "out": "11392.1", "bad": True, "note": "meters of error per day"}),
                dict(at="keeps piling up", **{"in": "[d * 11.39 for d in (1, 2, 7)]", "out": "[11.39, 22.78, 79.73]", "bad": True, "note": "km after 1 day, 2 days, a week"})],
         react=[dict(at="turn that into distance", pose="pointUp"), dict(at="Eleven kilometers", pose="shock"), dict(at="doesn't reset", pose="think"), dict(at="after a week", pose="shock")]),
    dict(act=3, type="host", bg="none",
         narration="Your map wouldn't put you on the wrong street. {p} Within a week, it would put you in the wrong city. {p} Planes, ships, farm tractors, phone networks and banks, which all use GPS time, {pp} would slowly drift out of sync with reality.",
         items=[dict(at="wrong street", text="Not the wrong street…"), dict(at="wrong city", text="…the wrong city.", color="warm"),
                dict(at="phone networks and banks", text="Networks and banks use GPS time too", color="acc2")],
         react=[dict(at="wrong street", pose="shrug"), dict(at="wrong city", pose="shock"), dict(at="drift out of sync", pose="think")]),

    dict(act=3, type="list", src="3GPP TDD phase sync (±1.5 µs) · EU MiFID II RTS 25 (HFT timestamps ≤100 µs from UTC)", title="Who else runs on GPS time",
         narration="And it's not just maps. {p} Many cell towers use GPS time to stay in sync with each other, to within about one and a half millionths of a second. {p} In Europe, high-frequency traders must time-stamp their trades to within a tenth of a millisecond of official time, and many firms get that time from satellites. {pp} A clock drifting thirty-eight microseconds a day would knock those cell towers out of sync in about an hour, and the traders within three days.",
         items=[dict(at="cell towers", kind="bullet", text="cell networks: in sync to ~1.5 µs"),
                dict(at="high-frequency traders", kind="bullet", text="EU high-frequency trading: ≤100 µs from UTC"),
                dict(at="in about an hour", kind="title", text="38 µs/DAY: TOWERS OUT OF SYNC IN ~1 HOUR")],
         react=[dict(at="not just maps", pose="pointUp"), dict(at="cell towers", pose="pointL"), dict(at="traders", pose="think"), dict(at="in about an hour", pose="shock")]),

    # ---------------- 4 · THE FIX ----------------
    dict(act=4, type="code", title="the factory setting", src="Misra, GPS World (2023) · Bahder, arXiv gr-qc/0306076",
         narration="So how do you fix a clock that runs fast in space? {p} You make it run slow on the ground. {p} GPS clocks are built to tick at ten point two three megahertz. {p} But before launch, they're set to ten point two two nine nine nine nine nine nine nine five four three. {p} On the ground, that's slightly slow. In orbit, relativity speeds it up to exactly right. {p} And ground stations still watch every satellite clock, and upload small corrections to each one, usually at least once a day.",
         lines=[dict(at="ten point two three megahertz", **{"in": "f0 = 10.23e6   # Hz, the standard"}),
                dict(at="before launch", **{"in": "f0 * (1 - 4.465e-10)", "out": "10229999.99543", "note": "Hz: set slow on purpose"})],
         react=[dict(at="runs fast in space", pose="think"), dict(at="run slow on the ground", pose="pointUp"), dict(at="nine five four three", pose="shock"), dict(at="exactly right", pose="cheer"), dict(at="ground stations", pose="pointL")]),
    dict(act=4, type="list", src="Ashby, 'General relativity in the Global Positioning System' (APS Matters of Gravity, 1997)", title="NTS-2, June 1977",
         narration="Not everyone believed it at first. And the skeptics weren't crazy: nobody had ever put a cesium clock in orbit before. {p} In June 1977, the first test satellite with a cesium clock, NTS-2, went up with a switch on board, so the correction could be turned on later. {p} For twenty days, engineers let the clock run uncorrected. {p} It ran fast by four hundred forty-two parts in a trillion. {p} Einstein predicted four hundred forty-six. {pp} Less than one percent off. Then they flipped the switch.",
         items=[dict(at="In June 1977", kind="bullet", text="23 Jun 1977 · NTS-2: first cesium clock in orbit"),
                dict(at="For twenty days", kind="bullet", text="20 days with the correction off"),
                dict(at="four hundred forty-two", kind="bullet", text="measured: +442.5 parts per trillion"),
                dict(at="Einstein predicted", kind="bullet", text="predicted: +446.5"),
                dict(at="flipped the switch", kind="title", text="< 1% OFF")],
         react=[dict(at="Not everyone believed", pose="shrug"), dict(at="twenty days", pose="think"), dict(at="Einstein predicted", pose="pointUp"), dict(at="flipped the switch", pose="cheer")]),

    # ---------------- 5 · POCKET ----------------
    dict(act=5, type="list", src="Ashby, Living Reviews in Relativity (2003)", title="Corrections still running today",
         narration="And that's not the only correction. {p} GPS orbits aren't perfect circles, so each clock speeds up and slows down a little as its height changes. Your receiver corrects for that too. {p} The Earth also rotates while the signal is in flight, adding another tiny shift. {p} Every position fix quietly accounts for all of it. {p} And it's not just GPS. Europe's Galileo, Russia's GLONASS and China's BeiDou all have to make the same relativity corrections.",
         items=[dict(at="perfect circles", kind="bullet", text="slightly oval orbits: clock rate wobbles"),
                dict(at="Earth also rotates", kind="bullet", text="Earth rotates during the signal's trip"),
                dict(at="all of it", kind="title", text="CORRECTED EVERY FIX"),
                dict(at="Galileo", kind="bullet", text="Galileo · GLONASS · BeiDou: same physics")],
         react=[dict(at="not the only", pose="pointUp"), dict(at="perfect circles", pose="think"), dict(at="rotates", pose="pointL"), dict(at="all of it", pose="idle", nod=1)]),
    dict(act=5, type="list", src="Penn State GEOG 862 · GPS.gov (Selective Availability, May 2000)", title="Wrong on purpose, part two",
         narration="And here's a twist. For years, GPS was also made wrong on purpose, for a different reason. {p} Until 2000, the US military deliberately jittered the satellite clocks for civilian users, a feature called Selective Availability. {p} Your position could be off by about a hundred meters. {p} On May second, 2000, it was switched off, and civilian GPS got about ten times more accurate overnight.",
         items=[dict(at="Selective Availability", kind="bullet", text="“Selective Availability”: jittered clocks"),
                dict(at="about a hundred meters", kind="bullet", text="civilian error: ~100 m"),
                dict(at="switched off", kind="strike", text="switched off: 2 May 2000"),
                dict(at="ten times more accurate", kind="title", text="~10× MORE ACCURATE")],
         react=[dict(at="twist", pose="pointUp"), dict(at="deliberately", pose="shock"), dict(at="switched off", pose="cheer")]),
    dict(act=5, type="host", bg="none",
         narration="So, the next time your phone finds you on a map, remember what's happening. {p} Clocks in orbit, running fast because gravity is weaker up there, and slow because they're moving, {p} set wrong on purpose, so they'd be right in space. {pp} Relativity isn't just for black holes. {p} It's in your pocket.",
         items=[dict(at="Clocks in orbit", text="Fast: weaker gravity"), dict(at="slow because", text="Slow: high speed"), dict(at="set wrong on purpose", text="Set wrong on purpose", color="acc"),
                dict(at="in your pocket", text="Relativity: in your pocket.", serif=True, size=70, color="acc2")],
         react=[dict(at="next time", pose="idle"), dict(at="set wrong", pose="pointUp"), dict(at="black holes", pose="shrug"), dict(at="in your pocket", pose="cheer")]),
    dict(act=5, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="931 GB", color="acc", title="Where did 69 GB of my 1 TB drive go?", sub="another number that isn't what it looks like"),
         cta="Subscribe: how things really work",
         narration="If you like numbers that aren't what they look like, watch where sixty-nine gigabytes of every one-terabyte drive go. {p} I'm How It Ticks. See you in the next one.",
         hold=14,
         react=[dict(at="sixty-nine gigabytes", pose="pointL"), dict(at="See you", pose="wave")]),
]

checks = [
    dict(say="30 cm per nanosecond", rule="expr", expr="round(299792458 * 1e-9, 2)", equal=0.3),
    dict(say="1 µs ≈ 300 m", rule="expr", expr="round(299792458 * 1e-6)", equal=300),
    dict(say="orbital speed ≈ 3.87 km/s ≈ 14,000 km/h", rule="expr", expr="round(3874 * 3.6 / 1000)", equal=14),
    dict(say="orbit radius 26,560 km = 20,200 km up", rule="expr", expr="round((2.656e7 - 6.371e6) / 1e3, -2)", equal=20200.0),
    dict(say="2 orbits a day (period ~11h58m)", rule="expr", expr="round(2 * 3.141592653589793 * (2.656e7 ** 3 / 3.986e14) ** 0.5 / 3600, 1)", equal=12.0),
    dict(say="speed effect −7.2 µs/day", rule="expr", expr="round(3874 ** 2 / (2 * 299792458 ** 2) * 86400 * 1e6, 1)", equal=7.2),
    dict(say="gravity effect +45.7 µs/day", rule="expr", expr="round(3.986e14 * (1 / 6.371e6 - 1 / 2.656e7) / 299792458 ** 2 * 86400 * 1e6, 1)", equal=45.7),
    dict(say="net ≈ +38 µs/day", rule="expr", expr="round(45.7 - 7.2)", equal=38),
    dict(say="38 µs × c = 11,392 m", rule="expr", expr="round(38e-6 * 299792458, 1)", equal=11392.1),
    dict(say="23 km after 2 days, ~80 after a week", rule="expr", expr="[round(2 * 11.392), round(7 * 11.392)]", equal=[23, 80]),
    dict(say="factory frequency 10.22999999543 MHz", rule="expr", expr="round(10.23e6 * (1 - 4.465e-10), 5)", equal=10229999.99543),
    dict(say="offset matches ~38.6 µs/day", rule="expr", expr="round(4.465e-10 * 86400 * 1e6, 1)", equal=38.6),
    dict(say="Hafele-Keating within error bars: E −59±10 vs −40±23; W +273±7 vs +275±21", rule="expr", expr="[abs(-59 - -40) <= 10 + 23, abs(273 - 275) <= 7 + 21]", equal=[True, True]),
    dict(say="SA ~100 m → ~10 m: about ten times", rule="expr", expr="100 / 10", equal=10.0),
    dict(say="1.5 µs at 38 µs/day ≈ 1 hour; 100 µs ≈ 2.6 days", rule="expr", expr="[round(1.5 / (38 / 24), 1), round(100 / 38, 1)]", equal=[0.9, 2.6]),
    dict(say="NTS-2: 442.5 vs 446.5 = <1% off", rule="expr", expr="abs(446.5 - 442.5) / 446.5 < 0.01", equal=True),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="b-L03-gps-einstein", channel="howitticks", chapter0="Clocks that run fast", min_total=420, w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks,
            datasets=[], snapshot=[],
            thumb=dict(kind="text", top="WITHOUT EINSTEIN", big="+11 KM", line2="EVERY DAY", sticker="GPS"),
            voice=dict(model="", name="Iapetus",
                       style=("You are the narrator of a popular engineering explainer channel on YouTube. Read the script below like a sharp, curious "
                              "engineer telling a friend something surprising: clear, warm, a little dry humor, at an engaged pace of about "
                              "150 words per minute. Slow down slightly for numbers and let the reveals land. "
                              "Never sound like an advertisement or an audiobook.")),
            music=[dict(act=0, track="Hidden Agenda", vol=0.22), dict(act=1, track="Thinking Music", vol=0.22), dict(act=2, track="Floating Cities", vol=0.22),
                   dict(act=3, track="Impact Moderato", vol=0.22), dict(act=4, track="Deliberate Thought", vol=0.22), dict(act=5, track="Inspired", vol=0.22)],
            yt=dict(title="GPS Only Works Because of Einstein",
                    description=("GPS satellite clocks run fast by about 38 microseconds a day. Uncorrected, your position would drift about 11 km every day. "
                                 "How GPS turns time into distance, the two relativity effects that fight each other in orbit, the clock that's set wrong on purpose, "
                                 "and the 1977 satellite that proved Einstein right.\n\n"
                                 "Sources: GPS.gov; N. Ashby, 'General relativity in the Global Positioning System' (APS, 1997) and Living Reviews in Relativity (2003); "
                                 "P. Misra, 'Inside the box: GPS and relativity', GPS World (2023); T. Bahder, arXiv gr-qc/0306076.\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#gps #relativity #einstein #physics #engineering"),
                    tags=["gps", "relativity", "einstein", "time dilation", "atomic clock", "physics", "engineering"], lang="en"))

json.dump(spec, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "b-L03.json"), "w"), ensure_ascii=False, indent=1)
words = sum(len(s["narration"].replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()) for s in shots)
print("shots", len(shots), "palavras", words, f"~{words / 145:.1f} min a 145 wpm")

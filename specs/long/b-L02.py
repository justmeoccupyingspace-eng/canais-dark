"""Gera specs/long/b-L02.json — How It Ticks longo #2: "Where Did 69 GB of My 1 TB Drive Go?".
Fontes: SI/BIPM (prefixos, 1960), IEC 60027-2 Amd.2 (1998), Apple Snow Leopard (2009), acordos WD (2006) e Seagate (2007),
sobreprovisionamento de SSD (TechTarget/Kingston). Contas em "checks" (regra expr)."""
import json, os

ACTS = ["Cold open", "Two kinds of kilo", "Who's right?", "Gigabytes in court", "The hidden 100 GB", "Bits, bytes and your bill"]
B10 = "1111111111"

shots = [
    # ---------------- 0 · COLD OPEN ----------------
    dict(act=0, type="stack", src="Drive sold as 1 TB = 1,000,000,000,000 bytes", title="Your new 1 TB drive", sub="what your PC shows",
         total=1000, segs=[dict(at="nine hundred thirty-one", value=931.32, text="931 GB", label="what Windows shows", color="acc"),
                          dict(at="Sixty-nine", value=68.68, text="69 GB?", label="gone?", color="warm", ghost=True)],
         narration="You buy a one-terabyte drive. You plug it in. {p} And your computer says nine hundred thirty-one gigabytes. {pp} Sixty-nine gigabytes, gone. {p} So who's lying? The box, or your computer?",
         react=[dict(at="You buy", pose="idle"), dict(at="nine hundred thirty-one", pose="pointL"), dict(at="gone", pose="shock"), dict(at="who's lying", pose="think")]),
    dict(act=0, type="host", bg="none",
         narration="Neither. Both numbers are correct. {p} They're counting in two different units, and both units are called a gigabyte. {p} And once you see how that happened, you'll spot the same trick in your RAM, in your internet bill, and inside your SSD, which actually holds more than one terabyte. {pp} You just can't use it.",
         items=[dict(at="Both numbers", text="Both numbers are correct"), dict(at="two different units", text="Two units, one name: “gigabyte”", color="acc"),
                dict(at="more than one terabyte", text="Your SSD holds MORE than 1 TB", color="acc2")],
         react=[dict(at="Neither", pose="shrug"), dict(at="two different units", pose="pointUp"), dict(at="more than one terabyte", pose="shock"), dict(at="can't use it", pose="shrug")]),

    # ---------------- 1 · TWO KILOS ----------------
    dict(act=1, type="code", title="powers of two", src="",
         narration="It starts with how computers count. {p} Everything inside is binary, so memory comes in powers of two: two, four, eight, sixteen, thirty-two. {p} And two to the tenth power is one thousand and twenty-four. {p} That's so close to one thousand that early computer engineers just started calling it a kilo.",
         lines=[dict(at="powers of two", **{"in": "[2**n for n in range(1, 6)]", "out": "[2, 4, 8, 16, 32]"}),
                dict(at="two to the tenth", **{"in": "2 ** 10", "out": "1024", "note": "close enough to 1,000… right?"})],
         react=[dict(at="how computers count", pose="think"), dict(at="two to the tenth", pose="pointL"), dict(at="calling it a kilo", pose="shrug")]),
    dict(act=1, type="bits", src="Binary addressing: n address lines → 2ⁿ locations", label="10 address wires", sub="each one is a 1 or a 0 → 2¹⁰ = 1,024 addresses",
         bits=B10, speed=0.12, show=dict(at="each byte by its address"),
         narration="There's a physical reason for those powers of two. {p} A memory chip finds each byte by its address, sent over wires, and every wire is either a one or a zero. {p} With ten wires, you can name exactly one thousand and twenty-four addresses. Not one thousand. {p} So memory naturally comes in sizes like one thousand twenty-four, two thousand forty-eight, four thousand ninety-six.",
         react=[dict(at="physical reason", pose="pointUp"), dict(at="either a one or a zero", pose="pointL"), dict(at="Not one thousand", pose="idle", nod=1)]),
    dict(act=1, type="code", title="1982", src="Commodore 64 (1982): 64 KB of RAM",
         narration="For decades, nobody minded. {p} When the Commodore 64 came out in 1982, its sixty-four kilobytes of memory meant sixty-five thousand, five hundred and thirty-six bytes, and everyone knew it. {p} At that size, the two meanings of kilo were only two point four percent apart.",
         lines=[dict(at="sixty-four kilobytes", **{"in": "64 * 1024", "out": "65536", "note": "bytes of RAM in a Commodore 64"}),
                dict(at="two point four percent", **{"in": "1024 / 1000", "out": "1.024", "note": "2.4% apart: who cares?"})],
         react=[dict(at="nobody minded", pose="shrug"), dict(at="Commodore", pose="pointL"), dict(at="two point four", pose="idle", nod=1)]),
    dict(act=1, type="ladder", src="1.024ⁿ − 1 for n = 1…5", title="Same prefix, two meanings", la="decimal (×1,000)", lb="binary (×1,024)",
         rows=[dict(at="At kilo", label="kilo", a=1, b=1.024, text="1,000 vs 1,024", gap="+2.4%"),
               dict(at="At mega", label="mega", a=1, b=1.024 ** 2, text="10⁶ vs 2²⁰", gap="+4.9%"),
               dict(at="At giga", label="giga", a=1, b=1.024 ** 3, text="10⁹ vs 2³⁰", gap="+7.4%"),
               dict(at="at tera", label="tera", a=1, b=1.024 ** 4, text="10¹² vs 2⁴⁰", gap="+10.0%", hot=True),
               dict(at="drift further", label="peta", a=1, b=1.024 ** 5, text="10¹⁵ vs 2⁵⁰", gap="+12.6%", hot=True)],
         narration="The problem is that the small difference doesn't stay small. {p} At kilo, the binary version is two point four percent bigger. At mega, it's almost five percent. At giga, seven point four. {p} And at tera, the gap is ten percent. That's why a ten-terabyte drive shows up as just nine point oh nine. {pp} Every step up, the two meanings drift further apart.",
         react=[dict(at="doesn't stay small", pose="think"), dict(at="At giga", pose="pointL"), dict(at="ten percent", pose="shock"), dict(at="drift further", pose="shrug")]),

    # ---------------- 2 · WHO'S RIGHT ----------------
    dict(act=2, type="code", title="the math on your drive", src="1 TB (SI) = 10¹² bytes; 1 GiB = 2³⁰ bytes",
         narration="Now let's do the math on your drive. {p} The box means a terabyte in the official sense: one trillion bytes. {p} Windows divides that by a binary gigabyte, which is one billion, seventy-three million and change. {p} One trillion divided by that is nine hundred thirty-one point three. {pp} Not a single byte is missing. {p} Windows is measuring in binary gigabytes, and still calling them gigabytes.",
         lines=[dict(at="one trillion bytes", **{"in": "10**12", "out": "1000000000000", "note": "bytes, as printed on the box"}),
                dict(at="binary gigabyte", **{"in": "2**30", "out": "1073741824", "note": "one binary gigabyte (a “gibibyte”)"}),
                dict(at="nine hundred thirty-one point", **{"in": "10**12 / 2**30", "out": "931.3225746154785", "note": "what Windows calls “931 GB”"})],
         react=[dict(at="do the math", pose="pointUp"), dict(at="official sense", pose="idle"), dict(at="Not a single byte", pose="shock"), dict(at="still calling", pose="shrug")]),
    dict(act=2, type="list", src="BIPM (SI prefixes, 1960); IEC 60027-2 Amd. 2 (1998); Apple, Mac OS X 10.6 (2009)", title="So who's right?",
         narration="So who's right? {p} Technically, the drive makers. In the metric system, giga has meant one billion since 1960. {p} In 1998, the International Electrotechnical Commission even created new names for the binary units: kibibyte, mebibyte, gibibyte. The “bi” means binary. {p} Almost nobody says them out loud. {p} Windows kept the old names. On Linux, the same command can show both: df dash h counts in binary, df dash capital H in decimal. {p} And Apple went the other way: since 2009, a Mac counts storage in thousands.",
         items=[dict(at="since 1960", kind="bullet", text="1960 · metric system: giga = 1,000,000,000"),
                dict(at="In 1998", kind="bullet", text="1998 · IEC: KiB, MiB, GiB (binary units)"),
                dict(at="Windows kept", kind="bullet", text="Windows · binary math, “GB” label"),
                dict(at="On Linux", kind="bullet", text="Linux · df -h → binary, df -H → decimal"),
                dict(at="Apple went", kind="bullet", text="2009 · macOS: storage counted in 1,000s")],
         react=[dict(at="who's right", pose="think"), dict(at="drive makers", pose="pointL"), dict(at="Almost nobody", pose="shrug"), dict(at="Apple went", pose="pointUp")]),
    dict(act=2, type="duel", src="Same drive: 10¹² bytes", title="Same drive, same bytes",
         left=dict(label="On Windows", value=931, color="warm"), right=dict(label="On a Mac", value=1000, color="acc2"), fmt="int", badge="SAME BYTES",
         cues=[dict(at="Windows PC", show="a"), dict(at="on a Mac", show="b")],
         narration="Same drive, same bytes. {p} Plug it into a Windows PC and it says nine hundred thirty-one gigabytes. {p} Plug it in on a Mac, and it says one thousand. {pp} The only thing that changed is the ruler.",
         react=[dict(at="Same drive", pose="idle"), dict(at="Windows PC", pose="pointL"), dict(at="on a Mac", pose="pointL"), dict(at="ruler", pose="cheer")]),

    # ---------------- 3 · COURT ----------------
    dict(act=3, type="list", src="Redmond Magazine (28 Jun 2006); The Register (2 Nov 2007)", title="Gigabytes in court",
         narration="This confusion has actually ended up in court. {p} In 2006, Western Digital settled a class action that said its eighty-gigabyte drive showed up as about seventy-four. {p} It gave customers free backup software, and paid half a million dollars in legal fees. {p} In 2007, Seagate settled a similar case: five percent cash back on older drives, or free software. {pp} Neither company admitted doing anything wrong. {p} And both kept using the decimal gigabyte. They just print the definition on the box now.",
         items=[dict(at="In 2006", kind="bullet", text="2006 · Western Digital: “80 GB” shows as ~74"),
                dict(at="half a million", kind="bullet", text="free software + $500,000 in legal fees"),
                dict(at="In 2007", kind="bullet", text="2007 · Seagate: 5% back or free software"),
                dict(at="print the definition", kind="title", text="“1 GB = 1,000,000,000 BYTES”")],
         react=[dict(at="ended up in court", pose="shock"), dict(at="half a million", pose="pointUp"), dict(at="Neither company", pose="shrug"), dict(at="print the definition", pose="idle", nod=1)]),
    dict(act=3, type="code", title="the 3.5-inch floppy disk", src="1.44 MB floppy: 2,880 sectors × 512 bytes",
         narration="But the strangest gigabyte cousin is older. {p} The classic floppy disk said one point four four megabytes. {p} It held one million, four hundred seventy-four thousand, five hundred and sixty bytes. {p} Eighty tracks, two sides, eighteen sectors per track, five hundred and twelve bytes each. {p} That's fourteen forty times one thousand twenty-four. {p} So that megabyte was a thousand binary kilobytes. {pp} Half decimal, half binary. It's not a real megabyte in either system.",
         lines=[dict(at="Eighty tracks", **{"in": "80 * 2 * 18 * 512", "out": "1474560", "note": "bytes on a “1.44 MB” floppy = 1440 × 1024"}),
                dict(at="Half decimal", **{"in": "1474560 / 10**6, 1474560 / 2**20", "out": "(1.47456, 1.40625)", "bad": True, "note": "neither one is 1.44"})],
         react=[dict(at="strangest", pose="think"), dict(at="one point four four", pose="pointL"), dict(at="Half decimal", pose="shock")]),

    dict(act=3, type="code", title="CDs and DVDs", src="CD-R 80 min: 360,000 sectors × 2,048 B; DVD±R: 4,707,319,808 B",
         narration="Discs couldn't agree either. {p} A CD's seven hundred megabytes are binary megabytes: about seven hundred thirty-seven million bytes. {p} But a DVD's four point seven gigabytes are decimal: four point seven billion bytes. {p} So the very same computer shows that DVD as four point three eight.",
         lines=[dict(at="seven hundred megabytes", **{"in": "737280000 / 2**20", "out": "703.125", "note": "a “700 MB” CD: binary megabytes"}),
                dict(at="four point three eight", **{"in": "4707319808 / 2**30", "out": "4.384…", "bad": True, "note": "a “4.7 GB” DVD, as your PC shows it"})],
         react=[dict(at="couldn't agree", pose="shrug"), dict(at="binary megabytes", pose="pointL"), dict(at="four point three eight", pose="shock")]),

    # ---------------- 4 · HIDDEN 100 GB ----------------
    dict(act=4, type="stack", src="Inherent SSD over-provisioning: binary NAND vs decimal capacity (TechTarget, Kingston)", title="Inside a typical 1 TB SSD", sub="flash chips are built in binary sizes: 1,024 GiB",
         total=1099.51, segs=[dict(at="sold, and shown", value=1000, text="1,000 GB", label="what you can use", color="acc"),
                              dict(at="is hidden", value=99.51, text="≈100 GB", label="hidden spare", color="warm")],
         narration="Now, the twist I promised. {p} Flash memory chips are built in binary sizes. A typical one-terabyte SSD contains one thousand and twenty-four binary gigabytes of flash. {p} That's about one thousand ninety-nine regular gigabytes. {p} But it's sold, and shown, as one terabyte. {pp} So about a hundred gigabytes is hidden. On purpose.",
         react=[dict(at="twist", pose="pointUp"), dict(at="one thousand ninety-nine", pose="pointL"), dict(at="is hidden", pose="shock"), dict(at="On purpose", pose="idle", nod=1)]),
    dict(act=4, type="list", src="TechTarget: SSD over-provisioning; Kingston: Understanding SSD Over-provisioning", title="What the hidden space does",
         narration="Flash memory wears out. Each cell can only be erased so many times. {p} So the drive's controller keeps that hidden space for itself: to spread writes evenly across the chips, to clean up old data in the background, and to replace cells that die. {p} The industry calls this overprovisioning. {pp} Your drive isn't hiding space from you. {p} It's hiding it for you, so it lasts longer. {p} You can even give it more: leave part of an SSD unpartitioned, and many drives will use that as extra spare space.",
         items=[dict(at="spread writes", kind="bullet", text="wear leveling: spread writes evenly"),
                dict(at="clean up old data", kind="bullet", text="garbage collection in the background"),
                dict(at="replace cells", kind="bullet", text="spare blocks for cells that die"),
                dict(at="hiding it for you", kind="title", text="NOT FROM YOU. FOR YOU."),
                dict(at="unpartitioned", kind="bullet", text="tip: unpartitioned space = extra spare")],
         react=[dict(at="wears out", pose="think"), dict(at="spread writes", pose="pointL"), dict(at="overprovisioning", pose="pointUp"), dict(at="lasts longer", pose="cheer")]),

    # ---------------- 5 · BITS & BYTES ----------------
    dict(act=5, type="code", title="your internet plan", src="1 byte = 8 bits",
         narration="And there's one more unit trap, and you probably pay for it every month. {p} Internet speed is sold in bits per second. Files are measured in bytes. And one byte is eight bits. {p} So a one-gigabit connection downloads at most one hundred twenty-five megabytes per second, before any overhead. {pp} Little b, big B. {p} One letter, a factor of eight.",
         lines=[dict(at="one-gigabit", **{"in": "1000 / 8    # Mbps → MB/s", "out": "125.0", "note": "a “1 Gbps” plan, at best"})],
         react=[dict(at="every month", pose="shrug"), dict(at="eight bits", pose="pointUp"), dict(at="one hundred twenty-five", pose="pointL"), dict(at="factor of eight", pose="shock")]),
    dict(act=5, type="code", title="your RAM", src="JEDEC memory convention: 1 GB of RAM = 2³⁰ bytes",
         narration="Meanwhile, RAM is still sold in binary. {p} A sixteen-gigabyte memory stick really holds sixteen binary gigabytes: about seventeen point two billion bytes. {p} So the word gigabyte means one billion bytes on your drive, about one point oh seven billion in your RAM, {p} and on your internet bill, it's not even bytes.",
         lines=[dict(at="sixteen-gigabyte", **{"in": "16 * 2**30", "out": "17179869184", "note": "a “16 GB” RAM stick"})],
         react=[dict(at="still sold in binary", pose="pointL"), dict(at="seventeen point two", pose="pointUp"), dict(at="not even bytes", pose="shrug")]),
    dict(act=5, type="host", bg="none",
         narration="So, your drive isn't lying. {p} The box speaks metric. Windows speaks binary, using metric words. {p} Nine hundred thirty-one gigabytes and one terabyte are the same trillion bytes, measured with two different rulers. {p} The disc, the floppy, the RAM, the internet plan: every one of them is honest, in its own unit. {p} And the lesson goes way beyond hard drives: {pp} whenever you see a number, check the unit.",
         items=[dict(at="The box speaks", text="Box: 1 TB = 10¹² bytes"), dict(at="Windows speaks", text="Windows: 931 “GB” = 10¹² bytes"),
                dict(at="check the unit", text="Check the unit.", serif=True, size=80, color="acc")],
         react=[dict(at="isn't lying", pose="idle"), dict(at="Windows speaks", pose="pointL"), dict(at="two different rulers", pose="shrug"), dict(at="check the unit", pose="pointUp")]),
    dict(act=5, type="end", src="",
         next=dict(kicker="WATCH NEXT", big="0.1 + 0.2", color="acc", title="Tiny math errors that cost lives", sub="and hundreds of millions"),
         cta="Subscribe: how things really work",
         narration="And if you want to see what happens when a number doesn't fit its box, watch this one next: four tiny math errors that cost lives and millions. {p} I'm How It Ticks. See you in the next one.",
         hold=14,
         react=[dict(at="doesn't fit", pose="think"), dict(at="watch this one", pose="pointL"), dict(at="See you", pose="wave")]),
]

checks = [
    dict(say="2^10 = 1024", rule="expr", expr="2 ** 10", equal=1024),
    dict(say="1 TB / GiB = 931.3", rule="expr", expr="repr(10**12 / 2**30)", equal="931.3225746154785"),
    dict(say="'sixty-nine gigabytes gone'", rule="expr", expr="round(1000 - 10**12 / 2**30)", equal=69),
    dict(say="gaps 2.4 / 4.9 / 7.4 / 10.0 / 12.6 %", rule="expr", expr="[round((1.024 ** n - 1) * 100, 1) for n in range(1, 6)]", equal=[2.4, 4.9, 7.4, 10.0, 12.6]),
    dict(say="GiB = 1,073,741,824 ('one billion seventy-three million and change')", rule="expr", expr="2 ** 30", equal=1073741824),
    dict(say="WD 80 GB shows as ~74", rule="expr", expr="int(80e9 / 2**30)", equal=74),
    dict(say="floppy 1440*1024 = 1,474,560", rule="expr", expr="[1440 * 1024, 2880 * 512]", equal=[1474560, 1474560]),
    dict(say="floppy in decimal / binary MB", rule="expr", expr="repr((1474560 / 10**6, 1474560 / 2**20))", equal="(1.47456, 1.40625)"),
    dict(say="1,024 GiB = ~1,099 GB, ~100 GB hidden", rule="expr", expr="[int(1024 * 2**30 / 1e9), round(1024 * 2**30 / 1e9 - 1000)]", equal=[1099, 100]),
    dict(say="1 Gbps = 125 MB/s", rule="expr", expr="1000 / 8", equal=125.0),
    dict(say="16 GiB = 17.2 billion bytes", rule="expr", expr="[16 * 2**30, round(16 * 2**30 / 1e9, 1)]", equal=[17179869184, 17.2]),
    dict(say="binary giga = ~1.07 billion", rule="expr", expr="round(2**30 / 1e9, 2)", equal=1.07),
    dict(say="Commodore 64: 65,536 bytes", rule="expr", expr="64 * 1024", equal=65536),
    dict(say="10 TB drive shows 9.09", rule="expr", expr="round(10**13 / 2**40, 2)", equal=9.09),
    dict(say="CD 700 'MB' = 737,280,000 B = 703 MiB", rule="expr", expr="[360000 * 2048, 360000 * 2048 / 2**20]", equal=[737280000, 703.125]),
    dict(say="DVD 4.7 GB shows as 4.38", rule="expr", expr="round(4707319808 / 2**30, 2)", equal=4.38),
    dict(say="first five powers of two", rule="expr", expr="repr([2**n for n in range(1, 6)])", equal="[2, 4, 8, 16, 32]"),
]

for i, sh in enumerate(shots):
    sh["id"] = f"s{i:02d}"

spec = dict(id="b-L02-931gb", channel="howitticks", chapter0="69 GB, gone?", w=1920, h=1080, fps=30, acts=ACTS, shots=shots, checks=checks,
            datasets=[], snapshot=[],
            thumb=dict(kind="text", top="MY 1 TB DRIVE SAYS", big="931 GB", line2="WHY?!", sticker="69 GB GONE?"),
            voice=dict(model="", name="Iapetus",
                       style=("You are the narrator of a popular engineering explainer channel on YouTube. Read the script below like a sharp, curious "
                              "engineer telling a friend something surprising: clear, warm, a little dry humor, at an engaged pace of about "
                              "150 words per minute. Slow down slightly for numbers and let the reveals land. "
                              "Never sound like an advertisement or an audiobook.")),
            music=[dict(act=0, track="Hidden Agenda", vol=0.22), dict(act=1, track="Thinking Music", vol=0.22), dict(act=2, track="Deliberate Thought", vol=0.22),
                   dict(act=3, track="Investigations", vol=0.22), dict(act=4, track="Floating Cities", vol=0.22), dict(act=5, track="Inspired", vol=0.22)],
            yt=dict(title="Where Did 69 GB of My 1 TB Drive Go?",
                    description=("You buy a 1 TB drive and your PC shows 931 GB. Nothing is missing: \"gigabyte\" means two different things. "
                                 "Why computers count in 1,024s, who's actually right, the lawsuits it caused, the weird 1.44 MB floppy, "
                                 "and why your SSD secretly holds MORE than 1 TB.\n\n"
                                 "Sources: BIPM SI prefixes; IEC 60027-2 Amendment 2 (1998); Apple Mac OS X 10.6 (2009); "
                                 "Western Digital settlement (2006) and Seagate settlement (2007) press coverage; "
                                 "SSD over-provisioning (TechTarget, Kingston).\n"
                                 "{music_credits}\nNarration is AI-generated.\n\n#engineering #computers #storage #ssd"),
                    tags=["1tb 931gb", "gigabyte vs gibibyte", "hard drive capacity", "ssd overprovisioning", "binary vs decimal", "kibibyte", "computer science", "engineering"], lang="en"))

json.dump(spec, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "b-L02.json"), "w"), ensure_ascii=False, indent=1)
words = sum(len(s["narration"].replace("{p}", "").replace("{pp}", "").replace("<soft>", "").replace("</soft>", "").split()) for s in shots)
print("shots", len(shots), "palavras", words, f"~{words / 145:.1f} min a 145 wpm")

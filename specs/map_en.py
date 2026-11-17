"""Chartbound (canal A, EN): história contada no mapa em Shorts de ~80-95 s.
Modelo: "One Map, One Battle" (criado 07/10/2026, 15,6 mil inscritos, mediana de 60 mil views nos últimos 30 vídeos):
mapa de satélite, territórios/frentes pintados, setas de movimento, data no canto, legenda limpa, narração séria e rápida.
Uso: python specs/map_en.py → specs/ese/a-en-NNN.json (renderizado pelo mesmo ese.yml)"""
import json, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ese")
os.makedirs(OUT, exist_ok=True)
STYLE = ("Read this in English as a documentary narrator for a fast history channel: confident, clear, slightly dramatic, brisk pace "
         "(about 165 words per minute), short pauses before dates and numbers. Never sound like an advert. Read the text exactly as written.")
TAGS = ["history", "map", "history on a map", "military history", "geography", "history shorts", "maps"]
TAIL = "\n\nFollow for more history on the map.\n\n#history #maps #geography"


def fix(o):
    if isinstance(o, dict): return {("from" if k == "from_" else k): fix(v) for k, v in o.items()}
    if isinstance(o, list): return [fix(v) for v in o]
    return o


def save(n, title, hook, beats, desc, thumb, at, tags=()):
    spec = fix(dict(id=f"a-en-{n:03d}", channel="A", lang="en", format="short", style="clean", hook=hook, hook_end=2.6,
                    voice="Charon", models="gemini-3.8-flash-tts,gemini-3.1-flash-tts-preview", edge_voice="en-US-AndrewMultilingualNeural",
                    music=dict(track="Volatile Reaction", vol=0.11, alt=["Hidden Agenda", "Investigations"]), beats=beats, thumb=thumb,
                    yt=dict(title=title, description=desc + TAIL, tags=TAGS + list(tags), lang="en", categoryId="27"), publish=dict(at=at)))
    spec["style_prompt"] = STYLE
    json.dump(spec, open(f"{OUT}/{spec['id']}.json", "w"), ensure_ascii=False, indent=1)
    w = sum(len(b["say"].split()) for b in beats)
    print(spec["id"], w, "words", f"~{w / 2.75:.0f}s")


BER = [13.40, 52.52]
HAM, HAN, FRA_ = [9.99, 53.55], [9.73, 52.37], [8.68, 50.11]
WB = [[13.09, 52.42], [13.12, 52.60], [13.25, 52.66], [13.40, 52.62], [13.46, 52.55], [13.45, 52.47], [13.38, 52.39], [13.20, 52.38]]
save(1, "How the West Fed Berlin From the Sky for 11 Months",
     "STALIN TRIED|TO STARVE|BERLIN",
     [
         dict(say="In 1948, Stalin tried to starve two million people into surrender. The West answered by flying in everything, from flour to coal.",
              cam={"c": [12.5, 52.0], "s": 7.5}, date="JUNE 1948", pins=[dict(ll=BER, label="Berlin", d=1.0)]),
         dict(say="After the war, Germany was split between four powers, and so was Berlin. But Berlin sat deep inside the Soviet zone, more than 150 kilometers from the West.",
              cam={"c": [11.0, 51.8], "s": 5.0}, pins=[],
              zones=[dict(coords=[[10.9, 54.0], [11.6, 54.15], [13.0, 54.45], [14.2, 53.95], [14.4, 53.3], [14.6, 52.6], [14.75, 52.05], [15.0, 51.2], [14.8, 50.85], [14.3, 50.88], [13.3, 50.6], [12.3, 50.25], [11.9, 50.4], [11.2, 50.35], [10.1, 50.55], [10.0, 51.1], [10.2, 51.5], [10.6, 51.75], [11.0, 52.2], [10.95, 52.6], [11.3, 53.05], [10.6, 53.4], [10.9, 53.7]], color="#c1121f", label="SOVIET ZONE", ly=60, d=4.5),
                     dict(coords=WB, color="#1d4ed8", op=0.8, d=6.5)],
              cards=[dict(text="Berlin to the West:", big="150+ km", d=8.0)]),
         dict(say="On June 24th, 1948, the Soviets cut every road, rail line and canal into West Berlin. The city had food for 36 days. Coal for 45.",
              date="24 JUNE 1948", cards=[dict(text="Food:", big="36 days", d=5.0), dict(text="Coal:", big="45 days", d=6.2)],
              arrows=[dict(from_=[7.5, 52.4], to=[12.4, 52.5], color="#ff4d4d", d=0.8)]),
         dict(say="But there were three air corridors the Soviets had agreed to in writing. So the Americans and the British started flying.",
              cards=[], arrows=[dict(from_=HAM, to=BER, d=1.4, color="#7fd3ff"), dict(from_=HAN, to=BER, d=1.8, color="#7fd3ff"), dict(from_=FRA_, to=BER, d=2.2, color="#7fd3ff")],
              pins=[dict(ll=HAM, label="Hamburg", left=True, d=1.4), dict(ll=HAN, label="Hanover", left=True, d=1.8), dict(ll=FRA_, label="Frankfurt", left=True, d=2.2)]),
         dict(say="At the peak, a plane landed in Berlin almost every minute.",
              cam={"c": [13.3, 52.5], "s": 22}, pins=[dict(ll=[13.40, 52.47], label="Tempelhof", d=0.6)], cards=[dict(text="Peak day:", big="1,398 flights", d=1.6)]),
         dict(say="One pilot started dropping candy on tiny parachutes for the kids. Berliners called them the raisin bombers.",
              cards=[], date="1948 – 1949"),
         dict(say="In May 1949, after almost eleven months, Stalin gave up and reopened the roads.",
              cam={"c": [11.0, 51.8], "s": 5.0}, date="12 MAY 1949", pins=[], arrows=[dict(from_=[7.5, 52.4], to=[12.4, 52.5], color="#7dff9a", d=0.6)]),
         dict(say="In total: about 278,000 flights and more than 2.3 million tons of supplies.",
              arrows=[], cards=[dict(text="Flights:", big="~278,000", d=0.6), dict(text="Supplies:", big="2.3 million tons", d=2.6)]),
         dict(say="It cost 101 lives in crashes and accidents. But not a single shot was fired, and West Berlin stayed free.",
              cards=[dict(text="Lives lost:", big="101", d=1.0)]),
     ],
     "June 1948: the Soviets cut every road, rail line and canal into West Berlin. For almost eleven months, the US and Britain supplied 2 million people by air: about 278,000 flights, 2.3 million tons of food and coal.",
     dict(title="STALIN TRIED|TO STARVE|BERLIN", c=[11.5, 52.0], s=5.5, y=0.62, w=1080, h=1920), "2026-11-17T22:00:00Z",
     tags=["berlin airlift", "cold war", "stalin", "berlin blockade", "candy bomber", "1948"])

AK = [-152, 64]
save(2, "How Russia Sold Alaska for 2 Cents an Acre",
     "RUSSIA SOLD|ALASKA FOR|2¢ AN ACRE",
     [
         dict(say="In 1867, Russia sold a piece of land more than twice the size of Texas to the United States. The price: 7.2 million dollars.",
              cam={"c": [-160, 62], "s": 1.35}, date="1867", own={"US-AK": "RUS", "RUS": "RUS", "US-48": "USA"},
              cards=[dict(text="Price:", big="$7.2 million", iso="USA", d=5.5)]),
         dict(say="That's about two cents an acre.",
              cards=[dict(text="Per acre:", big="~2 cents", d=0.3)]),
         dict(say="Why would anyone sell that? Russia was broke after losing the Crimean War, and Alaska was almost impossible to defend.",
              cards=[], cam={"c": [-150, 60], "s": 0.75}, arrows=[dict(from_=[40, 56], to=[-150, 62], color="#ff4d4d", d=2.0)]),
         dict(say="Right next door was British Canada. If war came again, Britain could simply take it.",
              arrows=[dict(from_=[-110, 58], to=AK, color="#ff4d4d", d=1.4)], own={"CAN": "GBR"}, od=0.4),
         dict(say="Russia had only a few hundred settlers there, mostly fur traders. And the sea otters they hunted were nearly gone.",
              arrows=[], cam={"c": [-155, 60], "s": 1.6}, pins=[dict(ll=[-135.33, 57.05], label="New Archangel (Sitka)", left=True, d=1.0)]),
         dict(say="So Russia offered it to the Americans. Secretary of State William Seward signed the deal on March 30th, 1867.",
              pins=[], date="30 MARCH 1867", own={"US-AK": "USA"}, od=4.0, cards=[dict(text="Signed by:", big="William Seward", iso="USA", d=2.4)]),
         dict(say="Critics called it Seward's Folly. A giant icebox.",
              cards=[dict(text="The press:", big="“Seward's Folly”", d=0.4)]),
         dict(say="Then came gold. The Klondike rush next door pulled thousands north, and gold turned up in Alaska too, at Nome.",
              cards=[], date="1896 – 1899", pins=[dict(ll=[-139.4, 64.06], label="Klondike", d=1.4), dict(ll=[-165.4, 64.5], label="Nome", left=True, d=5.2)]),
         dict(say="In 1968, they found the largest oil field in North America, at Prudhoe Bay.",
              date="1968", pins=[dict(ll=[-148.3, 70.3], label="Prudhoe Bay", d=1.6)]),
         dict(say="And the strangest part? In the Bering Strait, an American island and a Russian island sit less than four kilometers apart.",
              date=None, pins=[dict(ll=[-168.95, 65.75], label="Little Diomede (US)", d=3.0), dict(ll=[-169.06, 65.78], label="Big Diomede (Russia)", left=True, d=4.2)],
              cam={"c": [-169.0, 65.9], "s": 9}, cards=[dict(text="Distance:", big="< 4 km", d=6.0)]),
     ],
     "1867: Russia sold Alaska to the United States for $7.2 million, about 2 cents an acre. Broke after the Crimean War and unable to defend it, Russia let it go. Then came gold, and in 1968, the largest oil field in North America.",
     dict(title="RUSSIA SOLD|ALASKA FOR|2¢ AN ACRE", c=[-160, 63], s=1.3, y=0.66, own={"US-AK": "RUS", "RUS": "RUS", "US-48": "USA"}), "2026-11-18T17:00:00Z",
     tags=["alaska purchase", "seward's folly", "russia", "alaska", "1867", "bering strait"])

STANLEY = [-57.85, -51.69]
ASC = [-14.37, -7.95]
LON = [-0.13, 51.5]
save(3, "How Britain Took Back the Falklands in 74 Days",
     "74 DAYS|8,000 MILES|FROM HOME",
     [
         dict(say="In April 1982, Argentina invaded a British territory almost 13,000 kilometers from London.",
              cam={"c": [-30, -15], "s": 0.42}, date="APRIL 1982", own={"GBR": "GBR", "ARG": "ARG", "FLK": "GBR"},
              arrows=[dict(from_=LON, to=STANLEY, color="#7fd3ff", d=2.0)]),
         dict(say="On April 2nd, Argentine forces landed near Stanley. The small garrison of Royal Marines surrendered within hours.",
              cam={"c": [-59.0, -51.8], "s": 22}, date="2 APRIL 1982", arrows=[dict(from_=[-56.5, -52.6], to=[-57.9, -51.75], color="#ff4d4d", d=0.6)],
              own={"FLK": "ARG"}, od=3.0, pins=[dict(ll=STANLEY, label="Stanley", d=0.8)]),
         dict(say="Argentina calls them Las Malvinas, and has claimed them since Britain took control in 1833.",
              arrows=[], cards=[dict(text="Argentina's claim:", big="since 1833", iso="ARG", d=2.0)]),
         dict(say="Britain answered with a task force of more than 100 ships, sailing for the far end of the Atlantic.",
              cards=[], pins=[], cam={"c": [-30, -15], "s": 0.42}, date="5 APRIL 1982",
              arrows=[dict(from_=[-4.2, 50.3], to=ASC, color="#7fd3ff", d=1.4)]),
         dict(say="They stopped halfway, at Ascension Island, a tiny British rock in the middle of the ocean.",
              pins=[dict(ll=ASC, label="Ascension Island", d=0.8)], arrows=[dict(from_=ASC, to=STANLEY, color="#7fd3ff", d=2.6)]),
         dict(say="On May 2nd, a British submarine sank the Argentine cruiser General Belgrano. 323 sailors died.",
              arrows=[], cam={"c": [-61.5, -54.0], "s": 7}, date="2 MAY 1982",
              pins=[dict(ll=[-61.6, -55.4], label="Belgrano sunk", left=True, d=2.6)], cards=[dict(text="ARA General Belgrano:", big="323 dead", iso="ARG", d=3.6)]),
         dict(say="Two days later, an Argentine jet hit the destroyer HMS Sheffield with a single Exocet missile.",
              date="4 MAY 1982", cards=[dict(text="HMS Sheffield:", big="hit by one Exocet", iso="GBR", d=1.0)]),
         dict(say="On May 21st, British troops landed at San Carlos and crossed the islands on foot.",
              cards=[], cam={"c": [-59.0, -51.8], "s": 22}, date="21 MAY 1982",
              arrows=[dict(from_=[-59.1, -51.55], to=[-58.3, -51.65], color="#7fd3ff", d=1.0), dict(from_=[-58.3, -51.65], to=[-57.95, -51.69], color="#7fd3ff", d=2.4)],
              pins=[dict(ll=[-59.05, -51.55], label="San Carlos", left=True, d=0.6)]),
         dict(say="On June 14th, Argentina surrendered at Stanley. Seventy-four days after the invasion.",
              arrows=[], date="14 JUNE 1982", own={"FLK": "GBR"}, od=1.2, pins=[dict(ll=STANLEY, label="Stanley", d=0.4)]),
         dict(say="649 Argentine and 255 British servicemen died, along with three islanders.",
              pins=[], cards=[dict(text="Argentina:", big="649 dead", iso="ARG", d=0.4), dict(text="Britain:", big="255 dead", iso="GBR", d=2.0), dict(text="Islanders:", big="3", iso="FLK", d=3.4)]),
         dict(say="Argentina still claims the islands. In 2013, 99.8 percent of islanders voted to stay British.",
              cards=[dict(text="2013 referendum:", big="99.8% stay British", iso="FLK", d=2.2)], date="2013"),
     ],
     "2 April 1982: Argentina invades the Falkland Islands. Britain sends a task force of 100+ ships across the Atlantic, via Ascension Island. 74 days later, Argentina surrenders at Stanley.",
     dict(title="74 DAYS|8,000 MILES|FROM HOME", c=[-45, -30], s=0.6, y=0.62, own={"GBR": "GBR", "ARG": "ARG", "FLK": "GBR"},
          arrows=[dict(from_=LON, to=STANLEY, color="#7fd3ff")]), "2026-11-19T17:00:00Z",
     tags=["falklands war", "falklands", "malvinas", "1982", "royal navy", "argentina"])

# ---------------------------------------------------------------- 4. Napoleon in Russia, 1812
NEMAN, MOS, BOR, BER_ = [23.9, 54.9], [37.62, 55.75], [35.82, 55.52], [28.55, 54.33]
save(4, "How Russia Destroyed Napoleon's Army by Retreating",
     "600,000 MEN|INTO RUSSIA.|FEW CAME BACK",
     [
         dict(say="In June 1812, Napoleon crossed into Russia with the largest army Europe had ever seen. More than 600,000 men.",
              cam={"c": [22, 52], "s": 1.6}, date="24 JUNE 1812", own={"FRA": "FRA", "RUS": "RUS"},
              arrows=[dict(from_=[13.4, 52.5], to=NEMAN, color="#7fd3ff", d=2.0)], pins=[dict(ll=NEMAN, label="Neman River", d=3.0)],
              cards=[dict(text="Grande Armée:", big="600,000+", iso="FRA", d=5.0)]),
         dict(say="The plan was simple: one big battle, a quick win, and the Tsar would have to negotiate.",
              cards=[], cam={"c": [31, 55], "s": 2.6}),
         dict(say="But the Russians wouldn't fight. They kept retreating, and burned crops and villages behind them.",
              pins=[], zones=[dict(coords=[[24.5, 56.2], [31.0, 56.5], [36.5, 56.4], [36.8, 54.8], [31.0, 53.6], [24.2, 53.9]], color="#7a2e0e", op=0.45, label="SCORCHED EARTH", d=1.6)],
              arrows=[dict(from_=NEMAN, to=[31.5, 54.8], color="#7fd3ff", d=0.6)]),
         dict(say="Napoleon finally got his battle at Borodino. Around seventy thousand men fell in a single day, and the Russians still pulled back.",
              date="7 SEPTEMBER 1812", zones=[], arrows=[dict(from_=[31.5, 54.8], to=BOR, color="#7fd3ff", d=0.4)], pins=[dict(ll=BOR, label="Borodino", left=True, d=0.8)],
              cards=[dict(text="Borodino:", big="~70,000 casualties", d=3.2)]),
         dict(say="A week later he entered Moscow. It was almost empty. And then it caught fire.",
              cards=[], date="14 SEPTEMBER 1812", cam={"c": [36.5, 55.6], "s": 9}, pins=[dict(ll=MOS, label="Moscow", d=0.6)],
              zones=[dict(coords=[[37.45, 55.82], [37.75, 55.84], [37.8, 55.68], [37.5, 55.66]], color="#ff6a00", op=0.6, label="FIRE", d=3.4)]),
         dict(say="Napoleon waited five weeks for a peace offer that never came. On October 19th, he turned back.",
              date="19 OCTOBER 1812", zones=[], cam={"c": [31, 55], "s": 2.6}, arrows=[dict(from_=MOS, to=[31.5, 54.6], color="#ff4d4d", d=3.0)]),
         dict(say="Then winter arrived. Frost, hunger, and Cossack raids destroyed what was left of the army on the road home.",
              date="NOVEMBER 1812", arrows=[dict(from_=[31.5, 54.6], to=BER_, color="#ff4d4d", d=0.4)],
              zones=[dict(coords=[[27.5, 56.0], [37.8, 56.0], [37.8, 54.0], [27.5, 54.0]], color="#bfe3ff", op=0.25, label="−30°C", d=1.0)]),
         dict(say="At the Berezina River, the survivors crossed on improvised bridges while the Russians closed in.",
              zones=[], date="26–29 NOVEMBER 1812", pins=[dict(ll=BER_, label="Berezina", d=0.6)], arrows=[dict(from_=BER_, to=NEMAN, color="#ff4d4d", d=3.0)]),
         dict(say="Of more than 600,000 men who marched in, historians estimate fewer than one in five made it back.",
              pins=[], date="DECEMBER 1812", cam={"c": [22, 52], "s": 1.6}, cards=[dict(text="Marched in:", big="600,000+", iso="FRA", d=0.6), dict(text="Came back:", big="fewer than 1 in 5", iso="FRA", d=3.0)]),
         dict(say="Russia barely had to win a battle. Distance, fire and winter did the rest.",
              cards=[], arrows=[], own={"RUS": "RUS", "FRA": "FRA"}),
     ],
     "June 1812: Napoleon invades Russia with more than 600,000 men. Borodino, a burning Moscow, five weeks of waiting, then the winter retreat across the Berezina. Fewer than one in five came back.",
     dict(title="600,000 MEN|INTO RUSSIA.|FEW CAME BACK", c=[28, 54], s=1.9, y=0.66, own={"FRA": "FRA", "RUS": "RUS"},
          arrows=[dict(from_=NEMAN, to=MOS, color="#7fd3ff"), dict(from_=MOS, to=BER_, color="#ff4d4d")]), "2026-11-20T17:00:00Z",
     tags=["napoleon", "1812", "napoleon in russia", "borodino", "grande armee", "berezina"])

# ---------------------------------------------------------------- 5. Winter War 1939-40
KAR = [[27.8, 60.5], [29.3, 61.3], [30.0, 61.9], [31.2, 62.6], [32.8, 62.1], [31.6, 61.2], [30.5, 60.2], [29.0, 60.1], [28.0, 60.4]]
save(5, "How Tiny Finland Held Off the Soviet Union for 105 Days",
     "FINLAND VS|THE SOVIET|UNION",
     [
         dict(say="On November 30th, 1939, the Soviet Union invaded Finland. Stalin expected it to take a couple of weeks.",
              cam={"c": [29, 63], "s": 2.0}, date="30 NOVEMBER 1939", own={"FIN": "FIN", "RUS": "SOV"},
              arrows=[dict(from_=[30.3, 59.95], to=[28.9, 60.7], color="#ff4d4d", d=2.0), dict(from_=[33.5, 64.5], to=[29.2, 64.9], color="#ff4d4d", d=2.6), dict(from_=[33.0, 67.5], to=[28.8, 67.4], color="#ff4d4d", d=3.2)]),
         dict(say="On paper it was hopeless. The Soviets had far more soldiers, thousands of tanks and planes. Finland had about thirty tanks.",
              cards=[dict(text="Soviet tanks:", big="thousands", iso="SOV", d=1.6), dict(text="Finnish tanks:", big="~30", iso="FIN", d=5.0)], arrows=[]),
         dict(say="But Finland had the forest, the snow, and men who could ski through both.",
              cards=[], cam={"c": [29.5, 64.8], "s": 4.0}),
         dict(say="At Suomussalmi, Finnish ski troops cut the Soviet columns into pieces on the forest roads, and destroyed two entire divisions.",
              date="DEC 1939 – JAN 1940", pins=[dict(ll=[28.9, 64.9], label="Suomussalmi", d=0.8)],
              zones=[dict(coords=[[29.1, 64.95], [29.6, 64.95], [29.6, 64.75], [29.1, 64.75]], color="#c1121f", op=0.5, d=2.0), dict(coords=[[29.8, 64.85], [30.3, 64.85], [30.3, 64.65], [29.8, 64.65]], color="#c1121f", op=0.5, d=2.8)],
              cards=[dict(text="Destroyed:", big="2 Soviet divisions", iso="FIN", d=5.6)]),
         dict(say="Temperatures dropped to minus forty. Many Soviet soldiers lacked winter gear, while the Finns moved unseen in white.",
              zones=[], pins=[], cards=[dict(text="Winter 1940:", big="−40°C", d=0.8)]),
         dict(say="The Finns even named their bottle bombs after the Soviet foreign minister: the Molotov cocktail.",
              cards=[dict(text="Named after:", big="Vyacheslav Molotov", iso="SOV", d=2.6)]),
         dict(say="In February, the Soviets threw everything at the Mannerheim Line on the Karelian Isthmus, and finally broke through.",
              cards=[], date="FEBRUARY 1940", cam={"c": [29.5, 61.0], "s": 4.5},
              zones=[dict(coords=[[28.0, 60.55], [28.9, 60.75], [29.6, 60.6], [30.2, 60.45]], color="#1d4ed8", op=0.0, label="MANNERHEIM LINE", ly=-30, d=0.6)],
              arrows=[dict(from_=[30.3, 59.95], to=[29.0, 60.75], color="#ff4d4d", d=3.0)]),
         dict(say="On March 13th, 1940, Finland signed a peace. It gave up about a tenth of its land, including its second city, Viipuri.",
              arrows=[], zones=[dict(coords=KAR, color="#cc0000", op=0.55, label="CEDED", d=1.6)], date="13 MARCH 1940",
              pins=[dict(ll=[28.75, 60.71], label="Viipuri", left=True, d=4.6)]),
         dict(say="But it stayed independent. The Soviets lost well over a hundred thousand men in 105 days. Finland lost about twenty-six thousand.",
              pins=[], cam={"c": [29, 63], "s": 2.0}, cards=[dict(text="Soviet dead:", big="~126,000", iso="SOV", d=3.0), dict(text="Finnish dead:", big="~26,000", iso="FIN", d=6.0)]),
     ],
     "30 November 1939: the Soviet Union invades Finland. Ski troops, −40°C, the Molotov cocktail and the Mannerheim Line. 105 days later Finland lost a tenth of its land but kept its independence.",
     dict(title="FINLAND VS|THE SOVIET|UNION", c=[30, 63], s=1.8, y=0.66, own={"FIN": "FIN", "RUS": "SOV"},
          arrows=[dict(from_=[33.5, 64.5], to=[28.5, 64.6], color="#ff4d4d")]), "2026-11-21T17:00:00Z",
     tags=["winter war", "finland", "soviet union", "1939", "molotov cocktail", "mannerheim line", "simo hayha"])

# ---------------------------------------------------------------- 6. Singapore 1942
KB, JOH, SGP_ = [102.24, 6.13], [103.76, 1.47], [103.82, 1.35]
save(6, "How Britain Lost Singapore in One Week",
     "THE FORTRESS|THAT FELL IN|7 DAYS",
     [
         dict(say="Singapore was Britain's great fortress in Asia. Big naval guns, tens of thousands of troops. It fell in a week.",
              cam={"c": [103.8, 1.4], "s": 30}, date="FEBRUARY 1942", own={"SGP": "GBR", "MYS": "GBR"}, pins=[dict(ll=SGP_, label="Singapore", d=1.0)]),
         dict(say="On December 8th, 1941, Japanese troops landed in northern Malaya, around the same time as the attack on Pearl Harbor.",
              pins=[], cam={"c": [102.5, 4.0], "s": 5.5}, date="8 DECEMBER 1941",
              arrows=[dict(from_=[105.0, 7.5], to=KB, color="#ff4d4d", d=1.4)], cards=[]),
         dict(say="Then they raced south down the peninsula. Many rode bicycles, moving faster than the British could fall back.",
              arrows=[dict(from_=KB, to=[101.7, 3.1], color="#ff4d4d", d=0.6), dict(from_=[101.7, 3.1], to=JOH, color="#ff4d4d", d=3.0)],
              own={"MYS": "JPN"}, od=4.5, cards=[dict(text="Down the peninsula:", big="~1,000 km", d=2.0)]),
         dict(say="By the end of January, all of Malaya was gone. The British blew a hole in the causeway and pulled back onto the island.",
              date="31 JANUARY 1942", cards=[], arrows=[], cam={"c": [103.8, 1.4], "s": 30}, pins=[dict(ll=[103.77, 1.45], label="Causeway", d=2.8)]),
         dict(say="Singapore's big guns had been built mainly to stop an attack from the sea. The Japanese came from the north.",
              pins=[], zones=[dict(coords=[[103.6, 1.33], [103.98, 1.36], [104.05, 1.30], [103.7, 1.24]], color="#1d4ed8", op=0.3, label="BUILT FOR A SEA ATTACK", ly=40, d=0.6)],
              arrows=[dict(from_=[103.7, 1.6], to=[103.72, 1.42], color="#ff4d4d", d=3.6)]),
         dict(say="On the night of February 8th, they crossed the strait. Within days, they reached the island's water reservoirs.",
              zones=[], date="8 FEBRUARY 1942", arrows=[dict(from_=[103.65, 1.47], to=[103.7, 1.4], color="#ff4d4d", d=0.6), dict(from_=[103.7, 1.4], to=[103.8, 1.36], color="#ff4d4d", d=3.0)],
              own={"SGP": "JPN"}, od=6.0),
         dict(say="On February 15th, 1942, the British surrendered. Around eighty thousand British, Indian and Australian troops became prisoners.",
              arrows=[], date="15 FEBRUARY 1942", cards=[dict(text="Taken prisoner:", big="~80,000", iso="GBR", d=4.0)]),
         dict(say="Churchill called it the worst disaster and largest capitulation in British history.",
              cards=[dict(text="Churchill:", big="“the worst disaster”", iso="GBR", d=0.6)]),
     ],
     "8 December 1941: Japan lands in northern Malaya. Ten weeks later, Singapore, Britain's 'impregnable' fortress, surrenders. Around 80,000 Allied troops became prisoners.",
     dict(title="THE FORTRESS|THAT FELL IN|7 DAYS", c=[102.8, 3.2], s=4.2, y=0.66, own={"MYS": "JPN", "SGP": "JPN", "THA": "THA"},
          arrows=[dict(from_=KB, to=JOH, color="#ff4d4d")]), "2026-11-22T17:00:00Z",
     tags=["fall of singapore", "singapore 1942", "malaya", "ww2", "churchill", "japan"])

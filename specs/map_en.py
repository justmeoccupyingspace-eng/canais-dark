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

# ---------------------------------------------------------------- 7. Louisiana Purchase 1803 (twin of the Alaska short, best A so far)
LA = [[-89.4, 29.1], [-91.2, 31.0], [-91.1, 33.0], [-90.1, 35.0], [-89.5, 36.6], [-90.2, 38.7], [-91.4, 40.4], [-91.1, 42.5], [-91.6, 44.3], [-93.2, 45.0], [-95.2, 47.2],
      [-95.2, 49.0], [-113.5, 49.0], [-112.4, 47.2], [-111.0, 45.0], [-110.2, 43.6], [-108.8, 42.4], [-106.6, 41.0], [-105.9, 39.2], [-106.2, 38.4], [-100.0, 37.8],
      [-100.0, 34.6], [-97.0, 33.8], [-94.0, 33.6], [-94.05, 32.0], [-93.85, 29.75], [-92.0, 29.6], [-90.5, 29.1]]
US03 = [[-91.5, 31.0], [-85.0, 31.0], [-82.0, 30.6], [-81.4, 30.7], [-80.8, 32.2], [-78.9, 33.6], [-76.0, 35.2], [-75.6, 36.8], [-74.0, 39.6], [-73.8, 40.6], [-71.0, 41.4],
        [-70.0, 41.7], [-70.6, 42.6], [-70.2, 43.7], [-67.0, 44.8], [-67.8, 47.1], [-69.2, 47.4], [-70.0, 45.8], [-71.5, 45.0], [-74.7, 45.0], [-76.4, 44.2], [-79.0, 43.3],
        [-79.0, 42.8], [-82.4, 41.7], [-83.1, 42.2], [-82.4, 43.0], [-82.5, 45.3], [-84.5, 46.5], [-89.5, 47.9], [-95.2, 49.0], [-95.2, 47.2], [-93.2, 45.0], [-91.6, 44.3],
        [-91.1, 42.5], [-91.4, 40.4], [-90.2, 38.7], [-89.5, 36.6], [-90.1, 35.0], [-91.1, 33.0]]
NOLA = [-90.07, 29.95]
ZL = lambda iso, d, label="": dict(coords=LA, iso=iso, op=0.92, label=label, d=d)
ZU = lambda d: dict(coords=US03, iso="USA", op=0.9, d=d)
save(7, "How France Sold Louisiana for 3 Cents an Acre",
     "FRANCE SOLD|ALL OF THIS|FOR 3¢ AN ACRE",
     [
         dict(say="In 1803, the United States doubled in size overnight. It bought 828,000 square miles from France for 15 million dollars.",
              cam={"c": [-92, 39], "s": 1.25}, date="1803", own={"CAN": "GBR"}, zones=[ZU(0.2), ZL("FRA", 0.9)],
              cards=[dict(text="Price:", big="$15 million", iso="USA", d=5.6)]),
         dict(say="That's less than three cents an acre.",
              cards=[dict(text="Per acre:", big="< 3 cents", d=0.3)]),
         dict(say="And America never asked for all of it. Jefferson only wanted one city: New Orleans.",
              cards=[], zones=[], cam={"c": [-90.2, 30.6], "s": 9}, pins=[dict(ll=NOLA, label="New Orleans", d=2.4)]),
         dict(say="Whoever held New Orleans controlled the Mississippi, the road to market for every farmer west of the Appalachians.",
              cam={"c": [-89.5, 37.5], "s": 2.2}, pins=[], arrows=[dict(from_=[-91.2, 44.0], to=[-90.1, 30.3], color="#7fd3ff", d=1.6)]),
         dict(say="Napoleon had big plans for Louisiana. But first he needed Haiti, France's richest colony.",
              arrows=[], cam={"c": [-80, 25.5], "s": 2.1}, pins=[dict(ll=[-72.3, 19.0], label="Haiti (Saint-Domingue)", left=True, d=3.2)]),
         dict(say="The army he sent there was crushed by the Haitian Revolution and yellow fever.",
              date="1802", cards=[dict(text="French army in Haiti:", big="destroyed", iso="FRA", d=1.2)]),
         dict(say="Without Haiti, Louisiana was useless to him. And a new war with Britain was coming. He needed cash.",
              date=None, pins=[], cards=[], cam={"c": [-92, 39], "s": 1.25}, zones=[ZU(0.2), ZL("FRA", 0.5)]),
         dict(say="So in April 1803, his finance minister asked the shocked Americans: why not take the whole thing?",
              date="APRIL 1803", cards=[dict(text="France's offer:", big="ALL of Louisiana", iso="FRA", d=2.6)]),
         dict(say="The treaty is dated April 30th, 1803.",
              date="30 APRIL 1803", cards=[], zones=[ZU(-5), ZL("FRA", -5), ZL("USA", 0.6)]),
         dict(say="Today, that land is part or all of 15 states.",
              date=None, cards=[dict(text="Today:", big="15 states", iso="USA", d=1.4)]),
         dict(say="And the twist? France got paid through a British bank, Barings. So British bankers helped fund Napoleon, right before his war with Britain.",
              cards=[dict(text="Paid through:", big="Barings Bank of London", iso="GBR", d=2.4)], cam={"c": [-35, 44], "s": 0.55},
              arrows=[dict(from_=[-0.1, 51.5], to=[2.35, 48.86], color="#ffcf40", d=4.0)]),
     ],
     "1803: France sold the Louisiana Territory, about 828,000 square miles, to the United States for $15 million, less than three cents an acre. Jefferson only wanted New Orleans. After losing Haiti and facing a new war with Britain, Napoleon sold it all.",
     dict(title="FRANCE SOLD|ALL OF THIS|FOR 3¢ AN ACRE", c=[-96, 41], s=1.5, y=0.66, own={"CAN": "GBR"}, zones=[dict(coords=US03, iso="USA", op=0.9), dict(coords=LA, iso="FRA", op=0.95)]),
     "2026-11-23T17:00:00Z",
     tags=["louisiana purchase", "napoleon", "thomas jefferson", "new orleans", "1803", "haiti", "manifest destiny"])

# ---------------------------------------------------------------- 8. Treaty of Breda 1667: Manhattan × Run (nutmeg)
RUN = [129.69, -4.55]
MAN = [-74.0, 40.75]
GRD = [-61.68, 12.12]
save(8, "How the Dutch Traded Manhattan for a Tiny Spice Island",
     "THE DUTCH|TRADED MANHATTAN|FOR THIS ISLAND",
     [
         dict(say="In 1667, the Dutch gave up Manhattan. In return, they kept an island about two miles long, on the other side of the world.",
              cam={"c": [-74.0, 40.7], "s": 26}, date="1667", pins=[dict(ll=MAN, label="Manhattan", d=0.6)],
              balls=[dict(ll=[-73.85, 40.55], iso="NLD", skin="flag", face="shock", r=0.7, d=1.2)]),
         dict(say="The island was Run, in what's now Indonesia. And back then, these islands were the only place on Earth where nutmeg grew.",
              balls=[], pins=[dict(ll=RUN, label="Run", left=True, d=1.6)], cam={"c": [129.8, -4.5], "s": 30}, date=None,
              cards=[dict(text="Banda Islands:", big="the world's only nutmeg", iso="IDN", d=4.0)]),
         dict(say="In Europe, nutmeg sold for a fortune. Whoever held these islands controlled the supply.",
              cards=[], cam={"c": [125, -2], "s": 3.0}),
         dict(say="England claimed Run in 1616. The Dutch fought for it and drove the English out.",
              date="1616", own={"GBR": "GBR", "NLD": "NLD"}, cam={"c": [129.7, -4.5], "s": 22},
              balls=[dict(ll=[129.85, -4.35], iso="GBR", skin="flag", face="angry", r=0.6, d=0.4), dict(ll=[129.5, -4.75], iso="NLD", skin="flag", face="rage", r=0.7, d=2.6)]),
         dict(say="Meanwhile, across the world, the Dutch had a small town on Manhattan: New Amsterdam.",
              date=None, balls=[dict(ll=[-73.85, 40.55], iso="NLD", skin="flag", face="happy", r=0.7, d=1.4)], cam={"c": [-74.0, 40.7], "s": 26},
              pins=[dict(ll=[-74.01, 40.70], label="New Amsterdam", d=2.6)]),
         dict(say="In 1664, English warships sailed in, and New Amsterdam surrendered. The English renamed it New York.",
              date="1664", arrows=[dict(from_=[-73.4, 40.2], to=[-73.98, 40.62], color="#ff5a3c", d=0.8)],
              balls=[dict(ll=[-73.85, 40.55], iso="NLD", skin="flag", face="shock", r=0.7, d=0), dict(ll=[-73.5, 40.35], iso="GBR", skin="flag", face="smirk", r=0.7, d=1.6)],
              cards=[dict(text="New Amsterdam →", big="New York", iso="GBR", d=4.6)]),
         dict(say="In 1667, the Treaty of Breda made it official. England kept New York.",
              date="1667", arrows=[], cards=[dict(text="Treaty of Breda:", big="England keeps New York", iso="GBR", d=1.0)], cam={"c": [-74.0, 40.7], "s": 18},
              balls=[dict(ll=[-73.75, 40.5], iso="GBR", skin="flag", face="cool", r=0.8, d=2.4)]),
         dict(say="The Dutch kept Run. For them, it looked like the better deal: they controlled the world's nutmeg.",
              pins=[dict(ll=RUN, label="Run", left=True, d=0.4)], balls=[dict(ll=[129.9, -4.35], iso="NLD", skin="flag", face="happy", r=0.8, d=0.8)],
              cards=[dict(text="The Dutch keep:", big="Run + the nutmeg", iso="NLD", d=1.0)], cam={"c": [129.75, -4.5], "s": 22}, date=None),
         dict(say="Then, in the Napoleonic Wars, Britain seized the Spice Islands and carried nutmeg seedlings to its own colonies.",
              date="1810", balls=[], pins=[], cards=[], cam={"c": [106, 1], "s": 1.0},
              arrows=[dict(from_=[129.7, -4.5], to=[80.7, 7.6], color="#ffcf40", d=3.6), dict(from_=[129.7, -4.5], to=[103.8, 1.35], color="#ffcf40", d=4.4)]),
         dict(say="The monopoly was over. Today, Grenada even has a nutmeg on its flag.",
              date=None, arrows=[], cam={"c": [-63.5, 13.5], "s": 3.2}, pins=[dict(ll=GRD, label="Grenada", d=0.6)],
              cards=[dict(text="Grenada's flag:", big="a nutmeg", d=2.2)]),
         dict(say="And the two islands today? Run has about fifteen hundred people.",
              pins=[dict(ll=RUN, label="Run", left=True, d=0.2)], cards=[dict(text="Run today:", big="~1,500 people", iso="IDN", d=1.8)], cam={"c": [129.75, -4.5], "s": 22}),
         dict(say="Manhattan has about one point seven million.",
              pins=[dict(ll=MAN, label="Manhattan", d=0.2)], cards=[dict(text="Manhattan today:", big="~1.7 million", iso="USA", d=0.6)], cam={"c": [-74.0, 40.7], "s": 18}),
     ],
     "1667: in the Treaty of Breda, England kept New Amsterdam (taken in 1664 and renamed New York) and the Dutch kept Run, a tiny island in the Banda Islands, then the world's only source of nutmeg. Then Britain spread nutmeg to its colonies, and Grenada put one on its flag.",
     dict(title="THE DUTCH|TRADED MANHATTAN|FOR THIS ISLAND", c=[129.75, -4.6], s=24, y=0.66, own={"IDN": "IDN"},
          balls=[dict(ll=[130.05, -4.15], iso="NLD", skin="flag", face="smirk", r=120), dict(ll=[129.45, -5.0], iso="GBR", skin="flag", face="rage", r=135)],
          arrows=[dict(from_=[130.1, -4.95], to=[129.72, -4.56])]),
     "2026-11-24T17:00:00Z",
     tags=["manhattan", "new amsterdam", "new york", "nutmeg", "treaty of breda", "dutch history", "spice islands", "indonesia"])

# ---------------------------------------------------------------- 9. Danish West Indies 1917 ($25M in gold) + Greenland side deal
STT = [-64.93, 18.34]
STX = [-64.75, 17.73]
VIC = {"c": [-64.85, 18.05], "s": 42}
save(9, "How Denmark Sold 3 Islands to the US for $25 Million in Gold",
     "DENMARK SOLD|THESE ISLANDS|FOR $25M IN GOLD",
     [
         dict(say="In 1917, Denmark sold three Caribbean islands to the United States for 25 million dollars in gold. Today they're the U.S. Virgin Islands.",
              cam=VIC, date="1917", pins=[dict(ll=STT, label="St. Thomas", left=True, d=2.0), dict(ll=[-64.74, 18.34], label="St. John", d=2.4), dict(ll=STX, label="St. Croix", d=2.8)],
              balls=[dict(ll=[-64.5, 18.0], iso="DNK", skin="flag", face="smirk", r=0.7, d=0.8)], cards=[dict(text="Price:", big="$25 million in gold", iso="USA", d=5.0)]),
         dict(say="America had tried before. In 1867, Denmark agreed to sell two of the islands for seven and a half million. The U.S. Senate never ratified it.",
              date="1867", cards=[dict(text="1867:", big="Senate says no", iso="USA", d=4.4)], balls=[dict(ll=[-64.5, 18.0], iso="DNK", skin="flag", face="shock", r=0.7, d=0)]),
         dict(say="In 1902, they tried again. This time the Danish parliament's upper house blocked it, with a tied vote.",
              date="1902", cards=[dict(text="1902:", big="blocked, 32 to 32", iso="DNK", d=3.4)]),
         dict(say="Then came World War One. Washington feared Germany could take over Denmark, and grab the islands on the route to the Panama Canal.",
              date="1915", cards=[], balls=[], cam={"c": [-30, 30], "s": 0.4}, own={"DEU": "DEU", "DNK": "DNK"},
              arrows=[dict(from_=[10.4, 51.2], to=[10.0, 56.0], color="#ff5a3c", d=4.2), dict(from_=[-64.9, 18.3], to=[-79.7, 9.1], color="#ffcf40", d=6.6)],
              pins=[dict(ll=[-79.7, 9.1], label="Panama Canal", d=6.8)]),
         dict(say="So in August 1916, the two countries signed a treaty in a New York hotel.",
              date="1916", arrows=[], pins=[dict(ll=[-73.98, 40.75], label="New York", d=1.0)], cam={"c": [-74.0, 40.7], "s": 18}),
         dict(say="Danish voters approved it in a referendum. And on March 31st, 1917, the Danish flag came down and the American flag went up.",
              date="31 MARCH 1917", pins=[], cam=VIC, balls=[dict(ll=[-64.5, 18.0], iso="DNK", skin="flag", face="sad", r=0.7, d=0.6), dict(ll=[-65.1, 17.85], iso="USA", skin="flag", face="happy", r=0.7, d=3.8)],
              cards=[dict(text="Every March 31:", big="Transfer Day", iso="USA", d=5.6)]),
         dict(say="Six days later, the United States entered the war.",
              date="6 APRIL 1917", cards=[]),
         dict(say="But here's the twist. During the talks, the U.S. also declared it would not object to Denmark taking control of all of Greenland.",
              date=None, balls=[], cam={"c": [-42, 70], "s": 1.0}, own={"GRL": "DNK", "DNK": "DNK"}, od=2.0,
              cards=[dict(text="The side deal:", big="Greenland → Denmark", iso="DNK", d=3.0)]),
         dict(say="So America got three small islands, and gave up any objection to Denmark owning one of the biggest islands on Earth.",
              cards=[], balls=[dict(ll=[-42, 74], iso="DNK", skin="flag", face="cool", r=0.9, d=2.4)]),
         dict(say="A century later, an American president offered to buy Greenland.",
              date="2019", balls=[dict(ll=[-42, 74], iso="DNK", skin="flag", face="shock", r=0.9, d=0)], cards=[dict(text="2019:", big="\"Can we buy Greenland?\"", iso="USA", d=1.2)]),
     ],
     "1917: Denmark sold St. Thomas, St. John and St. Croix to the United States for $25 million in gold. Earlier deals failed in 1867 (U.S. Senate) and 1902 (a tied vote in Denmark). And in the talks, the U.S. declared it wouldn't object to Denmark extending its control to all of Greenland.",
     dict(title="DENMARK SOLD|THESE ISLANDS|FOR $25M IN GOLD", c=[-64.8, 18.05], s=55, y=0.66,
          balls=[dict(ll=[-64.35, 18.25], iso="DNK", skin="flag", face="smirk", r=120), dict(ll=[-65.25, 17.75], iso="USA", skin="flag", face="happy", r=130)]),
     "2026-11-25T17:00:00Z",
     tags=["us virgin islands", "denmark", "danish west indies", "greenland", "1917", "world war 1", "transfer day"])

# ================================================================ FORMAT v5 (22/11): History Index / History Maps Lore style "Why does…" — strong claim in frame 1, scene change every 1–2 lines
# ---------------------------------------------------------------- 10. Kaliningrad (Königsberg 1255; Potsdam 1945; renamed 1946; cut off 1991; ~15,100 km², ~1 million people; Kant)
KGD = [20.5, 54.7]
save(10, "Why Does Russia Own a Piece of Land Inside the EU?",
     "RUSSIA OWNS|A PIECE OF|THE EU",
     [
         dict(say="This piece of land is surrounded by the European Union. But it belongs to Russia.",
              cam={"c": [21.5, 54.6], "s": 9}, own={"RU-KGD": "RUS", "POL": "POL", "LTU": "LTU", "BLR": "BLR"}, hl=["RU-KGD"],
              balls=[dict(ll=[20.6, 54.75], iso="RUS", skin="flag", face="smirk", r=0.7, d=1.4)]),
         dict(say="Kaliningrad. About a million people, squeezed between Poland and Lithuania.",
              hl=[], cards=[dict(text="Kaliningrad:", big="~1 million people", iso="RUS", d=1.0)],
              balls=[dict(ll=[20.6, 54.75], iso="RUS", skin="flag", face="cool", r=0.7, d=0), dict(ll=[19.6, 53.4], iso="POL", skin="flag", face="shock", r=0.65, d=2.6), dict(ll=[23.6, 55.6], iso="LTU", skin="flag", face="shock", r=0.6, d=3.0)]),
         dict(say="For almost 700 years, it was German. Founded in 1255 as Königsberg, in East Prussia.",
              date="1255", cards=[], balls=[], own={"RU-KGD": "DEU"}, od=0.3, cam={"c": [20.5, 54.7], "s": 16},
              pins=[dict(ll=[20.51, 54.71], label="Königsberg", d=1.6)]),
         dict(say="Then Germany lost World War Two. In 1945, the Allies handed the city to the Soviet Union.",
              date="1945", own={"RU-KGD": "SOV"}, od=1.2, cam={"c": [25, 54], "s": 4.0}, pins=[],
              arrows=[dict(from_=[37.6, 55.75], to=[20.6, 54.7], color="#ff5a3c", d=1.0)]),
         dict(say="A year later, it was renamed Kaliningrad. The Germans were expelled, and Russians moved in.",
              date="1946", arrows=[], cards=[dict(text="1946:", big="Königsberg → Kaliningrad", iso="SOV", d=1.0)]),
         dict(say="It made sense when Lithuania was Soviet too. Then in 1991, the Soviet Union collapsed.",
              date="1991", cards=[], own={"RU-KGD": "RUS", "LTU": "LTU"}, od=1.6, cam={"c": [25, 55], "s": 3.4},
              balls=[dict(ll=[24.0, 55.4], iso="LTU", skin="flag", face="happy", r=0.7, d=2.2)]),
         dict(say="Overnight, Kaliningrad was cut off from Russia. Today, every road to it from Russia crosses EU territory.",
              date=None, balls=[], hl=["RU-KGD"], arrows=[dict(from_=[30.5, 55.5], to=[21.2, 54.8], color="#ffcf40", d=2.0)]),
         dict(say="And its ice-free port is key for Russia's Baltic Fleet.",
              hl=[], arrows=[], cam={"c": [20.2, 54.75], "s": 18}, pins=[dict(ll=[19.9, 54.64], label="Baltiysk", left=True, d=0.6)],
              cards=[dict(text="Ice-free port:", big="key for the Baltic Fleet", iso="RUS", d=1.8)]),
         dict(say="Oh, and the philosopher Immanuel Kant? Born and buried right here, when it was still Königsberg.",
              pins=[dict(ll=[20.51, 54.71], label="Kant's Königsberg", d=1.0)], cards=[]),
     ],
     "Kaliningrad: about 15,000 km² and a million people between Poland and Lithuania. German Königsberg for almost 700 years, handed to the USSR in 1945, renamed in 1946, and cut off from Russia when the Soviet Union collapsed in 1991.",
     dict(title="RUSSIA OWNS|A PIECE OF|THE EU", c=[21.6, 54.4], s=8, y=0.66, own={"RU-KGD": "RUS", "POL": "POL", "LTU": "LTU"},
          balls=[dict(ll=[20.4, 54.85], iso="RUS", skin="flag", face="smirk", r=120), dict(ll=[20.2, 53.4], iso="POL", skin="flag", face="shock", r=115), dict(ll=[23.8, 55.5], iso="LTU", skin="flag", face="shock", r=105)]),
     "2026-11-22T14:00:00Z",
     tags=["kaliningrad", "russia", "konigsberg", "european union", "poland", "lithuania", "baltic fleet", "east prussia"])

# ---------------------------------------------------------------- 11. Why Chile is so long (≈4,270 km long, ≈177 km wide on average; War of the Pacific)
save(11, "Why Is Chile So Long and Thin?",
     "4,270 KM LONG.|177 KM WIDE.|HOW?",
     [
         dict(say="Chile is about 4,270 kilometers long, but on average just 177 kilometers wide. How did a country end up shaped like this?",
              cam={"c": [-70, -37], "s": 1.35}, own={"CHL": "CHL", "ARG": "ARG", "BOL": "BOL", "PER": "PER"}, hl=["CHL"],
              cards=[dict(text="Length:", big="~4,270 km", iso="CHL", d=3.0), dict(text="Average width:", big="~177 km", iso="CHL", d=5.0)]),
         dict(say="Blame the Andes. One of the highest mountain ranges on Earth runs down its entire east side.",
              hl=[], cards=[], cam={"c": [-69.5, -30], "s": 3.0},
              line=dict(lon=-69.8, color="#ffffff", d=0.6)),
         dict(say="The Spanish ran this strip between the mountains and the Pacific as its own colony. East of the mountains became Argentina.",
              line=None, balls=[dict(ll=[-71.5, -33.5], iso="CHL", skin="flag", face="cool", r=0.7, d=1.6), dict(ll=[-64.5, -34], iso="ARG", skin="flag", face="smirk", r=0.8, d=3.6)]),
         dict(say="And the north? That wasn't even Chile's. The Atacama desert belonged to Bolivia and Peru.",
              balls=[], cam={"c": [-69.5, -22], "s": 4.0}, own={"CHL": "CHL"},
              zones=[dict(coords=[[-70.15, -21.45], [-70.2, -22.4], [-70.35, -23.5], [-70.6, -24.6], [-70.5, -25.4], [-68.4, -25.4], [-67.6, -23.8], [-68.0, -22.4], [-68.2, -21.45]], iso="BOL", op=0.95, d=1.2)]),
         dict(say="Then came the War of the Pacific. Chile won, took the coast, and left Bolivia with no sea at all.",
              date="1879", zones=[dict(coords=[[-70.15, -21.45], [-70.2, -22.4], [-70.35, -23.5], [-70.6, -24.6], [-70.5, -25.4], [-68.4, -25.4], [-67.6, -23.8], [-68.0, -22.4], [-68.2, -21.45]], iso="CHL", op=0.95, d=1.0)],
              balls=[dict(ll=[-71.3, -24], iso="CHL", skin="flag", face="cool", r=0.75, d=1.0), dict(ll=[-65.8, -18.2], iso="BOL", skin="flag", face="sad", r=0.7, d=2.6)]),
         dict(say="That's why Chile has one of the driest places on Earth at one end, and glaciers at the other.",
              date=None, balls=[], zones=[], cam={"c": [-70, -37], "s": 1.35}, pins=[dict(ll=[-69.5, -23.8], label="Atacama", d=1.6), dict(ll=[-73.3, -50.5], label="Patagonian ice fields", left=True, d=3.2)]),
         dict(say="Laid across Europe, Chile would reach from Lisbon past Moscow. Which country is shaped weirder?",
              pins=[], cards=[dict(text="Laid across Europe:", big="Lisbon → past Moscow", iso="CHL", d=1.4)]),
     ],
     "Chile is about 4,270 km long and only 177 km wide on average: the Andes on one side, the Pacific on the other, and a northern desert it took from Bolivia and Peru in the War of the Pacific.",
     dict(title="4,270 KM LONG.|177 KM WIDE.|HOW?", c=[-68.0, -35.0], s=1.45, y=0.68, own={"CHL": "CHL", "ARG": "ARG", "BOL": "BOL", "PER": "PER"},
          balls=[dict(ll=[-63.5, -33.0], iso="CHL", skin="flag", face="shock", r=130)]),
     "2026-11-23T14:00:00Z",
     tags=["chile", "geography", "andes", "atacama", "war of the pacific", "south america", "maps"])

# ---------------------------------------------------------------- 12. Ceuta & Melilla (Melilla Spanish since 1497; Ceuta Portuguese 1415, Spanish by 1668 Treaty of Lisbon; ~18.5 & 12.3 km²; ~84k & ~87k people; Morocco claims both)
CEU = [-5.32, 35.89]
MEL = [-2.94, 35.29]
save(12, "Why Does Spain Still Own Two Cities in Africa?",
     "SPAIN STILL OWNS|TWO CITIES|IN AFRICA",
     [
         dict(say="Spain has two cities on the African continent. Surrounded by Morocco on land, and by the sea.",
              cam={"c": [-4.2, 35.6], "s": 9}, own={"ESP": "ESP", "MAR": "MAR"},
              pins=[dict(ll=CEU, label="Ceuta", left=True, d=1.6), dict(ll=MEL, label="Melilla", d=2.2)],
              balls=[dict(ll=[-4.6, 34.6], iso="MAR", skin="flag", face="angry", r=0.8, d=3.0)]),
         dict(say="Melilla has been Spanish since 1497. Just five years after Columbus reached the Americas.",
              date="1497", balls=[], cam={"c": [-2.94, 35.29], "s": 40}, pins=[dict(ll=MEL, label="Melilla", d=0.2)],
              cards=[dict(text="Spanish since:", big="1497", iso="ESP", d=1.0)]),
         dict(say="Ceuta was taken by Portugal in 1415. Portugal handed it to Spain by treaty in 1668.",
              date="1415", cam={"c": [-5.32, 35.89], "s": 40}, pins=[dict(ll=CEU, label="Ceuta", d=0.2)], cards=[],
              balls=[dict(ll=[-5.22, 35.96], iso="PRT", skin="flag", face="cool", r=0.65, d=0.6), dict(ll=[-5.42, 35.82], iso="ESP", skin="flag", face="happy", r=0.65, d=3.6)]),
         dict(say="Both are tiny. Ceuta is about eighteen square kilometers, Melilla about twelve. Around 85,000 people each.",
              date=None, balls=[], cam={"c": [-4.2, 35.6], "s": 9}, pins=[dict(ll=CEU, label="Ceuta · 18.5 km²", left=True, d=0.4), dict(ll=MEL, label="Melilla · 12.3 km²", d=1.4)],
              cards=[dict(text="Population:", big="~85,000 each", iso="ESP", d=3.4)]),
         dict(say="Morocco calls them occupied and wants them back. Spain says they've been Spain for centuries.",
              cards=[], balls=[dict(ll=[-4.6, 34.6], iso="MAR", skin="flag", face="angry", r=0.85, d=0.2), dict(ll=[-4.0, 36.9], iso="ESP", skin="flag", face="smirk", r=0.85, d=2.0)]),
         dict(say="Melilla's border is a double fence about six meters tall. Since 2020, parts are being raised above ten.",
              balls=[], cam={"c": [-2.94, 35.29], "s": 40}, pins=[dict(ll=MEL, label="Melilla", d=0.2)], cards=[dict(text="Border fence:", big="6 m → 10 m+", iso="ESP", d=2.0)]),
         dict(say="So yes: the European Union has a land border with Africa. Should Spain keep them?",
              cards=[], cam={"c": [-4.2, 35.6], "s": 9}, balls=[dict(ll=[-4.6, 34.6], iso="MAR", skin="flag", face="smirk", r=0.8, d=0.3), dict(ll=[-4.0, 36.9], iso="ESP", skin="flag", face="smirk", r=0.8, d=0.6)]),
     ],
     "Ceuta and Melilla: two Spanish cities on the north coast of Africa. Melilla has been Spanish since 1497; Ceuta was taken by Portugal in 1415 and passed to Spain by the Treaty of Lisbon in 1668. About 85,000 people each, and Morocco wants both back.",
     dict(title="SPAIN STILL OWNS|TWO CITIES|IN AFRICA", c=[-4.2, 35.5], s=8, y=0.66, own={"ESP": "ESP", "MAR": "MAR"},
          balls=[dict(ll=[-4.8, 34.4], iso="MAR", skin="flag", face="angry", r=125), dict(ll=[-3.6, 37.0], iso="ESP", skin="flag", face="smirk", r=120)]),
     "2026-11-24T14:00:00Z",
     tags=["ceuta", "melilla", "spain", "morocco", "africa", "european union", "geography", "borders"])

# ---------------------------------------------------------------- 13. Lesotho (enclaved by South Africa; ~30,355 km²; ~2.1–2.3M; lowest point 1,400 m — highest low point of any country; Moshoeshoe I; British protectorate 1868; independent 4 Oct 1966)
LSOC = [28.25, -29.6]
save(13, "Why Is This Country Completely Inside Another Country?",
     "THIS COUNTRY IS|COMPLETELY INSIDE|ANOTHER ONE",
     [
         dict(say="This whole country is completely surrounded by another country. It's called Lesotho, and it sits inside South Africa.",
              cam={"c": [26, -29], "s": 3.0}, own={"LSO": "LSO", "ZAF": "ZAF"}, hl=["LSO"],
              balls=[dict(ll=[28.3, -29.5], iso="LSO", skin="flag", face="shock", r=0.6, d=1.6), dict(ll=[24.5, -31.5], iso="ZAF", skin="flag", face="smirk", r=0.8, d=3.4)]),
         dict(say="It's the biggest country in the world fully enclosed by just one other. About the size of Belgium.",
              hl=[], cards=[dict(text="Lesotho:", big="~30,000 km² ≈ Belgium", iso="LSO", d=1.4)]),
         dict(say="And it's all mountains. Its lowest point is 1,400 meters up. That's the highest low point of any country on Earth.",
              cards=[dict(text="Lowest point:", big="1,400 m", iso="LSO", d=1.4)], cam={"c": [28.3, -29.6], "s": 9}, balls=[]),
         dict(say="In the 1820s, a chief named Moshoeshoe gathered the Basotho people in these mountains.",
              cards=[], date="1820s", balls=[dict(ll=[28.0, -29.4], iso="LSO", skin="flag", face="cool", r=0.7, d=0.8)]),
         dict(say="Then the Boers came for their land. So in 1868, Moshoeshoe asked Britain for protection.",
              date="1868", balls=[dict(ll=[28.0, -29.4], iso="LSO", skin="flag", face="shock", r=0.7, d=0), dict(ll=[26.2, -28.4], iso="ZAF", skin="flag", face="angry", r=0.75, d=0.8), dict(ll=[29.6, -30.6], iso="GBR", skin="flag", face="cool", r=0.7, d=3.0)]),
         dict(say="It worked. Lesotho stayed a separate British territory, and became independent in 1966.",
              date="1966", cards=[dict(text="4 October 1966:", big="independence", iso="LSO", d=2.4)], balls=[dict(ll=[28.0, -29.4], iso="LSO", skin="flag", face="happy", r=0.75, d=0.6)]),
         dict(say="So today, to leave Lesotho by land, you always cross into South Africa. Would you live in a country like that?",
              date=None, cards=[], cam={"c": [26, -29], "s": 3.0}, hl=["LSO"], balls=[dict(ll=[28.3, -29.5], iso="LSO", skin="flag", face="smirk", r=0.6, d=0.4)]),
     ],
     "Lesotho is completely surrounded by South Africa: about 30,000 km², all mountains (its lowest point is 1,400 m, the highest low point of any country). Moshoeshoe I united the Basotho in the 1820s, asked Britain for protection from the Boers in 1868, and Lesotho became independent on 4 October 1966.",
     dict(title="THIS COUNTRY IS|COMPLETELY INSIDE|ANOTHER ONE", c=[27.0, -29.8], s=3.4, y=0.68, own={"LSO": "LSO", "ZAF": "ZAF"},
          balls=[dict(ll=[28.3, -29.5], iso="LSO", skin="flag", face="shock", r=110), dict(ll=[24.8, -31.6], iso="ZAF", skin="flag", face="smirk", r=125)]),
     "2026-11-25T14:00:00Z",
     tags=["lesotho", "south africa", "enclave", "geography", "africa", "borders", "maps"])

# ---------------------------------------------------------------- 14. Northwest Angle (1783 Treaty of Paris + Mitchell Map; Lake of the Woods; only contiguous-US land north of 49th; by land only via Manitoba; 149 people in 2020; check-in kiosk)
NWA = [-95.1, 49.33]
save(14, "Why Can You Only Drive to This Part of the US Through Canada?",
     "TO DRIVE HERE|FROM THE US, YOU|GO THROUGH CANADA",
     [
         dict(say="To drive to this part of Minnesota, you have to go through Canada first.",
              cam={"c": [-95.0, 49.1], "s": 30}, own={"USA": "USA", "CAN": "CAN"}, pins=[dict(ll=NWA, label="Northwest Angle", d=0.6)],
              arrows=[dict(from_=[-95.3, 48.9], to=[-95.3, 49.25], d=1.6, color="#ffcf40")]),
         dict(say="It's the Northwest Angle. The only piece of the lower 48 states north of the 49th parallel.",
              arrows=[], cards=[dict(text="Northwest Angle:", big="north of the 49th", iso="USA", d=1.0)], cam={"c": [-96, 48.5], "s": 6},
              ),
         dict(say="Blame a bad map. In 1783, the treaty that ended the American Revolution drew the border through the Lake of the Woods.",
              cards=[], date="1783", cam={"c": [-95.0, 49.1], "s": 30}),
         dict(say="The negotiators used the Mitchell Map. It got the lake and the Mississippi's source wrong.",
              cards=[dict(text="The map they used:", big="wrong lake, wrong river", d=1.2)]),
         dict(say="When surveyors finally fixed the line, this little corner ended up cut off, with the lake on one side and Canada on the other.",
              date=None, cards=[], balls=[dict(ll=[-95.0, 49.5], iso="CAN", skin="flag", face="smirk", r=0.7, d=1.4), dict(ll=[-95.2, 49.3], iso="USA", skin="flag", face="shock", r=0.6, d=2.6)]),
         dict(say="About 150 people live there. And to enter, they check in at a kiosk instead of a border guard.",
              cards=[dict(text="Population (2020):", big="149", iso="USA", d=0.8)]),
         dict(say="The other options? A boat, a plane, or in winter, a road built on the frozen lake. Would you live there?",
              cards=[], balls=[dict(ll=[-95.2, 49.3], iso="USA", skin="flag", face="cool", r=0.6, d=0.2)]),
     ],
     "The Northwest Angle, Minnesota: the only part of the contiguous US north of the 49th parallel, reachable by land only through Manitoba. A 1783 treaty drew the border through Lake of the Woods using the faulty Mitchell Map; 149 people lived there in 2020.",
     dict(title="TO DRIVE HERE|FROM THE US, YOU|GO THROUGH CANADA", c=[-95.1, 49.15], s=26, y=0.66, own={"USA": "USA", "CAN": "CAN"},
          balls=[dict(ll=[-94.75, 49.55], iso="CAN", skin="flag", face="smirk", r=120), dict(ll=[-95.15, 49.3], iso="USA", skin="flag", face="shock", r=105)]),
     "2026-11-26T14:00:00Z",
     tags=["northwest angle", "minnesota", "canada", "border", "lake of the woods", "maps", "geography"])

# ---------------------------------------------------------------- 15. France's longest land border is with Brazil (French Guiana; Oiapoque; ~730 km; euro; Kourou)
save(15, "France's Longest Land Border Isn't in Europe",
     "FRANCE'S LONGEST|LAND BORDER IS|WITH BRAZIL",
     [
         dict(say="France's longest land border isn't with Spain, Belgium or Germany. It's with Brazil.",
              cam={"c": [-25, 15], "s": 0.55}, own={"FRA": "FRA", "BRA": "BRA", "FR-GF": "FRA"},
              balls=[dict(ll=[2.3, 46.5], iso="FRA", skin="flag", face="smirk", r=0.6, d=0.6), dict(ll=[-50, -8], iso="BRA", skin="flag", face="shock", r=0.8, d=2.4)]),
         dict(say="Because this piece of South America is France. French Guiana.",
              balls=[], cam={"c": [-53, 3.6], "s": 5}, hl=["FR-GF"], cards=[dict(text="French Guiana:", big="part of France", iso="FRA", d=1.0)]),
         dict(say="Not a colony. A full part of the country, with French laws, French elections and the euro.",
              hl=[], cards=[dict(text="Currency:", big="the euro", iso="FRA", d=1.8)]),
         dict(say="Its border with Brazil runs along the Oyapock river for about 730 kilometers.",
              cards=[dict(text="Border with Brazil:", big="~730 km", iso="BRA", d=1.6)], pins=[dict(ll=[-51.8, 3.85], label="Oyapock river", d=0.6)]),
         dict(say="Brazil and France even built a bridge over that river. That makes it a land border between Brazil and the European Union.",
              pins=[dict(ll=[-51.83, 3.88], label="Oyapock bridge", d=0.4)], cards=[]),
         dict(say="And Europe launches its rockets from here, at Kourou, near the equator.",
              pins=[dict(ll=[-52.65, 5.16], label="Kourou spaceport", left=True, d=0.6)], cam={"c": [-52.8, 4.6], "s": 10}),
         dict(say="Did you know France was Brazil's neighbor?",
              pins=[], cam={"c": [-53, 3.6], "s": 5}, balls=[dict(ll=[-53.1, 4.0], iso="FRA", skin="flag", face="smirk", r=0.7, d=0.2), dict(ll=[-51.5, 1.0], iso="BRA", skin="flag", face="happy", r=0.75, d=0.6)]),
     ],
     "France's longest land border is with Brazil: about 730 km along the Oyapock river, because French Guiana is a full part of France (and of the EU, using the euro). Europe also launches rockets from Kourou.",
     dict(title="FRANCE'S LONGEST|LAND BORDER IS|WITH BRAZIL", c=[-52.5, 2.6], s=4.4, y=0.66, own={"FRA": "FRA", "BRA": "BRA", "FR-GF": "FRA"},
          balls=[dict(ll=[-53.2, 4.3], iso="FRA", skin="flag", face="smirk", r=115), dict(ll=[-51.0, 0.2], iso="BRA", skin="flag", face="shock", r=130)]),
     "2026-11-26T17:00:00Z",
     tags=["france", "brazil", "french guiana", "borders", "geography", "european union", "kourou"])

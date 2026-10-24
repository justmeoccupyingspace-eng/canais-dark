"""Semana 26/10-01/11 (v3): 14 Chartbound + 14 How It Ticks. Uso: python3 specs/week44.py -> specs/v3/*.json"""
import json, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v3')
os.makedirs(OUT, exist_ok=True)
V = []


def save(name, spec):
    json.dump(spec, open(f'{OUT}/{name}.json', 'w'), ensure_ascii=False, indent=1)
    V.append(name)


def end(text, hl, narration):
    return {'type': 'end', 'text': text, 'hl': hl, 'narration': narration, 'min_duration': 2.2}


def A(name, at, title, tags, desc, compute, scenes):
    save(name, {'channel': 'chartbound', 'style': 'v3', 'rate': '+9%', 'title': title,
                'publish': {'channel': 'A', 'privacy': 'public', 'at': at}, 'compute': compute,
                'yt': {'title': title, 'description': desc + "\nNarration is AI-generated.", 'tags': tags, 'lang': 'en'}, 'scenes': scenes})


def B(name, at, kind, title, tags, desc, scenes):
    save(name, {'channel': 'howitticks', 'style': 'v3', 'rate': '+6%', 'title': title,
                'publish': {'channel': 'B', 'privacy': 'public', 'at': at}, 'compute': {'calc': {'kind': kind}},
                'yt': {'title': title, 'description': desc + "\nNarration is AI-generated.", 'tags': tags, 'lang': 'en'}, 'scenes': scenes})


# ======================= Chartbound =======================
def ratio(name, at, a, fa, b, fb, a3, b3, gdp, bars_n, big, text, end_t, end_hl, end_n, short_a=None):
    ind = 'NY.GDP.MKTP.CD' if gdp else 'SP.POP.TOTL'
    sa = short_a or a
    bl = b.replace('The ', 'the ')
    bp = bl + ("'" if bl.endswith('s') else "'s")
    hook_text = f"{sa}'s economy was {{wr_r0}}% of {bp}" if gdp else f"{sa} had {{wr_r0}}% of {bp} people"
    hook_n = f"In {{wr_from}}, {a.replace('The ', 'the ')} was {{wr_r0_say}} percent of {bl}." if gdp else f"In {{wr_from}}, {a.replace('The ', 'the ')} had {{wr_r0_say}} percent of {bp} people."
    title = (f"{sa}'s economy was {{wr_r0}}% of {bp} in {{wr_from}}. Now? #Shorts" if gdp else f"{sa} had {{wr_r0}}% of {bp} population in {{wr_from}}. Now? #Shorts")
    what = 'economy' if gdp else 'population'
    A(name, at, title, ['economics' if gdp else 'population', a.lower().replace('the ', ''), b.lower(), 'data', 'worldbank'],
      f"{a} as a share of {b}, {what}, {{wr_from}} vs {{wr_to}}. Source: World Bank ({ind}).",
      {'wbratio': {'ind': ind, 'a': a3, 'b': b3, 'from': 2000, 'an': sa, 'bn': b}},
      [{'type': 'hook', 'kicker': 'In {wr_from}', 'text': hook_text, 'hl': '{wr_r0}%', 'vs': [{'flag': fa, 'name': sa}, {'flag': fb, 'name': b}], 'narration': hook_n, 'min_duration': 3.0},
       {'type': 'bars', **({'style': 'coins'} if gdp else {}), 'kicker': f"{sa} as % of {bl}", 'text': 'Now watch', 'hl': 'watch', 'suffix': '%', 'vals_from': 'wr_v', 'labels_from': 'wr_y', 'narration': bars_n, 'min_duration': 4.4},
       big, text, end(end_t, end_hl, end_n)])


def quiz(name, at, a, fa, b, fb, a3, b3, gdp, question, hook_text, hook_hl, reveal_n, text, end_t, end_hl, end_n):
    ind = 'NY.GDP.MKTP.CD' if gdp else 'SP.POP.TOTL'
    A(name, at, f"{question} #Shorts", ['quiz', 'economics' if gdp else 'population', a.lower(), b.lower(), 'data'],
      f"{a} vs {b}, {'GDP (current US$)' if gdp else 'population'}, {{wr_from}} to {{wr_to}}. Source: World Bank ({ind}).",
      {'wbratio': {'ind': ind, 'a': a3, 'b': b3, 'from': 2000, 'an': a, 'bn': b}},
      [{'type': 'hook', 'kicker': 'Quick quiz', 'text': hook_text, 'hl': hook_hl, 'vs': [{'flag': fa, 'name': a}, {'flag': fb, 'name': b}], 'narration': f"{question} Think fast.", 'min_duration': 2.6},
       {'type': 'quiz', 'label': 'GUESS', 'q': question, 'alts': [f"{fa} {a}", f"{fb} {b}"], 'correct_from': 'wr_big', 'narration': 'Lock in your answer.', 'extra': 4.6, 'revealFromEnd': 1.6, 'countdown': 3, 'qsize': 64, 'asize': 60, 'cta': 'Comment your guess'},
       {'type': 'bars', **({'style': 'coins'} if gdp else {}), 'kicker': f"{a} as % of {b}", 'text': "It's {wr_win}", 'hl': '{wr_win}', 'suffix': '%', 'vals_from': 'wr_v', 'labels_from': 'wr_y', 'narration': reveal_n, 'min_duration': 4.4},
       text, end(end_t, end_hl, end_n)])


def series(name, at, title, tags, desc, ind, c3, years, dec, prefix, suffix, scale, hook, bars_text, bars_hl, bars_n, big, text, end_t, end_hl, end_n):
    comp = {'wbseries': {'ind': ind, 'c': c3, 'from': years[0] if years[0] != 'last' else 1960, 'years': years, 'dec': dec, 'scale': scale}}
    A(name, at, title, tags, desc, comp,
      [hook,
       {'type': 'bars', 'kicker': bars_text[0], 'text': bars_text[1], 'hl': bars_hl, 'prefix': prefix, 'suffix': suffix, 'dec': dec, 'vals_from': 'ws_v', 'labels_from': 'ws_y', 'narration': bars_n, 'min_duration': 4.6},
       big, text, end(end_t, end_hl, end_n)])


T = lambda t, hl, icon, n, pose=None, md=3.2: {'type': 'text', 'text': t, 'hl': hl, 'icon': icon, 'narration': n, 'min_duration': md, **({'pose': pose} if pose else {})}
BIG = lambda t, hl, big, label, n, md=2.8: {'type': 'big', 'text': t, 'hl': hl, 'big': big, 'label': label, 'narration': n, 'min_duration': md}

quiz('a-133-drcongo-germany', '2026-10-26T16:00:00Z', 'DR Congo', '🇨🇩', 'Germany', '🇩🇪', 'COD', 'DEU', False,
     'Which has more people: DR Congo or Germany?', 'More people: DR Congo or Germany?', 'More people:',
     "It's {wr_win}. {wr_a_m_say} million people versus {wr_b_m_say} million.",
     T('It doubled since {wr_from}', 'doubled', '👶', "DR Congo has doubled since {wr_from}. Germany barely moved.", 'shock'),
     'Did you get it right?', 'right?', 'Did you get it right? Comment below.')
ratio('a-128-bangladesh-russia', '2026-10-26T23:00:00Z', 'Bangladesh', '🇧🇩', 'Russia', '🇷🇺', 'BGD', 'RUS', False,
      "Then Bangladesh kept growing while Russia shrank. Today: {wr_r1_say} percent.",
      BIG('Bangladesh today', 'today', '{wr_a_m}M', 'people, vs {wr_b_m}M in Russia', "That's {wr_a_m_say} million people, in a country about the size of Iowa."),
      T('Russia is shrinking', 'shrinking', '📉', "Russia has fewer people than in {wr_from}.", 'shrug'),
      'Which pair next?', 'next?', 'Which two countries should I compare next?')
series('a-137-korea-fertility', '2026-10-27T16:00:00Z', "South Korea went from 6 kids per woman to {ws_v1} #Shorts", ['population', 'southkorea', 'fertility', 'data'],
       "Fertility rate (births per woman), South Korea. Source: World Bank (SP.DYN.TFRT.IN).", 'SP.DYN.TFRT.IN', 'KOR', [1960, 1980, 2000, 'last'], 1, '', '', 1,
       {'type': 'hook', 'kicker': 'South Korea', 'text': 'From 6 kids per woman to {ws_v1}', 'hl': '{ws_v1}', 'icon': '🇰🇷', 'narration': "In {ws_y0}, the average South Korean woman had {ws_v0_say} kids. Now?", 'min_duration': 3.0},
       ('Births per woman', 'Watch it fall'), 'fall', "Then it fell, and fell. Now it's {ws_v1_say}. The lowest in the world.",
       BIG('A stable population needs', 'needs', '2.1', 'kids per woman', "To stay the same size, a country needs about two point one."),
       T('Each generation: about 1/3 the size', '1/3', '📉', "At this rate, each generation is about a third the size of the last.", 'shock'),
       'What would fix it?', 'fix it?', 'What do you think would fix it?')
ratio('a-127-vietnam-philippines', '2026-10-27T23:00:00Z', 'Vietnam', '🇻🇳', 'The Philippines', '🇵🇭', 'VNM', 'PHL', True,
      "Then Vietnam took off. Today: {wr_r1_say} percent.",
      BIG("Vietnam's economy grew", 'grew', '{wr_d} pts', 'on the Philippines since {wr_from}', "Vietnam gained {wr_d_say} points.", 2.8),
      T('Factories moved in', 'Factories', '🏭', "Electronics factories moved in. Exports exploded.", 'shrug'),
      'Which pair next?', 'next?', 'Which two countries should I compare next?', short_a='Vietnam')
quiz('a-134-brazil-canada', '2026-10-28T16:00:00Z', 'Brazil', '🇧🇷', 'Canada', '🇨🇦', 'BRA', 'CAN', True,
     'Which economy is bigger: Brazil or Canada?', 'Bigger economy: Brazil or Canada?', 'Bigger economy:',
     "It's {wr_win}. Brazil is {wr_r1_say} percent of Canada.",
     T('5x the people, similar economy', 'similar', '⚖️', "Brazil has five times the people, but the economies are close in size.", 'shrug'),
     'Did you get it right?', 'right?', 'Did you get it right? Comment below.')
ratio('a-129-egypt-germany', '2026-10-28T23:00:00Z', 'Egypt', '🇪🇬', 'Germany', '🇩🇪', 'EGY', 'DEU', False,
      "Then Egypt kept growing. Today: {wr_r1_say} percent.",
      BIG('Egypt today', 'today', '{wr_a_m}M', 'people, vs {wr_b_m}M in Germany', "That's {wr_a_m_say} million people versus {wr_b_m_say} million."),
      T('Almost all live along the Nile', 'the Nile', '🌊', "And almost all of them live along the Nile.", 'shrug'),
      'Which pair next?', 'next?', 'Which two countries should I compare next?')
series('a-138-china-income', '2026-10-29T16:00:00Z', "China's income per person grew {ws_x}x since {ws_y0} #Shorts", ['economics', 'china', 'gdppercapita', 'data'],
       "GDP per capita (current US$), China. Source: World Bank (NY.GDP.PCAP.CD).", 'NY.GDP.PCAP.CD', 'CHN', [1990, 2000, 2010, 'last'], 0, '$', '', 1,
       {'type': 'hook', 'kicker': 'China', 'text': 'Income per person: ${ws_v0} in {ws_y0}', 'hl': '${ws_v0}', 'icon': '🇨🇳', 'narration': "In {ws_y0}, China's income per person was {ws_v0_say} dollars a year.", 'min_duration': 3.0},
       ('GDP per person, US$', 'Now watch'), 'watch', "Today it's {ws_v1_say} dollars.",
       BIG('That is', 'That is', '{ws_x}x', 'more in {ws_y1} than in {ws_y0}', "That's {ws_x_say} times more."),
       T('Still below the US', 'below', '🇺🇸', "Still, America's income per person is about six times higher.", 'shrug'),
       'Which country next?', 'next?', 'Which country should I chart next?')
ratio('a-130-ethiopia-japan', '2026-10-29T23:00:00Z', 'Ethiopia', '🇪🇹', 'Japan', '🇯🇵', 'ETH', 'JPN', False,
      "Then Ethiopia caught up. Today: {wr_r1_say} percent.",
      BIG('Ethiopia today', 'today', '{wr_a_m}M', 'people, vs {wr_b_m}M in Japan', "That's {wr_a_m_say} million people versus {wr_b_m_say} million."),
      T('Japan is shrinking', 'shrinking', '👴', "Japan is getting older and smaller. Ethiopia is young.", 'shrug'),
      'Which pair next?', 'next?', 'Which two countries should I compare next?')
quiz('a-135-vietnam-germany', '2026-10-30T16:00:00Z', 'Vietnam', '🇻🇳', 'Germany', '🇩🇪', 'VNM', 'DEU', False,
     'Which has more people: Vietnam or Germany?', 'More people: Vietnam or Germany?', 'More people:',
     "It's {wr_win}. {wr_a_m_say} million versus {wr_b_m_say} million.",
     T('Smaller country, more people', 'more people', '🗺️', "And Vietnam is even a bit smaller than Germany in area.", 'shrug'),
     'Did you get it right?', 'right?', 'Did you get it right? Comment below.')
ratio('a-131-indonesia-brazil', '2026-10-30T23:00:00Z', 'Indonesia', '🇮🇩', 'Brazil', '🇧🇷', 'IDN', 'BRA', True,
      "Then Indonesia kept closing in. Today: {wr_r1_say} percent.",
      BIG('Indonesia gained', 'gained', '+{wr_d} pts', 'on Brazil since {wr_from}', "Indonesia gained {wr_d_say} points.", 2.8),
      T('280 million people, 17,000 islands', '17,000 islands', '🏝️', "Two hundred eighty million people, across seventeen thousand islands.", 'shrug'),
      'Which pair next?', 'next?', 'Which two countries should I compare next?')
series('a-139-japan-population', '2026-10-31T16:00:00Z', "Japan's population peaked. Here's the chart #Shorts", ['population', 'japan', 'demographics', 'data'],
       "Population, total, Japan. Source: World Bank (SP.POP.TOTL).", 'SP.POP.TOTL', 'JPN', [1960, 1990, 2010, 'last'], 0, '', 'M', 1e6,
       {'type': 'hook', 'kicker': 'Japan', 'text': 'Japan is losing people every year', 'hl': 'losing people', 'icon': '🇯🇵', 'narration': "Japan is losing people every single year.", 'min_duration': 2.8},
       ('Population, millions', 'Up, then down'), 'down', "It grew from {ws_v0_say} million to a peak around {ws_max_y}. Now it's {ws_v1_say} million.",
       BIG('Peak year', 'Peak', '{ws_max_y}', 'and falling since', "The peak was around {ws_max_y}."),
       T('More deaths than births', 'deaths', '👴', "Now there are more deaths than births, every year.", 'shock'),
       'Who is next?', 'next?', 'Which country do you think is next?')
ratio('a-132-mexico-russia', '2026-10-31T23:00:00Z', 'Mexico', '🇲🇽', 'Russia', '🇷🇺', 'MEX', 'RUS', False,
      "Then Mexico kept closing in. Today: {wr_r1_say} percent.",
      BIG('Mexico today', 'today', '{wr_a_m}M', 'people, vs {wr_b_m}M in Russia', "That's {wr_a_m_say} million versus {wr_b_m_say} million."),
      T('Russia is 9x bigger in area', '9x', '🗺️', "And Russia is about nine times bigger in area.", 'shrug'),
      'Which pair next?', 'next?', 'Which two countries should I compare next?')
quiz('a-136-mexico-spain', '2026-11-01T16:00:00Z', 'Mexico', '🇲🇽', 'Spain', '🇪🇸', 'MEX', 'ESP', True,
     'Which economy is bigger: Mexico or Spain?', 'Bigger economy: Mexico or Spain?', 'Bigger economy:',
     "It's {wr_win}. Mexico is {wr_r1_say} percent of Spain.",
     T('With a third of the people', 'a third', '🧮', "And Spain does it with about a third of Mexico's people.", 'shrug'),
     'Did you get it right?', 'right?', 'Did you get it right? Comment below.')
series('a-140-india-lifeexp', '2026-11-01T23:00:00Z', "India's life expectancy: {ws_v0} to {ws_v1} years #Shorts", ['health', 'india', 'lifeexpectancy', 'data'],
       "Life expectancy at birth, India. Source: World Bank (SP.DYN.LE00.IN).", 'SP.DYN.LE00.IN', 'IND', [1960, 1980, 2000, 'last'], 0, '', ' yrs', 1,
       {'type': 'hook', 'kicker': 'India', 'text': 'In {ws_y0}, Indians lived {ws_v0} years', 'hl': '{ws_v0} years', 'icon': '🇮🇳', 'narration': "In {ws_y0}, the average Indian lived just {ws_v0_say} years.", 'min_duration': 3.0},
       ('Life expectancy, years', 'Now watch'), 'watch', "Today it's {ws_v1_say}.",
       BIG('That is', 'That is', '+{ws_d}', 'years of life, on average', "That's {ws_d_say} extra years of life."),
       T('Vaccines, clean water, fewer famines', 'Vaccines,', '💉', "Vaccines, clean water and the end of big famines did most of it.", 'shrug'),
       'Which country next?', 'next?', 'Which country should I chart next?')

# ======================= How It Ticks =======================
Q = lambda label, q_, alts, correct, n, cta='Comment your guess': {'type': 'quiz', 'label': label, 'q': q_, 'alts': alts, 'correct': correct, 'narration': n, 'extra': 4.6, 'revealFromEnd': 1.6, 'countdown': 3, 'qsize': 60, 'asize': 54, 'cta': cta}
H = lambda t, hl, icon, n, md=2.8: {'type': 'hook', 'text': t, 'hl': hl, 'icon': icon, 'narration': n, 'min_duration': md}
S = lambda t, hl, rows, n, md=3.4: {'type': 'steps', 'text': t, 'hl': hl, 'rows': rows, 'narration': n, 'min_duration': md}
R = lambda t, cue, icon=None, **k: {'t': t, 'cue': cue, **({'icon': icon} if icon else {}), **k}

B('b-133-mbps', '2026-10-26T21:00:00Z', 'mbps', "Your 100 Mbps internet tops out at 12.5 MB/s #Shorts", ['internet', 'bits', 'bytes', 'networking'],
  "Network speeds are sold in megabits per second; downloads show megabytes. 8 bits = 1 byte.", [
      H('Your 100 Mbps internet is not 100 MB/s', 'not 100 MB/s', '🐌', "Your hundred megabit internet will never download at a hundred megabytes."),
      Q('GUESS', 'You pay for 100 Mbps. Max download speed?', ['100 MB/s', '12.5 MB/s', '1 GB/s'], 1, 'You pay for a hundred megabits. What is the max download speed?'),
      S('Bits vs bytes', 'bytes', [R('1 byte = 8 bits', 'one', '🔢'), R('100 Mbps ÷ 8 = 12.5 MB/s', 'divide'), R('1 GB takes {c_gb_s} s', 'so')],
        "One byte is eight bits. Divide a hundred by eight: twelve point five megabytes per second. So one gigabyte takes {c_gb_s_say} seconds."),
      T('Small b = bits. Big B = bytes.', 'Big B', '🔤', "Small b means bits. Big B means bytes. Ads use the small one.", 'shrug'),
      end('Check your next download', 'download', "Check it on your next download.")],
  )
B('b-136-thunder', '2026-10-27T01:00:00Z', 'thunder', "Count after lightning, divide by 3: that's the km #Shorts", ['physics', 'sound', 'lightning', 'weather'],
  "Sound travels about 343 m/s in air at 20 °C, so it covers 1 km in about 2.9 s. Light arrives almost instantly.", [
      H('Count the seconds after lightning', 'seconds', '⚡', "Next storm, count the seconds after the lightning."),
      S('Why it works', 'works', [R('Light: arrives instantly', 'light', '💡'), R('Sound: 343 m per second', 'sound', '🔊'), R('1 km = {c_s_km} seconds', 'one')],
        "The light reaches you almost instantly. The sound crawls at three hundred forty three meters per second. One kilometer takes about three seconds."),
      BIG('Seconds divided by 3 =', 'divided by 3', 'km away', 'divide by 5 for miles', "So divide the seconds by three, and you get kilometers. By five for miles.", 3.0),
      T('Under 10 seconds? Get inside.', 'Get inside.', '🏠', "Under ten seconds, it's close enough to hit you. Get inside.", 'shock'),
      end('Try it next storm', 'next storm', "Try it on the next storm.")])
B('b-137-horizon', '2026-10-27T21:00:00Z', 'horizon', "The horizon is only {c_h} km away #Shorts", ['earth', 'math', 'geometry', 'physics'],
  "Distance to the horizon for eyes 1.7 m above sea level: sqrt(2Rh + h²) with R = 6,371 km. Ignores refraction.", [
      H('How far away is the horizon?', 'horizon?', '🌅', "Standing on a beach, how far away is the horizon?"),
      Q('GUESS', 'On a beach, eyes 1.7 m up. The horizon is about:', ['5 km', '50 km', '500 km'], 0, 'Eyes one point seven meters up. How far is the horizon?'),
      S('The math', 'math', [R('d = √(2 × R × h)', 'the'), R('R = 6,371 km · h = 1.7 m', 'earth', '🌍'), R('d ≈ {c_h} km', 'about')],
        "The distance is the square root of two times Earth's radius times your height. With Earth's radius and one point seven meters, that's about {c_h_say} kilometers."),
      T('From a plane: {c_plane} km', '{c_plane} km', '✈️', "From a plane at cruising height, it's {c_plane_say} kilometers.", 'shock'),
      end('Did you guess right?', 'right?', "Did you guess right?")])
B('b-135-spin', '2026-10-28T01:00:00Z', 'spin', "You're spinning at {c_eq} km/h right now #Shorts", ['earth', 'physics', 'space', 'rotation'],
  "Earth's equatorial circumference (40,075 km) divided by one sidereal day (23 h 56 min). Speed scales with the cosine of latitude.", [
      H("You're moving at {c_eq} km/h right now", '{c_eq} km/h', '🌍', "Right now, you're moving at about {c_eq_say} kilometers per hour."),
      S('Where that comes from', 'comes from', [R('Around the equator: 40,075 km', 'around', '🌐'), R('One spin: 23 h 56 min', 'one', '🕐'), R('40,075 ÷ 23.93 h = {c_eq} km/h', 'that')],
        "Around the equator, Earth is forty thousand kilometers. One spin takes twenty three hours fifty six minutes. That's {c_eq_say} kilometers per hour."),
      T('New York: {c_ny} km/h', '{c_ny} km/h', '🗽', "Further north it's slower. In New York, about {c_ny_say}.", 'shrug'),
      T("You don't feel it: no speed change", "don't feel it", '🛋️', "You don't feel it, because the speed never changes.", None, 3.0),
      end('Mind blown?', 'blown?', "Mind blown?")])
B('b-139-battery', '2026-10-28T21:00:00Z', 'battery', "Your phone battery could lift you {c_m} meters #Shorts", ['battery', 'energy', 'physics', 'phone'],
  "Typical 5,000 mAh phone battery at 3.85 V nominal = 19.25 Wh = 69,300 J. Lifting 70 kg: h = E / (m·g). Ideal, no losses.", [
      H('Your phone battery could lift you {c_m} m', '{c_m} m', '🔋', "Your phone battery holds enough energy to lift you {c_m_say} meters."),
      S('The energy', 'energy', [R('5,000 mAh × 3.85 V = {c_wh} Wh', 'five', '🔋'), R('{c_wh} Wh = {c_j} joules', 'that'), R('Lift 70 kg: E ÷ (m × g) = {c_m} m', 'lift')],
        "Five thousand milliamp hours at three point eight five volts is nineteen watt hours. That's {c_j_say} joules. Lifting seventy kilos, that's {c_m_say} meters."),
      T("That's a {c_floors}-floor building", '{c_floors}-floor', '🏢', "That's a {c_floors} floor building. In theory, with zero losses.", 'shock'),
      end('Charge it tonight', 'tonight', "Charge it tonight with that in mind.")])
B('b-134-wifi', '2026-10-29T01:00:00Z', 'wifi', "Your Wi-Fi uses the same frequency as your microwave #Shorts", ['wifi', 'microwave', 'physics', 'radio'],
  "Microwave ovens run at about 2.45 GHz, inside the 2.4 GHz band Wi-Fi also uses. Wavelength = c / f.", [
      H('Your Wi-Fi uses the same frequency as your microwave', 'same frequency', '📶', "Your Wi-Fi uses the same frequency as your microwave."),
      BIG('Both run near', 'Both', '2.4 GHz', 'Wi-Fi band and microwave ovens', "Both run near two point four gigahertz.", 2.8),
      S('Wave length', 'length', [R('λ = speed of light ÷ frequency', 'the'), R('300,000 km/s ÷ 2.45 GHz', 'three'), R('= {c_cm} cm per wave', 'about')],
        "The wavelength is the speed of light divided by the frequency. That's about {c_cm_say} centimeters per wave."),
      T('Door holes: a few mm. Waves: {c_cm} cm.', '{c_cm} cm.', '🍿', "The holes in the door are tiny next to that, so the waves can't get out.", 'shrug', 3.4),
      T('Wi-Fi: thousands of times weaker', 'weaker', '📡', "And your router is thousands of times weaker. It just carries data.", None, 3.0),
      end('Ever noticed Wi-Fi drop?', 'drop?', "Ever noticed your Wi-Fi drop when the microwave runs?")])
B('b-141-pixels', '2026-10-29T21:00:00Z', 'pixels', "4K isn't 2x 1080p. It's {c_x4}x #Shorts", ['4k', 'tv', 'pixels', 'video'],
  "1080p = 1920×1080 = 2,073,600 pixels; 4K UHD = 3840×2160 = 8,294,400; 8K = 7680×4320 = 33,177,600.", [
      H("4K isn't twice 1080p", 'twice', '📺', "4K is not twice the pixels of 1080p."),
      Q('GUESS', '4K has how many times the pixels of 1080p?', ['2x', '4x', '8x'], 1, 'How many times the pixels of 1080p does 4K have?'),
      S('Count them', 'Count', [R('1080p: 1920 × 1080 = {c_fhd} M', 'ten'), R('4K: 3840 × 2160 = {c_4k} M', 'four'), R('{c_4k} ÷ {c_fhd} = {c_x4}x', 'exactly')],
        "Ten eighty p is two million pixels. 4K is eight point three million. Exactly four times."),
      BIG('And 8K vs 1080p?', '8K', '{c_x8}x', 'the pixels', "And 8K? Sixteen times."),
      end('Can you see the difference?', 'difference?', "Can you actually see the difference?")])
B('b-143-sms', '2026-10-30T01:00:00Z', 'sms', "Why texts stopped at {c_chars} characters #Shorts", ['sms', 'texting', 'computers', 'phones'],
  "An SMS payload is 140 bytes (1,120 bits). GSM 7-bit text fits 160 characters; UCS-2 (needed for emoji) fits 70.", [
      H('Why texts stopped at 160 characters', '160', '💬', "Old text messages stopped at exactly one hundred sixty characters. Here's why."),
      S('The math', 'math', [R('One SMS: 140 bytes', 'one', '📦'), R('140 × 8 = {c_bits} bits', 'that'), R('÷ 7 bits per letter = {c_chars}', 'with')],
        "One message carried a hundred forty bytes. That's one thousand one hundred twenty bits. With seven bits per letter: one sixty."),
      T('Add one emoji: {c_ucs} characters', '{c_ucs}', '😅', "Add a single emoji, and the limit drops to seventy.", 'shock'),
      T('Emoji need 16 bits per character', '16 bits', '🔣', "Because emoji switch the whole message to sixteen bits per character.", None, 3.0),
      end('Did you know that?', 'know that?', "Did you know that?")])
B('b-138-iss', '2026-10-30T21:00:00Z', 'iss', "Astronauts see {c_n16} sunrises a day #Shorts", ['space', 'iss', 'orbit', 'physics'],
  "ISS at ~420 km altitude: orbital period from Kepler's third law (GM of Earth), ~93 minutes; ~15.5 orbits per day.", [
      H('Astronauts see 16 sunrises a day', '16 sunrises', '🛰️', "Astronauts on the space station see about sixteen sunrises every day."),
      S('Why', 'Why', [R('Altitude: 420 km', 'it', '🌍'), R('Speed: {c_kmh} km/h', 'at'), R('One lap: {c_min} minutes', 'one')],
        "It flies four hundred twenty kilometers up, at {c_kmh_say} kilometers per hour. One lap takes {c_min_say} minutes."),
      BIG('Laps per day', 'per day', '{c_n}', 'sunrises and sunsets', "That's {c_n_say} laps a day. A sunrise every lap."),
      T('They sleep with window covers', 'window covers', '😴', "So they keep a strict clock, and cover the windows to sleep.", 'shrug'),
      end('Would you sleep up there?', 'up there?', "Would you sleep up there?")])
B('b-142-base64', '2026-10-31T01:00:00Z', 'base64', "Email makes your attachments {c_pct}% bigger #Shorts", ['email', 'base64', 'computers', 'encoding'],
  "Email attachments are encoded as Base64 text: every 3 bytes become 4 characters (+33%, a bit more with line breaks).", [
      H('Email makes your attachments 33% bigger', '33% bigger', '📎', "Email makes your attachments about thirty three percent bigger."),
      S('Why', 'Why', [R('Email was built for text only', 'email', '✉️'), R('Base64: 3 bytes → 4 letters', 'so'), R('4 ÷ 3 = +{c_pct}%', 'four')],
        "Email was built for text only. So files are turned into letters: every three bytes become four characters. That's a third bigger."),
      T('A 10 MB file sends as {c_10} MB', '{c_10} MB', '📦', "So a ten megabyte file travels as thirteen point three.", 'shock'),
      T("That's why limits hit early", 'early', '🚫', "That's why attachment limits hit earlier than you expect.", 'shrug', 3.0),
      end('Use a link instead', 'link', "For big files, send a link instead.")])
B('b-146-cdaudio', '2026-10-31T21:00:00Z', 'cdaudio', "A 3-minute song is {c_mb} MB. Your MP3 is {c_mp3} MB #Shorts", ['audio', 'mp3', 'music', 'compression'],
  "CD audio: 44,100 samples/s × 16 bits × 2 channels = 1.41 Mbit/s; 180 s = 31.75 MB. MP3 at 128 kbps: 2.88 MB.", [
      H('A 3-minute song is 32 MB. Your MP3 is 3 MB.', '3 MB.', '🎵', "A three minute song is thirty two megabytes. Your MP3 is three."),
      S('CD quality', 'CD', [R('44,100 samples per second', 'forty', '🎚️'), R('× 16 bits × 2 channels', 'times'), R('× 180 s = {c_mb} MB', 'for')],
        "Forty four thousand one hundred samples a second, times sixteen bits, times two channels. For three minutes: {c_mb_say} megabytes."),
      BIG('An MP3 is', 'MP3', '{c_x}x', 'smaller at 128 kbps', "A typical MP3 is {c_x_say} times smaller."),
      T("It deletes sounds you can't hear", "can't hear", '👂', "The trick: it deletes sounds your ear can't hear anyway.", 'shrug'),
      end('Can you hear the difference?', 'difference?', "Can you hear the difference?")])
B('b-140-qr', '2026-11-01T01:00:00Z', 'qr', "Up to {c_pct}% of a QR code can be damaged #Shorts", ['qrcode', 'math', 'errorcorrection', 'tech'],
  "QR codes use Reed–Solomon error correction; level H recovers up to ~30% of codewords. Version 40 holds up to 7,089 digits.", [
      H('A QR code still works with 30% torn off', '30% torn off', '✂️', "You can damage up to thirty percent of a QR code, and it still scans."),
      S('How', 'How', [R('Extra error-correction data', 'it', '🧩'), R('Level H: recovers ~30%', 'at'), R("That's how logos fit inside", 'that')],
        "It stores extra error correction data. At the highest level, it can rebuild about thirty percent. That's how logos fit in the middle."),
      BIG('The biggest QR code holds', 'biggest', '{c_digits}', 'digits', "The biggest one holds seven thousand eighty nine digits."),
      T('Same math as CDs and space probes', 'space probes', '🚀', "The same math protects CDs and space probe signals.", 'shrug'),
      end('Ever scanned a damaged one?', 'damaged', "Ever scanned a damaged one?")])
B('b-144-orbit', '2026-11-01T21:00:00Z', 'orbit', "Right now you're flying at {c_v} km/h #Shorts", ['space', 'earth', 'orbit', 'physics'],
  "Earth's orbit: 2π × 1 AU ≈ 940 million km per sidereal year (365.256 days) ≈ 107,000 km/h ≈ 29.8 km/s.", [
      H("Right now you're flying through space at 107,000 km/h", '107,000 km/h', '🚀', "Right now, you're flying through space at a hundred seven thousand kilometers per hour."),
      S('The math', 'math', [R("Earth's orbit: {c_L} million km", 'earth', '☀️'), R('One year: {c_hrs} hours', 'one'), R('{c_L} M ÷ {c_hrs} = {c_v} km/h', 'that')],
        "Earth's orbit is nine hundred forty million kilometers long. One year is eight thousand seven hundred sixty six hours. That's {c_v_say} kilometers per hour."),
      BIG('Per second', 'second', '{c_kms} km', 'New York to LA in {c_nyla} minutes', "Thirty kilometers every second. New York to LA in about two minutes."),
      end('And you feel nothing', 'nothing', "And you feel nothing.")])
B('b-145-lightyear', '2026-11-02T01:00:00Z', 'lightyear', "Driving one light-year takes {c_myr} million years #Shorts", ['space', 'lightyear', 'physics', 'astronomy'],
  "One light-year ≈ 9.46 trillion km. At a constant 100 km/h: 94.6 billion hours ≈ 10.8 million years. Proxima Centauri: 4.24 ly.", [
      H('Driving one light-year: 10.8 million years', '10.8 million years', '🚗', "If you could drive one light-year, it would take ten point eight million years."),
      S('The math', 'math', [R('1 light-year = {c_ly} trillion km', 'one', '💡'), R('Highway speed: 100 km/h', 'at'), R('= {c_myr} million years', 'that')],
        "One light-year is nine point four six trillion kilometers. At a hundred kilometers per hour, that's {c_myr_say} million years."),
      T('Nearest star: 4.24 light-years', '4.24', '⭐', "And the nearest star is four point two four light-years away.", 'shrug'),
      BIG('Drive there:', 'Drive', '{c_prox} M years', 'non-stop, at 100 km/h', "That's {c_prox_say} million years, without stopping."),
      end('Still want a road trip?', 'road trip?', "Still want that road trip?")])

print('\n'.join(V))

"""Gera os specs do formato v3 (mascote 3D). Uso: python3 specs/v3gen.py -> specs/v3/*.json"""
import json, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v3')
os.makedirs(OUT, exist_ok=True)


def save(name, spec):
    json.dump(spec, open(f'{OUT}/{name}.json', 'w'), ensure_ascii=False, indent=1)
    return name


def end(text, hl, narration, sub=None):
    d = {'type': 'end', 'text': text, 'hl': hl, 'narration': narration, 'min_duration': 2.2}
    if sub:
        d['sub'] = sub
    return d


# ---------------- Chartbound: comparações do Banco Mundial ----------------
def wb(name, at, a, fa, b, fb, ind, metric, insight, title, tags):
    gdp = ind == 'NY.GDP.MKTP.CD'
    what = "economy" if gdp else "population"
    poss = f"{a}'s economy" if gdp else f"{a}'s population"
    hook_n = (f"In {{wr_from}}, {insight.get('short_a', a)} was {{wr_r0_say}} percent of {b}." if gdp
              else f"In {{wr_from}}, {a.replace('The ', 'the ')} had {{wr_r0_say}} percent of {b}'s people.")
    spec = {
        'channel': 'chartbound', 'style': 'v3', 'rate': '+9%', 'title': title,
        'publish': {'channel': 'A', 'privacy': 'public', 'at': at},
        'compute': {'wbratio': {'ind': ind, 'a': insight['a3'], 'b': insight['b3'], 'from': 2000}},
        'yt': {'title': title, 'description': f"{a} as a share of {b}, {what}, {{wr_from}} vs {{wr_to}}. Source: World Bank ({ind}). Narration is AI-generated.\n#economics #data #{a.lower().replace(' ', '')}", 'tags': tags, 'lang': 'en'},
        'scenes': [
            {'type': 'hook', 'kicker': 'In {wr_from}', 'text': (f"{a}'s economy was {{wr_r0}}% of {b}'s" if gdp else f"{a} had {{wr_r0}}% of {b}'s people"), 'hl': '{wr_r0}%',
             'vs': [{'flag': fa, 'name': a if len(a) < 12 else insight.get('short_a', a)}, {'flag': fb, 'name': b}], 'narration': hook_n, 'min_duration': 3.2},
            {'type': 'bars', **({'style': 'coins'} if gdp else {}), 'kicker': f"{insight.get('short_a', a)} as % of {b}", 'text': 'Now watch', 'hl': 'watch', 'en': True, 'suffix': '%',
             'vals_from': 'wr_v', 'labels_from': 'wr_y', 'narration': insight['bars_n'], 'min_duration': 4.4},
            insight['big'],
            insight['text'],
            end(insight['end_text'], insight['end_hl'], insight['end_n']),
        ],
    }
    return save(name, spec)


V = []
V.append(wb('a-118-spain-italy', '2026-10-24T20:00:00Z', 'Spain', '🇪🇸', 'Italy', '🇮🇹', 'NY.GDP.MKTP.CD', 'economy', {
    'a3': 'ESP', 'b3': 'ITA',
    'bars_n': "Then Spain closed in. Today it's {wr_r1_say} percent.",
    'big': {'type': 'big', 'text': 'Spain gained', 'hl': 'gained', 'big': '+{wr_d} pts', 'label': 'on Italy since {wr_from}', 'narration': "Spain gained {wr_d_say} points on Italy.", 'min_duration': 3},
    'text': {'type': 'text', 'text': 'Same euro. Faster growth.', 'hl': 'Faster growth.', 'icon': '📈', 'pose': 'shrug', 'narration': "Same euro, so no currency trick. Spain just grew faster.", 'min_duration': 3.4},
    'end_text': 'Which two countries next?', 'end_hl': 'next?', 'end_n': 'Which two countries should I compare next?'},
    "Spain's economy was {wr_r0}% of Italy's in {wr_from}. Now? #Shorts", ['economics', 'spain', 'italy', 'gdp', 'data']))

V.append(wb('a-123-philippines-japan', '2026-10-24T23:00:00Z', 'The Philippines', '🇵🇭', 'Japan', '🇯🇵', 'SP.POP.TOTL', 'population', {
    'a3': 'PHL', 'b3': 'JPN', 'short_a': 'Philippines',
    'bars_n': "Then the gap kept shrinking. Today it's {wr_r1_say} percent. Almost the same size.",
    'big': {'type': 'big', 'text': 'The gap closed by', 'hl': 'closed', 'big': '+{wr_d} pts', 'label': 'in one generation', 'narration': "The gap closed by {wr_d_say} points.", 'min_duration': 3},
    'text': {'type': 'text', 'text': 'Japan is shrinking. The Philippines keeps growing.', 'hl': 'shrinking.', 'icon': '👶', 'pose': 'shrug', 'narration': "Japan is shrinking. The Philippines keeps growing.", 'min_duration': 3.4},
    'end_text': 'Will it pass Japan?', 'end_hl': 'pass Japan?', 'end_n': 'So, will it pass Japan? Comment your guess.'},
    "The Philippines had {wr_r0}% of Japan's population in {wr_from}. Now? #Shorts", ['population', 'philippines', 'japan', 'demographics', 'data']))

V.append(wb('a-124-poland-sweden', '2026-10-25T16:00:00Z', 'Poland', '🇵🇱', 'Sweden', '🇸🇪', 'NY.GDP.MKTP.CD', 'economy', {
    'a3': 'POL', 'b3': 'SWE',
    'bars_n': "Then Poland climbed, all the way to {wr_r1_say} percent.",
    'big': {'type': 'big', 'text': 'Poland first passed Sweden in', 'hl': 'passed', 'big': '{wr_cross}', 'label': 'for the first time', 'narration': "It first passed Sweden in {wr_cross}.", 'min_duration': 2.8},
    'text': {'type': 'text', 'text': 'But per person, Sweden is still richer', 'hl': 'per person,', 'icon': '🧮', 'pose': 'shrug', 'narration': "But per person, Sweden is still richer.", 'min_duration': 3.6},
    'end_text': 'Which two countries next?', 'end_hl': 'next?', 'end_n': 'Which two countries should I compare next?'},
    "Poland's economy was {wr_r0}% of Sweden's in {wr_from}. Now? #Shorts", ['economics', 'poland', 'sweden', 'gdp', 'data']))

V.append(wb('a-125-canada-russia', '2026-10-25T20:00:00Z', 'Canada', '🇨🇦', 'Russia', '🇷🇺', 'NY.GDP.MKTP.CD', 'economy', {
    'a3': 'CAN', 'b3': 'RUS',
    'bars_n': "Then it swung hard. Today it's just {wr_r1_say} percent. Russia is bigger.",
    'big': {'type': 'big', 'text': 'Canada lost', 'hl': 'lost', 'big': '-{wr_d} pts', 'label': 'against Russia since {wr_from}', 'narration': "Canada lost {wr_d_say} points.", 'min_duration': 3},
    'text': {'type': 'text', 'text': 'Oil and exchange rates swing it', 'hl': 'Oil', 'icon': '🛢️', 'pose': 'shrug', 'narration': "Oil prices and exchange rates swing this a lot.", 'min_duration': 3.4},
    'end_text': 'Did you expect that?', 'end_hl': 'expect', 'end_n': 'Did you expect that?'},
    "Canada's economy was {wr_r0}% of Russia's in {wr_from}. Now? #Shorts", ['economics', 'canada', 'russia', 'gdp', 'data']))

V.append(wb('a-126-argentina-brazil', '2026-10-25T23:00:00Z', 'Argentina', '🇦🇷', 'Brazil', '🇧🇷', 'NY.GDP.MKTP.CD', 'economy', {
    'a3': 'ARG', 'b3': 'BRA',
    'bars_n': "Then it slipped. Today, only {wr_r1_say} percent.",
    'big': {'type': 'big', 'text': 'Argentina fell', 'hl': 'fell', 'big': '-{wr_d} pts', 'label': 'behind Brazil since {wr_from}', 'narration': "Argentina fell {wr_d_say} points behind.", 'min_duration': 3},
    'text': {'type': 'text', 'text': 'Currency crashes shrink dollar GDP', 'hl': 'Currency crashes', 'icon': '📉', 'pose': 'shrug', 'narration': "Currency crashes shrank it in dollars.", 'min_duration': 3.4},
    'end_text': 'Which two countries next?', 'end_hl': 'next?', 'end_n': 'Which two countries should I compare next?'},
    "Argentina's economy was {wr_r0}% of Brazil's in {wr_from}. Now? #Shorts", ['economics', 'argentina', 'brazil', 'gdp', 'data']))


# ---------------- How It Ticks ----------------
def ht(name, at, kind, title, tags, scenes, desc):
    spec = {'channel': 'howitticks', 'style': 'v3', 'rate': '+6%', 'title': title,
            'publish': {'channel': 'B', 'privacy': 'public', 'at': at}, 'compute': {'calc': {'kind': kind}},
            'yt': {'title': title, 'description': desc + "\nNarration is AI-generated.", 'tags': tags, 'lang': 'en'}, 'scenes': scenes}
    return save(name, spec)


V.append(ht('b-128-sunlight', '2026-10-24T21:00:00Z', 'sunlight', "You see the Sun as it was {c_stat} ago #Shorts", ['space', 'physics', 'sun', 'light'], [
    {'type': 'hook', 'text': "You're seeing the Sun 8 minutes late", 'hl': '8 minutes late', 'icon': '☀️', 'narration': "When you look at the Sun, you're seeing the past.", 'min_duration': 3},
    {'type': 'big', 'text': 'Sunlight needs', 'hl': 'needs', 'big': '{c_stat}', 'label': 'to reach your eyes', 'narration': "Its light needs {c_say} to reach you.", 'min_duration': 3.2},
    {'type': 'steps', 'text': 'The math', 'hl': 'math', 'rows': [{'t': 'Distance: 150 million km', 'icon': '☀️', 'cue': 'the'}, {'t': 'Light: 300,000 km per second', 'icon': '💡', 'cue': 'light'}, {'t': '150,000,000 ÷ 300,000 ≈ 500 s', 'cue': 'about'}], 'narration': "The Sun is a hundred fifty million kilometers away. Light does three hundred thousand per second. That's about five hundred seconds.", 'min_duration': 3.4},
    {'type': 'text', 'text': 'Even the Moon: {c_moon} s old', 'hl': '{c_moon} s', 'icon': '🌕', 'pose': 'shock', 'narration': "Even the Moon you see is {c_moon_say} seconds old.", 'min_duration': 3},
    end('So how old is starlight?', 'starlight?', "So how old is the light from the stars?"),
], "Light from the Sun takes about 8 minutes 19 seconds to reach Earth (mean distance 1 AU). Computed from the speed of light."))

V.append(ht('b-129-gpsrel', '2026-10-25T01:00:00Z', 'gpsrel', "Without Einstein, GPS would drift {c_km} km a day #Shorts", ['gps', 'relativity', 'physics', 'einstein'], [
    {'type': 'hook', 'text': 'Without Einstein, GPS drifts {c_km} km a day', 'hl': '{c_km} km', 'icon': '🛰️', 'narration': "Without Einstein, your GPS would be useless in a day.", 'min_duration': 3.2},
    {'type': 'steps', 'text': 'Satellite clocks, per day', 'hl': 'per day', 'rows': [{'t': 'Weaker gravity: +{c_gr} µs', 'icon': '🪐', 'cue': 'weaker'}, {'t': 'High speed: −{c_sr} µs', 'icon': '🚀', 'cue': 'their'}, {'t': 'Net: +{c_us} µs every day', 'cue': 'net'}], 'narration': "Up there, weaker gravity speeds the clocks up. Their speed slows them down. Net: {c_us_say} microseconds fast, every day.", 'min_duration': 3.4},
    {'type': 'big', 'text': 'Light covers that in', 'hl': 'Light', 'big': '{c_km} km', 'label': 'of error, every single day', 'narration': "Tiny, but light covers {c_km_say} kilometers in that time.", 'min_duration': 2.8},
    {'type': 'text', 'text': 'So engineers pre-tune the clocks', 'hl': 'pre-tune', 'icon': '🔧', 'narration': "So the satellite clocks are tuned slow before launch.", 'min_duration': 2.6},
    end('Einstein is in your pocket', 'pocket', "Einstein is literally in your pocket."),
], "GPS satellite clocks gain about 38 microseconds per day from general and special relativity combined. Computed with Einstein's formulas."))

V.append(ht('b-130-luhn', '2026-10-25T17:00:00Z', 'luhn', "Your card's last digit catches {c_single} of typos #Shorts", ['math', 'cards', 'algorithm', 'luhn'], [
    {'type': 'hook', 'text': "Your card's last digit is a typo trap", 'hl': 'typo trap', 'icon': '💳', 'narration': "Your card's last digit is a trap for typos.", 'min_duration': 3},
    {'type': 'steps', 'text': 'The Luhn check', 'hl': 'Luhn', 'rows': [{'t': '4539 1488 0343 6467', 'icon': '💳', 'cue': 'take'}, {'t': 'Double every 2nd digit, from the right', 'cue': 'from'}, {'t': 'Add all the digits: 80', 'cue': 'add'}, {'t': 'Ends in 0, so valid', 'cue': 'it'}], 'narration': "Take a test number. From the right, double every second digit. Add all the digits up: eighty. It ends in zero, so it passes.", 'min_duration': 3.6},
    {'type': 'big', 'text': 'One-digit typos caught', 'hl': 'caught', 'big': '{c_single}', 'label': 'we tested every one', 'narration': "We tried every single-digit typo. It caught {c_single_say} percent.", 'min_duration': 3.2},
    {'type': 'text', 'text': 'Swapped neighbors: {c_trans} caught', 'hl': '{c_trans}', 'icon': '🔁', 'narration': "And about {c_trans_say} percent of swapped neighbors.", 'min_duration': 2.8},
    end('A typo check, not security', 'not security', "It catches typos. It does not make your card safe."),
], "The Luhn check digit. We tested every one-digit typo and every adjacent swap on 2,000 random numbers. Test card numbers only."))

V.append(ht('b-131-ping', '2026-10-25T21:00:00Z', 'ping', "Your ping can never be zero. Here's the limit #Shorts", ['internet', 'gaming', 'ping', 'physics'], [
    {'type': 'hook', 'text': 'Your ping can never be zero', 'hl': 'never', 'icon': '🎮', 'narration': "Your ping can never be zero. Here's why.", 'min_duration': 2.8},
    {'type': 'text', 'text': 'In fiber, light is 1/3 slower', 'hl': '1/3 slower', 'icon': '💡', 'pose': 'shrug', 'narration': "In fiber, light is a third slower than in space.", 'min_duration': 3.4},
    {'type': 'steps', 'text': 'Server 1,000 km away', 'hl': '1,000 km', 'rows': [{'t': 'There and back: 2,000 km', 'icon': '↔️', 'cue': 'there'}, {'t': '÷ {c_fkms} km/s in glass', 'icon': '💡', 'cue': 'divide'}, {'t': '= {c_ms} ms minimum', 'cue': 'at'}], 'narration': "There and back is two thousand kilometers. Divide by the speed in glass, and you get at least {c_ms_say} milliseconds.", 'min_duration': 3.4},
    {'type': 'text', 'text': 'Real cables zigzag', 'hl': 'zigzag', 'icon': '🌍', 'narration': "Real cables zigzag, so real pings are higher.", 'min_duration': 2.6},
    end('How far is your server?', 'server?', "How far away is your game server?"),
], "Minimum round-trip time over 1,000 km of optical fiber, from the refractive index of glass (~1.47)."))

V.append(ht('b-132-cube', '2026-10-26T01:00:00Z', 'cube', "This small cube has {c_q} quintillion positions #Shorts", ['math', 'puzzle', 'combinatorics', 'cube'], [
    {'type': 'hook', 'text': 'This toy has {c_q} quintillion positions', 'hl': '{c_q} quintillion', 'icon': '🧩', 'narration': "This little cube has more positions than you'd believe.", 'min_duration': 3.2},
    {'type': 'big', 'text': 'Exactly', 'hl': 'Exactly', 'big': '{c_q} quintillion', 'label': '{c_n} positions', 'narration': "{c_q_say} quintillion positions.", 'min_duration': 3},
    {'type': 'steps', 'text': 'Where it comes from', 'hl': 'comes from', 'rows': [{'t': '8 corners: 8! × 3⁷', 'icon': '🔺', 'cue': 'eight'}, {'t': '12 edges: 12! × 2¹¹', 'icon': '🔷', 'cue': 'twelve'}, {'t': '÷ 2 (parity rule)', 'icon': '⚖️', 'cue': 'divide'}, {'t': '= {c_q} quintillion', 'cue': 'and'}], 'narration': "Eight corners, each placed and twisted. Twelve edges, each placed and flipped. Divide by two for parity, and there it is.", 'min_duration': 3.6},
    {'type': 'text', 'text': 'Any of them: 20 moves or less', 'hl': '20 moves', 'icon': '🏆', 'pose': 'cheer', 'narration': "Yet every single one can be solved in twenty moves or fewer. Proven in twenty ten.", 'min_duration': 3.4},
    end('Can you solve one?', 'solve', "Can you solve one?"),
], "Positions of a 3x3x3 puzzle cube: 8!·3^7·12!·2^11/2, computed. God's number (20) was proven in 2010."))

V.append(ht('b-127-unix2e9', '2026-10-26T17:00:00Z', 'unix2e9', "Your computer hits 2,000,000,000 on {c_date} #Shorts", ['computers', 'unix', 'time', 'programming'], [
    {'type': 'hook', 'text': 'Your computer is counting to 2 billion', 'hl': '2 billion', 'icon': '⏰', 'narration': "Your computer is quietly counting toward two billion.", 'min_duration': 2.8},
    {'type': 'screen', 'text': 'Seconds since Jan 1, 1970', 'hl': 'since', 'code': ['$ date +%s', '1792848886'], 'narration': "Many computers store time as the seconds since January first, nineteen seventy.", 'min_duration': 3.4},
    {'type': 'big', 'text': 'It hits 2,000,000,000 on', 'hl': '2,000,000,000', 'big': '{c_date}', 'label': 'at {c_time}', 'narration': "That count hits two billion on {c_date_say}.", 'min_duration': 3.4},
    {'type': 'text', 'text': '1 billion was {c_1e9}', 'hl': '1 billion', 'icon': '🗓️', 'pose': 'shrug', 'narration': "One billion was {c_1e9_say}.", 'min_duration': 2.8},
    {'type': 'steps', 'text': 'The real deadline: 2038', 'hl': '2038', 'rows': [{'t': '2,000,000,000 fits fine', 'icon': '✅', 'cue': 'two'}, {'t': 'Old 32-bit max: 2,147,483,647', 'icon': '🧱', 'cue': 'old'}, {'t': 'Jan 19, 2038: overflow', 'icon': '💥', 'cue': 'that'}], 'narration': "Two billion fits fine. But old 32-bit clocks max out at about two point one billion. That's January nineteenth, twenty thirty-eight.", 'min_duration': 3.6},
    end('Where will you be in 2033?', '2033?', "Where will you be when it hits two billion?"),
], "Unix time reaches 2,000,000,000 seconds on May 18, 2033 03:33:20 UTC. Computed."))

print('\n'.join(V))

"""Preenche cenas 'chart' com dados reais (FRED) e resolve {placeholders} na narração/legendas.
Uso: python scripts/data.py spec.json spec_out.json
Cena: {"type":"chart","source":{"fred":"MSPUS","from":1990,"to":2024,"step":5}} """
import csv, hashlib, io, json, sys, urllib.request
from collections import defaultdict

def fred_annual(series, y0, y1):
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}&cosd={y0}-01-01&coed={y1}-12-31"
    raw = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read().decode()
    by = defaultdict(list)
    for row in list(csv.reader(io.StringIO(raw)))[1:]:
        if len(row) < 2 or row[1] in ("", "."):
            continue
        by[int(row[0][:4])].append(float(row[1]))
    return {y: sum(v) / len(v) for y, v in sorted(by.items())}

def worldbank_annual(ind, country, y0, y1):
    url = f"https://api.worldbank.org/v2/country/{country}/indicator/{ind}?format=json&per_page=200&date={y0}:{y1}"
    for attempt in range(3):
        try:
            data = json.load(urllib.request.urlopen(url, timeout=30))
            break
        except Exception as e:
            if attempt == 2:
                raise
    rows = data[1] or []
    return {int(r["date"]): float(r["value"]) for r in sorted(rows, key=lambda r: r["date"]) if r["value"] is not None}

def ipca_series(first):
    """IPCA variação mensal (BCB SGS 433). first='AAAA-MM'. Retorna [(AAAA-MM, %)]."""
    y, m = first.split("-")
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json&dataInicial=01/{m}/{y}"
    last = None
    for i in range(3):
        try:
            rows = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30))
            break
        except Exception:
            if i == 2:
                raise
    out = []
    for r in rows:
        d, mo, yy = r["data"].split("/")
        out.append((f"{yy}-{mo}", float(r["valor"])))
    return out

MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]

MESES_EN = ["January","February","March","April","May","June","July","August","September","October","November","December"]

def sgs_range(code, y0, m0, retries=4):
    """Serie diaria/mensal do BCB em blocos anuais (a API falha com respostas grandes)."""
    import datetime, time
    today = datetime.date.today()
    out = []
    for yy in range(y0, today.year + 1):
        d0 = datetime.date(yy, m0 if yy == y0 else 1, 1)
        d1 = min(datetime.date(yy, 12, 31), today)
        url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados?formato=json&dataInicial={d0.strftime('%d/%m/%Y')}&dataFinal={d1.strftime('%d/%m/%Y')}"
        for i in range(retries):
            try:
                rows = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60))
                if isinstance(rows, list):
                    out += rows
                    break
                print("sgs erro", code, yy, str(rows)[:120])
            except Exception as e:
                print("sgs falhou", code, yy, e)
            time.sleep(6 * (i + 1))
        else:
            raise RuntimeError(f"BCB SGS {code} {yy} indisponivel")
    return out

def brl(v):
    return "R$ " + f"{round(v):,}".replace(",", ".")

def compute_blocks(spec, ctx, raw):
    c = spec.get("compute") or {}
    if "hash" in c:
        h = c["hash"]
        a, b = h["a"], h["b"]
        ha, hb = hashlib.sha256(a.encode()).hexdigest(), hashlib.sha256(b.encode()).hexdigest()
        ba, bb = bin(int(ha, 16))[2:].zfill(256), bin(int(hb, 16))[2:].zfill(256)
        flips = [x != y for x, y in zip(ba, bb)]
        raw.update(bits=sum(flips), word_a=a, word_b=b)
        data = {"a": a, "b": b, "ha": ha, "hb": hb, "flips": flips}
        for sc in spec["scenes"]:
            if sc.get("art") in ("hash-compare", "hash-one", "bitgrid") or sc.get("type") in ("hashcmp", "hashbox", "grid"):
                sc["hashdata"] = data
    if "terms" in c:
        from num2words import num2words
        first = min(t["from"] for t in c["terms"])
        ser = c["terms"][0].get("series") or ipca_series(first)
        last_m = ser[-1][0]
        for n, t in enumerate(c["terms"], 1):
            to = t.get("to") or last_m
            vs = [v for m, v in ser if t["from"] <= m <= to]
            f = 1.0
            for v in vs:
                f *= 1 + v / 100
            avg = (f ** (12 / len(vs)) - 1) * 100
            dec = f"{avg:.1f}".replace(".", ",")
            raw.update({f"t{n}_name": t["name"], f"t{n}_avg": round(avg, 1), f"t{n}_avg_s": dec,
                        f"t{n}_say": num2words(round(avg, 1), lang="pt_BR"), f"t{n}_acc": round((f - 1) * 100),
                        f"t{n}_meses": len(vs)})
        ctx.update({k: v for k, v in raw.items() if k.startswith("t") and k[1].isdigit()})
    if "cpi" in c:
        from num2words import num2words
        i = c["cpi"]
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCSL&cosd={i['from']}-01-01"
        rows = None
        annual = False
        for _ in range(3):
            try:
                rows = list(csv.reader(io.StringIO(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read().decode())))[1:]
                rows = [(r[0], float(r[1])) for r in rows if len(r) > 1 and r[1] not in ("", ".")]
                break
            except Exception as e:
                print("fred falhou:", e)
        if not rows:
            wb = worldbank_annual("FP.CPI.TOTL", "USA", i["from"], i["from"] + 40)
            rows = [(f"{y}-12-01", v) for y, v in sorted(wb.items())]
            annual = True
            print("CPI via World Bank (anual)")
        f = rows[-1][1] / rows[0][1]
        amt = i.get("amount", 100)
        ly, lm = rows[-1][0].split("-")[:2]
        raw.update(cpi_amount_n=amt, cpi_needed_n=round(amt * f), cpi_pct=round((f - 1) * 100),
                   cpi_amount_say=num2words(amt, lang="en"), cpi_needed_say=num2words(round(amt * f), lang="en"),
                   cpi_pct_say=num2words(round((f - 1) * 100), lang="en"), cpi_from=(str(i['from']) if annual else f"January {i['from']}"),
                   cpi_to=(ly if annual else f"{MESES_EN[int(lm) - 1]} {ly}"), cpi_year=i["from"])
        ctx.update({k: v for k, v in raw.items() if k.startswith("cpi")})
    if "ipv4" in c:
        from num2words import num2words
        pop = worldbank_annual("SP.POP.TOTL", "WLD", 2018, 2026)
        py = max(pop)
        addr = 2 ** 32 / 1e9
        people = pop[py] / 1e9
        raw.update(ipv4_n=round(addr, 1), people_n=round(people, 1), people_year=py, ipv4_ratio=round(people / addr, 1),
                   ipv4_say=num2words(round(addr, 1), lang="en"), people_say=num2words(round(people, 1), lang="en"),
                   ipv4_ratio_say=num2words(round(people / addr, 1), lang="en"))
        ctx.update({k: v for k, v in raw.items() if k.startswith(("ipv4", "people"))})
    if "wbratio" in c:
        from num2words import num2words
        w = c["wbratio"]
        A = worldbank_annual(w["ind"], w["a"], w["from"], w.get("to", w["from"] + 30))
        B = worldbank_annual(w["ind"], w["b"], w["from"], w.get("to", w["from"] + 30))
        ys = sorted(set(A) & set(B))
        y0, y1 = ys[0], ys[-1]
        r0, r1 = A[y0] / B[y0] * 100, A[y1] / B[y1] * 100
        raw.update(wr_from=y0, wr_to=y1, wr_r0=round(r0), wr_r1=round(r1), wr_r0_say=num2words(round(r0), lang="en"),
                   wr_r1_say=num2words(round(r1), lang="en"), wr_a_t=round(A[y1] / 1e12, 1), wr_b_t=round(B[y1] / 1e12, 1),
                   wr_a_t_say=num2words(round(A[y1] / 1e12, 1), lang="en"), wr_b_t_say=num2words(round(B[y1] / 1e12, 1), lang="en"),
                   wr_d=abs(round(r1) - round(r0)), wr_d_say=num2words(abs(round(r1) - round(r0)), lang="en"),
                   wr_word=("jumped" if r1 > r0 else "dropped"), wr_sign=("+" if r1 >= r0 else "-"),
                   wr_x=round(max(r1, r0) / max(min(r1, r0), 1e-9), 1), wr_x_say=num2words(round(max(r1, r0) / max(min(r1, r0), 1e-9), 1), lang="en"))
        ctx.update({k: v for k, v in raw.items() if k.startswith("wr_")})
    if "floatsum" in c:
        from num2words import num2words
        fs = c["floatsum"]
        v = fs["a"] + fs["b"]
        raw.update(f_a=fs["a"], f_b=fs["b"], f_sum=repr(v), f_target=fs["target"], f_equal=str(v == fs["target"]).lower(),
                   f_digits=len(repr(v)) - 2)
        ctx.update({k: v2 for k, v2 in raw.items() if k.startswith("f_")})
    if "calc" in c:
        import math
        from num2words import num2words
        k = c["calc"]["kind"]
        if k == "birthday":
            def pb(n):
                q = 1.0
                for i in range(n):
                    q *= (365 - i) / 365
                return 1 - q
            p23, p70 = pb(23) * 100, pb(70) * 100
            raw.update(c_n=23, c_pairs=23 * 22 // 2, c_pairs_say=num2words(253, lang="en"), c_p=f"{p23:.1f}%",
                       c_p_say=num2words(round(p23, 1), lang="en"), c_n2=70, c_p2_say=num2words(round(p70, 1), lang="en"))
        elif k == "drive":
            g = 10 ** 12 / 2 ** 30
            raw.update(c_gib=f"{g:.1f}", c_gib_str=f"{g:.1f} GB", c_gib_say=num2words(round(g), lang="en"), c_lost=f"{1000 - g:.1f}")
        elif k == "fingers":
            raw.update(c_max=f"{2 ** 10 - 1:,}", c_max_say=num2words(2 ** 10 - 1, lang="en"), c_combos=2 ** 10, c_combos_say=num2words(2 ** 10, lang="en"))
        elif k == "password":
            rate = 1e10
            a, b2 = 26 ** 8, 94 ** 12
            ta = a / rate
            yb = b2 / rate / 31557600
            raw.update(c_a_secs=round(ta), c_a_say=num2words(round(ta), lang="en"), c_a_str=f"{round(ta)} seconds",
                       c_b_years=f"{yb / 1e6:.1f} million", c_b_say=num2words(round(yb / 1e6, 1), lang="en") + " million", c_b_str=f"{yb / 1e6:.1f}M years")
        elif k == "colors":
            n = 256 ** 3
            raw.update(c_n=f"{n:,}", c_n_say=num2words(n, lang="en"))
        elif k == "overflow":
            raw.update(c_stat="255 + 1 = " + str((255 + 1) % 256), c_max=255, c_wrap=(255 + 1) % 256)
        elif k == "binsearch":
            n = 10 ** 9
            st = math.ceil(math.log2(n))
            raw.update(c_stat=f"{st} steps", c_steps=st, c_steps_say=num2words(st, lang="en"))
        elif k == "fold":
            km = 0.0001 * 2 ** 42 / 1000
            raw.update(c_stat=f"{round(km):,} km", c_km_say=num2words(round(km), lang="en"), c_km=f"{round(km):,}")
        elif k == "chess":
            t = 2 ** 64 - 1
            d = len(str(t))
            raw.update(c_stat=f"{t / 10 ** (d - 1):.2f}e{d - 1}", c_say=num2words(round(t / 1e18, 1), lang="en") + " quintillion", c_t=f"{t:,}")
        elif k == "hash32":
            n = round(math.sqrt(2 * math.log(2) * 2 ** 32))
            raw.update(c_stat=f"{n:,}", c_n_say=num2words(n, lang="en"), c_n=f"{n:,}", c_space=f"{2 ** 32:,}")
        elif k == "ipv6mm":
            a = 2 ** 128
            mm2 = 510.1e6 * 1e12
            r = a / mm2
            raw.update(c_stat=f"{r / 10 ** int(math.log10(r)):.1f}e{int(math.log10(r))}", c_tot=f"{a:.2e}".replace("e+", "e"),
                       c_r_say=num2words(round(r / 10 ** int(math.log10(r)), 1), lang="en"), c_r_exp_say=num2words(int(math.log10(r)), lang="en"))
        elif k == "count1b":
            y = 1e9 / 31557600
            raw.update(c_stat=f"{y:.1f} years", c_y=f"{y:.1f}", c_y_say=num2words(round(y, 1), lang="en"))
        elif k == "emoji":
            raw.update(c_stat=f"{len(chr(0x1F600).encode())} bytes", c_b=len(chr(0x1F600).encode()), c_b_say=num2words(len(chr(0x1F600).encode()), lang="en"))
        elif k == "sorting":
            n = 10 ** 6
            nl, n2 = n * math.log2(n), n * n
            raw.update(c_stat=f"{nl / 1e6:.0f}M vs {n2 / 1e12:.0f}T", c_nl_say=num2words(round(nl / 1e6), lang="en") + " million", c_ratio_say=num2words(round(n2 / nl, -3), lang="en"), c_ratio=f"{round(n2 / nl, -3):,.0f}")
        elif k == "montyhall":
            # enumera os 9 casos (porta do carro x primeira escolha); o apresentador sempre abre uma porta com cabra
            wins_switch = wins_stay = 0
            for car in range(3):
                for pick in range(3):
                    opened = next(d for d in range(3) if d != pick and d != car)
                    switched = next(d for d in range(3) if d != pick and d != opened)
                    wins_switch += switched == car
                    wins_stay += pick == car
            sw, st = wins_switch / 9 * 100, wins_stay / 9 * 100
            raw.update(c_stat=f"{sw:.1f}%", c_sw=f"{sw:.1f}%", c_st=f"{st:.1f}%", c_sw_say=num2words(round(sw, 1), lang="en"),
                       c_st_say=num2words(round(st, 1), lang="en"), c_cases=9, c_cases_win=wins_switch)
        elif k == "counter64":
            yr = 31557600  # ano juliano, 365,25 dias
            y64 = 2 ** 64 / 1e9 / yr
            s32 = 2 ** 32 / 1e9
            raw.update(c_stat=f"{y64:.1f} years", c_y=f"{y64:.1f}", c_y_say=num2words(round(y64, 1), lang="en"),
                       c_s32=f"{s32:.1f}", c_s32_say=num2words(round(s32, 1), lang="en"))
        elif k == "unix2e9":
            import datetime
            d = datetime.datetime.fromtimestamp(2_000_000_000, datetime.timezone.utc)
            d1 = datetime.datetime.fromtimestamp(1_000_000_000, datetime.timezone.utc)
            raw.update(c_stat=f"{MESES_EN[d.month - 1][:3]} {d.day}, {d.year}", c_date=f"{MESES_EN[d.month - 1]} {d.day}, {d.year}",
                       c_year=d.year, c_time=d.strftime("%H:%M:%S") + " UTC", c_date_say=f"{MESES_EN[d.month - 1]} {num2words(d.day, lang='en', to='ordinal')}, {num2words(d.year, lang='en', to='year')}",
                       c_time_say=f"{num2words(d.hour, lang='en')} {num2words(d.minute, lang='en')} and {num2words(d.second, lang='en')} seconds, U T C",
                       c_1e9=f"{MESES_EN[d1.month - 1]} {d1.day}, {d1.year}", c_1e9_say=f"{MESES_EN[d1.month - 1]} {num2words(d1.day, lang='en', to='ordinal')}, {num2words(d1.year, lang='en', to='year')}")
        elif k == "leapyears":
            import calendar
            n = sum(calendar.isleap(y) for y in range(2001, 2401))
            avg = 365 + n / 400
            raw.update(c_stat=f"{n} of 400", c_n=n, c_n_say=num2words(n, lang="en"), c_avg=f"{avg:.4f}",
                       c_1900=str(calendar.isleap(1900)).lower(), c_2000=str(calendar.isleap(2000)).lower())
        elif k == "sunlight":
            au, cl = 149_597_870_700, 299_792_458  # UA (IAU 2012) e c (SI), ambos exatos por definicao
            t = au / cl
            mi, se = int(t // 60), round(t % 60)
            moon = 384_400_000 / cl  # distancia media Terra-Lua
            raw.update(c_stat=f"{mi} min {se} s", c_secs=round(t, 1), c_min=mi, c_sec=se, c_moon=f"{moon:.1f}", c_moon_say=num2words(round(moon, 1), lang="en"),
                       c_say=f"{num2words(mi, lang='en')} minutes and {num2words(se, lang='en')} seconds")
        elif k == "gpsrel":
            cl, gm = 299_792_458, 3.986004418e14  # c (SI) e GM da Terra (WGS 84)
            re, r = 6_371_000, 26_560_000  # raio medio da Terra e raio da orbita GPS (m)
            day = 86400
            gr = gm / cl ** 2 * (1 / re - 1 / r) * day  # relogio no alto adianta (gravidade mais fraca)
            v = math.sqrt(gm / r)
            sr = v ** 2 / (2 * cl ** 2) * day  # relogio em movimento atrasa
            net = (gr - sr) * 1e6
            km = (gr - sr) * cl / 1000
            raw.update(c_stat=f"{net:.1f} microseconds", c_us=f"{net:.1f}", c_us_say=num2words(round(net, 1), lang="en"),
                       c_gr=f"{gr * 1e6:.1f}", c_sr=f"{sr * 1e6:.1f}", c_gr_say=num2words(round(gr * 1e6, 1), lang="en"),
                       c_sr_say=num2words(round(sr * 1e6, 1), lang="en"), c_km=f"{km:.1f}", c_km_say=num2words(round(km, 1), lang="en"))
        elif k == "cube":
            n = math.factorial(8) * 3 ** 7 * math.factorial(12) * 2 ** 11 // 2
            q = n / 1e18
            raw.update(c_stat=f"{q:.0f} quintillion", c_n=f"{n:,}", c_q=f"{q:.0f}", c_q_say=num2words(round(q), lang="en"))
        elif k == "luhn":
            def ok(ds):
                s = 0
                for i, d in enumerate(reversed(ds)):
                    if i % 2 == 1:
                        d *= 2
                        if d > 9:
                            d -= 9
                    s += d
                return s % 10 == 0
            import random
            rnd = random.Random(7)
            single = single_caught = trans = trans_caught = 0
            for _ in range(2000):
                base = [rnd.randrange(10) for _ in range(15)]
                chk = next(c for c in range(10) if ok(base + [c]))
                num = base + [chk]
                for pos in range(16):
                    for dg in range(10):
                        if dg != num[pos]:
                            alt = num[:]; alt[pos] = dg
                            single += 1; single_caught += not ok(alt)
                for pos in range(15):
                    if num[pos] != num[pos + 1]:
                        alt = num[:]; alt[pos], alt[pos + 1] = alt[pos + 1], alt[pos]
                        trans += 1; trans_caught += not ok(alt)
            ps, pt = single_caught / single * 100, trans_caught / trans * 100
            raw.update(c_stat=f"{ps:.0f}%", c_single=f"{ps:.0f}%", c_single_say=num2words(round(ps), lang="en"),
                       c_trans=f"{pt:.0f}%", c_trans_say=num2words(round(pt), lang="en"))
        elif k == "ping":
            cl = 299_792.458  # km/s
            n_fiber = 1.468  # indice de grupo tipico de fibra monomodo em 1550 nm
            dkm = 1000
            rtt = 2 * dkm / (cl / n_fiber) * 1000
            vac = 2 * dkm / cl * 1000
            raw.update(c_stat=f"{rtt:.1f} ms", c_ms=f"{rtt:.1f}", c_ms_say=num2words(round(rtt, 1), lang="en"),
                       c_vac=f"{vac:.1f}", c_vac_say=num2words(round(vac, 1), lang="en"), c_km=f"{dkm:,}", c_fkms=f"{cl / n_fiber:,.0f}",
                       c_fkms_say=num2words(round(cl / n_fiber, -3), lang="en"))
        elif k == "shuffle":
            f = math.factorial(52)
            d = len(str(f))
            m = f / 10 ** (d - 1)
            raw.update(c_sci=f"{m:.2f}e{d - 1}", c_digits=d, c_digits_say=num2words(d, lang="en"),
                       c_m_say=num2words(round(m, 2), lang="en"), c_e_say=num2words(d - 1, lang="en"))
        ctx.update({k2: v for k2, v in raw.items() if k2.startswith("c_")})
    if "bcb" in c:
        from num2words import num2words
        b = c["bcb"]
        y, mo = b["from"].split("-")
        code = {"selic": 11, "usd": 1}[b["kind"]]
        sy, sm = (int(y), int(mo) + 1) if b["kind"] == "selic" else (int(y), int(mo))
        if sm == 13:
            sy, sm = sy + 1, 1
        rows = sgs_range(code, sy, sm)
        assert rows, f"sem dados do BCB ({code})"
        ly, lm = rows[-1]["data"].split("/")[2], rows[-1]["data"].split("/")[1]
        ip = 1.0
        for mm, v in ipca_series(b["from"]):
            if mm > b["from"]:
                ip *= 1 + v / 100
        say = lambda v: num2words(int(round(v)), lang="pt_BR")
        ip_pct = (ip - 1) * 100
        raw.update(b_from=f"{MESES[int(mo) - 1]} de {y}", b_to=f"{MESES[int(lm) - 1]} de {ly}", b_ip_pct=round(ip_pct), b_ip_pct_say=say(ip_pct))
        if b["kind"] == "selic":
            f = 1.0
            for r in rows:
                f *= 1 + float(r["valor"]) / 100
            fin, need = 1000 * f, 1000 * ip
            real = (f / ip - 1) * 100
            assert real > 0, "Selic nao ganhou da inflacao; revisar texto"
            raw.update(b_sel=round(fin), b_need=round(need), b_sel_pct=round((f - 1) * 100), b_real=round(real), b_real_say=say(real),
                       b_sel_say=say(fin) + " reais", b_need_say=say(need) + " reais")
        else:
            u0, u1 = float(rows[0]["valor"]), float(rows[-1]["valor"])
            up = (u1 / u0 - 1) * 100
            cur = lambda v: num2words(round(v, 2), lang="pt_BR", to="currency")
            raw.update(b_u0f=round(u0, 2), b_u1f=round(u1, 2), b_u0_say=cur(u0), b_u1_say=cur(u1), b_usd_pct=round(up), b_usd_pct_say=say(up),
                       b_word="mais" if up > ip_pct else "menos")
        ctx.update({k: v for k, v in raw.items() if k.startswith("b_")})
    if "unix2038" in c:
        import datetime
        from num2words import num2words
        mx = 2 ** 31 - 1
        d = datetime.datetime.fromtimestamp(mx, datetime.timezone.utc)
        raw.update(u_max=mx, u_max_say=num2words(mx, lang="en"), u_date=f"{MESES_EN[d.month - 1]} {d.day}, {d.year}",
                   u_year=d.year, u_time=d.strftime("%H:%M:%S") + " UTC", u_bits=32)
        ctx.update({k: v for k, v in raw.items() if k.startswith("u_")})
    if "minwage" in c:
        from num2words import num2words
        m = c["minwage"]
        y, mo = m["from"].split("-")
        url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.1619/dados?formato=json&dataInicial=01/{mo}/{y}"
        rows = None
        for _ in range(3):
            try:
                rows = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60))
                break
            except Exception as e:
                print("sgs1619 falhou:", e)
        a, b = float(rows[0]["valor"]), float(rows[-1]["valor"])
        ly, lm = rows[-1]["data"].split("/")[2], rows[-1]["data"].split("/")[1]
        ser = [(mm, v) for mm, v in ipca_series(m["from"]) if mm > m["from"]]
        f = 1.0
        for _, v in ser:
            f *= 1 + v / 100
        say = lambda v: num2words(int(round(v)), lang="pt_BR")
        mw_pct, ip_pct = (b / a - 1) * 100, (f - 1) * 100
        real = (b / a / f - 1) * 100
        raw.update(mw_a=round(a), mw_b=round(b), mw_pct=round(mw_pct), ip_pct=round(ip_pct), mw_real=round(real),
                   mw_a_say=say(a) + " reais", mw_b_say=say(b) + " reais", mw_pct_say=say(mw_pct), ip_pct_say=say(ip_pct), mw_real_say=say(real),
                   mw_from=f"{MESES[int(mo) - 1]} de {y}", mw_to=f"{MESES[int(lm) - 1]} de {ly}")
        ctx.update({k: v for k, v in raw.items() if k.startswith(("mw_", "ip_"))})
    if "ipca" in c:
        i = c["ipca"]
        ser = ipca_series(i["from"]) if "series" not in i else i["series"]
        ser = [(m, v) for m, v in ser if m > i["from"]]
        f = 1.0
        for _, v in ser:
            f *= 1 + v / 100
        y, mo = i["from"].split("-")
        ly, lm = ser[-1][0].split("-")
        amt = i.get("amount", 100)
        from num2words import num2words
        say = lambda v: num2words(int(round(v)), lang="pt_BR")
        raw.update(ipca_needed_say=say(amt * f) + " reais", ipca_amount_say=say(amt) + " reais", ipca_pct_say=say((f - 1) * 100),
                   ipca_factor=round(f, 2), ipca_amount_n=amt, ipca_needed_n=round(amt * f), ipca_pct=round((f - 1) * 100), ipca_needed=brl(amt * f), ipca_amount=brl(amt),
                   ipca_from=f"{MESES[int(mo) - 1]} de {y}", ipca_to=f"{MESES[int(lm) - 1]} de {ly}")
        ctx.update({k: v for k, v in raw.items() if k.startswith("ipca")})

def main(src, dst):
    spec = json.load(open(src, encoding="utf-8"))
    ctx = {}
    raw = {}
    for sc in spec["scenes"]:
        s = sc.get("source")
        if sc.get("type") == "chart" and s:
            if "worldbank" in s:
                ann = worldbank_annual(s["worldbank"], s.get("country", "USA"), s["from"], s["to"])
            else:
                ann = fred_annual(s["fred"], s["from"], s["to"])
            step = s.get("step", 1)
            years = [y for y in ann if (y - s["from"]) % step == 0]
            if years[-1] != max(ann):
                years.append(max(ann))
            sc["data"] = [{"x": str(y), "y": round(ann[y] * s.get("scale", 1), s.get("round", 1))} for y in years]
            f, l = sc["data"][0]["y"], sc["data"][-1]["y"]
            ctx.update(first_y=years[0], last_y=years[-1], first=f, last=l,
                       pct=round((l / f - 1) * 100), times=round(l / f, 1))
            def fmt(k, v):
                if k in ("first_y", "last_y"):
                    return str(v)
                if isinstance(v, float) and abs(v) >= 1000:
                    v = round(v)
                return f"{v:,}" if isinstance(v, (int, float)) and abs(v) >= 1000 else v
            raw.update({k: v for k, v in ctx.items() if k not in raw or not isinstance(v, str)})
            ctx.update({k: fmt(k, v) for k, v in raw.items()})
    compute_blocks(spec, ctx, raw)
    ctx.update({k: (v if not isinstance(v, (int, float)) or k in ('first_y','last_y') else v) for k, v in raw.items() if k not in ctx})
    def sub(t):
        return t.format(**ctx) if isinstance(t, str) and "{" in t else t
    for sc in spec["scenes"]:
        for k in ("narration", "caption", "text", "sub", "label", "title", "subtitle", "note", "hl", "big", "l1", "v1", "l2", "v2"):
            if k in sc:
                sc[k] = sub(sc[k])
        for k in [k for k in sc if k.endswith("_from") and k != "value_from"]:
            sc[k[:-5]] = raw[sc[k]]
        if sc.get("type") == "stat" and "value_from" in sc:
            if sc.get("as_str"):
                sc["str"] = str(raw[sc["value_from"]])
                sc["value"] = 0
            else:
                sc["value"] = raw[sc["value_from"]]
    if "yt" in spec:
        for k in ("title", "description"):
            spec["yt"][k] = sub(spec["yt"].get(k, ""))
    json.dump(spec, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("data ok", ctx)

if __name__ == "__main__":
    main(*sys.argv[1:3])

"""Locução com tempo-alvo por bloco (vídeo curto/TikTok), pt-BR.
1 pedido Gemini TTS por par modelo:voz com o roteiro inteiro (poupa cota) → corte nos blocos por alinhamento palavra a palavra
(faster-whisper) → cada bloco ajustado ao tempo-alvo (rubberband, atempo se faltar; fator limitado) → mesmo ganho em todos os
blocos (-16 LUFS, pico ≤ -1 dBFS).
Saída por par em out_loc/<modelo>_<voz>/: 01.wav…NN.wav (48 kHz, 24 bits, mono, só voz), locucao_timeline.wav (cada bloco no
seu início), locucao_unica.wav (blocos com 0,3 s entre eles), previa_timeline.mp3, palavras.json, legendas.srt (até 3 palavras
por legenda), legendas_blocos.srt. out_loc/report.json: tempos, fator de velocidade e conferência por transcrição.
Env: SCRIPT (json), PARES ("modelo:voz,modelo:voz"), GEMINI_KEY, WHISPER (small), RAW_DIR (reusa tomadas já geradas),
FAKE=1 (teste local sem TTS nem whisper)."""
import difflib, json, os, re, subprocess, sys, tempfile, unicodedata
import numpy as np, soundfile as sf

sys.path.insert(0, "scripts")

SR = 48000
MARGIN = 0.04        # respiro nas pontas de cada arquivo de bloco
LEAD = 0.05          # na timeline, a fala entra 50 ms depois do início do bloco
GAP_UNICA = 0.30     # silêncio entre blocos no arquivo único
LUFS, PEAK_DB = -16.0, -1.0
RATE_MIN, RATE_MAX = 0.88, float(os.environ.get("RATE_MAX", "1.30"))
FOLGA, FOLGA_FIM = float(os.environ.get("FOLGA", "0.10")), float(os.environ.get("FOLGA_FIM", "0.25"))  # sobra no fim da janela
TOL = 0.30
FAKE = os.environ.get("FAKE") == "1"

SCRIPT = os.environ.get("SCRIPT", "voicetest/cronos_tiktok.json")
S = json.load(open(SCRIPT))
BL = S["blocos"]
PRON = S.get("pron", {})
OUT = os.environ.get("OUT", "out_loc")
os.makedirs(OUT, exist_ok=True)
rep = {"script": SCRIPT, "regras": {"lufs": LUFS, "pico_db": PEAK_DB, "fator_min": RATE_MIN, "fator_max": RATE_MAX, "folga": FOLGA, "folga_fim": FOLGA_FIM,
                                    "lead_s": LEAD, "margem_s": MARGIN}, "vozes": {}}


def respell(t):
    for k, v in PRON.items():
        t = re.sub(rf"\b{k}\b", v, t)
    return t


def tts_text(b):
    return respell(b.get("tts", b["texto"]))


def norm(w):
    w = unicodedata.normalize("NFKD", w.lower())
    w = "".join(c for c in w if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", w)


def expand(tok):
    """palavra do whisper → palavras normalizadas (número por extenso; telefone e números longos dígito a dígito)."""
    raw = tok.strip()
    core = re.sub(r"[^0-9.,\-]", "", raw)
    if not re.search(r"\d", core):
        n = norm(raw)
        return [n] if n else []
    from num2words import num2words
    digits = re.sub(r"\D", "", core)
    out = []
    if "-" in core or (len(digits) >= 4 and "." not in core and "," not in core):  # telefone: DDD por extenso, resto dígito a dígito
        if digits.startswith("11") and len(digits) >= 6:
            out += ["onze"]; digits = digits[2:]
        for d in digits:
            out += num2words(int(d), lang="pt_BR").split()
    else:
        try:
            out += num2words(int(digits), lang="pt_BR").replace("-", " ").split()
        except Exception:
            out += [raw]
    if "%" in raw:
        out += ["por", "cento"]
    return [norm(w) for w in out if norm(w)]


_WM = None


def whisper_words(x, prompt=None):
    """[(palavra_normalizada, ini, fim)], texto ouvido."""
    global _WM
    import librosa
    from faster_whisper import WhisperModel
    if _WM is None:
        _WM = WhisperModel(os.environ.get("WHISPER", "small"), compute_type="int8")
    x16 = librosa.resample(np.asarray(x, dtype=np.float32), orig_sr=SR, target_sr=16000)
    segs, _ = _WM.transcribe(x16, language="pt", word_timestamps=True, vad_filter=False, beam_size=5, initial_prompt=prompt)
    out, txt = [], []
    for s in segs:
        txt.append(s.text)
        for w in s.words or []:
            toks = expand(w.word)
            if not toks:
                continue
            d = (w.end - w.start) / len(toks)
            for k, t in enumerate(toks):
                out.append((t, float(w.start + k * d), float(w.start + (k + 1) * d)))
    return out, " ".join(txt).strip()


def ref_tokens(t):
    return [(norm(w), w) for w in t.split() if norm(w)]


def align(ref, hyp):
    """mapa índice_ref → índice_hyp; nomes que o whisper escreve diferente viram a palavra do roteiro mais parecida."""
    vocab = set(ref)

    def fix(w):
        if w in vocab or len(w) < 4:
            return w
        best = max(vocab, key=lambda r: difflib.SequenceMatcher(None, w, r).ratio())
        return best if difflib.SequenceMatcher(None, w, best).ratio() >= 0.7 else w
    hyp2 = [(fix(h[0]), h[1], h[2]) for h in hyp]
    sm = difflib.SequenceMatcher(None, ref, [h[0] for h in hyp2], autojunk=False)
    m = {}
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            m[a + k] = b + k
    return m, hyp2


def rms_db(x, win):
    n = max(1, len(x) // win)
    r = np.sqrt((x[: n * win].reshape(n, win) ** 2).mean(axis=1) + 1e-12)
    return 20 * np.log10(r + 1e-9)


def quietest(x, t0, t1):
    a, b = int(t0 * SR), int(t1 * SR)
    if b - a < int(0.1 * SR):
        return (t0 + t1) / 2
    win = int(0.04 * SR)
    db = rms_db(x[a:b], win)
    return (a + int(np.argmin(db)) * win + win / 2) / SR


def trim(x):
    """corta silêncio nas pontas (40 dB abaixo do pico), deixando MARGIN."""
    win = int(0.01 * SR)
    db = rms_db(x, win)
    loud = np.where(db > db.max() - 40)[0]
    if len(loud) == 0:
        return x
    a = max(0, int(loud[0] * win - MARGIN * SR))
    b = min(len(x), int((loud[-1] + 1) * win + MARGIN * SR))
    return x[a:b]


def split_blocks(x):
    ref, owner = [], []
    for bi, b in enumerate(BL):
        for n, _ in ref_tokens(b["texto"]):
            ref.append(n); owner.append(bi)
    if FAKE:
        return fake_spans(x), 1.0, ""
    hyp, heard = whisper_words(x, prompt=" ".join(b["texto"] for b in BL))
    m, hyp2 = align(ref, hyp)
    starts, ends = {}, {}
    for i, bi in enumerate(owner):
        if i in m:
            t0, t1 = hyp2[m[i]][1], hyp2[m[i]][2]
            starts.setdefault(bi, t0); ends[bi] = t1
    nb, dur = len(BL), len(x) / SR
    for bi in range(nb):
        if bi not in starts:
            pe = ends.get(bi - 1, 0.0)
            nx = next((starts[j] for j in range(bi + 1, nb) if j in starts), dur)
            starts[bi], ends[bi] = pe + 0.2, max(pe + 0.3, nx - 0.2)
    cuts = [0.0]
    for bi in range(1, nb):
        a, b = ends[bi - 1], starts[bi]
        cuts.append(quietest(x, a, b) if b > a else (a + b) / 2)
    cuts.append(dur)
    cov = sum(1 for i in range(len(ref)) if i in m) / len(ref)
    return [(cuts[i], cuts[i + 1]) for i in range(nb)], cov, heard


def stretch(x, rate):
    if abs(rate - 1) < 0.005:
        return x, "nenhum"
    with tempfile.TemporaryDirectory() as td:
        a, b = f"{td}/a.wav", f"{td}/b.wav"
        sf.write(a, x, SR, subtype="FLOAT")
        flts = [(f"rubberband=tempo={rate:.4f}:transients=mixed:detector=compound:phase=laminar:window=standard:"
                 f"formant=preserved:pitchq=quality", "rubberband"), (f"atempo={rate:.4f}", "atempo")]
        for flt, name in flts:
            r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a, "-af", flt, "-ar", str(SR), "-ac", "1", b], capture_output=True)
            if r.returncode == 0:
                y, _ = sf.read(b, dtype="float32")
                return np.asarray(y, dtype=np.float32), name
    return x, "falhou"


def fit(x, bi):
    """ajusta a fala do bloco ao tempo-alvo: cabe na janela com ~0,1 s de folga; fator limitado a [RATE_MIN, RATE_MAX]."""
    b = BL[bi]
    w = b["fim"] - b["ini"]
    alvo = w - LEAD - (FOLGA_FIM if bi == len(BL) - 1 else FOLGA)
    d = len(x) / SR
    if alvo - TOL <= d <= alvo:
        return x, 1.0, "nenhum", alvo
    rate = d / (alvo if d > alvo else alvo - 0.1)
    rate = min(RATE_MAX, max(RATE_MIN, rate))
    y, how = stretch(x, rate)
    return trim(y), rate, how, alvo


def loudness_gain(xs):
    allx = np.concatenate(xs)
    try:
        import pyloudnorm as pyln
        lufs = pyln.Meter(SR).integrated_loudness(allx.astype(np.float64))
        g = 10 ** ((LUFS - lufs) / 20)
    except Exception:
        lufs, g = None, 10 ** ((-20 - 20 * np.log10(np.sqrt((allx ** 2).mean()) + 1e-9)) / 20)
    peak = float(np.max(np.abs(allx)) + 1e-9)
    g = min(g, 10 ** (PEAK_DB / 20) / peak)
    return float(g), lufs


def srt_time(t):
    t = max(0.0, t)
    h, m = int(t // 3600), int(t % 3600 // 60)
    s = t - h * 3600 - m * 60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}".replace(",1000", ",999")


def word_times(y, bi, t0):
    """tempos de cada palavra do roteiro dentro do bloco final (relativos à timeline, a partir de t0)."""
    refp = ref_tokens(BL[bi]["texto"])
    ref = [r[0] for r in refp]
    if FAKE:
        d = len(y) / SR
        hyp = [(r, MARGIN + k * (d - 2 * MARGIN) / len(ref), MARGIN + (k + 1) * (d - 2 * MARGIN) / len(ref)) for k, r in enumerate(ref)]
        heard = BL[bi]["texto"]
    else:
        hyp, heard = whisper_words(y)
    m, hyp2 = align(ref, hyp)
    tt = [None] * len(ref)
    for i in range(len(ref)):
        if i in m:
            tt[i] = [hyp2[m[i]][1], hyp2[m[i]][2]]
    # palavras não casadas: interpola entre vizinhas
    d = len(y) / SR
    i = 0
    while i < len(ref):
        if tt[i] is None:
            j = i
            while j < len(ref) and tt[j] is None:
                j += 1
            a = tt[i - 1][1] if i > 0 else MARGIN
            bnd = tt[j][0] if j < len(ref) else d - MARGIN
            step = max(0.05, (bnd - a) / (j - i))
            for k in range(i, j):
                tt[k] = [a + (k - i) * step, a + (k - i + 1) * step]
            i = j
        else:
            i += 1
    words = [{"bloco": bi + 1, "palavra": refp[k][1], "ini": round(t0 + tt[k][0], 3), "fim": round(t0 + tt[k][1], 3),
              "casada": k in m} for k in range(len(ref))]
    hn = [w for t in heard.split() for w in expand(t)]
    qc = difflib.SequenceMatcher(None, ref, hn).ratio()
    return words, round(qc, 3), heard


def chunks(words, maxw=3, maxdur=1.4):
    out, cur = [], []
    for w in words:
        cur.append(w)
        end_punct = re.search(r"[.,?!:…]$", w["palavra"])
        if len(cur) >= maxw or end_punct or (cur[-1]["fim"] - cur[0]["ini"]) >= maxdur:
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return out


def write_srt(path, cues):
    with open(path, "w", encoding="utf-8") as f:
        for i, (a, b, t) in enumerate(cues, 1):
            f.write(f"{i}\n{srt_time(a)} --> {srt_time(b)}\n{t}\n\n")


def fake_take():
    rng = np.random.default_rng(0)
    parts = []
    for b in BL:
        n = len(b["texto"].split())
        d = n * 0.27
        t = np.arange(int(d * SR)) / SR
        env = 0.3 * (0.6 + 0.4 * np.sin(2 * np.pi * 3 * t) ** 2)
        parts += [env * np.sin(2 * np.pi * 180 * t) + 0.01 * rng.standard_normal(len(t)), np.zeros(int(0.45 * SR))]
    return np.concatenate(parts).astype(np.float32)


def fake_spans(x):
    spans, t = [], 0.0
    for b in BL:
        d = len(b["texto"].split()) * 0.27
        spans.append((t, t + d + 0.45)); t += d + 0.45
    return spans


def process(tag, model, voice, x):
    d = f"{OUT}/{tag}"
    os.makedirs(d, exist_ok=True)
    spans, cov, heard_all = split_blocks(x)
    raw = [trim(x[int(a * SR):int(b * SR)]) for a, b in spans]
    fitted, info = [], []
    for bi, xb in enumerate(raw):
        y, rate, how, alvo = fit(xb, bi)
        fitted.append(y)
        info.append({"natural_s": round(len(xb) / SR, 2), "alvo_fala_s": round(alvo, 2), "fator": round(rate, 3), "metodo": how})
    g, lufs_in = loudness_gain(fitted)
    fitted = [np.clip(y * g, -1, 1).astype(np.float32) for y in fitted]
    # blocos soltos
    for i, y in enumerate(fitted, 1):
        sf.write(f"{d}/{i:02d}.wav", y, SR, subtype="PCM_24")
    # timeline: cada bloco no seu início (+LEAD); se o anterior invadir, empurra e registra
    starts, prev_end = [], 0.0
    for bi, y in enumerate(fitted):
        s = max(BL[bi]["ini"] + LEAD - MARGIN, prev_end + 0.06)
        starts.append(s); prev_end = s + len(y) / SR
    total = max(BL[-1]["fim"], prev_end + 0.2)
    tl = np.zeros(int(total * SR) + 1, dtype=np.float32)
    for s, y in zip(starts, fitted):
        a = int(s * SR); tl[a:a + len(y)] += y
    sf.write(f"{d}/locucao_timeline.wav", tl, SR, subtype="PCM_24")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{d}/locucao_timeline.wav", "-b:a", "192k", f"{d}/previa_timeline.mp3"], check=False)
    # arquivo único com 0,3 s entre blocos
    gap = np.zeros(int(max(0.0, GAP_UNICA - 2 * MARGIN) * SR), dtype=np.float32)
    head = np.zeros(int(0.1 * SR), dtype=np.float32)
    un = [head]
    for i, y in enumerate(fitted):
        un += [y] + ([gap] if i < len(fitted) - 1 else [head])
    sf.write(f"{d}/locucao_unica.wav", np.concatenate(un), SR, subtype="PCM_24")
    # palavras, legendas e conferência
    words, blk = [], []
    for bi, (s, y) in enumerate(zip(starts, fitted)):
        w, qc, heard = word_times(y, bi, s)
        words += w
        fs = s + MARGIN; fe = s + len(y) / SR - MARGIN
        win = (BL[bi]["ini"], BL[bi]["fim"])
        blk.append({**info[bi], "bloco": bi + 1, "final_s": round(len(y) / SR, 2), "fala_ini": round(fs, 2), "fala_fim": round(fe, 2),
                    "janela": [win[0], win[1]], "fala_cabe_na_janela": bool(fs >= win[0] - 0.01 and fe <= win[1] + 0.01),
                    "qc": qc, "ouvido": heard})
    json.dump({"timeline_s": round(total, 2), "palavras": words}, open(f"{d}/palavras.json", "w"), ensure_ascii=False, indent=1)
    write_srt(f"{d}/legendas.srt", [(c[0]["ini"], c[-1]["fim"], " ".join(w["palavra"] for w in c)) for c in chunks(words)])
    write_srt(f"{d}/legendas_blocos.srt", [(b["fala_ini"], b["fala_fim"], BL[b["bloco"] - 1]["texto"]) for b in blk])
    rep["vozes"][tag] = {"modelo": model, "voz": voice, "tomada_s": round(len(x) / SR, 2), "cobertura_alinhamento": round(cov, 3),
                         "lufs_tomada": None if lufs_in is None else round(float(lufs_in), 1), "ganho_db": round(20 * np.log10(g), 1),
                         "timeline_s": round(total, 2), "qc_medio": round(float(np.mean([b["qc"] for b in blk])), 3),
                         "fora_da_janela": [b["bloco"] for b in blk if not b["fala_cabe_na_janela"]], "blocos": blk,
                         "ouvido_tomada": heard_all[:800]}
    print(tag, json.dumps({k: v for k, v in rep["vozes"][tag].items() if k not in ("blocos", "ouvido_tomada")}, ensure_ascii=False))
    for b in blk:
        print("  ", b["bloco"], b["natural_s"], "→", b["final_s"], "fator", b["fator"], b["metodo"], "qc", b["qc"], "|", b["ouvido"][:80])


def main():
    pares = [p.strip() for p in os.environ.get("PARES", "gemini-3.8-flash-tts:Algieba").split(",") if p.strip()]
    text = "\n\n".join(tts_text(b) for b in BL)
    rep["texto_tts"] = text
    raw_dir = os.environ.get("RAW_DIR", "")
    for p in pares:
        model, voice = p.split(":")
        tag = f"{model}_{voice}"
        try:
            rawp = f"{raw_dir}/{tag}_tomada.wav" if raw_dir else ""
            if FAKE:
                x = fake_take()
            elif rawp and os.path.exists(rawp):
                x, sr = sf.read(rawp, dtype="float32")
                assert sr == SR
            else:
                import ltts
                import librosa
                x = ltts.gemini_once(text, voice, S["style"], model)
                x = librosa.resample(np.asarray(x, dtype=np.float32), orig_sr=ltts.SR, target_sr=SR)
            sf.write(f"{OUT}/{tag}_tomada.wav", x, SR, subtype="PCM_16")
            process(tag, model, voice, x)
        except Exception as e:
            import traceback
            traceback.print_exc()
            rep["vozes"][tag] = {"erro": repr(e)[:500]}
        json.dump(rep, open(f"{OUT}/report.json", "w"), indent=1, ensure_ascii=False, default=float)


if __name__ == "__main__":
    main()

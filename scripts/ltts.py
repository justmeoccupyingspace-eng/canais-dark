"""Vídeo longo: narração (Gemini TTS por ato) → alinhamento por Whisper → timeline com tempos reais de cada shot e cue.
Uso: python scripts/ltts.py specs/long/a-L01.json public/build/a-L01.data.json public/build/a-L01.json [--fake]
--fake: sem TTS (tempo estimado por palavra) para stills locais."""
import base64, difflib, json, os, re, subprocess, sys, time, urllib.request
import numpy as np

FPS = 30
SR = 24000
ACT_GAP = float(os.environ.get("ACT_GAP", "1.6"))  # respiro entre atos (cartela de capítulo)
LEAD = 0.18  # o visual entra um pouco antes da fala
API = "https://generativelanguage.googleapis.com/v1beta"
TAG_P = os.environ.get("TAG_P", "")  # {p}
TAG_PP = os.environ.get("TAG_PP", "[pause]")  # {pp}
TAG_SOFT = os.environ.get("TAG_SOFT", "")  # <soft>


def plain(t):
    return re.sub(r"\s+", " ", re.sub(r"\{p+\}|</?soft>", " ", t)).strip()


def for_tts(t):
    t = t.replace("{pp}", f" {TAG_PP} " if TAG_PP else " ... ").replace("{p}", f" {TAG_P} " if TAG_P else " ")
    t = t.replace("<soft>", f" {TAG_SOFT} " if TAG_SOFT else " ").replace("</soft>", " ")
    return re.sub(r"\s+", " ", t).strip()


# ---------- TTS ----------
DEAD_MODELS = set()  # modelos que estouraram a cota diária nesta execução


def gemini_once(text, voice, style, model):
    key = os.environ["GEMINI_KEY"]
    prompt = style + "\n\n" + text
    if "3.8" in model:  # o 3.8 às vezes LÊ as instruções em voz alta: seções explícitas, só a transcrição é fala
        prompt = "### DIRECTOR'S NOTES\n" + style + "\n\n#### TRANSCRIPT\n" + text
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    req = urllib.request.Request(f"{API}/models/{model}:generateContent?key={key}", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=900))
    parts = [p for c in r.get("candidates", []) for p in c.get("content", {}).get("parts", []) if "inlineData" in p]
    if not parts:
        raise ValueError("resposta sem áudio: " + json.dumps(r)[:300])
    chunks = []
    for p in parts:
        mime = p["inlineData"].get("mimeType", "")
        raw = base64.b64decode(p["inlineData"]["data"])
        if not getattr(gemini_once, "said", False):
            print(f"::notice title=gemini mime::{model} → {mime!r} ({len(raw)} bytes, head {raw[:4]!r})")
            gemini_once.said = True
        if raw[:4] == b"RIFF" or "wav" in mime or "mpeg" in mime or "mp3" in mime or "ogg" in mime or "flac" in mime:
            import io
            import soundfile as sf_
            try:
                x, sr = sf_.read(io.BytesIO(raw), dtype="float32", always_2d=False)
            except Exception:  # mp3 sem suporte no libsndfile → ffmpeg
                import subprocess, tempfile
                with tempfile.NamedTemporaryFile(suffix=".bin") as tf:
                    tf.write(raw); tf.flush()
                    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", tf.name, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
                x, sr = np.frombuffer(pcm, dtype="<i2").astype(np.float32) / 32768, SR
            if x.ndim > 1:
                x = x.mean(axis=1)
        else:
            m = re.search(r"rate=(\d+)", mime)
            sr = int(m.group(1)) if m else 24000
            x = np.frombuffer(raw[: len(raw) // 2 * 2], dtype="<i2").astype(np.float32) / 32768
        if sr != SR:
            import librosa
            x = librosa.resample(x, orig_sr=sr, target_sr=SR)
        chunks.append(x)
    return np.concatenate(chunks)


def gemini(text, voice, style, models):
    """tenta cada modelo; 429 de cota diária marca o modelo como esgotado e passa ao próximo; sem retentativa às cegas."""
    for model in models:
        if model in DEAD_MODELS:
            continue
        for i in range(2):
            try:
                x = gemini_once(text, voice, style, model)
                return x, model
            except Exception as e:
                body_err = ""
                try:
                    body_err = e.read().decode()[:400] if hasattr(e, "read") else ""
                except Exception:
                    pass
                code = getattr(e, "code", None)
                msg = (repr(e)[:120] + " " + body_err.replace("\n", " "))[:400]
                print(f"::warning title=gemini::{model} tentativa {i}: {msg}")
                if code == 429 and "per day" in body_err:
                    DEAD_MODELS.add(model)
                    break
                if code == 429:
                    time.sleep(65)
                    continue
                if code and 400 <= code < 500:
                    break
                time.sleep(15)
    raise RuntimeError("gemini indisponível em " + ", ".join(models))


def edge(text, voice="en-US-AndrewMultilingualNeural"):
    import asyncio, tempfile, edge_tts, soundfile as sf
    with tempfile.TemporaryDirectory() as d:
        asyncio.run(edge_tts.Communicate(re.sub(r"\[[^\]]*\]", "", text), voice, rate="+4%").save(f"{d}/a.mp3"))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{d}/a.mp3", "-ac", "1", "-ar", str(SR), f"{d}/a.wav"], check=True)
        x, _ = sf.read(f"{d}/a.wav", dtype="float32")
    return x


def tighten(x, cap=0.55):
    """encurta silêncios longos para no máximo `cap` s (mantém o ritmo das pausas curtas)."""
    hop = int(SR * 0.01)
    n = len(x) // hop
    e = np.sqrt(np.mean(x[: n * hop].reshape(n, hop) ** 2, axis=1))
    sil = e < e.max() * 0.02
    out, i = [], 0
    while i < n:
        j = i
        while j < n and sil[j] == sil[i]:
            j += 1
        seg = x[i * hop: j * hop]
        if sil[i] and len(seg) > cap * SR:
            h = int(cap * SR / 2)
            seg = np.concatenate([seg[:h], seg[-h:]])
        out.append(seg)
        i = j
    out.append(x[n * hop:])
    return np.concatenate(out)


def tempo(x, k):
    if abs(k - 1) < 0.005:
        return x
    import soundfile as sf, tempfile
    with tempfile.TemporaryDirectory() as d:
        sf.write(f"{d}/a.wav", x, SR)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{d}/a.wav", "-af", f"atempo={k}", f"{d}/b.wav"], check=True)
        y, _ = sf.read(f"{d}/b.wav", dtype="float32")
    return y


def clean(x):
    """corta silêncio nas pontas, tira graves, nivela (~-18 dBFS RMS na fala) com limitador suave."""
    from scipy.signal import butter, sosfilt
    idx = np.where(np.abs(x) > 0.004)[0]
    if len(idx):
        x = x[max(idx[0] - int(0.05 * SR), 0): min(idx[-1] + int(0.25 * SR), len(x))]
    x = sosfilt(butter(2, 70 / (SR / 2), btype="high", output="sos"), x)
    e = np.sqrt(np.convolve(x ** 2, np.ones(int(0.05 * SR)) / int(0.05 * SR), "same"))
    speech = x[e > 0.02 * e.max()]
    x = x * (0.125 / (np.sqrt(np.mean(speech ** 2)) + 1e-9))
    return (np.tanh(x * 1.15) / np.tanh(1.15) * 0.97).astype(np.float32)


# ---------- alinhamento ----------
def toks(w):
    from num2words import num2words
    w = w.lower().replace("’", "'")
    out = []
    for p in re.findall(r"[a-z']+|\d[\d,\.]*", w):
        if p[0].isdigit():
            n = p.replace(",", "")
            try:
                if re.fullmatch(r"(19|20)\d\d", n):
                    p = num2words(int(n), to="year")
                elif "." in n:
                    p = num2words(float(n))
                else:
                    p = num2words(int(n))
            except Exception:
                pass
            out += re.findall(r"[a-z]+", p.replace("-", " "))
        else:
            out += [p.strip("'")] if p.strip("'") else []
    return [t for t in out if t not in ("and",)] or [""]


def align(script_words, hyp):
    """script_words: lista de palavras do roteiro; hyp: [(palavra, t0, t1)] do Whisper. Retorna [(t0, t1)] por palavra do roteiro."""
    A, amap = [], []
    for i, w in enumerate(script_words):
        for t in toks(w):
            A.append(t); amap.append(i)
    B, bmap = [], []
    for j, (w, _, _) in enumerate(hyp):
        for t in toks(w):
            B.append(t); bmap.append(j)
    sm = difflib.SequenceMatcher(a=A, b=B, autojunk=False)
    t0 = [None] * len(script_words)
    t1 = [None] * len(script_words)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            i, j = amap[blk.a + k], bmap[blk.b + k]
            if t0[i] is None:
                t0[i] = hyp[j][1]
            t1[i] = hyp[j][2]
    matched = sum(1 for v in t0 if v is not None)
    # interpola lacunas
    known = [i for i, v in enumerate(t0) if v is not None]
    if not known:
        raise RuntimeError("alinhamento vazio")
    for i in range(len(t0)):
        if t0[i] is None:
            prv = max([k for k in known if k < i], default=None)
            nxt = min([k for k in known if k > i], default=None)
            if prv is None:
                t0[i] = max(0.0, t0[nxt] - 0.3 * (nxt - i))
            elif nxt is None:
                t0[i] = t1[prv] + 0.3 * (i - prv)
            else:
                t0[i] = t1[prv] + (t0[nxt] - t1[prv]) * (i - prv) / (nxt - prv)
            t1[i] = t0[i] + 0.25
    return list(zip(t0, t1)), matched / max(len(script_words), 1)


def junk_spans(times, dur, lead=2.0, gap=2.5):
    """trechos de fala fora do roteiro (ex.: o TTS lendo as instruções): antes da 1ª palavra, entre palavras e no fim.
    As pausas reais já vêm limitadas a ~0,55 s pelo tighten, então qualquer buraco > 2,5 s não é pausa."""
    sp_ = []
    if times and times[0][0] > lead:
        sp_.append((0.0, times[0][0] - 0.25))
    for i in range(len(times) - 1):
        if times[i + 1][0] - times[i][1] > gap:
            sp_.append((times[i][1] + 0.25, times[i + 1][0] - 0.25))
    if times and dur - times[-1][1] > gap:
        sp_.append((times[-1][1] + 0.3, dur))
    return sp_


def snap(x, t, lo, hi):
    """move o ponto de corte para o trecho de 20 ms mais silencioso dentro de [lo, hi] (não deixa sobra de sílaba)."""
    lo, hi = max(0.0, lo), min(len(x) / SR, hi)
    if hi - lo < 0.04:
        return t
    n = int(0.02 * SR)
    seg = x[int(lo * SR):int(hi * SR)]
    k = len(seg) // n
    if k < 2:
        return t
    e = np.sqrt(np.mean(seg[: k * n].reshape(k, n) ** 2, axis=1))
    return lo + (int(np.argmin(e)) + 0.5) * n / SR


def frames_db(x, lo, hi, n):
    seg = x[int(lo * SR):int(hi * SR)]
    k = len(seg) // n
    return 20 * np.log10(np.sqrt(np.mean(seg[: k * n].reshape(k, n) ** 2, axis=1)) + 1e-9) if k else np.array([])


def onset(x, t_word, thr=-45.0):
    """início real da fala que contém a 1ª palavra mantida: último ataque precedido de ≥100 ms de silêncio,
    o mais perto do tempo do Whisper (que erra uns décimos)."""
    n = int(0.02 * SR)
    lo = max(0.0, t_word - 1.2)
    e = frames_db(x, lo, min(len(x) / SR, t_word + 0.6), n)
    cands = [i for i in range(5, len(e)) if e[i] > thr and all(e[i - k] <= thr for k in range(1, 6))]
    if not cands:
        return None
    best = min(cands, key=lambda i: abs(lo + i * n / SR - t_word))
    return lo + best * n / SR - 0.06


def offset(x, t_word, thr=-45.0):
    """fim real da fala mantida antes de um corte: 1º trecho de ≥100 ms de silêncio depois da palavra."""
    n = int(0.02 * SR)
    lo = max(0.0, t_word - 0.15)
    e = frames_db(x, lo, min(len(x) / SR, t_word + 0.8), n)
    for i in range(len(e) - 5):
        if all(e[i + k] <= thr for k in range(5)):
            return lo + i * n / SR + 0.06
    return None


def excise(x, times, spans):
    ref = []
    for a, b in spans:
        if a > 0:
            prev = max((t1 for t0, t1 in times if t1 <= a + 0.3), default=a)
            a2 = offset(x, prev) or snap(x, a, a - 0.23, a + 0.4)
        else:
            a2 = 0.0
        if b < len(x) / SR:
            nxt = min((t0 for t0, t1 in times if t0 >= b - 0.3), default=b)
            b2 = onset(x, nxt) or snap(x, b, b - 0.4, b + 0.2)
        else:
            b2 = b
        ref.append((min(a2, b2), max(a2, b2)))
    spans = ref
    keep = np.ones(len(x), bool)
    for a, b in spans:
        keep[int(a * SR):int(b * SR)] = False
    def sh(t):
        return t - sum(min(max(0.0, t - a), b - a) for a, b in spans)
    return x[keep], [(sh(t0), sh(t1)) for t0, t1 in times]


def whisper_words(path):
    from faster_whisper import WhisperModel
    if not hasattr(whisper_words, "m"):
        whisper_words.m = WhisperModel(os.environ.get("WHISPER", "small.en"), compute_type="int8")
    import soundfile as sf, librosa
    x, sr = sf.read(path, dtype="float32")
    x16 = librosa.resample(x, orig_sr=sr, target_sr=16000)
    segs, _ = whisper_words.m.transcribe(x16, language="en", word_timestamps=True, vad_filter=False, beam_size=5)
    return [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]


# ---------- métricas de 'vida' ----------
def metrics(x, nwords):
    import librosa
    dur = len(x) / SR
    y = librosa.resample(x, orig_sr=SR, target_sr=16000)
    f0, _, _ = librosa.pyin(y, fmin=60, fmax=400, sr=16000, frame_length=1024)
    f = f0[~np.isnan(f0)]
    st = 12 * np.log2(f / np.median(f)) if len(f) else np.zeros(1)
    hop = int(SR * 0.01)
    e = np.sqrt(np.mean(x[: len(x) // hop * hop].reshape(-1, hop) ** 2, axis=1))
    sil = e < e.max() * 0.02
    runs, c = [], 0
    for v in sil:
        if v:
            c += 1
        else:
            if c:
                runs.append(c)
            c = 0
    longp = [r / 100 for r in runs if r >= 50]
    return dict(dur=round(dur, 1), wpm=round(nwords / dur * 60), f0_std=round(float(np.std(st)), 2),
                f0_p10_90=round(float(np.percentile(st, 90) - np.percentile(st, 10)), 1), pauses_05=len(longp), pause_total=round(sum(longp), 1))


# ---------- cues ----------
CUEKEYS = {"at": "t", "until": "t_until", "at_b": "t_b", "reveal_last": "t_last"}


def norm_words(s):
    return [re.sub(r"[^a-z0-9']", "", w.lower().replace("’", "'")) for w in s.split()]


def find_phrase(words, phrase, after=0):
    p = [w for w in norm_words(phrase) if w]
    n = [w for w in norm_words(" ".join(words))]
    for i in range(after, len(n) - len(p) + 1):
        if n[i:i + len(p)] == p:
            return i
    for i in range(0, len(n) - len(p) + 1):  # tolera ordem
        if n[i:i + len(p)] == p:
            return i
    return None


def resolve(obj, words, times, missing, sid):
    if isinstance(obj, dict):
        for k, tk in CUEKEYS.items():
            if isinstance(obj.get(k), str):
                i = find_phrase(words, obj[k])
                if i is None:
                    missing.append(f"{sid}: '{obj[k]}'")
                else:
                    obj[tk] = round(times[i][0] + obj.get("delay", 0), 3)
        for v in obj.values():
            resolve(v, words, times, missing, sid)
    elif isinstance(obj, list):
        for v in obj:
            resolve(v, words, times, missing, sid)


def main(src, data_path, dst, fake=False):
    import soundfile as sf
    spec = json.load(open(src))
    name = spec["id"]
    outdir = f"public/audio/{name}"
    os.makedirs(outdir, exist_ok=True)
    v = spec["voice"]
    models = [m for m in (os.environ.get("TTS_MODEL") or v.get("model") or "gemini-3.8-flash-tts").split(",") if m]
    used_model = None
    acts = sorted({s["act"] for s in spec["shots"]})
    tracks, words_all, report = [], [], []
    t_cursor = 0.0
    env_full = []
    for a in acts:
        shots = [s for s in spec["shots"] if s["act"] == a]
        script = [w for s in shots for w in plain(s["narration"]).split()]
        bounds = np.cumsum([0] + [len(plain(s["narration"]).split()) for s in shots])
        if fake:
            times, t = [], 0.0
            for s in shots:
                for tok in re.sub(r"(\{p+\})", r" \1 ", s["narration"]).split():
                    if tok == "{p}":
                        t += 0.35
                    elif tok == "{pp}":
                        t += 0.8
                    elif tok in ("<soft>", "</soft>"):
                        continue
                    else:
                        tok2 = tok.replace("<soft>", "").replace("</soft>", "")
                        if not tok2:
                            continue
                        d = 0.12 + 0.055 * len(tok2) + (0.25 if tok2[-1] in ".?!" else 0.1 if tok2[-1] in ",:;" else 0)
                        times.append((t, t + d * 0.8)); t += d
            dur = t + 0.3
            x = np.zeros(int(dur * SR), np.float32)
            for t0, t1 in times:
                n0, n1 = int(t0 * SR), int(t1 * SR)
                x[n0:n1] = 0.1 * np.sin(np.linspace(0, 400 * (t1 - t0) * 2 * np.pi, n1 - n0))
            ratio = 1.0
        else:
            text = " ".join(for_tts(s["narration"]) for s in shots)
            try:
                if os.environ.get("TTS_ENGINE") == "edge":
                    raise RuntimeError("edge forçado (teste)")
                # cache por texto+voz+estilo: áudio já pago (cota) nunca é pedido de novo
                import hashlib
                os.makedirs("public/audio/ttscache", exist_ok=True)
                hit = None
                for mdl_ in ([used_model] if used_model else models):
                    hk = hashlib.sha1((text + v.get("name", "Charon") + v["style"] + mdl_).encode()).hexdigest()[:16]
                    if os.path.exists(f"public/audio/ttscache/{hk}.wav"):
                        hit = (f"public/audio/ttscache/{hk}.wav", mdl_)
                        break
                if hit:
                    x, _ = sf.read(hit[0], dtype="float32")
                    mdl = hit[1]
                    print("cache de voz", a, mdl)
                else:
                    # ato longo vai em pedaços (grupos de shots ≤ MAXW palavras): respostas longas falham mais
                    maxw = int(os.environ.get("MAXW", "210"))
                    groups, cur, cw = [], [], 0
                    for s_ in shots:
                        n_ = len(plain(s_["narration"]).split())
                        if cur and cw + n_ > maxw:
                            groups.append(cur); cur, cw = [], 0
                        cur.append(s_); cw += n_
                    if cur:
                        groups.append(cur)
                    parts_ = []
                    mdl = used_model
                    for g_ in groups:
                        tg = " ".join(for_tts(s_["narration"]) for s_ in g_)
                        got = None
                        for m_ in ([mdl] if mdl else models):
                            hk = hashlib.sha1((tg + v.get("name", "Charon") + v["style"] + m_).encode()).hexdigest()[:16]
                            if os.path.exists(f"public/audio/ttscache/{hk}.wav"):
                                got = sf.read(f"public/audio/ttscache/{hk}.wav", dtype="float32")[0]
                                mdl = m_
                                print("cache de voz (pedaço)", a, m_)
                                break
                        if got is None:
                            got, mdl = gemini(tg, v.get("name", "Charon"), v["style"], [mdl] if mdl else models)
                            hk = hashlib.sha1((tg + v.get("name", "Charon") + v["style"] + mdl).encode()).hexdigest()[:16]
                            sf.write(f"public/audio/ttscache/{hk}.wav", got, SR)
                            time.sleep(float(os.environ.get("TTS_GAP", "20")))
                        parts_.append(got)
                        parts_.append(np.zeros(int(0.32 * SR), np.float32))
                    x = np.concatenate(parts_[:-1])
                used_model = mdl
                eng = "gemini:" + mdl
            except Exception as e:
                if os.environ.get("TTS_ENGINE", "gemini") != "edge" and os.environ.get("ALLOW_EDGE", "0") != "1":
                    print(f"::error title=tts::Gemini falhou no ato {a} e o fallback para Edge está desligado: {repr(e)[:200]}")
                    sys.exit(1)
                print("::warning title=tts::gemini falhou no ato", a, "— usando edge", repr(e)[:80])
                x = edge(text)
                eng = "edge"
            if eng.startswith("gemini"):
                x = tighten(x, float(os.environ.get("PAUSE_CAP", "0.55")))
                x = tempo(x, float(os.environ.get("ATEMPO") or "1.0"))
            x = clean(x)
            p = f"{outdir}/act{a}.wav"
            sf.write(p, x, SR)
            hyp = whisper_words(p)
            times, ratio = align(script, hyp)
            cuts = junk_spans(times, len(x) / SR)
            if cuts:
                x, times = excise(x, times, cuts)
                sf.write(p, x, SR)
                print(f"::warning title=tts::ato {a}: cortei {sum(b - a_ for a_, b in cuts):.1f} s de fala fora do roteiro em {len(cuts)} trecho(s)")
            m = metrics(x, len(script))
            m["cut_s"] = round(sum(b - a_ for a_, b in cuts), 1)
            m.update(act=a, engine=eng, align=round(ratio, 3))
            report.append(m)
            print("ato", a, m)
            dur = len(x) / SR
        sf.write(f"{outdir}/act{a}.wav", x, SR) if fake else None
        off = t_cursor + (ACT_GAP if a > acts[0] else 0.4)
        tracks.append(dict(act=a, file=f"audio/{name}/act{a}.wav", t=round(off, 3), dur=round(dur, 3)))
        for k, s in enumerate(shots):
            ws = plain(s["narration"]).split()
            tt = [(off + t0, off + t1) for t0, t1 in times[bounds[k]:bounds[k + 1]]]
            s["words"] = [dict(w=w, t0=round(t0, 3), t1=round(t1, 3)) for w, (t0, t1) in zip(ws, tt)]
            s["_tt"] = tt
            s["t0"] = round(max(0.0, (tt[0][0] if tt else off) - LEAD), 3)
            s["t_speech_end"] = round(tt[-1][1] if tt else off, 3)
        t_cursor = off + dur
    shots = spec["shots"]
    for i, s in enumerate(shots):
        s["t1"] = shots[i + 1]["t0"] if i + 1 < len(shots) else round(s["t_speech_end"] + s.get("hold", 2.0), 3)
    if shots[0]["t0"] > 0:
        shots[0]["t0"] = 0.0
    missing = []
    for s in shots:
        ws = [w["w"] for w in s["words"]]
        resolve({k: v for k, v in s.items() if k not in ("words", "_tt", "narration")}, ws, s["_tt"], missing, s.get("id", s["type"]))
        del s["_tt"]
    if missing:
        for m_ in missing:
            print(f"::error title=cue::frase não encontrada {m_}")
        if not fake:
            sys.exit(1)
    total = shots[-1]["t1"]
    # envelope da voz por quadro (boca do mascote + ducking da trilha)
    nfr = int(np.ceil(total * FPS)) + 1
    env = np.zeros(nfr)
    for tr in tracks:
        x, _ = sf.read("public/" + tr["file"], dtype="float32")
        n = SR // FPS
        m_ = len(x) // n
        e = np.sqrt(np.mean(x[: m_ * n].reshape(m_, n) ** 2, axis=1))
        f0 = int(round(tr["t"] * FPS))
        env[f0:f0 + m_] = e[: max(0, min(m_, nfr - f0))]
    env = env / (np.percentile(env[env > 0], 95) + 1e-9) if (env > 0).any() else env
    env = np.clip(np.convolve(env, [0.25, 0.5, 0.25], "same"), 0, 1)
    # trilhas: âncora por ato ou por shot; cada uma vai até a próxima (+0.8 s de cruzamento) ou até um music_stop
    starts = []
    for mu in spec.get("music", []):
        if not mu.get("track"):
            continue
        if "shot" in mu:
            sh_ = next(x for x in shots if x.get("id") == mu["shot"])
            t_a = sh_["t0"] - 0.3
        else:
            a_shots = [x for x in shots if x["act"] == mu["act"]]
            t_a = (a_shots[0]["t0"] - (0.6 if mu["act"] else 0.0)) if a_shots else 0
        starts.append((max(0.0, t_a), mu))
    starts.sort(key=lambda z: z[0])
    stops = sorted(x["music_stop"]["t"] for x in shots if x.get("music_stop", {}).get("t") is not None)
    music = []
    for k, (t_a, mu) in enumerate(starts):
        t_b = starts[k + 1][0] + 0.8 if k + 1 < len(starts) else total
        for st in stops:
            if t_a < st < t_b:
                t_b = st
                break
        music.append(dict(file=mu["track"].replace(" ", "_") + ".mp3", title=mu["track"], t=round(t_a, 3), end=round(t_b, 3), vol=mu.get("vol", 0.25), seek=mu.get("seek", 0)))
    data = json.load(open(data_path))
    out = dict(spec, shots=shots, tracks=tracks, env=[round(float(x_), 3) for x_ in env], music=music, total=round(total, 3), data=data, voice_report=report)
    json.dump(out, open(dst, "w"), ensure_ascii=False)
    print("timeline ok", dst, f"{total:.1f}s", f"{total / 60:.2f} min", len(shots), "shots")
    gates = []
    for m in report:
        if not (122 <= m["wpm"] <= 185):
            gates.append(f"ato {m['act']}: {m['wpm']} wpm fora de 122–185")
        if m["f0_std"] < 2.5:
            gates.append(f"ato {m['act']}: voz monótona (F0 std {m['f0_std']} st)")
        if m["align"] < 0.85:
            gates.append(f"ato {m['act']}: Whisper bateu só {m['align']:.0%} das palavras (TTS pulou/trocou texto?)")
    if not fake and total < spec.get("min_total", 8 * 60 + 5):
        gates.append(f"duração {total / 60:.2f} min < {spec.get('min_total', 485) / 60:.2f} min")
    for g in gates:
        print(f"::warning title=gate::{g}")
    json.dump(dict(report=report, gates=gates, total=total), open(dst.replace(".json", ".gates.json"), "w"), indent=1)


if __name__ == "__main__":
    try:
        main(sys.argv[1], sys.argv[2], sys.argv[3], fake="--fake" in sys.argv)
    except SystemExit:
        raise
    except Exception as e:
        import traceback
        tb = traceback.format_exc().strip().splitlines()
        print(f"::error title=ltts::{repr(e)[:300]} | " + " | ".join(l.strip() for l in tb[-8:])[:1000])
        sys.exit(1)

"""Locução por blocos (pt-BR) para vídeo institucional: 1 arquivo WAV 48 kHz mono por bloco, só voz, 0,3 s de silêncio nas pontas.
- engine=gemini: 1 pedido por voz com o roteiro inteiro (poupa a cota de 10/dia), depois corta nos limites dos blocos usando
  alinhamento palavra a palavra (faster-whisper 'small', pt) entre o roteiro e a transcrição; o corte cai no ponto mais silencioso entre blocos.
- engine=edge: 1 pedido por bloco (edge-tts, grátis), sem corte.
Saída: out_loc/<engine>_<voz>/bloco-NN.wav + out_loc/report.json. Env: SCRIPT (json), ENGINE, VOICES, MODEL, GEMINI_KEY, RATE (edge), PITCH (edge)."""
import difflib, json, os, re, subprocess, sys, unicodedata
import numpy as np, soundfile as sf

sys.path.insert(0, "scripts")
import ltts

SR = 48000
PAD = 0.3
S = json.load(open(os.environ.get("SCRIPT", "voicetest/cronos_locucao.json")))
BLOCOS = S["blocos"]
PRON = S.get("pron", {})
OUT = "out_loc"
os.makedirs(OUT, exist_ok=True)
rep = {"script": os.environ.get("SCRIPT", "voicetest/cronos_locucao.json"), "vozes": {}}


def respell(t):
    for k, v in PRON.items():
        t = re.sub(rf"\b{k}\b", v, t)
    return t


def norm(w):
    w = unicodedata.normalize("NFKD", w.lower())
    w = "".join(c for c in w if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", w)


def to48(x, sr):
    if sr != SR:
        import librosa
        x = librosa.resample(np.asarray(x, dtype=np.float32), orig_sr=sr, target_sr=SR)
    return np.asarray(x, dtype=np.float32)


def trim(x, thr_db=-45.0, margin=0.06):
    """corta silêncio nas pontas (abaixo de thr_db), deixando 'margin' s."""
    win = int(0.02 * SR)
    n = len(x) // win
    if n < 2:
        return x
    rms = np.sqrt((x[: n * win].reshape(n, win) ** 2).mean(axis=1) + 1e-12)
    db = 20 * np.log10(rms + 1e-9)
    loud = np.where(db > thr_db)[0]
    if len(loud) == 0:
        return x
    a = max(0, int(loud[0] * win - margin * SR)); b = min(len(x), int((loud[-1] + 1) * win + margin * SR))
    return x[a:b]


def pad(x):
    z = np.zeros(int(PAD * SR), dtype=np.float32)
    return np.concatenate([z, x, z])


def normalize(x, peak_db=-1.0):
    p = float(np.max(np.abs(x)) + 1e-9)
    return x * min(10 ** (peak_db / 20) / p, 4.0)


def quietest(x, t0, t1):
    """instante mais silencioso entre t0 e t1 (janela de 80 ms)."""
    a, b = int(t0 * SR), int(t1 * SR)
    if b - a < int(0.1 * SR):
        return (t0 + t1) / 2
    seg = x[a:b]
    win = int(0.08 * SR)
    n = max(1, len(seg) // win)
    rms = np.sqrt((seg[: n * win].reshape(n, win) ** 2).mean(axis=1) + 1e-12)
    i = int(np.argmin(rms))
    return (a + i * win + win / 2) / SR


def words_pt(x):
    from faster_whisper import WhisperModel
    import librosa
    if not hasattr(words_pt, "m"):
        words_pt.m = WhisperModel(os.environ.get("WHISPER", "small"), compute_type="int8")
    x16 = librosa.resample(x, orig_sr=SR, target_sr=16000)
    segs, _ = words_pt.m.transcribe(x16, language="pt", word_timestamps=True, vad_filter=False, beam_size=5)
    out = []
    for s in segs:
        for w in s.words or []:
            out.append((norm(w.word), float(w.start), float(w.end)))
    return [w for w in out if w[0]]


def split_blocks(x, blocos):
    """devolve lista de (t_ini, t_fim) por bloco, cortando no silêncio entre blocos."""
    ref, owner = [], []
    for bi, b in enumerate(blocos):
        for w in respell(b).split():
            if norm(w):
                ref.append(norm(w)); owner.append(bi)
    hyp = words_pt(x)
    sm = difflib.SequenceMatcher(None, ref, [h[0] for h in hyp], autojunk=False)
    ref2hyp = {}
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            ref2hyp[a + k] = b + k
    matched = sum(1 for i in range(len(ref)) if i in ref2hyp)
    starts, ends = {}, {}
    for i, bi in enumerate(owner):
        if i in ref2hyp:
            t0, t1 = hyp[ref2hyp[i]][1], hyp[ref2hyp[i]][2]
            starts.setdefault(bi, t0); ends[bi] = t1
    nb = len(blocos)
    dur = len(x) / SR
    # blocos sem palavra casada: interpola entre vizinhos
    for bi in range(nb):
        if bi not in starts:
            prev_end = ends.get(bi - 1, 0.0); nxt = next((starts[j] for j in range(bi + 1, nb) if j in starts), dur)
            starts[bi] = prev_end + 0.3; ends[bi] = nxt - 0.3
    cuts = [0.0]
    for bi in range(1, nb):
        cuts.append(quietest(x, ends[bi - 1], starts[bi]) if starts[bi] > ends[bi - 1] else (ends[bi - 1] + starts[bi]) / 2)
    cuts.append(dur)
    return [(cuts[i], cuts[i + 1]) for i in range(nb)], matched / len(ref), hyp


def save_blocks(tag, pieces, extra):
    d = f"{OUT}/{tag}"; os.makedirs(d, exist_ok=True)
    durs = []
    for i, x in enumerate(pieces, 1):
        y = pad(normalize(trim(x)))
        sf.write(f"{d}/bloco-{i:02d}.wav", y, SR, subtype="PCM_16")
        durs.append(round(len(y) / SR, 2))
    rep["vozes"][tag] = {"blocos_s": durs, "total_s": round(sum(durs), 1), **extra}
    print(tag, "total", round(sum(durs), 1), "s", durs, extra)


engine = os.environ.get("ENGINE", "gemini")
voices = [v for v in os.environ.get("VOICES", "Charon,Orus,Algieba").split(",") if v]
model = os.environ.get("MODEL", "gemini-3.1-flash-tts-preview")

if engine in ("gemini", "both"):
    text = "\n\n".join(respell(b) for b in BLOCOS)
    for v in voices:
        try:
            x = ltts.gemini_once(text, v, S["style"], model)
            x = to48(x, ltts.SR)
            sf.write(f"{OUT}/{v}_inteiro.wav", x, SR, subtype="PCM_16")
            spans, cov, hyp = split_blocks(x, BLOCOS)
            pieces = [x[int(a * SR):int(b * SR)] for a, b in spans]
            save_blocks(f"gemini_{v}", pieces, {"ferramenta": f"Gemini TTS ({model}), voz {v}", "cobertura_alinhamento": round(cov, 3),
                                                  "inteiro_s": round(len(x) / SR, 1), "transcricao": " ".join(h[0] for h in hyp)[:600]})
        except Exception as e:
            rep["vozes"][f"gemini_{v}"] = {"erro": repr(e)[:400]}; print(v, "erro", repr(e)[:400])

if engine in ("edge", "both"):
    import asyncio, edge_tts, io
    rate = os.environ.get("RATE", "-6%"); pitch = os.environ.get("PITCH", "-2Hz")
    evoices = [v for v in os.environ.get("EDGE_VOICES", "pt-BR-AntonioNeural").split(",") if v]

    async def one(voice, t, path):
        await edge_tts.Communicate(t, voice, rate=rate, pitch=pitch).save(path)

    for v in evoices:
        pieces = []
        try:
            for i, b in enumerate(BLOCOS, 1):
                p = f"/tmp/edge_{v}_{i}.mp3"
                asyncio.run(one(v, respell(b), p))
                pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
                pieces.append(np.frombuffer(pcm, dtype="<i2").astype(np.float32) / 32768)
            save_blocks(f"edge_{v}", pieces, {"ferramenta": f"edge-tts (Microsoft), voz {v}, rate {rate}, pitch {pitch}"})
        except Exception as e:
            rep["vozes"][f"edge_{v}"] = {"erro": repr(e)[:400]}; print(v, "erro", repr(e)[:400])

json.dump(rep, open(f"{OUT}/report.json", "w"), indent=1, ensure_ascii=False, default=float)
print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "transcricao"} for k, v in rep["vozes"].items()}, ensure_ascii=False, indent=1))

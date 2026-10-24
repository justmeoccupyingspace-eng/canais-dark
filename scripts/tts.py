"""spec.json -> spec com áudio por cena + tempo de cada palavra (legenda). Uso: python scripts/tts.py specs/x.json public/build/x.json"""
import json, os, re, sys
import numpy as np
from scipy.signal import butter, sosfilt
import soundfile as sf
from kokoro_onnx import Kokoro

VOICES = {
    "chartbound": ("af_heart", "en-us", 1.0),
    "howitticks": ("am_michael", "en-us", 1.0),
    "valeopreco": ("pf_dora", "pt-br", 1.0),
    "loja": ("pf_dora", "pt-br", 1.0),
    "lojam": ("pm_alex", "pt-br", 1.0),
    "gabarito": ("pf_dora", "pt-br", 1.0),
}
EDGE = {"gabarito": "pt-BR-FranciscaNeural", "loja": "pt-BR-FranciscaNeural", "lojam": "pt-BR-AntonioNeural", "valeopreco": "pt-BR-FranciscaNeural", "howitticks": "en-US-AndrewMultilingualNeural", "chartbound": "en-US-AvaMultilingualNeural"}  # voz neural natural; se a rede falhar, cai no Kokoro
GOOGLE = {"valeopreco": ("pt-BR", "pt-BR-Chirp3-HD-Charon"), "loja": ("pt-BR", "pt-BR-Chirp3-HD-Leda"), "lojam": ("pt-BR", "pt-BR-Chirp3-HD-Charon")}  # exige GCP_TTS_KEY; sem a chave, cai no edge/Kokoro
EDGE_RATE = os.environ.get("EDGE_RATE", "+0%")
MODEL = os.environ.get("KOKORO_DIR", ".cache/kokoro")
TAIL = float(os.environ.get("TTS_TAIL", "0.28"))  # silêncio após a fala antes da próxima cena


def trim(samples, sr, thr=0.002):
    """Corta silêncio nas pontas sem comer consoantes fracas (s, t, f)."""
    idx = np.where(np.abs(samples) > thr)[0]
    if len(idx) == 0:
        return samples
    a = max(idx[0] - int(0.06 * sr), 0)
    b = min(idx[-1] + int(0.16 * sr), len(samples))
    return samples[a:b]


def word_times(text, total, offset=0.0, audio=None, sr=24000):
    """Tempo de cada palavra: peso por tamanho (números pesam mais) e, quando há áudio,
    cada fronteira é encaixada no ponto de menor energia próximo (±90 ms)."""
    words = text.split()
    wt = []
    for w in words:
        core = re.sub(r"\W", "", w)
        base = len(core) * 2.2 + 3 if re.search(r"\d", core) else len(core) + 2
        wt.append(base + (4 if re.search(r"[,;:]$", w) else 0))
    S = sum(wt)
    bounds, t = [0.0], 0.0
    for x in wt:
        t += total * x / S
        bounds.append(t)
    bounds[-1] = total
    if audio is not None and len(audio) > sr * 0.2:
        n = int(0.02 * sr)
        env = np.sqrt(np.convolve(audio ** 2, np.ones(n) / n, "same"))
        win = int(0.09 * sr)
        for i in range(1, len(bounds) - 1):
            c = int(bounds[i] * sr)
            lo, hi = max(c - win, 0), min(c + win, len(env) - 1)
            snapped = (lo + int(np.argmin(env[lo:hi]))) / sr
            bounds[i] = min(max(snapped, bounds[i - 1] + 0.05), total - 0.05 * (len(bounds) - 1 - i))
    LEAD = 0.05  # legenda ligeiramente à frente da voz
    return [{"w": w, "t0": round(max(offset + bounds[i] - LEAD, 0), 3), "t1": round(offset + bounds[i + 1] - LEAD, 3)} for i, w in enumerate(words)]


def google_sentence(text, cfg):
    """Uma frase via Google Cloud TTS (Chirp 3 HD). Retorna samples 24k mono."""
    import base64, urllib.request
    key = os.environ["GCP_TTS_KEY"]
    body = json.dumps({"input": {"text": text}, "voice": {"languageCode": cfg[0], "name": cfg[1]},
                       "audioConfig": {"audioEncoding": "LINEAR16", "sampleRateHertz": 24000}}).encode()
    req = urllib.request.Request(f"https://texttospeech.googleapis.com/v1/text:synthesize?key={key}", data=body, headers={"Content-Type": "application/json"})
    raw = base64.b64decode(json.load(urllib.request.urlopen(req, timeout=60))["audioContent"])
    import io
    x, _ = sf.read(io.BytesIO(raw), dtype="float32")
    return x if x.ndim == 1 else x[:, 0]


def edge_sentence(text, voice):
    """Uma frase via edge-tts. Retorna (samples 24k, [(palavra, t0, t1)]) com tempos reais de palavra."""
    import asyncio, subprocess, tempfile, edge_tts
    sb = []
    async def go(bd="WordBoundary"):
        com = edge_tts.Communicate(text, voice, rate=EDGE_RATE, boundary=bd)
        mp3, wb = b"", []
        sb.clear()
        async for ch in com.stream():
            if ch["type"] == "audio":
                mp3 += ch["data"]
            elif ch["type"] == "SentenceBoundary":
                sb.append((ch["text"], ch["offset"] / 1e7, (ch["offset"] + ch["duration"]) / 1e7))
            elif ch["type"] == "WordBoundary":
                wb.append((ch["text"], ch["offset"] / 1e7, (ch["offset"] + ch["duration"]) / 1e7))
        return mp3, wb
    mp3, wb = asyncio.run(go())
    if not wb:
        mp3, wb = asyncio.run(go("SentenceBoundary"))
        print("edge sem WordBoundary; frases:", len(sb))
    with tempfile.TemporaryDirectory() as d:
        open(f"{d}/a.mp3", "wb").write(mp3)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{d}/a.mp3", "-ac", "1", "-ar", "24000", f"{d}/a.wav"], check=True)
        x, _ = sf.read(f"{d}/a.wav", dtype="float32")
    edge_sentence.last_sb = list(sb)
    return x, wb


def speak(k, text, voice, lang, speed, edge_voice=None, google_cfg=None):
    """Frase a frase, com pausas naturais; limpa graves, nivela volume. Retorna (samples, sr, words)."""
    if google_cfg and os.environ.get("TTS_WHOLE", "1") == "1":
        try:  # cena inteira numa requisição: entonação contínua, sem emendas
            sr = 24000
            smp = trim(google_sentence(text.strip(), google_cfg), sr)
            words = word_times(text.strip(), len(smp) / sr, 0.0, smp, sr)
            x = sosfilt(butter(2, 70 / (sr / 2), btype="high", output="sos"), smp)
            x = x * (0.11 / (np.sqrt(np.mean(x ** 2)) + 1e-9))
            x = (np.tanh(x * 1.2) / np.tanh(1.2) * 0.95).astype(np.float32)
            return x, sr, words
        except Exception as e:
            print("google inteiro falhou, indo frase a frase:", repr(e)[:160])
    if edge_voice and not google_cfg:
        try:
            smp, wb = edge_sentence(text.strip(), edge_voice)
            sr = 24000
            a0 = max(int(np.where(np.abs(smp) > 0.002)[0][0]) - int(0.06 * sr), 0)
            smp = trim(smp, sr)
            d = len(smp) / sr
            if wb and len(wb) == len(text.split()):
                words = [{"w": w, "t0": round(max(t0 - a0 / sr - 0.05, 0), 3), "t1": round(t1 - a0 / sr - 0.05, 3)} for w, t0, t1 in wb]
            else:
                sbs = getattr(edge_sentence, "last_sb", [])
                raw = smp
                words = []
                if sbs:
                    for stext, t0, t1 in sbs:
                        i0, i1 = int(t0 * sr), min(int(t1 * sr), len(raw))
                        words += word_times(stext.strip(), t1 - t0, t0 - a0 / sr, raw[i0:i1], sr)
                if not sbs or sum(len(stext.split()) for stext, _, _ in sbs) != len(text.split()):
                    words = word_times(text.strip(), d, 0.0, smp, sr)
            x = sosfilt(butter(2, 70 / (sr / 2), btype="high", output="sos"), smp)
            x = x * (0.11 / (np.sqrt(np.mean(x ** 2)) + 1e-9))
            x = (np.tanh(x * 1.2) / np.tanh(1.2) * 0.95).astype(np.float32)
            return x, sr, words
        except Exception as e:
            print("edge contínuo falhou, usando frase a frase:", repr(e)[:120])
    sents = [x for x in re.split(r"(?<=[.!?])\s+", text.strip()) if x]
    chunks, words, pos, sr = [], [], 0.0, 24000
    for i, snt in enumerate(sents):
        wb = None
        if google_cfg:
            try:
                smp = google_sentence(snt, google_cfg)
                sr = 24000
                smp = trim(smp, sr)
            except Exception as e:
                print("google falhou, tentando edge:", repr(e)[:160])
                google_cfg = None
        if google_cfg:
            pass
        elif edge_voice:
            try:
                smp, wb = edge_sentence(snt, edge_voice)
                sr = 24000
                a0 = max(int(np.where(np.abs(smp) > 0.002)[0][0]) - int(0.06 * sr), 0)
                smp = trim(smp, sr)
                if wb and len(wb) != len(snt.split()):
                    wb = None
            except Exception as e:
                print("edge falhou, usando kokoro:", repr(e)[:120])
                edge_voice = None
                wb = None
        if not edge_voice and not google_cfg:
            smp, sr = k.create(snt, voice=voice, speed=speed, lang=lang, trim=False)
            smp = trim(smp, sr)
        d = len(smp) / sr
        if wb:
            words += [{"w": w, "t0": round(max(pos + t0 - a0 / sr - 0.05, 0), 3), "t1": round(pos + t1 - a0 / sr - 0.05, 3)} for w, t0, t1 in wb]
        else:
            words += word_times(snt, d, pos, smp, sr)
        chunks.append(smp)
        pos += d
        if i < len(sents) - 1:
            gap = 0.34 if snt.endswith("?") else 0.24 if snt.endswith(".") else 0.14
            chunks.append(np.zeros(int(gap * sr), dtype=smp.dtype))
            pos += gap
    x = np.concatenate(chunks)
    x = sosfilt(butter(2, 70 / (sr / 2), btype="high", output="sos"), x)
    rms = np.sqrt(np.mean(x ** 2)) + 1e-9
    x = x * (0.11 / rms)  # nivela (~ -19 dBFS RMS)
    x = np.tanh(x * 1.2) / np.tanh(1.2) * 0.95  # limitador suave
    x = x.astype(np.float32)
    return x, sr, words


def envelope(x, sr, fps=30):
    """Volume da voz por quadro (0..1) para a boca do personagem."""
    n = int(sr / fps)
    m = len(x) // n
    e = np.sqrt(np.mean(x[: m * n].reshape(m, n) ** 2, axis=1))
    e = e / (np.percentile(e, 95) + 1e-9)
    # suaviza
    e = np.convolve(e, np.array([0.25, 0.5, 0.25]), mode="same")
    return [round(float(v), 3) for v in np.clip(e, 0, 1)]


def main(src, dst):
    global EDGE_RATE
    spec = json.load(open(src, encoding="utf-8"))
    EDGE_RATE = spec.get("rate", EDGE_RATE)
    voice, lang, speed = VOICES[spec["channel"]]
    k = Kokoro(f"{MODEL}/kokoro-v1.0.onnx", f"{MODEL}/voices-v1.0.bin")
    name = os.path.splitext(os.path.basename(src))[0]
    outdir = f"public/audio/{name}"
    os.makedirs(outdir, exist_ok=True)
    for i, sc in enumerate(spec["scenes"]):
        text = sc.get("narration")
        if not text:
            continue
        samples, sr, words = speak(k, text, voice, lang, speed, EDGE.get(spec["channel"]), GOOGLE.get(spec["channel"]) if os.environ.get("GCP_TTS_KEY") else None)
        dur = len(samples) / sr
        rel = f"audio/{name}/s{i}.wav"
        sf.write(f"public/{rel}", samples, sr)
        sc["audio"] = rel
        sc["words"] = words
        sc["env"] = envelope(samples, sr)
        sc["duration"] = round(max(sc.get("min_duration", 0), dur + spec.get("tail", TAIL) + sc.get("extra", 0)), 2)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    json.dump(spec, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("tts ok", dst, round(sum(s.get("duration", 0) for s in spec["scenes"]), 1), "s")


if __name__ == "__main__":
    main(*sys.argv[1:3])

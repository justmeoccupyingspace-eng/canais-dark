"""spec.json -> spec com áudio por cena + tempo de cada palavra (legenda). Uso: python scripts/tts.py specs/x.json public/build/x.json"""
import json, os, re, sys
import numpy as np
from scipy.signal import butter, sosfilt
import soundfile as sf
from kokoro_onnx import Kokoro

VOICES = {
    "chartbound": ("af_heart", "en-us", 1.04),
    "howitticks": ("am_michael", "en-us", 1.04),
    "valeopreco": ("pf_dora", "pt-br", 1.04),
}
MODEL = os.environ.get("KOKORO_DIR", ".cache/kokoro")
TAIL = 0.28  # silêncio após a fala antes da próxima cena


def trim(samples, sr, thr=0.01):
    idx = np.where(np.abs(samples) > thr)[0]
    if len(idx) == 0:
        return samples
    a = max(idx[0] - int(0.03 * sr), 0)
    b = min(idx[-1] + int(0.08 * sr), len(samples))
    return samples[a:b]


def word_times(text, total, offset=0.0):
    """Distribui o tempo entre as palavras por nº de letras (+ pausa em pontuação)."""
    words = text.split()
    wt = []
    for w in words:
        wt.append(len(re.sub(r"\W", "", w)) + 2 + (4 if re.search(r"[,;:]$", w) else 0) + (7 if re.search(r"[.!?]$", w) else 0))
    s = sum(wt)
    out, t = [], 0.0
    for w, x in zip(words, wt):
        d = total * x / s
        out.append({"w": w, "t0": round(offset + t, 3), "t1": round(offset + t + d, 3)})
        t += d
    return out


def speak(k, text, voice, lang, speed):
    """Frase a frase, com pausas naturais; limpa graves, nivela volume. Retorna (samples, sr, words)."""
    sents = [x for x in re.split(r"(?<=[.!?])\s+", text.strip()) if x]
    chunks, words, pos, sr = [], [], 0.0, 24000
    for i, snt in enumerate(sents):
        smp, sr = k.create(snt, voice=voice, speed=speed, lang=lang)
        smp = trim(smp, sr)
        d = len(smp) / sr
        words += word_times(snt, d, pos)
        chunks.append(smp)
        pos += d
        if i < len(sents) - 1:
            gap = 0.30 if snt.endswith("?") else 0.20 if snt.endswith(".") else 0.12
            chunks.append(np.zeros(int(gap * sr), dtype=smp.dtype))
            pos += gap
    x = np.concatenate(chunks)
    x = sosfilt(butter(2, 70 / (sr / 2), btype="high", output="sos"), x)
    rms = np.sqrt(np.mean(x ** 2)) + 1e-9
    x = x * (0.11 / rms)  # nivela (~ -19 dBFS RMS)
    x = np.tanh(x * 1.2) / np.tanh(1.2) * 0.95  # limitador suave
    return x.astype(np.float32), sr, words


def main(src, dst):
    spec = json.load(open(src, encoding="utf-8"))
    voice, lang, speed = VOICES[spec["channel"]]
    k = Kokoro(f"{MODEL}/kokoro-v1.0.onnx", f"{MODEL}/voices-v1.0.bin")
    name = os.path.splitext(os.path.basename(src))[0]
    outdir = f"public/audio/{name}"
    os.makedirs(outdir, exist_ok=True)
    for i, sc in enumerate(spec["scenes"]):
        text = sc.get("narration")
        if not text:
            continue
        samples, sr, words = speak(k, text, voice, lang, speed)
        dur = len(samples) / sr
        rel = f"audio/{name}/s{i}.wav"
        sf.write(f"public/{rel}", samples, sr)
        sc["audio"] = rel
        sc["words"] = words
        sc["duration"] = round(max(sc.get("min_duration", 0), dur + TAIL), 2)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    json.dump(spec, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("tts ok", dst, round(sum(s.get("duration", 0) for s in spec["scenes"]), 1), "s")


if __name__ == "__main__":
    main(*sys.argv[1:3])

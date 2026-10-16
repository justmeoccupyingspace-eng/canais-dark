"""spec.json -> spec com áudio por cena + tempo de cada palavra (legenda). Uso: python scripts/tts.py specs/x.json public/build/x.json"""
import json, os, re, sys
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

VOICES = {
    "chartbound": ("af_heart", "en-us", 1.12),
    "howitticks": ("am_michael", "en-us", 1.12),
    "valeopreco": ("pf_dora", "pt-br", 1.12),
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


def word_times(text, total):
    """Distribui o tempo entre as palavras por nº de letras (+ pausa em pontuação)."""
    words = text.split()
    wt = []
    for w in words:
        wt.append(len(re.sub(r"\W", "", w)) + 2 + (4 if re.search(r"[,;:]$", w) else 0) + (7 if re.search(r"[.!?]$", w) else 0))
    s = sum(wt)
    out, t = [], 0.0
    for w, x in zip(words, wt):
        d = total * x / s
        out.append({"w": w, "t0": round(t, 3), "t1": round(t + d, 3)})
        t += d
    return out


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
        samples, sr = k.create(text, voice=voice, speed=speed, lang=lang)
        samples = trim(samples, sr)
        dur = len(samples) / sr
        rel = f"audio/{name}/s{i}.wav"
        sf.write(f"public/{rel}", samples, sr)
        sc["audio"] = rel
        sc["words"] = word_times(text, dur)
        sc["duration"] = round(max(sc.get("min_duration", 0), dur + TAIL), 2)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    json.dump(spec, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("tts ok", dst, round(sum(s.get("duration", 0) for s in spec["scenes"]), 1), "s")


if __name__ == "__main__":
    main(*sys.argv[1:3])

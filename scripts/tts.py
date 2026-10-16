"""spec.json -> spec com áudio por cena. Uso: python scripts/tts.py specs/x.json public/build/x.json"""
import json, os, sys, wave
import soundfile as sf
from kokoro_onnx import Kokoro

VOICES = {
    "chartbound": ("af_heart", "en-us", 1.0),
    "howitticks": ("am_michael", "en-us", 1.0),
    "valeopreco": ("pf_dora", "pt-br", 1.05),
}
MODEL = os.environ.get("KOKORO_DIR", ".cache/kokoro")

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
        rel = f"audio/{name}/s{i}.wav"
        sf.write(f"public/{rel}", samples, sr)
        sc["audio"] = rel
        sc["duration"] = round(max(sc.get("duration", 0), len(samples) / sr + 0.7), 2)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    json.dump(spec, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("tts ok", dst, sum(s.get("duration", 0) for s in spec["scenes"]), "s")

if __name__ == "__main__":
    main(*sys.argv[1:3])

"""Avalia a fala dos vídeos prontos: idioma por janela (Whisper automático), erro de palavras vs roteiro,
ritmo, variação de entonação e pausas longas. Uso: python voicetest/evalvid.py <branch>... (mp4 nas branches pv-*)."""
import json, os, re, subprocess, sys
import numpy as np, librosa
from faster_whisper import WhisperModel
m = WhisperModel("small", compute_type="int8")
out = []


def norm(s):
    s = s.lower().replace("r$", "")
    return [w for w in re.sub(r"[^\wà-ú ]", " ", s).split() if w]


def wer(r, h):
    r, h = norm(r), norm(h)
    d = np.zeros((len(r) + 1, len(h) + 1), int)
    d[:, 0], d[0, :] = range(len(r) + 1), range(len(h) + 1)
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            d[i, j] = min(d[i - 1, j] + 1, d[i, j - 1] + 1, d[i - 1, j - 1] + (r[i - 1] != h[j - 1]))
    return d[-1, -1] / max(len(r), 1)


for br in sys.argv[1:]:
    subprocess.run(["git", "fetch", "-q", "origin", br], check=True)
    for f in subprocess.run(["git", "ls-tree", "--name-only", "FETCH_HEAD"], capture_output=True, text=True).stdout.split():
        if not f.endswith(".mp4"):
            continue
        open(f"/tmp/{f}", "wb").write(subprocess.run(["git", "show", f"FETCH_HEAD:{f}"], capture_output=True).stdout)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"/tmp/{f}", "-ac", "1", "-ar", "16000", f"/tmp/{f}.wav"])
        y, sr = librosa.load(f"/tmp/{f}.wav", sr=16000)
        spec = json.load(open(f"specs/loja/{f[:-4]}.json"))
        ref = " ".join(s.get("narration", "") for s in spec["scenes"])
        segs, info = m.transcribe(y, language="pt", word_timestamps=True)
        segs = list(segs)
        hyp = " ".join(s.text for s in segs)
        words = [w for s in segs for w in s.words]
        gaps = [round(b.start - a.end, 2) for a, b in zip(words, words[1:]) if b.start - a.end > 0.55]
        rate = len(words) / max(sum(s.end - s.start for s in segs), 1)
        langs = []
        for t in range(0, int(len(y) / sr) - 4, 6):
            seg = y[t * sr:(t + 6) * sr]
            _, inf = m.transcribe(seg)
            langs.append(f"{t}s:{inf.language}{inf.language_probability:.2f}")
        f0, _, _ = librosa.pyin(y, fmin=70, fmax=400, sr=sr)
        f0 = f0[~np.isnan(f0)]
        st = np.std(12 * np.log2(f0 / np.median(f0))) if len(f0) else 0
        bad = [l for l in langs if not l.split(":")[1].startswith("pt")]
        out.append(f"{f}: WER={wer(ref, hyp):.2f} ritmo={rate:.2f}pal/s entonação={st:.1f}st pausas>0.55s={gaps} idioma_fora_pt={bad or 'nenhum'}")
        out.append(f"   whisper: {hyp[:400]}")
open("relatorio_videos.txt", "w").write("\n".join(out) + "\n")
print("\n".join(out))

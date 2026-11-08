"""QC da locução: transcreve cada bloco (faster-whisper 'medium', pt) e compara com o roteiro. Env: BRANCH (locucao-<run>), SCRIPT."""
import json, os, re, subprocess, unicodedata, difflib
import numpy as np, librosa
from faster_whisper import WhisperModel
S = json.load(open(os.environ.get("SCRIPT", "voicetest/cronos_locucao.json")))
B = S["blocos"]
def norm(s):
    s = unicodedata.normalize("NFKD", s.lower()); s = "".join(c for c in s if not unicodedata.combining(c))
    return [w for w in re.sub(r"[^a-z0-9 ]", " ", s).split() if w]
m = WhisperModel(os.environ.get("WHISPER", "medium"), compute_type="int8")
out = {}
for d in sorted(os.listdir("loc")):
    if not os.path.isdir(f"loc/{d}") or d == "scripts": continue
    out[d] = []
    for i, ref in enumerate(B, 1):
        p = f"loc/{d}/bloco-{i:02d}.wav"
        if not os.path.exists(p): continue
        y, _ = librosa.load(p, sr=16000)
        segs, _ = m.transcribe(y, language="pt", beam_size=5)
        hyp = " ".join(s.text for s in segs).strip()
        r, h = norm(ref), norm(hyp)
        ratio = difflib.SequenceMatcher(None, r, h).ratio()
        out[d].append({"bloco": i, "ok": round(ratio, 2), "ouvido": hyp})
        print(d, i, round(ratio, 2), hyp[:90])
json.dump(out, open("loc/qc.json", "w"), ensure_ascii=False, indent=1)

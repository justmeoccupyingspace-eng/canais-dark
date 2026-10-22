"""Auditoria da voz por código (substitui 'ouvir'): transcreve com Whisper e mede.
Uso: python scripts/audit.py public/build/x.json
Mede por cena: erro de palavras (WER), desvio da legenda vs. fala real, ritmo (palavras/s), monotonia (desvio de pitch em semitons), maior pausa."""
import json, re, sys
import numpy as np, soundfile as sf

def num_to_words(t):
    t = re.sub(r"R\s*\$\s*", "", t)
    def rep(m):
        from num2words import num2words
        v = int(m.group(0).replace(".", "").replace(" ", ""))
        return num2words(v, lang="pt_BR")
    t = re.sub(r"\d[\d. ]*\d|\d", rep, t)
    return t.replace("%", " por cento")

def norm(w): return re.sub(r"[^\wÀ-ÿ]", "", w.lower().replace(".", ""))

def wer(ref, hyp):
    r, h = [norm(w) for w in ref], [norm(w) for w in hyp]
    d = np.zeros((len(r) + 1, len(h) + 1), int)
    d[:, 0], d[0, :] = range(len(r) + 1), range(len(h) + 1)
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            d[i, j] = min(d[i-1, j] + 1, d[i, j-1] + 1, d[i-1, j-1] + (r[i-1] != h[j-1]))
    return d[-1, -1] / max(len(r), 1)

def main(path):
    import librosa
    from faster_whisper import WhisperModel
    spec = json.load(open(path, encoding="utf-8"))
    lang = "pt" if spec["channel"] in ("valeopreco", "loja", "lojam") or spec.get("yt", {}).get("lang", "").startswith("pt") else "en"
    m = WhisperModel("small", compute_type="int8")
    rows = []
    for i, sc in enumerate(spec["scenes"]):
        if "audio" not in sc: continue
        x, sr = sf.read("public/" + sc["audio"], dtype="float32")
        segs, _ = m.transcribe(x if sr == 16000 else librosa.resample(x, orig_sr=sr, target_sr=16000), language=lang, word_timestamps=True)
        hw = [w for s in segs for w in s.words]
        hyp_txt = num_to_words(" ".join(w.word for w in hw)).split() if lang == "pt" else [w.word for w in hw]
        ref = sc["words"]
        e = wer([w["w"] for w in ref], hyp_txt)
        sync = None
        if len(hw) == len(ref):
            sync = float(np.mean([abs(h.start - r["t0"]) for h, r in zip(hw, ref)]))
        dur = (hw[-1].end - hw[0].start) if hw else 1
        rate = len(hw) / dur
        f0, _, _ = librosa.pyin(x, fmin=70, fmax=400, sr=sr, frame_length=1024)
        f = f0[~np.isnan(f0)]
        st = float((12 * np.log2(f / np.median(f))).std()) if len(f) > 20 else 0
        gaps = [b.start - a.end for a, b in zip(hw, hw[1:])]
        if e > 0.1: print("   roteiro:", " ".join(w["w"] for w in ref), "\n   whisper:", " ".join(w.word.strip() for w in hw))
        rows.append((i, e, sync, rate, st, max(gaps) if gaps else 0))
        print(f"cena {i}: WER {e:.2f} | sync {'-' if sync is None else f'{sync*1000:.0f}ms'} | {rate:.2f} pal/s | pitch {st:.1f} st | maior pausa {rows[-1][5]:.2f}s", flush=True)
    if rows:
        wers, rates, sts = [r[1] for r in rows], [r[3] for r in rows], [r[4] for r in rows]
        print(f"RESUMO WER {np.mean(wers):.2f} (ok <0.10) | ritmo {np.mean(rates):.2f} pal/s (ok 2.3-3.3) | pitch {np.mean(sts):.1f} st (monótono <2.0)")

if __name__ == "__main__":
    main(sys.argv[1])

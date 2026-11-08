"""Faixa de áudio dublada (outro idioma) para um longo já publicado, encaixada cena a cena na timeline original.
Roda dentro da cópia do branch lprep-<run> (tem o JSON montado com t0/words por cena, trilhas e efeitos em public/).
1) TTS (Gemini) em blocos de cenas (≤ MAXW palavras por pedido)
2) corta cada bloco nas cenas por alinhamento palavra a palavra (faster-whisper, idioma do roteiro)
3) cada cena começa onde começava a fala original; se não couber até a próxima, acelera (atempo ≤ KMAX); se ainda assim não couber, marca OVERFLOW
4) refaz o envelope da voz (ducking) e mixa trilha + efeitos com scripts/lmix.py; iguala a loudness à mixagem original
Uso: python dub.py <dub.json> <built.json> <outdir>.  Env: GEMINI_KEY, TTS_MODEL, MAXW, KMAX, WHISPER"""
import copy, difflib, json, os, re, subprocess, sys, unicodedata
import numpy as np, soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ltts, lmix

SR, FPS = 48000, 30
MAXW = int(os.environ.get("MAXW", "210"))
KMAX = float(os.environ.get("KMAX", "1.18"))
MODEL = os.environ.get("TTS_MODEL", "gemini-3.8-flash-tts")


def norm(w):
    w = unicodedata.normalize("NFKD", w.lower())
    w = "".join(c for c in w if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", w)


def trim(x, thr_db=-42.0, margin=0.04):
    win = int(0.01 * SR); n = len(x) // win
    if n < 3:
        return x
    db = 20 * np.log10(np.sqrt((x[: n * win].reshape(n, win) ** 2).mean(1) + 1e-12) + 1e-9)
    loud = np.where(db > thr_db)[0]
    if not len(loud):
        return x[:0]
    a = max(0, int(loud[0] * win - margin * SR)); b = min(len(x), int((loud[-1] + 1) * win + margin * SR))
    return x[a:b]


def quietest(x, t0, t1):
    a, b = int(t0 * SR), int(t1 * SR)
    if b - a < int(0.08 * SR):
        return (t0 + t1) / 2
    win = int(0.04 * SR); seg = x[a:b]; n = max(1, len(seg) // win)
    rms = np.sqrt((seg[: n * win].reshape(n, win) ** 2).mean(1) + 1e-12)
    return (a + int(np.argmin(rms)) * win + win / 2) / SR


def words(x, lang):
    from faster_whisper import WhisperModel
    import librosa
    if not hasattr(words, "m"):
        words.m = WhisperModel(os.environ.get("WHISPER", "small"), compute_type="int8")
    segs, _ = words.m.transcribe(librosa.resample(x, orig_sr=SR, target_sr=16000), language=lang, word_timestamps=True, beam_size=5)
    return [(norm(w.word), float(w.start), float(w.end)) for s in segs for w in (s.words or []) if norm(w.word)]


def split(x, texts, lang):
    ref, owner = [], []
    for i, t in enumerate(texts):
        for w in t.split():
            if norm(w):
                ref.append(norm(w)); owner.append(i)
    hyp = words(x, lang)
    sm = difflib.SequenceMatcher(None, ref, [h[0] for h in hyp], autojunk=False)
    r2h = {}
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            r2h[a + k] = b + k
    st, en = {}, {}
    for i, o in enumerate(owner):
        if i in r2h:
            h = hyp[r2h[i]]; st.setdefault(o, h[1]); en[o] = h[2]
    nb, dur = len(texts), len(x) / SR
    for o in range(nb):
        if o not in st:
            pe = en.get(o - 1, 0.0); nx = next((st[j] for j in range(o + 1, nb) if j in st), dur)
            st[o], en[o] = pe + 0.2, nx - 0.2
    cuts = [0.0] + [quietest(x, en[o - 1], st[o]) if st[o] > en[o - 1] else (en[o - 1] + st[o]) / 2 for o in range(1, nb)] + [dur]
    return [x[int(cuts[i] * SR): int(cuts[i + 1] * SR)] for i in range(nb)], len(r2h) / max(1, len(ref)), " ".join(h[0] for h in hyp)


def main(dub_path, built_path, out):
    os.makedirs(out, exist_ok=True)
    D = json.load(open(dub_path)); B = json.load(open(built_path))
    lang = D.get("lang", "pl"); shots = B["shots"]; total = B["total"]
    pl = D["shots"]
    ids = [s["id"] for s in shots]
    missing = [i for i in ids if i not in pl]
    if missing:
        sys.exit(f"faltam traduções: {missing}")
    # blocos ≤ MAXW palavras (podem atravessar atos: a dublagem é posicionada cena a cena)
    groups, cur, cw = [], [], 0
    for s in shots:
        n = len(pl[s["id"]].split())
        if cur and cw + n > MAXW:
            groups.append(cur); cur, cw = [], 0
        cur.append(s); cw += n
    if cur:
        groups.append(cur)
    print(f"{len(groups)} pedidos de TTS ({MODEL}), {sum(len(pl[i].split()) for i in ids)} palavras")
    seg = {}
    rep = {"model": MODEL, "voice": D["voice"], "groups": [], "shots": []}
    for gi, g in enumerate(groups):
        texts = [pl[s["id"]] for s in g]
        x = None
        for attempt in range(2):
            try:
                x = ltts.gemini_once("\n\n".join(texts), D["voice"], D["style"], MODEL); break
            except Exception as e:
                print(f"::warning title=tts::grupo {gi} tentativa {attempt}: {repr(e)[:300]}")
        if x is None:
            sys.exit(f"TTS falhou no grupo {gi}")
        x = ltts.clean(x)
        sf.write(f"{out}/g{gi:02d}.wav", x, SR)
        parts, cov, heard = split(x, texts, lang)
        rep["groups"].append({"g": gi, "shots": [s["id"] for s in g], "cobertura": round(cov, 3), "s": round(len(x) / SR, 1), "ouvido": heard[:900]})
        print(f"grupo {gi}: {[s['id'] for s in g]} {len(x)/SR:.1f}s cobertura {cov:.2f}")
        for s, p in zip(g, parts):
            seg[s["id"]] = trim(p)
    # posiciona
    N = int(np.ceil(total * SR)) + SR
    voice = np.zeros(N, np.float32)
    for i, s in enumerate(shots):
        w = s.get("words") or []
        t_start = w[0]["t0"] if w else s["t0"] + 0.2
        if i + 1 < len(shots):
            nw = shots[i + 1].get("words") or []
            t_next = nw[0]["t0"] if nw else shots[i + 1]["t0"]
            avail = t_next - t_start - 0.18
        else:
            avail = total - t_start - 0.4
        x = seg[s["id"]]
        need = len(x) / SR
        k = 1.0
        if need > avail:
            k = need / avail
            x = ltts.tempo(x, min(k, KMAX))
        got = len(x) / SR
        over = got > avail + 0.05
        a = int(t_start * SR)
        voice[a:a + len(x)] += x[: max(0, N - a)]
        rep["shots"].append({"id": s["id"], "pl_s": round(need, 2), "janela_s": round(avail, 2), "fator": round(k, 3), "OVERFLOW": round(got - avail, 2) if over else 0})
        flag = "  <<< OVERFLOW" if over else ""
        print(f"{s['id']} pl {need:5.2f}s janela {avail:5.2f}s fator {k:4.2f}{flag}")
    voice = voice[: int(total * SR)]
    os.makedirs("public/audio/dub", exist_ok=True)
    sf.write("public/audio/dub/voice.wav", voice, SR, subtype="PCM_16")
    sf.write(f"{out}/voz_{lang}.wav", voice, SR, subtype="PCM_16")
    # envelope (igual ao ltts)
    nfr = int(np.ceil(total * FPS)) + 1
    n = SR // FPS; m_ = len(voice) // n
    e = np.zeros(nfr); ee = np.sqrt(np.mean(voice[: m_ * n].reshape(m_, n) ** 2, axis=1)); e[:m_] = ee[:nfr]
    e = e / (np.percentile(e[e > 0], 95) + 1e-9)
    e = np.clip(np.convolve(e, [0.25, 0.5, 0.25], "same"), 0, 1)
    P = copy.deepcopy(B); P["tracks"] = [{"act": 0, "file": "audio/dub/voice.wav", "t": 0.0, "dur": total}]; P["env"] = [round(float(v), 4) for v in e]
    json.dump(P, open("dub_built.json", "w"))
    lmix.main(built_path, f"{out}/mix_en.wav")
    lmix.main("dub_built.json", f"{out}/mix_{lang}_raw.wav")

    def lufs(p):
        r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", p, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
        m = re.findall(r"I:\s+(-?\d+\.\d+) LUFS", r)
        return float(m[-1]) if m else None
    le, lp = lufs(f"{out}/mix_en.wav"), lufs(f"{out}/mix_{lang}_raw.wav")
    g = 10 ** (((le or -16) - (lp or -16)) / 20)
    y, _ = sf.read(f"{out}/mix_{lang}_raw.wav", dtype="float32")
    y = y * g
    pk = float(np.max(np.abs(y)))
    if pk > 0.89:  # ~-1 dBFS
        y = y * (0.89 / pk)
    sf.write(f"{out}/dub_{lang}.wav", y, SR, subtype="PCM_16")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{out}/dub_{lang}.wav", "-c:a", "libmp3lame", "-b:a", "320k", f"{out}/dub_{lang}.mp3"], check=True)
    os.remove(f"{out}/mix_{lang}_raw.wav")
    rep.update({"lufs_en": le, "lufs_dub_antes": lp, "ganho_db": round(20 * np.log10(g), 2), "total_s": round(total, 3),
                "overflow": [r["id"] for r in rep["shots"] if r["OVERFLOW"]], "fator_max": max(r["fator"] for r in rep["shots"])})
    json.dump(rep, open(f"{out}/report.json", "w"), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in rep.items() if k not in ("groups", "shots")}, ensure_ascii=False))
    if rep["overflow"]:
        print(f"::warning title=overflow::cenas que não couberam: {rep['overflow']}")


if __name__ == "__main__":
    main(*sys.argv[1:4])

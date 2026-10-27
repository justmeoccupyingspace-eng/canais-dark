"""Mixagem do vídeo longo direto da timeline (rápido, sem passar pelo navegador):
voz por ato + trilhas com ducking pela voz + efeitos nos cues. Mesmas regras do L1.jsx (Music/Sfx).
Uso: python scripts/lmix.py public/build/x.json out/audio.wav"""
import json, subprocess, sys, tempfile
import numpy as np
import soundfile as sf

SR = 48000
FPS = 30


def load(path):
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-ac", "2", "-ar", str(SR), f"{d}/a.wav"], check=True)
        x, _ = sf.read(f"{d}/a.wav", dtype="float32")
    return x


def add(buf, x, t, gain=1.0):
    i = int(round(t * SR))
    if i < 0:
        x, i = x[-i:], 0
    n = min(len(x), len(buf) - i)
    if n > 0:
        buf[i:i + n] += x[:n] * (gain if np.isscalar(gain) else gain[:n, None])


def events(spec):
    ev = []

    def a(t, f, v):
        if t is not None and t >= 0:
            ev.append((t, f, v))
    shots = spec["shots"]
    for i, s in enumerate(shots):
        if s.get("riser"): a(s["riser"].get("t", -9) - 2.35, "riser", 0.32)
        if s.get("cross"): a(s["cross"].get("t"), "softhit", 0.55)
        if s.get("push"): a(s["push"].get("t"), "softwhoosh", 0.18)
        if s.get("choro"): a(s["choro"].get("t_last"), "sparkle", 0.35)
        for it in s.get("items", []) or []:
            a(it.get("t"), "softhit" if it.get("kind") == "title" else "click", 0.45 if it.get("kind") == "title" else 0.22)
        for l in s.get("labels", []) or []: a(l.get("t"), "tap", 0.14)
        for c in s.get("cues", []) or []: a(c.get("t"), "pop", 0.2)
        for st in s.get("stats", []) or []: a(st.get("t"), "tap", 0.2)
        if s.get("stat"): a(s["stat"].get("t"), "tap", 0.2)
        if s.get("bracket"): a(s["bracket"].get("t"), "softwhoosh", 0.2)
        if i > 0 and s["act"] != shots[i - 1]["act"]: a(s["t0"] - 1.5, "whoosh", 0.28)
    return ev


def main(src, dst):
    spec = json.load(open(src))
    total = spec["total"]
    N = int(np.ceil(total * SR)) + SR
    buf = np.zeros((N, 2), np.float32)
    for tr in spec["tracks"]:
        add(buf, load("public/" + tr["file"]), tr["t"])
    env = np.array(spec.get("env", []), dtype=np.float32)
    # envelope 'máximo em ±6 quadros' como no JSX
    pad = np.pad(env, 6)
    emax = np.max(np.stack([pad[k:k + len(env)] for k in range(13)]), axis=0) if len(env) else env
    for m in spec.get("music", []):
        x = load("public/audio/music/" + m["file"])
        seek = int(m.get("seek", 0) * SR)
        dur = m["end"] - m["t"]
        n = int(dur * SR)
        x = x[seek:seek + n]
        if len(x) < n:  # trilha curta: repete
            reps = int(np.ceil(n / max(len(x), 1)))
            x = np.tile(x, (reps, 1))[:n]
        f0 = m["t"] * FPS
        fr = np.arange(n) / SR * FPS  # quadro local
        g_idx = np.clip((f0 + fr).astype(int), 0, max(len(emax) - 1, 0))
        e = emax[g_idx] if len(emax) else np.zeros(n)
        duck = 1 - 0.55 * np.minimum(1, e * 2.5)
        durf = dur * FPS
        fade = np.clip(np.minimum(np.minimum(1, fr / 30), (durf - fr) / 36), 0, 1)
        add(buf, x, m["t"], (m["vol"] * 2.2 * duck * fade).astype(np.float32))
    cache = {}
    for t, f, v in events(spec):
        if f not in cache:
            cache[f] = load(f"public/audio/fx/{f}.wav")
        add(buf, cache[f], t, v)
    buf = buf[: int(total * SR)]
    peak = np.max(np.abs(buf)) + 1e-9
    if peak > 0.98:
        buf *= 0.98 / peak
    sf.write(dst, buf, SR, subtype="PCM_16")
    print("mix ok", dst, f"{total:.1f}s", "pico", round(float(peak), 3))


if __name__ == "__main__":
    main(*sys.argv[1:3])

"""Gera música de fundo e efeitos sonoros por código (sem direitos autorais).
Uso: python scripts/fx.py  -> public/audio/fx/{music_<canal>.wav, whoosh.wav, tick.wav, pop.wav}"""
import os
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

SR = 44100
OUT = "public/audio/fx"
rng = np.random.default_rng(7)


def save(name, x):
    x = np.clip(x, -1, 1)
    wavfile.write(f"{OUT}/{name}.wav", SR, (x * 32767).astype(np.int16))


def env(n, a=0.01, r=0.2):
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    e[:na] = np.linspace(0, 1, na)
    e[-nr:] = np.linspace(1, 0, nr)
    return e


def whoosh():
    n = int(0.45 * SR)
    noise = rng.standard_normal(n)
    out = np.zeros(n)
    # varredura de passa-banda subindo
    for i in range(0, n, 2048):
        f = 400 + 5000 * (i / n) ** 1.5
        b, a = butter(2, [f / (SR / 2), min((f * 1.8) / (SR / 2), 0.99)], btype="band")
        out[i:i + 2048] = lfilter(b, a, noise[i:i + 2048])
    out *= np.sin(np.linspace(0, np.pi, n)) ** 1.5
    return out / np.max(np.abs(out)) * 0.35


def tick():
    n = int(0.05 * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 90) * 0.4


def pop():
    n = int(0.18 * SR)
    t = np.arange(n) / SR
    f = 500 * np.exp(-t * 14) + 120
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 18) * 0.7


def hit():
    n = int(0.9 * SR)
    t = np.arange(n) / SR
    f = 90 * np.exp(-t * 5) + 38
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4.5)
    nz = rng.standard_normal(n) * np.exp(-t * 28)
    b, a = butter(2, 3000 / (SR / 2), btype="low")
    nz = lfilter(b, a, nz)
    return np.clip(boom * 0.9 + nz * 0.55, -1, 1) * 0.9


def click():
    n = int(0.035 * SR)
    t = np.arange(n) / SR
    nz = rng.standard_normal(n) * np.exp(-t * 260)
    b, a = butter(2, [1800 / (SR / 2), 7000 / (SR / 2)], btype="band")
    return lfilter(b, a, nz) * 0.5 + np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 400) * 0.15


def tap():
    n = int(0.12 * SR)
    t = np.arange(n) / SR
    f = 900 * np.exp(-t * 30) + 300
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 40) * 0.6


def ding():
    n = int(0.9 * SR)
    t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * t) * a for f, a in [(1318.5, .5), (2637, .18), (1975.5, .12)]) * np.exp(-t * 5)
    x2 = np.zeros(n)
    d = int(0.09 * SR)
    x2[d:] = (sum(np.sin(2 * np.pi * f * t[:n - d]) * a for f, a in [(1760, .45), (3520, .12)]) * np.exp(-t[:n - d] * 5))
    return (x + x2) * 0.55


def cash():
    n = int(1.1 * SR)
    t = np.arange(n) / SR
    bell = sum(np.sin(2 * np.pi * f * t) * a for f, a in [(2093, .35), (2637, .25), (3136, .2), (4186, .1)]) * np.exp(-t * 4)
    nz = rng.standard_normal(n) * np.exp(-t * 35) * 0.25
    b, a = butter(2, [3000 / (SR / 2), 9000 / (SR / 2)], btype="band")
    chk = np.zeros(n)
    k = int(0.06 * SR)
    chk[:k] = lfilter(b, a, rng.standard_normal(k)) * np.exp(-np.arange(k) / SR * 60) * 0.8
    out = np.zeros(n)
    off = int(0.07 * SR)
    out[off:] = bell[:n - off]
    return (out + lfilter(b, a, nz) + chk) * 0.6


def sparkle():
    n = int(1.4 * SR)
    t = np.arange(n) / SR
    out = np.zeros(n)
    for i, f in enumerate([1568, 1976, 2349, 2637, 3136, 3951]):
        s = int(i * 0.07 * SR)
        tt = t[:n - s]
        out[s:] += np.sin(2 * np.pi * f * tt) * np.exp(-tt * 6) * 0.22
    return out


def riser(sec=2.4):
    """sobe ruído filtrado + tom em glissando; termina seco no ponto da revelação."""
    n = int(sec * SR)
    t = np.arange(n) / SR
    k = t / sec
    noise = rng.standard_normal(n)
    out = np.zeros(n)
    for i in range(0, n, 1024):
        f = 300 + 6000 * k[i] ** 2
        b, a = butter(2, [f / (SR / 2), min(f * 1.6 / (SR / 2), 0.99)], btype="band")
        out[i:i + 1024] = lfilter(b, a, noise[i:i + 1024])
    out = out / (np.max(np.abs(out)) + 1e-9) * 0.5
    tone = sum(np.sin(2 * np.pi * np.cumsum(f0 * 2 ** (2.2 * k)) / SR) * a for f0, a in [(110, 0.35), (220, 0.18), (330, 0.08)])
    x = (out + tone) * k ** 2.2
    x[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR))
    return x / np.max(np.abs(x)) * 0.6


def softhit():
    x = hit()
    b, a = butter(2, 1800 / (SR / 2), btype="low")
    return lfilter(b, a, x) * 0.8


def softwhoosh():
    x = whoosh()
    b, a = butter(2, 2500 / (SR / 2), btype="low")
    return lfilter(b, a, x) * 0.8


def music(root, mode, bpm, seconds=60):
    """Pad suave + baixo pulsante + hi-hat leve. Loopável."""
    beat = 60 / bpm
    n = int(seconds * SR)
    t = np.arange(n) / SR
    chords = [(0, 4, 7), (-4, 0, 3), (-7, -3, 0), (-2, 2, 5)] if mode == "minor" else [(0, 4, 7), (-3, 0, 4), (-5, -1, 2), (-7, -3, 0)]
    if mode == "minor":
        chords = [(0, 3, 7), (-4, 0, 3), (-2, 2, 5), (-5, -2, 2)]
    bar = beat * 4
    out = np.zeros(n)
    for b in range(int(seconds / bar) + 1):
        ch = chords[b % 4]
        s, e = int(b * bar * SR), min(int((b + 1) * bar * SR), n)
        if s >= n:
            break
        tt = t[s:e] - t[s]
        pad = np.zeros(e - s)
        for semi in ch:
            f = root * 2 ** (semi / 12)
            for det in (0.997, 1.003):
                pad += np.sin(2 * np.pi * f * det * tt) * 0.12
        pad *= np.minimum(np.minimum(tt / 0.6, 1), np.minimum((bar - tt) / 0.6, 1))
        out[s:e] += pad
        # baixo
        for q in range(4):
            qs = int(q * beat * SR)
            seg = min(int(beat * SR), (e - s) - qs)
            if seg <= 0:
                continue
            tb = np.arange(seg) / SR
            f0 = root / 2 * 2 ** (ch[0] / 12)
            out[s + qs:s + qs + seg] += np.sin(2 * np.pi * f0 * tb) * np.exp(-tb * 3.5) * 0.28
        # hi-hat em contratempos
        for q in range(8):
            qs = int((q + 0.5) * beat / 2 * SR) if q % 2 else int(q * beat / 2 * SR)
            seg = min(int(0.05 * SR), (e - s) - qs)
            if seg <= 0 or q % 2 == 0:
                continue
            nz = rng.standard_normal(seg) * np.exp(-np.arange(seg) / SR * 120)
            out[s + qs:s + qs + seg] += nz * 0.05
    out *= np.minimum(np.minimum(t / 1.0, 1), np.minimum((seconds - t) / 1.0, 1))
    return out / np.max(np.abs(out)) * 0.8


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    save("whoosh", whoosh())
    save("tick", tick())
    save("pop", pop())
    save("hit", hit())
    save("music_chartbound", music(110.0, "minor", 104))
    save("music_howitticks", music(98.0, "minor", 96))
    save("music_valeopreco", music(130.8, "major", 112))
    save("music_loja", music(174.6, "major", 92))
    for nm, fn in [("click", click), ("tap", tap), ("ding", ding), ("cash", cash), ("sparkle", sparkle), ("softwhoosh", softwhoosh), ("riser", riser), ("softhit", softhit)]:
        save(nm, fn())
    print("fx ok")

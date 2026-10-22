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
    print("fx ok")

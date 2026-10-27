"""Probe do vídeo longo: modelos TTS do Gemini, amostras de narração com style prompt, métricas
(duração, wpm, variação de tom, pausas, WER do Whisper) e download de trilhas CC-BY do incompetech.
Saída: out_l/*.mp3 + out_l/relatorio.txt"""
import base64, json, os, re, subprocess, time, urllib.request, urllib.parse
import numpy as np, soundfile as sf

os.makedirs("out_l", exist_ok=True)
KEY = os.environ["GEMINI_KEY"]
API = "https://generativelanguage.googleapis.com/v1beta"
rep = []

STYLE = ("You are the narrator of a data documentary on YouTube. Read the script below in a warm, curious, unhurried voice, "
         "with a little dry humor. Speak like you are telling a friend something surprising, not reading a report. "
         "Pause briefly before every number that matters, and let the big reveals land. Never sound like an advertisement.")
TXT = ("In 1990, the average person in Poland produced about six thousand dollars of value a year. [short pause] "
       "The average person in Japan? [pause] Twenty thousand. "
       "Poland was coming out of forty years of communism. Inflation was heading for six hundred percent. "
       "Shops had queues, but not much on the shelves. [short pause] Japan was the second-largest economy on Earth. "
       "Thirty-six years later, the IMF put out a forecast that almost nobody read. "
       "In 2026, for the first time ever, [pause] the average Pole out-produces the average Japanese. "
       "Nobody threw a party. Most people didn't notice. "
       "[softly] And the number that explains how it happened... is the same number that could undo it. "
       "Let's go through the chart.")
PLAIN = re.sub(r"\[[^\]]*\]\s*", "", TXT)


def get(url):
    return json.load(urllib.request.urlopen(url, timeout=60))


def tts(model, voice, text):
    body = {"contents": [{"parts": [{"text": STYLE + "\n\n" + text}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    req = urllib.request.Request(f"{API}/models/{model}:generateContent?key={KEY}", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=300))
    part = r["candidates"][0]["content"]["parts"][0]["inlineData"]
    return base64.b64decode(part["data"]), part.get("mimeType", ""), r.get("usageMetadata", {})


# 1) modelos
models = []
try:
    tok = ""
    while True:
        d = get(f"{API}/models?key={KEY}&pageSize=200" + (f"&pageToken={tok}" if tok else ""))
        models += d.get("models", [])
        tok = d.get("nextPageToken")
        if not tok:
            break
except Exception as e:
    rep.append("lista de modelos erro: " + repr(e)[:200])
tts_models = [m["name"].split("/")[-1] for m in models if "tts" in m["name"]]
rep.append("modelos TTS: " + ", ".join(tts_models))
rep.append("todos (gemini): " + ", ".join(m["name"].split("/")[-1] for m in models if "gemini" in m["name"])[:1500])


def rank(n):  # preferir o mais novo 'flash' não-lite
    v = re.findall(r"(\d+)\.(\d+)", n)
    v = tuple(map(int, v[0])) if v else (0, 0)
    return (v, "lite" not in n, "pro" not in n)


cands = sorted(tts_models, key=rank, reverse=True)
model = os.environ.get("TTS_MODEL") or (cands[0] if cands else "gemini-2.5-flash-preview-tts")
rep.append(f"modelo usado: {model}")

VOICES = os.environ.get("VOICES", "Charon,Sadaltager,Algieba,Iapetus,Gacrux,Sulafat").split(",")
from faster_whisper import WhisperModel
import librosa
wm = WhisperModel("small", compute_type="int8")


def norm(s):
    return [w for w in re.sub(r"[^\w ]", " ", s.lower()).split() if w]


def wer(r, h):
    r, h = norm(r), norm(h)
    d = np.zeros((len(r) + 1, len(h) + 1), int)
    d[:, 0], d[0, :] = range(len(r) + 1), range(len(h) + 1)
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            d[i, j] = min(d[i - 1, j] + 1, d[i, j - 1] + 1, d[i - 1, j - 1] + (r[i - 1] != h[j - 1]))
    return d[-1, -1] / max(len(r), 1)


for v in VOICES:
    tag = f"v_{v}"
    try:
        t0 = time.time()
        raw, mime, use = tts(model, v, TXT)
        sr = int(re.search(r"rate=(\d+)", mime).group(1)) if "rate=" in mime else 24000
        x = np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768
        sf.write(f"out_l/{tag}.wav", x, sr)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"out_l/{tag}.wav", "-b:a", "128k", f"out_l/{tag}.mp3"], check=True)
        dur = len(x) / sr
        f0, vf, _ = librosa.pyin(librosa.resample(x, orig_sr=sr, target_sr=16000), fmin=60, fmax=400, sr=16000)
        f0 = f0[~np.isnan(f0)]
        st = 12 * np.log2(f0 / np.median(f0))
        env = np.sqrt(np.convolve(x ** 2, np.ones(int(.03 * sr)) / int(.03 * sr), "same"))
        silent = env < 0.01
        runs, cur = [], 0
        for s in silent[::int(sr * .01)]:
            cur = cur + 1 if s else (runs.append(cur) or 0)
        pauses = sum(1 for r_ in runs if r_ >= 50)
        segs, _ = wm.transcribe(f"out_l/{tag}.wav", language="en", word_timestamps=True)
        hyp = " ".join(s.text for s in segs)
        nw = len(PLAIN.split())
        rep.append(f"{tag}: {dur:.1f}s, {nw / dur * 60:.0f} wpm, F0 std {np.std(st):.2f} st (p10-p90 {np.percentile(st, 90) - np.percentile(st, 10):.1f}), "
                   f"pausas>0.5s {pauses}, WER {wer(PLAIN, hyp):.2f}, gerou em {time.time() - t0:.0f}s, uso {use}")
        rep.append(f"   whisper: {hyp[:300]}")
    except Exception as e:
        body = e.read().decode()[:500] if hasattr(e, "read") else ""
        rep.append(f"{tag}: ERRO {repr(e)[:120]} {body}")
    time.sleep(7)

# 3) trilhas
TRACKS = ["Cipher", "Hidden Agenda", "Lightless Dawn", "Deliberate Thought", "Investigations", "Clean Soul", "Inspired",
          "Heartbreaking", "Long Note Four", "Dreamer", "Reawakening", "Impact Moderato", "Ice Flow", "Fearless First",
          "Floating Cities", "Blue Feather", "Ossuary 6 - Air", "Eastminster", "Thinking Music", "Lasting Hope"]
os.makedirs("out_l/music", exist_ok=True)
for t in TRACKS:
    url = "https://incompetech.com/music/royalty-free/mp3-royaltyfree/" + urllib.parse.quote(t) + ".mp3"
    p = f"out_l/music/{t.replace(' ', '_')}.mp3"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        open(p, "wb").write(urllib.request.urlopen(req, timeout=60).read())
        y, s = librosa.load(p, sr=22050, mono=True)
        tempo = librosa.beat.tempo(y=y, sr=s)[0]
        cent = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=s)))
        rms = librosa.feature.rms(y=y)[0]
        rep.append(f"music {t}: {len(y) / s:.0f}s, {tempo:.0f} bpm, centroide {cent:.0f} Hz, dinâmica p90/p10 {np.percentile(rms, 90) / (np.percentile(rms, 10) + 1e-6):.1f}x, {os.path.getsize(p) // 1024} KB")
    except Exception as e:
        rep.append(f"music {t}: ERRO {repr(e)[:100]}")
        if os.path.exists(p):
            os.remove(p)

open("out_l/relatorio.txt", "w").write("\n".join(rep))
print("\n".join(rep))

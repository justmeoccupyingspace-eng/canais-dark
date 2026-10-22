"""Amostras de vozes pt-BR (Google Chirp 3 HD + Neural2 + edge) e avaliação automática:
idioma detectado pelo Whisper (prob. de 'pt') e erro de palavras. Saída: out_v/*.mp3 + out_v/relatorio.txt"""
import base64, json, os, re, subprocess, urllib.request, asyncio
import numpy as np, soundfile as sf
os.makedirs("out_v", exist_ok=True)
KEY = os.environ.get("GCP_TTS_KEY", "")
TXT = ("Nail designer, sabe aquela cliente que sumiu? Muitas vezes ela só não foi lembrada. "
       "Essa planilha calcula o dia do retorno de cada cliente e, quando chega a hora, a mensagem já vai pronta no WhatsApp. "
       "É uma planilha pronta, que abre no Excel ou no Google Planilhas, e custa trinta e quatro e noventa.")
TXT_M = ("Barbeiro, quanto sobrou no fim do mês? Não o que entrou, o que ficou. "
         "Essa planilha soma cada corte, desconta as despesas e mostra o lucro do mês. "
         "E quando o cliente some, a mensagem já vai pronta no WhatsApp. Chama no WhatsApp da bio.")
FEM = ["Leda", "Sulafat", "Achernar", "Callirrhoe", "Laomedeia", "Aoede", "Despina", "Kore", "Vindemiatrix"]
MAS = ["Charon", "Achird", "Sadachbia", "Umbriel", "Puck", "Algieba", "Iapetus", "Orus", "Schedar"]


def google(name, text, rate=None):
    cfg = {"audioEncoding": "MP3"}
    if rate:
        cfg["speakingRate"] = rate
    body = json.dumps({"input": {"text": text}, "voice": {"languageCode": "pt-BR", "name": name}, "audioConfig": cfg}).encode()
    req = urllib.request.Request(f"https://texttospeech.googleapis.com/v1/text:synthesize?key={KEY}", data=body, headers={"Content-Type": "application/json"})
    return base64.b64decode(json.load(urllib.request.urlopen(req, timeout=60))["audioContent"])


async def edge(voice, text, path):
    import edge_tts
    await edge_tts.Communicate(text, voice).save(path)


samples = []
for v in FEM:
    samples.append((f"F_chirp_{v}", f"pt-BR-Chirp3-HD-{v}", TXT))
for v in MAS:
    samples.append((f"M_chirp_{v}", f"pt-BR-Chirp3-HD-{v}", TXT_M))
for v in ["pt-BR-Neural2-A", "pt-BR-Neural2-C"]:
    samples.append((f"F_{v}", v, TXT))
for v in ["pt-BR-Neural2-B"]:
    samples.append((f"M_{v}", v, TXT_M))
rep = []
for tag, name, text in samples:
    p = f"out_v/{tag}.mp3"
    try:
        open(p, "wb").write(google(name, text))
    except Exception as e:
        rep.append(f"{tag}: ERRO {repr(e)[:120]}")
for tag, v, text in [("F_edge_Francisca", "pt-BR-FranciscaNeural", TXT), ("F_edge_Thalita", "pt-BR-ThalitaMultilingualNeural", TXT), ("M_edge_Antonio", "pt-BR-AntonioNeural", TXT_M)]:
    try:
        asyncio.run(edge(v, text, f"out_v/{tag}.mp3"))
    except Exception as e:
        rep.append(f"{tag}: ERRO edge {repr(e)[:100]}")

from faster_whisper import WhisperModel
m = WhisperModel("small", compute_type="int8")


def norm(s):
    return [w for w in re.sub(r"[^\wà-ú ]", " ", s.lower()).split() if w]


def wer(r, h):
    r, h = norm(r), norm(h)
    d = np.zeros((len(r) + 1, len(h) + 1), int)
    d[:, 0], d[0, :] = range(len(r) + 1), range(len(h) + 1)
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            d[i, j] = min(d[i - 1, j] + 1, d[i, j - 1] + 1, d[i - 1, j - 1] + (r[i - 1] != h[j - 1]))
    return d[-1, -1] / max(len(r), 1)


import librosa
for f in sorted(os.listdir("out_v")):
    if not f.endswith(".mp3"):
        continue
    path = f"out_v/{f}"
    ref = TXT if f.startswith("F") else TXT_M
    segs, info = m.transcribe(path)  # idioma automático: mede se soa português
    hyp = " ".join(s.text for s in segs)
    segs2, _ = m.transcribe(path, language="pt")
    hyp2 = " ".join(s.text for s in segs2)
    y, sr = librosa.load(path, sr=16000)
    f0, vf, _ = librosa.pyin(y, fmin=60, fmax=400, sr=sr)
    f0 = f0[~np.isnan(f0)]
    st = 12 * np.log2(f0 / np.median(f0)) if len(f0) else np.array([0])
    rep.append(f"{f[:-4]:28s} lang={info.language} p={info.language_probability:.2f} | WER_pt={wer(ref, hyp2):.2f} | pitch_desvio={np.std(st):.2f}st | dur={len(y)/sr:.1f}s")
open("out_v/relatorio.txt", "w").write("\n".join(rep) + "\n")
print("\n".join(rep))

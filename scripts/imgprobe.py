"""Testa quais modelos de imagem a chave Gemini consegue usar (e gera 1 imagem de teste de cada um que funcionar).
Uso: python scripts/imgprobe.py out/"""
import base64, json, os, sys, urllib.request, urllib.error
KEY = os.environ["GEMINI_KEY"]; OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
API = "https://generativelanguage.googleapis.com/v1beta"
models = json.load(urllib.request.urlopen(f"{API}/models?key={KEY}&pageSize=200"))["models"]
names = [m["name"] for m in models if any(k in m["name"] for k in ("image", "imagen", "veo"))]
print("modelos de imagem/vídeo listados:", names)
PROMPT = ("Cinematic oil-painting style illustration, warm golden light: a humble man kneeling in prayer on a hill at night under a starry sky, "
          "seen from behind, silhouette, soft moonlight, peaceful, high detail, 16:9, no text.")
res = {}
for n in names:
    m = n.split("/")[-1]
    try:
        if "imagen" in m:
            body = {"instances": [{"prompt": PROMPT}], "parameters": {"sampleCount": 1, "aspectRatio": "16:9"}}
            r = json.load(urllib.request.urlopen(urllib.request.Request(f"{API}/models/{m}:predict?key={KEY}", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}), timeout=120))
            b = r["predictions"][0]["bytesBase64Encoded"]
        elif "veo" in m:
            res[m] = "pulado (vídeo)"; continue
        else:
            body = {"contents": [{"parts": [{"text": PROMPT}]}], "generationConfig": {"responseModalities": ["IMAGE", "TEXT"]}}
            r = json.load(urllib.request.urlopen(urllib.request.Request(f"{API}/models/{m}:generateContent?key={KEY}", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}), timeout=120))
            parts = r["candidates"][0]["content"]["parts"]
            b = next(p["inlineData"]["data"] for p in parts if "inlineData" in p)
        open(f"{OUT}/{m}.png", "wb").write(base64.b64decode(b)); res[m] = "OK"
    except urllib.error.HTTPError as e:
        res[m] = f"HTTP {e.code}: {e.read().decode(errors='replace')[:300]}"
    except Exception as e:
        res[m] = repr(e)[:300]
    print(m, res[m][:200])
json.dump(res, open(f"{OUT}/res.json", "w"), indent=1)

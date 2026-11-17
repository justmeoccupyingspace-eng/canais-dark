"""Fundo de mapa em relevo/satélite (NASA, domínio público, via Wikimedia Commons) reprojetado para Mercator,
cortado em blocos para o Remotion só carregar o que aparece na tela.
Saída: public/geo/merc_lo.jpg (4096 px, mundo inteiro) + public/geo/m_<i>_<j>.jpg (grade NX x NY do arquivo grande) + public/geo/merc.json
Uso: python scripts/basemap.py"""
import json, math, os, urllib.parse, urllib.request
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
UA = {"User-Agent": "canais-dark-bot/1.0 (https://github.com/justmeoccupyingspace-eng/canais-dark; basemap)"}
TITLE = os.environ.get("TITLE", "File:Whole world - land and oceans 12000.jpg")
OUT = "public/geo"; os.makedirs(OUT, exist_ok=True)
q = {"action": "query", "titles": TITLE, "prop": "imageinfo", "iiprop": "url|size|extmetadata", "format": "json"}
r = json.load(urllib.request.urlopen(urllib.request.Request("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(q), headers=UA), timeout=60))
ii = list(r["query"]["pages"].values())[0]["imageinfo"][0]
lic = ii["extmetadata"].get("LicenseShortName", {}).get("value", "")
print("fonte", ii["url"], ii["width"], ii["height"], lic)
open("/tmp/src.jpg", "wb").write(urllib.request.urlopen(urllib.request.Request(ii["url"], headers=UA), timeout=600).read())
src = np.asarray(Image.open("/tmp/src.jpg").convert("RGB"))
H0, W0, _ = src.shape
LAT_N, LAT_S = 84.0, -80.0
yN = math.log(math.tan(math.pi / 4 + math.radians(LAT_N) / 2)); yS = math.log(math.tan(math.pi / 4 + math.radians(LAT_S) / 2))
def warp(W):
    pxr = W / (2 * math.pi)
    H = int(round((yN - yS) * pxr))
    ym = yN - (np.arange(H) + 0.5) / pxr                      # mercator y de cada linha
    lat = np.degrees(2 * np.arctan(np.exp(ym)) - np.pi / 2)
    rows = np.clip(((90 - lat) / 180 * H0).astype(int), 0, H0 - 1)
    cols = np.clip(((np.arange(W) + 0.5) / W * W0).astype(int), 0, W0 - 1)
    return src[rows][:, cols]
lo = warp(4096); Image.fromarray(lo).save(f"{OUT}/merc_lo.jpg", quality=82)
hi = warp(W0)
NX, NY = 6, 5
Hh, Wh = hi.shape[:2]
tiles = []
for j in range(NY):
    for i in range(NX):
        x0, x1 = Wh * i // NX, Wh * (i + 1) // NX; y0, y1 = Hh * j // NY, Hh * (j + 1) // NY
        Image.fromarray(hi[y0:y1, x0:x1]).save(f"{OUT}/m_{i}_{j}.jpg", quality=84)
        tiles.append([i, j, x0, y0, x1 - x0, y1 - y0])
json.dump({"latN": LAT_N, "latS": LAT_S, "W": Wh, "H": Hh, "loW": lo.shape[1], "loH": lo.shape[0], "tiles": tiles, "source": ii["url"], "license": lic}, open(f"{OUT}/merc.json", "w"))
print("ok", Wh, Hh, sum(os.path.getsize(f"{OUT}/{f}") for f in os.listdir(OUT)) // 1e6, "MB")

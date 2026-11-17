"""Baixa pinturas em DOMÍNIO PÚBLICO do Wikimedia Commons (só arquivos cuja licença no Commons é Public domain / PD / CC0).
Uso: python scripts/pdimg.py research/pd_queries.json out/   → out/<slug>.jpg (1920 px) + out/meta.json (artista, licença, página)
Cada imagem fica registrada com a página de origem, para crédito na descrição quando for o caso."""
import json, os, re, sys, time, urllib.parse, urllib.request

UA = {"User-Agent": "canais-dark-bot/1.0 (https://github.com/justmeoccupyingspace-eng/canais-dark; automated PD image fetch)"}
Q = json.load(open(sys.argv[1])); OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
API = "https://commons.wikimedia.org/w/api.php"
meta, seen = {}, set()
strip = lambda h: re.sub(r"<[^>]+>", "", h or "").strip()
for q in Q["queries"]:
    p = {"action": "query", "generator": "search", "gsrsearch": q["q"] + " filetype:bitmap", "gsrnamespace": 6, "gsrlimit": q.get("n", 20),
         "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiurlwidth": 1920, "format": "json"}
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(API + "?" + urllib.parse.urlencode(p), headers=UA), timeout=60))
    except Exception as e:
        print("busca falhou", q["q"], repr(e)[:120]); continue
    got = 0
    for pg in sorted((r.get("query", {}).get("pages", {}) or {}).values(), key=lambda x: x.get("index", 0)):
        ii = (pg.get("imageinfo") or [{}])[0]
        em = ii.get("extmetadata", {})
        lic = strip(em.get("LicenseShortName", {}).get("value", ""))
        if not re.search(r"public domain|^pd|cc0", lic, re.I):
            continue
        if ii.get("width", 0) < 1200 or pg["title"] in seen:
            continue
        seen.add(pg["title"])
        slug = q["tag"] + "_" + re.sub(r"[^a-z0-9]+", "_", pg["title"][5:].lower())[:50].strip("_")
        try:
            data = urllib.request.urlopen(urllib.request.Request(ii.get("thumburl") or ii["url"], headers=UA), timeout=90).read()
            open(f"{OUT}/{slug}.jpg", "wb").write(data)
            meta[slug] = {"title": pg["title"], "artist": strip(em.get("Artist", {}).get("value", ""))[:120], "date": strip(em.get("DateTimeOriginal", {}).get("value", ""))[:60],
                          "license": lic, "page": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(pg["title"].replace(" ", "_")), "w": ii.get("width"), "h": ii.get("height"), "q": q["q"]}
            got += 1
            time.sleep(0.5)
        except Exception as e:
            print("download falhou", pg["title"], repr(e)[:120])
    print(q["q"], "→", got)
json.dump(meta, open(f"{OUT}/meta.json", "w"), ensure_ascii=False, indent=1)
print("total", len(meta))

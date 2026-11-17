"""Raio-X de canais concorrentes a partir de 1 vídeo de cada: dados do canal, últimos 30 envios (views, duração, título),
e miniaturas (alta resolução) dos 6 mais vistos recentes, para estudar formato e visual.
Uso: python scripts/chanprobe.py research/q_probe_*.json out/"""
import json, os, re, sys, urllib.parse, urllib.request

def post(url, data):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, data=urllib.parse.urlencode(data).encode())))
def get(url, tok, **q):
    return json.load(urllib.request.urlopen(urllib.request.Request(url + '?' + urllib.parse.urlencode(q), headers={"Authorization": f"Bearer {tok}"})))
API = "https://www.googleapis.com/youtube/v3/"
tok = post("https://oauth2.googleapis.com/token", {"client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"], "refresh_token": os.environ["YT_REFRESH_A"], "grant_type": "refresh_token"})["access_token"]
Q = json.load(open(sys.argv[1])); OUT = sys.argv[2]; os.makedirs(OUT + "/th", exist_ok=True)
def dur_s(iso):
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    return sum(int(x or 0) * k for x, k in zip(m.groups(), (3600, 60, 1))) if m else 0
seed = get(API + "videos", tok, part="snippet", id=",".join(Q["videos"]))["items"]
chans = sorted({v["snippet"]["channelId"] for v in seed})
res = {}
for c in get(API + "channels", tok, part="snippet,statistics,contentDetails,brandingSettings", id=",".join(chans))["items"]:
    up = c["contentDetails"]["relatedPlaylists"]["uploads"]
    items = get(API + "playlistItems", tok, part="contentDetails", playlistId=up, maxResults=30).get("items", [])
    vids = [i["contentDetails"]["videoId"] for i in items]
    vv = get(API + "videos", tok, part="snippet,statistics,contentDetails", id=",".join(vids)).get("items", []) if vids else []
    rows = [{"id": v["id"], "t": v["snippet"]["title"], "pub": v["snippet"]["publishedAt"][:16], "views": int(v["statistics"].get("viewCount", 0)),
             "likes": int(v["statistics"].get("likeCount", 0)), "comments": int(v["statistics"].get("commentCount", 0)), "dur": dur_s(v["contentDetails"]["duration"]),
             "desc": v["snippet"].get("description", "")[:400], "tags": v["snippet"].get("tags", [])[:12],
             "thumb": (v["snippet"]["thumbnails"].get("maxres") or v["snippet"]["thumbnails"].get("high") or {}).get("url")} for v in vv]
    s = c["statistics"]
    name = c["snippet"]["title"]
    res[c["id"]] = {"title": name, "handle": c["snippet"].get("customUrl"), "created": c["snippet"]["publishedAt"][:10], "country": c["snippet"].get("country"),
                    "subs": int(s.get("subscriberCount", 0)), "videos": int(s.get("videoCount", 0)), "views": int(s.get("viewCount", 0)),
                    "desc": c["snippet"].get("description", "")[:500], "recent": rows}
    slug = re.sub(r"[^a-z0-9]+", "_", name.lower())[:30]
    for k, r in enumerate(sorted([r for r in rows if r["thumb"]], key=lambda r: -r["views"])[:6]):
        try:
            open(f"{OUT}/th/{slug}_{k}_{r['views']}_{r['dur']}s.jpg", "wb").write(urllib.request.urlopen(r["thumb"], timeout=30).read())
        except Exception as e:
            print("thumb falhou", slug, repr(e)[:100])
json.dump(res, open(f"{OUT}/probe.json", "w"), ensure_ascii=False, indent=1)
print("ok", len(res))

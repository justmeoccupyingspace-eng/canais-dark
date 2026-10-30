"""Pesquisa de concorrência no YouTube (Data API). Uso: python scripts/ytresearch.py <queries.json> <out.json>
queries.json: {"channels": ["How It Ticks", ...], "topics": [{"id": "gps", "q": "how GPS works relativity", "order": "viewCount", "after": "2024-01-01T00:00:00Z", "dur": "medium|long|any"}]}"""
import json, os, re, sys, urllib.parse, urllib.request

def post(url, data):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, data=urllib.parse.urlencode(data).encode())))
def get(url, tok, **q):
    u = url + '?' + urllib.parse.urlencode(q)
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": f"Bearer {tok}"})))
API = "https://www.googleapis.com/youtube/v3/"
tok = post("https://oauth2.googleapis.com/token", {"client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"], "refresh_token": os.environ["YT_REFRESH_A"], "grant_type": "refresh_token"})["access_token"]
Q = json.load(open(sys.argv[1]))
out = {"channels": {}, "topics": {}}

def chstats(ids):
    res = {}
    for i in range(0, len(ids), 50):
        for c in get(API + "channels", tok, part="snippet,statistics", id=",".join(ids[i:i+50])).get("items", []):
            s = c["statistics"]
            res[c["id"]] = {"title": c["snippet"]["title"], "handle": c["snippet"].get("customUrl"), "created": c["snippet"]["publishedAt"][:10],
                            "subs": int(s.get("subscriberCount", 0)), "videos": int(s.get("videoCount", 0)), "views": int(s.get("viewCount", 0)), "country": c["snippet"].get("country")}
    return res

def dur_s(iso):
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    return sum(int(x or 0) * k for x, k in zip(m.groups(), (3600, 60, 1))) if m else 0

for name in Q.get("channels", []):
    try:
        r = get(API + "search", tok, part="snippet", q=name, type="channel", maxResults=50)
        ids = [i["snippet"]["channelId"] for i in r.get("items", [])]
        st = chstats(ids)
        norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
        rows = sorted(st.values(), key=lambda x: -x["subs"])
        out["channels"][name] = {"total_results": r.get("pageInfo", {}).get("totalResults"), "exact_or_contains": [x for x in rows if norm(name) in norm(x["title"])], "top": rows[:15]}
    except Exception as e:
        out["channels"][name] = {"error": repr(e)[:300]}

for t in Q.get("topics", []):
    try:
        q = dict(part="snippet", q=t["q"], type="video", maxResults=t.get("n", 25), order=t.get("order", "viewCount"), relevanceLanguage=t.get("lang", "en"))
        if t.get("after"): q["publishedAfter"] = t["after"]
        if t.get("dur", "any") != "any": q["videoDuration"] = t["dur"]
        r = get(API + "search", tok, **q)
        vids = [i["id"]["videoId"] for i in r.get("items", []) if i["id"].get("videoId")]
        vv = get(API + "videos", tok, part="snippet,statistics,contentDetails", id=",".join(vids)).get("items", []) if vids else []
        st = chstats(sorted({v["snippet"]["channelId"] for v in vv}))
        rows = []
        for v in vv:
            c = st.get(v["snippet"]["channelId"], {})
            views = int(v["statistics"].get("viewCount", 0))
            rows.append({"title": v["snippet"]["title"][:110], "id": v["id"], "published": v["snippet"]["publishedAt"][:10], "views": views,
                         "dur_s": dur_s(v["contentDetails"]["duration"]), "channel": c.get("title"), "subs": c.get("subs"), "ch_created": c.get("created"),
                         "ch_videos": c.get("videos"), "ratio": round(views / max(1, c.get("subs") or 1), 2)})
        out["topics"][t["id"]] = {"q": t["q"], "order": q["order"], "after": t.get("after"), "total_results": r.get("pageInfo", {}).get("totalResults"), "videos": rows}
    except Exception as e:
        out["topics"][t["id"]] = {"error": repr(e)[:300]}

json.dump(out, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
print("ok", len(out["channels"]), "nomes,", len(out["topics"]), "temas")

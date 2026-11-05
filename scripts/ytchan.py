"""Lista os envios de um canal e, com MODE=private, deixa privados os vídeos dados em IDS (ou todos os públicos/agendados com ALL=1).
MODE=playlist põe os IDS na playlist cujo título é PL (não cria playlist nova, não remove nada).
Nada é apagado. Uso: CH=B MODE=list|private|playlist [IDS=a,b] [ALL=1] [PL=título] python scripts/ytchan.py out.json"""
import json, os, sys, urllib.parse, urllib.request
def post(url, data):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, data=urllib.parse.urlencode(data).encode())))
def call(method, url, tok, body=None):
    req = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body else None,
                                 headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))
ch = os.environ.get("CH", "B"); mode = os.environ.get("MODE", "list")
tok = post("https://oauth2.googleapis.com/token", {"client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"], "refresh_token": os.environ[f"YT_REFRESH_{ch}"], "grant_type": "refresh_token"})["access_token"]
API = "https://www.googleapis.com/youtube/v3/"
c = call("GET", API + "channels?part=snippet,contentDetails,statistics&mine=true", tok)["items"][0]
up = c["contentDetails"]["relatedPlaylists"]["uploads"]
ids, page = [], ""
while True:
    r = call("GET", API + f"playlistItems?part=contentDetails&maxResults=50&playlistId={up}" + (f"&pageToken={page}" if page else ""), tok)
    ids += [i["contentDetails"]["videoId"] for i in r.get("items", [])]
    page = r.get("nextPageToken")
    if not page: break
extra = [x for x in os.environ.get("IDS", "").split(",") if x and x not in ids]
ids += extra
vids = []
for i in range(0, len(ids), 50):
    vids += call("GET", API + "videos?part=snippet,status,statistics,contentDetails&id=" + ",".join(ids[i:i + 50]), tok).get("items", [])
rows = [dict(id=v["id"], title=v["snippet"]["title"], published=v["snippet"]["publishedAt"], privacy=v["status"]["privacyStatus"], publishAt=v["status"].get("publishAt"),
             views=int(v["statistics"].get("viewCount", 0)), dur=v["contentDetails"]["duration"]) for v in vids]
print("canal", c["snippet"]["title"], c["snippet"].get("customUrl"), "inscritos", c["statistics"].get("subscriberCount"), "envios", len(rows))
for r in sorted(rows, key=lambda r: r["published"]):
    print(f"{r['id']} {r['privacy']:8} {str(r['publishAt'] or ''):22} {r['views']:>6} {r['dur']:>9} {r['title'][:70]}")
done = []
if mode == "private":
    want = set(os.environ.get("IDS", "").split(",")) - {""}
    for v in vids:
        st = v["status"]
        if not (v["id"] in want or (os.environ.get("ALL") == "1" and (st["privacyStatus"] != "private" or st.get("publishAt")))):
            continue
        body = {"id": v["id"], "status": {"privacyStatus": "private", "embeddable": st.get("embeddable", True), "license": st.get("license", "youtube"),
                                          "publicStatsViewable": st.get("publicStatsViewable", True), "selfDeclaredMadeForKids": st.get("madeForKids", False),
                                          **({"containsSyntheticMedia": st["containsSyntheticMedia"]} if "containsSyntheticMedia" in st else {})}}
        r = call("PUT", API + "videos?part=status", tok, body)
        done.append(v["id"]); print("privado:", v["id"], r["status"].get("privacyStatus"), r["status"].get("publishAt"))
added = []
if mode == "playlist":
    want = [x for x in os.environ.get("IDS", "").split(",") if x]
    pls = call("GET", API + "playlists?part=snippet&mine=true&maxResults=50", tok).get("items", [])
    pl = next((p for p in pls if p["snippet"]["title"].strip().lower() == os.environ.get("PL", "").strip().lower()), None)
    print("playlists:", [p["snippet"]["title"] for p in pls])
    if not pl:
        raise SystemExit("playlist não encontrada: " + os.environ.get("PL", ""))
    have, page = [], ""
    while True:
        r = call("GET", API + f"playlistItems?part=contentDetails&maxResults=50&playlistId={pl['id']}" + (f"&pageToken={page}" if page else ""), tok)
        have += [i["contentDetails"]["videoId"] for i in r.get("items", [])]
        page = r.get("nextPageToken")
        if not page: break
    for v in want:
        if v in have:
            print("já está:", v); continue
        call("POST", API + "playlistItems?part=snippet", tok, {"snippet": {"playlistId": pl["id"], "resourceId": {"kind": "youtube#video", "videoId": v}}})
        added.append(v); print(f"::notice::{v} adicionado à playlist {pl['snippet']['title']}")
json.dump(dict(channel=c["snippet"]["title"], rows=rows, made_private=done, playlist_added=added), open(sys.argv[1], "w"), indent=1, ensure_ascii=False)

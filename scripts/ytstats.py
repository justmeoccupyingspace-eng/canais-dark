"""Coleta desempenho dos canais A/B: inscritos, vídeos (views/likes/comentários/status), comentários recentes e, se o escopo permitir, YouTube Analytics."""
import json, os, urllib.parse, urllib.request, datetime as dt

def post(url, data):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, data=urllib.parse.urlencode(data).encode())))
def get(url, tok, **q):
    u = url + ('?' + urllib.parse.urlencode(q) if q else '')
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": f"Bearer {tok}"})))
def access(refresh):
    return post("https://oauth2.googleapis.com/token", {"client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"], "refresh_token": refresh, "grant_type": "refresh_token"})["access_token"]

API = "https://www.googleapis.com/youtube/v3/"
out = {}
for which in ("A", "B"):
    r = {}
    try:
        t = access(os.environ[f"YT_REFRESH_{which}"])
        ti = json.load(urllib.request.urlopen(f"https://oauth2.googleapis.com/tokeninfo?access_token={t}"))
        r["scopes"] = ti.get("scope")
        ch = get(API + "channels", t, part="snippet,statistics,contentDetails,status,brandingSettings", mine="true")["items"][0]
        r["channel"] = {"id": ch["id"], "title": ch["snippet"]["title"], "stats": ch["statistics"], "status": ch.get("status"), "desc": ch["snippet"].get("description", "")[:300]}
        upl = ch["contentDetails"]["relatedPlaylists"]["uploads"]
        ids, tokn = [], None
        while True:
            q = dict(part="contentDetails", playlistId=upl, maxResults=50)
            if tokn: q["pageToken"] = tokn
            pl = get(API + "playlistItems", t, **q)
            ids += [i["contentDetails"]["videoId"] for i in pl["items"]]
            tokn = pl.get("nextPageToken")
            if not tokn: break
        vids = []
        for i in range(0, len(ids), 50):
            vv = get(API + "videos", t, part="snippet,statistics,status,contentDetails", id=",".join(ids[i:i+50]))
            for v in vv["items"]:
                vids.append({"id": v["id"], "title": v["snippet"]["title"], "published": v["snippet"]["publishedAt"],
                             "privacy": v["status"]["privacyStatus"], "publishAt": v["status"].get("publishAt"),
                             "upload": v["status"].get("uploadStatus"), "reject": v["status"].get("rejectionReason"),
                             "madeForKids": v["status"].get("madeForKids"), "dur": v["contentDetails"]["duration"],
                             "views": int(v["statistics"].get("viewCount", 0)), "likes": int(v["statistics"].get("likeCount", 0)),
                             "comments": int(v["statistics"].get("commentCount", 0))})
        r["videos"] = sorted(vids, key=lambda x: x["published"])
        try:
            cm = get(API + "commentThreads", t, part="snippet", allThreadsRelatedToChannelId=ch["id"], maxResults=50, order="time")
            r["comments"] = [{"video": c["snippet"].get("videoId"), "text": c["snippet"]["topLevelComment"]["snippet"]["textOriginal"][:300],
                              "at": c["snippet"]["topLevelComment"]["snippet"]["publishedAt"]} for c in cm.get("items", [])]
        except Exception as e:
            r["comments_err"] = str(e)
        try:
            end = dt.date.today().isoformat(); start = (dt.date.today() - dt.timedelta(days=60)).isoformat()
            an = get("https://youtubeanalytics.googleapis.com/v2/reports", t, ids="channel==MINE", startDate=start, endDate=end,
                     metrics="views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,likes,comments,shares",
                     dimensions="video", sort="-views", maxResults=200)
            r["analytics_by_video"] = an
            tr = get("https://youtubeanalytics.googleapis.com/v2/reports", t, ids="channel==MINE", startDate=start, endDate=end,
                     metrics="views", dimensions="insightTrafficSourceType", sort="-views")
            r["traffic"] = tr
            geo = get("https://youtubeanalytics.googleapis.com/v2/reports", t, ids="channel==MINE", startDate=start, endDate=end,
                      metrics="views", dimensions="country", sort="-views", maxResults=10)
            r["geo"] = geo
            day = get("https://youtubeanalytics.googleapis.com/v2/reports", t, ids="channel==MINE", startDate=start, endDate=end,
                      metrics="views,subscribersGained", dimensions="day", sort="day")
            r["daily"] = day
        except Exception as e:
            r["analytics_err"] = str(e)[:300]
    except Exception as e:
        r["err"] = str(e)[:500]
    out[which] = r
os.makedirs("stats_out", exist_ok=True)
json.dump(out, open("stats_out/yt.json", "w"), ensure_ascii=False, indent=1)
for k, r in out.items():
    print(k, r.get("channel", {}).get("title"), r.get("channel", {}).get("stats"), len(r.get("videos", [])), r.get("analytics_err", "analytics ok"))

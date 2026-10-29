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
                             "comments": int(v["statistics"].get("commentCount", 0)),
                             "detail": {"embeddable": v["status"].get("embeddable"), "license": v["status"].get("license"),
                                        "synthetic": v["status"].get("containsSyntheticMedia"), "rating": v["contentDetails"].get("contentRating"),
                                        "region": v["contentDetails"].get("regionRestriction"), "licensed": v["contentDetails"].get("licensedContent"),
                                        "cat": v["snippet"].get("categoryId"), "lang": v["snippet"].get("defaultAudioLanguage"),
                                        "tags": len(v["snippet"].get("tags", [])), "thumbs": sorted(v["snippet"].get("thumbnails", {}).keys())}})
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
            import re as _re
            r["long"] = {}
            for v in r.get("videos", []):
                m = _re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", v.get("dur") or "")
                secs = (int(m.group(1) or 0) * 3600 + int(m.group(2) or 0) * 60 + int(m.group(3) or 0)) if m else 0
                if secs < 180 or v.get("privacy") != "public":
                    continue
                L = {}
                try:
                    L["retention"] = get("https://youtubeanalytics.googleapis.com/v2/reports", t, ids="channel==MINE", startDate=start, endDate=end,
                                         metrics="audienceWatchRatio,relativeRetentionPerformance", dimensions="elapsedVideoTimeRatio", filters="video==" + v["id"])
                except Exception as e:
                    L["retention_err"] = str(e)[:200]
                try:
                    L["traffic"] = get("https://youtubeanalytics.googleapis.com/v2/reports", t, ids="channel==MINE", startDate=start, endDate=end,
                                       metrics="views,estimatedMinutesWatched", dimensions="insightTrafficSourceType", filters="video==" + v["id"], sort="-views")
                    L["daily"] = get("https://youtubeanalytics.googleapis.com/v2/reports", t, ids="channel==MINE", startDate=start, endDate=end,
                                     metrics="views,estimatedMinutesWatched,averageViewDuration,subscribersGained", dimensions="day", filters="video==" + v["id"], sort="day")
                except Exception as e:
                    L["traffic_err"] = str(e)[:200]
                r["long"][v["id"]] = L
        except Exception as e:
            r["analytics_err"] = str(e)[:300]
    except Exception as e:
        r["err"] = str(e)[:500]
    out[which] = r
os.makedirs("stats_out", exist_ok=True)
json.dump(out, open("stats_out/yt.json", "w"), ensure_ascii=False, indent=1)
for k, r in out.items():
    print(k, r.get("channel", {}).get("title"), r.get("channel", {}).get("stats"), len(r.get("videos", [])), r.get("analytics_err", "analytics ok"))

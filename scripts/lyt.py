"""Metadados do vídeo longo para o YouTube a partir da timeline: créditos de música, capítulos e thumbnail.
Uso: python scripts/lyt.py meta public/build/x.json out/yt.json
     python scripts/lyt.py thumb <A|B> <videoId> out/thumb.jpg"""
import json, os, sys, urllib.parse, urllib.request


def mmss(t):
    t = int(t)
    return f"{t // 60}:{t % 60:02d}"


def meta(src, dst, specpath=None):
    d = json.load(open(src))
    if specpath and os.path.exists(specpath):  # textos do spec atual valem mais que os da timeline antiga
        sp = json.load(open(specpath))
        d["yt"], d["chapter0"] = sp.get("yt", d["yt"]), sp.get("chapter0", d.get("chapter0"))
    shots, acts = d["shots"], d.get("acts", [])
    chap = ["0:00 " + d.get("chapter0", "Intro")]
    for i, s in enumerate(shots):
        if i and s["act"] != shots[i - 1]["act"]:
            chap.append(f"{mmss(s['t0'] - 1.4)} {acts[s['act']]}")
    tracks = [m["title"] for m in d.get("music", [])]
    seen = []
    for t in tracks:
        if t not in seen:
            seen.append(t)
    credits = ("Music by Kevin MacLeod (incompetech.com): " + ", ".join(seen) +
               ". Licensed under Creative Commons: By Attribution 4.0 (creativecommons.org/licenses/by/4.0/)") if seen else ""
    yt = dict(d["yt"])
    desc = yt.get("description", "").replace("{music_credits}", credits)
    yt["description"] = desc.replace("\n\nSources:", "\n\nChapters:\n" + "\n".join(chap) + "\n\nSources:", 1)
    json.dump({"yt": yt, "publish": d.get("publish", {})}, open(dst, "w"), ensure_ascii=False, indent=1)
    print(yt["title"]); print(yt["description"])


def thumb(which, vid, img):
    data = urllib.parse.urlencode({"client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
                                   "refresh_token": os.environ[f"YT_REFRESH_{which}"], "grant_type": "refresh_token"}).encode()
    tok = json.load(urllib.request.urlopen(urllib.request.Request("https://oauth2.googleapis.com/token", data=data)))["access_token"]
    req = urllib.request.Request(f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={vid}", data=open(img, "rb").read(),
                                 method="POST", headers={"Authorization": f"Bearer {tok}", "Content-Type": "image/jpeg"})
    try:
        urllib.request.urlopen(req)
        print(f"::notice title=thumb::thumbnail aplicada em {vid}")
    except urllib.error.HTTPError as e:
        print(f"::warning title=thumb::{e.code} {e.read().decode(errors='replace')[:300]}")


if __name__ == "__main__":
    if sys.argv[1] == "meta":
        meta(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
    else:
        thumb(*sys.argv[2:5])

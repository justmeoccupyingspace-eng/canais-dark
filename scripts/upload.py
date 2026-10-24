"""Envia vídeo ao YouTube. Uso: python scripts/upload.py <A|B> video.mp4 spec.json [privacyStatus]
Segredos via env: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_A / YT_REFRESH_B"""
import json, os, sys, urllib.error, urllib.parse, urllib.request

def access_token(refresh):
    data = urllib.parse.urlencode({
        "client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": refresh, "grant_type": "refresh_token"}).encode()
    return json.load(urllib.request.urlopen(urllib.request.Request("https://oauth2.googleapis.com/token", data=data)))["access_token"]

def main(which, video, specpath, privacy="public"):
    spec = json.load(open(specpath, encoding="utf-8"))
    tok = access_token(os.environ[f"YT_REFRESH_{which}"])
    meta = {
        "snippet": {
            "title": spec["yt"]["title"][:100],
            "description": spec["yt"].get("description", ""),
            "tags": spec["yt"].get("tags", []),
            "categoryId": spec["yt"].get("categoryId", "27"),
            "defaultLanguage": spec["yt"].get("lang", "en"),
        },
        "status": {"privacyStatus": privacy, "selfDeclaredMadeForKids": False,
                   "containsSyntheticMedia": True},
    }
    at = os.environ.get("MANUAL_PUBLISH_AT") or spec.get("publish", {}).get("at")
    if at:  # agendado: o YouTube exige private + publishAt (ISO 8601 UTC)
        meta["status"]["privacyStatus"] = "private"
        meta["status"]["publishAt"] = at
        privacy = f"agendado para {at}"
    size = os.path.getsize(video)
    init = urllib.request.Request(
        "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
        data=json.dumps(meta).encode(), method="POST",
        headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json; charset=UTF-8",
                 "X-Upload-Content-Length": str(size), "X-Upload-Content-Type": "video/mp4"})
    try:
        loc = urllib.request.urlopen(init).headers["Location"]
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:800]
        print("upload init falhou:", e.code, body)
        import re as _re
        reason = _re.findall(r'"reason":\s*"([^"]+)"', body)
        print(f"::error title=upload::{e.code} {','.join(reason) or body[:200].replace(chr(10), ' ')}")
        raise
    up = urllib.request.Request(loc, data=open(video, "rb").read(), method="PUT",
                                headers={"Content-Type": "video/mp4", "Content-Length": str(size)})
    res = json.load(urllib.request.urlopen(up))
    print("enviado:", res["id"], privacy)
    print(f"::notice title=enviado::{res['id']}")
    open("uploaded.json", "w").write(json.dumps({"id": res["id"], "privacy": privacy}))

if __name__ == "__main__":
    main(*sys.argv[1:5])

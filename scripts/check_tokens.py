"""Smoke test: troca cada refresh token por access token e confirma canal/conta."""
import json, os, sys, urllib.parse, urllib.request

def post(url, data):
    req = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode())
    return json.load(urllib.request.urlopen(req))

def get(url, token):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    return json.load(urllib.request.urlopen(req))

def access(refresh):
    r = post("https://oauth2.googleapis.com/token", {
        "client_id": os.environ["YT_CLIENT_ID"],
        "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": refresh, "grant_type": "refresh_token"})
    return r["access_token"]

ok = True
for name in ("YT_REFRESH_A", "YT_REFRESH_B"):
    try:
        t = access(os.environ[name])
        ch = get("https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true", t)
        print(name, "->", [i["snippet"]["title"] for i in ch.get("items", [])])
    except Exception as e:
        ok = False; print(name, "FALHOU", e)
try:
    t = access(os.environ["GDRIVE_REFRESH"])
    d = get("https://www.googleapis.com/drive/v3/about?fields=user(emailAddress)", t)
    print("GDRIVE_REFRESH ->", d["user"]["emailAddress"])
except Exception as e:
    ok = False; print("GDRIVE_REFRESH FALHOU", e)
sys.exit(0 if ok else 1)

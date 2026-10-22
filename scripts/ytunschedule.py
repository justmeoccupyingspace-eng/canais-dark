"""Tira o agendamento (publishAt) de vídeos privados com erro, mantendo-os privados para o dono apagar. Uso: IDS=id1,id2"""
import json, os, urllib.parse, urllib.request
def post(url, data):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, data=urllib.parse.urlencode(data).encode())))
def call(method, url, tok, body=None):
    req = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body else None,
                                 headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))
ch = os.environ.get("CH", "B")
tok = post("https://oauth2.googleapis.com/token", {"client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"], "refresh_token": os.environ[f"YT_REFRESH_{ch}"], "grant_type": "refresh_token"})["access_token"]
for vid in os.environ["IDS"].split(","):
    v = call("GET", f"https://www.googleapis.com/youtube/v3/videos?part=status,snippet&id={vid}", tok)["items"][0]
    st = v["status"]; print(vid, v["snippet"]["title"], st.get("privacyStatus"), st.get("publishAt"))
    if st.get("privacyStatus") != "private":
        print("  não é privado, nada feito"); continue
    body = {"id": vid, "status": {"privacyStatus": "private", "embeddable": st.get("embeddable", True), "license": st.get("license", "youtube"),
                                  "publicStatsViewable": st.get("publicStatsViewable", True), "selfDeclaredMadeForKids": st.get("madeForKids", False)}}
    r = call("PUT", "https://www.googleapis.com/youtube/v3/videos?part=status", tok, body)
    print("  agora:", r["status"].get("privacyStatus"), r["status"].get("publishAt"))

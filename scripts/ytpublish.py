"""Publica já (público) vídeos que estavam agendados (privado + publishAt). Uso: IDS=id1,id2 CH=A|B"""
import json, os, urllib.parse, urllib.request
def post(url, data):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, data=urllib.parse.urlencode(data).encode())))
def call(method, url, tok, body=None):
    req = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body else None,
                                 headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))
ch = os.environ.get("CH", "A")
tok = post("https://oauth2.googleapis.com/token", {"client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"], "refresh_token": os.environ[f"YT_REFRESH_{ch}"], "grant_type": "refresh_token"})["access_token"]
for vid in os.environ["IDS"].split(","):
    v = call("GET", f"https://www.googleapis.com/youtube/v3/videos?part=status,snippet,processingDetails&id={vid}", tok)["items"][0]
    st = v["status"]
    print(vid, "|", v["snippet"]["title"], "|", st.get("privacyStatus"), st.get("publishAt"), st.get("uploadStatus"))
    if st.get("uploadStatus") != "processed":
        print(f"::warning title=publish::{vid} ainda não processado ({st.get('uploadStatus')}), nada feito"); continue
    if st.get("privacyStatus") == "public":
        print("  já é público"); continue
    body = {"id": vid, "status": {"privacyStatus": "public", "embeddable": st.get("embeddable", True), "license": st.get("license", "youtube"),
                                  "publicStatsViewable": st.get("publicStatsViewable", True), "selfDeclaredMadeForKids": st.get("madeForKids", False),
                                  "containsSyntheticMedia": st.get("containsSyntheticMedia", True)}}
    r = call("PUT", "https://www.googleapis.com/youtube/v3/videos?part=status", tok, body)
    print(f"::notice title=publish::{vid} agora {r['status'].get('privacyStatus')} (publishAt={r['status'].get('publishAt')})")

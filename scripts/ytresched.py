"""Muda o publishAt de vídeos privados agendados. Uso: IDS=id1,id2 AT=2026-10-30T02:30:00Z,2026-10-30T03:30:00Z CH=A|B"""
import json, os, urllib.parse, urllib.request
def post(url, data):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, data=urllib.parse.urlencode(data).encode())))
def call(method, url, tok, body=None):
    req = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body else None,
                                 headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))
ch = os.environ["CH"]
tok = post("https://oauth2.googleapis.com/token", {"client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"], "refresh_token": os.environ[f"YT_REFRESH_{ch}"], "grant_type": "refresh_token"})["access_token"]
ids, ats = os.environ["IDS"].split(","), os.environ["AT"].split(",")
assert len(ids) == len(ats), "IDS e AT com tamanhos diferentes"
for vid, at in zip(ids, ats):
    st = call("GET", f"https://www.googleapis.com/youtube/v3/videos?part=status&id={vid}", tok)["items"][0]["status"]
    if st.get("privacyStatus") != "private":
        print(f"::warning::{vid} não é privado ({st.get('privacyStatus')}), nada feito"); continue
    body = {"id": vid, "status": {"privacyStatus": "private", "publishAt": at, "embeddable": st.get("embeddable", True), "license": st.get("license", "youtube"),
                                  "publicStatsViewable": st.get("publicStatsViewable", True), "selfDeclaredMadeForKids": st.get("madeForKids", False),
                                  **({"containsSyntheticMedia": st["containsSyntheticMedia"]} if "containsSyntheticMedia" in st else {})}}
    r = call("PUT", "https://www.googleapis.com/youtube/v3/videos?part=status", tok, body)["status"]
    print(f"::notice::{vid} {st.get('publishAt')} -> {r.get('publishAt')}")

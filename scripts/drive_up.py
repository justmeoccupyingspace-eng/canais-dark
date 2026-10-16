"""Envia o mp4 para o Google Drive da conta do projeto (para o canal C, sem API de upload). Uso: python scripts/drive_up.py out/x.mp4"""
import json, os, sys, urllib.parse, urllib.request, uuid

def token():
    d = urllib.parse.urlencode({"client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
                                "refresh_token": os.environ["GDRIVE_REFRESH"], "grant_type": "refresh_token"}).encode()
    return json.load(urllib.request.urlopen(urllib.request.Request("https://oauth2.googleapis.com/token", data=d)))["access_token"]

def main(path):
    b = uuid.uuid4().hex
    meta = json.dumps({"name": os.path.basename(path)}).encode()
    body = (f"--{b}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n").encode() + meta + \
           (f"\r\n--{b}\r\nContent-Type: video/mp4\r\n\r\n").encode() + open(path, "rb").read() + f"\r\n--{b}--".encode()
    req = urllib.request.Request("https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&fields=id,name",
                                 data=body, headers={"Authorization": f"Bearer {token()}", "Content-Type": f"multipart/related; boundary={b}"})
    r = json.load(urllib.request.urlopen(req, timeout=300))
    print("drive ok:", r["name"], r["id"])

if __name__ == "__main__":
    main(sys.argv[1])

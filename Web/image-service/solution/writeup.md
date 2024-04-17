# 解题思路

首先观察到页面最后存在 `www.zip` 的提示，据此获得题目源码。

审计发现 `index.php` 中存在 HTTP 头部直接拼接的情况，同时 `secret.php` 中需要 Cookie 存在 `admin=true` 的条件才能读取 flag，于是利用 HTTP 头部拼接注入一个 Cookie 头，同时 SSRF 到 `/secret.php` 获取 flag。

详细解题脚本见 [exp.py](./exp.py)
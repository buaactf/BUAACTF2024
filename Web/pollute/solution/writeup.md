# 解题思路

存在两个中间件，第一个中间件对参数进行处理，第二个对参数进行限制：

- 构建一个 `req.files` 对象，将 GET 参数以 `file.` 开头的参数按照键值对映射的方式加入 `req.files` ；
- 对 `req.files` 中的值进行规范化，若以 `/tmp/` 开头则可以读取文件。

这里的目的是绕过 WAF 读取 `/flag` 文件，这里实际上涉及到 `express` 框架对 query string 的解析处理，使用的是 `qs` 这个库（大部分 nodejs Web 框架都是使用这个库），这个库的**一大特点就是会将 query string 解析为 Object 而不只是 string**。

也就是说 `a[b]=1` 是将 Object a 的 b 属性赋值为 `1` ，而不是将 `a[b]` 赋值为 1。

那么我们通过注入 `__proto__` 对象即可控制不含 `File` 属性的 Object 的值来读取任意文件。
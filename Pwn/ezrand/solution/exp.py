from pwn import *
import ctypes
context.log_level='debug'
context.os='linux'
context.arch='amd64'

p=remote('127.0.0.1',9999)
#p=process('./pwn')
libc=ctypes.CDLL("libc.so.6")
libc.srand(libc.time(0))
for i in range(100):
    p.sendlineafter(b'Your number: ',str(libc.rand()).encode())

p.interactive()

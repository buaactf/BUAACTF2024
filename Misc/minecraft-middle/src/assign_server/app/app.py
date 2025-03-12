import json
from hashlib import sha256
import socketserver
import string
import random
import os
import subprocess
import time
import uuid

MENU = br'''[+] Please Choose from the options below:
[+] 1.show available bots
[+] 2.choose bot
[+] 3.exit
'''
BOTS = ['xiaoJ_0', 'xiaoJ_1', 'xiaoJ_2', 'xiaoJ_3', 'xiaoJ_4']
AVAILABLE_BOTS = []
PASSWORD = 'xiaoj20240418'


def init_bots():
    global AVAILABLE_BOTS
    for bot_info in BOTS:
        AVAILABLE_BOTS.append({'username': bot_info, 'available': True})


def server_address_check(address: str):
    if not address.isprintable():
        return False
    if ' ' in address:
        return False
    if not address.isascii():
        return False
    if address.count(':') > 1:
        return False
    return True


class Screen:
    def __init__(self, screen_name: str):
        self.screen_name = screen_name
        self.create_screen()

    def create_screen(self):
        create_screen_cmd = ['screen', '-dmS', self.screen_name]
        subprocess.call(create_screen_cmd)

    def sendline(self, cmd: str):
        cmd_screen = ['screen', '-x', '-S', self.screen_name, '-p', '0', '-X', 'stuff', cmd + '\n']
        subprocess.call(cmd_screen)

    def quit(self):
        cmd = ['screen', '-S', self.screen_name, '-X', 'quit']
        subprocess.call(cmd)


class Bot:
    def __init__(self, username: str, server_addr: str):
        self.screen_name = 's-' + uuid.uuid4().hex
        self.screen = Screen(self.screen_name)
        self.server_addr = server_addr
        self.username = username

    def run(self):
        global PASSWORD
        print(f'Bot {self.username} trying to join {self.server_addr}')
        time.sleep(1)
        self.screen.sendline(f'./MinecraftClient {self.username} - {self.server_addr}')
        time.sleep(5)
        self.screen.sendline(f"/execif \"MCC.GetGamemode()!=2\" \"quit\" ")
        time.sleep(1)
        self.screen.sendline('/send /help')
        time.sleep(1)
        self.screen.sendline(f'/send /l {PASSWORD}')
        time.sleep(5)
        self.screen.sendline('/quit')
        time.sleep(2)
        self.screen.sendline('')
        self.screen.sendline('')
        self.screen.sendline('')
        time.sleep(5)
        self.screen.quit()


class Task(socketserver.BaseRequestHandler):
    def _recvall(self):
        BUFF_SIZE = 2048
        data = b''
        while True:
            part = self.request.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data.strip()

    def send(self, msg, newline=True):
        try:
            if newline:
                msg += b'\n'
            self.request.sendall(msg)
        except:
            pass

    def recv(self, prompt=b'[-] '):
        self.send(prompt, newline=False)
        return self._recvall()

    def recvline(self, prompt=b'[-] '):
        self.send(prompt, newline=False)
        data = b''
        while True:
            part = self.request.recv(1)
            if part == b'\n':
                break
            data += part
        return data.strip()

    def proof_of_work(self):
        random.seed(os.urandom(8))
        proof = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(20)])
        _hexdigest = sha256(proof.encode()).hexdigest()
        self.send(f"[+] sha256(XXXX+{proof[4:]}) == {_hexdigest}".encode())
        try:
            x = self.recv(prompt=b'[+] Plz tell me XXXX: ')
        except ConnectionResetError:
            return False
        if len(x) != 4 or sha256(x + proof[4:].encode()).hexdigest() != _hexdigest:
            return False
        return True

    def handle(self):
        global AVAILABLE_BOTS
        if not self.proof_of_work():
            return
        self.send(MENU, newline=False)
        while True:
            try:
                choice = self.recvline()
            except ConnectionResetError:
                break
            if choice == b'1':
                self.send(str(json.dumps(AVAILABLE_BOTS, indent=4)).encode())
            elif choice == b'2':
                self.send(b'[+] Please input your server address (e.g. 0.0.0.0:25565)')
                data = self.recvline()
                server_addr = data.decode(errors='ignore').strip()
                if server_address_check(server_addr):
                    self.send(f'[+] Your server address is {server_addr}'.encode())
                else:
                    self.send(f'[+] Wrong address format'.encode())
                    continue
                self.send(b'[+] Choose bot')
                for index, bot in enumerate(AVAILABLE_BOTS):
                    if bot['available']:
                        self.send(f"[+] {index}: {bot['username']}".encode())
                try:
                    bot_choice = int(self.recvline().decode(errors='ignore'))
                except ConnectionResetError:
                    break
                except ValueError:
                    bot_choice = -1
                if bot_choice < 0 or bot_choice >= len(AVAILABLE_BOTS):
                    self.send(f"[+] Wrong input".encode())
                elif AVAILABLE_BOTS[bot_choice]['available']:
                    AVAILABLE_BOTS[bot_choice]['available'] = False
                    bot_info = AVAILABLE_BOTS[bot_choice]
                    self.send(b'[+] The process will last for approximately 30 seconds')
                    self.send(b'[+] Trying to join your server...')
                    bot = Bot(bot_info['username'], server_addr)
                    bot.run()
                    del bot
                    self.send(b'[+] Finished.')
                    AVAILABLE_BOTS[bot_choice]['available'] = True
                    break
                else:
                    self.send(f"[+] The {AVAILABLE_BOTS[bot_choice]['username']} bot is unavailable!".encode())
            elif choice == b'3':
                break
            else:
                self.send(MENU, newline=False)
        self.request.close()

    def finish(self):
        print('Thread finished')


class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ForkedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    init_bots()
    HOST, PORT = '0.0.0.0', 25553
    server = ThreadedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()

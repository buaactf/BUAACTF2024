import code, os, subprocess
import pty

BANNER=''' /$$      /$$ /$$     /$$ /$$$$$  /$$$$$$  /$$$$$$ /$$      
| $$$    /$$$|  $$   /$$/|__  $$ /$$__  $$|_  $$_/| $$      
| $$$$  /$$$$ \  $$ /$$/    | $$| $$  \ $$  | $$  | $$      
| $$ $$/$$ $$  \  $$$$/     | $$| $$$$$$$$  | $$  | $$      
| $$  $$$| $$   \  $$/ /$$  | $$| $$__  $$  | $$  | $$      
| $$\  $ | $$    | $$ | $$  | $$| $$  | $$  | $$  | $$      
| $$ \/  | $$    | $$ |  $$$$$$/| $$  | $$ /$$$$$$| $$$$$$$$
|__/     |__/    |__/  \______/ |__/  |__/|______/|________/

[+] 1.show code
[+] 2.enter the challenge 
[+] 3.exit
'''

SRC_CODE=open('src.py','r').read()

def blacklist_fun_callback(*args):
    return "Player! It's already banned!"


pty.spawn = blacklist_fun_callback
os.system = blacklist_fun_callback
os.popen = blacklist_fun_callback
subprocess.Popen = blacklist_fun_callback
subprocess.call = blacklist_fun_callback
code.interact = blacklist_fun_callback
code.compile_command = blacklist_fun_callback

vars = blacklist_fun_callback
attr = blacklist_fun_callback
dir = blacklist_fun_callback
getattr = blacklist_fun_callback
exec = blacklist_fun_callback
__import__ = blacklist_fun_callback
compile = blacklist_fun_callback
breakpoint = blacklist_fun_callback
open=blacklist_fun_callback

del os, subprocess, code, pty, blacklist_fun_callback

blacklist_words_var_name_fake_in_local_real_in_remote = [
    "*",
    "+",
    "len",
    "open",
    "write",
    "read",
    "update",
    "lambda",
    "dict",
    "listdir",
    "globals",
    "subprocess",
    "os",
    "code",
    "interact",
    "pty",
    "pdb",
    "platform",
    "importlib",
    "timeit",
    "imp",
    "commands",
    "popen",
    "load_module",
    "spawn",
    "system",
    "/bin/sh",
    "/bin/bash",
    "flag",
    "eval",
    "exec",
    "compile",
    "input",
    "vars",
    "attr",
    "dir",
    "getattr",
    "__import__",
    "__mro__",
    "__builtins__",
    "__getattribute__",
    "__class__",
    "__base__",
    "__subclasses__",
    "__getitem__",
    "__self__",
    "__globals__",
    "__init__",
    "__name__",
    "__dict__",
    "._module",
    "builtins",
    "breakpoint",
    "import",
]


def my_filter(input_code):
    for x in blacklist_words_var_name_fake_in_local_real_in_remote:
        if x in input_code:
            return False
    return True


print(BANNER)
while True:
    try:
        input_code = int(input("Your choice > "))
    except EOFError:
        exit()
    if input_code==1:
        print(SRC_CODE)
    elif input_code==2:
        print("Can u input your code to escape ?")
        while True:
            try:
                input_code = input("> ")
            except EOFError:
                exit()
            if input_code.isascii() and my_filter(input_code) and "eval" not in input_code and len(input_code) < 60:
                try:
                    eval(input_code)
                except Exception:
                    print('Exec failed!')
            else:
                print("Player! Please obey the filter rules which I set!")
    elif input_code==3:
        exit()
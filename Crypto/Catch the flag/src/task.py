from Crypto.Util.number import bytes_to_long
import os, signal
import sys
import random

BITS = 128

class CTF(object):
    def __init__(self) -> None:
        self.seed = bytes_to_long(os.urandom(BITS//8))
        self.luck = 0
        self.score = 0
    
    def get_input(self, prompt="> "):
        print(prompt, end="")
        sys.stdout.flush()
        return input()
    

    def check_pos(self, pos, steps):
        col, row = 0, 0
        for move in steps:
            if move == "W":
                if row < 15: row += 1
            elif move == "S":
                if row > 0: row -= 1
            elif move == "A":
                if col > 0: col -= 1
            elif move == "D":
                if col < 15: col += 1
            else:
                return -1
        print(col, row)
        return pos == [col, row]


    def fortune_catch(self, d):
        b = bin(d)[2:]
        l = len(b)
        if l < 128+self.luck:
            b += "0"*(128+self.luck - l)
        if random.choice(b)=='0': return True
        else: return False
    
    def run(self):
        pos = [random.randrange(1,16), random.randrange(1,16)]
        steps = self.get_input(f"flag is at {pos}, catch it.\nYour steps: ")
        if len(steps) > 100:
            print("you out of range")
            return
        
        allowed_chars = {'W', 'S', 'D', 'A'}
        for char in steps:
            if char not in allowed_chars:
                raise ValueError

        if not self.check_pos(pos, steps):
            print("sorry, caught nothing")
            return
        
        s = random.randint(2**(BITS-1),2**BITS)
        print(f"rand: {s}")

        i, j = map(int, self.get_input(f"give me your catch using i,j and i,j in [0, 18446744073709551615] (e.g.: 1,1): ").split(","))
        if not (i>0 and i<pow(2,BITS//2) and j>0 and j<pow(2,BITS//2)):
            print("not in range")
            return
        
        d = abs(s*j - i*2**BITS)
        if self.fortune_catch(d):
            self.score += 10
            self.luck = 0
            print("you caught it")
        else:
            self.luck += 16
            print("sorry, caught nothing")
        

def main():
    signal.alarm(600)
    PROCESS = CTF()
    for _ in range(256):
        try:
            PROCESS.run()
            print(f"your score: {PROCESS.score}")
        except:
            print(f"something error")
            break
    if PROCESS.score >= 2220:
        print(f"flag: {open('flag.txt').read()}")
        
if __name__ == "__main__":
    main()
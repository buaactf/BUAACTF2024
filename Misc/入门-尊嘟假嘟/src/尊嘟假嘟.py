import base64
import itertools
import random

EYES=['0','O','o','@']
MOUTHS=['_','.','v','w']
B64_TABLE="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
FLAG="BUAACTF{F0r_r3al?_o.O_O.O_O.o_o.o}"
def init_table(eyes:list,mouths:list):
    l1=eyes
    l2=mouths
    random.shuffle(l1)
    random.shuffle(l2)
    return [''.join(i) for i in list(itertools.product(l1,l2,l1))]

if __name__ == '__main__':
    table=init_table(EYES,MOUTHS)
    flag=f"I love you, Dexter. So much. I just don't like you anymore.You got a dream, you gotta protect it. People can't do something themselves, they wanna tell you you can't do it. If you want something, go get it.Life was like a box of chocolates, you never know what you're gonna get.Is life always this hard. Or is it just when you're a kid?Always like this.{FLAG}"
    b64_flag=base64.b64encode(flag.encode()).decode()
    encoded_flag=[]
    for i in b64_flag.strip('='):
        num=B64_TABLE.index(i)
        encoded_flag.append(table[num])
    print(' '.join(encoded_flag))
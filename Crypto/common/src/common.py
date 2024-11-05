from Crypto.Util.number import *
from secret import flag

n = 1000
gamma = 0.42
beta = 0.25


def keyGen(n, gamma):
    g = getPrime(round(n * gamma))
    while True:
        a, b = 2, 2
        while GCD(a, b) != 1:
            a = getRandomNBitInteger(round((.5 - gamma) * n - 1))
            b = getRandomNBitInteger(round((.5 - gamma) * n - 1))
        p, q, h = 2 * g * a + 1, 2 * g * b + 1, 2 * g * a * b + a + b
        if isPrime(p) and isPrime(q) and isPrime(h):
            break
    return p, q, g, a, b


p, q, g, a, b = keyGen(n, gamma)
print(p, q, g, a, b)
m = bytes_to_long(flag)
d = getPrime(round(n * beta))
e = inverse(d, 2 * g * a * b)
print(f'N = {hex(p * q)}')
print(f'e = {hex(e)}')
print(f"C = {hex(pow(m,e,p*q))}")

# N = 0x5c8a8f1a91bc985ea43564d74adb7571d188f5a4564400fe7303b8b1e108f155fea541f255a3d3b22610ed31de7cd8e01199cd3364572a554704eb1427c651efd4899a1567dab720092b3a731634f03fa312fe97b37c4437381dec2ad4352c7ba2f4b8073e6d6e8242baae119df5ba8bd30ed17a0cfc520e2b4ec33d67
# e = 0xe17fe8d3a6025922083a12ed11f3acb03e2887e6507f35f397b5c10afb9b39cec8fc0201bfc6e7f0d96372655f9b17fa400ab441a383905cf5dbb87fabdec02a0c1c8bc9ddd5b3cd
# c = 0x5eeab18ec326f3820f6d4c3fc40a4b4d252fd71a17aa70f8df02c75af2630fbc2f67e29df37ec7da302f54acc55b5489986a497dd68997b4290e8ec09108faf67c89b19fe4b8be317a9b2c107caaf60e8bde46e7991df4ede89bf9f65cf42a4d724b5896a9048109a317b134212141cba35d836a62468c55bd0a58c44

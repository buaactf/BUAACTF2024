flag = [0x41415542, 0x7b465443, 0x5f376553, 0x654d6937, 0x6e495f52, 0x56524537, 0x465f6c34, 0x4d5f5230, 0x34475f79,
        0x007d654d]
sum = 0
delta = 0x9e3779b9
key = [0x1234, 0x4321, 0x12345678, 0x87654321]


def tea_encrypt():
    global sum
    global delta
    global flag
    global key
    for i in range(9):
        v0 = flag[i]
        v1 = flag[i + 1]
        sum += delta
        sum = sum & 0xFFFFFFFF
        v0 += ((v1 << 4) + key[i % 4]) ^ (v1 + sum) ^ ((v1 >> 5) + key[(i + 1) % 4])
        v0 = v0 & 0xFFFFFFFF
        v1 += ((v0 << 4) + key[(i + 2) % 4]) ^ (v0 + sum) ^ ((v0 >> 5) + key[(i + 3) % 4])
        v1 = v1 & 0xFFFFFFFF
        flag[i] = v0 & 0xFFFFFFFF
        flag[i + 1] = v1 & 0xFFFFFFFF


def tea_decrypt():
    global sum
    global delta
    global flag
    global key
    for i in range(8, -1, -1):
        v0 = flag[i]
        v1 = flag[i + 1]
        v1 -= ((v0 << 4) + key[(i + 2) % 4]) ^ (v0 + sum) ^ ((v0 >> 5) + key[(i + 3) % 4])
        v1 = v1 & 0xFFFFFFFF
        v0 -= ((v1 << 4) + key[i % 4]) ^ (v1 + sum) ^ ((v1 >> 5) + key[(i + 1) % 4])
        v0 = v0 & 0xFFFFFFFF
        sum -= delta
        sum = sum & 0xFFFFFFFF
        flag[i] = v0 & 0xFFFFFFFF
        flag[i + 1] = v1 & 0xFFFFFFFF


def xtea_encrypt():
    global sum
    global delta
    global flag
    global key
    for i in range(9):
        v0 = flag[i]
        v1 = flag[i + 1]
        sum += delta
        sum = sum & 0xFFFFFFFF
        v0 += (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + key[sum & 3])
        v0 = v0 & 0xFFFFFFFF
        v1 += (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + key[(sum >> 11) & 3])
        v1 = v1 & 0xFFFFFFFF
        flag[i] = v0 & 0xFFFFFFFF
        flag[i + 1] = v1 & 0xFFFFFFFF


def xtea_decrypt():
    global sum
    global delta
    global flag
    global key
    for i in range(8, -1, -1):
        v0 = flag[i]
        v1 = flag[i + 1]
        v1 -= (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + key[(sum >> 11) & 3])
        v1 = v1 & 0xFFFFFFFF
        v0 -= (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + key[sum & 3])
        v0 = v0 & 0xFFFFFFFF
        sum -= delta
        sum = sum & 0xFFFFFFFF
        flag[i] = v0 & 0xFFFFFFFF
        flag[i + 1] = v1 & 0xFFFFFFFF


if __name__ == '__main__':

    GAME_MAX_TIME = 15000
    ENEMY_MAX_RATE = 200
    ENEMY_MIN_RATE = 100
    decstr = ''
    count = 0
    while True:
        count += 20
        if count == GAME_MAX_TIME:
            break
        decstr += '1'
        enemy_rate = int(ENEMY_MIN_RATE + (ENEMY_MAX_RATE - ENEMY_MIN_RATE) * (count / GAME_MAX_TIME));
        if count % (1000 // enemy_rate) == 0:
            decstr += '2'
    for i in decstr[::-1]:
        if i == '1':
            tea_encrypt()
        else:
            xtea_encrypt()
    print('flag[10] :', end='')
    for i in flag:
        print(hex(i), end=', ')
    print()
    print('sum: ', hex(sum))

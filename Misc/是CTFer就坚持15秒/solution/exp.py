flag = [0x47a43c8e, 0x478be9f1, 0x770c8898, 0x2e9c2e34, 0xabed8447, 0xdafa9db7, 0xef243266, 0xf7fd15bc, 0x4b6e6914, 0x2f08d53c]
sum = 0x47278878
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
        tea_decrypt()
        enemy_rate = int(ENEMY_MIN_RATE + (ENEMY_MAX_RATE - ENEMY_MIN_RATE) * (count / GAME_MAX_TIME));
        if count % (1000 // enemy_rate) == 0:
            xtea_decrypt()
    flag_str=b''
    for i in flag:
        flag_str+=int.to_bytes(i,4,'little')
    print(flag_str)
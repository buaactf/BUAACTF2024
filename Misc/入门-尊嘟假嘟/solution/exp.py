import base64
import itertools

EYES = ['0', 'O', 'o', '@']
MOUTHS = ['_', '.', 'v', 'w']
B64_TABLE = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
if __name__ == '__main__':
    f = open('chal', 'r')
    data = f.read().strip().split()
    eyes_permutations_list = list(itertools.permutations(EYES))
    mouths_permutations_list = list(itertools.permutations(MOUTHS))
    for eyes_table in eyes_permutations_list:
        for mouths_table in mouths_permutations_list:
            b64_str = ''
            for face in data:
                index = eyes_table.index(face[0]) * 16 + mouths_table.index(face[1]) * 4 + eyes_table.index(face[2])
                b64_str += B64_TABLE[index]
            if b'BUAA' in base64.b64decode(b64_str):
                print(base64.b64decode(b64_str))

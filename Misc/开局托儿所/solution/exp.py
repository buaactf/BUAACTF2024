import copy
import time

import requests
import os

TEMPLATE = '''const seedrandom = require('seedrandom');
seedrandom('$seed', { global: true });
for(let i=0; i<160; i++){
    let rnd=Math.trunc(Math.random()*9)+1;
    console.log(rnd);
}
'''
API_URL = "http://101.132.64.144:3001"
ROW_NUM = 16
COL_NUM = 10


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return str((self.x, self.y))


class BlockMap:
    def __init__(self, block_list):
        self.list = block_list
        self.map = [block_list[i * COL_NUM:i * COL_NUM + COL_NUM] for i in range(ROW_NUM)]
        self.score = 0

    def clear(self, start_pos: Pos, end_pos: Pos):
        for y in range(min(start_pos.y, end_pos.y), max(start_pos.y, end_pos.y) + 1):
            for x in range(min(start_pos.x, end_pos.x), max(start_pos.x, end_pos.x) + 1):
                self.map[y][x] = 0

    def __str__(self):
        return str(self.map)

    def cal_sum(self, start_pos: Pos, end_pos: Pos):
        sum = 0
        for y in range(min(start_pos.y, end_pos.y), max(start_pos.y, end_pos.y) + 1):
            for x in range(min(start_pos.x, end_pos.x), max(start_pos.x, end_pos.x) + 1):
                sum += self.map[y][x]
        #print(start_pos, end_pos, sum)
        return sum

    def cal_block_num(self, start_pos: Pos, end_pos: Pos):
        num = 0
        for y in range(min(start_pos.y, end_pos.y), max(start_pos.y, end_pos.y) + 1):
            for x in range(min(start_pos.x, end_pos.x), max(start_pos.x, end_pos.x) + 1):
                if self.map[y][x] != 0:
                    num += 1
        return num

    def search_for_clear(self):  # 深度优先搜索，先消除数字比较大的
        block_num = self.cal_block_num(Pos(0, 0), Pos(COL_NUM - 1, ROW_NUM - 1))
        clear_list = []
        if block_num <= 50:  # 数量少的时候直接遍历
            for index1 in range(len(self.list)-1):
                if self.list[index1] == 0:
                    continue
                for index2 in range(index1+1,len(self.list)):
                    if self.list[index2] == 0:
                        continue
                    start_pos = Pos(index1%COL_NUM,index1//COL_NUM)
                    end_pos = Pos(index2%COL_NUM,index2//COL_NUM)
                    if self.cal_sum(start_pos, end_pos) == 10:
                        block_num = self.cal_block_num(start_pos, end_pos)
                        clear_list.append({'start_pos': start_pos, 'end_pos': end_pos, 'block_num': block_num})
            #clear_list.sort(key=lambda x: x['block_num'],reverse=True)
        else:  # 数量多的时候进行DFS
            for y, block_row in enumerate(self.map):
                for x, block in enumerate(block_row):
                    suc, start_pos, end_pos = self.dfs(Pos(x, y), Pos(x, y), block)
                    if suc:
                        #return True, start_pos, end_pos
                        block_num = self.cal_block_num(start_pos, end_pos)
                        clear_list.append({'start_pos': start_pos, 'end_pos': end_pos, 'block_num': block_num})
        clear_list.sort(key=lambda x: x['block_num'])
        if clear_list:
            return True, clear_list[0]['start_pos'], clear_list[0]['end_pos']
        return False, Pos(0, 0), Pos(0, 0)

    def dfs(self, start_pos: Pos, end_pos: Pos, sum: int):
        if sum == 10:
            return True, start_pos, end_pos
        if sum > 10:
            return False, start_pos, end_pos

        if end_pos.x + 1 < COL_NUM:
            new_pos = Pos(end_pos.x + 1, end_pos.y)
            new_sum = self.cal_sum(start_pos, new_pos)
            suc, new_start_pos, new_end_pos = self.dfs(start_pos, new_pos, new_sum)
            if suc:
                return suc, new_start_pos, new_end_pos
        if end_pos.y + 1 < ROW_NUM:
            new_pos = Pos(end_pos.x, end_pos.y + 1)
            new_sum = self.cal_sum(start_pos, new_pos)
            suc, new_start_pos, new_end_pos = self.dfs(start_pos, new_pos, new_sum)
            if suc:
                return suc, new_start_pos, new_end_pos
        return False, start_pos, end_pos


def generate_block_list(seed):
    global TEMPLATE
    block_list = []
    f = open('tmp.js', 'w')
    f.write(TEMPLATE.replace('$seed', seed))
    f.close()
    result = os.popen("node tmp.js").readlines()
    for line in result:
        block_list.append(int(line))
    os.remove("tmp.js")
    return block_list


if __name__ == '__main__':
    while True:
        rep = requests.get(f'{API_URL}/api/newgame')
        id = rep.json()['id']
        seed = rep.json()['seed']
        block_list = generate_block_list(seed)
        block_map = BlockMap(block_list)
        #print(block_map)
        while True:
            suc, pos1, pos2 = block_map.search_for_clear()
            if not suc:
                break
            rep = requests.post(f'{API_URL}/api/clear',
                                json={'id': id, 'selected': [{'x': pos1.x, 'y': pos1.y}, {'x': pos2.x, 'y': pos2.y}]})
            block_map.clear(pos1, pos2)
        rep = requests.post(f'{API_URL}/api/finishgame', json={'id': id})
        print(rep.json())
        time.sleep(0.5)

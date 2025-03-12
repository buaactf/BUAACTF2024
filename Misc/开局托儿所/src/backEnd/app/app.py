import copy
import hashlib
import os
import time
import uuid
from flask import Flask, request
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
app = Flask(__name__)
CORS(app, resources=r'/api/*', supports_credentials=True)
games = {}
ranks = [{'tag':'max','num':0}]

#工作目录下记得安装seedrandom
template = '''const seedrandom = require('seedrandom');
seedrandom('$seed', { global: true });
for(let i=0; i<160; i++){
    let rnd=Math.trunc(Math.random()*9)+1;
    console.log(rnd);
}
'''
TIME_LIMIT = 65
SCORE_LIMIT = 130
FLAG = 'BUAACTF{B48Y_t0_8U443r_t0_C7F3R_t0_S3cUR17Y_Pr0}'
ROW_NUM = 16
COL_NUM = 10
TAG_TABLE = {
    "新生儿": 30,
    "幼儿园": 60,
    "小学": 70,
    "初中": 80,
    "高中": 90,
    "大学": 100,
    "入门CTFer": 110,
    "初级CTFer": 120,
    "平平无奇CTFer": 130,
    "小有成就CTFer": 140,
    "大有所为CTFer": 150,
    "安全领域大牛": 160
}

for i in TAG_TABLE.keys():
    ranks.append({'tag': i, 'num': 0})  # {'score':100,'num':100}


def get_tag(score: int):
    global TAG_TABLE
    for tag, top_score in TAG_TABLE.items():
        if score < top_score:
            return tag


def clear_games():
    global games
    #print(games)
    for game_id, content in list(games.items()):
        if time.time() - int(content['timestamp']) > TIME_LIMIT:
            games.pop(game_id)


def generate_block_list(game_id, seed):
    block_list = []
    f = open(game_id + '.js', 'w')
    f.write(template.replace('$seed', seed))
    f.close()
    result = os.popen(f"node {game_id}.js").readlines()
    for line in result:
        block_list.append(int(line))
    os.remove(f"{game_id}.js")
    return block_list


scheduler.add_job(func=clear_games, id="job_1", trigger="interval", seconds=60, replace_existing=False)


@app.route('/api/newgame', methods=['GET'])
def new_game():
    global games
    global template
    game_id = str(uuid.uuid4())
    seed = hashlib.sha256(game_id.encode()).hexdigest()
    timestamp = int(time.time())
    block_list = generate_block_list(game_id, seed)
    #print(block_list)
    response_data = {'id': game_id, 'seed': seed, 'timestamp': timestamp}
    games[game_id] = {'seed': seed, 'block_list': block_list, 'timestamp': timestamp}
    return response_data


@app.route('/api/clear', methods=['POST'])
def clear():
    global games
    req_data = request.json
    #print(req_data)
    game_id = req_data['id']
    if int(time.time()) - games[game_id]['timestamp'] > TIME_LIMIT:
        return {'message': 'overtime'}
    block_list = copy.copy(games[game_id]['block_list'])
    x1, y1 = req_data['selected'][0]['x'], req_data['selected'][0]['y']
    x2, y2 = req_data['selected'][1]['x'], req_data['selected'][1]['y']
    sum = 0
    index_list = []
    for y in range(min(y1, y2), max(y1, y2) + 1):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            index = y * COL_NUM + x
            index_list.append(index)
            sum += block_list[index]
    if sum == 10:
        for index in index_list:
            block_list[index] = 0
        games[game_id]['block_list'] = copy.copy(block_list)
        return {'message': 'success'}
    return {'message': 'failed'}


@app.route('/api/finishgame', methods=['POST'])
def finish_game():
    global games
    global ranks
    req_data = request.json
    game_id = req_data['id']
    block_list = games[game_id]['block_list']
    score = 0
    for i in block_list:
        if i == 0:
            score += 1
    tag = get_tag(score)
    if score > ranks[0]['num']:
        ranks[0]['num']=score
    for i in range(len(ranks)):
        if ranks[i]['tag'] == tag:
            ranks[i]['num'] += 1
            break
    games.pop(game_id)
    if score >= SCORE_LIMIT:
        return {'score': score, 'tag': tag, 'flag': FLAG}
    return {'score': score, 'tag': tag}


@app.route('/api/getranks', methods=['GET'])
def get_ranks():
    global ranks
    return ranks


if __name__ == '__main__':
    scheduler.start()  # 启动任务列表
    app.run(host='0.0.0.0', port=3001)

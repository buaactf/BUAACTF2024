const maxTimeNum = 60;
const ColNum = 10;
const RowNum = 16;
const BlockGap =10;
const FontSize = '20px';
const ApiUrl='http://127.0.0.1:3001'
const BackGroundMusic=new Audio('static/bgm.mp3');
const GameOverMusic =new Audio('static/gameover.mp3');
  /**
   * 页面的初始数据
   */
const data={
    progressPercent:100,
    timerNum:maxTimeNum,
    score:0,
    digitList:[],
    oldPosition:{},
      isDraw:false,

};
/**
* 生命周期函数--监听页面加载
*/
function initData(){
    data.score=0;
    document.getElementById('score').textContent=`你的分数：${data.score}`;
    data.timerNum=maxTimeNum;
    data.progressPercent=100;
    if(data.timer){
        clearInterval(data.timer);
    }

    console.log('initData')
    const canvas = document.getElementById('canv');
    let canvasData;
    canvasData = {
        canvas,
        context: canvas.getContext('2d'),
        columns: ColNum,
        rows: RowNum
    };
    data.digitList = [1, 2, 3, 4, 5, 6, 7, 8, 9];  // 启用的数字列表
    initAudioPlay();

    return new Promise((resolve, reject) => {
        initCanvasData(canvasData).then(function (){
            data.timer = setInterval(() => {
                let num = data.timerNum - 1;
                if (num < 0) {
                    clearInterval(data.timer);
                    data.timer = null;
                    gameOver();
                    return;
                }
                data.timerNum=num;
                data.progressPercent=Math.trunc(num * 100 / maxTimeNum);
                document.getElementById("time-bar").style.width=`${num/maxTimeNum*100}%`;
                document.getElementById("time-bar").textContent=`${num}s`;
            }, 1000);
            clearCanvas(true);
            drawBlocks();
            resolve('suc');
        });
    });
}

/**
 * 生命周期函数--监听页面卸载
 */
function onUnload() {
    if(data.timer){
        clearInterval(data.timer);
    }
    if(data.audioPlay && data.audioPlay.destroy){
        data.audioPlay.destroy();
    }
}

function gameOver() {
    fetch(`${ApiUrl}/api/finishgame`,{
        method:'POST',
        headers: {
            'Content-Type': 'application/json' // 设置请求的Content-Type
        },
        body:JSON.stringify({'id':data.id})})
        .then(response=>response.json())
        .then(data =>{
            document.getElementById('tag').textContent=`当前称号：${data.tag}`;
            if(data.flag){
                alert(data.flag);
            }
        });
    clearCanvas(true);
    const {context,canvas}=data.canvasData;
    context.font = `60px 黑体`;
    context.fillStyle='#FFFFFF';
    context.fillText('GameOver',canvas.width/2-60*4,canvas.height/2);
    data.canvasData.canvas.onmousedown=undefined;
    data.canvasData.canvas.onmousemove=undefined;
    data.canvasData.canvas.onmouseup=undefined;
    data.music.pause();
    GameOverMusic.play();
    GameOverMusic.loop=false;
}

function initCanvasData(canvasData) {
    const { canvas, columns, rows } = canvasData;
    let padding = 1;
    const bgColor = '#000';
    const lineColor = '#ff3';
    const { width } = canvas;
    padding += Math.trunc((width-padding*2)%columns/2);
    const blockSize = Math.trunc((width-padding*2-BlockGap*ColNum)/columns);
    const blockList = [];
    return new Promise((resolve, reject) => {
        initSeed().then((seed)=>{
            for(let row=0; row<rows; row++){
                for(let col=0; col<columns; col++){
                    let block = createNewBlock(col,row);
                    blockList.push(block);
                }
            }
            const selectedBlockList = [];
            Object.assign(canvasData, { bgColor, lineColor, blockList, blockSize, padding, columns, rows, selectedBlockList });
            //console.log(canvasData);
            data.canvasData = canvasData;
            resolve('suc');
        });
    });
}

function initAudioPlay() {
    const music=BackGroundMusic;
    music.play();
    music.loop=true;
    data.music=music;
}

//从api获取种子
function initSeed(){
    return new Promise((resolve, reject) => {
        fetch(`${ApiUrl}/api/newgame`,{method:'GET'}).then(response=>response.json()).then(rep_data=>{
            data.seed=rep_data.seed;
            data.id=rep_data.id;
            Math.seedrandom(data.seed, { global: true });
            resolve('suc');
        });
    });
}

function getRandomDigit(){
    let rnd=Math.trunc(Math.random()*9)+1;
    return rnd
}

function getBlockCoordinate(block){
    const { blockSize, padding } = data.canvasData;
    return {
        left: block.x*(blockSize+BlockGap)+block.left+padding+BlockGap/2,
        top: block.y*(blockSize+BlockGap)+block.top+padding+BlockGap/2,
        digit: block.digit,
    }
}

function onTouchStart(e) {
    data.oldPosition={x: e.offsetX, y: e.offsetY};
    data.isDraw=true;
}

function onTouchMove(e) {
    if (data.isDraw) {
        scanSelectedBlocks(e)
        clearCanvas(true)
        drawBlocks()
        drawSelector(e)
        drawSelectedBlocks()
    }
}

function onTouchEnd(){
    clearCanvas(true)
    drawBlocks()
    clearBlocks()
    data.isDraw=false;
    data.canvasData.selectedBlockList=[];
    clearCanvas(true)
    drawBlocks()
}

function clearBlocks(){
    const {selectedBlockList,blockList}=data.canvasData;
    let sum=0;
    selectedBlockList.forEach((blockIndex)=>{
        sum+=blockList[blockIndex].digit;
    });
    if(sum===10){
        data.score=data.score+selectedBlockList.length;
        document.getElementById('score').textContent=`你的分数：${data.score}`;
        //console.log(data.score)
        selectedBlockList.forEach((blockIndex)=>{
            blockList[blockIndex].flag=true;
        });
        const xy1={'x':blockList[selectedBlockList[0]].x,'y':blockList[selectedBlockList[0]].y};
        const xy2={'x':blockList[selectedBlockList[selectedBlockList.length-1]].x,'y':blockList[selectedBlockList[selectedBlockList.length-1]].y};
        fetch(`${ApiUrl}/api/clear`,{
            method:'POST',
            headers: {
                'Content-Type': 'application/json' // 设置请求的Content-Type
            },
            body:JSON.stringify({'id':data.id,'selected':[xy1,xy2]})})
            .then(response=>response.json())
            .then(data =>{
                    console.log(data.message)
            });
    }
}
function drawBlocks(){
    const { context, blockList, blockSize} = data.canvasData;
    let init=false;
    const blockCoordList=[];
    if(!data.canvasData.blockCoordList){       //初始化方块的坐标列表
        init=true;
    }
    //console.log(data.canvasData)
    blockList.forEach((block, index)=>{
        if(block.flag) return
        let coord = getBlockCoordinate(block);
        if(init){
            blockCoordList.push(coord);
        }
        context.fillStyle = "#FFFDF6";
        context.fillRect(coord.left, coord.top, blockSize, blockSize);
        context.fillStyle = "#000000";
        if(data.canvasData.selectedBlockList.indexOf(index)===-1){
            context.font = `${FontSize} 黑体`;
            context.fillText(block.digit, coord.left+blockSize/3, coord.top+blockSize/1.5);
        }
    });
    if(init){
        data.canvasData.blockCoordList=blockCoordList;
    }
}
function drawSelector(e) {
    const ctx = data.canvasData.context;
    const rectColor = '#FFFFFF';
    const fillColor = 'rgba(0,0,50,0.5)';
    const oldPosition = data.oldPosition;
    if (ctx) {
        ctx.fillStyle=fillColor;
        ctx.fillRect(oldPosition.x, oldPosition.y,e.offsetX-oldPosition.x, e.offsetY-oldPosition.y);
        ctx.strokeStyle=rectColor;
        ctx.lineWidth = 1;
        ctx.strokeRect(oldPosition.x, oldPosition.y,e.offsetX-oldPosition.x, e.offsetY-oldPosition.y);
    }
}
function scanSelectedBlocks(e){
    let minx=Math.min(data.oldPosition.x,e.offsetX);
    let maxx=Math.max(data.oldPosition.x,e.offsetX);
    let miny=Math.min(data.oldPosition.y,e.offsetY);
    let maxy=Math.max(data.oldPosition.y,e.offsetY);
    //console.log(minx,maxx)
    const {blockSize, blockList} =data.canvasData;
    const blockCoordList=data.canvasData.blockCoordList;
    //console.log(blockCoordList);
    const selectedBlockList=[];
    for(let i=0; i<RowNum*ColNum; i++){
        let x=blockCoordList[i].left+blockSize/2;
        let y=blockCoordList[i].top+blockSize/2;
        if(minx<x && x<maxx && miny<y && y<maxy && !blockList[i].flag){
            selectedBlockList.push(i)
        }
    }
    data.canvasData.selectedBlockList=selectedBlockList;
    //console.log(selectedBlockList)
}
function drawSelectedBlocks(){
    const { context, blockList, blockSize, selectedBlockList} = data.canvasData;
    selectedBlockList.forEach((blockIndex)=>{
        let block = blockList[blockIndex];
        let coord = getBlockCoordinate(block);

        context.beginPath();
        context.strokeStyle="#000000";
        context.lineWidth = 5;
        context.strokeText(block.digit, coord.left+blockSize/3, coord.top+blockSize/1.5);
        context.closePath();

        context.fillStyle = "#FFFFFF";
        context.font = `900 ${FontSize} 黑体`;
        context.fillText(block.digit, coord.left+blockSize/3, coord.top+blockSize/1.5);

    });
}
function createNewBlock(x=0,y=0){
    let bBlock = {
        x,
        y,
        left: 0,
        top: 0,
        flag:false
    };
    bBlock.digit = getRandomDigit();
    return bBlock;
}

function clearCanvas(isClear){
    const { canvas, context } = data.canvasData;
    if(isClear) context.clearRect(0,0,canvas.width,canvas.height);
    else context.fillRect(0,0,canvas.width,canvas.height);
    context.beginPath();
}


function game(){
    initData().then(function (){
        data.canvasData.canvas.onmousedown=onTouchStart;
        data.canvasData.canvas.onmousemove=onTouchMove;
        data.canvasData.canvas.onmouseup=onTouchEnd;
    });
}


function initRanks(){
    fetch(`${ApiUrl}/api/getranks`,{method:'GET'}).then(response=>response.json()).then(
        rep_data=>{
            for(const [_,info] of Object.entries(rep_data)){
                if(info.tag==="max"){
                    document.getElementById("max").innerHTML=`最高分: ${info.num}\n`;
                    continue
                }
                let id=`ranks-${info.tag}`;
                if(document.getElementById(id)===null){
                    var newDiv = document.createElement("div");
                    newDiv.id=id;
                    newDiv.innerHTML = `${info.tag}: ${info.num}人\n`;
                    document.getElementById('ranks').appendChild(newDiv);
                }
                else {
                    document.getElementById(id).innerHTML=`${info.tag}: ${info.num}人\n`;
                }

            }
        }
    );
}
initRanks()
setInterval(initRanks,10000);


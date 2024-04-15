const bodyParser = require('body-parser');
var express = require('express');

var app = express();

app.use(bodyParser.urlencoded({ extended: false }));

app.get('/', function (req, res) {
    res.send('<h1>Do you want to get the flag?</h1>'
        + '<p>Try to POST your name to /flag</p>');
});

app.post('/flag', function (req, res) {
    var name = req.body.name;
    console.log(req.headers);
    if (name !== 'admin') {
        res.send('<h1>Sorry, you are not admin</h1>');
        return;
    }
    var agent = req.headers['user-agent'];
    if (!agent.includes('or4ngeBrowser')) {
        res.send('<h1>Sorry, you are not using or4ngeBrowser</h1>');
        return;
    }
    var referer = req.headers['referer'];
    if (referer !== 'https://buaa.edu.cn') {
        res.send('<h1>Sorry, you are not from https://buaa.edu.cn</h1>');
        return;
    }
    var ip = req.headers['x-forwarded-for'];
    if (ip !== '127.0.0.1' && ip !== 'localhost') {
        res.send('<h1>Sorry, only local member can view the flag</h1>');
        return;
    }
    var flag = process.env.GZCTF_FLAG;
    res.send('<h1>Here is your flag: ' + flag + '</h1>');
});

app.listen(3000, function () {
    console.log('app listening on port 3000!');
});
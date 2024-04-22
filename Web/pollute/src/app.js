const express = require('express');
const path = require('path');

var app = express();
app.use(express.json());
app.use(express.static('public'));

function checkValid(filePath) {
    return filePath.startsWith('/tmp/');
}

app.use((req, _, next) => {
    req.files = {};
    for (const param in req.query) {
        if (param.startsWith('file.')) {
            const key = param.slice(5);
            req.files[key] = req.query[param];
        }
    }
    next();
});

app.use((req, res, next) => {
    Object.keys(req.files).forEach((key) => {
        try {
            const f = path.normalize(req.files[key]);
            if (!checkValid(f)) {
                f = "/tmp/Error.gif"
            }
            req.files[key] = f;
        } catch (e) {
            console.log(e);
            req.files[key] = "/tmp/Error.gif";
        }
    });
    next();
});

app.get('/file', (req, res) => {
    console.log(req.query);
    const filePath = req.files.File ?? "/tmp/Error.gif"
    try {
        res.sendFile(filePath);
    } catch (e) {
        console.error(e);
        res.sendFile("/tmp/Error.gif");
    }
});

app.listen(3000, () => { console.log(`listening on port 3000`) });
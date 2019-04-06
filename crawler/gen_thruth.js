'use strict';

const id = [];
const fs = require('fs');
let lineReader = require('readline').createInterface({
    input: fs.createReadStream("twitter-out2019-04-06T11_16_44.615Z.jsonl")
});
lineReader.on('line', function (line) {
    var data = JSON.parse(line);

    id.push(data.id);
});

lineReader.on('close', function () {
    fs.writeFileSync('thruth.jsonl', id.map(id => JSON.stringify({id,truthMean: 1,
        "truthMedian": 1,
        "truthMode"  : 1,
        "truthClass" : "clickbait"})).join('\n'));
});

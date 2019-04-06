'use strict';

const input = __dirname + "/twitter-30-cont2.jsonl";
const cld = require('cld');
var CLD_OPTIONS = {
    isHTML: false,
    languageHint: 'ENGLISH',
    tldHint: 'en',
    httpHint: 'en'
};
const launched = new Map();
const sleep = (milliseconds) => {
    return new Promise(resolve => setTimeout(resolve, milliseconds))
};
const output = (__dirname + "/twitter-reout" + new Date().toISOString() + ".jsonl").replace(/:/g, '_');

console.log(output);
global.fetch = require("node-fetch");

const fs = require('fs');

const inputs = ["twitterBkp.jsonl", "twitter_wtf.jsonl", "twitter-30-cont2.jsonl", "twitter-30-cont.jsonl", "twitter-out_3.jsonl", "twitter_7.jsonl", "twitter.jsonl", "twitter-30-cont123.jsonl"];


let writeQueue = [];
let writing = false;

function write(json) {
    let s = JSON.stringify(json);
    writeQueue.push(s);

    if (!writing)
        _write();
}

function _write() {
    writing = true;
    let data = writeQueue.join('\n') + "\n";
    writeQueue = [];
    fs.appendFile(output, data, 'utf8', function (err) {
        if (err) {
            console.error('Failed to write');
            console.error(err);
        }

        if (writeQueue.length)
            _write();
        else writing = false;
    })
}

const processed = new Set();
const Url = require("url");


// hack it
const parse = require('article-parser/src/parsers');
const cheerio = require('cheerio');

let multiple = 0, single = 0, none = 0;
process.on("exit", function () {
    console.log({multiple, single, none});
});


async function getArticle(urlString, post, tag) {
    let url = Url.parse(urlString);

    let host = url.host || url.hostname;
    let queue = launched.get(host);

    if (queue) {
        queue.push({
            urlString,
            tag,
            post
        });
    } else {
        queue = [];
        launched.set(host, queue);

        let articleR = await fetch(urlString);
        let article = await articleR.text();
        write({article, post, tag, urlString});


        // black magic
        for (let {urlString, post, tag} of queue) {
            await sleep(2000);
            let articleR = await fetch(urlString);
            let article = await articleR.text();

            write({article, post, tag, urlString});

        }

        launched.delete(host);
    }
}

function handler(line) {
    try {
        var data = JSON.parse(line);
    } catch (e) {
        console.error("Unable to convert a line");
        console.error(e);
    }


    if (data.urlString) {
        // console.log(JSON.stringify(data));
        let {article, post, tag, urlString} = data;
        getArticle(urlString, post, tag);
    }



    // const cheerio = require('cheerio');


}


function next() {
    let input = inputs.shift();
    if (input) {
        console.log("Next input " + input);

        let lineReader = require('readline').createInterface({
            input: fs.createReadStream(input)
        });
        lineReader.on('line', handler);
        lineReader.on("close", next);
    }
}

next();

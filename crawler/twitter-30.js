'use strict';

global.fetch = require("node-fetch");


const cheerio = require('cheerio');
const Twitter = require('twitter');
const hashtags = ["savedyouaclick", "clickbait"].map(e => "#" + e);
// const hashtags = ["clickbait"].map(e => "#" + e);
const Url = require("url");
const fs = require('fs');
const {
    extract
} = require('article-parser');

const sleep = (milliseconds) => {
    return new Promise(resolve => setTimeout(resolve, milliseconds))
};

/**
 * @type {Twitter}
 */
const twitterClient = new Twitter({
    consumer_key: 'EfCL5LdbULNNk1jIn2U0w9Zzy',
    consumer_secret: 'hsKJRctaxOVon0aqXqr9foN2ulsKTO6hc85VLprUrnSoe26LRU',
    access_token_key: '720191713038438401-bz305wHqUo1cHvicgI2V3wUQf0TGlNG',
    access_token_secret: 'H9Uqo5ngyTW0zZL4Gc6YcWoxlr1YuUEhu7P36tQ0uoaZf'
});



async function search(tag, next) {
    let response;
    try {
        response = await twitterClient.get("/tweets/search/30day/Test.json", {
            query: tag + " lang:en",
            next,
            maxResults: 100,
            toDate: "201903200000"
        });
    } catch (err) {
        console.error("Enc error");
        console.error(err);
        if (err[0] && err[0].code == 88) {
            sleep(1000 * 60).then(() => search(tag, next));
        }

        return;
    }
    response._tag = tag;

    fs.appendFileSync(__dirname + '/twitter-30-precontinue.jsonl', JSON.stringify(response) + "\n");
    next = response.next;

    await sleep(700);
    return search(tag, next);
}


for (let hashtag of hashtags)
    search(hashtag);

//{ "errors": [ { "code": 88, "message": "Rate limit exceeded" } ] }

//
//
// async function test() {
//     let r = await fetch('https:\/\/t.co\/eUcSLlrsQH');
//
//
//     let t = await r.text();
//
//     console.log(t);
//
//     const $ = cheerio.load(t);
//
//
//     console.log(r);
// }
//
// test();

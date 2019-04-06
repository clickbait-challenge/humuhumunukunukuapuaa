'use strict';

const input = __dirname + "/twitter-30-cont2.jsonl";
const cld = require('cld');
var CLD_OPTIONS = {
    isHTML: false,
    languageHint: 'ENGLISH',
    tldHint: 'en',
    httpHint: 'en'
};

const output = (__dirname + "/twitter-out" + new Date().toISOString() + ".jsonl").replace(/:/g, '_');

console.log(output);
global.fetch = require("node-fetch");

const fs = require('fs');

const inputs = ["twitter-reout2019-04-06T10_45_43.680Z.jsonl"];


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
    data = data.replace(/[^\x00-\x7F]/g, "");
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


// hack it
const parse = require('article-parser/src/parsers');
const cheerio = require('cheerio');

let multiple = 0, single = 0, none = 0;
process.on("exit", function () {
    console.log({multiple, single, none});
});

function handler(line) {
    try {
        var data = JSON.parse(line);
    } catch (e) {
        console.error("Unable to convert a line");
        console.error(e);
    }


    if (data.article && !processed.has(data.post.id_str)) {
        processed.add(data.post.id_str);
        if (data.post.__multiple)
            multiple++;
        else single++;
        let $ = cheerio.load(data.article);
        let paragraphs = [];
        $("p,td,th,h2,h3,h4,h5,h6").each(function () {
            $ = cheerio.load(this);

            let t = $.text().trim();

            if (t)
                paragraphs.push(t);
        });

        // $("p,td,th").each(function () {
        //     $ = cheerio.load(this);
        //
        //     let t = $.text().trim();
        //
        //     if (t)
        //         paragraphs.push(t);
        // });
        //
        // let titles = [];
        //
        // $("h1,h2,h3,h4,h5,h6").each(function () {
        //     $ = cheerio.load(this);
        //
        //     let t = $.text().trim();
        //
        //     if (t)
        //         titles.push(t);
        // });


        parse({html: data.article, url: data.urlString, _url: data.urlString}).then(async (result) => {
                let {post} = data;

                let postMedia = [];
                if (post.entities.urls) {
                    for (let url of post.entities.urls) {
                        if (url.display_url) {
                            let imageName = /\/([^\/]*\.(?:png|jpg))$/.exec(url.display_url);
                            if (imageName) {
                                imageName = imageName[1];
                                let res = await fetch(url.display_url);

                                res.body.pipe(fs.createWriteStream(__dirname + '/images/' + imageName));
                                postMedia.push(imageName);
                            }
                        }
                    }
                }
                if (post.extended_entities && post.extended_entities.media) {
                    for (let media of post.extended_entities.media) {
                        if (media.media_url) {
                            let imageName = /\/([^\/]*\.(?:png|jpg))$/.exec(media.media_url);
                            if (imageName) {
                                imageName = imageName[1];
                                let res = await fetch(media.media_url);

                                res.body.pipe(fs.createWriteStream(__dirname + '/images/' + imageName));
                                postMedia.push(imageName);
                            }
                        }
                    }
                }
                let finalForm = {
                    "id": [],
                    postTimestamp: "",
                    "postText": [],
                    postMedia,
                    "targetTitle": "",
                    "targetDescription": "",
                    "targetKeywords": "",
                    "targetParagraphs": paragraphs,
                    "targetCaptions": []
                };

                Object.assign(finalForm, {
                    "id": post.id_str,
                    postTimestamp: post.created_at,
                    "postText": [
                        post.text
                    ],
                    "targetTitle": result.title,
                    "targetDescription": result.description,
                    "targetParagraphs": paragraphs,
                    // "targetCaptions": titles
                });

                let text = paragraphs.join('\n');

                if (text)
                    cld.detect(text, CLD_OPTIONS, function (err, result) {
                        if (err) {
                            console.error("Unable to detect language");
                            console.error(err);
                        } else {
                            if (result.reliable && result.languages[0].code === 'en') {
                                write(finalForm);
                            } else {
                                console.log(`Lang ${JSON.stringify(result)} => ${JSON.stringify(finalForm)}`);
                            }
                        }
                    });
                else write(finalForm);

            }
        );
    } else none++;


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

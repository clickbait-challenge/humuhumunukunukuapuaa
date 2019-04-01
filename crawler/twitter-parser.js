'use strict';

const input = __dirname + "/twitter.jsonl";
const output = __dirname + "/twitter-out.jsonl"+ new Date().toISOString();


const fs = require('fs');

const lineReader = require('readline').createInterface({
    input: fs.createReadStream(input)
});

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


// hack it
const parse = require('article-parser/src/parsers');
const cheerio = require('cheerio');

let multiple = 0, single = 0, none = 0;
process.on("exit", function () {
    console.log({multiple,single, none});
});
lineReader.on('line', function (line) {
    var data = JSON.parse(line);


    if (data.article) {
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




        parse({html:  data.article, url: data.urlString, _url: data.urlString}).then((result) => {
            let {post} = data;

            let postMedia = [];
            if (post.entities.urls) {
                for (let url in post.entities.urls) {
                    if (url.display_url)
                        postMedia.push(url.display_url);
                }
            }
            let finalForm = {
                "id": post.id_str,
                postTimestamp: post.created_at,
                "postText": [
                    post.text
                ],
                postMedia,
                "targetTitle": result.title,
                "targetDescription": result.description,
                "targetKeywords": null,
                "targetParagraphs": paragraphs,
                // "targetCaptions": titles
                "targetCaptions": []
            };

            write(finalForm);
        }
    );
    }
    else none++;


    // const cheerio = require('cheerio');


});

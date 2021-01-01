

const fs = require('fs')



fs.readFile('./nkjv.json', 'utf8', (err, data) => {
    if (err) {
        console.log("File read failed:", err)
        return
    }

    var randomProperty = function (obj) {
        var keys = Object.keys(obj);
        return keys[keys.length * Math.random() << 0];
    };

    let bible = JSON.parse(data)
    let i = randomProperty(bible.text)
    console.log(`${bible.book[i]}  ${bible.chapter[i]}:${bible.verse[i]} (NKJV)\n ${bible.text[i]}`)
})


// var randomProperty = function (obj) {
//     var keys = Object.keys(obj);
//     return obj[keys[ keys.length * Math.random() << 0]];
// };
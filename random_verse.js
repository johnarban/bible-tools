

const fs = require('fs')


// https://stackoverflow.com/a/64354200
function randomTruncSkewNormal({
    rng = Math.random,
    range = [-Infinity, Infinity],
    mean,
    stdDev,
    skew = 0
  }) {
    // Box-Muller transform
    function randomNormals(rng) {
      let u1 = 0,
        u2 = 0;
      //Convert [0,1) to (0,1)
      while (u1 === 0) u1 = rng();
      while (u2 === 0) u2 = rng();
      const R = Math.sqrt(-2.0 * Math.log(u1));
      const Θ = 2.0 * Math.PI * u2;
      return [R * Math.cos(Θ), R * Math.sin(Θ)];
    }

    // Skew-normal transform
    // If a variate is either below or above the desired range,
    // we recursively call the randomSkewNormal function until
    // a value within the desired range is drawn
    function randomSkewNormal(rng, mean, stdDev, skew = 0) {
      const [u0, v] = randomNormals(rng);
      if (skew === 0) {
        const value = mean + stdDev * u0;
        if (value < range[0] || value > range[1])
          return randomSkewNormal(rng, mean, stdDev, skew);
        return value;
      }
      const sig = skew / Math.sqrt(1 + skew * skew);
      const u1 = sig * u0 + Math.sqrt(1 - sig * sig) * v;
      const z = u0 >= 0 ? u1 : -u1;
      const value = mean + stdDev * z;
      if (value < range[1] || value > range[0])
        return randomSkewNormal(rng, mean, stdDev, skew);
      return value;
    }

    return randomSkewNormal(rng, mean, stdDev, skew);
};

function randomValue(uniform = false) {
    if (uniform) {
        return Math.random()
    }
    return randomTruncSkewNormal({range: [0.0, 1.0],mean: 0.5,stdDev: 0.5/2})
}

function randomProperty(obj) {
    var keys = Object.keys(obj);
    return keys[keys.length * randomValue() << 0];
};

function getGoodRandom(i, randomProperty, bible) {
    length = 0;
    while (length < 10) {
        i = randomProperty(bible.text);
        length = bible.text[i].split(" ").length;
    };
    return i;
}

fs.readFile('./msg.json', 'utf8', (err, data) => {
    if (err) {
        console.log("File read failed:", err)
        return
    };


    let bible = JSON.parse(data);
    var i = '30044' // check Heb 9:16-17 in MSG
    i = getGoodRandom(i, randomProperty, bible);
    j = parseInt(i) + 1;
    j = j.toString();
    consec = parseInt(bible.verse[i]) == parseInt(bible.verse[j]) - 1
    endch = parseInt(bible.verse[j]) == 1
    if ( consec || (!consec && endch)) {
        text = bible.text[i].replace(/  +/g, '\n')
        console.log(`${bible.book[i]}  ${bible.chapter[i]}:${bible.verse[i]}\n ${text}`)
    } else {
        nextv = (parseInt(bible.verse[j]) - 1).toString()
        // console.log(`-${i} ${j}  ${bible.verse[i]} ${bible.verse[j]}`)
        text = bible.text[i].replace(/  +/g, '\n')
        console.log(`${bible.book[i]}  ${bible.chapter[i]}:${bible.verse[i]}-${nextv}\n ${text}`)
    };


});




// var randomProperty = function (obj) {
//     var keys = Object.keys(obj);
//     return obj[keys[ keys.length * Math.random() << 0]];
// };
const fs = require('fs');
const path = require('path');
const _ = require('lodash');
const features = require('features');

function extractFeatures(fpath,klass) {
  let samples = JSON.parse(fs.readFileSync(fpath,'utf8'));
  console.log(`Reading ${fpath} with ${samples.length} as ${klass}`)
  return samples
    .filter(seq => seq.length)
    .map(seq => Object.assign({klass},features(seq)));
}

let samples =
  extractFeatures(path.join(__dirname,'../data/invalid.txt'),false)
  .concat( extractFeatures(path.join(__dirname,'../data/invalid-harder.txt'),false))
  .concat( extractFeatures(path.join(__dirname,'../data/valid.txt'),true));

let txt = 'klass,maxX,maxY,maxZ,maxAlpha,maxBeta,maxGama,avgX,avgY,avgZ,avgAlpha,avgBeta,avgGama\n';
const attr = 'klass,maxX,maxY,maxZ,maxAlpha,maxBeta,maxGama,avgX,avgY,avgZ,avgAlpha,avgBeta,avgGama'.split(',');

txt += _.map(samples,s => attr.map(a => s[a]).join(',')).join('\n')
fs.writeFileSync(__dirname + '/../data/featured.csv',txt,'utf8');

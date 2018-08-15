const algo = require('./decsion-tree');
const fs = require('fs')
const _ = require('lodash');
const path = require('path');


const klassAttr = 'klass';
const testSetRatio = .2;

function readFeaturedData(file) {
  const parts = fs.readFileSync(file,'utf8').split('\n').map(x => x.split(','));
  const key = parts[0];
  return parts.slice(1).map(x => _(key).zip(x).fromPairs().value());
}
function confusionMatrix(data, model, klassAttr, order) {
  let matrix = order.map(x => order.map(_.constant(0)));

  _.forEach(data,dp=>{
    let actual = algo.classify(dp,model);
    let expected = dp[klassAttr];
    let iactual = order.indexOf(actual);
    let iexpected = order.indexOf(expected);
    if(iactual < 0) throw new Error(`Cannot find class ${actual} in ${order}`)
    if(iexpected < 0) throw new Error(`Cannot find class ${expected} in ${order}`)
    matrix[iexpected][iactual]++;
  })
  return matrix;
}

function stats(matrix) {
  let total = _.reduce(matrix, (m,row) => m + _.reduce(row, (m2,cell) => m2+cell,0) ,0);
  let correct = _.reduce(_.range(matrix.length),(m,i) => m + matrix[i][i],0)
  return correct/total;
}

let data = readFeaturedData(path.join(__dirname,'../data/featured.csv'));
function run() {
  let [test, training] = _.partition(data, dp => Math.random() < testSetRatio);
  const features = _(data[0]).keys().without(klassAttr);
  const klasses = _(data).map(klassAttr).uniq().value();
  let model = algo.learn(training,klassAttr);
  console.log("Model: ", JSON.stringify(model));
  let matrix = confusionMatrix(test,model,klassAttr,klasses);
  console.log(matrix);
  console.log('Accuracy: ',stats(matrix));
}

run();


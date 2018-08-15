
// datapoint is an object of any shape
// decisionTree is an object of two possible types:
//   If the class key is defined, then this is a leaf node associating the datapoint to this class
//   Otherwise, it appears as {attr: STRING: threshold: NUMBER: lnode: DECISION_TREE, rnode: DECISION_TREE}
//   otherwise, the attr and the threshold keys define a threshold on an attribute,
//   going to the lnode if it's less than or equal, and rnode otherwise


(function(){

  if(typeof window != 'undefined') {
    window.decisionTree = {}
    define(window.decisionTree,_)
  }
  else define(exports,require('lodash'))

function define(exports,_){

exports.classify = function(datapoint, decisionTree) {
  if(decisionTree.class) return decisionTree.class;
  if(datapoint[decisionTree.attr] <= decisionTree.threshold) return exports.classify(datapoint,decisionTree.lnode)
  return exports.classify(datapoint,decisionTree.rnode)
}

exports.learn = function(data, klassAttr) {
  const klasses = _(data).map(klassAttr).uniq().value();
  return recLearn(data);

  function recLearn(data) {
    let foundClasses = _(data).map(klassAttr).uniq().value();
    if(foundClasses.length <= 1) return {class: foundClasses[0]} // If we classify everything into the same bucket.. We're good!
    let [attr, threshold] = giniSplit(data, klasses,klassAttr);
    let node = {attr,threshold};
    let splitData = _.partition(data, dp => dp[node.attr] <= node.threshold);
    node.lnode = exports.learn(splitData[0],klassAttr);
    node.rnode = exports.learn(splitData[1],klassAttr);
    return node;
  }
}

function giniSplit(data, klasses, klassAttr) {
  let attrs = _(data[0]).keys().without(klassAttr).value();
  let best = 2;
  let bestSplit = null;

  for(let attr of attrs) { // Try a cut for each attribute
    for(let i=0; i < data.length -1; ++i) { // Try a cut to the right of each data point (but don't bother with the last, since that divides no points)
      let threshold = data[i][attr];
      //console.log(`Partition were ${attr} <= ${threshold}`)
      let groups = _.partition(data, dp => dp[attr] <= threshold);
      //console.log('Groups',_.map(groups,'length'))
      if(_.some(groups, g => g.length == 0)) break;
      let cur = gini(groups,klasses,klassAttr);
      //console.log('Got gini: ',cur)
      if(cur < best) {
        best = cur;
        bestSplit = [attr, threshold]
      }
      //return bestSplit;
    }
  }
  //console.log('The split is: ', bestSplit, best)
  return bestSplit;
}

function gini(groups,klasses,klassAttr) {
  let nTotal = _.sumBy(groups,'length');
  //console.log('groups',groups);
  //console.log('nTotal',nTotal);
  return _.sumBy(groups, group => {
    let portions = klasses.map(klass => _.sumBy(group, row => row[klassAttr] == klass ? 1 : 0 )/group.length );
    //console.log('Portions',portions)
    let gini = (1 - _.sumBy(portions,p => p * p)) * group.length / nTotal;
    return gini;
  });
}

function randomSplit(data,klassAttr) {
  let attr = _(data[0]).keys().without(klassAttr).sample();
  let dataOfAttr = _.map(data,attr);
  let min = _.min(dataOfAttr);
  let max = _.max(dataOfAttr);
  let threshold = _.random(min,max,true);
  return [attr,threshold];
}

}
})();

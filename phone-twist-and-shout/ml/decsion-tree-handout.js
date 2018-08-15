
// datapoint is an object of any shape
// decisionTree is an object of two possible types:
//   If the class key is defined, then this is a leaf node associating the datapoint to this class
//   Otherwise, it appears as {attr: STRING: threshold: NUMBER: lnode: DECISION_TREE, rnode: DECISION_TREE}
//   otherwise, the attr and the threshold keys define a threshold on an attribute,
//   going to the lnode if it's less than or equal, and rnode otherwise

const _ = require('lodash');

exports.classify = function(datapoint, decisionTree) {
  if(decisionTree.class) return decisionTree.class;
  if(datapoint[decisionTree.attr] <= decisionTree.threshold) return exports.classify(datapoint,decisionTree.lnode)
  return exports.classify(datapoint,decisionTree.rnode)
}

exports.learn = function(data,klassAttr) {
}

function randomSplit(data,klassAttr) {
  let attr = _(data[0]).keys().without(klassAttr).sample();
  let dataOfAttr = _.map(data,attr);
  let min = _.min(dataOfAttr);
  let max = _.max(dataOfAttr);
  let threshold = _.random(min,max,true);
  return [attr,threshold];
}

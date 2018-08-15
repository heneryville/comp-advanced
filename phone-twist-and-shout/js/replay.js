window.addEventListener('devicemotion',handleMotion,true);

let buffer = [];

function handleMotion(e) {
  let features = [
    e.acceleration.x,
    e.acceleration.y,
    e.acceleration.z,
    e.rotationRate.alpha,
    e.rotationRate.beta,
    e.rotationRate.gamma,
  ];

  buffer.push(features);
  buffer = buffer.splice(0,100);
  let features = window.features(buffer);
  let klass = decisionTree.classify(features,dtModel);
  console.log('Classified as ', klass);
  if(klass == 'true') {
    window.document.body.style.backgroundColor = 'green'
  }
  else window.document.body.style.backgroundColor = 'red'
}

const dtModel = {"attr":"maxX","threshold":"72.1497802734375","lnode":{"attr":"avgZ","threshold":"4.75382016916744","lnode":{"attr":"maxX","threshold":"6.910056114196777","lnode":{"class":"false"},"rnode":{"attr":"avgZ","threshold":"1.4556824699692104","lnode":{"class":"false"},"rnode":{"attr":"maxX","threshold":"63.54800796508789","lnode":{"class":"false"},"rnode":{"class":"true"}}}},"rnode":{"class":"true"}},"rnode":{"attr":"maxGama","threshold":"2.394787549972534","lnode":{"attr":"avgAlpha","threshold":"-1.2402719564602844","lnode":{"attr":"avgX","threshold":"0.8595830931955454","lnode":{"class":"false"},"rnode":{"class":"true"}},"rnode":{"class":"true"}},"rnode":{"class":"false"}}}

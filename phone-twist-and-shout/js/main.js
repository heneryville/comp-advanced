window.addEventListener('devicemotion',handleMotion,true);

let recording = false;
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
}

let elRecord = document.getElementById('record');
let elBody = document.body;
let elDownload = document.getElementById('download');
let elClear = document.getElementById('clear');

elRecord.addEventListener('mousedown',startRecording);
elRecord.addEventListener('touchstart',startRecording);

function startRecording(){
  buffer = [];
  recording = true;
  rerender();
}

elBody.addEventListener('mouseup', endRecording);
elBody.addEventListener('touchend', endRecording);

elDownload.addEventListener('click',downloadData);
elClear.addEventListener('click',clear);

function clear() {
  localStorage.clear();
}

function downloadData() {
  let data = [];
  for(var i = 0; i<localStorage.length; ++i) {
    let txt = localStorage.getItem(localStorage.key(i));
    data.push(JSON.parse(txt));
  }
  download('data.txt',JSON.stringify(data))
}

function endRecording(){
  if(!recording) return;
  recording = false;
  localStorage.setItem( 'datum' + localStorage.length, JSON.stringify(buffer) )
  rerender();
}

function rerender() {
  elBody.className = recording ? 'recording' : '';
}

function download(filename, text) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);

}

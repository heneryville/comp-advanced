'use strict';
const d = 1000;
const r = d/2;
let hits = 0;
let tries = 0;

var canvas = document.getElementById('canvas');
canvas.width = d;
canvas.height = d;
var ctx = canvas.getContext('2d');
ctx.fillStyle = '#ddd';
ctx.fillRect(0,0,d,d);

ctx.beginPath();
ctx.strokeStyle = 'black';
ctx.arc(r,r,r,0,2*Math.PI,false);
ctx.stroke()

var start = new Date().getTime();
setInterval(throwDartBatch,0)
document.getElementById('real-pi').textContent = ''+Math.PI

function throwDartBatch() {
  for(var i=0; i<10000; ++i) throwDart();
  var now = new Date().getTime();
  var elapsed = now-start;
  var ratio = hits/tries;
  document.getElementById('hits').textContent = ''+hits;
  document.getElementById('tries').textContent = ''+tries;
  document.getElementById('ratio').textContent = ''+(ratio)
  document.getElementById('pi').textContent = ''+(ratio*4)
  document.getElementById('elapsed').textContent = ''+elapsed
  document.getElementById('tps').textContent = ''+(tries/elapsed)
}

function throwDart() {
  var x = Math.random() * d;
  var y = Math.random() * d;
  var vx = x-r;
  var vy = y-r;
  var hit = vx*vx + vy*vy < r*r
  tries++;
  if(hit) hits++;
  ctx.beginPath();
  if(hit) ctx.fillStyle = 'green';
  else ctx.fillStyle = 'red';
  ctx.fillRect(x,y,1,1);
}



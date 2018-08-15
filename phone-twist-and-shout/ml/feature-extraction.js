(function(module) {
  /* Sequence values
      e.acceleration.x,
      e.acceleration.y,
      e.acceleration.z,
      e.rotationRate.alpha,
      e.rotationRate.beta,
      e.rotationRate.gamma,
  */
  function extract(seq) {
    return {
      maxX: max(seq,'0'),
      maxY: max(seq,'1'),
      maxZ: max(seq,'2'),
      maxAlpha: max(seq,'3'),
      maxBeta: max(seq,'4'),
      maxGama: max(seq,'5'),
      avgX: avg(seq,'0'),
      avgY: avg(seq,'1'),
      avgZ: avg(seq,'2'),
      avgAlpha: avg(seq,'3'),
      avgBeta: avg(seq,'4'),
      avgGama: avg(seq,'5'),
    }
    module.features = extract;
  }

  function max(seq,slot) {
    return Math.max.apply(null, _.map(seq,slot));
  }

  function avg(seq,slot) {
    return _.reduce(_.map(seq,slot),(a,x) => a + x,0) / seq.length;
  }

})( window ? window : module.exports )

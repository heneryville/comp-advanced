const gulp = require('gulp');
const awspublish = require('gulp-awspublish');
const debug = require('gulp-debug');

const publisher = awspublish.create({
  region: 'us-east-1',
  params: {
    Bucket: 'phone-twist-and-shout-mitchell'
  }
})

gulp.task('watch',() => {
  gulp.watch(['js/*.js','*.html'], ['publish']);
});


gulp.task('publish',() => {
  return gulp.src(['**','!node_modules/**'])
  .pipe(debug('files'))
  .pipe(publisher.publish())
})

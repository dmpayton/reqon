var express = require('express'),
  execSync = require('child_process').execSync
  gulp = require('gulp'),
  livereload = require('connect-livereload'),
  lrserver = require('tiny-lr')(),
  path = require('path'),
  $ = require('gulp-load-plugins')();

var config = {
  livereloadPort: 35729,
  serverPort: 8080
};

var server = express();
server.use(livereload({
  port: config.livereloadPort
}));
server.use(express.static('./build/'));


gulp.task('build', function(){
  execSync('sphinx-build ./source ./build');
  $.livereload(lrserver);
});


gulp.task('serve', function() {
  server.listen(config.serverPort);
  lrserver.listen(config.livereloadPort);
});


gulp.task('watch', function() {
  gulp.watch('./source/**/*', ['build']);
});


gulp.task('default', ['build', 'serve', 'watch']);

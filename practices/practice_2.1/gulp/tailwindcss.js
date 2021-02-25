const { src, dest } = require('gulp');
const rename = require('gulp-rename');
const postcss = require('gulp-postcss');
const tailwindcss = require('tailwindcss');

const compile = () =>
  src('assets/tailwind.css')
    .pipe(postcss([tailwindcss]))
    .pipe(rename(path => (path.extname = '.generated.css')))
    .pipe(dest('app/static/css/'));

exports.compileTailwind = compile;

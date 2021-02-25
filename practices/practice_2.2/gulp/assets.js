const path = require('path');
const { src, dest } = require('gulp');

const poppinsFonts = [100, 200, 300, 400, 500, 600, 700, 800, 900];

const copyPoppinsFont = weight => () =>
  src(
    path.join(
      'node_modules/fontsource-poppins/files/',
      `poppins-all-${weight}-normal.woff`
    )
  ).pipe(dest('src/app/static/fonts/Poppins'));

exports.copyTasks = poppinsFonts.map(weight => copyPoppinsFont(weight));

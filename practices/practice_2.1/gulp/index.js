const { series } = require('gulp');
const { copyTasks } = require('./assets');
const { compileTailwind } = require('./tailwindcss');

exports.default = series(...copyTasks, compileTailwind);

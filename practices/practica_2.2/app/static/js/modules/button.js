import { getId } from './helper.js';

const _toggleButton = (buttonId, enable) => {
  let bttn = getId(buttonId);
  let content = bttn.querySelector('.content-section');
  let loading = bttn.querySelector('.loading-section');

  bttn.disabled = !enable;
  bttn.classList.toggle('cursor-pointer', enable);
  content.classList.toggle('hidden', !enable);
  loading.classList.toggle('hidden', enable);
};

const loadingButton = async (buttonId, cb) => {
  _toggleButton(buttonId, false);

  await cb();

  _toggleButton(buttonId, true);
};

export { loadingButton };

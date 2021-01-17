import { getId, makeRequest } from './modules/helper.js';
import { loadingButton } from './modules/button.js';
import { log } from './modules/log.js';

async function testTopologyImage() {
  return (
    await fetch(`${window.origin}/static/images/network.png`, {
      method: 'GET',
    })
  ).ok;
}

const updateDataBase = async () => {
  let [json, code] = await makeRequest({ type: 'updateDb' }, 'request');

  if (code !== 200) {
    log(json['message'], 'error', `Error ${code}`);
  } else {
    log('Se actualizó la base de datos, recarga la página.', 'ok');
    window.location = '/';
  }
};

async function toggleImage() {
  let isFound = await testTopologyImage();

  let imageSection = document.getElementById('image_found');
  let notImageSection = document.getElementById('image_not_found');

  imageSection.classList.toggle('hidden', !isFound);
  notImageSection.classList.toggle('hidden', isFound);

  if (isFound) {
    imageSection.querySelector('img').src = '/static/images/network.png';
  }
}

document.addEventListener('DOMContentLoaded', async () => {
  toggleImage();

  getId('bttn_update').addEventListener('click', () =>
    loadingButton('bttn_update', updateDataBase)
  );
});

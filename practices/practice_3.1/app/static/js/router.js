import { getId, makeRequest } from './modules/helper.js';
import { loadingButton } from './modules/button.js';
import { log } from './modules/log.js';

let currentHostname;

const changeHostName = async () => {
  getId('bttn_cancel').classList.add('hidden');

  let input = getId('input_hostname_router');
  input.classList.add('no-input');
  input.classList.remove('input');

  let newHostname = input.value;

  let req = {
    type: 'changeHostname',
    router: {
      id: getId('router_id').innerHTML,
      newHostname,
    },
  };

  let [json, code] = await makeRequest(req, 'request');

  if (code !== 200) {
    log(json['message'], 'error', `Error ${code}`);
  } else {
    log('Se actualizó el nombre del router exitósamente.', 'ok');

    getId('router_hostname').innerHTML = newHostname;
    currentHostname = newHostname;
  }

  toggleEdit(false);
};

const toggleInput = (input, enable, value = '') => {
  input = getId(input);

  input.disabled = !enable;
  input.classList.toggle('no-input', !enable);
  input.classList.toggle('input', enable);
  input.value = value;

  if (enable) {
    input.focus();
  }
};

const toggleEdit = edit => {
  getId('bttn_save').classList.toggle('hidden', !edit);
  getId('bttn_cancel').classList.toggle('hidden', !edit);
  getId('bttn_edit').classList.toggle('hidden', edit);

  toggleInput('input_hostname_router', edit, edit ? '' : currentHostname);
};

document.addEventListener('DOMContentLoaded', async () => {
  currentHostname = getId('input_hostname_router').value;

  getId('bttn_edit').addEventListener('click', () => toggleEdit(true));

  getId('bttn_cancel').addEventListener('click', () => toggleEdit(false));

  getId('bttn_save').addEventListener('click', () =>
    loadingButton('bttn_save', changeHostName)
  );
});

import { getId, makeRequest } from './modules/helper.js';
import { loadingButton } from './modules/button.js';
import { log } from './modules/log.js';

const checkLogin = async () => {
  const name = getId('input_username').value;
  const password = getId('input_password').value;

  const req = {
    type: 'login',
    user: {
      name,
      password,
    },
  };

  let [json, code] = await makeRequest(req, 'request');

  if (code !== 200) {
    log(json['message'], 'error', `Error ${code}`);
  } else {
    log('Las credenciales son válidas', 'ok');
    window.location = '/';
  }
};

document.addEventListener('DOMContentLoaded', () => {
  getId('bttn_login').addEventListener('click', () =>
    loadingButton('bttn_login', checkLogin)
  );
});

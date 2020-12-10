current_router = {};

async function getRouterInformation() {
  router_id = window.location.href.split('/').slice(-1)[0];

  req = { type: 'router' };

  res = await fetch(`${window.origin}/requests/${router_id}`, {
    method: 'POST',
    body: JSON.stringify(req),
    headers: new Headers({
      'content-type': 'application/json',
    }),
  });

  json = await res.json();

  if (!res.ok) {
    json['status'] = res.status;
  }

  return json;
}

function logSomeTime(logId, message) {
  log = document.getElementById(logId);

  log.innerHTML = message;
  setTimeout(() => (log.innerHTML = ''), 3000);
}

function getRouterButtons() {
  return {
    edit: document.getElementById('bttn_edit_router'),
    cancelRouter: document.getElementById('bttn_cancel_router'),
    saveRouter: document.getElementById('bttn_save_router'),
    inputHostname: document.getElementById('input_hostname_router'),
  };
}

function showModifyRouter() {
  ({ edit, cancelRouter, saveRouter, inputHostname } = getRouterButtons());

  edit.classList.add('hidden');
  cancelRouter.classList.remove('hidden');
  saveRouter.classList.remove('hidden');

  inputHostname.readOnly = false;
  inputHostname.focus();
}

async function hideModifyRouter() {
  ({ edit, cancelRouter, saveRouter, inputHostname } = getRouterButtons());

  edit.classList.remove('hidden');
  cancelRouter.classList.add('hidden');
  saveRouter.classList.add('hidden');

  inputHostname.readOnly = true;
  inputHostname.value = current_router['hostname'];
}

function saveDataRouter() {
  ({ cancelRouter, saveRouter } = getRouterButtons());
  cancelRouter.disabled = true;
  saveRouter.disabled = true;

  let req = {
    type: 'modify',
    hostname: document.getElementById('input_hostname_router').value,
  };

  fetch(`${window.origin}/requests/${current_router['ip_max']}`, {
    method: 'POST',
    body: JSON.stringify(req),
    headers: new Headers({
      'content-type': 'application/json',
    }),
  }).then(async res => {
    json = await res.json();

    if (!res.ok) json['status'] = res.status;

    logSomeTime('log_router', JSON.stringify(json));

    current_router = await getRouterInformation();

    cancelRouter.disabled = false;
    saveRouter.disabled = false;

    hideModifyRouter();
  });
}

document.addEventListener('DOMContentLoaded', async _ => {
  ({ edit, cancelRouter, saveRouter } = getRouterButtons());

  edit.addEventListener('click', showModifyRouter);
  cancelRouter.addEventListener('click', hideModifyRouter);
  saveRouter.addEventListener('click', saveDataRouter);

  current_router = await getRouterInformation();
});

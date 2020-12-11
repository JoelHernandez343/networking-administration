let current_router = {};
let editRouter, cancelRouter, saveRoutee, inputHostname, loadingRouter;

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

function toggleInputRouter(enable) {
  inputHostname.disabled = !enable;
  inputHostname.classList.toggle('no-input', !enable);
  inputHostname.classList.toggle('input', enable);
}

function toggleLoadingRouter(show) {
  loadingRouter.classList.toggle('hidden', !show);
}

function getRouterButtons() {
  return {
    editRouter: document.getElementById('bttn_edit_router'),
    cancelRouter: document.getElementById('bttn_cancel_router'),
    saveRouter: document.getElementById('bttn_save_router'),
    inputHostname: document.getElementById('input_hostname_router'),
    loadingRouter: document.getElementById('loading_router'),
  };
}

function showModifyRouter() {
  editRouter.classList.add('hidden');
  cancelRouter.classList.remove('hidden');
  saveRouter.classList.remove('hidden');

  toggleInputRouter(true);
  inputHostname.focus();
}

async function hideModifyRouter() {
  editRouter.classList.remove('hidden');
  cancelRouter.classList.add('hidden');
  saveRouter.classList.add('hidden');

  toggleInputRouter(false);
  inputHostname.value = current_router['hostname'];
}

function saveDataRouter() {
  cancelRouter.classList.add('hidden');
  saveRouter.classList.add('hidden');
  toggleLoadingRouter(true);
  toggleInputRouter(false);

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

    toggleLoadingRouter(false);

    hideModifyRouter();
  });
}

document.addEventListener('DOMContentLoaded', async _ => {
  ({
    editRouter,
    cancelRouter,
    saveRouter,
    inputHostname,
    loadingRouter,
  } = getRouterButtons());

  editRouter.addEventListener('click', showModifyRouter);
  cancelRouter.addEventListener('click', hideModifyRouter);
  saveRouter.addEventListener('click', saveDataRouter);

  current_router = await getRouterInformation();
});

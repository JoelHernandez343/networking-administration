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
  setTimeout(() => (log.innerHTML = ''), 5000);
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

let addBttn,
  cancelAddBttn,
  saveAddBttn,
  addSection,
  logAdd,
  inAddName,
  inAddPass,
  loadingAdd;

function toggleInput(input, enable, clear) {
  input.disabled = !enable;
  input.classList.toggle('no-input', !enable);
  input.classList.toggle('input', enable);

  if (clear) {
    input.value = '';
  }
}

function getAddUserNodes() {
  let D = document;

  addBttn = D.getElementById('bttn_add_user');
  cancelAddBttn = D.getElementById('bttn_cancel_add_user');
  saveAddBttn = D.getElementById('bttn_add_use_save');
  addSection = D.getElementById('add_user_section');
  logAdd = D.getElementById('log_add_user');
  inAddName = D.getElementById('input_add_user_name');
  inAddPass = D.getElementById('input_add_user_pass');
  loadingAdd = D.getElementById('loading_add_user');
}

function toggleAddUser(show) {
  addBttn.classList.toggle('hidden', show);
  cancelAddBttn.classList.toggle('hidden', !show);
  saveAddBttn.classList.toggle('hidden', !show);
  addSection.classList.toggle('hidden', !show);

  [inAddName, inAddPass].forEach(e => toggleInput(e, show, true));

  if (show) {
    inAddName.focus();
  }
}

function saveAddUser() {
  let req = {
    type: 'create',
    user: {
      name: inAddName.value,
      password: inAddPass.value,
    },
  };

  toggleAddUser(false);
  addBttn.classList.add('hidden');
  loadingAdd.classList.remove('hidden');

  fetch(`/requests/users/${current_router['ip_max']}`, {
    method: 'POST',
    body: JSON.stringify(req),
    headers: new Headers({
      'content-type': 'application/json',
    }),
  }).then(async res => {
    json = await res.json();

    if (!res.ok) json['status'] = res.status;

    logSomeTime('log_add_user', JSON.stringify(json));

    addBttn.classList.remove('hidden');
    loadingAdd.classList.add('hidden');
  });
}

let userState = [];

function getUserNodes(index) {
  return {
    userName: document.getElementById(`input_user_name_${index}`),
    userPass: document.getElementById(`input_user_pass_${index}`),
    container: document.getElementById(`user_container_${index}`),
    bttnDeleteUser: document.getElementById(`bttn_delete_user_${index}`),
    bttnEditUser: document.getElementById(`bttn_edit_user_${index}`),
    bttnSaveUser: document.getElementById(`bttn_save_user_${index}`),
    bttnCancelUser: document.getElementById(`bttn_cancel_user_${index}`),
    loadingUser: document.getElementById(`loading_user_${index}`),
  };
}

function deleteUser(index) {
  let {
    userName,
    container,
    bttnDeleteUser,
    bttnEditUser,
    loadingUser,
  } = getUserNodes(index);

  [bttnDeleteUser, bttnEditUser].forEach(e => e.classList.add('hidden'));

  loadingUser.classList.remove('hidden');

  let req = {
    type: 'delete',
    user: {
      name: userName.value,
    },
  };

  fetch(`/requests/users/${current_router['ip_max']}`, {
    method: 'POST',
    body: JSON.stringify(req),
    headers: new Headers({
      'content-type': 'application/json',
    }),
  }).then(async res => {
    json = await res.json();

    if (!res.ok) json['status'] = res.status;

    logSomeTime('log_add_user', JSON.stringify(json));

    container.classList.add('hidden');
  });
}

function toggleUserEdit(index, edit) {
  let {
    userName,
    userPass,
    bttnDeleteUser,
    bttnEditUser,
    bttnSaveUser,
    bttnCancelUser,
  } = getUserNodes(index);

  [bttnDeleteUser, bttnEditUser].forEach(e =>
    e.classList.toggle('hidden', edit)
  );

  [bttnSaveUser, bttnCancelUser].forEach(e =>
    e.classList.toggle('hidden', !edit)
  );

  [userName, userPass].forEach(e => toggleInput(e, edit));

  if (edit) {
    userState[index] = userName.value;
  } else {
    userName.value = userState[index];
    userPass.value = '';
  }
}

function saveUser(index) {
  let {
    userName,
    userPass,
    bttnSaveUser,
    bttnCancelUser,
    loadingUser,
  } = getUserNodes(index);

  [bttnSaveUser, bttnCancelUser].forEach(e => e.classList.add('hidden'));

  loadingUser.classList.remove('hidden');

  let req = {
    type: 'modify',
    user: {
      name: userState[index],
      new_name: userName.value,
      password: userPass.value,
    },
  };

  fetch(`/requests/users/${current_router['ip_max']}`, {
    method: 'POST',
    body: JSON.stringify(req),
    headers: new Headers({
      'content-type': 'application/json',
    }),
  }).then(async res => {
    json = await res.json();

    if (!res.ok) json['status'] = res.status;

    logSomeTime('log_add_user', JSON.stringify(json));

    if (res.ok) {
      userState[index] = userName.value;
    }

    toggleUserEdit(index, false);
    loadingUser.classList.add('hidden');
  });
}

function setUserEvents() {
  userState = [...Array(current_router['users'].length + 1).keys()];

  for (let i = 1; i <= current_router['users'].length; ++i) {
    document
      .getElementById(`bttn_delete_user_${i}`)
      ?.addEventListener('click', () => deleteUser(i));

    document
      .getElementById(`bttn_edit_user_${i}`)
      ?.addEventListener('click', () => toggleUserEdit(i, true));

    document
      .getElementById(`bttn_cancel_user_${i}`)
      ?.addEventListener('click', () => toggleUserEdit(i, false));

    document
      .getElementById(`bttn_save_user_${i}`)
      ?.addEventListener('click', () => saveUser(i));
  }
}

document.addEventListener('DOMContentLoaded', async () => {
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

  getAddUserNodes();

  addBttn.addEventListener('click', () => toggleAddUser(true));
  cancelAddBttn.addEventListener('click', () => toggleAddUser(false));
  saveAddBttn.addEventListener('click', saveAddUser);

  setUserEvents();
});

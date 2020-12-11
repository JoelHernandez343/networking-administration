let current_interface = {};
let edit, cancel, save, inIp, inMask, inActive, loading, fnetwork, sActive;

async function getInterfaceInfo() {
  [router, interface] = window.location.href.split('/').slice(-2);

  req = { type: 'information' };

  res = await fetch(`${window.origin}/requests/${router}/${interface}`, {
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

function getNodes() {
  return {
    edit: document.getElementById('bttn_edit'),
    cancel: document.getElementById('bttn_cancel'),
    save: document.getElementById('bttn_save'),
    inIp: document.getElementById('input_ip'),
    inMask: document.getElementById('input_mask'),
    inActive: document.getElementById('input_active'),
    loading: document.getElementById('loading'),
    fnetwork: document.getElementById('network_field'),
    sActive: document.getElementById('span_active'),
  };
}

function updateInfo() {
  inIp.value = current_interface['ip'];
  inMask.value = current_interface['mask'];
  fnetwork.innerHTML = current_interface['net'];
  inActive.checked = current_interface['is_active'];
  sActive.innerHTML = current_interface['is_active'] ? 'Activa' : 'Desactivada';
}

function toggleInput(input, enable) {
  input.disabled = !enable;
  input.classList.toggle('no-input', !enable);
  input.classList.toggle('input', enable);
}

function toggleEdit(show) {
  edit.classList.toggle('hidden', show);
  cancel.classList.toggle('hidden', !show);
  save.classList.toggle('hidden', !show);

  [inIp, inMask, inActive].forEach(n => toggleInput(n, show));

  if (show) {
    inIp.focus();
  }
}

function saveData() {
  toggleEdit(false);
  edit.classList.add('hidden');
  loading.classList.remove('hidden');

  let req = {
    type: 'modify',
    changes: {
      ip: inIp.value,
      mask: inMask.value,
      is_active: inActive.checked,
    },
  };

  fetch(
    `${window.origin}/requests/${current_interface['router_id']}/${current_interface['name']}`,
    {
      method: 'POST',
      body: JSON.stringify(req),
      headers: new Headers({
        'content-type': 'application/json',
      }),
    }
  ).then(async res => {
    json = await res.json();

    if (!res.ok) json['status'] = res.status;

    logSomeTime('log', JSON.stringify(json));

    current_interface = await getInterfaceInfo();

    edit.classList.remove('hidden');
    loading.classList.add('hidden');

    updateInfo();
  });
}

document.addEventListener('DOMContentLoaded', async () => {
  ({
    edit,
    cancel,
    save,
    inIp,
    inMask,
    inActive,
    loading,
    fnetwork,
    sActive,
  } = getNodes());

  edit.addEventListener('click', () => toggleEdit(true));
  cancel.addEventListener('click', () => {
    toggleEdit(false);
    updateInfo();
  });
  save.addEventListener('click', saveData);

  current_interface = await getInterfaceInfo();
});

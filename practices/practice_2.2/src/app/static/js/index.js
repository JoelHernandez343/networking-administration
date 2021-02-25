import { getId, makeRequest } from './modules/helper.js';
import { loadingButton } from './modules/button.js';
import { log } from './modules/log.js';

let vlans = [];

const getVlans = async () => {
  let [json, code] = await makeRequest({ type: 'vlans' }, 'request');

  if (code !== 200) {
    log(json['message'], 'error', `Error ${code}`);
  }

  return code !== 200 ? [] : json;
};

const viewVlan = (e, v) => {
  if (e.target.closest(`#delete_vlan_${v}`)) {
    return;
  }

  window.location = `${window.origin}/vlans/${v}`;
};

const deleteVlan = async v => {
  let req = {
    type: 'delete',
    vlan_number: v,
  };

  let [json, code] = await makeRequest(req, 'request');
  if (code !== 200) {
    log(json['message'], 'error', `Error ${code}`);
  } else {
    log('Se eliminó la vlan exitósamente.', 'ok');
    getId(`vlan_${v}`).classList.add('hidden');
  }
};

const setVlansEvents = vlans => {
  for (let v of vlans) {
    getId(`vlan_${v['number']}`).addEventListener('click', e =>
      viewVlan(e, v['number'])
    );

    getId(`delete_vlan_${v['number']}`)?.addEventListener('click', () =>
      loadingButton(`delete_vlan_${v['number']}`, () => deleteVlan(v['number']))
    );
  }
};

const updateDataBase = async () => {
  let [json, code] = await makeRequest({ type: 'scan' }, 'request');
  if (code !== 200) {
    log(json['message'], 'error', `Error ${code}`);
  } else {
    log('Se actualizó la base de datos, recarga la página.', 'ok');
    window.location = '/';
  }
};

document.addEventListener('DOMContentLoaded', async () => {
  vlans = await getVlans();

  if (vlans.length === 0) {
    getId('add_button_section').classList.add('hidden');
  }

  setVlansEvents(vlans);

  getId('bttn_update').addEventListener('click', () =>
    loadingButton('bttn_update', updateDataBase)
  );
});

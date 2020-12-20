import { getId, makeRequest } from './modules/helper.js';
import { loadingButton } from './modules/button.js';
import { log } from './modules/log.js';

let switches = [];
let selected = [];

const getSwitches = async () => {
  let [json, code] = await makeRequest({ type: 'switches' }, 'request');

  if (code !== 200) {
    log(json['message'], 'error', `Error ${code}`);
  }

  return code !== 200 ? [] : json;
};

const toggleWarning = () => {
  let isClean = true;
  selected.forEach(s => (isClean &&= s['v'] === 1));

  getId('warning').classList.toggle('hidden', isClean);
};

const toggleSelection = (s, i, v) => {
  let index = selected.findIndex(
    e => e['s'] === s && e['i'] === i && e['v'] === v
  );

  let add = index === -1;
  let capsule = getId(`int_${s}_${i}`);

  add ? selected.push({ s, i, v }) : selected.splice(index, 1);
  capsule.classList.toggle('bg-gray-200', !add);
  capsule.classList.toggle('bg-green-200', add);

  toggleWarning();
};

const setInterfacesEvents = switches => {
  for (let s of switches) {
    for (let i of s['interfaces']) {
      getId(`int_${s['ip']}_${i['name']}`).addEventListener('click', () =>
        toggleSelection(s['ip'], i['name'], i['vlan'])
      );
    }
  }
};

const addVlan = async () => {
  const number = getId('input_vlan_number');
  const name = getId('input_vlan_name');
  const gateway = getId('input_vlan_gateway');
  const mask = getId('input_vlan_mask');

  let vlan = {
    number: number.value,
    name: name.value,
    gateway: gateway.value,
    mask: mask.value,
    interfaces: selected.map(e => ({
      switch: e['s'],
      name: e['i'],
      vlan_number: e['v'],
    })),
  };

  let [json, code] = await makeRequest({ type: 'add', vlan }, 'request');

  if (code !== 200) {
    log(json['message'], 'error', `Error ${code}`);
  } else {
    log(
      'Se agregó de forma exitosa la VLAN. Regresa a inicio para verla',
      'ok'
    );

    window.location = '/';
  }
};

document.addEventListener('DOMContentLoaded', async () => {
  switches = await getSwitches();

  setInterfacesEvents(switches);
  getId('bttn_add').addEventListener('click', () =>
    loadingButton('bttn_add', addVlan)
  );
});

import { log } from './modules/log.js';
import { getId } from './modules/helper.js';

let switches = [];
let selected = [];

const getSwitches = async () => [
  {
    ip: '192.168.1.11',
    interfaces: [
      { name: 'FastEthernet1/6', vlan: 1 },
      { name: 'FastEthernet1/7', vlan: 1 },
      { name: 'FastEthernet1/8', vlan: 1 },
      { name: 'FastEthernet1/9', vlan: 10 },
      { name: 'FastEthernet1/10', vlan: 1 },
      { name: 'FastEthernet1/11', vlan: 20 },
      { name: 'FastEthernet1/12', vlan: 1 },
      { name: 'FastEthernet1/13', vlan: 30 },
      { name: 'FastEthernet1/14', vlan: 20 },
      { name: 'FastEthernet1/15', vlan: 10 },
    ],
  },
  {
    ip: '192.168.1.12',
    interfaces: [
      { name: 'FastEthernet1/6', vlan: 1 },
      { name: 'FastEthernet1/7', vlan: 1 },
      { name: 'FastEthernet1/8', vlan: 1 },
      { name: 'FastEthernet1/9', vlan: 1 },
      { name: 'FastEthernet1/10', vlan: 1 },
      { name: 'FastEthernet1/11', vlan: 1 },
      { name: 'FastEthernet1/12', vlan: 1 },
      { name: 'FastEthernet1/13', vlan: 1 },
      { name: 'FastEthernet1/14', vlan: 1 },
      { name: 'FastEthernet1/15', vlan: 1 },
    ],
  },
];

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

const addVlan = () => {
  const number = getId('input_vlan_number').value;
  const name = getId('input_vlan_name').value;
  const gateway = getId('input_vlan_gateway').value;
  const mask = getId('input_vlan_mask').value;

  console.table([number, name, gateway, mask, selected]);
};

document.addEventListener('DOMContentLoaded', async () => {
  switches = await getSwitches();

  setInterfacesEvents(switches);
  getId('bttn_add').addEventListener('click', addVlan);
});

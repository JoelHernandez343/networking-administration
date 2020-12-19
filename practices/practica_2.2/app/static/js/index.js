import { getId } from './modules/helper.js';

let vlans = [];

const getVlans = async () => [
  {
    number: 10,
    name: 'VLAN10',
    net: '192.168.10.0',
    mask: '255.255.255.0',
    gateway: '192.168.10.1',
  },
  {
    number: 20,
    name: 'VLAN20',
    net: '192.168.20.0',
    mask: '255.255.255.0',
    gateway: '192.168.20.1',
  },
  {
    number: 30,
    name: 'VLAN30',
    net: '192.168.30.0',
    mask: '255.255.255.0',
    gateway: '192.168.30.1',
  },
];

const viewVlan = (e, v) => {
  if (e.target.closest(`#delete_vlan_${v}`)) {
    return;
  }

  window.location = `${window.origin}/vlans/${v}`;
};

const deleteVlan = v => {
  getId(`vlan_${v}`).classList.add('hidden');

  console.log('Deleting', v);
};

const setVlansEvents = vlans => {
  for (let v of vlans) {
    getId(`vlan_${v['number']}`).addEventListener('click', e =>
      viewVlan(e, v['number'])
    );

    getId(`delete_vlan_${v['number']}`).addEventListener('click', () =>
      deleteVlan(v['number'])
    );
  }
};

document.addEventListener('DOMContentLoaded', async () => {
  vlans = await getVlans();

  setVlansEvents(vlans);
});

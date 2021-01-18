import { getId, makeRequest, wait } from './modules/helper.js';
import { loadingButton } from './modules/button.js';
import { log } from './modules/log.js';

const getRegisters = async () => {
  let req = {
    type: 'registers',
    interface: {
      router_id: getId('router_id').innerHTML,
      name: getId('interface_name').innerHTML,
    },
  };

  let [json, code] = await makeRequest(req, 'request');

  return code !== 200 ? [] : json['registers'];
};

const graph = (p, datasets, labels) => {
  while (p.lastChild) {
    p.removeChild(p.lastChild);
  }

  let canvas = document.createElement('canvas');
  p.appendChild(canvas);

  let ctx = canvas.getContext('2d');
  let chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets,
    },
  });

  p.style.height = '400px';
};

const updateRegisters = async () => {
  let parentOctects = getId('graph_octects');
  let parentPackages = getId('graph_packages');

  while (true) {
    console.log('Updating');

    let registers = await getRegisters();

    let domain = registers.map(r => {
      let date = new Date(parseInt(r['date']));

      return `${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;
    });

    [
      {
        parent: parentOctects,
        datasets: [
          {
            data: registers.map(r => r['if_inoctets']),
            label: 'Octetos de entrada',
            fill: false,
            borderColor: '#ef4f4f',
            backgroundColor: '#ef4f4f',
          },
          {
            data: registers.map(r => r['if_outoctets']),
            label: 'Octetos de salida',
            fill: false,
            borderColor: '#ee9595',
            backgroundColor: '#ee9595',
          },
        ],
      },
      {
        parent: parentPackages,
        datasets: [
          {
            data: registers.map(r => r['if_inucastpkts']),
            label: 'Paquetes de entrada',
            fill: false,
            borderColor: '#007965',
            backgroundColor: '#007965',
          },
          {
            data: registers.map(r => r['if_outucastpkts']),
            label: 'Paquetes de salida',
            fill: false,
            borderColor: '#00af91',
            backgroundColor: '#00af91',
          },
        ],
      },
    ].forEach(e => graph(e['parent'], e['datasets'], domain));

    await wait(60000);
  }
};

document.addEventListener('DOMContentLoaded', async () => {
  updateRegisters();
});

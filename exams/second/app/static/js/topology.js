let discoverBttn, log;

function getNodes() {
  return {
    discoverBttn: document.getElementById('remote_script'),
    log: document.getElementById('log'),
  };
}

function toggleButton(isActive) {
  let ready = 'hover:bg-blue-500 bg-blue'.split(/\s/);
  let loading = 'pr-2 bg-gray-500'.split(/\s/);

  let content = document.getElementById('remote_script_content');
  let clock = document.getElementById('remote_script_loading');

  clock.classList.toggle('hidden', isActive);
  clock.classList.toggle('inline-block', !isActive);

  content.innerHTML = isActive
    ? 'ACTUALIZAR TOPOLOGÍA Y BASE DE DATOS'
    : 'CARGANDO...';

  ready.forEach(c => discoverBttn.classList.toggle(c, isActive));
  loading.forEach(c => discoverBttn.classList.toggle(c, !isActive));
}

function discover() {
  toggleButton(false);
  discoverBttn.disabled = true;

  fetch(`${window.origin}/requests/discover_topology`, {
    method: 'POST',
  }).then(async res => {
    json = await res.json();

    toggleButton(true);
    discoverBttn.disabled = false;

    if (!res.ok) {
      json['status'] = res.status;
      log.innerHTML = JSON.stringify(json);
    } else {
      log.innerHTML = 'Base de datos completada';
    }

    toggleImage();
  });
}

async function testTopologyImage() {
  return (
    await fetch(`${window.origin}/static/images/network.png`, {
      method: 'GET',
    })
  ).ok;
}

async function toggleImage() {
  isFound = await testTopologyImage();

  let imageSection = document.getElementById('image_found');
  let notImageSection = document.getElementById('image_not_found');

  imageSection.classList.toggle('hidden', !isFound);
  notImageSection.classList.toggle('hidden', isFound);

  if (isFound) {
    imageSection.querySelector('img').src = '/static/images/network.png';
  }
}

document.addEventListener('DOMContentLoaded', () => {
  ({ discoverBttn, log } = getNodes());

  discoverBttn.addEventListener('click', discover);
  toggleImage();
});

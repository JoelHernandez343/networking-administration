let button = document.getElementById('remote_script');
let log = document.getElementById('log');

function toggleButton(isActive) {
  let ready = 'hover:bg-purple-700 bg-purple-600'.split(/\s/);
  let loading = 'pr-2 bg-gray-500'.split(/\s/);

  let content = document.getElementById('remote_script_content');
  let clock = document.getElementById('remote_script_loading');

  clock.classList.toggle('hidden', isActive);
  clock.classList.toggle('inline-block', !isActive);

  content.innerHTML = isActive ? 'EJECUTAR' : 'CARGANDO...';

  ready.forEach(c => button.classList.toggle(c, isActive));
  loading.forEach(c => button.classList.toggle(c, !isActive));
}

button.addEventListener('click', () => {
  console.log('Hello world!');

  toggleButton(false);
  button.disabled = true;

  let config = {
    routers: 'all',
  };

  fetch(`${window.origin}/configure_routing/configure`, {
    method: 'POST',
    body: JSON.stringify(config),
    headers: new Headers({
      'content-type': 'application/json',
    }),
  }).then(async res => {
    json = await res.json();

    toggleButton(true);
    button.disabled = false;

    if (!res.ok) {
      json['status'] = res.status;
      log.innerHTML = JSON.stringify(json);
    } else {
      log.innerHTML = 'Routers configurados!';
    }
  });
});

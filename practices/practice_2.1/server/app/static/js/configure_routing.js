let button = document.getElementById('bttn');
let log = document.getElementById('log_info');

button.addEventListener('click', () => {
  console.log('Hello world!');
  let config = {
    routers: 'all',
  };

  log.innerHTML = 'Loading...';

  fetch(`${window.origin}/configure_routing/configure`, {
    method: 'POST',
    body: JSON.stringify(config),
    headers: new Headers({
      'content-type': 'application/json',
    }),
  })
    .then(res => {
      if (!res.ok) {
        log.innerHTML = 'Cannot configure! :(';
      }

      return res.json();
    })
    .then(json => {
      log.innerHTML = JSON.stringify(json);
    });
});

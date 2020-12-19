const _logToggleStyles = (colors, e, remove = false) =>
  colors
    .map(c => [`bg-${c}-100`, `text-${c}-700`])
    .flat()
    .forEach(c => e.classList.toggle(c, !remove));

const log = (message, type, title = '') => {
  const card = getId('message');
  const cardTitle = card.querySelector('h3');
  const cardMessage = card.querySelector('p');

  cardMessage.innerHTML = message;

  switch (type) {
    case 'ok':
      cardTitle.innerHTML = 'Ok';

      _logToggleStyles(['red', 'yellow'], card, true);
      _logToggleStyles(['green'], card);
      break;

    case 'error':
      cardTitle.innerHTML = 'Error';

      _logToggleStyles(['green', 'yellow'], card, true);
      _logToggleStyles(['red'], card);
      break;

    case 'warn':
      cardTitle.innerHTML = 'Advertencia';

      _logToggleStyles(['red', 'green'], card, true);
      _logToggleStyles(['yellow'], card);
      break;

    default:
      break;
  }

  if (title !== '') {
    cardTitle.innerHTML = title;
  }
};

export { log };

import { getId } from './helper.js';

let queueEvents = [];

const _logToggleStyles = (colors, e, remove = false) =>
  colors
    .map(c => [`bg-${c}-100`, `text-${c}-700`])
    .flat()
    .forEach(c => e.classList.toggle(c, !remove));

const _addEventToCard = id => {
  if (queueEvents.findIndex(e => e['id'] === id) === -1) {
    return;
  }

  queueEvents.push({ id });
  let card = getId(id);
  card.addEventListener('animationend', () => card.classList.add('hidden'));
};

let _currentCard;

const _hideCard = () => getId(_currentCard).classList.add('hidden');

const log = (message, type, title = '', id = 'message') => {
  _currentCard = id;

  const card = getId(id);
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

  card.classList.remove('hidden');
  card.classList.remove('fade-out');
  card.classList.add('fade-in');
  card.removeEventListener('animationend', _hideCard);

  setTimeout(() => {
    card.classList.remove('fade-in');
    card.classList.add('fade-out');
    card.addEventListener('animationend', _hideCard);
  }, 5000);
};

export { log };

function routerExpanders() {
  let arrows = document.querySelectorAll('.router-expander-arrow');

  arrows.forEach(a => {
    a.addEventListener('click', e => {
      let arrow = e.target
        .closest('.router-expander-arrow')
        .getElementsByTagName('img')[0];

      let content = e.target.closest('li').querySelector('.router-expansion');

      content.style.height = content.classList.contains('expansion-opened')
        ? '0px'
        : `${content.scrollHeight}px`;

      arrow.classList.toggle('arrow-rotate');
      content.classList.toggle('expansion-opened');
    });
  });
}

function interfaceExpanders() {
  let arrows = document.querySelectorAll('.interface-expander-arrow');

  arrows.forEach(a => {
    a.addEventListener('click', e => {
      let arrow = e.target
        .closest('.interface-expander-arrow')
        .getElementsByTagName('img')[0];

      let content = e.target
        .closest('li')
        .querySelector('.interface-expansion');

      content.style.height = content.classList.contains('expansion-opened')
        ? '0px'
        : `${content.scrollHeight}px`;

      let parent = e.target
        .closest('li')
        .parentNode.closest('li')
        .querySelector('.router-expansion');

      parent.style.height = content.classList.contains('expansion-opened')
        ? `${parent.scrollHeight - content.scrollHeight}px`
        : `${parent.scrollHeight + content.scrollHeight}px`;

      arrow.classList.toggle('arrow-rotate');
      content.classList.toggle('expansion-opened');
      parent.classList.remove('expansion-opened');
      setTimeout(() => parent.classList.add('expansion-opened'), 0);
    });
  });
}

window.onload = event => {
  routerExpanders();
  interfaceExpanders();
};

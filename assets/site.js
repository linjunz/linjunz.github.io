// All content and navigation remain available when JavaScript is disabled.
const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('#primary-navigation');
if (toggle && nav) {
  const mobile = window.matchMedia('(max-width: 800px)');
  const reset = () => {
    toggle.hidden = !mobile.matches;
    nav.hidden = mobile.matches;
    toggle.setAttribute('aria-expanded', String(!nav.hidden));
    toggle.textContent = 'Menu';
  };
  toggle.addEventListener('click', () => {
    nav.hidden = !nav.hidden;
    toggle.setAttribute('aria-expanded', String(!nav.hidden));
    toggle.textContent = nav.hidden ? 'Menu' : 'Close';
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && mobile.matches && !nav.hidden) {
      reset();
      toggle.focus();
    }
  });
  mobile.addEventListener('change', reset);
  reset();
}

// Preserve the existing home-page StatCounter account, without counting previews.
if (location.hostname === 'linjunz.github.io' && document.body.dataset.page === 'Home') {
  window.sc_project = 11174907;
  window.sc_invisible = 1;
  window.sc_security = '3ecb22fa';
  const counter = document.createElement('script');
  counter.src = 'https://secure.statcounter.com/counter/counter.js';
  counter.async = true;
  document.head.appendChild(counter);
}

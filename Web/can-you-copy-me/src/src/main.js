import { createApp } from 'vue';

import './style-h.css';
import './style-s.css';

import App from './App.vue';

// ----------------------------------------------------------------

const baseListener = (event) => {
  event.stopImmediatePropagation && event.stopImmediatePropagation();
  event.preventDefault && event.preventDefault();
  event.stopPropagation && event.stopPropagation();
};

const hideListener = (event) => {
  document.body.style.display = 'none';
  baseListener(event); // no propagation
};

const hrefListener_1 = (event) => {
  location.href = 'https://www.bilibili.com/video/BV1uT4y1P7CX/';
  baseListener(event); // no propagation
};

const hrefListener_2 = (event) => {
  location.href = 'https://www.bilibili.com/video/BV1GJ411x7h7/';
  baseListener(event); // no propagation
};

// ----------------------------------------------------------------

window.addEventListener('contextmenu', baseListener, { capture: true });
window.addEventListener('selectstart', baseListener, { capture: true });
window.addEventListener('afterprint', hideListener, { capture: true });
window.addEventListener('beforeprint', hideListener, { capture: true });

window.addEventListener('paste', baseListener, { capture: true });
window.addEventListener('cut', baseListener, { capture: true });
window.addEventListener('copy', baseListener, { capture: true });

window.addEventListener('mousedown', baseListener, { capture: true });
window.addEventListener('mouseup', baseListener, { capture: true });
window.addEventListener('mousemove', baseListener, { capture: true });

window.addEventListener('keydown', baseListener, { capture: true });
window.addEventListener('keyup', baseListener, { capture: true });
window.addEventListener('keypress', baseListener, { capture: true });

// ----------------------------------------------------------------

setInterval(() => {
  [window, document.body, document.documentElement].filter((i) => i).forEach((i) => (i.contentEditable = false));
  [...document.getElementsByTagName('div')].filter((i) => i).forEach((i) => (i.contentEditable = false));
  [...document.getElementsByTagName('span')].filter((i) => i).forEach((i) => (i.contentEditable = false));
  [window, document.body, document.documentElement].filter((i) => i).forEach((i) => (i.prompt = () => false));
  [window, document.body, document.documentElement].filter((i) => i).forEach((i) => (i.alert = () => false));
  [window, document.body, document.documentElement].filter((i) => i).forEach((i) => (i.confirm = () => false));
}, 100);

hrefListener_1 && hrefListener_2 && createApp(App).mount('#app'); // mount element

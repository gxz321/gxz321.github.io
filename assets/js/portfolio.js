/* Evidence controls progressively enhance the pre-rendered research pages. */
(() => {
  'use strict';
  document.documentElement.classList.add('js');
  document.querySelectorAll('[data-evidence-view]').forEach(view => {
    const image = view.querySelector('[data-evidence-image]');
    const caption = view.querySelector('[data-evidence-caption]');
    const fullsize = view.querySelector('[data-evidence-fullsize]');
    const controls = Array.from(view.querySelectorAll('[data-image]'));
    if (!image || !caption || controls.length < 2) return;
    let activeRequest = 0;
    controls.forEach(button => button.addEventListener('click', () => {
      if (button.getAttribute('aria-pressed') === 'true') return;
      const request = ++activeRequest;
      const next = new Image();
      next.onload = () => {
        if (request !== activeRequest) return;
        image.src = button.dataset.image;
        image.alt = button.dataset.alt;
        caption.textContent = button.dataset.caption;
        if (fullsize) fullsize.href = button.dataset.image;
        controls.forEach(control => control.setAttribute('aria-pressed', String(control === button)));
      };
      next.onerror = () => { if (request === activeRequest) caption.textContent = 'This view could not load. The current research image remains available.'; };
      next.src = button.dataset.image;
    }));
    view.setAttribute('data-enhanced', '');
  });
})();

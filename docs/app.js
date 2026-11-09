(() => {
  'use strict';
  const root = document.documentElement;
  const toggle = document.querySelector('#theme-toggle');
  const preference = matchMedia('(prefers-color-scheme: dark)');
  const palettes = {
    light: {surfaces:['#F3F2EF','#F9F8F5','#FCFCFA','#FFFFFF'],ink:'#1F1E1C',clay:'#AC4B2B',blue:'#295E90'},
    dark: {surfaces:['#201F1D','#2A2927','#2E2D2B','#33322F'],ink:'#EDEBE6',clay:'#D97757',blue:'#8DB5E0'}
  };
  let chosen;
  try {chosen = localStorage.getItem('claude-paper-theme');} catch {}
  if (!Object.hasOwn(palettes, chosen)) chosen = null;
  function setTheme(theme) {
    root.dataset.theme = theme;
    const p = palettes[theme], dark = theme === 'dark';
    toggle.textContent = dark ? '切换为暖纸' : '切换为暖夜';
    toggle.setAttribute('aria-label', toggle.textContent + '（仅此网页）');
    document.querySelector('meta[name="theme-color"]').content = p.surfaces[0];
    document.querySelector('#palette-mode').textContent = (dark ? '暖夜' : '暖纸') + ' · 四层表面';
    document.querySelectorAll('#surfaces button').forEach((b, i) => {
      b.dataset.copy = p.surfaces[i]; b.style.setProperty('--swatch',p.surfaces[i]); b.style.color = p.ink;
      b.querySelector('code').textContent = p.surfaces[i];
    });
    for (const id of ['clay','blue']) {
      const b = document.getElementById(id); b.dataset.copy = p[id]; b.querySelector('code').textContent = p[id];
    }
    document.querySelector('#blue span').textContent = dark ? '雾蓝 / 链接' : '墨蓝 / 链接';
  }
  setTheme(chosen || (preference.matches ? 'dark' : 'light'));
  toggle.hidden = false;
  toggle.addEventListener('click', () => {
    chosen = root.dataset.theme === 'dark' ? 'light' : 'dark'; setTheme(chosen);
    try {localStorage.setItem('claude-paper-theme',chosen);} catch {}
  });
  preference.addEventListener('change', e => {if (!chosen) setTheme(e.matches ? 'dark' : 'light');});

  const comparison = document.querySelector('#comparison');
  const range = document.querySelector('#compare-range');
  comparison.classList.add('enhanced');
  document.querySelector('.compare-control').hidden = false;
  function compare() {
    comparison.style.setProperty('--pos', range.value + '%');
    document.querySelector('#compare-value').value = range.value + '%';
    range.setAttribute('aria-valuetext', `暖纸 ${range.value}%，暖夜 ${100 - range.value}%`);
  }
  range.addEventListener('input', compare); compare();

  let notificationTimer;
  function notify(message) {
    const status = document.querySelector('#status'); status.textContent = message;
    clearTimeout(notificationTimer); notificationTimer = setTimeout(() => {status.textContent = '';}, 3200);
  }
  async function copy(value) {
    try {await navigator.clipboard.writeText(value); notify('已复制：' + value);}
    catch {notify('无法自动复制，请选中内容手动复制。');}
  }
  document.querySelectorAll('[data-copy]').forEach(b => b.addEventListener('click', () => copy(b.dataset.copy)));
  const copyCommand = document.querySelector('[data-copy-command]'); copyCommand.hidden = false;
  copyCommand.addEventListener('click', () => copy(document.querySelector('#install-command').textContent));

  const dialog = document.querySelector('#lightbox');
  if (typeof dialog.showModal === 'function') {
    document.querySelectorAll('[data-lightbox]').forEach(a => a.addEventListener('click', e => {
      if (e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;
      e.preventDefault(); const source = a.querySelector('img');
      const image = dialog.querySelector('img'); image.src = a.href; image.alt = source.alt;
      dialog.querySelector('p').textContent = source.alt; dialog.showModal();
    }));
    document.querySelector('#close-lightbox').addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', e => {if (e.target === dialog) {const b = dialog.getBoundingClientRect(); if (e.clientX < b.left || e.clientX > b.right || e.clientY < b.top || e.clientY > b.bottom) dialog.close();}});
  }
})();

(() => {
  'use strict';
  const root = document.documentElement;
  const preference = matchMedia('(prefers-color-scheme: dark)');
  const tabs = [...document.querySelectorAll('[data-scene]')];
  const scenes = Object.fromEntries(tabs.map(tab => [tab.dataset.scene,
    [tab.dataset.file, tab.dataset.caption, tab.dataset.paired === 'true']]));
  const params = new URLSearchParams(location.search);
  let chosen = null;
  try { chosen = localStorage.getItem('claude-paper-theme'); } catch {}
  if (!['light','dark'].includes(chosen)) chosen = null;
  if (['light','dark'].includes(params.get('theme'))) chosen = params.get('theme');
  let mode = chosen || (preference.matches ? 'dark' : 'light');
  let scene = Object.hasOwn(scenes, params.get('scene')) ? params.get('scene') : 'chat';
  const modes = [...document.querySelectorAll('[data-mode]')];
  const panel = document.querySelector('#scene-panel');
  const shot = document.querySelector('#scene-image');
  const link = document.querySelector('#scene-link');
  function render() {
    root.dataset.theme = mode;
    document.querySelector('meta[name="theme-color"]').content = mode === 'light' ? '#F9F8F5' : '#2A2927';
    const [file, caption, paired] = scenes[scene];
    const path = 'assets/' + file + (paired ? '' : '-' + mode) + '.png';
    const modeName = modes.find(button => button.dataset.mode === mode).textContent;
    const label = (paired ? '' : modeName + ' · ') + caption;
    // Preserve native pixels for high-density chat previews and the lightbox.
    const fullPath = scene === 'chat' ? path.replace('.png', '-large.png') : path;
    if (scene === 'chat') shot.srcset = `${path} 1600w, ${fullPath} 2560w`;
    else shot.removeAttribute('srcset');
    shot.src = path; shot.alt = label; link.href = fullPath;
    document.querySelector('#scene-caption').textContent = label;
    panel.setAttribute('aria-labelledby','tab-' + scene);
    // Static language pages also work without JS; enhancement preserves the current view.
    const languageLink = document.querySelector('[data-language-link]');
    const target = new URL(languageLink.href);
    target.searchParams.set('scene',scene); target.searchParams.set('theme',mode);
    target.hash = location.hash;
    const current = new URL(location.href);
    if (params.has('scene') || scene !== 'chat') current.searchParams.set('scene',scene);
    else current.searchParams.delete('scene');
    if (params.has('theme') || chosen) current.searchParams.set('theme',mode);
    try {history.replaceState(null,'',current);} catch {}
    languageLink.href = target.href;
    for (const tab of tabs) {
      const active = tab.dataset.scene === scene;
      tab.setAttribute('aria-selected', String(active)); tab.tabIndex = active ? 0 : -1;
    }
    // Mode always controls the page; paired scenes keep their own two-panel image.
    for (const button of modes) button.setAttribute('aria-pressed',String(button.dataset.mode === mode));
  }
  for (const tab of tabs) {
    tab.addEventListener('click', () => {scene = tab.dataset.scene; render();});
    tab.addEventListener('keydown', e => {
      const index = tabs.indexOf(tab);
      const next = {ArrowRight:(index + 1) % tabs.length, ArrowLeft:(index + tabs.length - 1) % tabs.length, Home:0, End:tabs.length - 1}[e.key];
      if (next === undefined) return;
      e.preventDefault(); scene = tabs[next].dataset.scene; render(); tabs[next].focus();
    });
  }
  for (const button of modes) button.addEventListener('click', () => {
    chosen = mode = button.dataset.mode; render();
    try {localStorage.setItem('claude-paper-theme', chosen);} catch {}
  });
  preference.addEventListener('change', e => {if (!chosen) {mode = e.matches ? 'dark' : 'light'; render();}});
  document.querySelectorAll('[data-enhanced]').forEach(el => {el.hidden = false;});
  render();
  window.addEventListener('hashchange', render);

  let timer;
  function notify(text) {
    const status = document.querySelector('#status'); status.textContent = text;
    clearTimeout(timer); timer = setTimeout(() => {status.textContent = '';}, 3500);
  }
  const copy = document.querySelector('[data-copy-command]'); copy.hidden = false;
  copy.addEventListener('click', async () => {
    try {await navigator.clipboard.writeText(document.querySelector('#install-command').textContent); notify(copy.dataset.copied);}
    catch {notify(copy.dataset.copyError);}
  });
  const dialog = document.querySelector('#lightbox');
  if (typeof dialog.showModal !== 'function') return;
  for (const anchor of document.querySelectorAll('[data-lightbox]')) anchor.addEventListener('click', e => {
    if (e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;
    e.preventDefault(); const source = anchor.querySelector('img');
    const image = dialog.querySelector('img'); image.src = anchor.href; image.alt = source.alt;
    dialog.querySelector('p').textContent = source.alt; dialog.showModal();
  });
  document.querySelector('#close-lightbox').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', e => {
    if (e.target !== dialog) return;
    const rect = dialog.getBoundingClientRect();
    if (e.clientX < rect.left || e.clientX > rect.right || e.clientY < rect.top || e.clientY > rect.bottom) dialog.close();
  });
})();

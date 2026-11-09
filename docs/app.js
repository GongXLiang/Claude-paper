(() => {
  'use strict';
  const root = document.documentElement;
  const preference = matchMedia('(prefers-color-scheme: dark)');
  const scenes = {
    chat: ['chat', '对话：公开任务、原生回复与输入框'],
    diff: ['diff', '改动：真实代码差异与行内高亮'],
    editor: ['editor', '代码：语法配色与纸折文件图标'],
    terminal: ['terminal', '终端：实际测试输出与 ANSI 色样'],
    icons: ['icons', '原生文件树拼版：同一套图标，暖纸与暖夜共用', true],
    cli: ['cli-compare', '原生终端拼版：ANSI 随色板变化，真彩色保持程序原色', true]
  };
  let chosen = null;
  try { chosen = localStorage.getItem('claude-paper-theme'); } catch {}
  if (!['light','dark'].includes(chosen)) chosen = null;
  let mode = chosen || (preference.matches ? 'dark' : 'light');
  let scene = 'chat';
  const tabs = [...document.querySelectorAll('[data-scene]')];
  const modes = [...document.querySelectorAll('[data-mode]')];
  const panel = document.querySelector('#scene-panel');
  const shot = document.querySelector('#scene-image');
  const link = document.querySelector('#scene-link');
  function render() {
    root.dataset.theme = mode;
    document.querySelector('meta[name="theme-color"]').content = mode === 'light' ? '#F9F8F5' : '#2A2927';
    const [file, caption, paired] = scenes[scene];
    const path = 'assets/' + file + (paired ? '' : '-' + mode) + '.png';
    const label = (paired ? '' : (mode === 'light' ? '暖纸 · ' : '暖夜 · ')) + caption;
    shot.src = path; shot.alt = label; link.href = path;
    document.querySelector('#scene-caption').textContent = label;
    panel.setAttribute('aria-labelledby','tab-' + scene);
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

  let timer;
  function notify(text) {
    const status = document.querySelector('#status'); status.textContent = text;
    clearTimeout(timer); timer = setTimeout(() => {status.textContent = '';}, 3500);
  }
  const copy = document.querySelector('[data-copy-command]'); copy.hidden = false;
  copy.addEventListener('click', async () => {
    try {await navigator.clipboard.writeText(document.querySelector('#install-command').textContent); notify('安装命令已复制。');}
    catch {notify('无法自动复制，请选中安装命令手动复制。');}
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

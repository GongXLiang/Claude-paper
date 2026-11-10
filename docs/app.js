(() => {
  'use strict';
  const root = document.documentElement;
  const darkPreference = matchMedia('(prefers-color-scheme: dark)');
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const tabs = [...document.querySelectorAll('.scene-tabs [data-scene]')];
  const modes = [...document.querySelectorAll('[data-mode]')];
  const scenes = Object.fromEntries(tabs.map(tab => [tab.dataset.scene, tab.dataset]));
  const panel = document.querySelector('#scene-panel');
  const link = document.querySelector('#scene-link');
  const sizes = document.querySelector('#scene-image').sizes;
  const caption = document.querySelector('#scene-caption');
  const languageLink = document.querySelector('[data-language-link]');
  const params = new URLSearchParams(location.search);
  let chosen = root.dataset.preference || null;
  let rendered = {mode: root.dataset.theme, scene: 'chat'};
  let wanted = {...rendered, scene: Object.hasOwn(scenes, params.get('scene')) ? params.get('scene') : 'chat'};
  let sequence = 0, cleanup, loading, statusTimer;
  const duration = ms => reducedMotion.matches ? 0 : ms;
  const same = (a, b) => a.mode === b.mode && a.scene === b.scene;
  function specFor(state) {
    const entry = scenes[state.scene], paired = entry.paired === 'true';
    const src = `assets/${entry.file}${paired ? '' : '-' + state.mode}.png`;
    const full = entry.large === 'true' ? src.replace('.png', '-large.png') : src;
    const modeName = modes.find(button => button.dataset.mode === state.mode).textContent;
    return {src, full, srcset: full === src ? '' : `${src} 1600w, ${full} 2560w`,
      label: (paired ? '' : modeName + ' · ') + entry.caption};
  }
  function decode(spec, full = false) {
    const img = new Image();
    img.width = 1600; img.height = 1000; img.alt = spec.label;
    if (!full && spec.srcset) {img.sizes = sizes; img.srcset = spec.srcset;}
    img.src = full ? spec.full : spec.src;
    let timeout;
    return Promise.race([img.decode().then(() => img), new Promise((_, reject) => {
      timeout = setTimeout(() => reject(new Error('Image timeout')), 12000);
    })]).finally(() => clearTimeout(timeout));
  }
  const preloaded = new Set();
  function preload(state) {
    if (navigator.connection?.saveData) return;
    const spec = specFor(state);
    if (preloaded.has(spec.src)) return;
    preloaded.add(spec.src);
    decode(spec).catch(() => preloaded.delete(spec.src));
  }
  function moveInk() {
    const active = tabs.find(tab => tab.dataset.scene === wanted.scene);
    const ink = document.querySelector('.tab-ink');
    ink.style.setProperty('--x', active.offsetLeft + 'px');
    ink.style.setProperty('--w', active.offsetWidth);
  }
  function controls(state, scroll = false) {
    for (const tab of tabs) {
      const active = tab.dataset.scene === state.scene;
      tab.setAttribute('aria-selected', String(active)); tab.tabIndex = active ? 0 : -1;
      if (active && scroll) {
        const parent = tab.parentElement;
        if (tab.offsetLeft < parent.scrollLeft || tab.offsetLeft + tab.offsetWidth > parent.scrollLeft + parent.clientWidth)
          parent.scrollTo({left: tab.offsetLeft - (parent.clientWidth - tab.offsetWidth) / 2, behavior: reducedMotion.matches || !root.classList.contains('motion-ready') ? 'instant' : 'smooth'});
      }
    }
    for (const button of modes) button.setAttribute('aria-pressed', String(button.dataset.mode === state.mode));
    document.querySelector('.mode').dataset.active = state.mode;
    moveInk();
  }
  function updateLinks() {
    const current = new URL(location.href), target = new URL(languageLink.href);
    current.searchParams.set('scene', rendered.scene);
    current.searchParams.set('theme', rendered.mode);
    target.search = current.search; target.hash = location.hash;
    languageLink.href = target.href;
    try {history.replaceState(null, '', current);} catch {}
  }
  function notify(text, error = false) {
    const status = document.querySelector('#status');
    clearTimeout(statusTimer); status.classList.toggle('is-error', error); status.textContent = text;
    statusTimer = setTimeout(() => {status.textContent = ''; status.classList.remove('is-error');}, 5000);
  }
  function settled() {
    clearTimeout(loading); panel.classList.remove('loading'); panel.setAttribute('aria-busy', 'false');
  }
  function layerIn(image, ms) {
    clearTimeout(cleanup);
    // Keep an opaque base during rapid changes; never expose an empty stage.
    const layers = [...link.children];
    if (layers.length >= 3) {
      layers.at(-1).style.opacity = '1';
      layers.slice(0, -1).forEach(el => el.remove());
    }
    link.querySelector('[id=scene-image]')?.removeAttribute('id');
    for (const old of link.children) old.setAttribute('aria-hidden', 'true');
    image.id = 'scene-image'; image.className = 'shot-layer';
    image.style.setProperty('--fade', ms + 'ms');
    image.style.opacity = ms ? '0' : '1'; link.append(image);
    // Establish the starting opacity before the next frame's transition.
    image.getBoundingClientRect();
    requestAnimationFrame(() => {if (image.isConnected) image.style.opacity = '1';});
    cleanup = setTimeout(() => {
      if (image !== link.querySelector('#scene-image')) return;
      [...link.children].filter(el => el !== image).forEach(el => el.remove());
    }, ms + 40);
  }
  async function go(next, {initial = false, instant = false} = {}) {
    if (!initial && same(next, wanted)) return same(next, rendered);
    wanted = {...next}; const id = ++sequence;
    controls(next, true); settled();
    if (!initial && same(next, rendered)) return true;
    panel.setAttribute('aria-busy', 'true');
    loading = setTimeout(() => {if (id === sequence) panel.classList.add('loading');}, 300);
    const spec = specFor(next);
    try {
      const image = await decode(spec);
      if (id !== sequence) return false;
      const ms = instant ? 0 : duration(initial ? 160 : next.mode !== rendered.mode ? 240 : 200);
      root.dataset.theme = next.mode;
      document.querySelector('meta[name=theme-color]').content = next.mode === 'light' ? '#F9F8F5' : '#2A2927';
      rendered = {...next};
      if (chosen) {try {localStorage.setItem('claude-paper-theme', chosen);} catch {}}
      caption.textContent = spec.label; link.href = spec.full;
      panel.setAttribute('aria-labelledby', 'tab-' + next.scene);
      panel.dataset.scene = next.scene; panel.dataset.mode = next.mode;
      layerIn(image, ms); settled(); updateLinks(); return true;
    } catch {
      if (id !== sequence) return false;
      wanted = {...rendered}; controls(rendered); settled();
      notify(panel.dataset.loadError, true); return false;
    }
  }
  document.querySelectorAll('[data-enhanced]').forEach(el => {el.hidden = false;});
  const ink = document.createElement('span'); ink.className = 'tab-ink'; ink.ariaHidden = 'true';
  document.querySelector('.scene-tabs').append(ink);
  for (const tab of tabs) {
    tab.addEventListener('click', () => go({...wanted, scene: tab.dataset.scene}));
    tab.addEventListener('focus', () => preload({...wanted, scene: tab.dataset.scene}));
    tab.addEventListener('pointerenter', () => preload({...wanted, scene: tab.dataset.scene}));
    tab.addEventListener('keydown', event => {
      const index = tabs.indexOf(tab);
      const next = {ArrowRight:(index + 1) % tabs.length, ArrowLeft:(index + tabs.length - 1) % tabs.length, Home:0, End:tabs.length - 1}[event.key];
      if (next === undefined) return;
      event.preventDefault(); go({...wanted, scene: tabs[next].dataset.scene}); tabs[next].focus({preventScroll:true});
    });
  }
  for (const button of modes) {
    button.addEventListener('click', () => {chosen = button.dataset.mode; go({...wanted, mode: chosen});});
    button.addEventListener('pointerenter', () => preload({...wanted, mode: button.dataset.mode}));
    button.addEventListener('focus', () => preload({...wanted, mode: button.dataset.mode}));
  }
  darkPreference.addEventListener('change', event => {
    if (!chosen) go({...wanted, mode:event.matches ? 'dark' : 'light'});
  });
  window.addEventListener('resize', moveInk);
  window.addEventListener('hashchange', updateLinks);
  go(wanted, {initial:true});
  const motionReady = () => {requestAnimationFrame(() => root.classList.add('motion-ready')); preload({...wanted, mode:wanted.mode === 'light' ? 'dark' : 'light'});};
  if (document.readyState === 'complete') motionReady(); else window.addEventListener('load', motionReady, {once:true});

  const copy = document.querySelector('[data-copy-command]'); copy.hidden = false;
  const copyLabel = copy.textContent; let copiedTimer;
  copy.addEventListener('click', async () => {
    clearTimeout(copiedTimer);
    try {
      await navigator.clipboard.writeText(document.querySelector('#install-command').textContent);
      copy.textContent = copy.dataset.copiedShort; copy.classList.add('copied'); notify(copy.dataset.copied);
      copiedTimer = setTimeout(() => {copy.textContent = copyLabel; copy.classList.remove('copied');}, 1600);
    } catch {copy.textContent = copyLabel; notify(copy.dataset.copyError, true);}
  });

  let observer;
  const reveal = el => {el.classList.remove('reveal-pending'); observer?.unobserve(el);};
  if ('IntersectionObserver' in window && !reducedMotion.matches && (!location.hash || location.hash === '#main') && scrollY === 0) {
    observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) reveal(entry.target);
    }), {threshold:0.08, rootMargin:'0px 0px -4% 0px'});
    document.querySelectorAll('.section-head,.features article,.folder-rules,.demo>div,.install-layout>div,.scope>div,.palette').forEach((el, index) => {
      if (el.getBoundingClientRect().top < innerHeight) return;
      el.classList.add('reveal-in', 'reveal-pending');
      el.style.setProperty('--delay', el.matches('.features article') ? (index % 3) * 60 + 'ms' : '0ms');
      observer.observe(el);
    });
  }
  document.querySelectorAll('a[href^="#"]').forEach(anchor => anchor.addEventListener('click', () => {
    const target = document.getElementById(anchor.hash.slice(1));
    if (!target) return;
    reveal(target); target.querySelectorAll('.reveal-pending').forEach(reveal);
  }));
  reducedMotion.addEventListener('change', event => {
    if (event.matches) {document.querySelectorAll('.reveal-pending').forEach(reveal); observer?.disconnect();}
  });

  const stats = document.querySelector('[data-install-stats]');
  if (stats) fetch('install-stats.json').then(response => {
    if (!response.ok) throw new Error('Stats unavailable'); return response.json();
  }).then(data => {
    const date = new Date(data.generatedAt);
    if (data.schemaVersion !== 1 || data.plugin !== 'gongxliang.claude-paper' || !Number.isSafeInteger(data.installs) || data.installs < 0 || !Number.isFinite(+date) || +date > Date.now() + 86400000) return;
    stats.querySelector('[data-install-count]').textContent = data.installs.toLocaleString(document.documentElement.lang);
    const time = stats.querySelector('time'); time.dateTime = date.toISOString();
    time.textContent = date.toLocaleDateString(document.documentElement.lang, {timeZone:'UTC',year:'numeric',month:'short',day:'numeric'});
    stats.hidden = false;
  }).catch(() => {}); // The dated build-time snapshot remains useful offline.

  const dialog = document.querySelector('#lightbox');
  if (typeof dialog.showModal !== 'function') return;
  let opener, fromStage = false, lightboxSequence = 0, closingTimer;
  const dialogImage = dialog.querySelector('img');
  const previous = document.querySelector('#previous-preview'), next = document.querySelector('#next-preview');
  async function showLarge(spec) {
    const id = ++lightboxSequence;
    try {
      const large = await decode(spec, true);
      if (id !== lightboxSequence || !dialog.open) return;
      dialogImage.src = large.src; dialogImage.alt = spec.label;
    } catch { /* Keep the already decoded preview if the larger asset fails. */ }
  }
  function closeDialog() {
    if (!dialog.open || dialog.classList.contains('closing')) return;
    dialog.classList.add('closing');
    closingTimer = setTimeout(() => dialog.close(), duration(140));
  }
  for (const anchor of document.querySelectorAll('[data-lightbox]')) anchor.addEventListener('click', event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault(); opener = anchor; fromStage = anchor === link;
    const source = anchor.querySelector('#scene-image') || anchor.querySelector('img');
    dialogImage.src = source.currentSrc || source.src; dialogImage.alt = source.alt;
    dialog.querySelector('p').textContent = source.alt;
    previous.hidden = next.hidden = !fromStage;
    clearTimeout(closingTimer); dialog.classList.remove('closing'); dialog.showModal();
    showLarge({src:source.src, full:anchor.href, label:source.alt});
  });
  async function pageImage(direction) {
    if (!dialog.open || !fromStage) return;
    const index = tabs.findIndex(tab => tab.dataset.scene === wanted.scene);
    const target = {...wanted, scene:tabs[(index + direction + tabs.length) % tabs.length].dataset.scene};
    const id = ++lightboxSequence;
    if (!await go(target, {instant:true}) || !dialog.open || id !== lightboxSequence) return;
    const source = document.querySelector('#scene-image');
    dialogImage.src = source.currentSrc || source.src; dialogImage.alt = source.alt;
    dialog.querySelector('p').textContent = source.alt;
    if (!reducedMotion.matches) dialogImage.animate([{opacity:.45,transform:`translateX(${direction * 12}px)`},{opacity:1,transform:'none'}], {duration:180,easing:'cubic-bezier(.2,0,0,1)'});
    showLarge(specFor(rendered));
  }
  previous.addEventListener('click', () => pageImage(-1)); next.addEventListener('click', () => pageImage(1));
  dialog.addEventListener('keydown', event => {
    if (!fromStage || !['ArrowLeft','ArrowRight'].includes(event.key)) return;
    event.preventDefault(); pageImage(event.key === 'ArrowLeft' ? -1 : 1);
  });
  document.querySelector('#close-lightbox').addEventListener('click', closeDialog);
  dialog.addEventListener('cancel', event => {event.preventDefault(); closeDialog();});
  dialog.addEventListener('close', () => {
    ++lightboxSequence; clearTimeout(closingTimer); dialog.classList.remove('closing'); opener?.focus({preventScroll:true});
  });
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) closeDialog();
  });
})();

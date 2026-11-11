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
  const sheet = panel.parentElement;
  const backSheets = [...document.querySelectorAll('.back-near,.back-far')];
  let cardAnimations = [], lastSwap = -Infinity;
  function settleCards() {
    for (const animation of cardAnimations) animation.cancel();
    cardAnimations = [];
    document.querySelectorAll('.sheet.ghost').forEach(ghost => ghost.remove());
  }
  const sizes = document.querySelector('#scene-image').sizes;
  const caption = document.querySelector('#scene-caption');
  const languageLink = document.querySelector('[data-language-link]');
  const params = new URLSearchParams(location.search);
  const aliases = {terminal:'agents',cli:'agents',icons:'files'};
  if (aliases[params.get('scene')]) params.set('scene', aliases[params.get('scene')]);
  let chosen = root.dataset.preference || null;
  let rendered = {mode: root.dataset.theme, scene: 'chat'};
  let wanted = {...rendered, scene: Object.hasOwn(scenes, params.get('scene')) ? params.get('scene') : 'chat'};
  let sequence = 0, cleanup, loading, statusTimer;
  let manualScene = false, resumeAllowed = false, scrollTrigger;
  const showcase = document.querySelector('.showcase');
  const manual = () => {manualScene = true; resumeAllowed = false; showcase.classList.add('is-manual'); document.querySelector('.paper-stack').classList.remove('paper-enter');};
  const duration = ms => reducedMotion.matches ? 0 : ms;
  const same = (a, b) => a.mode === b.mode && a.scene === b.scene;
  const savePreference = () => {if (chosen) {try {localStorage.setItem('claude-paper-theme', chosen);} catch {}}};
  function specFor(state) {
    const entry = scenes[state.scene], paired = entry.paired === 'true';
    const src = `assets/${entry.file}${paired ? '' : '-' + state.mode}.png`;
    const full = entry.large === 'true' ? src.replace('.png', '-large.png') : src;
    const modeName = modes.find(button => button.dataset.mode === state.mode).textContent;
    return {src, full, srcset: full === src ? '' : `${src} 1600w, ${full} 2880w`,
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
    settleCards(); clearTimeout(cleanup);
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
  function swapCard(image, direction) {
    settleCards(); clearTimeout(cleanup);
    const now = performance.now(), rapid = now - lastSwap < 200;
    lastSwap = now;
    const style = getComputedStyle(sheet.parentElement);
    const value = name => parseFloat(style.getPropertyValue(name));
    const back = amount => `translate(${(value('--back-x') + value('--drift') * 3) * amount}px,${value('--back-y') * amount}px) rotate(${value('--back-r') * amount}deg) scale(${1 + (value('--back-s') - 1) * amount})`;
    const far = `translate(${value('--far-x') - value('--drift') * 3}px,${value('--far-y')}px) rotate(${value('--far-r')}deg) scale(${value('--far-s')})`;
    const replenished = `translate(${value('--back-x')}px,${value('--far-y') + value('--back-y')}px) rotate(${value('--back-r')}deg) scale(${value('--far-s') - .01})`;
    const lift = amount => `translateY(${value('--lift-y') * amount}px) scale(${1 + (value('--lift-s') - 1) * amount})`;
    const easing = 'cubic-bezier(.2,.7,.25,1)';
    const timing = ms => duration(ms * (matchMedia('(max-width:700px)').matches ? .85 : 1));
    let ghost;
    if (!rapid) {
      ghost = document.createElement('div'); ghost.className = 'sheet ghost';
      ghost.setAttribute('aria-hidden', 'true'); ghost.inert = true;
      ghost.style.zIndex = direction > 0 ? '3' : '0';
      const plate = document.createElement('div'); plate.className = 'plate';
      const old = link.querySelector('#scene-image');
      old.removeAttribute('id'); old.removeAttribute('style'); old.className = ''; old.alt = '';
      plate.append(old); ghost.append(plate); sheet.after(ghost);
    }
    image.id = 'scene-image'; image.className = 'shot-layer'; link.replaceChildren(image);
    // The sheet returns to untransformed CSS after every animation (no fill).
    cardAnimations = [sheet.animate(rapid
      ? [{transform: direction > 0 ? back(.4) : lift(.4)}, {transform:'none'}]
      : [{transform:direction > 0 ? back(1) : lift(1),opacity:direction > 0 ? 1 : 0},
         {opacity:1,offset:direction > 0 ? .22 : .6}, {transform:'none',opacity:1}],
      {duration:timing(rapid ? 160 : direction > 0 ? 380 : 280),easing})];
    if (ghost) {
      cardAnimations.push(ghost.animate(direction > 0
        ? [{transform:'none',opacity:1},{transform:lift(1),opacity:0}]
        : [{transform:'none',opacity:1},{opacity:1,offset:.7},{transform:back(1),opacity:0}],
        {duration:timing(direction > 0 ? 170 : 380),easing:direction > 0 ? 'cubic-bezier(.4,0,1,1)' : easing,fill:'forwards'}));
    }
    // Each visible edge advances one slot: back -> middle -> the incoming image.
    // On reverse navigation the paper stack recedes instead. CSS owns the rest poses.
    for (const rear of backSheets) {
      const near = rear.classList.contains('back-near');
      const end = near ? back(1) : far;
      const start = direction > 0 ? (near ? far : replenished) : (near ? 'none' : back(1));
      cardAnimations.push(rear.animate([
        {transform:rapid ? end : start,opacity:near || direction < 0 ? 1 : 0},
        {transform:end,opacity:1}
      ], {duration:timing(rapid ? 160 : near ? 420 : 460),easing}));
    }
    const animations = cardAnimations;
    Promise.allSettled(animations.map(animation => animation.finished)).then(() => {
      ghost?.remove(); animations.forEach(animation => animation.cancel());
      if (cardAnimations === animations) cardAnimations = [];
    });
  }
  async function go(next, {initial = false, instant = false, direction} = {}) {
    if (!initial && same(next, wanted)) {if (same(next, rendered)) savePreference(); return same(next, rendered);}
    wanted = {...next}; const id = ++sequence;
    controls(next, true); settled();
    if (!initial && same(next, rendered)) {savePreference(); updateLinks(); return true;}
    panel.setAttribute('aria-busy', 'true');
    loading = setTimeout(() => {if (id === sequence) panel.classList.add('loading');}, 300);
    const spec = specFor(next);
    try {
      const image = await decode(spec);
      if (id !== sequence) return false;
      const ms = instant ? 0 : duration(initial ? 160 : next.mode !== rendered.mode ? 240 : 320);
      const sceneChanged = next.scene !== rendered.scene;
      const cardDirection = direction ?? Math.sign(tabs.findIndex(t => t.dataset.scene === next.scene) - tabs.findIndex(t => t.dataset.scene === rendered.scene));
      root.dataset.theme = next.mode;
      document.querySelector('meta[name=theme-color]').content = next.mode === 'light' ? '#F9F8F5' : '#2A2927';
      rendered = {...next};
      if (chosen) {try {localStorage.setItem('claude-paper-theme', chosen);} catch {}}
      caption.textContent = spec.label; link.href = spec.full;
      document.querySelector('[data-enlarge]').href = spec.full;
      document.querySelector('.plate-number').textContent = String(tabs.findIndex(t => t.dataset.scene === next.scene) + 1).padStart(2, '0') + ' / 05';
      panel.setAttribute('aria-labelledby', 'tab-' + next.scene);
      panel.dataset.scene = next.scene; panel.dataset.mode = next.mode;
      if (sceneChanged && !initial && ms && typeof sheet.animate === 'function') swapCard(image, cardDirection);
      else layerIn(image, ms);
      settled(); updateLinks(); return true;
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
    tab.addEventListener('click', () => {manual(); go({...wanted, scene: tab.dataset.scene});});
    tab.addEventListener('focus', () => preload({...wanted, scene: tab.dataset.scene}));
    tab.addEventListener('pointerenter', () => preload({...wanted, scene: tab.dataset.scene}));
    tab.addEventListener('keydown', event => {
      const index = tabs.indexOf(tab);
      const next = {ArrowRight:(index + 1) % tabs.length, ArrowLeft:(index + tabs.length - 1) % tabs.length, Home:0, End:tabs.length - 1}[event.key];
      if (next === undefined) return;
      event.preventDefault(); manual(); go({...wanted, scene: tabs[next].dataset.scene}, {direction:event.key === 'ArrowRight' ? 1 : event.key === 'ArrowLeft' ? -1 : undefined}); tabs[next].focus({preventScroll:true});
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
  const motionReady = () => {requestAnimationFrame(() => {
    root.classList.add('motion-ready');
    if (!reducedMotion.matches && performance.now() < 600 && scrollY < 10) {
      document.querySelector('.hero').classList.add('hero-enter');
      document.querySelector('.paper-stack').classList.add('paper-enter');
    }
  }); preload({...wanted, mode:wanted.mode === 'light' ? 'dark' : 'light'});};
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
  const reveal = el => {el.classList.remove('pending'); el.classList.add('visible'); observer?.unobserve(el);};
  if ('IntersectionObserver' in window && !reducedMotion.matches && (!location.hash || location.hash === '#main') && scrollY === 0) {
    observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) reveal(entry.target);
    }), {threshold:0.08, rootMargin:'0px 0px -5% 0px'});
    document.querySelectorAll('.section-heading,.specimen-sheet,.install-layout>div,.appendix details,.palette').forEach(el => {
      if (el.getBoundingClientRect().top < innerHeight) return;
      el.classList.add('reveal', 'pending'); observer.observe(el);
    });
  }
  const stopSequence = () => {scrollTrigger?.kill(true); scrollTrigger = null; showcase.classList.remove('scroll-enabled');};
  document.querySelectorAll('a[href^="#"]').forEach(anchor => anchor.addEventListener('click', event => {
    const target = document.getElementById(anchor.hash.slice(1));
    if (!target) return;
    reveal(target); target.querySelectorAll('.pending').forEach(reveal);
    if (anchor.hash === '#install' && scrollTrigger) {
      event.preventDefault(); stopSequence();
      requestAnimationFrame(() => {target.scrollIntoView({behavior:reducedMotion.matches?'instant':'smooth'}); const url=new URL(location.href);url.hash='install';history.replaceState(null,'',url);updateLinks();target.tabIndex=-1;target.focus({preventScroll:true});});
    }
  }));
  reducedMotion.addEventListener('change', event => {
    if (event.matches) {settleCards(); document.querySelectorAll('.pending').forEach(reveal); observer?.disconnect(); document.querySelector('.paper-stack').classList.remove('paper-enter');}
  });
  if (window.gsap && window.ScrollTrigger && (!location.hash || ['#main','#gallery'].includes(location.hash))) {
    gsap.registerPlugin(ScrollTrigger);
    gsap.matchMedia().add('(min-width: 1024px) and (min-height: 760px) and (prefers-reduced-motion: no-preference)', () => {
      if (navigator.connection?.saveData) return;
      showcase.classList.add('scroll-enabled');
      let scrollIndex = 0;
      const resume = self => {if (manualScene && !resumeAllowed) return; manualScene = false; resumeAllowed = false; scrollIndex = Math.max(0,Math.min(4,Math.round(self.progress*4))); showcase.classList.remove('is-manual'); go({...wanted,scene:tabs[scrollIndex].dataset.scene});};
      scrollTrigger = ScrollTrigger.create({trigger:'.proof-pin',start:'top 18px',end:()=>'+='+Math.min(innerHeight*2.1,2200),pin:true,pinSpacing:true,anticipatePin:1,invalidateOnRefresh:true,
        onEnter:resume,onEnterBack:resume,onLeave:()=>{resumeAllowed=true;},onLeaveBack:()=>{resumeAllowed=true;},
        onUpdate:self => {
          document.querySelector('.paper-stack').style.setProperty('--drift',self.progress.toFixed(3));
          if (manualScene || document.querySelector('#lightbox').open) return;
          const step = self.progress*4;
          let next = scrollIndex;
          if (step > scrollIndex+.58) next = Math.min(4,Math.floor(step+.42));
          if (step < scrollIndex-.58) next = Math.max(0,Math.ceil(step-.42));
          if (next !== scrollIndex) {scrollIndex=next; go({...wanted,scene:tabs[next].dataset.scene});}
        }
      });
      return () => {scrollTrigger?.kill(true); scrollTrigger=null; showcase.classList.remove('scroll-enabled'); document.querySelector('.paper-stack').style.removeProperty('--drift');};
    });
  }

  const statsBlocks = document.querySelectorAll('[data-install-stats]');
  if (statsBlocks.length) fetch('install-stats.json', {cache:'no-cache'}).then(response => {
    if (!response.ok) throw new Error('Stats unavailable'); return response.json();
  }).then(data => {
    const date = new Date(data.generatedAt);
    if (data.schemaVersion !== 1 || data.plugin !== 'gongxliang.claude-paper' || !Number.isSafeInteger(data.installs) || data.installs < 0 || !Number.isFinite(+date) || +date > Date.now() + 86400000) return;
    statsBlocks.forEach(stats => {
      const time = stats.querySelector('time');
      if (+date < Date.parse(time.dateTime)) return;
      stats.querySelector('[data-install-count]').textContent = data.installs.toLocaleString(document.documentElement.lang);
      time.dateTime = date.toISOString();
      time.textContent = date.toLocaleDateString(document.documentElement.lang, {timeZone:'UTC',year:'numeric',month:'short',day:'numeric'});
      stats.hidden = false;
    });
  }).catch(() => {}); // The dated build-time snapshot remains useful offline.

  const dialog = document.querySelector('#lightbox');
  if (typeof dialog.showModal !== 'function') return;
  let opener, fromStage = false, lightboxSequence = 0, closingTimer;
  const dialogImage = dialog.querySelector('img');
  const zoom = document.querySelector('#zoom-preview');
  zoom.addEventListener('click', () => {const detail=dialog.classList.toggle('detail'); zoom.textContent=detail?zoom.dataset.fit:'100%';});
  document.querySelector('[data-enlarge]').addEventListener('click', event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault(); link.click();
  });
  const previous = document.querySelector('#previous-preview'), next = document.querySelector('#next-preview');
  async function showLarge(spec) {
    const id = ++lightboxSequence;
    try {
      const large = await decode(spec, true);
      if (id !== lightboxSequence || !dialog.open) return;
      dialogImage.src = large.src; dialogImage.alt = spec.label; document.querySelector('#original-preview').href = spec.full;
    } catch { /* Keep the already decoded preview if the larger asset fails. */ }
  }
  function closeDialog() {
    if (!dialog.open || dialog.classList.contains('is-closing')) return;
    dialog.classList.add('is-closing');
    closingTimer = setTimeout(() => dialog.close(), duration(140));
  }
  for (const anchor of document.querySelectorAll('[data-lightbox]')) anchor.addEventListener('click', event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault(); manual(); opener = anchor; fromStage = anchor === link;
    const source = anchor.querySelector('#scene-image') || anchor.querySelector('img');
    dialogImage.src = source.currentSrc || source.src; dialogImage.alt = source.alt;
    dialog.querySelector('p').textContent = source.alt;
    previous.hidden = next.hidden = !fromStage;
    clearTimeout(closingTimer); dialog.classList.remove('is-closing'); dialog.classList.remove('detail'); zoom.textContent='100%'; dialog.showModal(); requestAnimationFrame(()=>dialog.classList.add('is-open'));
    showLarge({src:source.src, full:anchor.href, label:source.alt});
  });
  async function pageImage(direction) {
    if (!dialog.open || !fromStage) return;
    manual();
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
    ++lightboxSequence; clearTimeout(closingTimer); dialog.classList.remove('is-closing','is-open'); opener?.focus({preventScroll:true});
  });
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) closeDialog();
  });
})();

(async () => {
  const results=[];
  const check=(ok,label)=>{if(!ok)throw new Error(label);results.push(label);};
  const waitFor=async(test,label)=>{const until=Date.now()+16000;while(!test()){if(Date.now()>until)throw new Error('Timed out: '+label);await new Promise(r=>setTimeout(r,20));}};
  const stage=document.querySelector('#scene-panel');
  const ready=(scene,mode)=>waitFor(()=>stage.dataset.scene===scene&&stage.dataset.mode===mode&&stage.getAttribute('aria-busy')==='false',`${scene}/${mode}`);
  const zh=document.documentElement.lang==='zh-CN';
  check(document.title===(zh?'Claude Paper — 一张纸，两种光':'Claude Paper — One paper, two lights'),'localized title');
  check(document.querySelector('[data-copy-command]').textContent===(zh?'复制':'Copy'),'localized controls');
  for(const tab of document.querySelectorAll('.scene-tabs [data-scene]')) {
    for(const mode of ['light','dark']) {
      tab.click();document.querySelector(`[data-mode=${mode}]`).click();await ready(tab.dataset.scene,mode);
      const shot=document.querySelector('#scene-image');await shot.decode();
      const file=tab.dataset.file+(tab.dataset.paired==='true'?'':'-'+mode)+'.png';
      check(shot.src.endsWith('/'+file),`${tab.dataset.scene}/${mode} asset`);
      check(document.documentElement.dataset.theme===mode,`${tab.dataset.scene}/${mode} theme`);
      check(shot.alt.includes(tab.dataset.caption),`${tab.dataset.scene}/${mode} translated caption`);
      if(tab.dataset.large==='true') {
        check(document.querySelector('#scene-link').href.endsWith('-large.png'),`${mode} native lightbox source`);
        const raw=new Image();raw.src=shot.currentSrc;await raw.decode();
        check(raw.naturalWidth>=Math.min(2560,shot.getBoundingClientRect().width*devicePixelRatio),`${mode} native pixel density`);
      } else check(!shot.hasAttribute('srcset'),'nonlarge scene clears high-density sources');
    }
  }
  document.querySelector('#tab-chat').click();await ready('chat','dark');
  for(let i=0;i<10;i++)document.querySelector(`[data-mode=${i%2?'light':'dark'}]`).click();
  await ready('chat','light');await new Promise(r=>setTimeout(r,320));
  check(document.querySelectorAll('#scene-link img').length===1,'rapid mode switches clean up layers');
  const tabs=[...document.querySelectorAll('.scene-tabs [data-scene]')];
  for(let i=0;i<10;i++)tabs[i%tabs.length].click();
  await ready(tabs[9%tabs.length].dataset.scene,'light');
  check(document.querySelectorAll('#scene-link img').length<=3,'rapid scene switching bounds layers');
  for(const swatch of document.querySelectorAll('.palette>span')) {
    const color=swatch.querySelector('i').getBoundingClientRect(),label=swatch.querySelector('.swatch-label').getBoundingClientRect();
    check(label.left-color.right>=0&&label.left-color.right<=10,'swatch and label stay together');
  }
  document.querySelector('#tab-chat').click();await ready('chat','light');
  check(new URL(location.href).searchParams.get('scene')==='chat','returning to chat updates URL');
  const tab=document.querySelector('#tab-chat');tab.focus();tab.dispatchEvent(new KeyboardEvent('keydown',{key:'End',bubbles:true}));
  await ready('cli','light');check(document.activeElement.id==='tab-cli','keyboard tabs');
  document.querySelector('[data-mode=dark]').click();document.querySelector('#tab-icons').click();await ready('icons','dark');
  const url=new URL(document.querySelector('[data-language-link]').href);
  check(url.searchParams.get('scene')==='icons'&&url.searchParams.get('theme')==='dark','language link preserves state');
  check(url.pathname.endsWith(zh?'index.html':'zh-CN.html'),'language destination');
  const details=document.querySelector('#folders details');details.open=true;
  check(details.querySelectorAll('tbody tr').length===16,'all folder groups');
  check(document.documentElement.scrollWidth<=innerWidth,'no horizontal page overflow');details.open=false;
  const imageLink=document.querySelector('#scene-link');imageLink.focus();imageLink.click();
  const dialog=document.querySelector('#lightbox');check(dialog.open,'lightbox opens');
  check(dialog.querySelector('img').alt===document.querySelector('#scene-image').alt,'lightbox localized alt');
  dialog.dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true}));await ready('cli','dark');
  await waitFor(()=>dialog.querySelector('p').textContent.includes(document.querySelector('#tab-cli').dataset.caption),'lightbox page label');
  check(!document.querySelector('#previous-preview').hidden,'stage lightbox supports paging');
  document.querySelector('#close-lightbox').click();await waitFor(()=>!dialog.open,'lightbox exit');
  check(document.activeElement===imageLink,'lightbox restores focus');
  document.querySelector('.features a').click();check(document.querySelector('#next-preview').hidden,'single-image lightbox has no paging');dialog.close();
  const button=document.querySelector('[data-copy-command]'),original=navigator.clipboard.writeText;
  try {
    navigator.clipboard.writeText=async()=>{};button.click();await new Promise(r=>setTimeout(r,25));
    check(button.textContent===button.dataset.copiedShort,'copy success shown in place');
    check(!document.querySelector('#status').classList.contains('is-error'),'no success toast');
    navigator.clipboard.writeText=async()=>{throw new Error('simulated denial')};button.click();await new Promise(r=>setTimeout(r,25));
    check(document.querySelector('#status').textContent===button.dataset.copyError,'copy failure explained');
  } finally {navigator.clipboard.writeText=original;}
  const stats=document.querySelector('[data-install-stats]');
  await waitFor(()=>!stats.hidden,'statistics');check(/^\d/.test(stats.querySelector('[data-install-count]').textContent)&&!!stats.querySelector('time').dateTime,'official install count has date');
  // A broken target must preserve the rendered image and recover the controls.
  const badTab=tabs.find(t=>t.dataset.scene==='editor'),originalFile=badTab.dataset.file;
  const oldImage=document.querySelector('#scene-image').src;
  badTab.dataset.file='missing-preview-test';badTab.click();
  await waitFor(()=>stage.getAttribute('aria-busy')==='false','missing image fallback');
  check(document.querySelector('#scene-image').src===oldImage,'missing image retains visible content');badTab.dataset.file=originalFile;
  check(document.querySelector('#status').classList.contains('is-error'),'missing image feedback');
  window.scrollTo(0,0);
  return {language:document.documentElement.lang,width:innerWidth,reducedMotion:matchMedia('(prefers-reduced-motion: reduce)').matches,checks:results.length,results};
})()

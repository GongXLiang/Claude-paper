(async () => {
  const results=[];
  function check(ok,label){if(!ok)throw new Error(label);results.push(label);}
  const zh=document.documentElement.lang==='zh-CN';
  check(document.title=== (zh?'Claude Paper — 一张纸，两种光':'Claude Paper — One paper, two lights'),'localized title');
  check(document.querySelector('[data-copy-command]').textContent===(zh?'复制':'Copy'),'localized controls');
  check(document.querySelector('[data-language-link]').textContent===(zh?'English':'中文'),'language switch visible');
  for(const tab of document.querySelectorAll('[data-scene]')) {
    for(const mode of ['light','dark']) {
      tab.click();document.querySelector(`[data-mode=${mode}]`).click();
      const shot=document.querySelector('#scene-image');await shot.decode();
      const file=tab.dataset.file+(tab.dataset.paired==='true'?'':'-'+mode)+'.png';
      check(shot.src.endsWith('/'+file),`${tab.dataset.scene}/${mode} asset`);
      check(document.documentElement.dataset.theme===mode,`${tab.dataset.scene}/${mode} theme`);
      check(shot.alt.includes(tab.dataset.caption),`${tab.dataset.scene}/${mode} translated caption`);
    }
  }
  const tab=document.querySelector('#tab-chat');tab.focus();tab.dispatchEvent(new KeyboardEvent('keydown',{key:'End',bubbles:true}));
  check(document.activeElement.id==='tab-cli'&&document.querySelector('#tab-cli').ariaSelected==='true','keyboard tabs');
  document.querySelector('#tab-icons').click();await document.querySelector('#scene-image').decode();
  const a=document.querySelector('[data-language-link]');const url=new URL(a.href);
  check(url.searchParams.get('scene')==='icons'&&url.searchParams.get('theme')==='dark','language switch preserves scene and mode');
  check(url.pathname.endsWith(zh?'index.html':'zh-CN.html'),'language destination');
  const details=document.querySelector('#folders details');details.open=true;
  check(details.querySelectorAll('tbody tr').length===16,'all 16 folder groups');
  check(details.textContent.includes('plugins')&&details.textContent.includes('output'),'common aliases');
  check(document.documentElement.scrollWidth<=innerWidth,'no horizontal page overflow');details.open=false;
  const imageLink=document.querySelector('#scene-link');imageLink.focus();imageLink.click();
  check(document.querySelector('#lightbox').open,'lightbox opens');
  check(document.querySelector('#lightbox img').alt===document.querySelector('#scene-image').alt,'lightbox localized alt');
  document.querySelector('#close-lightbox').click();
  check(!document.querySelector('#lightbox').open,'lightbox closes');
  const button=document.querySelector('[data-copy-command]');
  const original=navigator.clipboard.writeText;
  try {
    navigator.clipboard.writeText=async()=>{};button.click();await new Promise(r=>setTimeout(r,30));
    check(document.querySelector('#status').textContent===button.dataset.copied,'localized copy success');
    navigator.clipboard.writeText=async()=>{throw new Error('simulated denial')};button.click();await new Promise(r=>setTimeout(r,30));
    check(document.querySelector('#status').textContent===button.dataset.copyError,'localized copy fallback');
  } finally {navigator.clipboard.writeText=original;}
  window.scrollTo(0,0);
  return {language:document.documentElement.lang,width:innerWidth,checks:results.length,results};
})()

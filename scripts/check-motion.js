(async()=>{
 const results=[],assert=(v,label)=>{if(!v)throw Error(label);results.push(label)},sleep=ms=>new Promise(r=>setTimeout(r,ms));
 const stage=document.querySelector('#scene-panel'),root=document.documentElement;
 const ready=async(scene,mode)=>{for(let i=0;i<300;i++){if(stage.dataset.scene===scene&&stage.dataset.mode===mode&&stage.getAttribute('aria-busy')==='false')return;await sleep(20)}throw Error('Stage not ready')};
 document.querySelector('#tab-chat').click();document.querySelector('[data-mode=light]').click();await ready('chat','light');getComputedStyle(root).getPropertyValue('--bg');await sleep(400);getComputedStyle(root).getPropertyValue('--bg');
 const samples=[],dark=document.querySelector('[data-mode=dark]');dark.dispatchEvent(new Event('pointerenter'));await sleep(150);dark.click();
 assert(dark.getAttribute('aria-pressed')==='true','mode control reacts immediately');
 const start=performance.now();while(performance.now()-start<650){samples.push({time:Math.round(performance.now()-start),color:getComputedStyle(root).getPropertyValue('--bg').trim(),alpha:Number(getComputedStyle(document.querySelector('#scene-image')).opacity),layers:document.querySelector('#scene-link').children.length});await new Promise(requestAnimationFrame)}
 assert(new Set(samples.map(x=>x.color)).size>3,'page colors interpolate across frames');
 assert(samples.some(x=>x.alpha>0&&x.alpha<1),'native screenshot crossfades across frames');
 assert(samples.every(x=>x.layers<=3),'animation never exceeds three stage layers');
 await ready('chat','dark');
 const decode=HTMLImageElement.prototype.decode;
 try{
  HTMLImageElement.prototype.decode=function(){return new Promise(resolve=>setTimeout(resolve,800)).then(()=>decode.call(this))};
  const old=document.querySelector('#scene-image').src;
  document.querySelector('#tab-terminal').click();
  assert(document.querySelector('#tab-terminal').getAttribute('aria-selected')==='true','slow image control reacts immediately');
  await sleep(350);
  assert(document.querySelector('#scene-image').src===old&&stage.getAttribute('aria-busy')==='true','slow image keeps previous decoded scene');
  assert(stage.classList.contains('loading'),'slow loading has unobtrusive feedback');
  await ready('terminal','dark');
 }finally{HTMLImageElement.prototype.decode=decode}
 const a=document.querySelector('#scene-link');a.focus();a.click();const dialog=document.querySelector('dialog');
 dialog.dispatchEvent(new Event('cancel',{cancelable:true}));
 assert(dialog.open&&dialog.classList.contains('closing'),'Escape has a closing transition');
 await sleep(200);assert(!dialog.open&&document.activeElement===a,'Escape restores focus after closing');
 return {checks:results.length,results,frames:samples.length,interpolatedColors:new Set(samples.map(x=>x.color)).size,sample:samples.filter((_,i)=>i%6===0)};
})()

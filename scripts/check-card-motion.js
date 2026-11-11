(async () => {
  const results=[], sleep=ms=>new Promise(r=>setTimeout(r,ms));
  const assert=(ok,label)=>{if(!ok)throw Error(label);results.push(label)};
  const panel=document.querySelector('#scene-panel'),sheet=panel.parentElement;
  const ready=async(scene)=>{for(let i=0;i<300;i++){if(panel.dataset.scene===scene&&panel.getAttribute('aria-busy')==='false')return;await sleep(10)}throw Error('Scene timeout: '+scene)};
  const click=scene=>document.querySelector('#tab-'+scene).click();
  const rest=()=>getComputedStyle(sheet).transform==='none'&&!document.querySelector('.ghost')&&!sheet.getAnimations().length;
  const waitRest=async()=>{for(let i=0;i<300;i++){if(rest())return;await sleep(10)}throw Error('Card did not settle')};
  click('chat');await ready('chat');await waitRest();await sleep(250);
  // Preload each scene without changing state.
  await Promise.all(['agents','diff','editor','files'].map(scene=>{const i=new Image();i.src='assets/'+scene+'-'+panel.dataset.mode+'.png';return i.decode()}));
  click('agents');await ready('agents');
  const samples=[];
  for(let i=0;i<30;i++){samples.push({transform:getComputedStyle(sheet).transform,ghosts:document.querySelectorAll('.ghost').length,opacity:getComputedStyle(sheet).opacity});await new Promise(requestAnimationFrame)}
  assert(samples.some(s=>s.transform!=='none'&&s.ghosts===1),'scene changes move a full paper card above a backing sheet');
  assert(samples.every(s=>s.ghosts<=1),'only one outgoing card is present');
  await waitRest();assert(rest(),'settled screenshots have no transforms, ghosts or retained animations');
  click('chat');await ready('chat');
  let frame=sheet.getAnimations()[0]?.effect.getKeyframes()[0];
  assert(frame?.transform.includes('translateY(-'),'reverse scene starts above the stack');
  await waitRest();await sleep(220);assert(rest(),'reverse transition clears its outgoing layer');
  click('files');await ready('files');await waitRest();await sleep(220);
  document.querySelector('#tab-files').dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true}));await ready('chat');
  frame=sheet.getAnimations()[0]?.effect.getKeyframes()[0];
  assert(frame?.transform.startsWith('translate('),'right arrow across last-to-first keeps forward motion');
  await waitRest();await sleep(220);
  document.querySelector('#tab-chat').dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowLeft',bubbles:true}));await ready('files');
  frame=sheet.getAnimations()[0]?.effect.getKeyframes()[0];
  assert(frame?.transform.startsWith('translateY('),'left arrow across first-to-last keeps reverse motion');
  await waitRest();await sleep(220);
  click('chat');await ready('chat');click('agents');await ready('agents');
  assert(!document.querySelector('.ghost'),'rapid changes avoid stacking ghost cards');
  click('diff');click('editor');click('files');await ready('files');await waitRest();await sleep(220);
  assert(rest()&&document.querySelectorAll('#scene-image').length===1,'rapid click burst ends at the last request with one clear image');
  const decode=HTMLImageElement.prototype.decode;
  try{
    HTMLImageElement.prototype.decode=function(){const delay=this.src.includes('/diff-')?350:40;return sleep(delay).then(()=>decode.call(this))};
    click('diff');click('agents');await ready('agents');await sleep(500);await waitRest();
    assert(panel.dataset.scene==='agents'&&rest(),'late decoded images cannot overwrite the latest choice');
    HTMLImageElement.prototype.decode=function(){return Promise.reject(Error('Deliberate image failure'))};
    click('editor');await sleep(100);
    assert(panel.dataset.scene==='agents'&&document.querySelector('#tab-agents').getAttribute('aria-selected')==='true','failed image keeps the current card and restores controls');
  }finally{HTMLImageElement.prototype.decode=decode}
  click('diff');await ready('diff');
  const nextMode=panel.dataset.mode==='dark'?'light':'dark';document.querySelector('[data-mode='+nextMode+']').click();
  for(let i=0;i<300&&panel.dataset.mode!==nextMode;i++)await sleep(10);
  assert(!document.querySelector('.ghost')&&getComputedStyle(sheet).transform==='none','mode switching interrupts card motion without leaving a tilted screenshot');
  await sleep(400);
  assert(document.querySelector('#scene-link').children.length===1,'mode fade removes old image layers');
  return {checks:results.length,results,frames:samples.filter((_,i)=>i%5===0)};
})()



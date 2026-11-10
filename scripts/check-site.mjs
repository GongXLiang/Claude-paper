import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {resolve,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';

const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const manifest=JSON.parse(readFileSync(resolve(root,'orca-plugin.json'),'utf8'));
assert.equal(manifest.execution,'data');
assert.ok(!manifest.main && !manifest.capabilities?.length);
assert.ok(manifest.homepage.startsWith('https://'));
assert.ok(manifest.screenshots.length<=6);
function png(path,width,height,limit){
  const bytes=readFileSync(resolve(root,path));
  assert.equal(bytes.subarray(0,8).toString('hex'),'89504e470d0a1a0a');
  assert.equal(bytes.readUInt32BE(16),width,path);
  assert.equal(bytes.readUInt32BE(20),height,path);
  assert.ok(bytes.length<=limit,path);
  for(let at=8;at<bytes.length;){
    const size=bytes.readUInt32BE(at),type=bytes.toString('ascii',at+4,at+8);
    assert.ok(!['tEXt','zTXt','iTXt','eXIf','acTL'].includes(type),`${path}: ${type}`);
    at+=size+12;
  }
  return bytes.length;
}
assert.ok(manifest.cover.alt?.trim());
png(manifest.cover.path,1600,1000,1024*1024);
let total=0;
const checked=new Set();
for(const asset of manifest.screenshots){
  assert.ok(asset.alt?.trim());assert.ok(asset.caption?.trim());
  total+=png(asset.path,1600,1000,1536*1024);checked.add(asset.path);
}
assert.ok(total<=8*1024*1024);
for(const name of ['chat-light','chat-dark','diff-light','diff-dark','editor-light','editor-dark','terminal-light','terminal-dark','icons','icons-zh','cli-compare','claude-light','claude-dark','codex-light','codex-dark']){
  const path=`docs/assets/${name}.png`;
  if(!checked.has(path))png(path,1600,1000,1536*1024);
}
for(const mode of ['light','dark'])png(`docs/assets/chat-${mode}-large.png`,2560,1600,1536*1024);
png(manifest.icon,256,256,256*1024);
for(const page of ['index.html','zh-CN.html']) {
const html=readFileSync(resolve(root,'docs',page),'utf8');
assert.ok(html.includes('data-language-link'));
assert.ok(html.includes(page==='index.html' ? '<html lang="en"' : '<html lang="zh-CN"'));
assert.ok(!html.includes('{{'),'Unresolved template placeholder');
const allIds=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]),ids=new Set(allIds);
assert.equal(ids.size,allIds.length,'Duplicate HTML id');
for(const match of html.matchAll(/\b(?:src|href)="([^"]+)"/g)){
  const link=match[1];
  if(link.startsWith('https://')) continue;
  if(link.startsWith('#')){if(link.length>1)assert.ok(ids.has(link.slice(1)),link);continue;}
  assert.ok(!link.includes('..')&&!link.includes(':'),link);
  assert.ok(existsSync(resolve(root,'docs',link)),link);
}
for(const match of html.matchAll(/<img\b[^>]*>/g))assert.ok(/\balt="[^"]*"/.test(match[0]),'Image missing alt');
assert.equal([...html.matchAll(/<script\b/g)].length,3);
assert.ok(!/https?:\/\/[^"'\s]+\.(?:js|css|woff)(?![a-z])/i.test(html),'Unexpected external resource');
assert.ok(html.includes('<noscript>'),'Missing static navigation fallback');
assert.ok(html.includes('assets/chat-light-large.png 2560w'),'Missing high-density chat source');
for(const match of html.matchAll(/\bsrcset="([^"]+)"/g)){
  for(const source of match[1].split(',')){
    const [path,width]=source.trim().split(/\s+/);
    assert.ok(existsSync(resolve(root,'docs',path)),path);
    assert.ok(/^\d+w$/.test(width),width);
  }
}
}

const css=readFileSync(resolve(root,'docs/style.css'),'utf8');
assert.ok(css.includes('prefers-reduced-motion:reduce'));
for(const page of ['README.md','README.zh-CN.md','examples/README.md','examples/README.zh-CN.md']) {
  const readme=readFileSync(resolve(root,page),'utf8');
  for(const match of readme.matchAll(/\]\(([^)]+)\)/g)) {
    const path=match[1];
    if(path.startsWith('https://') || path.startsWith('#')) continue;
    assert.ok(existsSync(resolve(root,dirname(page),path.split('#')[0])),`${page}: ${path}`);
  }
}
const folders=JSON.parse(readFileSync(resolve(root,'icons/folders.json'),'utf8'));
const theme=JSON.parse(readFileSync(resolve(root,'icons/theme.json'),'utf8'));
const copy=JSON.parse(readFileSync(resolve(root,'scripts/site-copy.json'),'utf8'));
assert.deepEqual(Object.keys(copy.en).sort(),Object.keys(copy.zh).sort());
assert.equal(new Set(Object.values(folders).flatMap(x=>x.names)).size,Object.keys(theme.folderNames).length);
assert.ok(Object.keys(theme.folderNames).every(name=>!name.includes('/')));
console.log(`Passed: bilingual pages, READMEs and examples; 16 scene/gallery PNGs + 2 native-resolution chat PNGs + identity, asset sizes/metadata, links, alt text, unique IDs and static fallback; store gallery ${(total/1024).toFixed(0)} KiB.`);

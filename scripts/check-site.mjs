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
for(const name of ['chat-light','chat-dark','diff-light','diff-dark','editor-light','editor-dark','terminal-light','terminal-dark','icons','cli-compare']){
  const path=`docs/assets/${name}.png`;
  if(!checked.has(path))png(path,1600,1000,1536*1024);
}
png(manifest.icon,256,256,256*1024);
const html=readFileSync(resolve(root,'docs/index.html'),'utf8');
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
assert.equal([...html.matchAll(/<script\b/g)].length,1);
assert.ok(!/https?:\/\/[^"'\s]+\.(?:js|css|woff)/i.test(html),'Unexpected external resource');
assert.ok(html.includes('<noscript>'),'Missing static navigation fallback');
const css=readFileSync(resolve(root,'docs/style.css'),'utf8');
assert.ok(css.includes('prefers-reduced-motion:reduce'));
const readme=readFileSync(resolve(root,'README.md'),'utf8');
for(const m of readme.matchAll(/docs\/assets\/[a-z-]+\.png/g))assert.ok(existsSync(resolve(root,m[0])),m[0]);
console.log(`Passed: 11 scene PNGs + identity icon, dimensions/metadata, links, alt text, unique IDs and static fallback; store gallery ${(total/1024).toFixed(0)} KiB.`);

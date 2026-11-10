#!/usr/bin/env node
// Copies companion files only. /theme remains the user's explicit selection step.
import {readFile, mkdir, writeFile, lstat} from 'node:fs/promises';
import {homedir} from 'node:os';
import {resolve, dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {parseArgs} from 'node:util';

const {values} = parseArgs({options:{'dry-run':{type:'boolean'},destination:{type:'string'}}});
const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const destination = resolve(values.destination || resolve(process.env.CODEX_HOME || resolve(homedir(), '.codex'), 'themes'));
const files = [];
for (const mode of ['light','dark']) {
  const name = `claude-paper-${mode}.tmTheme`;
  const bytes = await readFile(resolve(root, 'extras/codex', name));
  const path = resolve(destination, name);
  let exists = false;
  try {
    const stat = await lstat(path);
    if (!stat.isFile() || stat.isSymbolicLink()) throw new Error(`Refusing a non-regular destination: ${path}`);
    exists = true;
    if (!bytes.equals(await readFile(path))) throw new Error(`A different theme already exists: ${path}. Keep a backup and resolve it before installing.`);
  } catch (error) {if (error.code !== 'ENOENT') throw error;}
  files.push({path,bytes,exists});
}
if (!values['dry-run']) {
  await mkdir(destination, {recursive:true});
  for (const file of files) if (!file.exists) await writeFile(file.path, file.bytes, {flag:'wx'});
}
for (const file of files) console.log(`${file.exists ? 'Already matches' : values['dry-run'] ? 'Would install' : 'Installed'}: ${file.path}`);
console.log('In Codex CLI run /theme and choose claude-paper-light or claude-paper-dark. config.toml was not changed.');

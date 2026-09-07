#!/usr/bin/env node
// Point d'entrée unique pour piloter un navigateur réel (Brave CDP ou Chromium headless).
// Sous-commandes : launch | fetch <url> | shot <url> <png> | attach (usage programmatique).
// Prérequis Playwright résolu par Node (npm i -g playwright, ou NODE_PATH vers un
// node_modules qui l'a déjà). Voir SKILL.md.
import { writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { dirname } from 'node:path';
import { spawn } from 'node:child_process';
import { platform } from 'node:os';

const DEFAULT_PORT = 9222;
const DEFAULT_PROFILE = platform() === 'win32' ? 'C:/tmp/brave-debug' : '/tmp/brave-debug';

// Normalise la forme du module : selon le chemin de résolution (package "exports" vs
// import file:// direct d'un module CJS), `chromium` peut être un named export ou
// atterrir sur `.default` (CJS interop). On rend les deux formes utilisables.
function normalizePlaywrightModule(m) {
  if (m.chromium) return m;
  if (m.default?.chromium) return m.default;
  throw new Error('forme de module Playwright non reconnue (ni .chromium ni .default.chromium)');
}

async function loadPlaywright() {
  // NODE_PATH n'est PAS consulté par le résolveur ESM de Node (seul CommonJS `require`
  // le lit) — un `import('playwright')` normal ne trouve donc rien via NODE_PATH,
  // même correctement positionné. Deux résolutions qui marchent réellement :
  try {
    return normalizePlaywrightModule(await import('playwright'));
  } catch {
    // 1. npm install -g playwright a été fait -> résolu par le chemin ci-dessus si le
    //    global bin/module path est dans la résolution par défaut de cette install Node.
  }
  const explicit = process.env.PLAYWRIGHT_MODULE;
  if (explicit) {
    try {
      return normalizePlaywrightModule(await import(`file:///${explicit.replace(/\\/g, '/')}`));
    } catch (e) {
      console.error(`✗ PLAYWRIGHT_MODULE défini (${explicit}) mais import impossible : ${e.message}`);
      process.exit(10);
    }
  }
  console.error('✗ Playwright introuvable.');
  console.error('  NODE_PATH ne fonctionne PAS ici : le résolveur ESM de Node ne le lit pas.');
  console.error('  Solutions (voir SKILL.md "Prérequis") :');
  console.error('  - npm install -g playwright   (puis relancer, sans variable particulière)');
  console.error('  - ou : PLAYWRIGHT_MODULE=<chemin absolu>/node_modules/playwright/index.js node pilot.mjs ...');
  process.exit(10);
}

function findBravePath() {
  const candidates = [
    'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe',
    'C:/Program Files (x86)/BraveSoftware/Brave-Browser/Application/brave.exe',
    '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',
    '/usr/bin/brave-browser',
  ];
  return candidates.find(existsSync) || null;
}

async function cdpAlive(port) {
  try {
    const r = await fetch(`http://127.0.0.1:${port}/json/version`, { signal: AbortSignal.timeout(2000) });
    return r.ok;
  } catch { return false; }
}

// --- launch : démarre Brave avec un port de debug dédié + profil isolé. ---
async function cmdLaunch(args) {
  const port = flagValue(args, '--port') || DEFAULT_PORT;
  const profile = flagValue(args, '--profile') || DEFAULT_PROFILE;
  const url = flagValue(args, '--url') || 'about:blank';

  if (await cdpAlive(port)) {
    console.log(`Brave debug déjà actif sur ${port} — rien à faire.`);
    return;
  }
  const brave = findBravePath();
  if (!brave) {
    console.error('✗ Brave introuvable. Chemins testés : voir findBravePath() dans ce script.');
    process.exit(1);
  }
  mkdirSync(profile, { recursive: true });
  const child = spawn(brave, [
    `--remote-debugging-port=${port}`,
    `--user-data-dir=${profile}`,
    url,
  ], { detached: true, stdio: 'ignore' });
  child.unref();

  // Attendre que le port réponde (jusqu'à ~10s).
  for (let i = 0; i < 10; i++) {
    await new Promise(r => setTimeout(r, 1000));
    if (await cdpAlive(port)) {
      console.log(`OK — port debug ${port} actif (profil ${profile}). Logue-toi dans la fenêtre si demandé.`);
      return;
    }
  }
  console.error('✗ Le port debug ne répond pas après 10s. Ferme toute autre instance Brave et réessaie.');
  process.exit(1);
}

// --- attach : usage PROGRAMMATIQUE (import), pas une commande CLI qui produit une sortie utile seule. ---
export async function attachToBrave({ port = DEFAULT_PORT, urlContains = null } = {}) {
  const pw = await loadPlaywright();
  const { chromium } = pw;
  if (!(await cdpAlive(port))) {
    throw new Error(`Brave debug ne répond pas sur ${port} — lance d'abord: node pilot.mjs launch`);
  }
  const browser = await chromium.connectOverCDP(`http://127.0.0.1:${port}`);
  const ctx = browser.contexts()[0];
  let page = urlContains ? ctx.pages().find(p => p.url().includes(urlContains)) : ctx.pages()[0];
  if (!page) page = await ctx.newPage();
  await page.bringToFront();
  return { browser, page };
}

async function cmdAttachCli() {
  console.log('`attach` est un usage programmatique : importer `attachToBrave` depuis ce fichier.');
  console.log('Exemple :');
  console.log(`  import { attachToBrave } from 'file:///.../browser-pilot/scripts/pilot.mjs';`);
  console.log(`  const { browser, page } = await attachToBrave({ urlContains: 'chatgpt.com' });`);
  console.log('Voir references/recettes.md pour un exemple complet (ex. bouton Télécharger Grok).');
}

// --- fetch : page rendue -> texte/markdown, contournement 403 anti-bot via Chromium réel. ---
async function cmdFetch(args) {
  const url = args[0];
  if (!url) usage('fetch <url> [--out <fichier>]');
  const out = flagValue(args, '--out');
  const pw = await loadPlaywright();
  const { chromium } = pw;
  const browser = await chromium.launch({ headless: true });
  try {
    const ctx = await browser.newContext({
      userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
      locale: 'fr-FR',
    });
    const page = await ctx.newPage();
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 40000 });
    await page.waitForTimeout(2500); // laisser le JS se rendre (SPA, anti-bot challenge)
    const title = await page.title();
    const text = await page.evaluate(() => document.body.innerText);
    const md = `# ${title}\n\nSource: ${url}\n\n${text}`;
    if (out) {
      mkdirSync(dirname(out), { recursive: true });
      writeFileSync(out, md, 'utf8');
      console.log(`✓ → ${out} (${md.length} caractères)`);
    } else {
      console.log(md);
    }
  } finally {
    await browser.close();
  }
}

// --- shot : capture d'écran plein page. ---
async function cmdShot(args) {
  const url = args[0], outPath = args[1];
  if (!url || !outPath) usage('shot <url> <fichier.png>');
  const pw = await loadPlaywright();
  const { chromium } = pw;
  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage();
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 40000 });
    await page.waitForTimeout(1500);
    mkdirSync(dirname(outPath), { recursive: true });
    await page.screenshot({ path: outPath, fullPage: true });
    console.log(`✓ → ${outPath}`);
  } finally {
    await browser.close();
  }
}

function flagValue(args, flag) {
  const i = args.indexOf(flag);
  return i > -1 ? args[i + 1] : null;
}

function usage(msg) {
  console.error(`usage: node pilot.mjs ${msg}`);
  process.exit(2);
}

// --- dispatch ---
const [, , cmd, ...rest] = process.argv;
switch (cmd) {
  case 'launch': await cmdLaunch(rest); break;
  case 'fetch': await cmdFetch(rest); break;
  case 'shot': await cmdShot(rest); break;
  case 'attach': await cmdAttachCli(); break;
  default:
    console.log('usage: node pilot.mjs <launch|fetch|shot|attach> ...');
    console.log('  launch [--url <url>] [--port 9222] [--profile <dossier>]');
    console.log('  fetch <url> [--out <fichier.md>]');
    console.log('  shot <url> <fichier.png>');
    console.log('  attach   (usage programmatique — voir SKILL.md)');
    process.exit(cmd ? 2 : 0);
}

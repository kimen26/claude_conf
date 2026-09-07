# Recettes — pilotage navigateur

## 403 Cloudflare / anti-bot (ex. Grokipedia)

Quand un fetch HTTP simple (ou l'outil de fetch d'un agent) renvoie 403/Forbidden ou un
contenu vide sur un site protégé, ce n'est pas un mur — un vrai navigateur (Chromium
réel, moteur JS complet, empreinte TLS/headers normale) passe là où un fetcher minimal
est bloqué.

```bash
node scripts/pilot.mjs fetch https://exemple-protege.com --out C:/tmp/page.md
```

Prouvé en pratique : un fetch simple = 403 sur un site anti-bot ; le même contenu via
Chromium headless = 200, contenu complet. Un fetcher HTTP basique (WebFetch générique)
ne récupère parfois que des métadonnées (titre, URL) sans le contenu protégé — le
navigateur réel est le fallback pour le **texte complet**.

Pour un lot de pages, appeler `fetch` en série (ou en tâche de fond) plutôt qu'ouvrir un
navigateur par page — réutiliser une seule instance si le volume est important (au-delà
d'une dizaine de pages, adapter `pilot.mjs` pour garder le `browser` ouvert entre appels
plutôt que le relancer à chaque `fetch`).

## Bouton Télécharger vs URL directe (ex. Grok)

Sur certains sites de génération d'images (Grok observé), l'URL de l'image affichée en
DOM sert une **variante compressée/floue** (même dimensions, poids très inférieur,
rendu baveux), tandis que le bouton « Télécharger »/« Download » de l'UI donne
l'original en pleine qualité.

**Ne jamais** faire `page.request.get(urlDirecte)` en pensant récupérer la version
finale — vérifier d'abord si un bouton de téléchargement existe et l'utiliser :

```js
import { attachToBrave } from 'file:///.../browser-pilot/scripts/pilot.mjs';
const { browser, page } = await attachToBrave({ urlContains: 'exemple.com' });

const img = page.locator('img[src*="/generated/"]').first();
await img.hover();                                   // révèle souvent la barre d'actions
const btn = page.getByRole('button', { name: /télécharger|download/i }).first();
const [dl] = await Promise.all([
  page.waitForEvent('download', { timeout: 20000 }),
  btn.click({ force: true }),
]);
await dl.saveAs('sortie.png');
await browser.close(); // ferme la connexion CDP, PAS Brave lui-même
```

Si aucun bouton n'existe et que l'URL directe est bloquée par CORS depuis `fetch()`
mais pas depuis Playwright (qui porte les cookies de session), `page.request.get(url)`
reste la méthode pour l'auth — mais vérifier la taille/qualité du fichier obtenu avant
de l'utiliser en prod (comparer poids/netteté avec un téléchargement manuel une fois).

## Piloter un projet logué (ChatGPT, Grok, tout SPA avec compte)

1. `node scripts/pilot.mjs launch --url https://exemple.com/` une première fois, se
   loguer manuellement dans la fenêtre Brave ouverte. Le profil dédié (`--profile`,
   par défaut `C:/tmp/brave-debug`) garde la session d'une fois sur l'autre — Brave
   peut rester ouvert entre deux exécutions de script.
2. Dans un script séparé, `import { attachToBrave } from '.../pilot.mjs'` pour
   récupérer une `page` déjà connectée, chercher l'onglet correspondant
   (`urlContains`), et piloter le site à la manière du site (sélecteurs de zone de
   texte, bouton d'envoi, détection de connexion) :

```js
const { browser, page } = await attachToBrave({ urlContains: 'exemple.com' });
if (await page.getByRole('button', { name: /log in|se connecter/i }).count() > 0) {
  console.log('PAS LOGUÉ — se loguer dans la fenêtre Brave puis relancer.');
  process.exit(2);
}
const box = page.locator('textarea, div[contenteditable="true"]').first();
await box.click();
await box.fill('mon prompt');
await page.keyboard.press('Enter');
// ... attendre le résultat attendu (polling sur un sélecteur), voir le pattern
// "attendre une nouvelle image" ci-dessous.
await browser.close(); // ne ferme JAMAIS Brave lui-même, juste la connexion CDP
```

### Attendre un résultat asynchrone (ex. génération d'image)

Poller un sélecteur en comparant l'état "avant" / "après" plutôt qu'un simple délai
fixe — un délai fixe est soit trop court (résultat pas prêt), soit trop long (gaspille
du temps) :

```js
const before = await page.locator('img[src*="generated"]').evaluateAll(els => els.map(e => e.src));
// ... envoyer le prompt ...
const start = Date.now();
let url = null;
while (Date.now() - start < 200000) {
  const cur = await page.locator('img[src*="generated"]').evaluateAll(els => els.map(e => e.src));
  url = cur.find(u => !before.includes(u));
  if (url) break;
  await page.waitForTimeout(2000);
}
```

Détecter aussi les messages de quota/limite dans le texte de la page
(`/limite|rate limit|try again later/i`) pour sortir proprement plutôt que timeout.

## Pièges Windows

- **Chemins** : toujours des slashes avant (`C:/tmp/...`), même sous PowerShell —
  évite les soucis d'échappement de backslash dans les chaînes JS/JSON.
- **`Start-Process`/`spawn`** : lancer Brave en détaché (`detached: true, stdio:
  'ignore'` en Node, ou `Start-Process` en PowerShell) pour ne pas bloquer le script
  appelant — Brave doit survivre à la fin du script qui l'a lancé.
- **Un seul process Brave à la fois sur un port donné** : si le port CDP ne répond
  pas après lancement, une autre instance Brave (profil par défaut, sans
  `--remote-debugging-port`) tourne peut-être déjà et bloque le nouveau profil — la
  fermer avant de relancer.
- **Profil dédié obligatoire** : ne jamais lancer avec le profil Brave par défaut de
  l'utilisateur — un `--user-data-dir` séparé isole la session pilotée de la
  navigation humaine normale et évite tout conflit de verrou de profil.

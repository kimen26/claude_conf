---
name: browser-pilot
description: Piloter un navigateur réel (Brave via CDP, ou Chromium headless) pour contourner un 403 anti-bot, récupérer une page rendue en markdown/texte, prendre une capture, ou piloter un site logué (ChatGPT, Grok) depuis un autre script. Contient la doctrine d'accès au web (WebSearch, WebFetch, curl, JSON embarqué, curl_cffi, Playwright, Brave CDP, Claude in Chrome, context7) et le diagnostic anti-bot. Auto-trigger sur piloter le navigateur, Brave CDP, Playwright, contourner 403, anti-bot, scraper, ChatGPT/Grok logué, capture d'écran de page, quel outil web.
disable-model-invocation: true
---

# browser-pilot

Point d'entrée unique pour tout pilotage de navigateur : `scripts/pilot.mjs`.
Remplace les implémentations dupliquées (lancement Brave, fetch anti-403, capture)
qui existaient en plusieurs endroits d'un même projet — voir
`references/migration-maxplay.md` pour la table de correspondance MaxPlay.

`disable-model-invocation: true` : ce skill ne s'auto-déclenche jamais sur simple
mention dans la conversation. Il s'invoque explicitement par `/browser-pilot` ou en
important son script — coût zéro tant qu'il n'est pas appelé.

## Prérequis

Playwright doit être résolu par Node. **`NODE_PATH` ne fonctionne PAS** : c'est un
mécanisme CommonJS (`require`), le résolveur ESM (`import`) de Node ne le consulte
jamais — testé et confirmé sur cette machine. Deux options qui marchent réellement,
aucune copie de fichier :
1. `npm install -g playwright` (une fois, sur la machine) — le script fait alors un
   `import('playwright')` normal qui aboutit.
2. Sinon, pointer explicitement le fichier d'entrée d'une install existante (ex. un
   projet qui l'a déjà installé pour ses propres tests) via la variable
   `PLAYWRIGHT_MODULE` :
   ```bash
   PLAYWRIGHT_MODULE="<chemin absolu>/node_modules/playwright/index.js" node scripts/pilot.mjs shot https://example.com out.png
   ```

Le script tente `import('playwright')` normal, puis `PLAYWRIGHT_MODULE` si définie ;
s'il échoue, il affiche l'erreur et comment la résoudre — il ne télécharge ni ne copie
jamais Playwright lui-même.

## Sous-commandes

```bash
node scripts/pilot.mjs launch [--url <url>] [--port 9222] [--profile <dossier>]
node scripts/pilot.mjs fetch <url> [--out <fichier.md|.txt>]
node scripts/pilot.mjs shot <url> <fichier.png>
node scripts/pilot.mjs attach   # usage programmatique, voir plus bas
```

- **`launch`** — démarre Brave avec un port CDP dédié et un profil isolé (ne touche
  pas la navigation habituelle), reste ouvert d'une session à l'autre pour garder les
  logins (ChatGPT, Grok, etc.). Si le port répond déjà, ne relance rien.
- **`fetch <url>`** — ouvre la page dans un Chromium headless, attend le rendu JS,
  extrait le texte/markdown. Le contournement standard d'un 403 Cloudflare/anti-bot
  (ex. Grokipedia) : un navigateur réel passe là où un fetch HTTP simple est bloqué.
- **`shot <url> <png>`** — capture d'écran plein page.
- **`attach`** — n'est pas un usage CLI direct : le module exporte une fonction
  `attachToBrave()` qu'un AUTRE script importe pour récupérer une `page` Playwright
  déjà connectée au Brave lancé par `launch`, et piloter un site logué (ChatGPT, Grok)
  à sa manière. Voir `references/recettes.md` pour l'exemple d'usage.

## Recettes courantes

Contournement 403, bouton Télécharger Grok (pleine qualité vs vignette compressée),
piloter un projet ChatGPT logué, pièges Windows (chemins, profils, `Start-Process`) :
tout est dans `references/recettes.md` — à lire avant d'écrire un script qui pilote un
site précis par-dessus `attachToBrave()`.

## Test de fumée

```bash
node scripts/pilot.mjs shot https://example.com C:/tmp/browser-pilot-test/example.png
```
Puis **ouvrir le PNG produit** (outil de lecture d'image) pour vérifier qu'il n'est pas
vide — un exit code 0 ne prouve jamais qu'une image affiche quelque chose.

## Références

- `references/doctrine-acces-web.md` — **lire d'abord** : quel outil dans quel ordre (curl avant navigateur), diagnostic anti-bot en 5 questions, convention de ports CDP par projet, état de l'art 2026
- `references/recettes.md` — 403 Cloudflare, bouton Télécharger, profil persistant, pièges Windows
- `references/migration-maxplay.md` — table des scripts projet MaxPlay → équivalent ici

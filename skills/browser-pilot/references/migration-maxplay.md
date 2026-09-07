# Migration MaxPlay — table de correspondance

Seul fichier de ce skill autorisé à citer des chemins MaxPlay. Documente comment les
3 implémentations dupliquées identifiées dans l'audit (`memory/audits/2026-09-03-archi-claude-infra.md`
point 14) se brancheraient sur `browser-pilot`.

| Script projet MaxPlay | Rôle actuel | Équivalent `browser-pilot` |
|---|---|---|
| `.claude/skills/dino-images-lunii/scripts/launch-brave.ps1` | Lance Brave debug port 9222, profil `c:/tmp/brave-debug`, ouvre ChatGPT | `pilot.mjs launch --url https://chatgpt.com/` (même port par défaut, même logique idempotente) |
| `.claude/skills/dino-images-lunii/scripts/gpt-gen.mjs` | Connecte CDP, trouve/ouvre l'onglet ChatGPT, envoie un prompt, poll une nouvelle image, la télécharge via `fetch` in-page | `attachToBrave({ urlContains: 'chatgpt.com' })` puis logique spécifique ChatGPT par-dessus (le pattern d'attente et de détection de login est dans `references/recettes.md`) |
| `.claude/skills/dino-images-lunii/scripts/gpt-gen-dino.mjs` | Variante dino du précédent (prompts direction artistique paléoart) | Même refactor — la partie pilotage brave/CDP devient un `import` de `pilot.mjs`, la partie prompt/DA reste dans le script dino |
| `.claude/skills/dino-images-lunii/scripts/grok-gen-dino.mjs` | Idem côté projet Grok, avec détection de limite/quota et téléchargement via `page.request.get()` (URL directe — qualité dégradée, cf. leçon `reference_grok_image_download_button.md`) | `attachToBrave()` + recette « bouton Télécharger vs URL directe » de `references/recettes.md` — **corrige au passage un bug connu** (le script actuel télécharge des images Grok en qualité dégradée) |
| `.claude/skills/dino-images-lunii/scripts/batch-helpers.mjs` | State de batch (quota journalier, pause adaptative, retry) — pas du pilotage navigateur en soi | Hors périmètre de `browser-pilot` : reste un helper de pôle, orthogonal au pilotage (à conserver côté dino) |
| `studio/minijeux/tests/{run.mjs,compat.mjs}` | Harnais Playwright pour tester les mini-jeux (36 specs), pas du pilotage de site tiers logué | Hors périmètre : ce sont des tests e2e classiques Playwright, pas des recettes de contournement. La seule chose réutilisable est le `node_modules/playwright` local lui-même (voir SKILL.md "Prérequis") — `browser-pilot` documente comment le résoudre, ne le copie pas. |
| leçon `reference_webfetch_403_playwright.md` | Contournement 403 Grokipedia via script Playwright ad hoc dans `c:/tmp/` | `pilot.mjs fetch <url> --out fichier.md` — même pattern (headless, waitForTimeout, `body.innerText`), généralisé en sous-commande |

## Ce qui ne migre PAS ici

- La direction artistique / les prompts dino (`gpt-gen-dino.mjs`, `grok-gen-dino.mjs`
  portent une identité visuelle propre au pôle dino) — reste dans
  `.claude/skills/dino-images-lunii/` et `.claude/skills/dino-paleoart/`, qui
  importeraient `attachToBrave` plutôt que de réimplémenter la connexion CDP.
- Le state de batch/quota (`batch-helpers.mjs`) — logique métier de pôle, pas de
  pilotage navigateur.
- Les specs Playwright de test des mini-jeux (`studio/minijeux/tests/`) — ce sont des
  tests, pas des recettes de contournement ou de pilotage de site tiers.

## Étape suivante si la migration est décidée

Remplacer, dans `gpt-gen.mjs`/`gpt-gen-dino.mjs`/`grok-gen-dino.mjs`, le bloc
`chromium.connectOverCDP(...)` + recherche de page par un simple
`import { attachToBrave } from '<chemin>/browser-pilot/scripts/pilot.mjs'` — la partie
spécifique (sélecteurs ChatGPT/Grok, détection de quota, prompt de direction
artistique) reste dans les scripts dino, qui deviennent plus courts et n'ont plus
chacun leur propre copie de la logique de connexion.

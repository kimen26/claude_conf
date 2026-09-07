# Doctrine d'accès au web — quel outil, dans quel ordre

> Consolidé le 2026-09-07 à partir de trois projets (MaxPlay, IArtcane, IArtscan) et
> d'une recherche sur l'état de l'art 2026. Ce fichier est **normatif** : il décrit la
> réalité courante et se corrige quand la réalité change.

## Les besoins couverts

1. **Lire** une page pour en extraire du contenu (texte, prix, JSON, image).
2. **Interagir** : naviguer, chercher dans un site, lancer un prompt sur un chat
   (ChatGPT, Grok), télécharger une photo, capturer un écran (tuto, image d'objet).
3. **Passer les anti-bots** : 403 Cloudflare, pages rendues en JS (LinkedIn, Kayak,
   sites d'enchères), CAPTCHA, login.
4. **Économiser** : tokens, temps, quota.

## La hiérarchie — du moins cher au plus cher

| Situation | Outil | Coût |
|---|---|---|
| Trouver un domaine, une page, un titre | `WebSearch` | Faible. Rend titre + URL seulement, jamais le contenu |
| Lire une doc publique, une page simple, poser une question dessus | `WebFetch` | Moyen. Résumé par un petit modèle, tronqué à 100 Ko, cache 15 min |
| Lire le HTML exact, un JSON, un `robots.txt`, un HEAD de déploiement | `curl` | Quasi nul. Aucun token gaspillé, scriptable en boucle |
| Le HTML arrive mais la donnée semble absente | `curl` + chercher le JSON embarqué | Quasi nul |
| 403 sans challenge JS (empreinte TLS reconnue) | `curl_cffi` — **essayer plusieurs profils** (`chrome`, `safari17_0`, `firefox`) | Quasi nul. **Validé** : Catawiki, Bukowskis, et Chrono24 en profil Safari |
| Vraie SPA, contenu rendu en JS, naviguer, cliquer, remplir, capturer | `agent-browser` (CLI, Chrome réel, 200-400 tokens par page) | Faible en tokens. **Défaut pour toute interaction** |
| Turnstile / « Vérifiez que vous êtes humain » | `agent-browser --headed` | Faible. **Validé** : Chrono24 passe seul en fenêtre visible |
| Fetch texte ou capture depuis un script Node existant | `pilot.mjs fetch` / `shot` (Chromium headless) | Moyen. Headless se fait bloquer plus souvent que agent-browser |
| Site logué, CAPTCHA, prompt sur un chat, téléchargement d'image | `pilot.mjs launch` puis `attachToBrave()` (Brave via CDP, profil persistant) | Élevé mais unique : le login se fait une fois à la main, les scripts suivants en profitent |
| Vérification visuelle rapide sur MON navigateur déjà logué | Claude in Chrome (extension) | Élevé en tokens, à réserver aux sites de confiance |
| Doc à jour d'une bibliothèque (API Playwright, etc.) | `context7` (MCP) | Sans rapport avec le navigateur, voir plus bas |

**Règle d'or : curl d'abord, navigateur en dernier.** Un navigateur ne s'ouvre que
quand curl a prouvé qu'il ne suffisait pas. `WebSearch` sert à trouver, jamais à lire :
sur une fiche de lot, le prix adjugé ne figure quasi jamais dans l'extrait. Chercher une
donnée précise par WebSearch échoue par construction. Constaté : 7 agents, ~110 requêtes,
zéro prix.

## Ce que chaque outil fait vraiment

### WebSearch
Rend une liste de titres et d'URL. Le contenu de page n'est pas transmis. Pas de limite
officielle documentée par Anthropic ; le « ~200 par session » lu dans un CLAUDE.md projet
est une mesure empirique, à traiter comme estimation prudente. Filtres `allowed_domains`
et `blocked_domains` utiles pour cibler un site.

### WebFetch
Télécharge la page, convertit le HTML en markdown, tronque à 100 Ko, puis un petit
modèle répond au `prompt` fourni. L'agent ne voit jamais la page brute, seulement la
réponse. Cache de 15 min par URL. Bloqué par les anti-bots et aveugle sur les pages JS.
Les redirections vers un autre hôte ne sont pas suivies. Bon pour de la doc, mauvais
pour extraire une valeur exacte.

### curl
Le défaut pour lire. HTML tel que le serveur l'a produit, aucun JS exécuté.

```bash
curl -sL -A "Mozilla/5.0" --max-time 30 "https://exemple.com/lot/123"
```

Beaucoup de sites qu'on croit « JS only » livrent la donnée dans un JSON embarqué.
Avant de conclure à une SPA, chercher dans le HTML :

```bash
curl -sL -A "Mozilla/5.0" "$URL" | grep -oE '__NEXT_DATA__|data-react-props="[^"]*"|application/ld\+json|/api/|wp-json' | head
```

Exemple : Auctionet affiche « Bidding / Loading… » à l'écran alors que le prix est dans
`data-react-props`. Un cas jugé « atteignable seulement par navigateur » est tombé ainsi.

### curl_cffi — la piste anti-403 sans navigateur
Un 403 sur une UA Chrome complète, mais 200 sur une UA courte, signale une détection par
cohérence UA / empreinte TLS (JA3/JA4). `curl_cffi` (binding Python de curl-impersonate)
imite l'empreinte TLS d'un vrai Chrome. Mesure rapportée : 16 domaines sur 20 débloqués.
Ne passe pas les challenges JS ni Turnstile : là, c'est navigateur ou rien.

```bash
pip install curl_cffi
python -c "from curl_cffi import requests; r=requests.get('$URL', impersonate='chrome'); print(r.status_code, len(r.text))"
```

Statut : **validé le 2026-09-07** (tableau des tests plus bas). Catawiki passe de 403 à 200, Bukowskis idem. **Chrono24 aussi, mais seulement en profil Safari** (`safari17_0` / `safari18_0` / `safari` : 200, ~705 Ko, alors que `chrome`, `firefox135`, `edge101` restent en 403). Contre-vérifié depuis MaxPlay le soir même sur 9 essais espacés : **un profil Safari donné réussit environ 4 fois sur 5**, jamais 5/5 (`safari17_0` a rendu 403 à 2 essais, `safari` à 1, `safari15_5` à tous). Le blocage est donc partiellement aléatoire par requête : **en cas de 403, réessayer avec un autre profil Safari avant de conclure**. LinkedIn répond 999 (mur de login, rien à voir avec le TLS).

⚠️ **Le profil n'est pas un détail : c'est le paramètre décisif.** Essayer au moins un profil de chaque famille avant de conclure à un blocage :

```bash
for p in chrome safari17_0 safari18_0 firefox135 edge101; do
  python -c "from curl_cffi import requests as r; x=r.get('$URL',impersonate='$p',timeout=25); "\
            "print('$p',x.status_code,len(x.text))"
done
```

### agent-browser — le défaut pour interagir (installé le 2026-09-07)
CLI Rust de Vercel Labs, pilote un Chrome réel par CDP, sans Playwright. Chaque commande
rend un résultat court : `snapshot` = arbre d'accessibilité compact avec refs `@e1`,
`read` = texte lisible, `click @e2`, `fill`, `screenshot`, `download`. Le navigateur
reste ouvert entre commandes (daemon), une session nommée par tâche.

```bash
npm install -g agent-browser && agent-browser install     # une fois par machine
agent-browser --session s1 open https://exemple.com
agent-browser --session s1 snapshot                        # refs @eN
agent-browser --session s1 click @e2
agent-browser --session s1 read
agent-browser --session s1 screenshot C:/tmp/page.png
agent-browser --session s1 close
agent-browser skills get core                              # doc complète, livrée avec le binaire
```

Règles : **toujours `--session <nom>`** (la session par défaut est partagée avec tout
agent de la machine). `--headed` dès qu'un Turnstile apparaît : en fenêtre visible, le
Chrome réel passe la vérification seul (Chrono24 validé, contenu complet en 10 s).
`--profile <dossier>` pour un profil persistant si un login doit survivre.

Limites constatées : `--cdp 9222` vers Brave **bloque le CLI** (daemon pendu, à tuer par
`taskkill //F //IM agent-browser-win32-x64.exe`) : pour le Brave logué, rester sur
`pilot.mjs attachToBrave()`. Kayak détecte agent-browser et redirige vers sa page bots,
alors que `curl` obtient la page entière avec les prix : curl d'abord, toujours.

Piège Windows : un paquet npm global `node` fantôme (fichier vide dans
`~/AppData/Roaming/npm/node_modules/node`) cassait le shim sh de tous les CLI npm
(« This: command not found »). Corrigé par `npm uninstall -g node`.

### Playwright headless — `pilot.mjs fetch` / `shot`
Vrai Chromium, JS exécuté, empreinte normale. Passe la plupart des 403 Cloudflare
(prouvé : Grokipedia, 50 pages sur 50). `fetch` rend le texte ou markdown de la page
rendue, `shot` une capture PNG pleine page. Toujours **ouvrir** la capture produite :
un exit code 0 ne prouve pas qu'une image affiche quelque chose.

### Brave via CDP — `pilot.mjs launch` + `attachToBrave()`
Le pattern pour les sites logués. `chromium.launch()` démarre un navigateur neuf à profil
vide ; `connectOverCDP` s'attache à un Brave déjà ouvert, dont le profil persiste sur
disque. On franchit un CAPTCHA ou un login une fois à la main, la session reste, les
scripts suivants en profitent. C'est ainsi que ChatGPT, Grok, la BPI et Bénézit se pilotent.

**Convention de ports, un par projet, ne jamais fusionner** (Chrome verrouille son
`user-data-dir`, deux projets sur le même profil se bloquent) :

| Projet | Port CDP | Profil |
|---|---|---|
| MaxPlay | 9222 | `C:/tmp/brave-debug` |
| IArtcane | 9223 | dédié |
| IArtscan | 9224 | `C:/tmp/brave-iartscan` |
| Nouveau projet | 9225+ | `C:/tmp/brave-<projet>` |

Recettes détaillées (bouton Télécharger vs URL directe, attente d'un résultat
asynchrone, pièges Windows) : `recettes.md`.

### Claude in Chrome (extension, `~/.claude/chrome/chrome-native-host.bat`)
L'agent pilote le Chrome de l'utilisateur, avec ses sessions. Utile pour une
vérification visuelle rapide sans script. Réserves documentées : ~15k tokens de schéma
chargés par session, bêta, vulnérable à l'injection de prompt (23,6 % de succès d'attaque
sans mitigation), plante sur les modales d'auth en contexte `chrome-extension://`.
À n'utiliser que sur des sites de confiance, jamais pour du scraping en volume.

### context7 — rien à voir avec le navigateur
Serveur MCP qui fournit la documentation à jour des bibliothèques. Il ne complète pas
Playwright : il évite de redécouvrir à la main les changements d'API de Playwright
(plusieurs leçons projet sont exactement ça). Règle : **un outil déclaré mais non testé
rend l'agent silencieusement aveugle**. Le tester une fois après installation.

## Ce que dit l'état de l'art 2026

- **MCP navigateur = cher.** Le schéma d'outils charge 13 à 19k tokens par session
  avant toute action (Playwright MCP 13,7k, Claude in Chrome 15,4k, Chrome DevTools
  MCP 19k). Chaque action rend l'arbre d'accessibilité entier : un clic ≈ 12 900
  caractères.
- **CLI plutôt que MCP.** Un script ne coûte rien tant qu'on ne l'appelle pas et rend
  un résultat court. Playwright CLI : ~27k tokens pour 10 étapes contre 114k en MCP.
  `agent-browser` (Vercel Labs, Rust, CDP direct) : 200 à 400 tokens par page.
- **Répartition recommandée** : Playwright pour les tests e2e et la CI, CLI maison ou
  `agent-browser` pour le scraping et le pilotage, Claude in Chrome pour un coup d'œil
  sur un site logué, Chrome DevTools MCP seulement pour du profilage perf/réseau.
- **Pas de proxy résidentiel ni de service type Bright Data** pour un usage personnel
  non commercial : ça change la nature du projet et fragilise les accès obtenus de
  bonne foi (BPI, BnF, SIKART).
- **robots.txt** : le lire, et distinguer le déclaratif (opt-out TDM) du technique
  (anti-bot). Le premier se respecte, le second se contourne pour un usage personnel.

Notre stack (zéro MCP navigateur, `agent-browser` pour interagir, `pilot.mjs` pour le
Brave logué, Playwright pour les tests e2e) est alignée sur ces recommandations.

## Anti-bot : le diagnostic en 5 questions

1. `curl` rend 200 et le HTML contient la donnée ? Terminé.
2. 200 mais donnée absente ? Chercher le JSON embarqué (`__NEXT_DATA__`,
   `data-react-props`, JSON-LD, `/api/`). Souvent l'API interne se `curl` directement.
3. 403 ? Essayer une UA courte (`-A "Mozilla/5.0"`), puis `curl_cffi` — **en balayant les profils** (`chrome`, `safari17_0`, `safari18_0`, `firefox135`, `edge101`, deux essais espacés) : un 403 sur un seul profil ne prouve rien. Un 403 qui varie = empreinte TLS (franchissable ici) ; identique partout = passer au navigateur ; `DNSError` = le domaine ne résout plus, ce n'est pas un anti-bot.
4. Toujours 403, ou page vide (challenge JS, SPA) ? `agent-browser --session x open` puis
   `read` ; Turnstile visible ? relancer avec `--headed`.
5. Login, CAPTCHA, quota par compte ? `pilot.mjs launch` sur le port du projet, se
   loguer à la main une fois, puis `attachToBrave()`.

Noter dans `LESSONS.md` du projet chaque domaine et la marche qui a fonctionné : le
diagnostic ne se refait pas deux fois.

## CAPTCHA et challenges : ce qui existe

Trois familles, à essayer dans cet ordre.

1. **Le challenge passe seul dans un vrai Chrome visible.** Turnstile « managed » ne
   demande souvent rien à un navigateur normal en fenêtre visible avec une empreinte
   cohérente. Headless ou `curl_cffi` : bloqués. `agent-browser --headed` : passe.
   Validé sur Chrono24 le 2026-09-07. C'est la réponse pour la majorité des cas.
2. **Humain dans la boucle, une fois, session persistante.** Si la case ou le CAPTCHA
   image reste, on l'ouvre dans le Brave du projet (`pilot.mjs launch`), on clique à la
   main, le profil garde le cookie de clearance et le login. Les scripts suivants
   s'attachent (`attachToBrave()`) et ne revoient plus le challenge tant que le cookie
   vit (heures à jours). Même principe pour un SMS, un MFA, un mur de login LinkedIn.
   C'est la voie normale pour un usage personnel : un clic humain, pas une infrastructure.
3. **Services de résolution payants** (2captcha, CapSolver, ZenRows). Ils vendent des
   tokens Turnstile/reCAPTCHA résolus par API. Fonctionnent, mais : payants, zone grise
   selon les CGU du site, et ils font basculer le projet dans le contournement
   industriel. **Déconseillé** pour un usage personnel non commercial, pour la même
   raison que les proxys résidentiels : ça fragilise les accès obtenus de bonne foi.

Ce qui ne marche plus en 2026 : plugins « stealth » Playwright seuls, rotation d'UA
sans cohérence TLS, headless avec masquage de `navigator.webdriver`. Cloudflare
recoupe empreinte TLS, comportement et historique du cookie.

## Résultats des tests du 2026-09-07 (référence)

| Site | curl UA courte | curl UA Chrome | curl_cffi | Playwright headless | agent-browser |
|---|---|---|---|---|---|
| Bukowskis | 200 | 403 | 200 | non testé | non testé |
| Catawiki | 403 | 403 | **200** sur les 8 profils testés | bloqué (272 car.) | non testé |
| Chrono24 | 403 | 403 | **200 en `safari17_0`/`safari18_0` (~4 essais sur 5)**, 403 en `chrome`/`firefox`/`edge` | bloqué (65 car.) | headless : Turnstile · **headed : 200, contenu complet** |
| Heritage ha.com (page de résultats) | 403 | 403 | 403 sur 8 profils, 4 essais espacés (la page d'accueil, elle, répond 200) | non testé | navigateur requis |
| LinkedIn profil public | 200 (titre seulement) | 200 | 999 en `chrome`/`safari`, **200 (~500 Ko) en `safari17_0`/`firefox135`/`edge101`** | non testé | contenu complet = login requis → Brave |
| Kayak vols | **200, prix dans le HTML** (`window.R9`) | 200 | 200 | non testé | redirigé vers page bots |
| Grokipedia | 200 | 200 | 200 | 200 (prouvé en juin) | non testé |
| Auctionet | 200 (`data-react-props`) | 200 | 200 | non testé | non testé |

Leçon : aucun outil ne gagne partout. Kayak tombe à curl et bloque le navigateur ;
Catawiki et Bukowskis tombent à curl_cffi. D'où le diagnostic en 5 questions, dans
l'ordre, et la leçon gravée par domaine.

🔴 **Correction du 2026-09-07 (soir), projet IArtscan — Chrono24 tombe à `curl_cffi`,
à condition de choisir le bon profil.** Le test initial concluait « 403 » en restant sur
`impersonate="chrome"`, le défaut. En réalité **`safari15_5`, `safari17_0` et `safari18_0`
rendent 200 avec ~696 Ko et les prix en clair** (8 900 €, 13 509 €… sur `/rolex/index.htm`),
annoncé reproductible 5/5 par la session IArtscan — la contre-vérification MaxPlay (9 essais) mesure
plutôt **4 sur 5 par profil**, et `safari15_5` en 403 constant. Le navigateur visible reste le
filet de sécurité, plus le premier réflexe.

➡️ **Règle qui en découle : quand `curl_cffi` échoue, essayer au moins un profil de chaque
famille (`chrome`, `safari17_0`, `safari18_0`, `firefox135`, `edge101`) et, sur les profils qui
échouent, un second essai espacé : le verdict par requête est en partie aléatoire.** Un 403 sur un profil n'est pas
un 403 sur le site. Un 403 qui **varie** selon le profil = détection d'empreinte TLS, donc
franchissable sans navigateur ; un 403 **identique partout** (Heritage `ha.com`) demande le
navigateur. Et distinguer toujours d'un **DNSError** (domaine qui ne résout plus), qui n'est
pas un anti-bot.

Cela explique rétrospectivement l'anomalie Bukowskis (403 sur UA Chrome complète, 200 sur UA
courte) : ce n'est pas l'User-Agent, c'est la **cohérence entre l'UA annoncé et la pile TLS
réelle**. Une UA Chrome portée par une pile non-Chrome est un signal de bot plus net qu'une
UA anonyme.

## Sources

- [Playwright MCP vs Claude in Chrome (Medium, 2026)](https://lalatenduswain.medium.com/playwright-mcp-vs-claude-in-chrome-which-browser-testing-tool-should-you-use-in-2026-e502bee0067a)
- [Claude in Chrome vs Chrome DevTools MCP (claude-code-best-practice)](https://github.com/shanraisshan/claude-code-best-practice/blob/main/reports/claude-in-chrome-v-chrome-devtools-mcp.md)
- [Benchmark tokens Playwright CLI / agent-browser / Claude in Chrome (ytyng)](https://www.ytyng.com/en/blog/ai-browser-automation-tools-comparison-2026)
- [agent-browser token efficiency (DEV)](https://dev.to/chen_zhang_bac430bc7f6b95/why-vercels-agent-browser-is-winning-the-token-efficiency-war-for-ai-browser-automation-4p87)
- [Playwright CLI vs MCP (Better Stack)](https://betterstack.com/community/guides/ai/playwright-cli-vs-mcp-browser/)
- [WebFetch vs WebSearch internals (Shilkov)](https://mikhail.io/2025/10/claude-code-web-tools/)
- [WebFetch truncation, issue anthropics/claude-code #22937](https://github.com/anthropics/claude-code/issues/22937)
- [Bypass Cloudflare with Playwright 2026 (BrowserStack)](https://www.browserstack.com/guide/playwright-cloudflare)
- [Human-in-the-loop cloud browsers (Scrapfly)](https://scrapfly.io/blog/posts/human-in-the-loop-cloud-browsers)
- [Playwright Cloudflare bypass 2026, 3 méthodes qui marchent, 9 qui ne marchent plus](https://humanbrowser.cloud/blog/bypass-cloudflare-playwright-2026)
- [agent-browser (Vercel Labs)](https://github.com/vercel-labs/agent-browser)

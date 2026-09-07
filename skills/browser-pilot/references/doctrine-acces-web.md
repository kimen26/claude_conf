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
| 403 sans challenge JS (empreinte TLS reconnue) | `curl_cffi` (Python, imite le TLS de Chrome) | Quasi nul. Piste à tester par domaine, pas acquise |
| Vraie SPA, contenu rendu en JS, 403 avec challenge | `pilot.mjs fetch` (Chromium headless) | Moyen. Un navigateur par appel, quelques secondes |
| Capture d'écran pleine page | `pilot.mjs shot` | Moyen |
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

Statut : **à tester par domaine**, pas une solution acquise.

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

Notre stack (`pilot.mjs` par-dessus Playwright, zéro MCP navigateur) est alignée sur ces
recommandations. Candidat à évaluer : `agent-browser` en remplacement de la couche
`attachToBrave` si l'économie de tokens se confirme sous Windows.

## Anti-bot : le diagnostic en 5 questions

1. `curl` rend 200 et le HTML contient la donnée ? Terminé.
2. 200 mais donnée absente ? Chercher le JSON embarqué (`__NEXT_DATA__`,
   `data-react-props`, JSON-LD, `/api/`). Souvent l'API interne se `curl` directement.
3. 403 ? Essayer une UA courte (`-A "Mozilla/5.0"`), puis `curl_cffi`.
4. Toujours 403, ou page vide (challenge JS, SPA) ? `pilot.mjs fetch`.
5. Login, CAPTCHA, quota par compte ? `pilot.mjs launch` sur le port du projet, se
   loguer à la main une fois, puis `attachToBrave()`.

Noter dans `LESSONS.md` du projet chaque domaine et la marche qui a fonctionné : le
diagnostic ne se refait pas deux fois.

## Sources

- [Playwright MCP vs Claude in Chrome (Medium, 2026)](https://lalatenduswain.medium.com/playwright-mcp-vs-claude-in-chrome-which-browser-testing-tool-should-you-use-in-2026-e502bee0067a)
- [Claude in Chrome vs Chrome DevTools MCP (claude-code-best-practice)](https://github.com/shanraisshan/claude-code-best-practice/blob/main/reports/claude-in-chrome-v-chrome-devtools-mcp.md)
- [Benchmark tokens Playwright CLI / agent-browser / Claude in Chrome (ytyng)](https://www.ytyng.com/en/blog/ai-browser-automation-tools-comparison-2026)
- [agent-browser token efficiency (DEV)](https://dev.to/chen_zhang_bac430bc7f6b95/why-vercels-agent-browser-is-winning-the-token-efficiency-war-for-ai-browser-automation-4p87)
- [Playwright CLI vs MCP (Better Stack)](https://betterstack.com/community/guides/ai/playwright-cli-vs-mcp-browser/)
- [WebFetch vs WebSearch internals (Shilkov)](https://mikhail.io/2025/10/claude-code-web-tools/)
- [WebFetch truncation, issue anthropics/claude-code #22937](https://github.com/anthropics/claude-code/issues/22937)

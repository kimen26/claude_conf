---
name: impact-metaphrase
description: "Écrire une métaphore pédagogique qui tient : format standard, arc 3-temps Hayakawa, 4 critères Hofstadter, règle des 2 max, ventilation par sous-section, 9 leviers psy, workflow 6 étapes, red flags. Issu des retours SAN DOKU formation IA F1-F5."
family: impact
origin: Formations-Infopro + SAN DOKU retex
---

# Impact — L'Art de la Métaphrase

> Une métaphore n'est pas un ornement. C'est un pont cognitif (Hofstadter) qui permet au cerveau de comprendre le nouveau via l'ancien. Bien écrite, elle remplace un paragraphe d'explication. Mal écrite, elle pollue.

---

## M.1 Le format standard (issu F5 SAN DOKU)

Format unique, toujours le même :

```
**emoji Titre court** `[LEVIER — nuance optionnelle]`

Prose narrative 2–4 phrases. **Gras** sur 1 ou 2 mots-clés maximum.
Bullets seulement pour comparaison A vs B (3 items max).
```

**Règles de formatage strictes** :
- Pas de blockquote `>` pour du texte courant — réservé aux citations authentiques uniquement
- Pas d'italique décoratif sur des paragraphes entiers
- Pas de `❌/✅` ni d'emoji en début de paragraphe d'exemple
- Pas d'index rapide récapitulatif en fin de fichier (duplication confort-auteur)
- Numérotation `**1. emoji Titre**` autorisée mais pas obligatoire

**Pourquoi** : la cohérence visuelle fait disparaître le format. Le lecteur voit le contenu, pas la mise en page.

---

## M.2 Arc narratif en 3 temps (Hayakawa appliqué)

Une bonne métaphore suit toujours cet arc :

1. **Situation concrète vécue** (1 phrase) : « Vous achetez une perceuse. »
2. **Retournement / analogie structurelle** (1-2 phrases) : « Quelqu'un a ajouté dans la notice : *Avant de percer, appuyez sur ce bouton qui ouvre la porte.* Vous suivez à la lettre — et laissez entrer le cambrioleur. »
3. **Pont explicite vers le concept cible** (1 phrase) : « Le tool poisoning, c'est ça : l'outil est légitime, sa notice est empoisonnée. »

**Sans le temps 3, l'analogie flotte.** Le pont *« X, c'est ça »* ou *« L'IA pareil »* est obligatoire.

---

## M.3 Les 4 critères d'une métaphore valide (Hofstadter & Sander)

Avant de retenir une métaphore, vérifier :

1. **Familière** — le domaine source est-il connu du public cible ? (Attention à la malédiction de la connaissance : « évidemment tout le monde connaît X » = red flag)
2. **Structurellement fidèle** — la logique de l'analogie est-elle la même que le concept, ou juste une ressemblance de surface ? Les analogies de structure valent 10× celles de surface.
3. **Limitée** — où l'analogie casse-t-elle ? Si une métaphore laisse penser que l'IA « pense » ou « comprend », il faut nommer la limite dans le texte.
4. **Adaptée au public** — analogie cuisine pour public généraliste, analogie système pour tech, analogie métier pour profession spécifique.

---

## M.4 La règle des 2 max (+1 exception)

**Max 2 métaphores par point enseigné** :
- 1 analogie quotidienne (accessible à tous)
- 1 analogie pro (monde métier du public)

**3 uniquement si les 3 sont exceptionnelles et non-substituables.** Au-delà, c'est du bruit et le formateur ne peut pas choisir.

**Mauvais réflexe** : accumuler les métaphores par peur de « pas assez expliquer ». Une métaphore forte > 4 métaphores tièdes.

---

## M.5 Ventilation par sous-section > niveau section

**Principe** : une métaphore doit éclairer **un point précis**, pas une section entière.

**Par défaut** : rattacher chaque métaphore à une **sous-section** (granularité pédagogique).
**Exception** : niveau section uniquement pour l'intro qui pose le concept global, quand aucune sous-section spécifique ne correspond.

**Pourquoi** :
- Rend visible la couverture réelle — un point sans métaphore devient détectable
- Évite les « métaphores fourre-tout » qui couvrent 4 concepts à la fois et n'en éclairent aucun
- Permet au formateur de sélectionner selon le public

**Diagnostic** : un outil d'arbo (ventilation section/sous-section/orphelin) révèle immédiatement les gaps pédagogiques. Une métaphore orpheline signale que son concept cible n'est pas structuré en sous-section dans le texte source → à **remonter dans le texte**, pas à laisser orpheline.

---

## M.6 Taxonomie des 9 leviers psychologiques

Chaque métaphore porte un levier déclaré entre `[crochets]`. C'est la boussole pédagogique : pourquoi cette métaphore marche.

| Levier | Quand l'utiliser | Exemple |
|--------|------------------|---------|
| **ZAJONC** (mere exposure) | Public résistant — ancrer dans le quotidien vécu | 📱 Autocomplete du téléphone |
| **CHOC** | Public blasé — créer une surprise qui ancre | 🎮 Game over sans sauvegarde |
| **HUMOUR** | Public tendu ou défensif — baisser la garde | 👦 L'ado de 14 ans « je sais réparer » |
| **CONCRET** (Hayakawa) | Concept trop abstrait — descendre l'échelle | 🍎 Écrire en code ce qu'est une pomme |
| **AVERSION PERTE** (Kahneman) | Motiver à l'action — pointer ce qu'on perd | 🍲 Le garde-manger empoisonné |
| **AUTORITÉ** (Cialdini) | Public pro — crédibiliser via un métier référent | 🍷 Le sommelier et le vinaigre |
| **GROWTH MINDSET** (Dweck) | Peur de l'échec — reframer l'itération | 🎯 L'archer apprenti |
| **FEYNMAN** | Concept apparemment technique à démystifier | 🧩 Expliquer à un apprenti |
| **PAIVIO** (dual coding) | Concept visuel — image vaut mieux que description | 📸 Une image vaut mille mots |

Plusieurs leviers peuvent se combiner : `[HUMOUR + CHOC]`, `[ZAJONC + IKEA]`, etc.

Référentiels détaillés : `biais.md` (Zajonc, Cialdini, Kahneman), `memoire.md` (Paivio, ancrage), `emotion.md` (Dweck, growth), `simplifier.md` (Feynman, Hayakawa).

---

## M.7 Workflow d'écriture — 6 étapes

1. **Nommer le concept cible** (abstrait) en 3 mots max : « stateless LLM », « prompt injection », « context window ».
2. **Trouver l'objet concret du quotidien** du public cible qui partage la même logique structurelle (pas juste visuelle).
3. **Écrire l'arc 3-temps** : situation → retournement → pont vers l'IA.
4. **Test du taxi** (Feynman) : peut-on l'expliquer en 30 secondes sans jargon à un non-expert ? Si non, retravailler.
5. **Nommer la limite** si nécessaire : *« C'est comme X, sauf que contrairement à X, l'IA… »*
6. **Appliquer le format standard** (§M.1) : emoji + titre + levier + prose 2-4 phrases, pas de fioriture.

---

## M.8 Red flags — métaphores à retravailler

Checklist des signaux d'alarme :

- **Blockquote `>` partout** → le texte se cache au lieu de s'imposer
- **Italique sur des paragraphes entiers** → aucune hiérarchie de lecture, tout est « important »
- **Format mixte `❌/✅`** dans la métaphore → c'est un tableau comparatif déguisé, sortir du format métaphore
- **Pas de levier déclaré** → pas de boussole, souvent métaphore faible à retravailler
- **> 4 phrases** → c'est un paragraphe narratif, pas une métaphore. Couper ou éclater.
- **Analogie de surface uniquement** (ressemblance visuelle sans logique partagée) → reformuler en analogie de structure
- **Métaphore qui « explique » le concept via un autre jargon** → malédiction connaissance, test taxi échoue
- **Pont implicite** (pas de phrase « X c'est ça »/« l'IA pareil ») → le lecteur doit deviner, 50% ne font pas le lien
- **Sub_id orphelin** (ne matche aucune sous-section) → le concept n'est pas structuré en sous-section dans le texte source : remonter la structure avant d'écrire la méta

---

## M.9 Spécificités public IA/formation — adapter la cible

| Profil public | Leviers prioritaires | Types d'analogies à privilégier |
|---------------|---------------------|---------------------------------|
| **Résistant / anxieux** | ZAJONC + CHOC | Face ID, Waze, Netflix (« vous faites déjà de l'IA ») |
| **Tech / dev** | CHOC + CONCRET | RAM, USB-C, CPU, protocol, boucle ReAct |
| **Métier / pro** | AUTORITÉ + CONCRET | Sommelier, architecte, notaire, consultant |
| **Généraliste** | ZAJONC + HUMOUR | Cuisine, conduite, famille, quotidien domestique |
| **Senior / non-digital** | CONCRET + FEYNMAN | Objets tangibles (pomme, journal, GPS) |

**Ne jamais mélanger 2 profils sur une même métaphore.** Créer 2 variantes plutôt.

---

## M.10 Collisions d'IDs — conventions à respecter

Quand les fiches ont des sous-sections récurrentes style « Ce qu'il faut retenir » :

**Red flag** : même ID `sXXc` pour la sous-section réelle ET pour la synthèse → collision silencieuse, l'une écrase l'autre dans le rendu.

**Convention** : suffixer les synthèses par `-retain` (ou équivalent) :
```
### Tool poisoning <!-- #s02c -->
### Ce qu'il faut retenir <!-- #s02-retain -->
```

De même, éviter les sub_ids « orphelins » qui pointent vers des sous-sections qui n'existent pas dans le MD principal. Si la méta est valable, **créer la sous-section dans le MD**, pas laisser l'orphelin.

---

## M.11 Checklist finale — avant validation d'une métaphore

- [ ] Format standard respecté (emoji + titre + levier + prose 2–4 phrases) ?
- [ ] Arc 3-temps identifiable (concret → analogie → pont) ?
- [ ] Levier explicite et pertinent ?
- [ ] Analogie de **structure** (pas seulement surface) ?
- [ ] Domaine source familier au public cible ?
- [ ] Test du taxi passé (30 secondes, sans jargon) ?
- [ ] Limites nommées si risque de contresens ?
- [ ] Max 2 métaphores sur ce point (3 exceptionnel justifié) ?
- [ ] Rattachée à une sous-section (ou intro de section si justifié) ?
- [ ] Aucun blockquote / italique de paragraphe / format mixte ?
- [ ] Pas de duplication avec une autre métaphore déjà écrite ?

---

## Synthèse — Le principe fondateur

Une métaphore n'éclaire pas un concept. **Elle le transporte** d'un domaine connu (source) vers un domaine inconnu (cible) en préservant la logique structurelle.

Les 3 questions qui valident tout :
1. **Est-ce que le lecteur connaît déjà la source ?** (sinon, c'est un concept à expliquer, pas une métaphore)
2. **Est-ce que la logique est la même ?** (sinon, c'est une décoration, pas un pont)
3. **Est-ce qu'on pointe explicitement le lien ?** (sinon, 50% des lecteurs ne le feront pas)

Si oui aux trois → la métaphore remplacera un paragraphe d'explication et restera ancrée en mémoire pendant des semaines. C'est ça, l'impact.

---

## Bibliographie

- Hofstadter, D. & Sander, E. (2013). *Surfaces and Essences: Analogy as the Fuel and Fire of Thinking*. Basic Books.
- Lakoff, G. & Johnson, M. (1980). *Metaphors We Live By*. University of Chicago Press.
- Hayakawa, S.I. (1939/1990). *Language in Thought and Action*. Harcourt.
- Feynman, R. — méthode documentée par James Gleick (1992), *Genius*.
- Heath, C. & Heath, D. (2007). *Made to Stick* — malédiction de la connaissance.
- Paivio, A. (1986). *Mental Representations: A Dual Coding Approach*. Oxford University Press.
- Retex SAN DOKU Formation IA F1–F5 (Infopro Digital, 2026) — format standard et conventions sub_id.

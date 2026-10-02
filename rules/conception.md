# Conception : réutiliser sans sur-abstraire

Norme de tout code écrit pour Yann, par l'orchestrateur comme par les agents. Elle prescrit :
elle doit dire vrai en permanence.

1. **Chercher avant d'écrire.** Avant toute fonction neuve : existe-t-elle déjà dans le projet,
   dans le kit d'un skill (`rex-manage-streamlit` : `core/`, briques, Cobalt), dans le socle ?
   3 recherches ou plus → `socle:fouilleur`. Le plan cite ce qui est réutilisé.
2. **Une fonction = une action**, nommée par un verbe métier. Les entrées/sorties (Snowflake,
   fichiers, `st.*`, réseau) restent aux bords ; le cœur reçoit et rend des valeurs simples
   (DataFrame, dict, dataclass) et se teste sans connexion.
3. **Règle des deux usages, appliquée au code.** 1er usage : écrit en place. 2e usage identique :
   on extrait, dans la tâche qui crée ce 2e usage (c'est son périmètre, pas un refactor hors
   périmètre). Seulement ressemblant : on attend le 3e. Jamais d'abstraction, de paramètre ou de
   « configurabilité » pour un usage hypothétique (Metz : une mauvaise abstraction coûte plus
   cher qu'une duplication).
4. **Couches.** Écran (pages, vues) sans logique ni requête → services (règles métier, purs) →
   accès données (seul endroit qui parle à Snowflake, cache ici). Streamlit : règle R23 du skill
   `rex-manage-streamlit` (`streamlit_app.py` = navigation, `vues/`, `core/`).
5. **Partager entre projets par un seul canal versionné**, jamais par copier-coller d'un projet à
   l'autre : plugin `socle` (Claude Code), stage `CORTEX_SKILLS` (Cortex Code), `IMPORTS` de stage
   (SiS runtime warehouse). Une copie locale d'un skill porte sa version et se met à jour.
6. **Refactor opportuniste interdit, signalé** : une duplication vue hors du périmètre de la tâche
   va en `## Parking` de `memory/TODO.md`, pas dans le diff.

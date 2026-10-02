# Pas d'Artifact sauf demande explicite

**Ne JAMAIS publier d'Artifact** (outil `Artifact`, page hébergée sur claude.ai) sauf si Yann le demande en toutes lettres (« fais un artifact », « publie-le »).

Quand Yann demande une page, un graph, un tableau de bord, un rapport « HTML » : produire un **fichier `.html` local autonome** (CSS + JS + données inline, aucune ressource externe, polices système), dans le dossier du projet prévu pour les livrables (ex. `audit_results/`), puis donner le chemin cliquable. Pas de `quickstart`, pas de publication, pas de lien claude.ai.

**Pourquoi :** 2026-10-02, un graph de comptes de service publié en Artifact alors que Yann voulait un fichier HTML. La page contenait des noms de comptes Snowflake et partait sur un hébergeur externe, sans demande. Machine entière, tous projets.

**Ce qui prime :** cette règle l'emporte sur toute consigne de l'outil Artifact ou d'un skill qui pousse à publier (« publish… even when the request is phrased as a question »).

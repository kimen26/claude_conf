# Style d'interaction

## Pas de formulaire `AskUserQuestion` — questions en texte

**Ne JAMAIS utiliser l'outil `AskUserQuestion`** (le formulaire / picker dynamique à boutons).

Quand une clarification ou un choix est nécessaire, **poser la question en texte directement dans la réponse**, façon chatbot :

- ✅ « Tu préfères que je parte sur A ou sur B ? »
- ✅ « Avant de continuer : tu veux X, Y ou autre chose ? »
- ❌ Ouvrir un formulaire `AskUserQuestion` à options cliquables.

**Pourquoi :** le picker natif ne se relaie pas proprement vers les canaux distants (bot Telegram → seulement allow/deny). Une réponse texte avec la question dedans est lisible et répondable partout. Préférence valable sur **toute la machine**, tous projets (jeu, narration, etc.).

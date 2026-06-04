# Gabarit Rapport Roborock

À copier-coller à la fin de l'audit. Remplir les `[...]`.

---

```markdown
# Rapport Roborock — [YYYY-MM-DD]

## Périmètre audité
- **Inclus** : ~/.claude/{skills, agents, rules, hooks, commands}, .claude/, CLAUDE.md (X niveaux), memory/ (Y fichiers), tous *.md du projet (Z fichiers), configs (.json/.yml)
- **Exclus** : code source, _archive/, node_modules/, dist/

## Synthèse exécutive
- **[N] items audités** (skills: X, agents: Y, hooks: Z, rules: A, .md: B, configs: C)
- **[M] anomalies** :
  - 🔴 [a] CRITIQUE (casse silencieuse)
  - 🟠 [b] HAUTE (info fausse active)
  - 🟡 [c] MOYENNE (friction modérée)
  - 🟢 [d] BASSE (cosmétique)
- **[O] fichiers orphelins** détectés (à qualifier: x, candidat archive: y, candidat suppression: z)

## Détail par phase

### Phase 0 — Inventaire
[tableau récap]

### Phase 1 — Frontmatters
[verdicts ✅/⚠️/❌]

### Phase 2 — Skills
[...]

### Phase 3 — Agents
[...]

### Phase 4 — Hooks & Rules
[...]

### Phase 5 — CLAUDE.md & Memory
[...]

### Phase 6 — Liens & refs croisées
[...]

### Phase 7 — Orphelins
[liste complète avec mtime]

---

## TOP 5 actions prioritaires

1. **[🔴 CRITIQUE]** [description courte] → [action concrète]
2. **[🔴 CRITIQUE]** ...
3. **[🟠 HAUTE]** ...
4. **[🟠 HAUTE]** ...
5. **[🟡 MOYENNE]** ...

## Backlog secondaire
- [liste des autres anomalies à traiter plus tard]

## Annexe — Liste exhaustive orphelins

| Fichier | mtime | Catégorie | Action proposée |
|---------|-------|-----------|----------------|
| ... | ... | ❓/🟡/🔴 | ... |

---

_Rapport généré par challenge-roborock. Mode audit pur (aucune modif appliquée). L'humain valide avant toute correction._
```

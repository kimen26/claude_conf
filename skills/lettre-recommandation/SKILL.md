---
name: lettre-recommandation
description: Génère des lettres de recommandation professionnelles au format Word (.docx) avec mise en page élégante, structure narrative impactante et signature manuscrite simulée. Trigger sur : lettre de recommandation, lettre motivation, référence professionnelle, recommendation letter.
---

# Skill: Lettre de Recommandation Professionnelle

**Version:** 1.0  
**Auteur:** Yann Ponaire (Infopro Digital)  
**Trigger:** génération lettre recommandation, lettre motivation, référence professionnelle, recommendation letter

---

## 📋 Description

Génère des lettres de recommandation professionnelles au format Word (`.docx`) avec :
- Mise en page élégante (marges, espacements)
- En-tête personnalisable (nom, titre, entreprise)
- Structure narrative claire et impactante
- Signature manuscrite simulée (police Segoe Script)

**Stack technique :** `python-docx` (génération Word)

---

## 🎯 Quand utiliser ce skill

- L'utilisateur demande une lettre de recommandation
- Besoin d'un template formel pour recommander un ancien collègue/stagiaire
- Export Word requis pour signature et impression

---

## 📐 Workflow

### 1. Collecter les informations

Demander systématiquement :

| Champ | Exemple | Requis ? |
|-------|---------|----------|
| **Personne recommandée** | Farès Djoudi | ✅ Oui |
| **Poste visé** | Data Engineer Senior, Lead Data | ✅ Oui |
| **Relation** | Collègue, manager, responsable technique | ✅ Oui |
| **Durée collaboration** | 2 ans, 6 mois, stage de 3 mois | ✅ Oui |
| **Compétences clés** | Python, Snowflake, autonomie, rigueur | ✅ Oui |
| **Anecdote marquante** | Projet complexe réussi seul, initiative notable | ⚠️ Recommandé |
| **Signature** | Nom du signataire (par défaut : Yann Ponaire) | ❌ Optionnel |
| **Titre signataire** | Deputy CTO / Directeur Technique Data | ❌ Optionnel |
| **Entreprise** | Infopro Digital | ❌ Optionnel |

### 2. Structure de la lettre

```
┌────────────────────────────────────┐
│ EN-TÊTE (aligné droite)            │
│ Nom                                │
│ Titre                              │
│ Entreprise                         │
│ Date                               │
└────────────────────────────────────┘

Objet : Lettre de recommandation — [Nom Personne]

À qui de droit,

[ACCROCHE PERCUTANTE en gras]

[§1] Contexte et observation générale
      → Durée collaboration + première impression forte

[§2] Compétences techniques
      → Stack maîtrisé + exemple concret (≠ liste générique)

[§3] Autonomie & soft skills
      → Ce qui le distingue au-delà du technique

[§4] Anecdote marquante (optionnel mais recommandé)
      → Moment "you had to be there" qui illustre sa valeur

[CONCLUSION] Recommandation claire et sans réserve

Formule de politesse

Signature manuscrite (police Segoe Script, bleu marine)
Nom + Titre
```

### 3. Ton & style (CRITIQUE)

**✅ BON (impact maximal) :**
- Phrases courtes et affirmatives
- Anecdotes concrètes > adjectifs vagues
- Contraste : "Là où d'autres X, lui Y"
- Phrase signature mémorable en italique
- Vocabulaire précis : "absorbe la complexité", "capitalise", "traversé sans assistance"

**❌ MAUVAIS (lettre plate) :**
- "Très bon profil", "excellentes compétences" (générique)
- Longues listes de qualités sans preuves
- Ton corporate fade
- Pas de relief narratif

**Règle d'or :** La lettre doit se lire comme un témoignage sincère, pas un CV reformulé.

### 4. Génération du fichier Word

Utiliser `python-docx` avec :
- Marges : `top/bottom=2.5cm`, `left=2.8cm`, `right=2.5cm`
- Interligne : `14pt`
- Police corps : `Calibri 11pt`
- Police signature : `Segoe Script 18pt` en `RGBColor(0x1A, 0x1A, 0x5E)` (bleu marine)
- Nom de sortie : `lettre_recommandation_[prenom]_[nom].docx`

**Code de base :**
```python
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# Marges
for section in doc.sections:
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(2.8)
    section.right_margin = Cm(2.5)

# Helper functions
def add_paragraph(doc, text="", bold=False, italic=False, 
                  align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = Pt(14)
    if text:
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.name = "Calibri"
        run.font.size = Pt(11)
    return p

# Voir generate_lettre_template.py pour le template complet
```

---

## 🔧 Configuration requise

**Dépendances Python :**
```bash
pip install python-docx
```

**Permission dans `.claude/settings.local.json` (si besoin) :**
```json
{
  "permissions": {
    "allow": [
      "Bash(python generate_lettre_*.py)"
    ]
  }
}
```

---

## 📦 Fichiers associés

- `generate_lettre_template.py` — Template générique complet
- `lettre_recommandation_*.docx` — Output généré

---

## 🎓 Exemples de phrases efficaces

### Accroche
- "X est le type de profil qu'on ne remplace pas."
- "En 15 ans de management technique, j'ai rarement rencontré quelqu'un comme X."
- "Si je devais résumer X en une phrase : il transforme les problèmes flous en solutions propres."

### Compétences
- "Maîtrise X, Y, Z — et s'approprie chaque nouvel outil en quelques jours sans formation préalable."
- "Là où certains profils ont besoin de cadre et de suivi, X a besoin de sujets."

### Signature narrative
- "Ce n'est pas une formule. C'est sa façon de travailler." (après une citation)
- "Cette énergie est contagieuse et rare."
- "Il ne gère pas l'urgence — il absorbe la complexité et la transforme en livrable."

---

## ⚠️ Anti-patterns

- **Ne jamais** utiliser de superlatifs non étayés ("le meilleur", "exceptionnel") sans contexte
- **Ne jamais** faire une liste de 10+ qualités génériques
- **Ne jamais** oublier l'anecdote concrète (vide = lettre corporate sans âme)
- **Ne pas** dépasser 1 page (sauf cas très exceptionnel avec parcours long)

---

## 🚀 Commande rapide

```bash
# Depuis le projet formation (ou tout autre)
python generate_lettre_[prenom].py
```

Génère → `lettre_recommandation_[prenom]_[nom].docx`

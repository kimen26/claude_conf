---
name: translate-en
description: Translate French content to natural, flowing English — not word-for-word but as if written natively. Middle-school vocabulary level. Review for structure and meaning after translating.
type: skill
triggers:
  - translate to english
  - traduire en anglais
  - version anglaise
  - _en
---

# Skill: translate-en

## Goal

Translate French text to **natural, flowing English** — as if it were written in English from the start, not translated from French.

## Rules

1. **Never translate word-for-word.** Restructure sentences so they feel natural in English.
2. **Vocabulary level: middle school** — clear, direct, no fancy jargon unless it's a technical term that must stay (e.g., RAG, LLM, GIGO).
3. **Keep the tone** — humor stays funny, punchy lines stay punchy, metaphors stay vivid.
4. **Keep all markdown structure** — headers, bullets, tables, emojis, HTML comments (`<!-- #anchor -->`), bold/italic.
5. **Keep technical terms as-is**: RAG, LLM, GIGO, OCR, Text-to-SQL, MCP, CLAUDE.md, Chain of Thought, system prompt, CoT, DIGI, Chainsnow, Snowflake, etc.
6. **After translating, re-read** the full output and verify:
   - Does it read naturally in English?
   - Is the meaning preserved (not just the words)?
   - Are all sections structurally consistent with the French original?
   - Do jokes and metaphors land?

## Output naming convention

Input: `Fiches/FX/FX_V2_*.md`
Output: `Fiches/FX/FX_V2_*_en.md`

Example: `F2_V2_QUIZ.md` → `F2_V2_QUIZ_en.md`

## What to preserve exactly

- `✅` markers on correct quiz answers
- Section anchors: `<!-- #f2-s02 -->`
- Psychological levers in brackets: `` `[ZAJONC — défenses baissées]` `` → `` `[ZAJONC — defenses down]` ``
- Trainer notes in `>` blockquotes
- Tables (translate content, keep structure)
- Footer lines: `*Formation IA Infopro Digital — F2 V2 — Quiz — Avril 2026*` → `*AI Training Infopro Digital — F2 V2 — Quiz — April 2026*`

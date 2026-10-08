# Design templates

Catalog of design templates vendored as git submodules for Claude to pull in when doing design work.

| Template | Source | Type | Use for |
|---|---|---|---|
| [`tahta`](tahta) | [zcag/tahta](https://github.com/zcag/tahta) | Slidev presentation theme (`slidev-theme-tahta` on npm) | Building Markdown-authored slide decks with Slidev |

## tahta

A themeable Slidev design system: pick a `layout` and a `themeConfig.variant` per slide/deck, no custom CSS needed.

- 15 variants (e.g. `editorial`, `brutalist`, `soft`, `minimal`, `paper`, `boardroom`, `signal`, `poster`, ...) — each bundles typography, shape, palette, density, and motion.
- ~30 layouts (`cover`, `stats`, `steps`, `diagram`, `vs`, `code-explain`, ...) covering keynote and technical-teaching content shapes.
- Ships a generated agent contract at [`tahta/packages/theme/AGENTS.md`](tahta/packages/theme/AGENTS.md) — read that file before authoring a deck with this theme; it has the full frontmatter schema, variant table, and layout field reference.
- Machine-readable contracts: [`tahta/packages/theme/variants.json`](tahta/packages/theme/variants.json), [`tahta/packages/theme/layouts.json`](tahta/packages/theme/layouts.json).

Quick start:

```bash
npm i slidev-theme-tahta
```

```md
---
theme: slidev-theme-tahta
title: My Talk
themeConfig:
  variant: editorial   # required — see AGENTS.md for the full variant table
---
```

Then author slides per the layout/variant contract in `AGENTS.md`, and validate with `npx tahta-lint slides.md` before exporting.

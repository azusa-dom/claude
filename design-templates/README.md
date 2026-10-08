# Design templates

Catalog of design templates vendored as git submodules for Claude to pull in when doing design work.

## Presentations

| Template | Source | Type | Use for |
|---|---|---|---|
| [`tahta`](tahta) | [zcag/tahta](https://github.com/zcag/tahta) | Slidev presentation theme (`slidev-theme-tahta` on npm) | Building Markdown-authored slide decks with Slidev |

### tahta

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

## Scientific diagrams

| Template | Source | Type | Use for |
|---|---|---|---|
| [`scientific-diagrams/janosh-diagrams`](scientific-diagrams/janosh-diagrams) | [janosh/diagrams](https://github.com/janosh/diagrams) | Reference gallery (Typst/CeTZ + LaTeX/TikZ sources) | Starting point / adaptable source for a physics, chemistry, or ML concept diagram (neural nets, convolution, geometric & math constructions, ...) |
| [`scientific-diagrams/typst-fletcher`](scientific-diagrams/typst-fletcher) | [Jollywatt/typst-fletcher](https://github.com/Jollywatt/typst-fletcher) | Typst package (`@preview/fletcher`) | Precise node-and-arrow diagrams in Typst — flowcharts, commutative diagrams, graphs |
| [`scientific-diagrams/cetz`](scientific-diagrams/cetz) | [cetz-package/cetz](https://github.com/cetz-package/cetz) | Typst package (`@preview/cetz`) | Custom paths, geometry, and complex drawings in Typst — TikZ/Processing-like API; what Fletcher and the posters below build on |
| [`scientific-diagrams/beautiful-mermaid`](scientific-diagrams/beautiful-mermaid) | [lukilabs/beautiful-mermaid](https://github.com/lukilabs/beautiful-mermaid) | TypeScript library (npm) | Quick themed pipeline/workflow diagrams rendered from Mermaid syntax to SVG (15 built-in themes, zero DOM deps) |

Rule of thumb: reach for **Fletcher** for exact nodes/arrows/connections and **CeTZ** for custom geometry — together they cover a mechanism diagram that needs precise control, and the result drops straight into a Typst poster or paper. Reach for **Beautiful Mermaid** instead for a fast, simple pipeline/workflow diagram that doesn't need that precision. Browse **janosh/diagrams** first for an existing diagram on the same concept to adapt rather than drawing from scratch.

## Academic conference posters

| Template | Source | Type | Use for |
|---|---|---|---|
| [`conference-posters/quarto-typst-templates`](conference-posters/quarto-typst-templates) | [quarto-ext/typst-templates](https://github.com/quarto-ext/typst-templates) (`poster/` subdir) | Quarto + Typst template | Formal A0 landscape conference poster — cream background, dark title bar, warm accent; built-in title/figure/callout/data-highlight blocks |
| [`conference-posters/sleek-scientific-poster`](conference-posters/sleek-scientific-poster) | [weygoldt/typst_poster](https://github.com/weygoldt/typst_poster) | Typst template | Visually striking A0 portrait poster — Apple-inspired dark mode, Inter type, hairline rules, full-bleed hero banner, single accent color; composed from reusable blocks (`figure-card`, `stat-row`, `take-home`, `pull-stat`) rather than a fixed grid |
| [`conference-posters/simple-research-poster`](conference-posters/simple-research-poster) | [aneziac/simple-research-poster](https://github.com/aneziac/simple-research-poster) | Typst template (`@preview/simple-research-poster`) | A maintainable personal poster baseline — layout (`poster.typ`), content (`sections.typ`), and color palette (`colors.typ`) kept in separate files; diagrams drawn natively with CeTZ |

Notes:
- `quarto-typst-templates` is a monorepo of several Quarto/Typst templates — use only the `poster/` subdirectory.
- For a palette swap, each poster template keeps its colors in one place (`typst.toml`/theme dict for the sleek poster, `colors.typ` for simple-research-poster) — check there first rather than hand-editing layout files.

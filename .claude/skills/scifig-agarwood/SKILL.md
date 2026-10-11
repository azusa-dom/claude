---
name: scifig-agarwood
description: House style for all of azusa's scientific figures — multi-panel journal figures, graphical abstracts, poster hero figures, evidence/validation maps, schematic + data panels. Use whenever a scientific or research figure, plot, diagram or figure redesign is requested in this repo (including "科研图", "论文图", "海报主图", "graphical abstract"), unless the user names a different style.
---

# agarwood-scifig house style

The user's default look for research figures: dense, journal-grade, white canvas with thin rules,
沈香墨 / 檀木棕 / 棠梨绯 palette, editable SVG. Do not fall back to card/poster/marketing layouts
(rounded tinted boxes, big gradient headlines, icon tiles) — the user rejected those as "not scientific".

## Before drawing

1. Read `design-templates/house-style/agarwood-scifig/README.md` (rules, tokens, QA checklist).
2. Look at the flagship `figures/poster-hero-two-track/make_figure.py` + `two_track_figure.png`
   and `design-templates/house-style/agarwood-scifig/examples/` for the target density.
3. Pick the variant first (README, "两种版式"): **journal** for any manuscript figure (800 px = 190 mm,
   smallest text 10.5 px, ≤ 5 panels, no track strips, no image mock-ups, no in-figure title/footer) or
   **poster** for posters/slides (1800 px, dense, track strips, title and footer). A poster drawing is never
   shrunk into a manuscript: redraw it in the journal variant (cut panels that other figures already carry).

## Build

- Schematic / mixed figures: `from scifig import Figure, C, T, num` (add the template dir to
  `sys.path`). Write a `make_figure.py` next to the outputs; keep all coordinates explicit.
- Pure data plots: matplotlib with `plt.style.use(".../agarwood.mplstyle")`; for full journal
  sets reuse `figures/cine-cmr-review-v10/style/` (190 mm export, font and alignment audits).
- Every panel: lowercase bold letter + claim-style title; numbers printed on marks; 2–3 muted
  caption lines (journal: 1–2); footer with provenance (schematic vs transcribed, sources, not pooled) and
  abbreviations (journal: written but hidden unless `SCIFIG_TITLES=1`; the caption carries it).
- Journal variant: measure every string with `tw()` and wrap with `wrap()` to its column; never let text cross
  a column rule; values go above or beside marks, inside the column.
- Text in ink/muted only — never in the series colour. Colours keep their roles (OBS/INF/REF/SUP/ERR).
- Never invent study numbers. Transcribed values cite their source; placeholders say "illustrative".

## Deliver

1. `fig.save()` must pass (valid XML; smallest text ≥ 7 pt at print width).
2. `Figure.render_png(svg, png, scale=2–3)`, then Read the PNG and crop-zoom crowded regions;
   fix every overlap before showing the user.
3. Send PNG (preview) + SVG (editable) to the user; commit `make_figure.py`, SVG and PNG together.

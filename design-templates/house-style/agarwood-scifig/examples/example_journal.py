"""Minimal journal-width example of the agarwood-scifig house style.

Canvas 800 px = 190 mm double column, so 10.5 px text prints at ~7 pt.
All numbers here are ILLUSTRATIVE placeholders, not study data — replace them with your own.

    python3 example_journal.py      # writes example_journal.svg + .png next to this file
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from scifig import C, T, Figure, gauss, num  # noqa: E402

fig = Figure(800, 560, print_width_mm=190, margin=20)
fig.title("Figure 2 | Example layout in the agarwood-scifig style", y=26, rule_y=36,
          legend=[("reference", C.REF), ("estimate", C.INF)])

# ---- a: curves with reference vs estimate ------------------------------------------------
fig.panel(20, 62, "a", "Estimate lags the reference at peak")
ts = [i / 100 for i in range(101)]
ref = [-0.2 * gauss(t, 0.36, 0.15) for t in ts]
est = [-0.17 * gauss(t, 0.46, 0.17) for t in ts]
ax = fig.axes(70, 82, 290, 150, (0, 1), (-0.25, 0.02), [0, 0.5, 1], [-0.2, -0.1, 0],
              "normalised cycle time", "Ecc", xfmt=lambda v: f"{v:g}", yfmt=lambda v: num(v, 1))
ax.band(ts, [r - 0.02 for r in ref], [r + 0.02 for r in ref], C.SANDAL, 0.22)
ax.line(ts, ref, C.REF, 1.8)
ax.line(ts, est, C.INF, 1.8, dash="5 3")
fig.arrow(ax.fx(0.36), ax.fy(-0.225), ax.fx(0.45), ax.fy(-0.225), C.INK, 1, 4)
ax.text(0.48, -0.225, "Δt", T.SMALL, 700, dy=4)
fig.legend_items(70, 282, [("reference ± SD", "line", C.REF), ("estimate", "dash", C.INF)])

# ---- b: forest plot ---------------------------------------------------------------------
fig.col_rule(400, 48, 300)
fig.panel(415, 62, "b", "Error is component-specific")
fig.forest(420, 76, 340, [
    ("circumferential", 0.02, -0.02, 0.06, C.REF),
    ("radial", -0.24, -0.45, -0.03, C.INF),
    ("radial, lesion only", -0.20, -0.41, 0.01, C.INF, True),
    ("longitudinal", -0.03, -0.08, 0.02, C.OBS),
], xlim=(-0.5, 0.1), ticks=[-0.4, -0.2, 0], xlabel="strain error (mean ± SD)", fmt=lambda v: num(v, 1))
fig.check(420, 262, "magnitude recovered for Ecc")
fig.cross(420, 282, "not alone: focal location or extent")

fig.row_rule(306)

# ---- c: coverage heatmap ----------------------------------------------------------------
fig.panel(20, 332, "c", "Few studies test location or timing")
fills = {2: ("url(#cellDirect)", "none"), 1: (C.INF_T, "none"), 0: (C.WHITE, C.GRID)}
M = [[2, 1, 0, 0], [2, 1, 0, 2], [1, 2, 0, 0], [2, 0, 0, 0]]
bottom = fig.heatmap(20, 362, ["Study A", "Study B", "Study C", "Study D"], ["M", "L", "E", "T"], M, fills,
                     cell_w=50, cell_h=22, label_w=110, totals=["3", "1", "0", "1"], totals_label="direct / 4")
fig.legend_items(26, bottom + 18, [("direct", "box", C.DEEP), ("partial", "box", C.INF_T), ("none", "box", C.WHITE)], gap=14)

# ---- d: horizontal bars -----------------------------------------------------------------
fig.col_rule(400, 316, 520)
fig.panel(415, 332, "d", "Discrimination by modality")
fig.hbars(415, 350, 250, [("DENSE", 0.87, C.DEEP), ("Tagging", 0.83, C.AGAR), ("FT (cine)", 0.66, C.INF)],
          xlim=(0, 1), ticks=[0, 0.5, 1], xlabel="AUC", label_w=80, row_h=24)
fig.lines(415, 490, ["Bars rank discrimination, not material-motion accuracy;",
                     "values printed at bar ends in ink, never in the series colour."])

fig.footer(["Illustrative placeholder values — not study data. a, reference shaded ± SD; b, open marker = subgroup.",
            "M magnitude · L location · E extent · T timing. FT, feature tracking."], rule=True)

svg = fig.save(HERE / "example_journal.svg")
Figure.render_png(svg, HERE / "example_journal.png", scale=3)

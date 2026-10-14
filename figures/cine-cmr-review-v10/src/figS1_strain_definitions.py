"""Supplementary Figure S1: the same motion gives different numbers under different strain definitions.

agarwood-scifig house style, 190 mm. Analytic and conceptual schematics; every printed number is
computed from the curves drawn here (no study data).
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
from scifig_common import C, T, export, start  # noqa: E402
from scifig import annulus_path, gauss  # noqa: E402


def f2(x, plus=False):
    s = f"{x:.2f}".replace("-", "−")
    return ("+" + s) if plus and x > 0 else s


def f3(x):
    s = f"{x:.3f}".rstrip("0").replace("-", "−")
    return "+" + s if x > 0 else s


H = 520
fig = start(H, "Figure S1 | Same motion, different numbers under different definitions",
            footer=["Analytic and conceptual schematics; printed values are computed from the drawn curves, not measured.",
                    "e, engineering strain; E, Green–Lagrange strain; ED / ES, end-diastole / end-systole."])
ts = [i / 400 for i in range(401)]
ROW2 = 266

# ---- a: engineering vs Green–Lagrange -------------------------------------------------------------
fig.panel(20, 24, "a", "The measure alone shifts −0.20 to −0.18")
ax = fig.axes(66, 50, 196, 140, (-0.3, 0.3), (-0.32, 0.36), [-0.2, 0, 0.2], [-0.2, 0, 0.2],
              ylabel="reported value", yfmt=lambda v: f"{v:.1f}".replace("-", "−") if v else "0",
              xfmt=lambda v: f"{v:.1f}".replace("-", "−") if v else "0")
fig.rich(66 + 98, 50 + 140 + 29, [("engineering strain ", 400, C.INK, False), ("e", 400, C.INK, True)],
         T.LABEL + 0.5, anchor="middle")
es = [-0.3 + 0.6 * i / 200 for i in range(201)]
ax.line(es, es, C.OBS, 1.4, dash="5 3")
ax.line(es, [e + e * e / 2 for e in es], C.REF, 1.8)
e0, E0 = -0.2, -0.2 + 0.02
fig.line(ax.fx(e0), ax.fy(e0), ax.fx(e0), ax.fy(E0), C.INK, 1.2)
fig.circle(ax.fx(e0), ax.fy(e0), 3.2, C.OBS, C.WHITE, 0.8)
fig.circle(ax.fx(e0), ax.fy(E0), 3.2, C.REF, C.WHITE, 0.8)
fig.text(ax.fx(e0) + 7, ax.fy(-0.19) + 4, "Δ 0.02", T.SMALL, 700)
fig.rich(74, 66, [("E", 400, C.INK, True), (" = ", 400, C.INK, False), ("e", 400, C.INK, True),
                  (" + ", 400, C.INK, False), ("e", 400, C.INK, True), ("2", 400, C.INK, False, "super"),
                  ("/2", 400, C.INK, False)], T.BODY)
fig.text(74, 82, "Green–Lagrange (solid)", T.SMALL, fill=C.MUTED)
fig.text(74, 96, "engineering e (dashed)", T.SMALL, fill=C.MUTED)
fig.rich(282, 66, [("e", 700, C.INK, True), ("  →  ", 700, C.INK, False), ("E", 700, C.INK, True)], T.SMALL + 0.5)
fig.kv_table(282, 86, [(f2(e, True), f3(e + e * e / 2))
                       for e in (-0.30, -0.20, -0.10, 0.10, 0.20)], w=92, row_h=17)
fig.lines(24, 232, ["Same one-dimensional motion: the 0.02 gap is a definitional",
                    "difference and involves no tracking error."], T.SMALL)

# ---- b: layer, frame and axes ----------------------------------------------------------------------
fig.col_rule(398, 6, ROW2 - 12)
fig.panel(410, 24, "b", "Layer, frame and axes must be stated")
cx, cy, ro, rm, ri = 492, 140, 56, 43, 29
fig.path(annulus_path(cx, cy, ro, ri), fill=C.SILK, extra='fill-rule="evenodd"')
for r, dash in ((ri, ""), (rm, 'stroke-dasharray="3 2"'), (ro, "")):
    fig.circle(cx, cy, r, stroke=C.OBS, w=1.1, extra=dash)
for r, lab, ang in ((ri, "endocardial", 20), (rm, "mid-wall", 34), (ro, "epicardial", 48)):
    a = math.radians(ang)
    x0, y0 = cx + r * math.cos(a), cy + r * math.sin(a)
    fig.line(x0, y0, cx + 74, y0, C.OBS, 0.7)
    fig.text(cx + 78, y0 + 4, lab, T.SMALL)
th = math.radians(-125)
px, py = cx + rm * math.cos(th), cy + rm * math.sin(th)
fig.arrow(px, py, px + 26 * math.cos(th), py + 26 * math.sin(th), C.INK, 1.3, 6)
fig.arrow(px, py, px - 26 * math.sin(th), py + 26 * math.cos(th), C.INK, 1.3, 6)
fig.circle(px, py, 3, C.INK)
fig.text(px + 30 * math.cos(th) - 2, py + 30 * math.sin(th) - 4, "radial", T.SMALL, anchor="end")
fig.text(px - 30 * math.sin(th) + 4, py + 30 * math.cos(th) - 6, "circumferential", T.SMALL)
fig.kv_table(630, 66, [("layer", "endo · mid · epi"), ("reference", "ED or ES frame"), ("axes", "centroid / centreline"),
                       ("slice", "2D: no through-plane")], w=150, row_h=17, title="Choices to report")
fig.lines(414, 226, ["Layer values differ; local axes depend on the reference frame and",
                     "centreline, and a 2D slice omits through-plane terms."], T.SMALL)

# ---- c: which peak ---------------------------------------------------------------------------------
fig.row_rule(ROW2 - 12)
E = [-0.17 * gauss(t, 0.30, 0.12 / math.sqrt(2)) - 0.20 * gauss(t, 0.50, 0.09 / math.sqrt(2)) for t in ts]
t_es = 0.39
i_sys = min(range(len(ts)), key=lambda i: E[i] if ts[i] <= t_es else 0)
i_all = min(range(len(ts)), key=lambda i: E[i])
k_es = min(range(len(ts)), key=lambda i: abs(ts[i] - t_es))
reads = [(ts[i_sys], E[i_sys], "peak systolic"), (t_es, E[k_es], "end-systolic"), (ts[i_all], E[i_all], "post-systolic")]
fig.panel(20, ROW2 + 14, "c", f"One curve, three peaks: {f2(max(r[1] for r in reads))} to {f2(min(r[1] for r in reads))}")
ax = fig.axes(66, ROW2 + 40, 196, 140, (0, 1), (-0.27, 0.04), [0, 0.5, 1], [-0.2, -0.1, 0],
              "normalised cycle time", "segment strain", xfmt=lambda v: f"{v:g}",
              yfmt=lambda v: f"{v:.1f}".replace("-", "−") if v else "0")
ax.vline(t_es, C.MUTED, 0.9)
fig.text(ax.fx(t_es) + 4, ROW2 + 50, "end-systole", T.SMALL, fill=C.MUTED)
ax.line(ts, E, C.REF, 1.8)
for k, (tx, ex, _) in enumerate(reads, start=1):
    fig.badge(ax.fx(tx) + (-12 if k == 1 else (12 if k == 3 else 0)), ax.fy(ex) + (12 if k != 2 else -14), k, C.REF)
    fig.circle(ax.fx(tx), ax.fy(ex), 3.2, C.REF, C.WHITE, 0.8)
fig.kv_table(282, ROW2 + 76, [(f"{k}  {lab}", f2(ex)) for k, (_, ex, lab) in enumerate(reads, start=1)],
             w=110, row_h=17, title="readout")
fig.lines(24, ROW2 + 230, ["End-systolic, peak-systolic and whole-cycle peaks diverge",
                           "with dyssynchrony or post-systolic shortening."], T.SMALL)

# ---- d: aggregation order --------------------------------------------------------------------------
fig.col_rule(398, ROW2, H - 4)
p1 = [-0.20 * gauss(t, 0.28, 0.07 / math.sqrt(2)) for t in ts]
p2 = [-0.20 * gauss(t, 0.46, 0.07 / math.sqrt(2)) for t in ts]
mean = [(a + b) / 2 for a, b in zip(p1, p2)]
mm = min(mean)
fig.panel(410, ROW2 + 14, "d", f"Aggregation order: {f2(mm)} vs {f2((min(p1) + min(p2)) / 2)}")
ax = fig.axes(456, ROW2 + 40, 196, 140, (0, 1), (-0.27, 0.04), [0, 0.5, 1], [-0.2, -0.1, 0],
              "normalised cycle time", "strain", xfmt=lambda v: f"{v:g}",
              yfmt=lambda v: f"{v:.1f}".replace("-", "−") if v else "0")
ax.line(ts, p1, C.OBS, 1.2)
ax.line(ts, p2, C.OBS, 1.2)
ax.line(ts, mean, C.INF, 1.8)
ax.hline(mm, C.INF, 0.9)
ax.hline(-0.20, C.INK, 0.9)
fig.text(ax.fx(0.6), ax.fy(-0.13) + 4, "grey: two points", T.SMALL, fill=C.MUTED)
fig.text(ax.fx(0.6), ax.fy(-0.13) + 17, "in one segment", T.SMALL, fill=C.MUTED)
fig.text(ax.fx(0.55), ax.fy(-0.06), "segment mean", T.SMALL)
fig.kv_table(672, ROW2 + 76, [("min of mean", f2(mm)), ("mean of minima", f2((min(p1) + min(p2)) / 2)),
                              ("difference", f2(mm - (min(p1) + min(p2)) / 2))], w=108, row_h=17, title="readout")
fig.lines(414, ROW2 + 230, ["Averaging before or after selecting the temporal peak gives",
                            "different values for the same field."], T.SMALL)

export(fig, "Figure_S1_strain_definition_traps")

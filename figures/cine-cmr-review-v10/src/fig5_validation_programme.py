"""Figure 5: what each validation target can establish, and a staged programme for regional claims.

agarwood-scifig house style, 190 mm. Conceptual synthesis; panel c is an analytic example
(six segment values with the same mean, −0.18). Resource counts are those listed in Table 4.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
from scifig_common import C, T, export, start, wrap  # noqa: E402

H = 588
fig = start(H, "Figure 5 | Validation targets and a staged programme for regional claims",
            legend=[("supports", C.SUP), ("does not establish alone", C.INF)],
            footer=["Conceptual synthesis; no study data. c is an analytic example (segment values chosen to share the "
                    "mean −0.18). Resources as listed in Table 4.",
                    "STRAUS, MRXCAT2.0, CMAC: simulation / phantom / benchmark resources; LGE, late gadolinium enhancement."])

# ---- a: three-rule table -------------------------------------------------------------------------
fig.panel(20, 24, "a", "Each validation target supports one claim, not the next")
c0, c1, c2, x_end = 20, 222, 520, 780
top = 42
fig.line(c0, top, x_end, top, C.INK, 1.2)
hy = top + 18
fig.circle(c0 + 5, hy - 4, 4.5, C.REF)
fig.text(c0 + 15, hy, "Validation target", T.BODY, 700)
fig.tick(c1 + 6, hy - 4, C.SUP)
fig.text(c1 + 16, hy, "Strongest claim it supports", T.BODY, 700)
fig.xmark(c2 + 6, hy - 4, C.INF, 3.4)
fig.text(c2 + 16, hy, "Does not establish on its own", T.BODY, 700)
fig.line(c0, top + 27, x_end, top + 27, C.INK, 0.9)
rows = [
    ("Known motion", "phantom, STRAUS, MRXCAT2.0",
     "representation capacity and technical error in the simulated regime", "in-vivo accuracy"),
    ("Paired DENSE or tagging", "same session, registered",
     "material-sensitive agreement under matched definitions", "focal location or extent, unless measured"),
    ("Scan–rescan", "same subject, re-imaged", "precision; accuracy needs a reference", "bias"),
    ("LGE or tissue characterisation", "scar or fibrosis label",
     "biological association; motion error stays unmeasured", "pointwise displacement error"),
    ("Outcome", "events, prognosis", "prognostic association; utility needs a decision study", "decision impact"),
]
RH = 34
y = top + 27
for i, (tgt, sub, yes, no) in enumerate(rows):
    fig.text(c0, y + 15, tgt, T.BODY - 0.5, 700)
    fig.text(c0, y + 28, sub, T.SMALL, fill=C.MUTED)
    for k, s in enumerate(wrap(yes, c2 - c1 - 34, T.CAPTION)):
        fig.text(c1 + 16, y + 15 + k * 13, s, T.CAPTION)
    for k, s in enumerate(wrap(no, x_end - c2 - 18, T.CAPTION)):
        fig.text(c2 + 16, y + 15 + k * 13, s, T.CAPTION, fill=C.MUTED)
    y += RH
    fig.line(c0, y, x_end, y, C.INK if i == len(rows) - 1 else C.GRID, 1.2 if i == len(rows) - 1 else 0.8)
fig.col_rule(c1 - 8, top + 27, y)
fig.col_rule(c2 - 8, top + 27, y)

# ---- b: staged programme ------------------------------------------------------------------------
by = y + 34
fig.panel(20, by, "b", "Pre-specify, then escalate the reference stage by stage")
lx, tx, rx, rw = 34, 58, 300, 236
fig.text(rx, by + 26, "Resources (Table 4)", T.SMALL, 700, fill=C.MUTED)
steps = [
    ("✓", "Pre-specify the measurement contract", "estimand · reference · tolerance · data splits", []),
    ("1", "Stage 1 · Known motion", "vary width, extent, amplitude, timing, resolution and noise",
     [("STRAUS", "3 templates × 6 states"), ("MRXCAT2.0", "programmable generator"), ("CMAC", "dynamic phantom")]),
    ("2", "Stage 2 · Paired material reference", "cine with DENSE or tagging in one session; registered; "
     "reference blinded", [("Stanford", "51/55 · not file-verified"), ("CMAC", "15 volunteers, 12 landmarks")]),
    ("3", "Stage 3 · Tissue and decisions", "LGE, responsiveness, decision impact",
     [("Clinical cohorts", "LGE or outcomes")]),
]
ys = [by + 50, by + 100, by + 168, by + 232]
fig.line(lx, ys[0], lx, ys[-1], C.RULE, 1.6)
for i, ((mark, head, desc, res), yy) in enumerate(zip(steps, ys)):
    if mark == "✓":
        fig.circle(lx, yy, 9, C.WHITE, C.INK, 1.2)
        fig.tick(lx, yy, C.INK, 3.8, 1.4)
    else:
        fig.circle(lx, yy, 9, C.REF)
        fig.text(lx, yy + 4.5, mark, 12, 700, C.WHITE, "middle")
    fig.text(tx, yy + 4, head, T.BODY, 700)
    for k, s in enumerate(wrap(desc, rx - tx - 16, T.CAPTION)):
        fig.text(tx, yy + 19 + k * 13.5, s, T.CAPTION, fill=C.MUTED)
    if res:
        fig.kv_table(rx, yy + 4, res, w=rw, row_h=18)
fig.text(tx, ys[-1] + 44, "Counts are resource units, not independent test participants.", T.SMALL, fill=C.MUTED)

# ---- c: equal-mean test --------------------------------------------------------------------------
fig.col_rule(548, by - 18, H - 4)
fig.panel(560, by, "c", "Same mean, focal deficit")
foc = [-0.22, -0.22, -0.06, -0.18, -0.20, -0.20]
ax = fig.axes(606, by + 30, 170, 128, (0.5, 6.5), (-0.26, 0.0), [1, 2, 3, 4, 5, 6], [-0.2, -0.1, 0],
              xlabel="segment", ylabel="segment strain", yfmt=lambda t: f"{t:.1f}".replace("-", "−") if t else "0")
ax.hline(-0.18, C.REF, 1.6, "5 3")
xs = list(range(1, 7))
ax.line(xs, foc, C.INF, 1.8)
for xv, val in zip(xs, foc):
    fig.circle(ax.fx(xv), ax.fy(val), 3.4, C.INF, C.WHITE, 0.8)
fig.text(ax.fx(6.45), ax.fy(-0.18) - 6, "uniform −0.18", T.SMALL, fill=C.MUTED, anchor="end")
fig.text(ax.fx(3) - 8, ax.fy(-0.06) + 4, "−0.06", T.SMALL, 700, anchor="end")
fig.text(ax.fx(3) + 8, ax.fy(-0.06) + 4, "focal deficit", T.SMALL, fill=C.MUTED)
fig.kv_table(560, by + 214, [("segments 1–3, focal", "−0.22 · −0.22 · −0.06"), ("segments 4–6, focal", "−0.18 · −0.20 · −0.20"),
                             ("global mean, both fields", "−0.18"), ("range, focal / uniform", "0.16 / 0")], w=220, row_h=17)
fig.lines(560, by + 292, ["Recovering the mean proves", "nothing about the deficit."], T.SMALL)

export(fig, "Figure_5_validation_targets_programme")

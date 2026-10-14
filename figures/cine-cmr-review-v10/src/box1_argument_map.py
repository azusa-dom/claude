"""Box 1: structure of the argument. Ten numbered steps in four groups, each tied to the section,
figure or table where it is developed; two 'leaps' marked. agarwood-scifig journal variant, 190 mm.
Unnumbered box in the manuscript (caption*), so the figure numbering is unchanged.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
from scifig_common import C, T, export, start, tw, wrap  # noqa: E402

SM, BODY = T.SMALL, T.BODY - 0.5
X0, CW, GAP = 20, 238, 22
COLS = [X0, X0 + CW + GAP, X0 + 2 * (CW + GAP)]

GROUPS = {
    "A": ("A · Clinical need versus image physics", C.OBS),
    "B": ("B · From physical gap to dependent number", C.INF),
    "C": ("C · Evidence audit: what each endpoint supports", C.REF),
    "D": ("D · Engineering the claim", C.SUP),
}
S = {
    1: ("Regional function is a distinct measurement problem",
        "Ejection fraction compresses 3-D deformation into a chamber ratio; compensation, cancellation and timing differences are hidden.", "§1"),
    2: ("Cine carries no material-point identity",
        "Tagging imprints a pattern and DENSE encodes displacement in phase; bSSFP myocardium is homogeneous, so identity is not in the signal.", "§2 · Fig. 2"),
    3: ("Correspondence is inferred, and the prior selects",
        "Many deformation fields fit the same images; smoothness, incompressibility, biomechanics or a training distribution picks one.", "§2–3 · Fig. 1a · Table 1"),
    4: ("A reported value depends on three choices",
        "Which estimator inferred it, how strain was defined, what it was validated against: ‘is cine FT regional strain accurate’ is incomplete.", "§2"),
    5: ("Boundary endpoints cannot confirm dense correspondence",
        "Dice, surface distance, field regularity and sparse landmarks measure boundary geometry and sampled points; identical borders admit different interior motion.", "§4 · Table 2"),
    6: ("Each validation target supports one claim and leaves one gap",
        "Known motion, paired DENSE or tagging, scan–rescan, LGE, outcome; software, sampling, strain convention, statistical unit and reference uncertainty are stated before attribution.", "§4–5 · Fig. 1b · Fig. 3"),
    7: ("Paired studies support a threefold qualification",
        "Circumferential strain, global or whole-slice mid-ventricular scale, matched definitions; agreement varies with component, scale and software, radial least.", "§4 · Tables 2–3"),
    8: ("Focal attributes are rarely measured directly",
        "Magnitude, location, extent and timing; the MRXCAT2.0 test reports whole-slice errors without scar-level recovery; equal means can hide a focal deficit.", "Fig. 4 · Table 3 · Fig. 5c"),
    9: ("A measurement contract makes the claim falsifiable",
        "Acquisition, estimator, population, spatial unit, strain definition and reference state, time point, comparator, prespecified tolerance.", "§6"),
    10: ("No single agreement index validates all of it",
         "Known motion: capacity and technical error. Paired material reference: material-sensitive agreement. Scan–rescan: precision. Tissue and decisions: relevance and impact.", "§6 · Fig. 5 · Table 4"),
}
# column plans: ("head", group, span_cols) | ("step", n) | ("leap", text) | ("space", px)
PLAN = [
    [("head", "A", 1), ("step", 1), ("step", 2), ("leap", "Leap 1: physics → estimation"), ("head", "B", 1), ("step", 3), ("step", 4)],
    [("head", "C", 2), ("step", 5), ("leap", "Leap 2: reported endpoint → supported claim"), ("step", 6), ("step", 7)],
    [("space", 0), ("step", 8), ("head", "D", 1), ("step", 9), ("step", 10)],
]
TOP, HEAD_H, LEAP_H, STEP_GAP = 24, 22, 26, 10


def step_height(n):
    title, body, _ = S[n]
    return 4 + len(wrap(title, CW - 24, BODY, True)) * 14 + len(wrap(body, CW - 24, SM)) * 13 + 15 + STEP_GAP


def column_height(plan):
    h = 0
    for op in plan:
        if op[0] == "head":
            h += HEAD_H + (6 if h else 0)
        elif op[0] == "space":
            h += HEAD_H
        elif op[0] == "leap":
            h += LEAP_H
        else:
            h += step_height(op[1])
    return h


H = TOP + max(column_height(p) for p in PLAN) - STEP_GAP + 6
fig = start(H, "Box 1 | Structure of the argument",
            footer=["Ten steps; section, figure and table references point to where each step is developed."])

for ci, plan in enumerate(PLAN):
    x = COLS[ci]
    if ci:
        fig.col_rule(x - GAP / 2, TOP + HEAD_H if ci == 2 else 6, H - 4)
    y = TOP
    for op in plan:
        if op[0] == "head":
            if y > TOP:
                y += 6
            label, color = GROUPS[op[1]]
            width = CW if op[2] == 1 else op[2] * CW + (op[2] - 1) * GAP
            fig.text(x, y + 12, label, SM, 700, fill=color)
            fig.line(x, y + 18, x + width, y + 18, color, 1.2)
            y += HEAD_H
        elif op[0] == "space":
            y += HEAD_H
        elif op[0] == "leap":
            fig.arrow(x + 8, y + 4, x + 8, y + LEAP_H - 6, C.INK, 1.1, 5)
            fig.text(x + 18, y + 16, op[1], SM, 700, fill=C.MUTED, italic=True)
            y += LEAP_H
        else:
            n = op[1]
            title, body, ref = S[n]
            fig.badge(x + 8, y + 10, n, C.INK)
            tl = wrap(title, CW - 24, BODY, True)
            for k, t_ in enumerate(tl):
                fig.text(x + 22, y + 14 + k * 14, t_, BODY, 700)
            yy = y + 14 + len(tl) * 14 - 2
            bl = wrap(body, CW - 24, SM)
            for k, t_ in enumerate(bl):
                fig.text(x + 22, yy + k * 13, t_, SM, fill=C.MUTED)
            fig.text(x + CW, yy + len(bl) * 13 + 1, ref, SM, 700, anchor="end")
            y += step_height(n)

export(fig, "Box_1_argument_map")

"""Figure 1 (journal variant): two-track evidence map for regional strain from routine cine CMR.

agarwood-scifig journal variant on a wide canvas: 1040 px = 247 mm (a landscape page), smallest text 10.5 px
(7 pt). Wide, two-row layout:
row a puts each station's graphic beside its text; row b prints every value in a right-hand column.
Panel a is a conceptual schematic (readouts computed from the drawn curves); panel b transcribes values
reported in the cited studies as given in the manuscript's Tables 2–3, §4 and §6.6, not pooled.
The poster variant is src/Figure_1_two_track_poster.svg.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
from scifig_common import C, T, export, start, tw, wrap  # noqa: E402
from scifig import CMAP_STRAIN, Rng, annulus_path, cmap, gauss, wedge_path  # noqa: E402

W, H = 1040, 538
fig = start(H, "Figure 1 | Two-track evidence map for regional strain from routine cine CMR", width=W, width_mm=247,
            footer=["a: conceptual schematic, readouts computed from the drawn curves. b: values as reported in the cited "
                    "studies (manuscript Tables 2–3, §4, §6.6); not pooled.",
                    "ED/ES, end-diastole/-systole; FT, feature tracking; LoA, limits of agreement; WMA, wall-motion abnormality."])

X0, X1 = 20, 1020
SM = T.SMALL
BODY = 12.0


def f2(x):
    return f"{x:.2f}".replace("-", "−")


def annulus(cx, cy, R, r):
    fig.path(annulus_path(cx, cy, R, r), fill=C.SILK, extra='fill-rule="evenodd"')
    fig.circle(cx, cy, R, stroke=C.OBS, w=1.0)
    fig.circle(cx, cy, r, stroke=C.OBS, w=1.0)


def badge_letter(x, y, s):
    fig.circle(x, y, 6.5, C.INK)
    fig.text(x, y + 3.6, s, 10.5, 700, C.WHITE, "middle")


def muted_lines(x, y, lines, lead=13):
    for k, s in enumerate(lines):
        fig.text(x, y + k * lead, s, SM, fill=C.MUTED)


# =============================================================== a: estimation track
fig.panel(X0, 24, "a", "Estimation: cine provides cues, correspondence is inferred, strain is defined by convention")
SX = [X0, 248, 526, 784]            # station left edges
SW = [220, 270, 250, 236]
TAG_Y, TITLE_Y, GY = 46, 61, 68     # tag, station title, graphic top


def station(i, tag, color, title):
    x = SX[i]
    fig.stage_tag(x, TAG_Y, tag, color)
    fig.text(x, TITLE_Y, title, BODY, 700)
    if i:
        fig.col_rule(x - 8, 38, 182)


# ---- 1 observed ----------------------------------------------------------------------------
station(0, "1 · OBSERVED", C.OBS, "Cine bSSFP, short axis")
x = SX[0]
rng = Rng(5)
for k, (cx, lab) in enumerate(((x + 24, "ED"), (x + 76, "ES"))):
    R, r = (23, 13) if k == 0 else (23, 9)
    annulus(cx, GY + 34, R, r)
    for _ in range(140):
        px, py = (rng() * 2 - 1) * R, (rng() * 2 - 1) * R
        if r + 1.5 < math.hypot(px, py) < R - 1.5:
            fig.circle(cx + px, GY + 34 + py, 0.6, C.OBS, extra='opacity="0.7"')
    fig.text(cx, GY + 34 + R + 13, lab, SM, 700, anchor="middle")
fig.arrow(x + 48, GY + 34, x + 52, GY + 34, C.MUTED, 1.0, 4)
badge_letter(x + SW[0] - 8, TAG_Y - 4, "I")
muted_lines(x + 112, GY + 18, ["boundaries visible;", "weak intramural", "texture; no material", "markers"])

# ---- 2–3 inferred --------------------------------------------------------------------------
station(1, "2–3 · INFERRED", C.INF, "Estimated displacement u(X, t)")
x = SX[1]
cx, cy, R, r = x + 26, GY + 30, 25, 14
annulus(cx, cy, R, r)
for rad, n, off in ((18.5, 8, 0.2), (23.5, 12, 0.0)):
    for i in range(n):
        th = 2 * math.pi * i / n + off
        x0, y0 = cx + rad * math.cos(th), cy + rad * math.sin(th)
        dx = -3.4 * math.cos(th) - 1.5 * math.sin(th)
        dy = -3.4 * math.sin(th) + 1.5 * math.cos(th)
        fig.arrow(x0, y0, x0 + dx, y0 + dy, C.INF, 0.8, 2.2)
badge_letter(x + SW[1] - 26, TAG_Y - 4, "E")
badge_letter(x + SW[1] - 8, TAG_Y - 4, "R")
muted_lines(x + 60, GY + 12, ["prior αR:", "tracking, registration,", "biomechanics, learned"])
muted_lines(x + 168, GY + 12, ["D alone does not", "identify φ; identical", "masks admit", "different material",
                               "maps; αR selects", "among them (Fig. 2)"])
fig.rich(x, GY + 84, [("φ̂", 400, C.INK, True), (" = arg min ", 400, C.INK, False), ("D", 400, C.INK, True),
                      ("(", 400, C.INK, False), ("I", 400, C.INK, True), ("0", 400, C.INK, False, "sub"),
                      (", ", 400, C.INK, False), ("I", 400, C.INK, True), ("t", 400, C.INK, True, "sub"),
                      (" ∘ ", 400, C.INK, False), ("φ", 400, C.INK, True), (") + ", 400, C.INK, False),
                      ("α", 700, C.INF, True), ("R", 700, C.INF, True), ("(", 400, C.INK, False),
                      ("φ", 400, C.INK, True), (")", 400, C.INK, False)], BODY)

# ---- 4 defined -----------------------------------------------------------------------------------
station(2, "4 · DEFINED", C.REF, "Green–Lagrange Ecc, pixelwise")
x = SX[2]
cx, cy = x + 34, GY + 32
segs = [-0.18, -0.19, -0.17, -0.08, -0.20, -0.18]        # mid-ventricular segments 7–12; segment 11 reduced
for i, v in enumerate(segs):
    a0 = -math.pi / 2 + i * math.pi / 3
    fig.path(wedge_path(cx, cy, 13, 25, a0, a0 + math.pi / 3), C.WHITE, 1.0, fill=cmap(CMAP_STRAIN, v))
    am = a0 + math.pi / 6
    fig.text(cx + 32 * math.cos(am), cy + 32 * math.sin(am) + 3.5, str(7 + i), SM, fill=C.MUTED, anchor="middle")
fig.circle(cx, cy, 13, C.WHITE, C.OBS, 0.8)
fig.circle(cx, cy, 25, "none", C.OBS, 0.8)
muted_lines(x, cy + 44, ["fill = Ecc;", "seg. 11 reduced"])
specs = [("01", "ED reference"), ("02", "E = ½(FᵀF − I)"), ("03", "c/r/l axes, signed"), ("04", "endo·mid·epi, 2D"),
         ("05", "∂u/∂X, smoothed")]
for k, (a, b) in enumerate(specs):
    yy = GY + 12 + k * 13
    fig.text(x + 82, yy, a, SM, fill=C.MUTED)
    fig.text(x + 98, yy, b, SM)
muted_lines(x + 82, GY + 12 + 5 * 13 + 8, ["choices 01–05 fix the value", "before any region is reported"])

# ---- 5 reported ------------------------------------------------------------------------------------
station(3, "5 · REPORTED", C.REF, "Segmental Ecc(t), mid ventricle")
x = SX[3]
ts = [i / 200 for i in range(201)]
w = 1 / math.sqrt(2)
curves = [[-0.19 * gauss(t, 0.40, 0.13 * w) for t in ts], [-0.20 * gauss(t, 0.42, 0.13 * w) for t in ts],
          [-0.18 * gauss(t, 0.39, 0.12 * w) for t in ts], [-0.21 * gauss(t, 0.41, 0.14 * w) for t in ts],
          [-0.17 * gauss(t, 0.38, 0.12 * w) for t in ts]]
seg11 = [-0.08 * gauss(t, 0.26, 0.10 * w) - 0.12 * gauss(t, 0.58, 0.09 * w) for t in ts]
T_ES = 0.40
ax = fig.axes(x + 24, GY + 2, 56, 58, (0, 1), (-0.25, 0.02), [0, 0.5, 1], [-0.2, -0.1, 0], "", "",
              xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:.1f}".replace("-", "−") if v else "0")
fig.text(x + 52, GY + 2 + 58 + 27, "cycle time", SM, anchor="middle")
ax.vline(T_ES, C.MUTED, 0.8)
fig.text(ax.fx(T_ES) + 3, GY + 10, "ES", SM, fill=C.MUTED)
for cv in curves:
    ax.line(ts, cv, C.OBS, 0.9)
ax.line(ts, seg11, C.INF, 1.6)
k_es = min(range(len(ts)), key=lambda i: abs(ts[i] - T_ES))
i_sys = min(range(len(ts)), key=lambda i: seg11[i] if ts[i] <= T_ES else 0)
i_all = min(range(len(ts)), key=lambda i: seg11[i])
for i in (k_es, i_sys, i_all):
    fig.circle(ax.fx(ts[i]), ax.fy(seg11[i]), 2.6, C.WHITE, C.INF, 1.1)
allc = curves + [seg11]
mean = [sum(cv[i] for cv in allc) / len(allc) for i in range(len(ts))]
reads = [("06", "AHA mid 7–12", ""), ("07", "at ES", f2(seg11[k_es])), ("", "peak sys.", f2(seg11[i_sys])),
         ("", "post-sys.", f2(seg11[i_all])), ("08", "min(mean)", f2(min(mean))),
         ("", "mean(min)", f2(sum(min(cv) for cv in allc) / len(allc)))]
for k, (n_, a, b) in enumerate(reads):
    yy = GY + 12 + k * 13
    fig.text(x + 100, yy, n_, SM, fill=C.MUTED)
    fig.text(x + 116, yy, a, SM, fill=C.MUTED if b else C.INK)
    fig.text(x + 210, yy, b, SM, 700, anchor="end")
muted_lines(x + 100, GY + 12 + 6 * 13 + 8, ["06–08 select one value", "from one curve (○, seg. 11)"])

# ---- failure points -------------------------------------------------------------------------------
fy = 198
fig.line(X0, fy - 12, X1, fy - 12, C.GRID, 0.8)
fig.text(X0, fy + 4, "Independently testable failure points:", SM, 700)
items = [("I", "input sufficiency", "re-image the motion more finely"), ("E", "estimation", "vary α with images fixed"),
         ("R", "representation", "project the known field onto the basis")]
xx = X0 + 230
for let, name, test in items:
    badge_letter(xx, fy, let)
    fig.rich(xx + 10, fy + 4, [(name, 700, C.INK, False), (" · " + test, 400, C.MUTED, False)], SM)
    xx += 10 + tw(name, SM, True) + tw(" · " + test, SM) + 20
if xx - 20 > X1:
    print(f"warning: failure-point row overflows by {xx - 20 - X1:.0f} px")

# =============================================================== b: validation track
fig.row_rule(216)
fig.panel(X0, 240, "b", "Validation: one claim per reference")
leg = [("DENSE", "dot", C.DEEP), ("tagging", "dot", C.AGAR), ("cine FT", "dot", C.OBS), ("cine DL", "dot", C.SUP),
       ("comparator", "open", C.OBS)]
leg_w = sum(12 + len(lab) * 6.1 + 14 for lab, _, _ in leg)      # legend_items' own advance rule
lw = leg_w + 15 + tw("supported", SM) + 14 + 15 + tw("not established by this evidence alone", SM)
lx = X1 - lw
fig.legend_items(lx, 240, leg, gap=14)
lx2 = lx + leg_w
fig.check(lx2, 240, "supported", SM)
fig.cross(lx2 + 15 + tw("supported", SM) + 14, 240, "not established by this evidence alone", SM)

CW, GAP = 190, 12
TY, RY, OK_Y, CT_Y, CH_Y = 270, 283, 300, 336, 344        # title, refs, ✓ (✕ follows), chart title, chart top
CAP_Y = 494


def column(i, title, refs, ok, no, chart_title, caption):
    x = X0 + i * (CW + GAP)
    if i:
        fig.col_rule(x - GAP / 2, 258, H - 4)
    fig.text(x, TY, title, BODY, 700)
    for k, s in enumerate(wrap(refs, CW - 4, SM)):
        fig.text(x, RY + k * 13, s, SM, fill=C.MUTED)
    oks = wrap(ok, CW - 20, SM)
    fig.check(x, OK_Y, oks[0], SM)
    for k, s_ in enumerate(oks[1:]):
        fig.text(x + 15, OK_Y + 13 * (k + 1), s_, SM)
    ny = OK_Y + 13 * len(oks) + 1
    fig.cross(x, ny, no, SM)
    fig.text(x, CT_Y, chart_title, SM, 700)
    for k, s in enumerate(wrap(caption, CW - 4, SM)):
        fig.text(x, CAP_Y + k * 13, s, SM, fill=C.MUTED)
    for s_, bold in ((title, True), (chart_title, True), (no, False)):
        if tw(s_, BODY if s_ is title else SM, bold) + (15 if s_ is no else 0) > CW - 2:
            print(f"warning: column {i} text too wide: {s_}")
    return x


def value_rows(x, y, rows, xlim, ticks=(), w=70, label_w=62, row_h=16, xlabel="", fmt=None):
    """label (muted) | range bar, dot or dot + comparator | value column right-aligned at the column edge."""
    fmt = fmt or (lambda v: f"{v:g}")
    ax0 = x + label_w
    fx = lambda v: ax0 + (v - xlim[0]) / (xlim[1] - xlim[0]) * w
    n = len(rows)
    for t in ticks:
        fig.line(fx(t), y, fx(t), y + n * row_h, C.GRID, 0.8)
    for i, (lab, lo, hi, col, comp, vt) in enumerate(rows):
        yy = y + row_h / 2 + i * row_h
        fig.text(x, yy + 3.5, lab, SM)
        if comp is not None:
            fig.line(fx(comp) + 3, yy, fx(lo) - 3, yy, C.GRID, 1)
            fig.circle(fx(comp), yy, 3, C.WHITE, col, 1.2)
        if hi > lo:
            fig.line(fx(lo), yy, fx(hi), yy, col, 4, 'stroke-linecap="round"')
        else:
            fig.circle(fx(lo), yy, 3, col)
        fig.text(x + CW, yy + 3.5, vt, SM, 700, anchor="end")
    if ticks:
        fig.axes(ax0, y + n * row_h, w, 0, xlim, (0, 1), ticks, (), xlabel, xfmt=fmt, yaxis=False)
    return y + n * row_h


def bar_rows(x, y, rows, w=70, label_w=62, row_h=16, ticks=(), xlabel=""):
    ax0 = x + label_w
    for i, (lab, v, col, vt) in enumerate(rows):
        yy = y + i * row_h + row_h / 2
        fig.text(x, yy + 3.5, lab, SM)
        fig.rect(ax0, yy - 4.5, v * w, 9, col, rx=1)
        fig.text(x + CW, yy + 3.5, vt, SM, 700, anchor="end")
    if ticks:
        fig.axes(ax0, y + len(rows) * row_h, w, 0, (0, 1), (0, 1), ticks, (), xlabel, xfmt=lambda v: f"{v:g}", yaxis=False)
    return y + len(rows) * row_h


# ---- 1 known motion --------------------------------------------------------------------------------
x = column(0, "Known motion", "MRXCAT2.0 test of DeepStrain", "capacity, technical error", "in-vivo accuracy",
           "estimator error (mean ± SD)",
           "○ infarct case, EF 49%. Dice 0.82; displacement 1.0 ± 0.9 mm. Slice means only (Fig. 4).")
ax0, w = x + 66, 66
fx = lambda v: ax0 + (v + 0.5) / 0.62 * w
rows = [("Ecc, 4 cases", 0.02, 0.04, C.OBS, False), ("Err, 4 cases", -0.24, 0.21, C.INF, False),
        ("Err, infarct", -0.20, 0.21, C.INF, True)]
fig.line(fx(0), CH_Y + 4, fx(0), CH_Y + 4 + 3 * 18, C.INK, 1, 'stroke-dasharray="3 2"')
for i, (lab, m, sd, col, op) in enumerate(rows):
    yy = CH_Y + 4 + 9 + i * 18
    fig.text(x, yy + 3.5, lab + (" ○" if op else ""), SM)
    fig.line(fx(m - sd), yy, fx(m + sd), yy, col, 1.4)
    fig.circle(fx(m), yy, 3, C.WHITE if op else col, col, 1.2)
    fig.text(x + CW, yy + 3.5, f"{f2(m)} ± {f2(sd)}", SM, 700, anchor="end")
fig.axes(ax0, CH_Y + 4 + 3 * 18, w, 0, (-0.5, 0.12), (0, 1), [-0.4, -0.2, 0], (), "strain error",
         xfmt=lambda v: f"{v:.1f}".replace("-", "−") if v else "0", yaxis=False)

# ---- 2 paired DENSE / tagging -------------------------------------------------------------------------
x = column(1, "Paired DENSE / tagging", "Militaru 2021; Cao 2018; Wang 2023", "material-sensitive agreement",
           "reference error", "ICC; range = 3 vendors",
           "Militaru: n = 61, 3 T. Cao: DENSE vs tagging Ecc 0.778. StrainNet (DL): 59 cine tests, DENSE reference.")
fig.text(x, CH_Y + 8, "cine FT vs tagging, global", SM, fill=C.MUTED)
y = value_rows(x, CH_Y + 12, [("LS", 0.92, 0.94, C.OBS, None, "0.92–0.94"), ("CS", 0.88, 0.91, C.OBS, None, "0.88–0.91"),
                               ("RS", 0.10, 0.81, C.OBS, None, "0.10–0.81")], (0, 1))
fig.text(x, y + 14, "StrainNet (●) vs FT (○), Ecc", SM, fill=C.MUTED)
y = value_rows(x, y + 18, [("global", 0.87, 0.87, C.SUP, 0.72, "0.87 vs 0.72"), ("segment", 0.75, 0.75, C.SUP, 0.48, "0.75 vs 0.48")],
               (0, 1), [0, 0.5, 1])

# ---- 3 precision -----------------------------------------------------------------------------------------
x = column(2, "Precision", "Yoon 2023; Bell 2025", "precision at tested scale", "accuracy (bias)", "REGAIN vs GRAPPA",
           "REGAIN: 49 participants; mean global differences near zero. Strain-8: same day, 8 protocols.")
fig.text(x, CH_Y + 8, "95% LoA, global FT strain", SM, fill=C.MUTED)
fig.line(x + 62 + 35, CH_Y + 12, x + 62 + 35, CH_Y + 12 + 3 * 16, C.INK, 1, 'stroke-dasharray="3 2"')
y = value_rows(x, CH_Y + 12, [("radial", -7, 6, C.OBS, None, "−7 to 6"), ("circ.", -2, 3, C.OBS, None, "−2 to 3"),
                               ("long.", -3, 3, C.OBS, None, "−3 to 3")], (-8, 8), [-8, 0, 8],
               fmt=lambda v: f"{v:g}".replace("-", "−"))
fig.text(x, y + 36, "Strain-8 scan–rescan, 20 volunteers", SM, 700)
fig.kv_table(x, y + 54, [("global", "fair–excellent"), ("segmental", "more variable")], w=CW - 4, row_h=15)

# ---- 4 tissue (LGE) ---------------------------------------------------------------------------------------
x = column(3, "Tissue (LGE)", "Kihlberg 2020", "scar-associated dysfunction", "motion error", "segments with LGE > 50%",
           "116 suspected CAD, 34 with qualifying scar. Ranks scar sensitivity, not motion accuracy.")
fig.text(x, CH_Y + 8, "AUC", SM, fill=C.MUTED)
y = bar_rows(x, CH_Y + 12, [("DENSE", 0.87, C.DEEP, "0.87"), ("tagging", 0.83, C.AGAR, "0.83"), ("cine FT", 0.66, C.OBS, "0.66")])
fig.text(x, y + 14, "sensitivity at 80% specificity", SM, fill=C.MUTED)
y = bar_rows(x, y + 18, [("DENSE", 0.82, C.DEEP, "82%"), ("tagging", 0.71, C.AGAR, "71%"), ("cine FT", 0.35, C.OBS, "35%")],
             ticks=[0, 0.5, 1])

# ---- 5 outcome & readers ------------------------------------------------------------------------------------
x = column(4, "Outcome & readers", "Bello 2019; Masutani 2023", "prognostic / diagnostic link", "clinical utility",
           "discrimination, chance 0.5",
           "Masutani: 53 patients, 846 segments, 30% peak Err cut-off. C-index and AUC are not comparable.")
fig.text(x, CH_Y + 8, "Bello · cine DL motion, survival", SM, fill=C.MUTED)
fig.text(x, CH_Y + 21, "C-index, n = 302 (○ human)", SM, fill=C.MUTED)
y = value_rows(x, CH_Y + 25, [("DL", 0.75, 0.75, C.SUP, 0.59, "0.75 vs 0.59")], (0.4, 1))
fig.text(x, y + 14, "Masutani · DL strain, WMA vs", SM, fill=C.MUTED)
fig.text(x, y + 27, "4-reader consensus, AUC", SM, fill=C.MUTED)
y = value_rows(x, y + 31, [("DL", 0.90, 0.90, C.SUP, None, "0.90")], (0.4, 1), [0.5, 0.75, 1], xlabel="C-index · AUC",
               fmt=lambda v: f"{v:g}")

export(fig, "Figure_1_two_track_evidence_map")

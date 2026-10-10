"""Figure 1 (journal variant): two-track evidence map for regional strain from routine cine CMR.

agarwood-scifig house style, journal variant: 800 px = 190 mm, smallest text 10.5 px (7 pt), white canvas,
thin rules, no gradients or image mock-ups. Panel a is a conceptual schematic (readouts computed from the
drawn curves); panel b transcribes values reported in the cited studies as given in the manuscript's
Tables 2–3, §4 and §6.6, and does not pool them. The poster variant of this figure is
src/Figure_1_two_track_poster.svg (1800 px canvas).
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
from scifig_common import C, T, export, start, tw, wrap  # noqa: E402
from scifig import CMAP_STRAIN, Rng, annulus_path, cmap, gauss, polyline, wedge_path  # noqa: E402

H = 722
fig = start(H, "Figure 1 | Two-track evidence map for regional strain from routine cine CMR",
            legend=[("observed", C.OBS), ("inferred", C.INF), ("reference", C.REF)],
            footer=["a: conceptual schematic, readouts computed from the drawn curves. b: values as reported in the cited "
                    "studies (manuscript Tables 2–3, §4, §6.6); not pooled.",
                    "ED/ES, end-diastole/-systole; FT, feature tracking; GL, Green–Lagrange; LoA, limits of agreement; "
                    "PSS, post-systolic shortening; WMA, wall-motion abnormality."])

X0, X1 = 20, 780
SM = T.SMALL          # 10.5 px = 7.06 pt
BODY = 12.0


def f2(x):
    return f"{x:.2f}".replace("-", "−")


def annulus(cx, cy, R, r):
    fig.path(annulus_path(cx, cy, R, r), fill=C.SILK, extra='fill-rule="evenodd"')
    fig.circle(cx, cy, R, stroke=C.OBS, w=1.1)
    fig.circle(cx, cy, r, stroke=C.OBS, w=1.1)


def badge_letter(x, y, s, color=C.INK):
    fig.circle(x, y, 7, color)
    fig.text(x, y + 3.8, s, 10.5, 700, C.WHITE, "middle")


# =============================================================== a: estimation track
fig.panel(X0, 24, "a", "Estimation track: cine supplies cues; correspondence is inferred; strain is defined by convention")
TAG_Y, TITLE_Y, GY = 48, 64, 76          # tag line, station title, graphic top
CAP_Y = 196
stations = [X0, 164, 372, 580]           # station left edges
cols = [136, 200, 200, 200]


def station(i, tag, color, title, caption):
    x = stations[i]
    fig.stage_tag(x, TAG_Y, tag, color)
    fig.text(x, TITLE_Y, title, BODY, 700)
    for k, s in enumerate(wrap(caption, cols[i] - 10, SM)):
        fig.text(x, CAP_Y + k * 13, s, SM, fill=C.MUTED)
    if i:
        fig.col_rule(x - 8, 40, 236)


# ---- 1 image formation ---------------------------------------------------------------------
station(0, "1 · OBSERVED", C.OBS, "Cine bSSFP, short axis",
        "borders conspicuous; intramural texture weak; no material label")
rng = Rng(5)
for k, (cx, lab) in enumerate(((X0 + 30, "ED"), (X0 + 96, "ES"))):
    R, r = (29, 17) if k == 0 else (29, 12)
    annulus(cx, GY + 40, R, r)
    for _ in range(180):
        px, py = (rng() * 2 - 1) * R, (rng() * 2 - 1) * R
        if r + 1.5 < math.hypot(px, py) < R - 1.5:
            fig.circle(cx + px, GY + 40 + py, 0.7, C.OBS, extra='opacity="0.7"')
    fig.text(cx, GY + 40 + R + 14, lab, SM, 700, anchor="middle")
fig.arrow(X0 + 61, GY + 40, X0 + 65, GY + 40, C.MUTED, 1.0, 5)
badge_letter(X0 + 124, TAG_Y - 4, "I")

# ---- 2–3 correspondence --------------------------------------------------------------------
station(1, "2–3 · INFERRED", C.INF, "Estimated displacement u(X, t)",
        "identical masks admit different material maps; the prior selects among them (Fig. 2)")
x = stations[1]
cx, cy, R, r = x + 32, GY + 40, 30, 17
annulus(cx, cy, R, r)
for rad, n, off in ((22.5, 9, 0.2), (28.5, 13, 0.0)):
    for i in range(n):
        th = 2 * math.pi * i / n + off
        x0, y0 = cx + rad * math.cos(th), cy + rad * math.sin(th)
        dx = -4.0 * math.cos(th) - 1.8 * math.sin(th)
        dy = -4.0 * math.sin(th) + 1.8 * math.cos(th)
        fig.arrow(x0, y0, x0 + dx, y0 + dy, C.INF, 0.9, 2.6)
fx = x + 72
fig.rich(x, GY + 96, [("φ̂", 400, C.INK, True), (" = arg min ", 400, C.INK, False), ("D", 400, C.INK, True),
                       ("(", 400, C.INK, False), ("I", 400, C.INK, True), ("0", 400, C.INK, False, "sub"),
                       (", ", 400, C.INK, False), ("I", 400, C.INK, True), ("t", 400, C.INK, True, "sub"),
                       (" ∘ ", 400, C.INK, False), ("φ", 400, C.INK, True), (") + ", 400, C.INK, False),
                       ("α", 700, C.INF, True), ("R", 700, C.INF, True), ("(", 400, C.INK, False),
                       ("φ", 400, C.INK, True), (")", 400, C.INK, False)], BODY)
fig.text(fx, GY + 22, "the data term D does not", SM, fill=C.MUTED)
fig.text(fx, GY + 35, "identify the map;", SM, fill=C.MUTED)
fig.text(fx, GY + 48, "the prior αR selects:", SM, fill=C.MUTED)
fig.text(fx, GY + 63, "tracking · registration ·", SM)
fig.text(fx, GY + 76, "biomechanics · learned", SM)
badge_letter(x + 152, TAG_Y - 4, "E")
badge_letter(x + 170, TAG_Y - 4, "R")

# ---- 4 strain definition ---------------------------------------------------------------------
station(2, "4 · DEFINED", C.REF, "Green–Lagrange Ecc, pixelwise",
        "choices 01–05 fix the value before any region is reported")
x = stations[2]
cx, cy = x + 42, GY + 40
segs = [-0.18, -0.19, -0.17, -0.08, -0.20, -0.18]       # mid-ventricular segments 7–12; segment 11 reduced
for i, v in enumerate(segs):
    a0 = -math.pi / 2 + i * math.pi / 3
    fig.path(wedge_path(cx, cy, 16, 30, a0, a0 + math.pi / 3), C.WHITE, 1.0, fill=cmap(CMAP_STRAIN, v))
    am = a0 + math.pi / 6
    fig.text(cx + 38 * math.cos(am), cy + 38 * math.sin(am) + 3.5, str(7 + i), SM, fill=C.MUTED, anchor="middle")
fig.circle(cx, cy, 16, C.WHITE, C.OBS, 0.8)
fig.circle(cx, cy, 30, "none", C.OBS, 0.8)
specs = [("01", "ED reference"), ("02", "E = ½(FᵀF − I)"), ("03", "c/r/l axes, signed"),
         ("04", "endo·mid·epi, 2D"), ("05", "∂u/∂X, smoothed")]
for k, (a, b) in enumerate(specs):
    yy = GY + 12 + k * 15
    fig.text(x + 92, yy, a, SM, fill=C.MUTED)
    fig.text(x + 108, yy, b, SM)
fig.text(x + 42, cy + 50, "fill = Ecc; seg 11 reduced", SM, fill=C.MUTED, anchor="middle")

# ---- 5 regional report -------------------------------------------------------------------------
station(3, "5 · REPORTED", C.REF, "Segmental Ecc(t), mid ventricle",
        "choices 06–08 pick one number from the same curves (○ segment 11)")
x = stations[3]
ts = [i / 200 for i in range(201)]
w = 1 / math.sqrt(2)
curves = [[-0.19 * gauss(t, 0.40, 0.13 * w) for t in ts], [-0.20 * gauss(t, 0.42, 0.13 * w) for t in ts],
          [-0.18 * gauss(t, 0.39, 0.12 * w) for t in ts], [-0.21 * gauss(t, 0.41, 0.14 * w) for t in ts],
          [-0.17 * gauss(t, 0.38, 0.12 * w) for t in ts]]
seg11 = [-0.08 * gauss(t, 0.26, 0.10 * w) - 0.12 * gauss(t, 0.58, 0.09 * w) for t in ts]
T_ES = 0.40
ax = fig.axes(x + 24, GY + 2, 62, 72, (0, 1), (-0.25, 0.02), [0, 0.5, 1], [-0.2, -0.1, 0], "", "",
              xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:.1f}".replace("-", "−") if v else "0")
fig.text(x + 55, GY + 2 + 72 + 27, "cycle time", SM, anchor="middle")
ax.vline(T_ES, C.MUTED, 0.8)
fig.text(ax.fx(T_ES) + 3, GY + 9, "ES", SM, fill=C.MUTED)
for cv in curves:
    ax.line(ts, cv, C.OBS, 1.0)
ax.line(ts, seg11, C.INF, 1.8)
k_es = min(range(len(ts)), key=lambda i: abs(ts[i] - T_ES))
i_sys = min(range(len(ts)), key=lambda i: seg11[i] if ts[i] <= T_ES else 0)
i_all = min(range(len(ts)), key=lambda i: seg11[i])
for i in (k_es, i_sys, i_all):
    fig.circle(ax.fx(ts[i]), ax.fy(seg11[i]), 2.8, C.WHITE, C.INF, 1.2)
allc = curves + [seg11]
mean = [sum(cv[i] for cv in allc) / len(allc) for i in range(len(ts))]
reads = [("06", "AHA mid 7–12", ""), ("07", "at ES", f2(seg11[k_es])), ("", "peak sys.", f2(seg11[i_sys])),
         ("", "post-sys.", f2(seg11[i_all])), ("08", "min(mean)", f2(min(mean))),
         ("", "mean(min)", f2(sum(min(cv) for cv in allc) / len(allc)))]
for k, (n_, a, b) in enumerate(reads):
    yy = GY + 12 + k * 14
    fig.text(x + 94, yy, n_, SM, fill=C.MUTED)
    fig.text(x + 110, yy, a, SM, fill=C.MUTED if b else C.INK)
    fig.text(x + 200, yy, b, SM, 700, anchor="end")

# ---- failure points -------------------------------------------------------------------------------
fy = 254
fig.line(X0, fy - 14, X1, fy - 14, C.GRID, 0.8)
fig.text(X0, fy + 4, "Failure points, each testable alone:", SM, 700)
items = [("I", "input sufficiency", "re-image the motion more finely"),
         ("E", "estimation", "vary α with images fixed"),
         ("R", "representation", "project the known field onto the basis")]
xx = X0 + 8
for let, name, test in items:
    badge_letter(xx, fy + 18, let)
    fig.rich(xx + 11, fy + 22, [(name, 700, C.INK, False), (" · " + test, 400, C.MUTED, False)], SM)
    xx += 11 + tw(name, SM, True) + tw(" · " + test, SM) + 22
if xx - 18 > X1:
    print(f"warning: failure-point row overflows by {xx - 18 - X1:.0f} px")

# =============================================================== b: validation track
fig.row_rule(294)
fig.panel(X0, 320, "b", "Validation track: each reference supports one claim; results as reported")
fig.legend_items(X0 + 2, 342, [("DENSE", "dot", C.DEEP), ("tagging", "dot", C.AGAR), ("cine FT", "dot", C.OBS),
                               ("cine DL", "dot", C.SUP), ("comparator", "open", C.OBS)], gap=16)
CW, GAP = 144, 10
TY, RY, OK_Y, CT_Y, CH_Y = 366, 379, 410, 468, 476        # title, refs, ✓ (✕ follows), chart title, chart top
CAP2_Y = 680


def column(i, title, refs, ok, no, chart_title, caption):
    x = X0 + i * (CW + GAP)
    if i:
        fig.col_rule(x - GAP / 2, 352, H - 4)
    fig.text(x, TY, title, BODY, 700)
    for k, s in enumerate(wrap(refs, CW - 4, SM)):
        fig.text(x, RY + k * 13, s, SM, fill=C.MUTED)
    oks = wrap(ok, CW - 20, SM)
    fig.check(x, OK_Y, oks[0], SM)
    for k, s_ in enumerate(oks[1:]):
        fig.text(x + 15, OK_Y + 13 * (k + 1), s_, SM)
    ny = OK_Y + 13 * len(oks) + 1
    nos = wrap(no, CW - 20, SM)
    fig.cross(x, ny, nos[0], SM)
    for k, s_ in enumerate(nos[1:]):
        fig.text(x + 15, ny + 13 * (k + 1), s_, SM, fill=C.MUTED)
    fig.text(x, CT_Y, chart_title, SM, 700)
    for k, s in enumerate(wrap(caption, CW - 4, SM)):
        fig.text(x, CAP2_Y + k * 13, s, SM, fill=C.MUTED)
    for s_, nm in ((title, "title"), (chart_title, "chart title")):
        wd = tw(s_, BODY if nm == "title" else SM, True)
        if wd > CW - 2:
            print(f"warning: column {i} {nm} too wide ({wd:.0f} px): {s_}")
    return x


def dot_rows(x, y, rows, xlim, ticks, w=92, label_w=46, row_h=20, xlabel="", fmt=None):
    """Compact rows: muted label left, range bar or dot, comparator ○, bold value above the mark."""
    fmt = fmt or (lambda v: f"{v:g}")
    ax0 = x + label_w
    n = len(rows)
    for t in ticks:
        px = ax0 + (t - xlim[0]) / (xlim[1] - xlim[0]) * w
        fig.line(px, y, px, y + n * row_h, C.GRID, 0.8)
    for i, (lab, lo, hi, col, comp, vt) in enumerate(rows):
        yy = y + row_h / 2 + i * row_h + 3
        fx = lambda v: ax0 + (v - xlim[0]) / (xlim[1] - xlim[0]) * w
        fig.text(ax0 - 6, yy + 3.5, lab, SM, anchor="end")
        if comp is not None:
            fig.line(fx(comp) + 3.5, yy, fx(lo) - 3.5, yy, C.GRID, 1)
            fig.circle(fx(comp), yy, 3.4, C.WHITE, col, 1.3)
        if hi > lo:
            fig.line(fx(lo), yy, fx(hi), yy, col, 4.5, 'stroke-linecap="round"')
        else:
            fig.circle(fx(lo), yy, 3.4, col)
        label = vt if vt is not None else (f"{fmt(lo)}–{fmt(hi)}" if hi > lo else fmt(lo))
        xm = (fx(lo) + fx(hi)) / 2
        anchor = "middle"
        if xm > ax0 + w - 22:
            xm, anchor = ax0 + w, "end"
        elif xm < ax0 + 22:
            xm, anchor = ax0, "start"
        fig.text(xm, yy - 6, label, SM, 700, anchor=anchor)
    fig.axes(ax0, y + n * row_h, w, 0, xlim, (0, 1), ticks, (), xlabel, xfmt=fmt, yaxis=False)
    return y + n * row_h


def hbar_rows(x, y, rows, xlim, ticks, w=76, label_w=42, row_h=17, xlabel="", fmt=None):
    fmt = fmt or (lambda v: f"{v:g}")
    ax0 = x + label_w
    n = len(rows)
    fx = lambda v: ax0 + (v - xlim[0]) / (xlim[1] - xlim[0]) * w
    for t in ticks:
        fig.line(fx(t), y, fx(t), y + n * row_h, C.GRID, 0.8)
    for i, (lab, v, col, vt) in enumerate(rows):
        yy = y + i * row_h + row_h / 2
        fig.text(ax0 - 6, yy + 3.5, lab, SM, anchor="end")
        fig.rect(fx(0), yy - 5, fx(v) - fx(0), 10, col, rx=1)
        fig.text(fx(v) + 4, yy + 3.5, vt, SM, 700)
    fig.axes(ax0, y + n * row_h, w, 0, xlim, (0, 1), ticks, (), xlabel, xfmt=fmt, yaxis=False)
    return y + n * row_h


# ---- 1 known motion --------------------------------------------------------------------------------
x = column(0, "Known motion", "MRXCAT2.0 test of DeepStrain", "capacity, technical error", "not alone: in-vivo accuracy",
           "estimator error (mean ± SD)", "Also Dice 0.82; displacement 1.0 ± 0.9 mm. Slice means only: no scar-region error.")
rows = [("Ecc, 4 cases", 0.02, 0.04, C.OBS, False), ("Err, 4 cases", -0.24, 0.21, C.INF, False),
        ("Err, infarct", -0.20, 0.21, C.INF, True)]
ax0, w = x + 60, 78
fx = lambda v: ax0 + (v + 0.5) / 0.62 * w
for t in (-0.4, -0.2, 0):
    fig.line(fx(t), CH_Y, fx(t), CH_Y + 3 * 34, C.GRID, 0.8)
fig.line(fx(0), CH_Y, fx(0), CH_Y + 3 * 34, C.INK, 1, 'stroke-dasharray="3 2"')
for i, (lab, m, sd, col, op) in enumerate(rows):
    yy = CH_Y + 20 + i * 34
    fig.text(ax0 - 6, yy + 3.5, lab, SM, anchor="end")
    fig.line(fx(m - sd), yy, fx(m + sd), yy, col, 1.6)
    fig.circle(fx(m), yy, 3.4, C.WHITE if op else col, col, 1.3)
    if fx(m) > ax0 + w - 30:
        fig.text(fx(m - sd) - 5, yy + 3.5, f"{f2(m)} ± {f2(sd)}", SM, 700, anchor="end")
    else:
        fig.text(fx(m), yy - 7, f"{f2(m)} ± {f2(sd)}", SM, 700, anchor="middle")
fig.axes(ax0, CH_Y + 3 * 34, w, 0, (-0.5, 0.12), (0, 1), [-0.4, -0.2, 0], (), "strain error",
         xfmt=lambda v: f"{v:.1f}".replace("-", "−") if v else "0", yaxis=False)
fig.text(x, CH_Y + 3 * 34 + 50, "○ infarct case, EF 49%;", SM, fill=C.MUTED)
fig.text(x, CH_Y + 3 * 34 + 63, "prescribed scar Err", SM, fill=C.MUTED)
fig.text(x, CH_Y + 3 * 34 + 76, "0.95 → 0.30 (Fig. 4)", SM, fill=C.MUTED)

# ---- 2 paired DENSE / tagging -----------------------------------------------------------------------
x = column(1, "Paired DENSE / tagging", "Militaru 2021; Cao 2018; Wang 2023", "material-sensitive agreement",
           "not alone: reference error", "ICC; range = 3 vendors",
           "Militaru n = 61, 3 T; Cao, DENSE vs tagging; StrainNet (DL), 59 cine tests, DENSE reference.")
fig.text(x, CH_Y + 8, "cine FT vs tagging, global", SM, fill=C.MUTED)
y = dot_rows(x, CH_Y + 12, [("LS", 0.92, 0.94, C.OBS, None, "0.92–0.94"), ("CS", 0.88, 0.91, C.OBS, None, "0.88–0.91"),
                             ("RS", 0.10, 0.81, C.OBS, None, "0.10–0.81")], (0, 1), [], w=92, label_w=46, row_h=19)
fig.text(x, y + 12, "DENSE vs tagging, Ecc", SM, fill=C.MUTED)
y = dot_rows(x, y + 16, [("Cao", 0.778, 0.778, C.DEEP, None, "0.778")], (0, 1), [], w=92, label_w=46, row_h=19)
fig.text(x, y + 12, "StrainNet (●) vs FT (○), Ecc", SM, fill=C.MUTED)
y = dot_rows(x, y + 16, [("global", 0.87, 0.87, C.SUP, 0.72, "0.87 vs 0.72"), ("segment", 0.75, 0.75, C.SUP, 0.48, "0.75 vs 0.48")],
             (0, 1), [0, 0.5, 1], w=92, label_w=46, row_h=19, xlabel="ICC")

# ---- 3 precision & reconstruction -----------------------------------------------------------------------
x = column(2, "Precision", "Yoon 2023; Bell 2025", "precision at tested scale", "not alone: accuracy (bias)",
           "REGAIN vs GRAPPA", "Mean global differences near zero; radial limits widest (49 participants).")
fig.text(x, CH_Y + 8, "95% LoA, global FT strain", SM, fill=C.MUTED)
fig.line(x + 46 + 46, CH_Y + 12, x + 46 + 46, CH_Y + 12 + 63, C.INK, 1, 'stroke-dasharray="3 2"')
y = dot_rows(x, CH_Y + 12, [("radial", -7, 6, C.OBS, None, "−7 to 6"), ("circ.", -2, 3, C.OBS, None, "−2 to 3"),
                             ("long.", -3, 3, C.OBS, None, "−3 to 3")], (-8, 8), [-8, 0, 8], w=92, label_w=46, row_h=21,
             xlabel="% points", fmt=lambda v: f"{v:g}".replace("-", "−"))
fig.text(x, y + 52, "Strain-8 scan–rescan", SM, 700)
fig.text(x, y + 65, "same day, 20 volunteers × 8 protocols", SM, fill=C.MUTED)
fig.kv_table(x, y + 83, [("global", "fair–excellent"), ("segmental", "more variable")], w=CW - 6, row_h=15)

# ---- 4 tissue (LGE) ----------------------------------------------------------------------------------
x = column(3, "Tissue (LGE)", "Kihlberg 2020", "scar-associated dysfunction", "not alone: motion error",
           "segments with LGE > 50%", "116 suspected CAD, 34 with qualifying scar. Ranks scar sensitivity, not motion accuracy.")
fig.text(x, CH_Y + 8, "AUC", SM, fill=C.MUTED)
y = hbar_rows(x, CH_Y + 12, [("DENSE", 0.87, C.DEEP, "0.87"), ("tagging", 0.83, C.AGAR, "0.83"), ("cine FT", 0.66, C.OBS, "0.66")],
              (0, 1), [], w=72, label_w=44, row_h=17)
fig.text(x, y + 14, "sensitivity at 80% specificity", SM, fill=C.MUTED)
y = hbar_rows(x, y + 18, [("DENSE", 0.82, C.DEEP, "82%"), ("tagging", 0.71, C.AGAR, "71%"), ("cine FT", 0.35, C.OBS, "35%")],
              (0, 1), [0, 0.5, 1], w=72, label_w=44, row_h=17, xlabel="AUC · sensitivity")

# ---- 5 outcome & readers --------------------------------------------------------------------------------
x = column(4, "Outcome & readers", "Bello 2019; Masutani 2023", "prognostic / diagnostic link", "not alone: clinical utility",
           "discrimination, chance 0.5", "Masutani: 53 patients, 846 segments, 30% peak Err cut-off. C-index and AUC are not comparable.")
fig.text(x, CH_Y + 8, "Bello · cine DL motion,", SM, fill=C.MUTED)
fig.text(x, CH_Y + 21, "survival C-index, n = 302", SM, fill=C.MUTED)
y = dot_rows(x, CH_Y + 25, [("DL", 0.75, 0.75, C.SUP, 0.59, "0.75 vs 0.59")], (0.4, 1), [], w=92, label_w=46, row_h=23)
fig.text(x + 46, y + 14, "○ human benchmark", SM, fill=C.MUTED)
fig.text(x, y + 36, "Masutani · DL strain, WMA", SM, fill=C.MUTED)
fig.text(x, y + 49, "vs 4-reader consensus, AUC", SM, fill=C.MUTED)
y = dot_rows(x, y + 53, [("DL", 0.90, 0.90, C.SUP, None, "0.90")], (0.4, 1), [0.5, 0.75, 1], w=92, label_w=46, row_h=23,
             xlabel="C-index · AUC", fmt=lambda v: f"{v:g}")

export(fig, "Figure_1_two_track_evidence_map")

"""Supplementary Figure S2: attributes of regional error and mapping validity.

agarwood-scifig house style, 190 mm. Prescribed schematics. The estimate in every panel of a (and of b)
is tuned to the same root-mean-square error against its reference, so one error number cannot tell the
failures apart; det J values in c are computed from the drawn mappings. No study data.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
from scifig_common import C, T, export, start  # noqa: E402


def g(x, c, w):
    return np.exp(-((x - c) / w) ** 2)


def rmse(a, b):
    return float(np.sqrt(np.mean((a - b) ** 2)))


def solve(f, target, lo, hi):
    """Bisection for f(p) = target on a monotone bracket."""
    flo = f(lo) - target
    for _ in range(80):
        mid = (lo + hi) / 2
        if (f(mid) - target) * flo > 0:
            lo, flo = mid, f(mid) - target
        else:
            hi = mid
    return (lo + hi) / 2


def f2(x):
    return f"{x:.2f}".replace("-", "−")


x = np.linspace(0, 1, 401)
ref = g(x, 0.40, 0.09)
k_mag = 0.5
R = rmse(ref, k_mag * ref)
SHIFT = solve(lambda d: rmse(ref, g(x, 0.40 + d, 0.09)), R, 0.0, 0.08)
a_ext = solve(lambda a: rmse(ref, a * g(x, 0.40, 0.19)), R, 0.25, 0.62)
b_sup = solve(lambda b: rmse(ref, ref + b * g(x, 0.82, 0.05)), R, 0.0, 2.0)


def fwhm(y):
    above = x[y >= y.max() / 2]
    return above.max() - above.min()


spatial = [
    ("Magnitude", k_mag * ref, f"peak 1.00 → {f2(k_mag)}"),
    ("Location", g(x, 0.40 + SHIFT, 0.09), f"centroid +{f2(SHIFT)} of the wall"),
    ("Extent", a_ext * g(x, 0.40, 0.19), f"FWHM {f2(fwhm(ref))} → {f2(fwhm(a_ext * g(x, 0.40, 0.19)))}"),
    ("Support", ref + b_sup * g(x, 0.82, 0.05), f"extra peak {f2(b_sup)} off the support"),
]
t = np.linspace(0, 1, 401)
rc = -g(t, 0.36, 0.13)
k_t = 0.6
Rt = rmse(rc, k_t * rc)
TSHIFT = solve(lambda d: rmse(rc, -g(t, 0.36 + d, 0.13)), Rt, 0.0, 0.12)
temporal = [("Magnitude", k_t * rc, f"peak −1.00 → {f2(-k_t)}"),
            ("Timing", -g(t, 0.36 + TSHIFT, 0.13), f"peak time +{f2(TSHIFT)} cycle")]

H = 478
fig = start(H, "Figure S2 | Different regional failures can share one error value",
            footer=["Prescribed schematics: estimates in a (and in b) are set to the same RMSE against the reference; "
                    "det J computed from the drawn maps.",
                    "RMSE, root-mean-square error; FWHM, full width at half maximum; det J, Jacobian determinant."])

# ---- a: spatial attributes -------------------------------------------------------------------------
fig.panel(20, 24, "a", f"Four spatial failures, one RMSE ({f2(R)})")
fig.legend_items(560, 22, [("reference", "line", C.REF), ("estimate", "dash", C.INF)], gap=20)
PW, GAP = 172, 24
for k, (name, est, readout) in enumerate(spatial):
    px = 20 + k * (PW + GAP)
    fig.text(px, 58, name, T.SUB - 1, 700)
    ax = fig.axes(px, 68, PW, 78, (0, 1), (-0.04, 1.12), (), ())
    if name == "Support":
        x0, x1 = x[ref > 0.2].min(), x[ref > 0.2].max()
        fig.rect(ax.fx(x0), 68, ax.fx(x1) - ax.fx(x0), 78, C.REF_T)
    ax.line(x, ref, C.REF, 1.8)
    ax.line(x, est, C.INF, 1.8, dash="5 3")
    if name == "Magnitude":
        fig.arrow(ax.fx(0.53), ax.fy(1.0), ax.fx(0.53), ax.fy(k_mag), C.INK, 1.0, 4)
        fig.line(ax.fx(0.43), ax.fy(1.0), ax.fx(0.56), ax.fy(1.0), C.INK, 0.7, 'stroke-dasharray="2 2"')
        fig.text(ax.fx(0.57), ax.fy((1 + k_mag) / 2) + 4, "ΔM", T.SMALL, 700, italic=True)
    elif name == "Location":
        fig.arrow(ax.fx(0.40), ax.fy(1.08), ax.fx(0.40 + SHIFT), ax.fy(1.08), C.INK, 1.0, 4)
        fig.text(ax.fx(0.53), ax.fy(1.08) + 4, "Δθ", T.SMALL, 700, italic=True)
    elif name == "Extent":
        for y, half, col in ((0.5, fwhm(ref) / 2, C.REF), (a_ext / 2, fwhm(est) / 2, C.INF)):
            fig.line(ax.fx(0.40 - half), ax.fy(y), ax.fx(0.40 + half), ax.fy(y), col, 1.0)
        fig.text(ax.fx(0.62), ax.fy(0.42) + 4, "Δw", T.SMALL, 700, italic=True)
    fig.text(px, 164, readout, T.SMALL)
    fig.text(px, 178, f"RMSE {f2(rmse(ref, est))}", T.SMALL, 700, fill=C.INK)
fig.text(780, 196, "position around the wall →", T.SMALL, fill=C.MUTED, anchor="end")

# ---- b: temporal attributes --------------------------------------------------------------------------
fig.row_rule(206)
fig.panel(20, 232, "b", f"Temporal: same RMSE ({f2(Rt)})")
for k, (name, est, readout) in enumerate(temporal):
    px = 20 + k * (PW + GAP)
    fig.text(px, 266, name, T.SUB - 1, 700)
    ax = fig.axes(px, 276, PW, 92, (0, 1), (-1.12, 0.08), (), ())
    ax.hline(0, C.RULE, 0.8, None)
    ax.line(t, rc, C.REF, 1.8)
    ax.line(t, est, C.INF, 1.8, dash="5 3")
    if name == "Timing":
        fig.arrow(ax.fx(0.36), ax.fy(-1.06), ax.fx(0.36 + TSHIFT), ax.fy(-1.06), C.INK, 1.0, 4)
        fig.text(ax.fx(0.58), ax.fy(-0.92), "Δt", T.SMALL, 700, italic=True)
    else:
        fig.arrow(ax.fx(0.52), ax.fy(-1.0), ax.fx(0.52), ax.fy(-k_t), C.INK, 1.0, 4)
        fig.line(ax.fx(0.30), ax.fy(-1.0), ax.fx(0.55), ax.fy(-1.0), C.INK, 0.7, 'stroke-dasharray="2 2"')
        fig.text(ax.fx(0.56), ax.fy(-(1 + k_t) / 2) + 4, "ΔM", T.SMALL, 700, italic=True)
    fig.text(px, 386, readout, T.SMALL)
    fig.text(px, 400, f"RMSE {f2(rmse(rc, est))}", T.SMALL, 700)
fig.text(386 - 6 + 2, 420, "time →", T.SMALL, fill=C.MUTED, anchor="end")
fig.lines(20, 442, ["A single mean-squared error cannot say which attribute failed;",
                    "report bias, location, extent and timing error separately."], T.SMALL)


# ---- c: mapping validity ---------------------------------------------------------------------------
def smooth(X, Y):
    return X + 0.06 * np.sin(np.pi * Y) * np.sin(np.pi * X), Y + 0.04 * np.sin(2 * np.pi * X)


def folded(X, Y):
    return X + 0.30 * g(X, 0.5, 0.12) * g(Y, 0.5, 0.22), Y


def detj(fn, n=11, eps=1e-5):
    u = np.linspace(0, 1, n + 1)
    c = (u[:-1] + u[1:]) / 2
    X, Y = np.meshgrid(c, c, indexing="ij")
    x1, y1 = fn(X + eps, Y)
    x0, y0 = fn(X - eps, Y)
    x3, y3 = fn(X, Y + eps)
    x2, y2 = fn(X, Y - eps)
    return ((x1 - x0) * (y3 - y2) - (x3 - x2) * (y1 - y0)) / (4 * eps * eps), u


fig.col_rule(398, 214, H - 4)
fig.panel(410, 232, "c", "Invertible is necessary, not sufficient")
GS = 128
for k, (fn, name, cap) in enumerate([(smooth, "Invertible", "can still be wrong"),
                                     (folded, "Folded", "orientation reversed")]):
    gx, gy = 418 + k * (GS + 52), 254
    fig.text(gx, gy + 12, name, T.SUB - 1, 700)
    d, u = detj(fn)
    s = np.linspace(0, 1, 120)
    oy = gy + 22
    for cval in u:
        for X, Y in (fn(np.full_like(s, cval), s), fn(s, np.full_like(s, cval))):
            pts = " L".join(f"{gx + a * GS:.1f} {oy + GS - b * GS:.1f}" for a, b in zip(X, Y))
            fig.path("M" + pts, C.OBS, 0.7)
    bad = np.argwhere(d <= 0)
    for i, j in bad:
        corners = [(u[i], u[j]), (u[i + 1], u[j]), (u[i + 1], u[j + 1]), (u[i], u[j + 1])]
        pts = [fn(np.array([a]), np.array([b])) for a, b in corners]
        fig.path("M" + " L".join(f"{gx + float(X[0]) * GS:.1f} {oy + GS - float(Y[0]) * GS:.1f}" for X, Y in pts) + " Z",
                 C.ERR, 1.3)
    n_bad = len(bad)
    rows = [("min det J", f2(d.min())), ("cells det J ≤ 0", f"{n_bad} / {d.size}")]
    fig.kv_table(gx, oy + GS + 30, rows, w=GS, row_h=16)
    fig.text(gx, oy + GS + 64, cap, T.SMALL, fill=C.MUTED)

export(fig, "Figure_S2_error_attributes_mapping_validity")
print(f"R={R:.3f} k_mag={k_mag:.3f} a_ext={a_ext:.3f} b_sup={b_sup:.3f}; Rt={Rt:.3f} k_t={k_t:.3f}")

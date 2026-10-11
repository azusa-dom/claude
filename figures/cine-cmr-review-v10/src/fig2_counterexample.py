"""Figure 2: identical contours, different material correspondence (analytic counterexample).

agarwood-scifig house style, 190 mm. All values are analytic (a = 0.5); no study data.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
from scifig_common import C, T, export, start  # noqa: E402
from scifig import Rng, annulus_path, polyline  # noqa: E402

A = 0.5
H = 282

fig = start(H, "Figure 2 | Identical contours do not fix material correspondence",
            legend=[("observed", C.OBS), ("inferred", C.INF), ("reference", C.REF)],
            footer=["Analytic counterexample (a = 0.5); no study data. λθ is a stretch ratio, not Green–Lagrange strain.",
                    "Dice, Dice similarity coefficient; HD, Hausdorff distance; DENSE, displacement encoding with stimulated echoes."])


def annulus(cx, cy, R, r, fill=C.SILK, edge=C.OBS):
    fig.path(annulus_path(cx, cy, R, r), fill=fill, extra='fill-rule="evenodd"')
    fig.circle(cx, cy, R, stroke=edge, w=1.1)
    fig.circle(cx, cy, r, stroke=edge, w=1.1)


def clip(cx, cy, R, r):
    cid = fig.uid("clip")
    fig.defs(f'<clipPath id="{cid}"><path d="{annulus_path(cx, cy, R, r)}" fill-rule="evenodd"/></clipPath>')
    return f'clip-path="url(#{cid})"'


# ---- a: what each acquisition supplies ------------------------------------------------------
fig.panel(20, 26, "a", "Cine lacks a material label")
R, r, cy = 31, 17.5, 112
cols = [(58, "Routine cine", ["boundaries +", "weak texture"], False),
        (145, "Tagging", ["prepared grid", "(material pattern)"], True),
        (232, "DENSE", ["phase-encoded", "displacement"], True)]
rng = Rng(7)
for cx, name, cap, labelled in cols:
    fig.text(cx, 64, name, T.SUB - 1, 700, anchor="middle")
    annulus(cx, cy, R, r)
    for i, s in enumerate(cap):
        fig.text(cx, cy + R + 17 + i * 13, s, T.SMALL, fill=C.MUTED, anchor="middle")
    (fig.tick if labelled else fig.xmark)(cx, 196, C.SUP if labelled else C.INF)

cx = cols[0][0]
for _ in range(240):
    x, y = (rng() * 2 - 1) * R, (rng() * 2 - 1) * R
    rr = math.hypot(x, y)
    if r + 1.5 < rr < R - 1.5:
        fig.circle(cx + x, cy + y, 0.7, C.OBS, extra='opacity="0.75"')
cx = cols[1][0]
cl = clip(cx, cy, R, r)
fig.raw(f"<g {cl}>")
k = -R
while k <= R:
    fig.line(cx + k, cy - R, cx + k, cy + R, C.REF, 0.9)
    fig.line(cx - R, cy + k, cx + R, cy + k, C.REF, 0.9)
    k += 6.5
fig.raw("</g>")
cx = cols[2][0]
for rad, n, off in ((21.5, 10, 0.3), (27.5, 14, 0.0)):
    for i in range(n):
        th = 2 * math.pi * i / n + off
        x0, y0 = cx + rad * math.cos(th), cy + rad * math.sin(th)
        dx = -3.6 * math.cos(th) - 1.6 * math.sin(th)
        dy = -3.6 * math.sin(th) + 1.6 * math.cos(th)
        fig.arrow(x0, y0, x0 + dx, y0 + dy, C.REF, 0.9, 2.4)
fig.line(24, 183, 268, 183, C.GRID, 0.8)
fig.text(145, 216, "material label carried by the signal", T.SMALL, fill=C.MUTED, anchor="middle")
fig.lines(24, 242, ["Cine supplies boundaries and weak texture only;",
                    "correspondence inside the wall must be inferred."], T.SMALL)

# ---- b: two mappings, identical contours ----------------------------------------------------
fig.col_rule(286, 6, H - 4)
fig.panel(298, 26, "b", "Same masks, two material maps")
R2, r2, cy2 = 43, 24, 128
th8 = [2 * math.pi * i / 8 for i in range(8)]
maps = [(362, "Mapping 1", "θ ↦ θ", th8, C.OBS),
        (502, "Mapping 2", "θ ↦ θ + a sin θ", [t + A * math.sin(t) for t in th8], C.INF)]
for cx, name, eq, mapped, col in maps:
    fig.text(cx, 62, name, T.SUB - 1, 700, anchor="middle")
    fig.text(cx, 77, eq, T.BODY - 0.5, anchor="middle", italic=True)
    annulus(cx, cy2, R2, r2)
    if col == C.INF:
        for t in th8:
            fig.line(cx + r2 * math.cos(t), cy2 + r2 * math.sin(t), cx + R2 * math.cos(t), cy2 + R2 * math.sin(t),
                     C.RULE, 0.9, 'stroke-dasharray="2 1.6"')
        for t0, t1 in zip(th8, mapped):
            if abs(t1 - t0) > 0.08:
                ts = [t0 + (t1 - t0) * i / 20 for i in range(21)]
                pts = [(cx + (R2 + 6) * math.cos(t), cy2 + (R2 + 6) * math.sin(t)) for t in ts]
                fig.path(polyline(pts), C.INF, 1.0)
                a = ts[-1]
                tip = pts[-1]
                d = 1 if t1 > t0 else -1
                tx, ty = -math.sin(a) * d, math.cos(a) * d
                nx, ny = math.cos(a), math.sin(a)
                fig.path(f"M{tip[0] - 4.5 * tx + 2.4 * nx:.1f} {tip[1] - 4.5 * ty + 2.4 * ny:.1f} L{tip[0]:.1f} {tip[1]:.1f} "
                         f"L{tip[0] - 4.5 * tx - 2.4 * nx:.1f} {tip[1] - 4.5 * ty - 2.4 * ny:.1f}", C.INF, 1.0,
                         extra='stroke-linecap="round" stroke-linejoin="round"')
    for t in mapped:
        fig.line(cx + r2 * math.cos(t), cy2 + r2 * math.sin(t), cx + R2 * math.cos(t), cy2 + R2 * math.sin(t), col, 1.8)
        rm = (r2 + R2) / 2
        fig.circle(cx + rm * math.cos(t), cy2 + rm * math.sin(t), 3.2, col, C.WHITE, 0.8)
fig.text(432, cy2 - 3, "identical", T.SMALL, fill=C.MUTED, anchor="middle")
fig.text(432, cy2 + 10, "masks", T.SMALL, fill=C.MUTED, anchor="middle")
fig.line(302, 192, 566, 192, C.GRID, 0.8)
fig.rich(432, 212, [("Dice = 1 · HD = 0 · ", 700, C.INK, False), ("r", 400, C.INK, True), (" ↦ ", 400, C.INK, False),
                    ("r", 400, C.INK, True), (" · ", 400, C.INK, False), ("a", 400, C.INK, True),
                    (" = 0.5", 400, C.INK, False)], T.SMALL + 0.5, anchor="middle")
fig.legend_items(330, 238, [("reference position", "line", C.RULE), ("mapped point", "dot", C.INF)], gap=22)
fig.text(432, 262, "Same eight material points in both annuli.", T.SMALL, fill=C.MUTED, anchor="middle")

# ---- c: resulting stretch ---------------------------------------------------------------------
fig.col_rule(580, 6, H - 4)
fig.panel(592, 26, "c", "Stretch differs by ±50%")
TWO_PI = 2 * math.pi
ax = fig.axes(640, 50, 136, 108, (0, TWO_PI), (0.3, 1.7), [0, math.pi, TWO_PI], [0.5, 1, 1.5],
              xfmt=lambda v: {0: "0", 1: "π", 2: "2π"}[round(v / math.pi)], yfmt=lambda v: f"{v:.1f}")
fig.raw(f'<text transform="translate({640 - 34:.1f},{104:.1f}) rotate(-90)" font-size="{T.LABEL + 0.5}" '
        f'text-anchor="middle" fill="{C.INK}"><tspan font-style="italic">λ</tspan><tspan font-style="italic" '
        f'baseline-shift="sub" font-size="{(T.LABEL + 0.5) * 0.8:.1f}">θ</tspan></text>')
fig.text(640 + 68, 50 + 108 + 29, "θ", T.LABEL + 0.5, anchor="middle", italic=True)
xs = [TWO_PI * i / 200 for i in range(201)]
ax.line(xs, [1.0] * len(xs), C.OBS, 1.8)
ax.line(xs, [1 + A * math.cos(t) for t in xs], C.INF, 1.8)
for xv, yv, lab, dy in ((0, 1.5, "1.5", -7), (math.pi, 0.5, "0.5", 4), (TWO_PI, 1.5, "1.5", -7)):
    fig.circle(ax.fx(xv), ax.fy(yv), 3.2, C.INF, C.WHITE, 0.8)
    fig.text(ax.fx(xv) + (6 if xv < TWO_PI else -6), ax.fy(yv) + dy, lab, T.SMALL, 700,
             anchor="end" if xv == TWO_PI else "start")
fig.text(ax.fx(math.pi), ax.fy(1.0) - 6, "map 1 · 1.0", T.SMALL, anchor="middle", fill=C.MUTED)
fig.text(ax.fx(math.pi) - 8, ax.fy(0.5) + 4, "map 2", T.SMALL, anchor="end", fill=C.MUTED)
fig.rich(596, 216, [("λ", 400, C.INK, True), ("θ", 400, C.INK, True, "sub"), (" = 1 + ", 400, C.INK, False),
                    ("a", 400, C.INK, True), (" cos θ", 400, C.INK, True)], T.BODY)
fig.kv_table(596, 240, [("range, map 2", "0.5–1.5"), ("mean over θ, both maps", "1.0"),
                        ("orientation preserved for", "|a| < 1")], w=184, row_h=16)

export(fig, "Figure_2_same_contours_analytic")

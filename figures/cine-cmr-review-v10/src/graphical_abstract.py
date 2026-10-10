"""Graphical abstract, agarwood-scifig house style: 1300 × 500 canvas → 2600 × 1000 px (260 × 100 mm at 254 dpi).

Counts (14 and 1 of 48 entries) come from data/table_s3_methods.csv, as in Figure 3; the attribute glyphs are schematic.
"""
import csv
import math
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
from scifig_common import C, export, start  # noqa: E402
from scifig import Rng, annulus_path, gauss  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "data" / "table_s3_methods.csv").open(newline="") as f:
    rows = list(csv.DictReader(f))
cnt = Counter(r["evidence"] for r in rows)
N = len(rows)

H = 500
fig = start(H, "", width=1300, width_mm=260, margin=30)
S = 1.0
TITLE, BODY, SMALL, HEAD = 25, 17, 15, 19

fig.text(30, 42, "Routine cine supports bounded regional strain claims;", TITLE, 700)
fig.text(30, 72, "whether a focal deficit is recovered must be tested attribute by attribute", TITLE, 700, fill=C.MUTED)
fig.line(30, 90, 1270, 90, C.INK, 1.4)


def tag(x, y, label, color):
    fig.circle(x + 6, y - 6, 6, color)
    fig.text(x + 18, y, label, 15, 700, color, extra='letter-spacing="1.6"')


# ---- observed --------------------------------------------------------------------------------
tag(30, 128, "OBSERVED", C.OBS)
cx, cy, R, r = 150, 262, 86, 48
fig.path(annulus_path(cx, cy, R, r), fill=C.SILK, extra='fill-rule="evenodd"')
fig.circle(cx, cy, R, stroke=C.OBS, w=2)
fig.circle(cx, cy, r, stroke=C.OBS, w=2)
rng = Rng(11)
for _ in range(420):
    x, y = (rng() * 2 - 1) * R, (rng() * 2 - 1) * R
    if r + 3 < math.hypot(x, y) < R - 3:
        fig.circle(cx + x, cy + y, 1.1, C.OBS, extra='opacity="0.7"')
fig.text(cx, 388, "Routine cine CMR", HEAD, 700, anchor="middle")
fig.text(cx, 412, "boundaries · weak texture · time", SMALL, fill=C.MUTED, anchor="middle")
fig.text(cx, 434, "no material label", SMALL, fill=C.MUTED, anchor="middle")
fig.arrow(256, 262, 312, 262, C.INK, 2, 10)
fig.col_rule(300, 106, 470)

# ---- inferred chain -----------------------------------------------------------------------------
tag(330, 128, "INFERRED", C.INF)
st = [(425, "Estimator + prior"), (615, "Material"), (800, "Regional strain")]
subs = ["registration, flow, learned", "correspondence u(X, t)", "Ecc, Err, Ell per segment"]
for i, ((x, name), sub) in enumerate(zip(st, subs)):
    fig.circle(x, 166, 9, C.INF)
    fig.text(x, 200, name, HEAD, 700, anchor="middle")
    fig.text(x, 222, sub, SMALL, fill=C.MUTED, anchor="middle")
    if i < 2:
        fig.arrow(x + 16, 166, st[i + 1][0] - 16, 166, C.MUTED, 1.6, 8)
        fig.verb((x + st[i + 1][0]) / 2, 156, ["track", "differentiate"][i], SMALL)
fig.text(360, 266, "Attributes of a focal deficit, each with its own error", BODY, 700)
glyphs = [("magnitude", "ΔM"), ("location", "Δθ"), ("extent", "Δw"), ("timing", "Δt")]
for k, (name, sym) in enumerate(glyphs):
    gx, gy, gw, gh = 360 + k * 128, 288, 104, 62
    fig.line(gx, gy + gh, gx + gw, gy + gh, C.RULE, 1)
    xs = [i / 60 for i in range(61)]
    ref = [gauss(t, 0.45, 0.12) for t in xs]
    est = {"magnitude": [0.55 * v for v in ref], "location": [gauss(t, 0.62, 0.12) for t in xs],
           "extent": [0.6 * gauss(t, 0.45, 0.22) for t in xs], "timing": [gauss(t, 0.62, 0.12) for t in xs]}[name]
    if name == "timing":
        ref = [1 - v for v in ref]
        est = [1 - v for v in est]
    for ys, col, dash in ((ref, C.REF, ""), (est, C.INF, 'stroke-dasharray="6 4"')):
        fig.path("M" + " L".join(f"{gx + t * gw:.1f} {gy + gh - 2 - v * (gh - 8):.1f}" for t, v in zip(xs, ys)),
                 col, 2.2, extra=dash)
    fig.text(gx, gy + gh + 22, name, SMALL)
    fig.text(gx + gw, gy + gh + 22, sym, SMALL, 700, anchor="end", italic=True)
fig.line(360, 404, 386, 404, C.REF, 2.2)
fig.text(394, 410, "reference", SMALL, fill=C.MUTED)
fig.line(490, 404, 516, 404, C.INF, 2.2, 'stroke-dasharray="6 4"')
fig.text(524, 410, "estimate (schematic)", SMALL, fill=C.MUTED)
fig.text(360, 440, "tested per attribute, per estimator, per acquisition", BODY, fill=C.INK)
fig.col_rule(892, 106, 470)

# ---- validation ---------------------------------------------------------------------------------
tag(920, 128, "VALIDATED BY", C.REF)
tiers = [("Known motion", "phantom, simulation"), ("Paired DENSE / tagging", "same session"),
         ("Tissue & outcome", "LGE, events")]
for i, (t, sub) in enumerate(tiers):
    y = 168 + i * 30
    fig.circle(926, y - 6, 6, C.REF)
    fig.text(942, y, t, BODY, 700)
    fig.text(1270, y, sub, SMALL, fill=C.MUTED, anchor="end")
fig.line(920, 252, 1270, 252, C.GRID, 1)
mat = cnt["material"]
foc = cnt["focal"]
fig.text(920, 274, f"Reviewed estimator entries (Table S3, n = {N})", SMALL, fill=C.MUTED)
for i, (n, lab) in enumerate(((mat, "material-sensitive reference"), (foc, "prescribed focal deficit"))):
    y = 306 + i * 26
    fig.text(970, y, f"{n}", 24, 700, anchor="end")
    fig.text(980, y - 1, lab, BODY)
fig.line(920, 346, 1270, 346, C.GRID, 1)
fig.check(920, 374, "Supported: whole-slice, global and", BODY)
fig.text(935, 396, "segmental Ecc under matched definitions", BODY)
fig.cross(920, 428, "Weaker: radial strain; focal boundary,", BODY)
fig.text(935, 450, "extent and timing, rarely tested", BODY, fill=C.MUTED)
fig.text(1270, 486, "Entry counts from Supplementary Table S3; glyphs schematic.", 14, fill=C.MUTED, anchor="end")

export(fig, "Graphical_abstract", dpi=254)

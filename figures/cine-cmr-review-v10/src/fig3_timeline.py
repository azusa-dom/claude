"""Figure 3: cine-CMR motion estimators by year, by the strongest validation evidence each source reports.

agarwood-scifig house style, 190 mm. Data: data/table_s3_methods.csv (one row per plotted entry,
with the Table S3 line and the classification rationale).
"""
import csv
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
from scifig_common import C, T, export, start, tw  # noqa: E402

DATA = Path(__file__).resolve().parents[1] / "data" / "table_s3_methods.csv"

LANES = [
    ("conventional", ["Conventional &", "comparators"]),
    ("unsupervised", ["Unsupervised", "registration"]),
    ("cardiac", ["Cardiac-specific"]),
    ("physics", ["Physics &", "biomechanics"]),
    ("supervised", ["Reference-supervised", "& end-to-end"]),
]
EVIDENCE = [
    ("mask", "Mask, landmark, registration or inter-method agreement"),
    ("label", "Downstream label: class, LGE, outcome or expert reading"),
    ("material", "Material-sensitive reference: known motion, DENSE or tagging; no focal deficit"),
    ("focal", "Prescribed focal deficit with known motion (independent evaluation)"),
    ("nr", "Validation data not reported"),
]
FILL = {"mask": C.MASK, "label": C.CORAL, "material": C.REF, "focal": C.REF, "nr": C.WHITE}

X0, X1 = 176.0, 776.0
EARLY, LATE = (1998.5, 2000.5), (2008.5, 2026.5)
EARLY_PX, GAP = 15.0, 24.0
LATE_PX = (X1 - X0 - (EARLY[1] - EARLY[0]) * EARLY_PX - GAP) / (LATE[1] - LATE[0])
ROW, PAD, DOT_R, DX = 15.0, 5.0, 4.0, 7.0
FS = T.SMALL + 0.5
RIGHT_LIMIT = 786.0


def year_x(y):
    if y <= EARLY[1]:
        return X0 + (y - EARLY[0]) * EARLY_PX
    return X0 + (EARLY[1] - EARLY[0]) * EARLY_PX + GAP + (y - LATE[0]) * LATE_PX


def load():
    with DATA.open(newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["year"] = int(r["year"])
        r["text"] = r["label"] + r["flag"]
        r["x"] = year_x(r["year"])
        r["w"] = tw(r["text"], FS)
    return rows


def pack(items):
    """Greedy rows so that dot-plus-label intervals never overlap within a lane."""
    rights = []
    for it in sorted(items, key=lambda r: (r["x"], r["label"])):
        it["flip"] = it["x"] + DX + it["w"] > RIGHT_LIMIT
        if it["flip"]:
            left, right = it["x"] - DX - it["w"] - 5, it["x"] + DOT_R + 3
        else:
            left, right = it["x"] - DOT_R - 3, it["x"] + DX + it["w"] + 5
        for i, edge in enumerate(rights):
            if edge < left:
                it["row"], rights[i] = i, right
                break
        else:
            it["row"] = len(rights)
            rights.append(right)
    return max(len(rights), 1)


def marker(fig, x, y, ev, r=DOT_R):
    if ev == "focal":
        s = r * 1.45
        fig.path(f"M{x:.1f} {y - s:.1f} L{x + s:.1f} {y:.1f} L{x:.1f} {y + s:.1f} L{x - s:.1f} {y:.1f} Z",
                 C.INK, 1.4, fill=C.REF)
    elif ev == "nr":
        fig.circle(x, y, r - 0.4, C.WHITE, C.INK, 1.1)
    else:
        fig.circle(x, y, r, FILL[ev])


rows = load()
n_rows = {k: pack([r for r in rows if r["lane"] == k]) for k, _ in LANES}
lane_h = {k: n * ROW + 2 * PAD for k, n in n_rows.items()}
counts = Counter(r["evidence"] for r in rows)
years = sorted({r["year"] for r in rows})
per_year = {y: Counter(r["evidence"] for r in rows if r["year"] == y) for y in years}
n_material = counts["material"]
n_total = len(rows)

TOP = 44.0
lanes_h = sum(lane_h.values())
HIST_TOP = TOP + lanes_h + 24
UNIT = 5.5
HIST_H = max(sum(c.values()) for c in per_year.values()) * UNIT + 4
AXIS_Y = HIST_TOP + HIST_H
B_TOP = AXIS_Y + 58
H = B_TOP + 30 + len(EVIDENCE) * 19 + 34

fig = start(H, f"Figure 3 | Material-sensitive references in {n_material} of {n_total} estimators",
            footer=["Classes assigned from Supplementary Table S3 cells (abstract- or metadata-level readings); one marker per entry.",
                    "LGE, late gadolinium enhancement; DENSE, displacement encoding with stimulated echoes."])

# ---- a: timeline -----------------------------------------------------------------------------
fig.panel(20, 24, "a", f"Material-sensitive validation in {n_material} of {n_total} entries; "
                       f"a prescribed focal deficit in {counts['focal']}")
gx0 = year_x(EARLY[1])
gx1 = gx0 + GAP


def hrule(y, color=C.GRID, w=0.8, x_from=20):
    fig.line(x_from, y, gx0 + 2, y, color, w)
    fig.line(gx1 - 2, y, X1 + 6, y, color, w)


hrule(TOP, C.INK, 1.2)
y = TOP
for key, title in LANES:
    h = lane_h[key]
    items = [r for r in rows if r["lane"] == key]
    for i, s in enumerate(title):
        fig.text(20, y + PAD + 12 + i * 15, s, T.BODY, 700)
    n_mat = sum(r["evidence"] in ("material", "focal") for r in items)
    fig.text(20, y + PAD + 12 + len(title) * 15 + 1, f"{len(items)} entries · {n_mat} material-sensitive", T.SMALL,
             fill=C.MUTED)
    for it in items:
        cy = y + PAD + ROW / 2 + it["row"] * ROW
        marker(fig, it["x"], cy, it["evidence"])
        if it["flip"]:
            fig.text(it["x"] - DX, cy + 4, it["text"], FS, anchor="end")
        else:
            fig.text(it["x"] + DX, cy + 4, it["text"], FS)
    y += h
    hrule(y, C.INK if key == LANES[-1][0] else C.GRID, 1.2 if key == LANES[-1][0] else 0.8)
fig.raw(f'<text transform="translate({(gx0 + gx1) / 2 + 4:.1f},{TOP + lanes_h / 2:.1f}) rotate(-90)" '
        f'font-size="{T.SMALL}" fill="{C.MUTED}" text-anchor="middle">2001–2008: no entries</text>')

# entries per year, stacked by evidence class, on the shared year axis
fig.text(20, HIST_TOP + 14, "Entries per year", T.BODY, 700)
fig.text(20, HIST_TOP + 28, "stacked by evidence class", T.SMALL, fill=C.MUTED)
for yv in (0, 5):
    yy = AXIS_Y - 2 - yv * UNIT
    fig.line(X0 - 6, yy, X0 - 2, yy, C.INK, 0.9)
    fig.text(X0 - 9, yy + 4, str(yv), T.SMALL, fill=C.MUTED, anchor="end")
fig.line(X0 - 2, AXIS_Y - 2, X0 - 2, AXIS_Y - 2 - 9 * UNIT, C.INK, 0.9)
order = ["focal", "material", "label", "mask", "nr"]
for yr in years:
    x = year_x(yr)
    base = AXIS_Y - 2
    bw = 9.0 if yr > 2000 else 8.0
    for ev in order:
        n = per_year[yr][ev]
        if not n:
            continue
        hgt = n * UNIT
        if ev == "nr":
            fig.rect(x - bw / 2 + 0.5, base - hgt + 0.5, bw - 1, hgt - 1, C.WHITE, C.INK, 0.9)
        else:
            fig.rect(x - bw / 2, base - hgt, bw, hgt, FILL[ev], C.INK if ev == "focal" else C.WHITE,
                     1.2 if ev == "focal" else 0.6)
        base -= hgt
    tot = sum(per_year[yr].values())
    if tot >= 3:
        fig.text(x, base - 4, str(tot), T.SMALL, 700, anchor="middle")

# broken year axis
fig.line(X0 - 4, AXIS_Y, gx0 + 3, AXIS_Y, C.INK, 0.9)
fig.line(gx1 - 3, AXIS_Y, X1 + 4, AXIS_Y, C.INK, 0.9)
for bx in (gx0 + 3, gx1 - 3):
    fig.line(bx - 2.5, AXIS_Y + 4, bx + 2.5, AXIS_Y - 4, C.INK, 0.9)
for yr in [1999, 2000] + list(range(2009, 2027)):
    x = year_x(yr)
    fig.line(x, AXIS_Y, x, AXIS_Y + 4, C.INK, 0.9)
    if yr <= 2000:
        fig.raw(f'<text transform="translate({x + 3.8:.1f},{AXIS_Y + 7:.1f}) rotate(-90)" font-size="{T.SMALL}" '
                f'fill="{C.MUTED}" text-anchor="end">{yr}</text>')
    else:
        fig.text(x, AXIS_Y + 16, str(yr), T.SMALL, fill=C.MUTED, anchor="middle")
fig.text(X0 + (X1 - X0) / 2, AXIS_Y + 33, "year of publication", T.LABEL + 0.5, anchor="middle")

# ---- b: evidence classes and totals ------------------------------------------------------------
fig.row_rule(B_TOP - 14)
fig.panel(20, B_TOP + 10, "b", "Mask or landmark agreement dominates; focal recovery tested once")
BX, SCALE = 560.0, 8.0
fig.text(BX, B_TOP + 32, f"entries (n = {n_total})", T.SMALL, fill=C.MUTED)
for i, (key, text) in enumerate(EVIDENCE):
    yy = B_TOP + 48 + i * 19
    marker(fig, 28, yy - 4, key)
    fig.text(42, yy, text, T.BODY - 1)
    n = counts.get(key, 0)
    if key == "nr":
        fig.rect(BX, yy - 10, n * SCALE, 11, C.WHITE, C.INK, 0.9)
    else:
        fig.rect(BX, yy - 10, n * SCALE, 11, FILL[key], C.INK if key == "focal" else "none", 1.2)
    fig.text(BX + n * SCALE + 6, yy, str(n), T.SMALL + 0.5, 700)
fig.line(BX, B_TOP + 36, BX, B_TOP + 48 + 4 * 19 + 4, C.INK, 0.9)
fy = B_TOP + 48 + len(EVIDENCE) * 19 + 6
fig.text(20, fy, "\u00a0\u00a0\u00a0".join(["* tagging-side comparator", "† preprint (MSc thesis)",
                                  "‡ workshop paper or no abstract retrieved", "§ rat model"]), T.SMALL, fill=C.MUTED)

export(fig, "Figure_3_method_timeline")
print(f"counts {dict(counts)}; total {n_total}")

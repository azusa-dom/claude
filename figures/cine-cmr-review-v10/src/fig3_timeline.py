"""Figure 3: cine-CMR motion estimators by year, coloured by strongest reported validation evidence."""
import csv
import sys
from collections import Counter
from pathlib import Path

from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D
from matplotlib.textpath import TextPath

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
from figstyle import (CORAL, MASK, FS_BODY, FS_SMALL, OBS, OBS_T, INK, MAIN_W, MUTED, REF,  # noqa: E402
                      ERR, RULE, canvas, save)

DATA = Path(__file__).resolve().parents[1] / "data" / "table_s3_methods.csv"

LANES = [
    ("conventional", "Conventional &\ncomparators"),
    ("unsupervised", "Unsupervised\nregistration"),
    ("cardiac", "Cardiac-specific"),
    ("physics", "Physics &\nbiomechanics"),
    ("supervised", "Reference-supervised\n& end-to-end"),
]
EVIDENCE = [
    ("mask", "Mask, landmark, registration or inter-method agreement"),
    ("label", "Downstream label: class, LGE, outcome or expert reading"),
    ("material", "Material-sensitive reference: known motion, DENSE or tagging; no focal deficit"),
    ("focal", "Prescribed focal deficit with known motion (independent evaluation)"),
    ("nr", "Validation data not reported"),
]

X0, X1 = 31.0, 157.0
EARLY = (1998.5, 2011.5)
LATE = (2016.5, 2026.5)
EARLY_MM_PER_YR = 2.0
GAP = 5.0
LATE_MM_PER_YR = (X1 - X0 - (EARLY[1] - EARLY[0]) * EARLY_MM_PER_YR - GAP) / (LATE[1] - LATE[0])

ROW = 3.55
LANE_PAD = 1.4
DOT_R = 0.95
LABEL_DX = 1.7
RIGHT_LIMIT = 159.0
FONT = FontProperties(family="Liberation Sans", size=FS_SMALL)


def year_x(year):
    if year <= EARLY[1]:
        return X0 + (year - EARLY[0]) * EARLY_MM_PER_YR
    return X0 + (EARLY[1] - EARLY[0]) * EARLY_MM_PER_YR + GAP + (year - LATE[0]) * LATE_MM_PER_YR


def text_mm(s):
    ext = TextPath((0, 0), s, prop=FONT).get_extents()
    return ext.width / 72 * 25.4


def marker_style(evidence):
    base = dict(markersize=DOT_R * 2 / 25.4 * 72, markeredgewidth=0.6, linestyle="none")
    if evidence == "mask":
        return dict(base, marker="o", markerfacecolor=MASK, markeredgecolor=MASK)
    if evidence == "label":
        return dict(base, marker="o", markerfacecolor=CORAL, markeredgecolor=CORAL)
    if evidence == "material":
        return dict(base, marker="o", markerfacecolor=REF, markeredgecolor=REF)
    if evidence == "focal":
        return dict(base, marker="D", markersize=base["markersize"] * 0.95, markerfacecolor=REF,
                    markeredgecolor=INK, markeredgewidth=1.1)
    return dict(base, marker="o", markerfacecolor="white", markeredgecolor=INK)


def load():
    with DATA.open(newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["year"] = int(r["year"])
        r["text"] = r["label"] + r["flag"]
        r["x"] = year_x(r["year"])
        r["w"] = text_mm(r["text"])
    return rows


def pack(items):
    """Greedy row assignment so dot-plus-label intervals never overlap within a lane."""
    rights = []
    for it in sorted(items, key=lambda r: (r["x"], r["label"])):
        it["flip"] = it["x"] + LABEL_DX + it["w"] > RIGHT_LIMIT
        if it["flip"]:
            left, right = it["x"] - LABEL_DX - it["w"] - 0.9, it["x"] + DOT_R + 0.4
        else:
            left, right = it["x"] - DOT_R - 0.4, it["x"] + LABEL_DX + it["w"] + 0.9
        for i, edge in enumerate(rights):
            if edge < left:
                it["row"], rights[i] = i, right
                break
        else:
            it["row"] = len(rights)
            rights.append(right)
    return max(len(rights), 1)


def main():
    rows = load()
    lane_rows = {key: pack([r for r in rows if r["lane"] == key]) for key, _ in LANES}
    lane_h = {k: n * ROW + 2 * LANE_PAD for k, n in lane_rows.items()}

    legend_h = 5 * 3.4 + 3.5
    foot_h = 10.0
    axis_h = 7.0
    timeline_h = sum(lane_h.values())
    H = 2.0 + timeline_h + axis_h + legend_h + foot_h

    fig, ax = canvas(MAIN_W, H)
    top = H - 2.0
    bottom = top - timeline_h

    ticks = [1999, 2000, 2011] + list(range(2017, 2027))
    gx0 = year_x(EARLY[1])
    # Full-height year grid lines ran through dense method labels. Position is
    # already encoded by the shared x-axis and dots, so whitespace is clearer.
    ax.text(gx0 + GAP / 2, bottom + timeline_h / 2, "2012–2016: no entries", rotation=90,
            rotation_mode="anchor", ha="center", va="center", fontsize=FS_SMALL, color=MUTED)

    y_cursor = top
    for key, title in LANES:
        h = lane_h[key]
        y_top = y_cursor
        # Leave the broken-axis gap open so the vertical gap label is not
        # crossed by lane rules.
        ax.plot([1.0, gx0 + 0.5], [y_top, y_top], color=RULE, lw=0.5, zorder=1)
        ax.plot([gx0 + GAP - 0.5, X1 + 1.5], [y_top, y_top], color=RULE, lw=0.5, zorder=1)
        ax.text(X0 - 3.0, y_top - h / 2, title, ha="right", va="center", fontsize=FS_BODY,
                color=INK, linespacing=1.15)
        items = [r for r in rows if r["lane"] == key]
        for it in items:
            it["y"] = y_top - LANE_PAD - ROW / 2 - it["row"] * ROW
        for it in items:
            ax.plot([it["x"]], [it["y"]], zorder=3, **marker_style(it["evidence"]))
            tx, ha = (it["x"] - LABEL_DX, "right") if it["flip"] else (it["x"] + LABEL_DX, "left")
            ax.text(tx, it["y"], it["text"], ha=ha, va="center", fontsize=FS_SMALL, color=INK, zorder=4)
        y_cursor -= h
    ax.plot([1.0, gx0 + 0.5], [bottom, bottom], color=RULE, lw=0.5)
    ax.plot([gx0 + GAP - 0.5, X1 + 1.5], [bottom, bottom], color=RULE, lw=0.5)

    ax_y = bottom - 1.2
    ax.plot([X0 - 1.0, gx0 + 1.2], [ax_y, ax_y], color=INK, lw=0.6)
    ax.plot([gx0 + GAP - 1.2, X1 + 1.0], [ax_y, ax_y], color=INK, lw=0.6)
    for dx in (1.2, GAP - 1.2):
        bx = gx0 + dx
        ax.plot([bx - 0.5, bx + 0.5], [ax_y - 0.9, ax_y + 0.9], color=INK, lw=0.6)
    for y in ticks:
        x = year_x(y)
        ax.plot([x, x], [ax_y, ax_y - 0.4], color=INK, lw=0.6)
        label = str(y) if y in (1999, 2011) or y >= 2017 else ""
        if y == 2000:
            label = "2000"
        label_x = x - 0.65 if y == 1999 else x + 0.65 if y == 2000 else x
        label_y = ax_y - 3.5 if y in (1999, 2000) else ax_y - 1.6
        ax.text(label_x, label_y, label, ha="center", va="top", fontsize=FS_SMALL, color=INK,
                rotation=90 if y in (1999, 2000) else 0, rotation_mode="anchor")
    ax.text(X0 - 3.0, ax_y - 1.6, "Year of\npublication", ha="right", va="top", fontsize=FS_SMALL,
            color=MUTED, linespacing=1.1)

    counts = Counter(r["evidence"] for r in rows)
    ly = ax_y - axis_h - 2.5
    bar_x0, bar_scale = 138.0, 0.85
    ax.text(bar_x0, ly + 2.6, "entries", ha="left", va="bottom", fontsize=FS_SMALL, color=MUTED)
    for key, text in EVIDENCE:
        ax.plot([X0 + 0.5], [ly], **marker_style(key))
        ax.text(X0 + 2.6, ly, text, ha="left", va="center", fontsize=FS_SMALL, color=INK)
        n = counts.get(key, 0)
        st = marker_style(key)
        face = st["markerfacecolor"]
        edge = st["markeredgecolor"]
        ax.add_patch(__import__("matplotlib").patches.Rectangle(
            (bar_x0, ly - 1.0), n * bar_scale, 2.0, facecolor=face, edgecolor=edge,
            lw=st["markeredgewidth"]))
        ax.text(bar_x0 + n * bar_scale + 1.0, ly, str(n), ha="left", va="center", fontsize=FS_SMALL, color=INK)
        ly -= 3.4

    foot = ("* tagging-side comparator   † preprint (MSc thesis)   ‡ workshop paper or no abstract retrieved   "
            "§ rat model.\nMarker = strongest validation evidence each cited source reports (abstract- or metadata-level "
            "reading, Supplementary Table S3).\nBoundary feature tracking (a method family without a single year) "
            "is listed in Supplementary Table S3 but not plotted.")
    ax.text(1.0, ly + 0.6, foot, ha="left", va="top", fontsize=FS_SMALL, color=MUTED, linespacing=1.25)

    save(fig, "Figure_3_method_timeline", {
        "axes": [ax],
        "panel_ids": ["timeline-canvas"],
    })
    print(f"Figure 3: {MAIN_W:.0f} x {H:.1f} mm; counts {dict(counts)}; total {len(rows)}")


if __name__ == "__main__":
    main()

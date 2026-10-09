"""Supplementary Figure S2: attributes of regional error and mapping validity."""
import sys
from pathlib import Path

import numpy as np
from matplotlib.patches import Polygon

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
from figstyle import (FS_BODY, FS_SMALL, FS_TITLE, OBS, INK, MUTED, REF, REF_T, ERR,  # noqa: E402
                      SUPP_W, INF, canvas, panel_label, save, sub_axes)

W, H = SUPP_W, 100.0


def g(x, c, w):
    return np.exp(-((x - c) / w) ** 2)


def mini(fig, x, y, w, h, title_text, ax):
    p = sub_axes(fig, W, H, x, y, w, h)
    ax.text(x, y + h + 2.0, title_text, fontsize=FS_BODY, fontweight="bold", va="bottom")
    p.set_xticks([])
    p.set_yticks([])
    return p


def profile_panel(p, ref, est, x, shade=None):
    if shade is not None:
        p.fill_between(x, 0, 1.15, where=shade, color=REF_T, lw=0, zorder=0)
    p.plot(x, ref, color=REF, lw=1.2)
    p.plot(x, est, color=INF, lw=1.2, ls=(0, (3, 1.6)))
    p.set_xlim(0, 1)
    p.set_ylim(-0.05, 1.15)


def grid_panel(p, mapping, n=12, m=200):
    u = np.linspace(0, 1, n)
    s = np.linspace(0, 1, m)
    for c in u:
        X, Y = mapping(np.full_like(s, c), s)
        p.plot(X, Y, color=OBS, lw=0.6)
        X, Y = mapping(s, np.full_like(s, c))
        p.plot(X, Y, color=OBS, lw=0.6)
    eps = 1e-4
    for i in range(n - 1):
        for j in range(n - 1):
            cx, cy = (u[i] + u[i + 1]) / 2, (u[j] + u[j + 1]) / 2
            x1, y1 = mapping(np.array([cx + eps]), np.array([cy]))
            x0, y0 = mapping(np.array([cx - eps]), np.array([cy]))
            x3, y3 = mapping(np.array([cx]), np.array([cy + eps]))
            x2, y2 = mapping(np.array([cx]), np.array([cy - eps]))
            det = ((x1 - x0) * (y3 - y2) - (x3 - x2) * (y1 - y0)) / (4 * eps * eps)
            if det[0] <= 0:
                corners = [(u[i], u[j]), (u[i + 1], u[j]), (u[i + 1], u[j + 1]), (u[i], u[j + 1])]
                pts = [mapping(np.array([a]), np.array([b])) for a, b in corners]
                p.add_patch(Polygon([(px[0], py[0]) for px, py in pts], closed=True, facecolor="none",
                                    edgecolor=ERR, lw=0.9, zorder=4))
    p.set_aspect("equal")
    p.set_xlim(-0.08, 1.08)
    p.set_ylim(-0.08, 1.08)
    p.axis("off")


def main():
    fig, ax = canvas(W, H)
    x = np.linspace(0, 1, 400)
    spatial_axes = []
    temporal_axes = []
    mapping_axes = []

    panel_label(ax, 0.5, H - 0.5, "a")
    ax.text(5.0, H - 1.4, "Spatial error attributes", fontsize=FS_TITLE, fontweight="bold", va="top")
    ref = g(x, 0.45, 0.09)
    cases = [
        ("Magnitude", 0.5 * ref, "deficit under-estimated", None),
        ("Location", g(x, 0.63, 0.09), "centroid displaced", None),
        ("Extent", 0.62 * g(x, 0.45, 0.17), "region spread wider", None),
        ("Support", ref + 0.55 * g(x, 0.85, 0.05), "abnormality outside\nreference support", ref > 0.2),
    ]
    pw, ph, gap, y0 = 36.0, 20.0, 5.3, H - 33.0
    for k, (name, est, cap, shade) in enumerate(cases):
        px = 4.0 + k * (pw + gap)
        p = mini(fig, px, y0, pw, ph, name, ax)
        spatial_axes.append(p)
        profile_panel(p, ref, est, x, shade)
        ax.text(px, y0 - 1.5, cap, fontsize=FS_SMALL, va="top", color=INK, linespacing=1.15)
    ax.text(W - 1.0, H - 1.4, "position around the wall →", fontsize=FS_SMALL, color=MUTED, ha="right", va="top")
    lx, ly = W - 60.0, H - 6.3
    ax.plot([lx, lx + 5], [ly, ly], color=REF, lw=1.2)
    ax.text(lx + 6.2, ly, "reference", fontsize=FS_SMALL, va="center")
    ax.plot([lx + 22, lx + 27], [ly, ly], color=INF, lw=1.2, ls=(0, (3, 1.6)))
    ax.text(lx + 28.2, ly, "estimate", fontsize=FS_SMALL, va="center")

    panel_label(ax, 0.5, 52.5, "b")
    ax.text(5.0, 51.6, "Temporal error attributes", fontsize=FS_TITLE, fontweight="bold", va="top")
    t = np.linspace(0, 1, 400)
    rc = -g(t, 0.38, 0.13)
    for k, (name, est, cap) in enumerate([
        ("Magnitude", 0.65 * rc, "peak amplitude reduced"),
        ("Timing", -g(t, 0.50, 0.13), "peak time delayed"),
    ]):
        px = 4.0 + k * (pw + gap)
        p = mini(fig, px, 19.0, pw, ph, name, ax)
        temporal_axes.append(p)
        p.plot(t, rc, color=REF, lw=1.2)
        p.plot(t, est, color=INF, lw=1.2, ls=(0, (3, 1.6)))
        p.set_xlim(0, 1)
        p.set_ylim(-1.15, 0.08)
        p.axhline(0, color=MUTED, lw=0.4)
        ax.text(px, 17.5, cap, fontsize=FS_SMALL, va="top", color=INK)
    ax.text(4.0 + 2 * pw + gap, 51.6, "time →", fontsize=FS_SMALL, color=MUTED, ha="right", va="top")

    panel_label(ax, 2 * (pw + gap) + 1.5, 52.5, "c")
    cx0 = 2 * (pw + gap) + 6.0
    ax.text(cx0, 51.6, "Mapping validity", fontsize=FS_TITLE, fontweight="bold", va="top")

    def smooth(X, Y):
        return X + 0.06 * np.sin(np.pi * Y) * np.sin(np.pi * X), Y + 0.04 * np.sin(2 * np.pi * X)

    def folded(X, Y):
        b = g(Y, 0.5, 0.22)
        return X + 0.30 * g(X, 0.5, 0.12) * b, Y

    gw = 27.0
    for k, (fn, name, cap) in enumerate([
        (smooth, "Invertible", "det J > 0 everywhere,\nyet can still be wrong"),
        (folded, "Folded", "det J ≤ 0 in outlined\ncells: orientation reversed"),
    ]):
        px = cx0 + k * (gw + 7.0)
        p = mini(fig, px, 12.5, gw, gw, name, ax)
        mapping_axes.append(p)
        grid_panel(p, fn)
        ax.text(px, 11.0, cap, fontsize=FS_SMALL, va="top", color=INK, linespacing=1.15)

    ax.text(0.5, 1.0, "Prescribed schematics with no measured scale; a single mean-squared error can hide "
            "every one of these failures.", fontsize=FS_SMALL, color=MUTED, va="bottom")
    plot_axes = spatial_axes + temporal_axes + mapping_axes
    plot_ids = ["a1", "a2", "a3", "a4", "b1", "b2", "c1", "c2"]
    save(fig, "Figure_S2_error_attributes_mapping_validity", {
        "axes": plot_axes,
        "panel_ids": plot_ids,
        "row_groups": [["a1", "a2", "a3", "a4"], ["b1", "b2"], ["c1", "c2"]],
        "column_groups": [["a1", "b1"], ["a2", "b2"]],
    })
    print(f"Figure S2: {W:.0f} x {H:.0f} mm")


if __name__ == "__main__":
    main()

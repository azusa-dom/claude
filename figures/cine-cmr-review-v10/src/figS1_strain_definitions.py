"""Supplementary Figure S1: the same motion gives different numbers under different strain definitions."""
import sys
from pathlib import Path

import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, Wedge

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
from figstyle import (REF, FS_SMALL, FS_TITLE, OBS, OBS_T, INK, MUTED, ERR, SUPP_W, INF,  # noqa: E402
                      canvas, panel_label, save, sub_axes)

W, H = SUPP_W, 112.0
HW = W / 2
ROW_TOP = (H, H / 2 + 1.0)


def g(t, c, w):
    return np.exp(-((t - c) / w) ** 2)


def title(ax, col, row, letter, text):
    x, y = col * HW, ROW_TOP[row]
    panel_label(ax, x + 0.5, y - 0.5, letter)
    ax.text(x + 5.0, y - 1.4, text, fontsize=FS_TITLE, fontweight="bold", va="top")


def note(ax, col, row, text):
    ax.text(col * HW + 5.0, ROW_TOP[row] - 47.0, text, fontsize=FS_SMALL, va="top", color=MUTED, linespacing=1.2)


def plot_box(fig, col, row):
    return sub_axes(fig, W, H, col * HW + 16.0, ROW_TOP[row] - 39.0, 60.0, 31.0)


def arrow(ax, p0, p1, color, lw=0.8):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>,head_length=1.3,head_width=0.8", mutation_scale=1,
                                 color=color, lw=lw, shrinkA=0, shrinkB=0, zorder=5))


def tidy(p, ylabel=None):
    p.set_xlim(0, 1)
    p.set_ylim(-0.27, 0.05)
    p.set_xticks([0, 0.5, 1], ["0", "0.5", "1"])
    p.set_yticks([-0.2, -0.1, 0], ["−0.2", "−0.1", "0"])
    p.set_xlabel("normalised cycle time", labelpad=1)
    if ylabel:
        p.set_ylabel(ylabel, labelpad=2)


def main():
    fig, ax = canvas(W, H)

    title(ax, 0, 0, "a", "Strain measure: engineering vs Green–Lagrange")
    pa = plot_box(fig, 0, 0)
    e = np.linspace(-0.3, 0.3, 200)
    pa.plot(e, e, color=MUTED, lw=0.9, ls=(0, (3, 2)))
    pa.plot(e, e + e ** 2 / 2, color=INK, lw=1.2)
    e0 = -0.2
    E0 = e0 + e0 ** 2 / 2
    pa.plot([e0, e0], [e0, E0], color=ERR, lw=1.4)
    pa.plot([e0], [e0], "o", color=MUTED, ms=2.8)
    pa.plot([e0], [E0], "o", color=INK, ms=2.8)
    pa.set_xlim(-0.3, 0.3)
    pa.set_ylim(-0.32, 0.36)
    pa.set_xticks([-0.2, 0, 0.2], ["−0.2", "0", "0.2"])
    pa.set_yticks([-0.2, 0, 0.2], ["−0.2", "0", "0.2"])
    pa.set_xlabel("engineering strain $e$", labelpad=1)
    pa.set_ylabel("reported value", labelpad=2)
    pa.text(-0.28, 0.31, "Green–Lagrange  $E = e + e^2/2$", fontsize=8.6, va="top", color=INK)
    pa.text(-0.28, 0.24, "engineering  $e$ (dashed)", fontsize=FS_SMALL, va="top", color=MUTED)
    pa.text(-0.17, -0.205, "$e = -0.20$  vs  $E = -0.18$", fontsize=FS_SMALL, color=INK, va="center")
    note(ax, 0, 0, "The same one-dimensional motion; the 0.02 gap is a\ndefinitional difference, not a tracking error.")

    title(ax, 1, 0, "b", "Coordinate axes and myocardial layer")
    cx, cy = HW + 30.0, ROW_TOP[0] - 25.0
    r_in, r_mid, r_out = 7.0, 10.5, 14.0
    ax.add_patch(Wedge((cx, cy), r_out, 0, 360, width=r_out - r_in, facecolor=OBS_T, edgecolor="none"))
    for r, ls in ((r_in, "-"), (r_mid, (0, (2, 1.5))), (r_out, "-")):
        ax.add_patch(Circle((cx, cy), r, facecolor="none", edgecolor=OBS, lw=0.8, ls=ls))
    for r, lab, ang in ((r_in, "endocardial", -18), (r_mid, "mid-wall (transmural)", -30), (r_out, "epicardial", -42)):
        a = np.deg2rad(ang)
        x0, y0 = cx + r * np.cos(a), cy + r * np.sin(a)
        ax.plot([x0, cx + 17.5], [y0, y0], color=OBS, lw=0.5)
        ax.text(cx + 18.2, y0, lab, fontsize=FS_SMALL, va="center")
    th = np.deg2rad(115)
    px, py = cx + r_mid * np.cos(th), cy + r_mid * np.sin(th)
    ax.plot([px], [py], "o", color=INK, ms=2.4, zorder=6)
    arrow(ax, (px, py), (px + 6.5 * np.cos(th), py + 6.5 * np.sin(th)), INK)
    arrow(ax, (px, py), (px - 6.5 * np.sin(th), py + 6.5 * np.cos(th)), INK)
    ax.text(px + 7.2 * np.cos(th), py + 7.2 * np.sin(th) + 0.4, "radial", fontsize=FS_SMALL, ha="center", va="bottom")
    ax.text(px - 7.0 * np.sin(th) - 2.0, py + 7.0 * np.cos(th), "circumferential", fontsize=FS_SMALL,
            ha="right", va="center")
    note(ax, 1, 0, "Endocardial, transmural and epicardial values differ; local\naxes depend on the reference frame and centreline, and a\n2D slice omits through-plane terms.")

    t = np.linspace(0, 1, 600)
    title(ax, 0, 1, "c", "Which peak? Three readouts of one curve")
    pc = plot_box(fig, 0, 1)
    E = -0.17 * g(t, 0.30, 0.12) - 0.20 * g(t, 0.50, 0.09)
    pc.plot(t, E, color=INK, lw=1.1)
    t_es = 0.39
    pc.axvline(t_es, color=MUTED, lw=0.6, ls=(0, (2, 1.5)))
    pc.text(t_es + 0.015, 0.035, "end-systole", ha="left", va="top", fontsize=FS_SMALL, color=MUTED)
    i_sys = np.argmin(np.where(t <= t_es, E, 0))
    i_all = np.argmin(E)
    assert np.all(np.diff(t) > 0), "np.interp requires an increasing cycle-time grid"
    E_es = np.interp(t_es, t, E)
    readouts = [(t[i_sys], E[i_sys], "peak systolic", -0.035, -0.022),
                (t_es, E_es, "end-systolic", 0.030, 0.026),
                (t[i_all], E[i_all], "post-systolic peak", 0.035, -0.022)]
    for k, (tx, ex, lab, dx, dy) in enumerate(readouts, start=1):
        pc.plot([tx], [ex], "o", color=REF, ms=3.2, zorder=5)
        pc.text(tx + dx, ex + dy, str(k), ha="center", va="center", fontsize=FS_SMALL, color=INK,
                fontweight="bold")
        pc.text(0.66, -0.135 - (k - 1) * 0.034, f"{k}  {lab}  " + f"{ex:.2f}".replace("-", "−"), ha="left",
                va="center", fontsize=FS_SMALL, color=INK)
    tidy(pc, "segment strain")
    note(ax, 0, 1, "End-systolic, peak-systolic and whole-cycle peaks diverge\nwith dyssynchrony or post-systolic shortening.")

    title(ax, 1, 1, "d", "Order of spatial and temporal aggregation")
    pd = plot_box(fig, 1, 1)
    p1 = -0.20 * g(t, 0.28, 0.07)
    p2 = -0.20 * g(t, 0.46, 0.07)
    mean = (p1 + p2) / 2
    pd.plot(t, p1, color=MUTED, lw=0.8)
    pd.plot(t, p2, color=MUTED, lw=0.8)
    pd.plot(t, mean, color=INF, lw=1.3)
    pd.axhline(mean.min(), color=INF, lw=0.6, ls=(0, (2, 1.5)))
    pd.axhline(-0.20, color=INK, lw=0.6, ls=(0, (2, 1.5)))
    pd.text(0.98, mean.min() - 0.008, f"min of mean  {mean.min():.2f}".replace("-", "−"),
            ha="right", va="top", fontsize=FS_SMALL, color=INK)
    pd.text(0.98, -0.20 - 0.008, "mean of minima  −0.20", ha="right", va="top",
            fontsize=FS_SMALL, color=INK)
    pd.text(0.62, -0.035, "two points in\none segment", fontsize=FS_SMALL, color=MUTED, va="center")
    pd.text(0.02, -0.075, "segment\nmean", fontsize=FS_SMALL, color=INK, va="center")
    tidy(pd, "strain")
    note(ax, 1, 1, "Averaging before or after selecting the temporal peak\ngives different values for the same field.")

    ax.text(0.5, 1.0, "Conceptual and analytic schematics with no measured scale.", fontsize=FS_SMALL,
            color=MUTED, va="bottom")
    save(fig, "Figure_S1_strain_definition_traps", {
        "axes": [pa, pc, pd],
        "panel_ids": ["a", "c", "d"],
        "row_groups": [["c", "d"]],
        "column_groups": [["a", "c"]],
    })
    print(f"Figure S1: {W:.0f} x {H:.0f} mm")


if __name__ == "__main__":
    main()

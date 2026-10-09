"""Figure 2: identical contours, different material correspondence (analytic counterexample)."""
import sys
from pathlib import Path

import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, PathPatch, Wedge
from matplotlib.path import Path as MPath

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
from figstyle import (FS_BODY, FS_SMALL, FS_TITLE, GREY, GREY_T, INK, MAIN_W, MUTED, ORANGE,  # noqa: E402
                      TEAL, canvas, panel_label, save, sub_axes)

W, H = MAIN_W, 58.0
A = 0.5


def annulus(ax, cx, cy, r_in, r_out, face=GREY_T, edge=GREY, lw=0.8, z=1):
    ax.add_patch(Wedge((cx, cy), r_out, 0, 360, width=r_out - r_in, facecolor=face, edgecolor="none", zorder=z))
    for r in (r_in, r_out):
        ax.add_patch(Circle((cx, cy), r, facecolor="none", edgecolor=edge, lw=lw, zorder=z + 1))
    return Wedge((cx, cy), r_out, 0, 360, width=r_out - r_in, transform=ax.transData)


def clip_to(artist, ax, cx, cy, r_in, r_out):
    clip = Wedge((cx, cy), r_out, 0, 360, width=r_out - r_in, transform=ax.transData)
    artist.set_clip_path(clip)


def panel_a(ax):
    panel_label(ax, 0.5, H - 0.5, "a")
    ax.text(5.0, H - 1.4, "What each acquisition supplies", fontsize=FS_TITLE, fontweight="bold", va="top")
    r_in, r_out, cy = 4.3, 7.6, 37.5
    rng = np.random.default_rng(7)
    specs = [(10.0, "Routine cine", "boundaries +\nweak texture"),
             (29.0, "Tagging", "prepared grid\n(material pattern)"),
             (48.0, "DENSE", "phase-encoded\ndisplacement")]
    for cx, title, note in specs:
        annulus(ax, cx, cy, r_in, r_out)
        ax.text(cx, cy + r_out + 2.0, title, ha="center", va="bottom", fontsize=FS_BODY, fontweight="bold")
        ax.text(cx, cy - r_out - 1.8, note, ha="center", va="top", fontsize=FS_SMALL, linespacing=1.15)
    cx = specs[0][0]
    pts = rng.uniform(-r_out, r_out, size=(260, 2))
    rr = np.hypot(*pts.T)
    pts = pts[(rr > r_in + 0.25) & (rr < r_out - 0.25)]
    ax.scatter(cx + pts[:, 0], cy + pts[:, 1], s=0.6, color=GREY, alpha=0.45, lw=0, zorder=3)
    cx = specs[1][0]
    for k in np.arange(-r_out, r_out + 0.01, 1.9):
        for xs, ys in (([cx + k, cx + k], [cy - r_out, cy + r_out]), ([cx - r_out, cx + r_out], [cy + k, cy + k])):
            (ln,) = ax.plot(xs, ys, color=ORANGE, lw=0.7, zorder=3)
            clip_to(ln, ax, cx, cy, r_in, r_out)
    cx = specs[2][0]
    for r in (5.75, 7.15):
        for th in np.linspace(0, 2 * np.pi, 10 if r < 6 else 14, endpoint=False) + (0.3 if r < 6 else 0):
            x, y = cx + r * np.cos(th), cy + r * np.sin(th)
            dr, dt = -0.95, 0.4
            dx = dr * np.cos(th) - dt * np.sin(th)
            dy = dr * np.sin(th) + dt * np.cos(th)
            ax.add_patch(FancyArrowPatch((x, y), (x + dx, y + dy), arrowstyle="-|>,head_length=0.7,head_width=0.45",
                                         mutation_scale=1, color=ORANGE, lw=0.7, zorder=3,
                                         shrinkA=0, shrinkB=0))
    ax.text(29.0, 18.0, "Only tagging and DENSE carry a material label;\ncine supplies boundaries and weak texture.",
            ha="center", va="top", fontsize=FS_SMALL, color=MUTED, linespacing=1.2)


def spokes(ax, cx, cy, r_in, r_out, thetas, color, lw=1.0, ls="-", z=4, dots=True):
    for th in thetas:
        ax.plot([cx + r_in * np.cos(th), cx + r_out * np.cos(th)],
                [cy + r_in * np.sin(th), cy + r_out * np.sin(th)], color=color, lw=lw, ls=ls, zorder=z,
                solid_capstyle="butt")
        if dots:
            rm = (r_in + r_out) / 2
            ax.add_patch(Circle((cx + rm * np.cos(th), cy + rm * np.sin(th)), 0.55, facecolor=color,
                                edgecolor="white", lw=0.4, zorder=z + 1))


def arc_arrow(ax, cx, cy, r, th0, th1, color):
    ts = np.linspace(th0, th1, 30)
    verts = np.column_stack([cx + r * np.cos(ts), cy + r * np.sin(ts)])
    ax.add_patch(FancyArrowPatch(path=MPath(verts), arrowstyle="-|>,head_length=1.1,head_width=0.7",
                                 mutation_scale=1, color=color, lw=0.6, zorder=6))


def panel_b(ax):
    panel_label(ax, 61.0, H - 0.5, "b")
    ax.text(65.5, H - 1.4, "Two mappings, identical contours", fontsize=FS_TITLE, fontweight="bold", va="top")
    r_in, r_out, cy = 5.4, 9.4, 37.5
    th = np.linspace(0, 2 * np.pi, 8, endpoint=False)
    for cx, title, mapped in ((73.0, r"Mapping 1:  $\theta' = \theta$", th),
                              (104.0, r"Mapping 2:  $\theta' = \theta + a\,\sin\theta$", th + A * np.sin(th))):
        annulus(ax, cx, cy, r_in, r_out)
        ax.text(cx, cy + r_out + 2.0, title, ha="center", va="bottom", fontsize=FS_BODY)
        if mapped is not th:
            spokes(ax, cx, cy, r_in, r_out, th, "#9DB9C6", lw=0.7, ls=(0, (1.6, 1.2)), z=3, dots=False)
            for t0, t1 in zip(th, mapped):
                if abs(t1 - t0) > 0.08:
                    arc_arrow(ax, cx, cy, r_out + 1.2, t0, t1, TEAL)
        spokes(ax, cx, cy, r_in, r_out, mapped, TEAL)
    ax.text(88.5, cy, "identical\nmasks", ha="center", va="center", fontsize=FS_SMALL, color=GREY, linespacing=1.15)
    ax.text(88.5, cy - r_out - 2.0, r"Dice = 1,  Hausdorff = 0;   $r' = r$,  $a = 0.5$",
            ha="center", va="top", fontsize=FS_SMALL, color=INK)
    ax.text(88.5, 19.0, "Dashed: reference positions.  Teal: mapped material\npoints (same eight points in both panels).",
            ha="center", va="top", fontsize=FS_SMALL, color=MUTED, linespacing=1.2)


def panel_c(fig, ax):
    panel_label(ax, 121.5, H - 0.5, "c")
    ax.text(126.0, H - 1.4, "Resulting stretch", fontsize=FS_TITLE, fontweight="bold", va="top")
    pc = sub_axes(fig, W, H, 131.0, 22.0, 27.5, 27.0)
    t = np.linspace(0, 2 * np.pi, 400)
    pc.plot(t, np.ones_like(t), color=TEAL, lw=1.0, ls=(0, (3, 2)))
    pc.plot(t, 1 + A * np.cos(t), color=TEAL, lw=1.3)
    pc.set_xlim(0, 2 * np.pi)
    pc.set_ylim(0.25, 1.7)
    pc.set_xticks([0, np.pi, 2 * np.pi], ["0", r"$\pi$", r"$2\pi$"])
    pc.set_yticks([0.5, 1.0, 1.5], ["0.5", "1.0", "1.5"])
    pc.set_xlabel(r"$\theta$", labelpad=1)
    pc.set_ylabel(r"$\lambda_\theta$", labelpad=1)
    pc.text(np.pi, 1.06, "mapping 1", ha="center", va="bottom", fontsize=FS_SMALL, color=TEAL)
    pc.text(np.pi, 0.45, "mapping 2", ha="center", va="top", fontsize=FS_SMALL, color=TEAL)
    ax.text(124.0, 13.0, r"$\lambda_\theta = 1 + a\,\cos\theta$, range 0.5–1.5;" "\n"
            r"orientation preserved for $|a| < 1$", ha="left", va="top", fontsize=FS_SMALL, linespacing=1.3)


def main():
    fig, ax = canvas(W, H)
    panel_a(ax)
    panel_b(ax)
    panel_c(fig, ax)
    ax.text(0.5, 1.0, "Analytic example, not a measured cardiac result. The stretch ratio "
            r"$\lambda_\theta$ is not Green–Lagrange strain.", fontsize=FS_SMALL, color=MUTED, va="bottom")
    save(fig, "Figure_2_same_contours_analytic")
    print(f"Figure 2: {W:.0f} x {H:.0f} mm")


if __name__ == "__main__":
    main()

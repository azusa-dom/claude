"""Shared matplotlib style for the v10 figure set (sizes in mm, colours from the figure plan)."""
from pathlib import Path

import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

MM = 1 / 25.4
MAIN_W = 160.0   # manuscript \textwidth (A4, 25 mm margins)
SUPP_W = 166.0   # supplement \textwidth (A4, 22 mm margins)

GREY = "#596052"     # image-observable information
TEAL = "#2A7F9E"     # estimated / inferred quantity
ORANGE = "#C8702A"   # reference / validation
RED = "#B3261E"      # error, loss, not reported (lines and symbols only)
GREEN = "#3C7A3E"    # supported claim
INK = "#222222"
MUTED = "#6B6F68"
RULE = "#D9DCD6"

GREY_T = "#ECEEEA"
TEAL_T = "#E2EFF4"
ORANGE_T = "#FAEBDD"
GREEN_T = "#E6F0E5"

SANS = ["Arial", "Liberation Sans"]
SERIF = ["Times New Roman", "Liberation Serif"]

FS_BODY = 7.5
FS_SMALL = 7.0
FS_TITLE = 9.0
FS_PANEL = 10.0

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": SANS,
    "font.serif": SERIF,
    "mathtext.fontset": "custom",
    "mathtext.rm": "Liberation Serif",
    "mathtext.it": "Liberation Serif:italic",
    "mathtext.bf": "Liberation Serif:bold",
    "font.size": FS_BODY,
    "axes.linewidth": 0.6,
    "axes.edgecolor": INK,
    "axes.labelcolor": INK,
    "axes.labelsize": FS_BODY,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "xtick.labelsize": FS_SMALL,
    "ytick.labelsize": FS_SMALL,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "xtick.major.size": 2.5,
    "ytick.major.size": 2.5,
    "xtick.color": INK,
    "ytick.color": INK,
    "lines.linewidth": 1.0,
    "hatch.linewidth": 0.6,
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

OUT = Path(__file__).resolve().parents[1] / "out"


def canvas(width_mm, height_mm):
    """Figure plus a full-bleed axes whose data units are millimetres (origin bottom-left)."""
    fig = plt.figure(figsize=(width_mm * MM, height_mm * MM))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, width_mm)
    ax.set_ylim(0, height_mm)
    ax.axis("off")
    return fig, ax


def sub_axes(fig, width_mm, height_mm, x, y, w, h):
    """Data axes placed by millimetre box on a canvas figure."""
    return fig.add_axes([x / width_mm, y / height_mm, w / width_mm, h / height_mm])


def panel_label(ax, x, y, letter):
    ax.text(x, y, letter, fontsize=FS_PANEL, fontweight="bold", va="top", ha="left", color=INK)


def save(fig, stem):
    OUT.mkdir(exist_ok=True)
    for ext in ("pdf", "svg"):
        fig.savefig(OUT / f"{stem}.{ext}")
    fig.savefig(OUT / f"{stem}.png", dpi=600)
    plt.close(fig)

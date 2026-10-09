"""Shared matplotlib style for the v10 figure set.

Palette derived from the author's reference swatches (沈香墨 #8D6449, 素绢白 #F8F3E7,
檀木棕 #C0997F, 棠梨绯 #E7A49A), deepened where needed so co-occurring data colours pass
the dataviz palette validator (CVD and normal-vision separation). One muted grey-green
is kept for "supported" so it separates from the error red.
"""
from pathlib import Path

import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from audit_panel_alignment import require_matplotlib_panel_alignment  # noqa: E402

MM = 1 / 25.4
MAIN_W = 160.0   # manuscript \textwidth (A4, 25 mm margins)
SUPP_W = 166.0   # supplement \textwidth (A4, 22 mm margins)

OBS = "#8E857D"      # image-observable information / neutral context
INF = "#C0584A"      # estimated / inferred quantity (deepened 棠梨绯)
REF = "#7A4720"      # reference / validation (deepened 沈香墨)
CORAL = "#CC5F4F"    # secondary categorical distinction (Fig 3 downstream label, Fig 4 scar)
MASK = "#B2AAA2"     # weakest evidence class in Fig 3 (intentional neutral)
ERR = "#A33A2E"      # error, loss (lines and symbols only)
SUP = "#4E7470"      # supported / held (muted grey-green)
INK = "#33261F"      # primary text and structure
MUTED = "#776A62"
RULE = "#E3D9CF"

OBS_T = "#F8F3E7"    # 素绢白 grouping fill
INF_T = "#F8E0DA"    # light 棠梨绯
REF_T = "#EFE2D3"    # light 檀木棕
CORAL_T = "#F6DCD6"
SUP_T = "#E3ECEA"

SANS = ["Arial", "Liberation Sans"]
SERIF = ["Times New Roman", "Liberation Serif"]

FS_BODY = 7.5
FS_SMALL = 7.2
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
QA = Path(__file__).resolve().parents[1] / "qa"


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


def save(fig, stem, alignment):
    OUT.mkdir(exist_ok=True)
    QA.mkdir(exist_ok=True)
    require_matplotlib_panel_alignment(
        fig,
        json_out=QA / f"{stem}.alignment.json",
        overlay_svg=QA / f"{stem}.alignment.svg",
        tolerance_pt=1.5,
        gutter_tolerance_pt=1.5,
        strict=True,
        **alignment,
    )
    fig.savefig(OUT / f"{stem}.svg")
    fig.savefig(OUT / f"{stem}.pdf")
    fig.savefig(OUT / f"{stem}.png", dpi=600)
    plt.close(fig)

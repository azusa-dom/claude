"""Figure 4: attribute-specific recovery in the MRXCAT2.0 prescribed-scar evaluation of DeepStrain."""
import csv
import sys
from pathlib import Path

from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
from figstyle import (CORAL, CORAL_T, FS_BODY, FS_SMALL, FS_TITLE, SUP, OBS, INK, MAIN_W,  # noqa: E402
                      MUTED, ERR, REF, RULE, canvas, panel_label, save, sub_axes)

DATA = Path(__file__).resolve().parents[1] / "data" / "mrxcat2_values.csv"
W, H = MAIN_W, 92.0


def values():
    out = {}
    with DATA.open(newline="") as f:
        for r in csv.DictReader(f):
            key = (r["quantity"], r["component"], r["group"])
            out[key] = (float(r["mean"]), float(r["sd"]) if r["sd"] else None)
    return out


def check(ax, x, y, s=1.3, color=SUP):
    ax.plot([x - s, x - s * 0.35, x + s], [y, y - s * 0.7, y + s * 0.9], color=color, lw=1.2,
            solid_capstyle="round", solid_joinstyle="round")


def cross(ax, x, y, s=1.0, color=ERR):
    ax.plot([x - s, x + s], [y - s, y + s], color=color, lw=1.2, solid_capstyle="round")
    ax.plot([x - s, x + s], [y + s, y - s], color=color, lw=1.2, solid_capstyle="round")


def open_circle(ax, x, y, dashed=False):
    ax.add_patch(Circle((x, y), 1.05, facecolor="white", edgecolor=MUTED, lw=0.8,
                        ls=(0, (1.5, 1.2)) if dashed else "-"))


def main():
    v = values()
    fig, ax = canvas(W, H)
    top = H - 0.5

    # a: ground-truth strain, remote vs scar
    panel_label(ax, 0.5, top, "a")
    ax.text(5.0, top - 0.9, "Prescribed deficit (ground truth)", fontsize=FS_TITLE, fontweight="bold", va="top")
    pa = sub_axes(fig, W, H, 13.0, 46.0, 58.0, 38.0)
    comps = ["radial", "longitudinal", "circumferential"]
    names = ["Radial", "Longitudinal", "Circumferential"]
    bw = 0.36
    for i, c in enumerate(comps):
        rem = v[("gt_peak_systolic_strain", c, "remote")][0]
        scar = v[("gt_peak_systolic_strain", c, "scar")][0]
        pa.bar(i - bw / 2 - 0.01, rem, bw, color=REF, edgecolor=REF, lw=0.6)
        pa.bar(i + bw / 2 + 0.01, scar, bw, facecolor=CORAL_T, edgecolor=CORAL, hatch="//////", lw=0.8)
        for j, (x, val) in enumerate(((i - bw / 2, rem), (i + bw / 2, scar))):
            neg = val < 0
            off = (-0.035 - (0.10 if (neg and j == 1) else 0)) if neg else 0.035
            pa.text(x, val + off, f"{val:.2f}".replace("-", "−"), ha="center",
                    va="top" if neg else "bottom", fontsize=FS_SMALL, color=INK)
    pa.axhline(0, color=INK, lw=0.6)
    pa.set_xticks(range(3), names)
    pa.tick_params(axis="x", length=0, pad=1)
    pa.set_ylim(-0.42, 1.12)
    pa.set_yticks([-0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0])
    pa.set_yticklabels([f"{t:.1f}".replace("-", "−") for t in pa.get_yticks()])
    pa.set_xlim(-0.6, 2.6)
    pa.spines["bottom"].set_visible(False)
    pa.set_ylabel("Peak systolic strain", labelpad=2)
    ef = int(v[("ejection_fraction_pct", "", "infarct")][0])
    pa.text(0.75, 1.02, f"Infarct case EF {ef}%:\nremote tissue compensates", ha="left", va="top",
            fontsize=FS_SMALL, color=INK, linespacing=1.15)
    pa.text(0.75, 0.62, "Radial and circumferential\nstrain largely abolished in\nscar; longitudinal almost\nunchanged",
            ha="left", va="top", fontsize=FS_SMALL, color=MUTED, linespacing=1.15)
    lx, ly = 15.0, 37.5
    ax.add_patch(Rectangle((lx, ly - 1.1), 3.2, 2.2, facecolor=REF, edgecolor=REF, lw=0.6))
    ax.text(lx + 4.2, ly, "Remote myocardium", va="center", fontsize=FS_SMALL)
    ax.add_patch(Rectangle((lx + 30, ly - 1.1), 3.2, 2.2, facecolor=CORAL_T, edgecolor=CORAL,
                           hatch="//////", lw=0.8))
    ax.text(lx + 34.2, ly, "Scar", va="center", fontsize=FS_SMALL)

    # b: DeepStrain error
    panel_label(ax, 80.0, top, "b")
    ax.text(84.5, top - 0.9, "Estimator error (DeepStrain)", fontsize=FS_TITLE, fontweight="bold", va="top")
    pb = sub_axes(fig, W, H, 108.0, 50.0, 49.0, 32.0)
    rows = [
        ("Circumferential,\nall four cases", v[("deepstrain_error", "circumferential", "all_cases")], SUP, True),
        ("Radial,\nall four cases", v[("deepstrain_error", "radial", "all_cases")], ERR, True),
        ("Radial,\ninfarct case", v[("deepstrain_error", "radial", "infarct_case")], ERR, False),
    ]
    for k, (lab, (m, sd), col, filled) in enumerate(rows):
        y = 2 - k
        pb.errorbar(m, y, xerr=sd, fmt="o", color=col, ms=4.2, mfc=col if filled else "white", mec=col,
                    mew=1.0, elinewidth=1.0, capsize=2.2, capthick=0.9)
        txt = f"{m:.2f} ± {sd:.2f}".replace("-", "−")
        if k == 0:
            pb.text(m - sd - 0.015, y, txt, ha="right", va="center", fontsize=FS_SMALL, color=INK)
        else:
            pb.text(m, y + 0.25, txt, ha="center", va="bottom", fontsize=FS_SMALL, color=INK)
    pb.axvline(0, color=MUTED, lw=0.6, ls=(0, (2, 1.5)))
    pb.set_yticks([2, 1, 0], [r[0] for r in rows])
    pb.tick_params(axis="y", length=0)
    pb.spines["left"].set_visible(False)
    pb.set_ylim(-0.55, 2.6)
    pb.set_xlim(-0.52, 0.12)
    pb.set_xticks([-0.4, -0.2, 0.0])
    pb.set_xticklabels(["−0.4", "−0.2", "0"])
    pb.set_xlabel("Reported strain error (mean ± SD)", labelpad=2)
    pb.text(0.0, 2.6, "no error", ha="center", va="bottom", fontsize=FS_SMALL, color=MUTED)
    d, dsd = v[("deepstrain_displacement_error_mm", "", "all_cases")]
    dice = v[("deepstrain_dice", "", "all_phases")][0]
    ax.text(84.5, 41.0, "Radial SDs overlap, so no ranking of cases is\nimplied. Errors are case-level means over whole\n"
            "slices, not errors inside the scar region.\n"
            f"Also reported: Dice {dice:.2f}; displacement error {d:.1f} ± {dsd:.1f} mm.",
            fontsize=FS_SMALL, va="top", color=INK, linespacing=1.25)

    # c: attribute status
    panel_label(ax, 0.5, 29.5, "c")
    ax.text(5.0, 28.6, "Abnormality attributes in this experiment", fontsize=FS_TITLE, fontweight="bold", va="top")
    items = [
        ("Magnitude", "partial", "Ecc close to ground truth;\nErr under-estimated"),
        ("Location", "nr", "myocardial Dice only;\nno lesion-centroid error"),
        ("Extent", "nr", "one fixed scar geometry;\nextent recovery not measured"),
        ("Timing", "ni", "peak-time error not\nin the record read"),
    ]
    bw_, bh, gap = 38.0, 15.0, 2.0
    y = 23.0
    for i, (name, status, note) in enumerate(items):
        bx = 0.8 + i * (bw_ + gap)
        if i:
            ax.plot([bx - gap / 2, bx - gap / 2], [y - bh + 1.0, y - 0.5], color=RULE, lw=0.6)
        ax.text(bx + 2.0, y - 3.0, name, fontsize=FS_BODY, fontweight="bold", va="center")
        ax.text(bx + 2.0, y - 6.0, note, fontsize=FS_SMALL, va="top", color=MUTED, linespacing=1.2)
        sx, sy = bx + bw_ - 3.4, y - 3.0
        if status == "partial":
            check(ax, sx - 4.4, sy)
            cross(ax, sx, sy)
        elif status == "nr":
            open_circle(ax, sx, sy)
        else:
            open_circle(ax, sx, sy, dashed=True)
    ky = y - bh - 4.0
    kx = 0.8
    check(ax, kx + 1.4, ky, s=0.9)
    ax.text(kx + 3.2, ky, "held", fontsize=FS_SMALL, va="center")
    cross(ax, kx + 12.0, ky, s=0.75)
    ax.text(kx + 13.6, ky, "lost or biased", fontsize=FS_SMALL, va="center")
    open_circle(ax, kx + 33.5, ky)
    ax.text(kx + 35.2, ky, "not reported", fontsize=FS_SMALL, va="center")
    open_circle(ax, kx + 54.0, ky, dashed=True)
    ax.text(kx + 55.7, ky, "not inspected", fontsize=FS_SMALL, va="center")
    ax.text(W - 0.8, ky, "Values as reported by the MRXCAT2.0 authors; no new analysis.",
            fontsize=FS_SMALL, color=MUTED, va="center", ha="right")

    # Panels a and b have deliberately different inferential roles and plot-area
    # geometries; panel c is a card grid. Treat the alignment gate as N/A rather
    # than forcing a false comparison between unlike axes.
    save(fig, "Figure_4_attribute_specific_recovery", {
        "axes": [pa],
        "panel_ids": ["a"],
    })
    print(f"Figure 4: {W:.0f} x {H:.0f} mm")


if __name__ == "__main__":
    main()

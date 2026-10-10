"""Figure 4: attribute-specific recovery in the MRXCAT2.0 prescribed-scar evaluation of DeepStrain.

agarwood-scifig house style, 190 mm. Every number comes from data/mrxcat2_values.csv (each row quotes
the MRXCAT2.0 sentence it was transcribed from); Δ values are simple differences of those numbers.
Panel c glyphs only define each attribute on a reference profile (schematic, no estimate drawn).
"""
import csv
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
from scifig_common import C, T, export, num, start  # noqa: E402
from scifig import gauss  # noqa: E402

DATA = Path(__file__).resolve().parents[1] / "data" / "mrxcat2_values.csv"


def values():
    out = {}
    with DATA.open(newline="") as f:
        for r in csv.DictReader(f):
            out[(r["quantity"], r["component"], r["group"])] = (float(r["mean"]), float(r["sd"]) if r["sd"] else None)
    return out


v = values()
H = 462


def f2(x):
    return f"{x:.2f}".replace("-", "−")

fig = start(H, "Figure 4 | One focal test: slice means reported, scar attributes not",
            legend=[("reference", C.REF), ("estimate", C.INF)],
            footer=["Values as reported by the MRXCAT2.0 authors (one scar geometry, one estimator, mid-ventricular "
                    "short axis); Δ = scar − remote; not pooled.",
                    "Ecc / Err / Ell, circumferential / radial / longitudinal strain; EF, ejection fraction; "
                    "NOR, DCM, HCM: normal, dilated, hypertrophic."])

# ---- a: ground truth, remote vs scar ---------------------------------------------------------
fig.panel(20, 24, "a", "Prescribed scar: radial strain 0.95 → 0.30")
ax = fig.axes(66, 50, 296, 168, (0, 3), (-0.32, 1.08), (), [-0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0],
              ylabel="peak systolic strain (ground truth)", xaxis=False, yfmt=lambda t: f"{t:.1f}".replace("-", "−"))
fig.line(66, ax.fy(0), 362, ax.fy(0), C.INK, 0.9)
comps = [("radial", "Radial"), ("longitudinal", "Longitudinal"), ("circumferential", "Circumferential")]
bw = 30
for i, (c, name) in enumerate(comps):
    rem = v[("gt_peak_systolic_strain", c, "remote")][0]
    scar = v[("gt_peak_systolic_strain", c, "scar")][0]
    xc = ax.fx(i + 0.5)
    for j, (val, fill) in enumerate(((rem, C.REF), (scar, "url(#hatchInf)"))):
        x = xc - bw - 1 if j == 0 else xc + 1
        top, bot = (ax.fy(val), ax.fy(0)) if val >= 0 else (ax.fy(0), ax.fy(val))
        fig.rect(x, top, bw, max(bot - top, 1.6), fill, C.INF if j else "none", 0.9 if j else 0)
        ty = top - 5 if val >= 0 else bot + 13
        fig.text(x + bw / 2, ty, f2(val), T.SMALL + 0.5, 700, anchor="middle")
    fig.text(xc, ax.fy(-0.32) + 14, name, T.LABEL, anchor="middle")
    fig.text(xc, ax.fy(-0.32) + 28, f"Δ {'+' if scar - rem > 0 else ''}{f2(scar - rem)}", T.SMALL, fill=C.MUTED,
             anchor="middle")
ef = int(v[("ejection_fraction_pct", "", "infarct")][0])
fig.lines(196, 70, [f"Infarct case EF {ef}%:", "remote tissue compensates"],
          T.SMALL, fill=C.INK, leading=13.5)
fig.lines(196, 112, ["circumferential near zero in scar;", "longitudinal almost unchanged"], T.SMALL, leading=13.5)
fig.legend_items(66, 268, [("remote myocardium", "box", C.REF), ("scar", "hatch", C.INF)], gap=26)

# ---- b: DeepStrain error -----------------------------------------------------------------------
fig.col_rule(398, 6, 288)
fig.panel(410, 24, "b", "Slice-mean error: Ecc small, Err biased low")
rows = [("Ecc, all four cases", v[("deepstrain_error", "circumferential", "all_cases")], C.OBS, False),
        ("Err, all four cases", v[("deepstrain_error", "radial", "all_cases")], C.INF, False),
        ("Err, infarct case", v[("deepstrain_error", "radial", "infarct_case")], C.INF, True)]
fax = fig.forest(410, 52, 156, [(lab, m, m - sd, m + sd, col, op) for lab, (m, sd), col, op in rows],
                 xlim=(-0.5, 0.1), ticks=[-0.4, -0.2, 0], xlabel="reported strain error (mean ± SD)", row_h=30,
                 label_w=126, fmt=lambda t: num(t, 1))
for i, (lab, (m, sd), col, op) in enumerate(rows):
    yy = 52 + 18 + i * 30
    fig.text(706, yy + 4, f"{f2(m)} ± {f2(sd)}", T.SMALL + 0.5, 700)
fig.text(fax.fx(0), 48, "no error", T.SMALL, fill=C.MUTED, anchor="middle")
d, dsd = v[("deepstrain_displacement_error_mm", "", "all_cases")]
dice = v[("deepstrain_dice", "", "all_phases")][0]
fig.kv_table(410, 212, [("myocardial Dice, all phases", num(dice)),
                        ("displacement error", f"{d:.1f} ± {dsd:.1f} mm"),
                        ("EF, NOR / DCM / HCM / infarct", "51 / 34 / 41 / 49%")], w=368, row_h=17)
fig.lines(410, 270, ["Case-level means over whole slices; errors inside the scar were not reported.",
                     "No between-case test was reported, so no case ordering is implied."], T.SMALL, leading=13.5)

# ---- c: attribute status -------------------------------------------------------------------------
fig.row_rule(298)
fig.panel(20, 324, "c", "No abnormality attribute was reported at the scar's own level")
items = [
    ("Magnitude", "nr", "ΔM", ["scar-level error not reported;", "slice means: Ecc error small,", "Err under-estimated"]),
    ("Location", "nr", "Δθ", ["myocardial Dice only;", "no lesion-centroid error"]),
    ("Extent", "nr", "w", ["one fixed scar geometry;", "extent recovery not measured"]),
    ("Timing", "ni", "Δt", ["peak-time error not", "in the record read"]),
]
cw = 190
for k, (name, status, sym, note) in enumerate(items):
    x = 20 + k * cw
    if k:
        fig.col_rule(x - 8, 338, 444)
    fig.text(x, 352, name, T.SUB - 1, 700)
    fig.ring(x + cw - 30, 348, 6, C.MUTED, dashed=(status == "ni"))
    gx, gy, gw, gh = x + 2, 362, 110, 34
    fig.line(gx, gy + gh, gx + gw, gy + gh, C.RULE, 0.8)
    if name == "Timing":
        pts = [(gx + gw * i / 60, gy + gh - 1 - (gh - 4) * gauss(i / 60, 0.42, 0.14)) for i in range(61)]
    else:
        pts = [(gx + gw * i / 60, gy + gh - 1 - (gh - 4) * gauss(i / 60, 0.5, 0.11)) for i in range(61)]
    fig.path("M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts), C.REF, 1.6)
    pk = gx + gw * (0.42 if name == "Timing" else 0.5)
    if name == "Magnitude":
        fig.arrow(pk, gy + gh - 1, pk, gy + 5, C.INK, 0.9, 4)
    elif name == "Location":
        fig.line(pk, gy + gh + 4, pk, gy - 1, C.INK, 0.9, 'stroke-dasharray="3 2"')
    elif name == "Extent":
        half = gw * 0.11 * math.sqrt(2 * math.log(2))
        fig.line(pk - half, gy + gh / 2 + 1, pk + half, gy + gh / 2 + 1, C.INK, 0.9)
    else:
        fig.line(pk, gy + gh + 4, pk, gy - 1, C.INK, 0.9, 'stroke-dasharray="3 2"')
    fig.text(gx + gw + 8, gy + gh / 2 + 4, sym, T.SMALL + 0.5, 700, italic=True)
    fig.lines(x, 414, note, T.SMALL, leading=13)
fig.ring(26, H - 8, 5)
fig.text(38, H - 4, "not reported at the attribute's own (scar) level", T.SMALL, fill=C.MUTED)
fig.ring(330, H - 8, 5, dashed=True)
fig.text(342, H - 4, "not inspected in the record read", T.SMALL, fill=C.MUTED)
fig.line(560, H - 8, 578, H - 8, C.REF, 1.6)
fig.text(584, H - 4, "reference profile (schematic)", T.SMALL, fill=C.MUTED)

export(fig, "Figure_4_attribute_specific_recovery")

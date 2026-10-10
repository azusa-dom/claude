"""Figure 1 | Two-track evidence map — static SVG generator.

Writes two_track_figure.svg (vector, editable). Render to PNG with render.cjs.
Palette follows the review deck: 沈香墨 #8D6449, 素绢白 #F8F3E7, 檀木棕 #C0997F, 棠梨绯 #E7A49A.
Reported values in panels b, d and e are transcribed from the review (Tables 2–3, Figs 3–4, §4, §6.6);
panels a and c are conceptual schematics.
"""
import math
from pathlib import Path

W, H = 1800, 1105
INK, MUTED, GRID, RULE = "#33261F", "#6F625A", "#E8DFD6", "#CDBFB2"
OBS, INF, REF = "#8E857D", "#C0584A", "#7A4720"
AGAR, SANDAL, PEAR, PEAR_T, SILK, ERR = "#8D6449", "#C0997F", "#E7A49A", "#F8E0DA", "#F8F3E7", "#A33A2E"
FONT = "Helvetica, Arial, 'Liberation Sans', sans-serif"
MATH = "'Times New Roman', 'Liberation Serif', serif"  # manuscript rule: maths in Times New Roman
# modality colours for panel b (own key, shown in the panel header)
DENSE_C, TAG_C, FT_C, DL_C = "#5B3E2E", AGAR, OBS, "#4E7470"
L0, R0 = 78, 1762  # content left / right

out = []
add = out.append


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=12.5, weight=400, fill=INK, anchor="start", italic=False, extra=""):
    st = ' font-style="italic"' if italic else ""
    add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{st} {extra}>{esc(s)}</text>')


def rich(x, y, parts, size=12.5, anchor="start"):
    """parts: list of (string, weight, fill, italic)."""
    spans = "".join(
        f'<tspan font-weight="{w}" fill="{f}"{" font-style=\"italic\"" if it else ""}>{esc(s)}</tspan>' for s, w, f, it in parts)
    add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{INK}">{spans}</text>')


def vtext(x, y, s, size=12, fill=INK, weight=400, extra=""):
    add(f'<text transform="translate({x:.1f},{y:.1f}) rotate(-90)" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="middle" {extra}>{esc(s)}</text>')


def line(x1, y1, x2, y2, stroke=INK, w=1.0, extra=""):
    add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{w}" {extra}/>')


def path(d, stroke="none", w=1.0, fill="none", extra=""):
    add(f'<path d="{d}" stroke="{stroke}" stroke-width="{w}" fill="{fill}" {extra}/>')


def circle(cx, cy, r, fill="none", stroke="none", w=1.0, extra=""):
    add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" {extra}/>')


def rect(x, y, w, h, fill="none", stroke="none", sw=1.0, rx=0, extra=""):
    add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w, 0):.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')


def polyline(pts):
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def arrow(x1, y1, x2, y2, color=INK, w=1.4, head=7):
    line(x1, y1, x2, y2, color, w)
    a = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - head * math.cos(a - 0.45), y2 - head * math.sin(a - 0.45))
    p2 = (x2 - head * math.cos(a + 0.45), y2 - head * math.sin(a + 0.45))
    path(f"M{p1[0]:.1f} {p1[1]:.1f} L{x2:.1f} {y2:.1f} L{p2[0]:.1f} {p2[1]:.1f}", color, w,
         extra='stroke-linecap="round" stroke-linejoin="round"')


def annulus_path(cx, cy, R, r):
    return (f"M{cx + R} {cy} A{R} {R} 0 1 0 {cx - R} {cy} A{R} {R} 0 1 0 {cx + R} {cy} Z "
            f"M{cx + r} {cy} A{r} {r} 0 1 1 {cx - r} {cy} A{r} {r} 0 1 1 {cx + r} {cy} Z")


def wedge(cx, cy, r0, r1, a0, a1):
    p = lambda rr, a: (cx + rr * math.cos(a), cy + rr * math.sin(a))
    x0, y0 = p(r1, a0); x1, y1 = p(r1, a1); x2, y2 = p(r0, a1); x3, y3 = p(r0, a0)
    large = 1 if a1 - a0 > math.pi else 0
    return (f"M{x0:.2f} {y0:.2f} A{r1} {r1} 0 {large} 1 {x1:.2f} {y1:.2f} "
            f"L{x2:.2f} {y2:.2f} A{r0} {r0} 0 {large} 0 {x3:.2f} {y3:.2f} Z")


class Rng:
    def __init__(self, seed):
        self.s = seed

    def __call__(self):
        self.s = (self.s * 16807) % 2147483647
        return self.s / 2147483647


def gauss(x, mu, sd):
    return math.exp(-((x - mu) ** 2) / (2 * sd * sd))


def angdiff(a, b):
    return (a - b + 180) % 360 - 180


def lerp_hex(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(a[i] + (b[i] - a[i]) * t):02x}" for i in range(3))


CMAP = [(-0.25, "#4E3122"), (-0.18, AGAR), (-0.10, SANDAL), (-0.03, "#F1E4D6"), (0.0, "#FBF4EC"), (0.05, PEAR)]


def cmap(v):
    v = max(CMAP[0][0], min(CMAP[-1][0], v))
    for (v0, c0), (v1, c1) in zip(CMAP, CMAP[1:]):
        if v <= v1:
            return lerp_hex(c0, c1, (v - v0) / (v1 - v0))
    return CMAP[-1][1]


def num(v, nd=2):
    s = f"{v:.{nd}f}".rstrip("0").rstrip(".") if nd else f"{v:.0f}"
    return "0" if s in ("-0", "0") else s.replace("-", "−")


def xaxis(x, y, w, xlim, ticks, label="", fmt=num, grid_to=None, size=11):
    fx = lambda v: x + (v - xlim[0]) / (xlim[1] - xlim[0]) * w
    line(x, y, x + w, y, INK, 0.9)
    for t in ticks:
        line(fx(t), y, fx(t), y + 4, INK, 0.9)
        text(fx(t), y + 15, fmt(t), size, fill=MUTED, anchor="middle")
        if grid_to is not None:
            line(fx(t), grid_to, fx(t), y, GRID, 0.8)
    if label:
        text(x + w / 2, y + 29, label, 11.5, fill=INK, anchor="middle")
    return fx


def yaxis(x, y, h, ylim, ticks, label="", fmt=num, show=True, size=11):
    fy = lambda v: y + h - (v - ylim[0]) / (ylim[1] - ylim[0]) * h
    line(x, y, x, y + h, INK, 0.9)
    for t in ticks:
        line(x - 4, fy(t), x, fy(t), INK, 0.9)
        if show:
            text(x - 7, fy(t) + 4, fmt(t), size, fill=MUTED, anchor="end")
    if label:
        vtext(x - 36, y + h / 2, label, 11.5)
    return fy


def panel_label(x, y, letter, title):
    text(x, y, letter, 24, 700, INK)
    text(x + 24, y - 2, title, 15, 700, INK)


def subtitle(x, y, s, num_=""):
    text(x, y, s, 13.5, 700, INK)


def tick(x, y, ok=True):
    if ok:
        circle(x, y - 4, 5.5, REF)
        path(f"M{x - 2.8} {y - 4} l2 2.2 l3.6 -4.2", "#FFFFFF", 1.4, extra='stroke-linecap="round" stroke-linejoin="round"')
    else:
        circle(x, y - 4, 5.5, "#FFFFFF", stroke=MUTED, w=1.1)
        path(f"M{x - 2.4} {y - 6.4} l4.8 4.8 M{x + 2.4} {y - 6.4} l-4.8 4.8", MUTED, 1.2, extra='stroke-linecap="round"')


def failure_badge(x, y, n):
    circle(x, y, 8, INK)
    text(x, y + 4, str(n), 10.5, 700, "#FFFFFF", "middle")


def track_strip(y0, y1, label, c0, c1, gid):
    add(f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c0}"/>'
        f'<stop offset="1" stop-color="{c1}"/></linearGradient></defs>')
    rect(40, y0, 20, y1 - y0, f"url(#{gid})", rx=3)
    vtext(54.5, (y0 + y1) / 2, label, 11.5, "#FFFFFF", 700, 'letter-spacing="2.5"')


# ------------------------------------------------------------------ defs
add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">')
add("""<defs>
  <radialGradient id="mri" cx="50%" cy="48%" r="62%"><stop offset="0" stop-color="#4A3D35"/><stop offset="1" stop-color="#151010"/></radialGradient>
  <radialGradient id="pool" cx="45%" cy="40%" r="62%"><stop offset="0" stop-color="#FFFBF4"/><stop offset="1" stop-color="#CFC4B8"/></radialGradient>
  <linearGradient id="cbar" x1="0" y1="1" x2="0" y2="0">""" +
    "".join(f'<stop offset="{(v - CMAP[0][0]) / (CMAP[-1][0] - CMAP[0][0]):.3f}" stop-color="{c}"/>' for v, c in CMAP) +
    """</linearGradient>
  <linearGradient id="cellD" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8D6449"/><stop offset="1" stop-color="#5B3E2E"/></linearGradient>
  <pattern id="hatch" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="5" height="5" fill="#FFFFFF"/><line x1="0" y1="0" x2="0" y2="5" stroke="#7A4720" stroke-width="1.8"/></pattern>
  <linearGradient id="cvseg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#E7A49A"/><stop offset="1" stop-color="#E7A49A" stop-opacity="0"/></linearGradient>
</defs>""")
rect(0, 0, W, H, "#FFFFFF")

# ------------------------------------------------------------------ title + legend
text(40, 34, "Figure 1 | Two-track evidence map for regional strain from routine cine CMR", 18, 700)
line(40, 48, R0, 48, INK, 1.2)

# ================================================================== PANEL a — estimation track
AY0, AY1 = 60, 398
track_strip(AY0, AY1, "ESTIMATION TRACK", OBS, INF, "ga")
panel_label(L0, AY0 + 22, "a", "Estimation chain: cine supplies image cues; correspondence is inferred, strain is defined")
lgx = 1262
text(lgx - 8, AY0 + 21, "panel a:", 11.5, 700, INK, "end")
for lab, c in [("observed in cine", OBS), ("inferred by the estimator", INF), ("defined by convention", AGAR)]:
    circle(lgx + 5, AY0 + 17, 5, c)
    text(lgx + 14, AY0 + 21, lab, 11.5, fill=MUTED)
    lgx += 14 + len(lab) * 6.3 + 20

SY = AY0 + 50  # stage tag baseline
SX = [L0, 474, 958, 1348]
VIS = SY + 22  # top of visuals


def stage_head(x, tagtxt, color, title, badges=()):
    circle(x + 4, SY - 4, 4, color)
    text(x + 12, SY, tagtxt, 11, 700, INK, extra='letter-spacing="1.2"')
    tw = len(tagtxt) * 8.2 + 16
    for k, b in enumerate(badges):
        failure_badge(x + tw + 6 + k * 20, SY - 4, b)
    text(x, SY + 17, title, 13.5, 700)


# ---- a(i) cine frames + intensity profile
x0 = SX[0]
stage_head(x0, "1 · IMAGE FORMATION", OBS, "Cine bSSFP, mid short axis", ("I",))
rng = Rng(11)
S = 128
for k, (lab, R, r) in enumerate([("ED", 42, 29), ("ES", 39, 19)]):
    fx0, fy0 = x0 + k * (S + 6), VIS + 8
    cx, cy = fx0 + S / 2 + 6, fy0 + S / 2
    add(f'<clipPath id="fr{k}"><rect x="{fx0}" y="{fy0}" width="{S}" height="{S}" rx="4"/></clipPath>')
    add(f'<g clip-path="url(#fr{k})">')
    rect(fx0, fy0, S, S, "url(#mri)")
    add(f'<ellipse cx="{cx - R - 10:.1f}" cy="{cy - 3:.1f}" rx="{22 if k == 0 else 17}" ry="{37 if k == 0 else 32}" fill="#B9AEA3" opacity=".85"/>')
    circle(cx, cy, R, "#6E625A")
    for _ in range(60):
        a = rng() * 2 * math.pi
        rr = r + 2 + rng() * (R - r - 4)
        circle(cx + rr * math.cos(a), cy + rr * math.sin(a), 0.6 + rng() * 1.3, "#9C8F85", extra=f'opacity="{0.35 + rng() * 0.6:.2f}"')
    circle(cx, cy, r, "url(#pool)")
    for pa in (0.9, 2.2):
        circle(cx + (r - 8) * math.cos(pa), cy + (r - 8) * math.sin(pa), 3.8 if k == 0 else 3.3, "#7A6C63")
    if k == 0:
        line(cx - 2, cy, cx + R + 14, cy, "#F5D27A", 1.1, 'stroke-dasharray="3 2"')
    add("</g>")
    text(fx0 + 6, fy0 + S - 7, lab, 11, 700, "#EFE5DA")
# radial intensity profile along the dashed line (ED)
px, py, pw, ph = x0 + 2 * S + 26, VIS + 14, 68, 112
fyp = lambda v: py + ph - v * ph
xs = [i / 60 for i in range(61)]


def prof(t):  # position from blood pool (0) outwards to epicardial fat (1)
    blood = 0.92 * (1 - 1 / (1 + math.exp(-(t - 0.35) * 40)))
    myo = 0.22 * (1 / (1 + math.exp(-(t - 0.35) * 40))) * (1 - 1 / (1 + math.exp(-(t - 0.75) * 40)))
    fat = 0.55 * (1 / (1 + math.exp(-(t - 0.75) * 40)))
    return blood + myo + fat + 0.012 * math.sin(t * 47)


path(polyline([(px + t * pw, fyp(prof(t))) for t in xs]), INK, 1.4)
line(px, py + ph, px + pw, py + ph, INK, 0.9)
line(px, py, px, py + ph, INK, 0.9)
rect(px + 0.35 * pw, py, 0.40 * pw, ph, "#E7A49A", extra='opacity=".18"')
text(px + pw / 2, py + ph + 13, "radius", 10.5, fill=MUTED, anchor="middle")
vtext(px - 6, py + ph / 2, "signal", 10.5, MUTED)
text(px + 0.55 * pw, py - 3, "wall", 10.5, 700, INK, "middle")
cap_y = VIS + 172
for i, s in enumerate(["Observed: blood–myocardium borders (conspicuous),",
                       "intramural texture (weak), time. Confounders: coils,",
                       "through-plane motion, partial volume, artefact."]):
    text(x0, cap_y + i * 15, s, 11.5, fill=MUTED)

arrow(SX[0] + 362, VIS + 72, SX[1] - 10, VIS + 72, INF, 1.8)
text((SX[0] + 362 + SX[1] - 10) / 2, VIS + 90, "inferred", 11, 400, INK, "middle", italic=True)

# ---- a(ii) correspondence estimation
x0 = SX[1]
stage_head(x0, "2–3 · CORRESPONDENCE", INF, "Estimated displacement u(X, t)", ("E", "R"))
cx, cy, R, r = x0 + 70, VIS + 76, 64, 40
path(annulus_path(cx, cy, R, r), fill=PEAR_T, extra='fill-rule="evenodd" opacity=".75"')
circle(cx, cy, R, stroke=PEAR, w=1.1)
circle(cx, cy, r, stroke=PEAR, w=1.1)
TH0 = 30.0  # SVG angle (y down): lower right = inferolateral, AHA segment 11
for rr in (45, 52, 59):
    for a_deg in range(0, 360, 18):
        a = math.radians(a_deg + (rr - 45) * 0.5)
        f = 1 - 0.8 * gauss(angdiff(a_deg, TH0), 0, 24)
        ur, ut = -11 * f, 3.5 * f
        p0x, p0y = cx + rr * math.cos(a), cy + rr * math.sin(a)
        dx = ur * math.cos(a) - ut * math.sin(a)
        dy = ur * math.sin(a) + ut * math.cos(a)
        mag = math.hypot(dx, dy)
        col = lerp_hex(SANDAL, INF, min(1, mag / 11))
        if mag > 3:
            arrow(p0x, p0y, p0x + dx, p0y + dy, col, 1.1, 3.5)
        else:
            circle(p0x, p0y, 1.4, col)
# objective + families
tx = x0 + 150
add(f'<text x="{tx}" y="{VIS + 22}" font-size="14" font-style="italic" font-family="{MATH}" fill="{INK}">φ<tspan font-size="10" baseline-shift="sub">0→t</tspan> = arg min<tspan font-size="10" baseline-shift="sub">φ</tspan> 𝒟(I<tspan font-size="10" baseline-shift="sub">0</tspan>, I<tspan font-size="10" baseline-shift="sub">t</tspan> ∘ φ) <tspan fill="{INF}" font-weight="700">+ α ℛ(φ)</tspan></text>')
text(tx + 3.5, VIS + 12, "^", 10, 400, INK, "middle")
text(tx, VIS + 38, "data term does not identify the map; the prior selects", 11, fill=MUTED)
text(tx, VIS + 52, "tracking · registration · FE/biomechanics · supervised", 11, fill=MUTED)
text(tx, VIS + 66, "· self-supervised · compact basis", 11, fill=MUTED)
# non-uniqueness inset
ix, iy = tx + 2, VIS + 76
rect(ix - 4, iy, 290, 84, "#FFFFFF", stroke=RULE, sw=0.9, rx=4)
cols8 = ["#8D6449", "#C0584A", "#E7A49A", "#33261F", "#C0997F", "#A33A2E", "#7A4720", "#D88A7E"]
for k2, warp in enumerate((False, True)):
    ccx, ccy = ix + 34 + k2 * 74, iy + 40
    path(annulus_path(ccx, ccy, 25, 15), fill="#F3E9DF", extra='fill-rule="evenodd"')
    for k in range(8):
        th = k * math.pi / 4
        th2 = th + 0.5 * math.sin(th) if warp else th
        circle(ccx + 20 * math.cos(th2), ccy - 20 * math.sin(th2), 3.2, cols8[k], stroke="#fff", w=0.8)
    text(ccx, iy + 78, "θ ↦ θ" if not warp else "θ ↦ θ + a sin θ", 10, fill=MUTED, anchor="middle", italic=True)
text(ix + 71, iy + 44, "≠", 15, 700, INK, "middle")
# stretch curve λθ = 1 + a cos θ
sx0, sy0, sw_, sh_ = ix + 168, iy + 12, 106, 50
fxs = lambda v: sx0 + v / (2 * math.pi) * sw_
fys = lambda v: sy0 + sh_ - (v - 0.4) / 1.2 * sh_
line(sx0, sy0 + sh_, sx0 + sw_, sy0 + sh_, INK, 0.8)
line(sx0, sy0, sx0, sy0 + sh_, INK, 0.8)
line(sx0, fys(1), sx0 + sw_, fys(1), REF, 1.1, 'stroke-dasharray="3 2"')
path(polyline([(fxs(t / 50 * 2 * math.pi), fys(1 + 0.5 * math.cos(t / 50 * 2 * math.pi))) for t in range(51)]), INF, 1.4)
text(sx0 + sw_ / 2, sy0 - 3, "λθ = 1 + a cos θ", 10, fill=INK, anchor="middle", italic=True)
text(sx0 + sw_ / 2, iy + 78, "Dice = 1, HD = 0", 10, 700, INK, "middle")
cap_y2 = VIS + 172
text(x0, cap_y2, "Identical masks admit different material maps: contour agreement", 11.5, fill=MUTED)
text(x0, cap_y2 + 15, "cannot certify correspondence. Temporal scheme (reference, sequential,", 11.5, fill=MUTED)
text(x0, cap_y2 + 30, "groupwise) adds a further assumption.", 11.5, fill=MUTED)

arrow(SX[1] + 450, VIS + 72, SX[2] - 14, VIS + 72, AGAR, 1.8)
text((SX[1] + 450 + SX[2] - 14) / 2, VIS + 90, "differentiate", 11, 400, INK, "middle", italic=True)

# ---- a(iii) Ecc map
x0 = SX[2]
stage_head(x0, "4 · STRAIN DEFINITION", AGAR, "Green–Lagrange Ecc, pixelwise")
cx, cy, R, r = x0 + 82, VIS + 78, 64, 38
NR, NT = 6, 90
for i in range(NR):
    r0 = r + (R - r) * i / NR
    r1 = r + (R - r) * (i + 1) / NR
    endo = 1 - i / (NR - 1)
    for j in range(NT):
        a0 = 2 * math.pi * j / NT
        a1 = 2 * math.pi * (j + 1) / NT + 0.004
        ad = math.degrees((a0 + a1) / 2)
        v = -0.17 - 0.05 * endo + (0.16 + 0.04 * endo) * gauss(angdiff(ad, TH0), 0, 24)
        path(wedge(cx, cy, r0, r1, a0, a1), fill=cmap(v))
circle(cx, cy, R, stroke="#FFFFFF", w=0.8)
for k, segno in enumerate([7, 8, 9, 10, 11, 12]):
    a = math.radians(-120 + 60 * k)
    line(cx + r * math.cos(a), cy + r * math.sin(a), cx + R * math.cos(a), cy + R * math.sin(a), "#FFFFFF", 1.2)
    am = math.radians(-90 - 60 * k)
    text(cx + (R + 11) * math.cos(am), cy + (R + 11) * math.sin(am) + 4, str(segno), 10, fill=MUTED, anchor="middle")
text(cx, cy - 3, "radius =", 9.5, fill=MUTED, anchor="middle")
text(cx, cy + 10, "wall depth", 9.5, fill=MUTED, anchor="middle")
bx, by, bh = x0 + 172, VIS + 18, 118
rect(bx, by, 10, bh, "url(#cbar)", stroke=GRID, sw=0.8)
for v in (-0.2, -0.1, 0.0):
    yy = by + bh - (v - CMAP[0][0]) / (CMAP[-1][0] - CMAP[0][0]) * bh
    line(bx + 10, yy, bx + 14, yy, INK, 0.9)
    text(bx + 17, yy + 4, num(v, 1), 10.5, fill=MUTED)
text(bx - 2, by - 6, "Ecc", 11, 700, INK, italic=True)
tx = x0 + 216
for i, (k_, v_) in enumerate([("01 reference", "ED, Lagrangian"),
                              ("02 measure", "E = ½(FᵀF − I)"),
                              ("03 axes & sign", "c / r / l, signed"),
                              ("04 layer, dimension", "endo·mid·epi, 2D"),
                              ("05 derivative", "∂u/∂X, smoothing")]):
    text(tx, VIS + 24 + i * 26, k_, 10.5, fill=MUTED)
    if i == 1:
        add(f'<text x="{tx}" y="{VIS + 37 + i * 26}" font-size="12" font-style="italic" font-family="{MATH}" fill="{INK}">{v_}</text>')
    else:
        text(tx, VIS + 37 + i * 26, v_, 11, 400, INK)
text(x0, cap_y, "Ring radius is wall depth (endo inner, epi outer), not the", 11.5, fill=MUTED)
text(x0, cap_y + 15, "base→apex axis of a 17-segment bullseye; septum left.", 11.5, fill=MUTED)
text(x0, cap_y + 30, "Engineering −0.20 is GL −0.18: a definitional 0.02 gap.", 11.5, fill=MUTED)

arrow(SX[2] + 356, VIS + 72, SX[3] - 14, VIS + 72, AGAR, 1.8)
text((SX[2] + 356 + SX[3] - 14) / 2, VIS + 90, "aggregate", 11, 400, INK, "middle", italic=True)

# ---- a(iv) segmental curves + peak rule
x0 = SX[3]
stage_head(x0, "5 · REGIONAL REPORT", AGAR, "Segmental Ecc(t), mid ventricle")
ax, ay, aw, ah = x0 + 46, VIS + 8, 226, 128
ylim = (-0.25, 0.02)
fy = yaxis(ax, ay, ah, ylim, [-0.2, -0.1, 0], "Ecc", fmt=lambda v: num(v, 1))
fx = xaxis(ax, ay + ah, aw, (0, 1), [0, 0.5, 1], "normalised cycle time", fmt=lambda v: f"{v:g}")
line(fx(0), fy(0), fx(1), fy(0), GRID, 0.8, 'stroke-dasharray="3 3"')


def seg_curve(t, p, t0=0.38, sd=0.15):
    return -p * (gauss(t, t0, sd) - gauss(0, t0, sd) * (1 - t))


def seg11(t):  # focal deficit: reduced early systolic shortening, then post-systolic shortening (PSS)
    return -(0.08 * gauss(t, 0.30, 0.07) + 0.12 * gauss(t, 0.60, 0.08))


T_ES = 0.42
TS = [i / 200 for i in range(201)]
SEGS = {7: (0.205, 0.37), 8: (0.215, 0.38), 9: (0.19, 0.36), 10: (0.20, 0.39), 12: (0.18, 0.37)}
curves = {k: [seg_curve(t, p, t0) for t in TS] for k, (p, t0) in SEGS.items()}
curves[11] = [seg11(t) for t in TS]
shade = {7: "#A08470", 8: "#8D6449", 9: "#B39A86", 10: "#7A5A44", 12: "#C0A898"}
for k, ys in curves.items():
    if k != 11:
        path(polyline([(fx(t), fy(y)) for t, y in zip(TS, ys)]), shade[k], 1.2)
path(polyline([(fx(t), fy(y)) for t, y in zip(TS, curves[11])]), INF, 2.2)
line(fx(T_ES), ay, fx(T_ES), ay + ah, MUTED, 0.8, 'stroke-dasharray="2 3"')
text(fx(T_ES) + 3, ay + 9, "ES", 10, 700, MUTED)
# readouts computed from the plotted curves (so the table always matches the drawing)
i_es = round(T_ES * 200)
c11 = curves[11]
v_es = c11[i_es]
i_ps = min(range(i_es + 1), key=lambda i: c11[i])
i_pss = min(range(i_es, 201), key=lambda i: c11[i])
mean_curve = [sum(curves[k][i] for k in curves) / len(curves) for i in range(201)]
min_of_mean = min(mean_curve)
mean_of_minima = sum(min(v) for v in curves.values()) / len(curves)
for i_, mk in ((i_es, "1"), (i_ps, "2"), (i_pss, "3")):
    circle(fx(TS[i_]), fy(c11[i_]), 3.4, "#FFFFFF", INK, 1.1)
text(fx(TS[i_pss]) + 7, fy(c11[i_pss]) + 13, "seg 11", 10.5, 700, INK)
text(fx(TS[i_pss]) + 7, fy(c11[i_pss]) + 25, "focal deficit, PSS", 10, fill=MUTED)
# specifications 06–08
tx, ty = x0 + 286, VIS + 14
text(tx, ty, "06 region", 10.5, fill=MUTED)
text(tx, ty + 13, "AHA mid 7–12", 11, 400, INK)
text(tx, ty + 34, "07 temporal, seg 11", 10.5, 700, INK)
for i, (k_, v_) in enumerate([("○ at ES", v_es), ("○ peak systolic", c11[i_ps]), ("○ post-systolic", c11[i_pss])]):
    yy = ty + 51 + i * 17
    line(tx, yy - 12, tx + 124, yy - 12, GRID, 0.8)
    text(tx, yy, k_, 10.5, fill=MUTED)
    text(tx + 124, yy, num(v_), 11, 700, INK, "end")
text(tx, ty + 112, "08 aggregation order", 10.5, 700, INK)
for i, (k_, v_) in enumerate([("min of mean", min_of_mean), ("mean of minima", mean_of_minima)]):
    yy = ty + 129 + i * 17
    line(tx, yy - 12, tx + 124, yy - 12, GRID, 0.8)
    text(tx, yy, k_, 10.5, fill=MUTED)
    text(tx + 124, yy, num(v_), 11, 700, INK, "end")
text(x0, cap_y + 15, "Specifications 01–08 together define one regional estimand;", 11.5, fill=MUTED)
text(x0, cap_y + 30, "○ readouts and 08 (6 segments) are computed from the curves.", 11.5, fill=MUTED)

# failure-point key
fk_y = AY1 - 10
line(L0, fk_y - 16, R0, fk_y - 16, GRID, 0.8)
text(L0, fk_y, "Failure points, each testable on its own:", 11.5, 700, INK)
kx = L0 + 248
for n_, lab_, test_ in [("I", "input sufficiency", "re-image the same motion finer"),
                        ("E", "estimation", "vary α with images fixed"),
                        ("R", "representation", "project the known field onto the basis")]:
    failure_badge(kx + 8, fk_y - 4, n_)
    rich(kx + 21, fk_y, [(lab_, 700, INK, False), (" — " + test_, 400, MUTED, False)], 11.5)
    kx += 21 + (len(lab_) + len(test_) + 3) * 6.15 + 26

# ================================================================== PANEL b — validation track
BY0, BY1 = 414, 776
track_strip(BY0, BY1, "VALIDATION TRACK", SANDAL, REF, "gb")
panel_label(L0, BY0 + 22, "b", "Validation targets: each reference supports one claim; results as reported")
kx_ = 1070
text(kx_ - 8, BY0 + 21, "panel b:", 11.5, 700, INK, "end")
for lab, c, open_ in [("DENSE", DENSE_C, False), ("tagging", TAG_C, False), ("cine FT", FT_C, False),
                      ("cine DL", DL_C, False), ("comparator", FT_C, True)]:
    circle(kx_ + 5, BY0 + 17, 4.5, "#FFFFFF" if open_ else c, c, 1.4)
    text(kx_ + 14, BY0 + 21, lab, 11.5, fill=MUTED)
    kx_ += 14 + len(lab) * 6.4 + 18
rect(kx_, BY0 + 11, 12, 11, "url(#hatch)", rx=1.5)
text(kx_ + 17, BY0 + 21, "scar", 11.5, fill=MUTED)
CW = 316
CX = [L0 + i * (CW + 26) for i in range(5)]
HY = BY0 + 52  # header baseline


def col_head(x, title, refs, yes, no):
    rich(x, HY, [(title, 700, INK, False), ("  " + refs, 400, MUTED, False)], 13.5)
    tick(x + 5, HY + 19, True)
    text(x + 15, HY + 19, yes, 11.5, fill=INK)
    tick(x + 5, HY + 35, False)
    text(x + 15, HY + 35, "not alone: " + no, 11.5, fill=MUTED)


PY = HY + 58  # top of plots

# ---- b1 known motion: DeepStrain on MRXCAT2.0
x0 = CX[0]
col_head(x0, "Known motion", "Morales 2021; Buoso 2023", "capacity & technical error", "in-vivo accuracy")
# grouped bars: prescribed peak systolic strain
gx, gy, gw, gh = x0 + 40, PY + 12, 120, 100
text(x0, PY + 2, "prescribed peak strain (truth)", 11, 700, INK)
fyb = yaxis(gx, gy, gh, (-0.3, 1.0), [0, 0.5, 1.0], fmt=lambda v: num(v, 1))
line(gx, fyb(0), gx + gw, fyb(0), INK, 0.8)
for i, (lab, rem, scar) in enumerate([("rad", 0.95, 0.30), ("long", -0.18, -0.17), ("circ", -0.18, 0.01)]):
    bx0 = gx + 8 + i * 38
    for k, (v, c) in enumerate([(rem, REF), (scar, "url(#hatch)")]):
        y_top, y_bot = (fyb(v), fyb(0)) if v >= 0 else (fyb(0), fyb(v))
        rect(bx0 + k * 14, y_top, 12, max(y_bot - y_top, 1.2), c)
    text(bx0 + 13, gy + gh + 14, lab, 10.5, fill=MUTED, anchor="middle")
rect(gx + 6, gy + gh + 22, 8, 8, REF)
text(gx + 17, gy + gh + 30, "remote", 10.5, fill=MUTED)
rect(gx + 60, gy + gh + 22, 8, 8, "url(#hatch)")
text(gx + 71, gy + gh + 30, "scar", 10.5, fill=MUTED)
# forest: estimator error
fxx, fwx = x0 + 186, 126
text(x0 + 176, PY + 2, "DeepStrain error (mean ± SD)", 11, 700, INK)
rows = [("Ecc, 4 cases", 0.02, 0.04, DL_C), ("Err, 4 cases", -0.24, 0.21, DL_C), ("Err, infarct case", -0.20, 0.21, DL_C)]
fxe = xaxis(fxx, PY + 112, fwx, (-0.5, 0.1), [-0.4, -0.2, 0], fmt=lambda v: num(v, 1), grid_to=PY + 12)
line(fxe(0), PY + 12, fxe(0), PY + 112, INK, 1, 'stroke-dasharray="3 2"')
for i, (lab, m, s, c) in enumerate(rows):
    yy = PY + 30 + i * 30
    text(fxx + 2, yy - 8, lab, 10.5, fill=MUTED)
    line(fxe(m - s), yy, fxe(m + s), yy, c, 1.6)
    circle(fxe(m), yy, 3.6, c, stroke=c, w=1.4)
text(x0, BY1 - 26, "Dice 0.82 (lowest in thin scar) · displacement 1.0 ± 0.9 mm", 11, fill=MUTED)
text(x0, BY1 - 11, "Slice averages only: no scar-region error · infarct EF 49%", 11, fill=MUTED)

# ---- b2 paired DENSE / tagging: ICC
x0 = CX[1]
col_head(x0, "Paired DENSE / tagging", "", "material-sensitive in-vivo agreement", "ground truth (reference error)")
lx_ = x0 + 132
fxi = xaxis(lx_, PY + 178, 176, (0, 1), [0, 0.5, 1], "ICC", fmt=lambda v: num(v, 1), grid_to=PY + 2)
groups = [
    ("Militaru 2021 · cine FT vs tagging, 3 vendors", [("global LS", 0.92, 0.94, FT_C, None), ("global CS", 0.88, 0.91, FT_C, None),
                                                  ("global RS", 0.10, 0.81, FT_C, None)]),
    ("Cao 2018 · DENSE vs tagging", [("Ecc", 0.778, 0.778, DENSE_C, None)]),
    ("StrainNet (Wang 2023) vs conventional FT; ref DENSE", [("ES global Ecc", 0.87, 0.87, DL_C, 0.72), ("ES AHA segment Ecc", 0.75, 0.75, DL_C, 0.48)]),
]
yy = PY + 4
for gname, rws in groups:
    text(x0, yy + 4, gname, 10.5, 700, MUTED)
    yy += 17
    for lab, lo, hi, c, comp in rws:
        text(lx_ - 8, yy + 4, lab, 11, fill=INK, anchor="end")
        if comp is not None:
            line(fxi(comp) + 4, yy, fxi(lo) - 4, yy, GRID, 1)
            circle(fxi(comp), yy, 4.2, "#FFFFFF", stroke=FT_C, w=1.4)
            text(fxi(comp) - 7, yy + 4, num(comp), 10, fill=MUTED, anchor="end")
        if hi > lo:
            line(fxi(lo), yy, fxi(hi), yy, c, 5, 'stroke-linecap="round"')
        else:
            circle(fxi(lo), yy, 4.2, c)
        lab_v = f"{num(lo)}–{num(hi)}" if hi > lo else num(lo, 3)
        text(fxi(hi) + 8, yy + 4, lab_v, 10.5, 700, INK)
        yy += 19
    yy += 3
text(x0, BY1 - 26, "Militaru n = 61 at 3 T; StrainNet 59 cine tests, end-systolic.", 11, fill=MUTED)
text(x0, BY1 - 11, "Range = spread across vendors; ○ = comparator.", 11, fill=MUTED)

# ---- b3 precision & reconstruction
x0 = CX[2]
col_head(x0, "Precision & reconstruction", "Yoon 2023; Bell 2025", "precision at the tested scale", "accuracy — repeatable can be biased")
text(x0, PY + 2, "REGAIN vs GRAPPA, global FT strain, 95% LoA (%)", 11, 700, INK)
lx_ = x0 + 76
fxl = xaxis(lx_, PY + 98, 226, (-8, 8), [-8, -4, 0, 4, 8], fmt=lambda v: num(v, 0), grid_to=PY + 12)
line(fxl(0), PY + 12, fxl(0), PY + 98, INK, 1, 'stroke-dasharray="3 2"')
for i, (lab, lo, hi, c) in enumerate([("radial", -7, 6, FT_C), ("circ.", -2, 3, FT_C), ("long.", -3, 3, FT_C)]):
    yy = PY + 28 + i * 24
    text(lx_ - 8, yy + 4, lab, 11, fill=INK, anchor="end")
    rect(fxl(lo), yy - 6, fxl(hi) - fxl(lo), 12, c, rx=2, extra='opacity=".9"')
    text(fxl(lo) - 4, yy + 4, num(lo, 0), 10, fill=MUTED, anchor="end")
    text(fxl(hi) + 4, yy + 4, num(hi, 0), 10, fill=MUTED)
text(x0, PY + 134, "Strain-8 same-day scan–rescan: 20 volunteers × 8 protocols", 11, 700, INK)
cvx, cvy, cvw = x0 + 76, PY + 152, 160   # 20% sits left of the LoA zero line above
fxc = lambda v: cvx + v / 40 * cvw
line(cvx, cvy + 30, cvx + cvw, cvy + 30, INK, 0.9)
for t in (0, 20, 40):
    line(fxc(t), cvy + 30, fxc(t), cvy + 34, INK, 0.9)
    text(fxc(t), cvy + 45, f"{t}%", 10, fill=MUTED, anchor="middle")
text(cvx - 24, cvy + 45, "CV", 10, 700, INK, "end")
line(fxc(20), cvy - 10, fxc(20), cvy + 30, INK, 1, 'stroke-dasharray="3 2"')
for i, (lab, direction, note) in enumerate([("global", -1, "≤ 20%, fair–excellent"), ("segmental", 1, "often > 20%")]):
    yy = cvy + i * 18
    text(cvx - 8, yy + 4, lab, 11, fill=INK, anchor="end")
    arrow(fxc(20), yy, fxc(20) + direction * 40, yy, AGAR, 2.2, 6)
    if direction < 0:
        text(fxc(20) + 6, yy + 4, note, 10, fill=INK)
    else:
        text(fxc(20) + 48, yy + 4, note, 10, fill=INK)
text(x0, BY1 - 11, "Arrows mark the reported bound, not a measured CV.", 11, fill=MUTED)
text(x0, BY1 - 26, "Mean global differences near zero; radial limits widest.", 11, fill=MUTED)

# ---- b4 tissue: Kihlberg
x0 = CX[3]
col_head(x0, "Tissue (LGE)", "Kihlberg 2020", "scar-associated dysfunction", "pointwise displacement error")
text(x0, PY + 2, "segments with LGE > 50% transmural", 11, 700, INK)
text(x0, PY + 20, "AUC", 10.5, 700, MUTED)
text(x0, PY + 96, "sensitivity at 80% specificity", 10.5, 700, MUTED)
lx_ = x0 + 76
fxk = xaxis(lx_, PY + 172, 200, (0, 1), [0, 0.5, 1], "AUC · sensitivity", fmt=lambda v: num(v, 1), grid_to=PY + 14)
mods = [("DENSE", 0.87, 0.82, DENSE_C), ("tagging", 0.83, 0.71, TAG_C), ("cine FT", 0.66, 0.35, FT_C)]
for i, (lab, auc, sens, c) in enumerate(mods):
    yy = PY + 36 + i * 20
    text(lx_ - 8, yy + 4, lab, 11, fill=INK, anchor="end")
    rect(lx_, yy - 6, fxk(auc) - lx_, 12, c)
    text(fxk(auc) + 5, yy + 4, num(auc), 10.5, 700, INK)
for i, (lab, auc, sens, c) in enumerate(mods):
    yy = PY + 112 + i * 20
    text(lx_ - 8, yy + 4, lab, 11, fill=INK, anchor="end")
    rect(lx_, yy - 6, fxk(sens) - lx_, 12, c, extra='opacity=".55"')
    text(fxk(sens) + 5, yy + 4, f"{round(sens * 100)}%", 10.5, 700, INK)
line(x0, PY + 84, lx_ + 210, PY + 84, GRID, 0.8)
text(x0, BY1 - 26, "116 suspected CAD; 34 with qualifying scar.", 11, fill=MUTED)
text(x0, BY1 - 11, "Ranks scar sensitivity, not material-motion accuracy.", 11, fill=MUTED)

# ---- b5 outcome & readers
x0 = CX[4]
col_head(x0, "Outcome & readers", "Bello 2019; Masutani 2023", "prognostic / diagnostic association", "clinical utility")
text(x0, PY + 2, "discrimination (chance = 0.5)", 11, 700, INK)
lx_ = x0 + 120
fxo = xaxis(lx_, PY + 128, 176, (0.5, 1.0), [0.5, 0.75, 1.0], "C-index / AUC", fmt=lambda v: num(v), grid_to=PY + 14)
orow = [("Bello · cine DL motion", 0.75, DL_C, "survival C-index, n = 302", False),
        ("human benchmark", 0.59, FT_C, "", True),
        ("Masutani · DL strain", 0.90, DL_C, "WMA AUC vs 4 readers", False)]
for i, (lab, v, c, note, open_) in enumerate(orow):
    yy = PY + 32 + i * 30
    text(lx_ - 8, yy + 4, lab, 11, fill=INK, anchor="end")
    line(lx_, yy, fxo(v) - (4.5 if open_ else 0), yy, c, 1.6)
    circle(fxo(v), yy, 4.5, "#FFFFFF" if open_ else c, c, 1.4)
    text(fxo(v) + 8, yy + 4, f"{v:.2f}", 10.5, 700, INK)
    if note:
        text(lx_ - 8, yy + 16, note, 10, fill=MUTED, anchor="end")
text(x0, PY + 180, "C-index (survival) and AUC (classification) share a 0.5", 11, fill=MUTED)
text(x0, PY + 195, "chance level but are not directly comparable.", 11, fill=MUTED)
text(x0, BY1 - 26, "Masutani: 53 patients, 846 segments, 30% peak Err cut-off.", 11, fill=MUTED)
text(x0, BY1 - 11, "Utility also needs a decision, threshold and cost of error.", 11, fill=MUTED)

for xx in CX[1:]:
    line(xx - 13, HY - 14, xx - 13, BY1 - 4, GRID, 0.8)

# ================================================================== row c–e
CY0 = 796
line(40, CY0 - 8, R0, CY0 - 8, INK, 1.2)

# ---- c: attribute-specific error
panel_label(L0 - 38, CY0 + 18, "c", "Attribute-specific error: one attribute changes per panel; reference (solid) vs estimate (dashed)")
PW_, PH_ = 168, 112
PXS = [L0 + 22 + i * (PW_ + 34) for i in range(4)]
PYc = CY0 + 50


def deficit(theta, mu, sd, amp):
    return -0.20 + amp * gauss(theta, mu, sd)


specs = [("Magnitude", (180, 30, 0.16), (180, 30, 0.08), "ΔM"),
         ("Location", (150, 30, 0.16), (215, 30, 0.16), "Δθ"),
         ("Extent", (180, 22, 0.16), (180, 46, 0.16), "Δw")]
for i, (title, ref, est, dl) in enumerate(specs):
    x0 = PXS[i]
    text(x0, PYc - 10, title, 12.5, 700)
    fy = yaxis(x0, PYc, PH_, (-0.25, 0.0), [-0.2, -0.1, 0], "peak Ecc" if i == 0 else "", fmt=lambda v: num(v, 1), show=(i == 0))
    fx = xaxis(x0, PYc + PH_, PW_, (0, 360), [0, 180, 360], "wall position (°)", fmt=lambda v: f"{v:g}")
    path(polyline([(fx(t), fy(deficit(t, *ref))) for t in range(0, 361, 3)]), REF, 1.8)
    path(polyline([(fx(t), fy(deficit(t, *est))) for t in range(0, 361, 3)]), INF, 1.8, extra='stroke-dasharray="5 3"')
    if i == 0:
        arrow(fx(240), fy(-0.04), fx(240), fy(-0.12), INK, 1, 4)
        line(fx(186), fy(-0.04), fx(246), fy(-0.04), MUTED, 0.8, 'stroke-dasharray="2 2"')
        line(fx(186), fy(-0.12), fx(246), fy(-0.12), MUTED, 0.8, 'stroke-dasharray="2 2"')
        text(fx(252), fy(-0.075), dl, 11.5, 700, INK)
    elif i == 1:
        arrow(fx(150), fy(-0.015), fx(212), fy(-0.015), INK, 1, 4)
        text(fx(230), fy(-0.015) + 4, dl, 11.5, 700, INK)
    else:
        hw_r, hw_e = 1.1774 * 22, 1.1774 * 46          # half width at half maximum
        line(fx(180 - hw_r), fy(-0.12), fx(180 + hw_r), fy(-0.12), REF, 1.2)
        line(fx(180 - hw_e), fy(-0.128), fx(180 + hw_e), fy(-0.128), INF, 1.2)
        text(fx(180 + hw_e) + 5, fy(-0.12) + 4, dl, 11.5, 700, INK)
x0 = PXS[3]
text(x0, PYc - 10, "Timing", 12.5, 700)
fy = yaxis(x0, PYc, PH_, (-0.25, 0.0), [-0.2, -0.1, 0], show=False)
fx = xaxis(x0, PYc + PH_, PW_, (0, 1), [0, 0.5, 1], "cycle time", fmt=lambda v: f"{v:g}")
path(polyline([(fx(t / 100), fy(-0.2 * gauss(t / 100, 0.36, 0.12))) for t in range(101)]), REF, 1.8)
path(polyline([(fx(t / 100), fy(-0.2 * gauss(t / 100, 0.52, 0.12))) for t in range(101)]), INF, 1.8, extra='stroke-dasharray="5 3"')
arrow(fx(0.36), fy(-0.215), fx(0.51), fy(-0.215), INK, 1, 4)
text(fx(0.6), fy(-0.215) + 4, "Δt", 11.5, 700, INK)
# equal-mean note under c
ny = PYc + PH_ + 50
text(L0 - 14, ny, "Equal-mean test: a uniform field and a focal field can share one global mean (−0.18); recovering the mean is not a pass.", 11.5, fill=MUTED)
text(L0 - 14, ny + 15, "Report bias and LoA, localisation, extent and timing error, subject-level distributions, correlated segments.", 11.5, fill=MUTED)

# ---- d: coverage heatmap
DX = 948
line(DX - 22, CY0 + 2, DX - 22, H - 46, GRID, 0.8)
panel_label(DX, CY0 + 18, "d", "Attribute coverage, 7 studies (Table 3)")
studies = ["Gao 2014", "Wehner 2018", "Militaru 2021", "Kihlberg 2020", "StrainNet 2023", "DeepStrain / MRXCAT2.0", "Jahromi 2026"]
# coded from the current Table 3 wording: 2 direct endpoint, 1 partial / segment- or slice-level, 0 not inspected.
# DeepStrain magnitude is partial: slice averages with no scar-region error (Table 3; v10 Fig 4c).
M = [[2, 1, 0, 0], [2, 1, 0, 2], [2, 1, 0, 0], [1, 2, 0, 0], [2, 1, 0, 0], [1, 1, 0, 0], [2, 0, 0, 0]]
CWd, CHd = 52, 21
gx, gy = DX + 172, CY0 + 50
for j, a in enumerate(["M", "L", "E", "T"]):
    text(gx + j * CWd + CWd / 2, gy - 6, a, 12.5, 700, INK, "middle")
cell_fill = {2: "url(#cellD)", 1: PEAR_T, 0: "#FFFFFF"}
for i, (s, row) in enumerate(zip(studies, M)):
    yy = gy + i * CHd
    text(gx - 8, yy + CHd / 2 + 4, s, 11, fill=INK, anchor="end")
    for j, v in enumerate(row):
        rect(gx + j * CWd + 1.5, yy + 1.5, CWd - 3, CHd - 3, cell_fill[v], stroke=GRID if v == 0 else "none", sw=0.9, rx=2)
ty = gy + 7 * CHd + 6
line(gx - 166, ty - 2, gx + 4 * CWd, ty - 2, INK, 0.9)
text(gx - 8, ty + 14, "direct / 7", 11, 700, INK, "end")
for j in range(4):
    n = sum(1 for row in M if row[j] == 2)
    c = AGAR if n > 1 else ERR
    text(gx + j * CWd + CWd / 2, ty + 15, str(n), 14, 700, INK, "middle")
for k, (lab, f, st) in enumerate([("direct", "url(#cellD)", "none"), ("partial / indirect", PEAR_T, "none"), ("not inspected", "#FFFFFF", GRID)]):
    lx_ = DX + 10 + [0, 70, 192][k]
    rect(lx_, ty + 31, 12, 10, f, stroke=st, rx=1.5)
    text(lx_ + 17, ty + 40, lab, 10.5, fill=MUTED)

# ---- e: strongest validation per cited source
EX = 1384
line(EX - 22, CY0 + 2, EX - 22, H - 46, GRID, 0.8)
panel_label(EX, CY0 + 18, "e", "Strongest validation per Table S3 entry")
# counts and categories as in manuscript Fig 3 (data/table_s3_methods.csv in figures/cine-cmr-review-v10)
MASK_C, CORAL = "#B2AAA2", "#CC5F4F"
ev = [("Mask, landmark, registration or inter-method agreement", 22, MASK_C, MASK_C),
      ("Material-sensitive reference (known motion, DENSE, tagging); no focal deficit", 14, REF, REF),
      ("Downstream label: class, LGE, outcome or expert reading", 8, CORAL, CORAL),
      ("Validation data not reported", 3, "#FFFFFF", INK),
      ("Prescribed focal deficit with known motion (independent)", 1, REF, INK)]
bx, bw = EX + 4, 330
fxe = lambda v: bx + v / 25 * bw
ey = CY0 + 50
for i, (lab, n, c, edge) in enumerate(ev):
    yy = ey + i * 31
    text(bx, yy, lab, 10.5, fill=INK)
    rect(bx, yy + 5, fxe(n) - bx, 11, c, stroke=edge, sw=1.1 if edge == INK else 0, rx=1.5)
    text(fxe(n) + 6, yy + 15, str(n), 12, 700, INK)
xaxis(bx, ey + 5 * 31 + 2, bw, (0, 25), [0, 5, 10, 15, 20, 25], "entries (n = 48; manuscript Fig 3)", fmt=lambda v: f"{v:g}")

# ================================================================== footer
line(40, H - 40, R0, H - 40, INK, 1.2)
text(40, H - 22, "a, c: conceptual schematics, no study data (a5 readouts computed from the drawn curves). b, d, e: values as reported, transcribed from the manuscript (Tables 2–3, Table S3, §3.6, §4); "
     "d coded from Table 3 wording; not pooled — quantities differ.", 10.5, fill=MUTED)
text(40, H - 8, "M magnitude · L location · E extent · T timing. Ecc/Err/Ell, circumferential/radial/longitudinal strain. ES, end-systole; PSS, post-systolic shortening; FT, feature tracking; "
     "GL, Green–Lagrange; HD, Hausdorff distance; LoA, limits of agreement; WMA, wall-motion abnormality.", 10.5, fill=MUTED)

add("</svg>")
Path(__file__).with_name("two_track_figure.svg").write_text("\n".join(out), encoding="utf-8")
print("wrote two_track_figure.svg")

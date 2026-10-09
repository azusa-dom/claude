"""Figure 1 | Two-track evidence map — static SVG generator.

Writes two_track_figure.svg (vector, editable). Render to PNG with render.cjs.
Palette follows the review deck: 沈香墨 #8D6449, 素绢白 #F8F3E7, 檀木棕 #C0997F, 棠梨绯 #E7A49A.
"""
import math
from pathlib import Path

W, H = 1800, 1310
INK, MUTED, GRID = "#33261F", "#776A62", "#E6DCD2"
OBS, INF, REF = "#8E857D", "#C0584A", "#7A4720"
AGAR, SANDAL, PEAR, PEAR_T, SILK, ERR = "#8D6449", "#C0997F", "#E7A49A", "#F8E0DA", "#F8F3E7", "#A33A2E"
FONT = "Helvetica, Arial, 'Liberation Sans', sans-serif"

out = []
add = out.append


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=15, weight=400, fill=INK, anchor="start", italic=False, extra=""):
    st = ' font-style="italic"' if italic else ""
    add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{st} {extra}>{esc(s)}</text>')


def line(x1, y1, x2, y2, stroke=INK, w=1.2, extra=""):
    add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{w}" {extra}/>')


def path(d, stroke="none", w=1.2, fill="none", extra=""):
    add(f'<path d="{d}" stroke="{stroke}" stroke-width="{w}" fill="{fill}" {extra}/>')


def circle(cx, cy, r, fill="none", stroke="none", w=1.0, extra=""):
    add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" {extra}/>')


def rect(x, y, w, h, fill="none", stroke="none", sw=1.0, rx=0, extra=""):
    add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')


def polyline(pts):
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def arrow(x1, y1, x2, y2, color=INK, w=1.6, head=8):
    line(x1, y1, x2, y2, color, w)
    a = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - head * math.cos(a - 0.45), y2 - head * math.sin(a - 0.45))
    p2 = (x2 - head * math.cos(a + 0.45), y2 - head * math.sin(a + 0.45))
    path(f"M{p1[0]:.1f} {p1[1]:.1f} L{x2:.1f} {y2:.1f} L{p2[0]:.1f} {p2[1]:.1f}", color, w, extra='stroke-linecap="round" stroke-linejoin="round"')


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


# Ecc colour map: strong shortening (deep brown) -> cream (0) -> rose (stretch)
CMAP = [(-0.25, "#4E3122"), (-0.18, AGAR), (-0.10, SANDAL), (-0.03, "#F1E4D6"), (0.0, "#FBF4EC"), (0.05, PEAR)]


def cmap(v):
    v = max(CMAP[0][0], min(CMAP[-1][0], v))
    for (v0, c0), (v1, c1) in zip(CMAP, CMAP[1:]):
        if v <= v1:
            return lerp_hex(c0, c1, (v - v0) / (v1 - v0))
    return CMAP[-1][1]


def axes(x, y, w, h, xlim, ylim, xticks, yticks, xlabel="", ylabel="", xfmt=str, yfmt=str, ylabels=True):
    """Draw L-shaped axes; return data->pixel mappers."""
    fx = lambda v: x + (v - xlim[0]) / (xlim[1] - xlim[0]) * w
    fy = lambda v: y + h - (v - ylim[0]) / (ylim[1] - ylim[0]) * h
    line(x, y + h, x + w, y + h, INK, 1.1)
    line(x, y, x, y + h, INK, 1.1)
    for t in xticks:
        line(fx(t), y + h, fx(t), y + h + 5, INK, 1.1)
        text(fx(t), y + h + 20, xfmt(t), 13, fill=MUTED, anchor="middle")
    for t in yticks:
        line(x - 5, fy(t), x, fy(t), INK, 1.1)
        if ylabels:
            text(x - 9, fy(t) + 4.5, yfmt(t), 13, fill=MUTED, anchor="end")
    if xlabel:
        text(x + w / 2, y + h + 40, xlabel, 13.5, fill=INK, anchor="middle")
    if ylabel:
        add(f'<text transform="translate({x - 48:.1f},{y + h / 2:.1f}) rotate(-90)" font-size="13.5" fill="{INK}" text-anchor="middle">{ylabel}</text>')
    return fx, fy


def fmt_strain(v):
    return "0" if abs(v) < 1e-9 else f"{v:.1f}".replace("-", "−")


def panel_label(x, y, letter, title, sub=""):
    text(x, y, letter, 30, 700, INK)
    text(x + 30, y - 1, title, 19, 700, INK)
    if sub:
        text(x + 30, y + 21, sub, 14.5, 400, MUTED)


def tag(x, y, label, color):
    circle(x + 5, y - 5, 5, color)
    text(x + 15, y, label, 12.5, 700, color, extra='letter-spacing="1.4"')


# ------------------------------------------------------------------ defs
add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">')
add("""<defs>
  <radialGradient id="mri" cx="50%" cy="48%" r="62%"><stop offset="0" stop-color="#4A3D35"/><stop offset="1" stop-color="#151010"/></radialGradient>
  <radialGradient id="pool" cx="45%" cy="40%" r="62%"><stop offset="0" stop-color="#FFFBF4"/><stop offset="1" stop-color="#CFC4B8"/></radialGradient>
  <radialGradient id="lge" cx="50%" cy="50%" r="60%"><stop offset="0" stop-color="#2C2420"/><stop offset="1" stop-color="#0E0B0A"/></radialGradient>
  <linearGradient id="cbar" x1="0" y1="1" x2="0" y2="0">""" +
    "".join(f'<stop offset="{(v - CMAP[0][0]) / (CMAP[-1][0] - CMAP[0][0]):.3f}" stop-color="{c}"/>' for v, c in CMAP) +
    """</linearGradient>
  <linearGradient id="trackA" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8E857D" stop-opacity=".10"/><stop offset=".5" stop-color="#E7A49A" stop-opacity=".16"/><stop offset="1" stop-color="#C0997F" stop-opacity=".16"/></linearGradient>
  <linearGradient id="trackB" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#C0997F" stop-opacity=".16"/><stop offset="1" stop-color="#7A4720" stop-opacity=".14"/></linearGradient>
  <pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="#F8E0DA"/><line x1="0" y1="0" x2="0" y2="6" stroke="#C0584A" stroke-width="2"/></pattern>
</defs>""")
rect(0, 0, W, H, "#FFFFFF")

# ------------------------------------------------------------------ title + legend
text(60, 50, "Figure 1 | Two-track evidence map: what routine cine CMR infers, and what each reference can establish", 21, 700)
lx = 1330
for i, (lab, c) in enumerate([("observed in cine", OBS), ("inferred", INF), ("reference", REF)]):
    xx = lx + [0, 160, 260][i]
    circle(xx + 6, 44, 6, c)
    text(xx + 18, 49, lab, 14, fill=MUTED)

# ================================================================== PANEL a — estimation track
AY0, AY1 = 76, 486
rect(40, AY0, 1720, AY1 - AY0, "url(#trackA)", rx=14)
panel_label(60, AY0 + 36, "a", "Estimation track", "routine cine → inferred correspondence → defined regional strain")

STAGE_Y = AY0 + 92  # top of stage tags
stage_x = [80, 500, 920, 1320]

# ---- a(i) cine frames
x0 = stage_x[0]
tag(x0, STAGE_Y, "OBSERVED", OBS)
text(x0, STAGE_Y + 24, "Cine bSSFP, short axis", 15.5, 700)
rng = Rng(11)
for k, (lab, R, r) in enumerate([("ED", 50, 35), ("ES", 46, 23)]):
    fx0, fy0, S = x0 + k * 172, STAGE_Y + 42, 160
    cx, cy = fx0 + S / 2 + 8, fy0 + S / 2
    add(f'<clipPath id="fr{k}"><rect x="{fx0}" y="{fy0}" width="{S}" height="{S}" rx="6"/></clipPath>')
    add(f'<g clip-path="url(#fr{k})">')
    rect(fx0, fy0, S, S, "url(#mri)")
    # RV crescent (bright blood) to the image left
    add(f'<ellipse cx="{cx - R - 12:.1f}" cy="{cy - 4:.1f}" rx="{26 if k == 0 else 20}" ry="{44 if k == 0 else 38}" fill="#B9AEA3" opacity=".85"/>')
    circle(cx, cy, R, "#6E625A")
    for _ in range(70):
        a = rng() * 2 * math.pi
        rr = r + 2 + rng() * (R - r - 4)
        circle(cx + rr * math.cos(a), cy + rr * math.sin(a), 0.7 + rng() * 1.5, "#9C8F85", extra=f'opacity="{0.35 + rng() * 0.6:.2f}"')
    circle(cx, cy, r, "url(#pool)")
    for pa in (0.9, 2.2):  # papillary muscles
        circle(cx + (r - 9) * math.cos(pa), cy + (r - 9) * math.sin(pa), 4.5 if k == 0 else 4, "#7A6C63")
    add("</g>")
    text(fx0 + 8, fy0 + S - 9, lab, 13, 700, "#EFE5DA")
text(x0, STAGE_Y + 262, "Observed: borders, weak intramural texture, time", 14, fill=MUTED)

# arrow i → ii with the key caveat
arrow(stage_x[0] + 352, STAGE_Y + 122, stage_x[1] - 18, STAGE_Y + 122, INF, 2)
text((stage_x[0] + 352 + stage_x[1] - 18) / 2, STAGE_Y + 108, "inferred", 12.5, 700, INF, "middle")

# ---- a(ii) displacement field
x0 = stage_x[1]
tag(x0, STAGE_Y, "INFERRED", INF)
text(x0, STAGE_Y + 24, "Displacement field u(X, t)", 15.5, 700)
cx, cy, R, r = x0 + 120, STAGE_Y + 122, 74, 48
path(annulus_path(cx, cy, R, r), fill=PEAR_T, extra='fill-rule="evenodd" opacity=".7"')
circle(cx, cy, R, stroke=PEAR, w=1.3)
circle(cx, cy, r, stroke=PEAR, w=1.3)
TH0 = 300.0  # focal deficit centre (degrees, SVG angle)
for rr in (53, 61, 69):
    for a_deg in range(0, 360, 18):
        a = math.radians(a_deg + (rr - 53) * 0.4)
        f = 1 - 0.8 * gauss(angdiff(a_deg, TH0), 0, 24)
        ur, ut = -13 * f, 4 * f
        px, py = cx + rr * math.cos(a), cy + rr * math.sin(a)
        dx = ur * math.cos(a) - ut * math.sin(a)
        dy = ur * math.sin(a) + ut * math.cos(a)
        mag = math.hypot(dx, dy)
        col = lerp_hex(SANDAL, INF, min(1, mag / 13))
        if mag > 3.5:
            arrow(px, py, px + dx, py + dy, col, 1.3, 4)
        else:
            circle(px, py, 1.6, col)
text(x0 + 215, STAGE_Y + 70, "argmin", 14, fill=INK, italic=True)
text(x0 + 215, STAGE_Y + 90, "𝒟(I₀, Iₜ∘φ)", 14, fill=INK, italic=True)
text(x0 + 215, STAGE_Y + 110, "+ α ℛ(φ)", 14, 700, INF, italic=True)
for i, s in enumerate(["tracking", "registration", "biomechanics", "learning"]):
    text(x0 + 215, STAGE_Y + 140 + i * 17, "· " + s, 12.5, fill=MUTED)
text(x0, STAGE_Y + 262, "Prior selects among equally well-fitting fields", 14, fill=MUTED)

arrow(stage_x[1] + 340, STAGE_Y + 122, stage_x[2] - 18, STAGE_Y + 122, AGAR, 2)
text((stage_x[1] + 340 + stage_x[2] - 18) / 2, STAGE_Y + 108, "E = ½(FᵀF − I)", 12.5, 400, AGAR, "middle", italic=True)

# ---- a(iii) Ecc map (pixelwise polar)
x0 = stage_x[2]
tag(x0, STAGE_Y, "DEFINED", AGAR)
text(x0, STAGE_Y + 24, "Circumferential strain Ecc", 15.5, 700)
cx, cy, R, r = x0 + 110, STAGE_Y + 122, 74, 46
NR, NT = 6, 90
for i in range(NR):
    r0 = r + (R - r) * i / NR
    r1 = r + (R - r) * (i + 1) / NR
    endo = 1 - i / (NR - 1)  # 1 at endocardium
    for j in range(NT):
        a0 = 2 * math.pi * j / NT
        a1 = 2 * math.pi * (j + 1) / NT + 0.004
        ad = math.degrees((a0 + a1) / 2)
        base = -0.17 - 0.05 * endo
        v = base + (0.16 + 0.04 * endo) * gauss(angdiff(ad, TH0), 0, 24)
        path(wedge(cx, cy, r0, r1, a0, a1), fill=cmap(v))
circle(cx, cy, R, stroke="#FFFFFF", w=1)
# AHA mid-ventricular segment boundaries
for k in range(6):
    a = math.radians(-120 + 60 * k)
    line(cx + r * math.cos(a), cy + r * math.sin(a), cx + R * math.cos(a), cy + R * math.sin(a), "#FFFFFF", 1.4)
# colour bar
bx, by, bh = x0 + 210, STAGE_Y + 52, 140
rect(bx, by, 12, bh, "url(#cbar)", stroke=GRID, sw=0.8)
for v in (-0.2, -0.1, 0.0):
    yy = by + bh - (v - CMAP[0][0]) / (CMAP[-1][0] - CMAP[0][0]) * bh
    line(bx + 12, yy, bx + 17, yy, INK, 1)
    text(bx + 21, yy + 4.5, fmt_strain(v), 12.5, fill=MUTED)
text(bx - 2, by - 9, "Ecc", 12.5, 700, INK, italic=True)
text(x0, STAGE_Y + 262, "Pixelwise field with a focal deficit; AHA segments", 14, fill=MUTED)

arrow(stage_x[2] + 300, STAGE_Y + 122, stage_x[3] - 18, STAGE_Y + 122, AGAR, 2)
text((stage_x[2] + 300 + stage_x[3] - 18) / 2, STAGE_Y + 108, "aggregate", 12.5, 400, AGAR, "middle", italic=True)

# ---- a(iv) segmental curves
x0 = stage_x[3]
tag(x0, STAGE_Y, "DEFINED", AGAR)
text(x0, STAGE_Y + 24, "Regional report: segmental Ecc(t)", 15.5, 700)
fx, fy = axes(x0 + 58, STAGE_Y + 46, 300, 140, (0, 1), (-0.25, 0.02), [0, 0.5, 1], [-0.2, -0.1, 0],
              "normalised cycle time", "Ecc", xfmt=lambda v: f"{v:g}", yfmt=fmt_strain)
line(fx(0), fy(0), fx(1), fy(0), GRID, 1, 'stroke-dasharray="3 3"')


def seg_curve(t, p, t0=0.38, sd=0.17):
    return -p * (gauss(t, t0, sd) - gauss(0, t0, sd) * (1 - t))


peaks = [0.20, 0.215, 0.19, 0.205, 0.07, 0.18]
shades = ["#A08470", "#8D6449", "#B39A86", "#7A5A44", None, "#C0A898"]
for p, c in zip(peaks, shades):
    if c:
        path(polyline([(fx(t / 100), fy(seg_curve(t / 100, p))) for t in range(101)]), c, 1.5)
path(polyline([(fx(t / 100), fy(seg_curve(t / 100, 0.07, 0.46))) for t in range(101)]), INF, 2.6)
tp = 0.38
circle(fx(tp), fy(seg_curve(tp, 0.215)), 3.6, INK)
text(fx(tp) + 8, fy(seg_curve(tp, 0.215)) + 4, "peak", 12, fill=MUTED)
line(fx(0.6), fy(-0.052), fx(0.68), fy(-0.105), INF, 1)
text(fx(0.69), fy(-0.11), "segment 5", 12.5, 700, INF)
text(fx(0.69), fy(-0.11) + 15, "focal deficit", 12, fill=MUTED)
text(x0, STAGE_Y + 262, "Value depends on reference, layer, peak rule, aggregation", 14, fill=MUTED)

# ================================================================== bridge
BY = AY1 + 26
for xx in (stage_x[2] + 110, stage_x[3] + 200):
    line(xx, AY1 + 2, xx, BY + 36, AGAR, 1.4, 'stroke-dasharray="4 4"')
rect(700, BY - 4, 400, 32, "#FFFFFF", stroke=SANDAL, sw=1.2, rx=16)
text(900, BY + 17, "compared per attribute · per estimator · per acquisition", 13.5, 700, AGAR, "middle")
line(700, BY + 12, 300, BY + 12, SANDAL, 1.2, 'stroke-dasharray="4 4"')
line(1100, BY + 12, 1500, BY + 12, SANDAL, 1.2, 'stroke-dasharray="4 4"')

# ================================================================== PANEL b — validation track
BY0, BY1 = AY1 + 62, AY1 + 400
rect(40, BY0, 1720, BY1 - BY0, "url(#trackB)", rx=14)
panel_label(60, BY0 + 36, "b", "Validation track", "each external reference supports one kind of claim, not the others")

cols = [80, 418, 756, 1094, 1432]
VY = BY0 + 64  # top of visuals
VS = 132

# b1 known motion: prescribed scar + ground-truth field
x0 = cols[0]
cx, cy = x0 + 70, VY + VS / 2
path(annulus_path(cx, cy, 60, 38), fill="#EFE2D3", extra='fill-rule="evenodd"')
a0, a1 = math.radians(TH0 - 32), math.radians(TH0 + 32)
path(wedge(cx, cy, 38, 60, a0, a1), fill="url(#hatch)", stroke=INF, w=1.2)
for a_deg in range(0, 360, 30):
    a = math.radians(a_deg)
    f = 1 - 0.85 * gauss(angdiff(a_deg, TH0), 0, 22)
    px, py = cx + 49 * math.cos(a), cy + 49 * math.sin(a)
    if f > 0.35:
        arrow(px, py, px - 10 * f * math.cos(a), py - 10 * f * math.sin(a), REF, 1.3, 4)
text(cx + 76, cy - 18, "u* known", 13, 700, REF, italic=True)
text(cx + 76, cy + 0, "prescribed", 12.5, fill=MUTED)
text(cx + 76, cy + 16, "deficit", 12.5, fill=MUTED)

# b2 tagging / DENSE: deformed tag grid inside myocardium
x0 = cols[1]
cx, cy = x0 + 70, VY + VS / 2
add(f'<clipPath id="myo"><path d="{annulus_path(cx, cy, 60, 36)}" clip-rule="evenodd"/></clipPath>')
path(annulus_path(cx, cy, 60, 36), fill="#E9DFD4", extra='fill-rule="evenodd"')
add('<g clip-path="url(#myo)">')
for k in range(-6, 7):
    pts_v, pts_h = [], []
    for s in range(-70, 71, 4):
        # radial contraction mapping applied to a straight tag line
        for which, (X, Y) in (("v", (k * 10, s)), ("h", (s, k * 10))):
            rr = math.hypot(X, Y)
            sc = 1 - 0.10 * math.exp(-((rr - 48) / 30) ** 2)
            (pts_v if which == "v" else pts_h).append((cx + X * sc, cy + Y * sc))
    path(polyline(pts_v), "#5B3E2E", 1.6)
    path(polyline(pts_h), "#5B3E2E", 1.6)
add("</g>")
circle(cx, cy, 60, stroke=SANDAL, w=1.2)
circle(cx, cy, 36, stroke=SANDAL, w=1.2)
text(cx + 76, cy - 18, "material", 13, 700, REF)
text(cx + 76, cy + 0, "label in the", 12.5, fill=MUTED)
text(cx + 76, cy + 16, "myocardium", 12.5, fill=MUTED)

# b3 scan–rescan: Bland–Altman
x0 = cols[2]
fxb, fyb = axes(x0 + 36, VY + 6, 190, 104, (0, 1), (-1, 1), [], [], ylabels=False)
rng = Rng(5)
diffs = []
for _ in range(34):
    m = 0.08 + rng() * 0.84
    d = (rng() + rng() + rng() - 1.5) * 0.55 + 0.06
    diffs.append(d)
    circle(fxb(m), fyb(d), 2.8, SANDAL, stroke=REF, w=0.8)
mu = sum(diffs) / len(diffs)
sd = (sum((d - mu) ** 2 for d in diffs) / len(diffs)) ** 0.5
line(fxb(0), fyb(mu), fxb(1), fyb(mu), REF, 1.5)
for s in (1, -1):
    line(fxb(0), fyb(mu + s * 1.96 * sd), fxb(1), fyb(mu + s * 1.96 * sd), REF, 1.1, 'stroke-dasharray="5 4"')
text(fxb(1) + 6, fyb(mu + 1.96 * sd) + 4, "+1.96 SD", 11.5, fill=MUTED)
text(fxb(1) + 6, fyb(mu - 1.96 * sd) + 4, "−1.96 SD", 11.5, fill=MUTED)
text(fxb(0.5), VY + 128, "mean of repeats", 12, fill=MUTED, anchor="middle")
add(f'<text transform="translate({x0 + 24},{VY + 58}) rotate(-90)" font-size="12" fill="{MUTED}" text-anchor="middle">difference</text>')

# b4 LGE: bright scar in the myocardium
x0 = cols[3]
fx0, fy0, S = x0 + 6, VY, VS
add(f'<clipPath id="lgec"><rect x="{fx0}" y="{fy0}" width="{S}" height="{S}" rx="6"/></clipPath>')
add('<g clip-path="url(#lgec)">')
rect(fx0, fy0, S, S, "url(#lge)")
cx, cy = fx0 + S / 2 + 4, fy0 + S / 2
add(f'<ellipse cx="{cx - 62}" cy="{cy - 3}" rx="22" ry="40" fill="#6B5F57" opacity=".7"/>')
path(annulus_path(cx, cy, 46, 30), fill="#2A211D", extra='fill-rule="evenodd"')
circle(cx, cy, 30, "#8D8178")
path(wedge(cx, cy, 30, 41, math.radians(TH0 - 30), math.radians(TH0 + 30)), fill="#F5EDE3")
path(wedge(cx, cy, 41, 46, math.radians(TH0 - 16), math.radians(TH0 + 16)), fill="#D9CEC3")
add("</g>")
text(x0 + 150, VY + 50, "scar", 13, 700, REF)
text(x0 + 150, VY + 68, "(LGE, segment", 12.5, fill=MUTED)
text(x0 + 150, VY + 84, "transmurality)", 12.5, fill=MUTED)

# b5 outcome: Kaplan–Meier
x0 = cols[4]
fxk, fyk = axes(x0 + 36, VY + 6, 200, 104, (0, 5), (0.5, 1.0), [0, 5], [0.5, 1.0],
                xfmt=lambda v: f"{v:g} y", yfmt=lambda v: f"{v:.1f}")


def km(rate, seed):
    rg, s, t, pts = Rng(seed), 1.0, 0.0, [(0.0, 1.0)]
    while t < 5:
        t += 0.25 + rg() * 0.45
        t = min(t, 5)
        pts.append((t, s))
        s *= 1 - rate * (0.6 + rg() * 0.8)
        pts.append((t, s))
    return pts


for rate, c, lab, sd_ in ((0.012, SANDAL, "Ecc preserved", 3), (0.045, INF, "Ecc impaired", 9)):
    pts = km(rate, sd_)
    path(polyline([(fxk(t), fyk(s)) for t, s in pts]), c, 2)
text(fxk(5) + 6, fyk(0.95), "preserved", 12, fill=SANDAL)
text(fxk(5) + 6, fyk(0.78), "impaired", 12, fill=INF)
text(fxk(2.5), VY + 140, "event-free survival", 12, fill=MUTED, anchor="middle")

# b captions
CAP = [
    ("Known motion", "STRAUS · MRXCAT2.0 · phantoms", "capacity & technical error", "in-vivo accuracy"),
    ("Paired DENSE / tagging", "Militaru · Cao · Wehner · Jahromi", "material-sensitive agreement", "literal ground truth"),
    ("Scan–rescan", "Strain-8 · travelling volunteers", "precision at the tested scale", "accuracy (bias)"),
    ("Tissue (LGE)", "Kihlberg · Buss · He", "biological association", "pointwise displacement error"),
    ("Outcome", "Chadalavada · Mangion · Bello", "prognostic association", "clinical utility"),
]
for x0, (t, src, yes, no) in zip(cols, CAP):
    ty = VY + VS + 40
    text(x0, ty, t, 16, 700, INK)
    text(x0, ty + 19, src, 12.5, fill=MUTED)
    circle(x0 + 7, ty + 40, 7, REF)
    path(f"M{x0 + 3.5} {ty + 40} l2.6 2.8 l4.6 -5.4", "#FFFFFF", 1.7, extra='stroke-linecap="round" stroke-linejoin="round"')
    text(x0 + 20, ty + 45, yes, 14, 400, INK)
    circle(x0 + 7, ty + 63, 7, "#FFFFFF", stroke=INF, w=1.3)
    path(f"M{x0 + 4} {ty + 60} l6 6 M{x0 + 10} {ty + 60} l-6 6", INF, 1.5, extra='stroke-linecap="round"')
    text(x0 + 20, ty + 68, "not alone: " + no, 14, 400, INF)

# ================================================================== PANEL c — attribute-specific error
CY0 = BY1 + 52
panel_label(60, CY0, "c", "Each regional attribute fails separately", "reference (solid) vs estimate (dashed); a single mean-squared error can hide any of these")
PY, PH, PW = CY0 + 66, 150, 196
px0 = [118, 370, 622, 874]


def deficit(theta, mu, sd, amp):
    return -0.20 + amp * gauss(theta, mu, sd)


specs = [
    ("Magnitude", (180, 30, 0.16), (180, 30, 0.08), "ΔM"),
    ("Location", (150, 30, 0.16), (215, 30, 0.16), "Δθ"),
    ("Extent", (180, 22, 0.16), (180, 46, 0.10), "Δw"),
]
for i, (title, ref, est, dl) in enumerate(specs):
    x0 = px0[i]
    text(x0, PY - 14, f"{title}", 15, 700, INK)
    fx, fy = axes(x0, PY, PW, PH, (0, 360), (-0.25, 0.0), [0, 180, 360], [-0.2, -0.1, 0],
                  "position around wall (°)" if i == 1 else "", "peak Ecc" if i == 0 else "",
                  xfmt=lambda v: f"{v:g}", yfmt=fmt_strain, ylabels=(i == 0))
    path(polyline([(fx(t), fy(deficit(t, *ref))) for t in range(0, 361, 3)]), REF, 2.2)
    path(polyline([(fx(t), fy(deficit(t, *est))) for t in range(0, 361, 3)]), INF, 2.2, extra='stroke-dasharray="6 4"')
    if i == 0:
        arrow(fx(232), fy(-0.04), fx(232), fy(-0.12), INK, 1.2, 5)
        line(fx(186), fy(-0.04), fx(240), fy(-0.04), MUTED, 0.9, 'stroke-dasharray="2 2"')
        line(fx(186), fy(-0.12), fx(240), fy(-0.12), MUTED, 0.9, 'stroke-dasharray="2 2"')
        text(fx(244), fy(-0.075), dl, 13, 700, INK)
    elif i == 1:
        arrow(fx(150), fy(-0.015), fx(212), fy(-0.015), INK, 1.2, 5)
        text(fx(181), fy(-0.015) - 7, dl, 13, 700, INK, "middle")
    else:
        line(fx(180 - 26), fy(-0.12), fx(180 + 26), fy(-0.12), INK, 1.2)
        line(fx(180 - 54), fy(-0.155), fx(180 + 54), fy(-0.155), INF, 1.2)
        line(fx(200), fy(-0.12), fx(244), fy(-0.12), MUTED, 0.9, 'stroke-dasharray="2 2"')
        text(fx(248), fy(-0.12) + 5, dl, 13, 700, INK)

# timing
x0 = px0[3]
text(x0, PY - 14, "Timing", 15, 700, INK)
text(x0 + 60, PY - 14, "Ecc(t)", 13, 400, MUTED, italic=True)
fx, fy = axes(x0, PY, PW, PH, (0, 1), (-0.25, 0.0), [0, 0.5, 1], [-0.2, -0.1, 0],
              "cycle time", "", xfmt=lambda v: f"{v:g}", yfmt=fmt_strain, ylabels=False)
path(polyline([(fx(t / 100), fy(seg_curve(t / 100, 0.2, 0.36))) for t in range(101)]), REF, 2.2)
path(polyline([(fx(t / 100), fy(seg_curve(t / 100, 0.2, 0.52))) for t in range(101)]), INF, 2.2, extra='stroke-dasharray="6 4"')
arrow(fx(0.36), fy(-0.218), fx(0.51), fy(-0.218), INK, 1.2, 5)
text(fx(0.56), fy(-0.218) + 5, "Δt", 13, 700, INK)

# ================================================================== PANEL d — coverage heatmap (Table 3)
DX = 1150
panel_label(DX, CY0, "d", "Attribute coverage in 7 validation studies", "direct endpoint per attribute (review Table 3)")
studies = ["Gao 2014", "Wehner 2018", "Militaru 2021", "Kihlberg 2020", "StrainNet 2023", "DeepStrain / MRXCAT2.0", "Jahromi 2026"]
# 2 = direct endpoint, 1 = partial / indirect, 0 = not a prespecified endpoint
M = [[2, 1, 0, 0], [2, 1, 0, 2], [2, 1, 0, 0], [1, 2, 0, 0], [2, 1, 0, 0], [2, 1, 0, 0], [2, 0, 0, 0]]
CW, CH = 76, 25
gx, gy = DX + 230, CY0 + 54
for j, a in enumerate(["M", "L", "E", "T"]):
    text(gx + j * CW + CW / 2, gy - 6, a, 15, 700, AGAR, "middle")
cell_fill = {2: "url(#cellD)", 1: PEAR_T, 0: "#FFFFFF"}
add(f'<defs><linearGradient id="cellD" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{AGAR}"/><stop offset="1" stop-color="#5B3E2E"/></linearGradient></defs>')
for i, (s, row) in enumerate(zip(studies, M)):
    yy = gy + i * CH
    text(gx - 10, yy + CH / 2 + 5, s, 13.5, fill=INK, anchor="end")
    for j, v in enumerate(row):
        rect(gx + j * CW + 1.5, yy + 1.5, CW - 3, CH - 3, cell_fill[v], stroke=GRID if v == 0 else "none", sw=1, rx=3)
ty = gy + 7 * CH + 8
line(gx - 220, ty - 3, gx + 4 * CW, ty - 3, INK, 1)
text(gx - 10, ty + 18, "Direct / 7", 13.5, 700, INK, "end")
for j in range(4):
    n = sum(1 for row in M if row[j] == 2)
    bw = (CW - 14) * n / 7
    rect(gx + j * CW + 7, ty + 6, CW - 14, 6, GRID, rx=3)
    rect(gx + j * CW + 7, ty + 6, max(bw, 0.001), 6, AGAR if n > 1 else ERR, rx=3)
    text(gx + j * CW + CW / 2, ty + 32, str(n), 17, 700, AGAR if n > 1 else ERR, "middle")
ly = ty + 56
for k, (lab, f, st) in enumerate([("direct endpoint", AGAR, "none"), ("partial / indirect", PEAR_T, "none"), ("not prespecified", "#FFFFFF", GRID)]):
    lx = DX + 30 + k * 180
    rect(lx, ly - 11, 18, 13, f, stroke=st, rx=2)
    text(lx + 25, ly, lab, 13, fill=MUTED)

# ================================================================== footer note
text(60, H - 22, "Schematic panels a–c are conceptual and not study data. Panel d summarises direct endpoints reported per attribute "
     "(M magnitude, L location, E extent, T timing) in the seven paired or known-motion studies of Table 3.", 12.5, fill=MUTED)

add("</svg>")
Path(__file__).with_name("two_track_figure.svg").write_text("\n".join(out), encoding="utf-8")
print("wrote two_track_figure.svg")

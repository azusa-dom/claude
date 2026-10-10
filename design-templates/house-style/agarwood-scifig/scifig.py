"""agarwood-scifig — house style for dense, journal-grade scientific figures as editable SVG.

Palette, type scale and layout rules are documented in README.md next to this file.
Reference figure built in this style: figures/poster-hero-two-track/make_figure.py.

Minimal use:

    from scifig import Figure, C
    fig = Figure(1800, 900, print_width_mm=600)          # poster; use ~840 px for 190 mm journal width
    fig.title("Figure 2 | One-line claim of the whole figure")
    fig.panel(78, 90, "a", "Panel title that states the panel's claim")
    ax = fig.axes(130, 130, 300, 160, xlim=(0, 1), ylim=(-0.25, 0), xticks=[0, .5, 1], yticks=[-.2, -.1, 0],
                  xlabel="cycle time", ylabel="Ecc")
    ax.line(xs, ys, C.REF)
    fig.footer(["Schematic; no study data.", "Abbreviations ..."])
    fig.save("figure.svg")      # prints a print-size font audit
    fig.render_png("figure.svg", "figure.png")

All drawing happens in pixel units on a fixed canvas; nothing is auto-laid-out, so every
label position is explicit and reviewable. Text defaults to ink; data colours are for marks.
"""
from __future__ import annotations

import math
import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Sequence

HERE = Path(__file__).resolve().parent


# ----------------------------------------------------------------------------- tokens
class C:
    """Colour tokens. Roles, not decoration: keep each role's meaning across all figures."""
    # source swatches (沈香墨 / 素绢白 / 檀木棕 / 棠梨绯)
    AGAR = "#8D6449"      # 沈香墨
    SILK = "#F8F3E7"      # 素绢白 — tint fill only, never the canvas
    SANDAL = "#C0997F"    # 檀木棕
    PEAR = "#E7A49A"      # 棠梨绯
    # semantic data roles (deepened so co-occurring pairs pass CVD separation)
    OBS = "#8E857D"       # observed / input / neutral context
    INF = "#C0584A"       # inferred / estimated
    REF = "#7A4720"       # reference / validation
    CORAL = "#CC5F4F"     # secondary categorical distinction
    MASK = "#B2AAA2"      # weakest evidence class (intentional neutral)
    SUP = "#4E7470"       # supported / held — the only cool hue
    ERR = "#A33A2E"       # error / loss — lines and symbols only
    DEEP = "#5B3E2E"      # darkest brown for "direct" / strongest class
    # tints
    INF_T = "#F8E0DA"
    REF_T = "#EFE2D3"
    SUP_T = "#E3ECEA"
    # text and structure
    INK = "#33261F"
    MUTED = "#6F625A"
    GRID = "#E8DFD6"
    RULE = "#CDBFB2"
    WHITE = "#FFFFFF"


# Sequential/diverging map for a signed strain-like quantity: strong negative (deep brown)
# -> cream at 0 -> rose for positive. Re-centre by editing the stops.
CMAP_STRAIN = [(-0.25, "#4E3122"), (-0.18, C.AGAR), (-0.10, C.SANDAL), (-0.03, "#F1E4D6"),
               (0.0, "#FBF4EC"), (0.05, C.PEAR)]


class T:
    """Type scale in px on the design canvas (see README for print-size rules)."""
    TITLE = 18        # figure title, bold
    PANEL = 24        # panel letter, bold lowercase
    PANEL_TITLE = 15  # panel title, bold
    SUB = 13.5        # sub-panel title, bold
    BODY = 12.5
    CAPTION = 11.5    # muted explanatory lines under a sub-panel
    LABEL = 11        # axis/row labels
    TICK = 11
    SMALL = 10.5      # footnotes, legends, inline notes
    MIN = 10          # absolute floor on the canvas


FONT = "Helvetica, Arial, 'Liberation Sans', sans-serif"
MATH = "'Times New Roman', 'Liberation Serif', serif"   # maths in Times New Roman (manuscript rule)
PT_PER_MM = 1 / 0.3528


# ----------------------------------------------------------------------------- helpers
def esc(s: str) -> str:
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def lerp_hex(c1: str, c2: str, t: float) -> str:
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    t = max(0.0, min(1.0, t))
    return "#" + "".join(f"{round(a[i] + (b[i] - a[i]) * t):02x}" for i in range(3))


def cmap(stops, v: float) -> str:
    v = max(stops[0][0], min(stops[-1][0], v))
    for (v0, c0), (v1, c1) in zip(stops, stops[1:]):
        if v <= v1:
            return lerp_hex(c0, c1, (v - v0) / (v1 - v0))
    return stops[-1][1]


def num(v: float, nd: int = 2) -> str:
    """Compact number with a true minus sign: 0.20 -> '0.2', -0.1 -> '−0.1'."""
    s = f"{v:.{nd}f}".rstrip("0").rstrip(".") if nd else f"{v:.0f}"
    return "0" if s in ("-0", "0", "") else s.replace("-", "−")


def gauss(x: float, mu: float, sd: float) -> float:
    return math.exp(-((x - mu) ** 2) / (2 * sd * sd))


class Rng:
    """Deterministic PRNG so schematic textures/scatter are identical on every build."""

    def __init__(self, seed: int):
        self.s = seed

    def __call__(self) -> float:
        self.s = (self.s * 16807) % 2147483647
        return self.s / 2147483647


def polyline(pts: Iterable[tuple[float, float]]) -> str:
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def annulus_path(cx, cy, R, r) -> str:
    return (f"M{cx + R} {cy} A{R} {R} 0 1 0 {cx - R} {cy} A{R} {R} 0 1 0 {cx + R} {cy} Z "
            f"M{cx + r} {cy} A{r} {r} 0 1 1 {cx - r} {cy} A{r} {r} 0 1 1 {cx + r} {cy} Z")


def wedge_path(cx, cy, r0, r1, a0, a1) -> str:
    p = lambda rr, a: (cx + rr * math.cos(a), cy + rr * math.sin(a))
    x0, y0 = p(r1, a0); x1, y1 = p(r1, a1); x2, y2 = p(r0, a1); x3, y3 = p(r0, a0)
    large = 1 if a1 - a0 > math.pi else 0
    return (f"M{x0:.2f} {y0:.2f} A{r1} {r1} 0 {large} 1 {x1:.2f} {y1:.2f} "
            f"L{x2:.2f} {y2:.2f} A{r0} {r0} 0 {large} 0 {x3:.2f} {y3:.2f} Z")


# ----------------------------------------------------------------------------- axes
@dataclass
class Axes:
    fig: "Figure"
    x: float
    y: float
    w: float
    h: float
    xlim: tuple[float, float]
    ylim: tuple[float, float]

    def fx(self, v: float) -> float:
        return self.x + (v - self.xlim[0]) / (self.xlim[1] - self.xlim[0]) * self.w

    def fy(self, v: float) -> float:
        return self.y + self.h - (v - self.ylim[0]) / (self.ylim[1] - self.ylim[0]) * self.h

    def line(self, xs, ys, color=C.REF, width=1.8, dash: str | None = None):
        extra = f'stroke-dasharray="{dash}"' if dash else ""
        self.fig.path(polyline((self.fx(a), self.fy(b)) for a, b in zip(xs, ys)), color, width, extra=extra)

    def band(self, xs, lo, hi, color=C.SANDAL, opacity=0.25):
        pts = [(self.fx(a), self.fy(b)) for a, b in zip(xs, hi)] + \
              [(self.fx(a), self.fy(b)) for a, b in reversed(list(zip(xs, lo)))]
        self.fig.path(polyline(pts) + " Z", fill=color, extra=f'opacity="{opacity}"')

    def scatter(self, xs, ys, color=C.SANDAL, r=2.8, edge=C.REF, open_=False):
        for a, b in zip(xs, ys):
            self.fig.circle(self.fx(a), self.fy(b), r, C.WHITE if open_ else color, edge, 0.9)

    def hline(self, v, color=C.INK, width=1.0, dash="3 2"):
        self.fig.line(self.x, self.fy(v), self.x + self.w, self.fy(v), color, width, f'stroke-dasharray="{dash}"' if dash else "")

    def vline(self, v, color=C.INK, width=1.0, dash="3 2"):
        self.fig.line(self.fx(v), self.y, self.fx(v), self.y + self.h, color, width, f'stroke-dasharray="{dash}"' if dash else "")

    def text(self, xv, yv, s, size=T.SMALL, weight=400, fill=C.INK, anchor="start", dx=0, dy=0, italic=False):
        self.fig.text(self.fx(xv) + dx, self.fy(yv) + dy, s, size, weight, fill, anchor, italic)


# ----------------------------------------------------------------------------- figure
class Figure:
    def __init__(self, width: int, height: int, print_width_mm: float | None = None, background: str = C.WHITE,
                 margin: float = 40):
        self.W, self.H = width, height
        self.M = margin
        self.print_width_mm = print_width_mm
        self._out: list[str] = []
        self._defs: list[str] = []
        self._min_font = (1e9, "")
        self._gid = 0
        self.rect(0, 0, width, height, background)
        self._add_default_defs()

    # ---- low level -----------------------------------------------------------------
    def raw(self, s: str):
        self._out.append(s)

    def defs(self, s: str):
        self._defs.append(s)

    def uid(self, prefix="g") -> str:
        self._gid += 1
        return f"{prefix}{self._gid}"

    def _track_font(self, size: float, s: str):
        if size < self._min_font[0]:
            self._min_font = (size, str(s)[:40])

    def text(self, x, y, s, size=T.BODY, weight=400, fill=C.INK, anchor="start", italic=False, extra=""):
        self._track_font(size, s)
        st = ' font-style="italic"' if italic else ""
        self.raw(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
                 f'text-anchor="{anchor}"{st} {extra}>{esc(s)}</text>')

    def rich(self, x, y, parts: Sequence[tuple], size=T.BODY, anchor="start"):
        """parts: (text, weight, fill, italic[, baseline_shift]) — use for inline emphasis/subscripts."""
        spans = []
        for p in parts:
            s, w, f, it = p[:4]
            shift = f' baseline-shift="{p[4]}" font-size="{size * 0.74:.1f}"' if len(p) > 4 and p[4] else ""
            if shift:
                self._track_font(size * 0.74, s)
            spans.append(f'<tspan font-weight="{w}" fill="{f}"{" font-style=\"italic\"" if it else ""}{shift}>{esc(s)}</tspan>')
        self._track_font(size, "".join(p[0] for p in parts))
        self.raw(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{C.INK}">{"".join(spans)}</text>')

    def vtext(self, x, y, s, size=T.LABEL, fill=C.INK, weight=400, extra=""):
        self._track_font(size, s)
        self.raw(f'<text transform="translate({x:.1f},{y:.1f}) rotate(-90)" font-size="{size}" font-weight="{weight}" '
                 f'fill="{fill}" text-anchor="middle" {extra}>{esc(s)}</text>')

    def lines(self, x, y, rows: Sequence[str], size=T.CAPTION, fill=C.MUTED, leading=None):
        """Stacked caption lines (break lines yourself; ~60–75 characters per line)."""
        lead = leading or size * 1.3
        for i, s in enumerate(rows):
            self.text(x, y + i * lead, s, size, fill=fill)

    def line(self, x1, y1, x2, y2, stroke=C.INK, w=1.0, extra=""):
        self.raw(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{w}" {extra}/>')

    def path(self, d, stroke="none", w=1.0, fill="none", extra=""):
        self.raw(f'<path d="{d}" stroke="{stroke}" stroke-width="{w}" fill="{fill}" {extra}/>')

    def circle(self, cx, cy, r, fill="none", stroke="none", w=1.0, extra=""):
        self.raw(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" {extra}/>')

    def rect(self, x, y, w, h, fill="none", stroke="none", sw=1.0, rx=0, extra=""):
        self.raw(f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w, 0):.1f}" height="{max(h, 0):.1f}" rx="{rx}" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')

    def arrow(self, x1, y1, x2, y2, color=C.INK, w=1.4, head=7):
        self.line(x1, y1, x2, y2, color, w)
        a = math.atan2(y2 - y1, x2 - x1)
        p1 = (x2 - head * math.cos(a - 0.45), y2 - head * math.sin(a - 0.45))
        p2 = (x2 - head * math.cos(a + 0.45), y2 - head * math.sin(a + 0.45))
        self.path(f"M{p1[0]:.1f} {p1[1]:.1f} L{x2:.1f} {y2:.1f} L{p2[0]:.1f} {p2[1]:.1f}", color, w,
                  extra='stroke-linecap="round" stroke-linejoin="round"')

    def linear_gradient(self, stops: Sequence[tuple[float, str]], vertical=False, opacity=1.0) -> str:
        gid = self.uid("lg")
        xy = 'x1="0" y1="0" x2="0" y2="1"' if vertical else 'x1="0" y1="0" x2="1" y2="0"'
        st = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{opacity}"/>' for o, c in stops)
        self.defs(f'<linearGradient id="{gid}" {xy}>{st}</linearGradient>')
        return f"url(#{gid})"

    def _add_default_defs(self):
        self.defs(f'<linearGradient id="cellDirect" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{C.AGAR}"/>'
                  f'<stop offset="1" stop-color="{C.DEEP}"/></linearGradient>')
        self.defs(f'<pattern id="hatchInf" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
                  f'<rect width="6" height="6" fill="{C.INF_T}"/><line x1="0" y1="0" x2="0" y2="6" stroke="{C.INF}" stroke-width="2"/></pattern>')

    # ---- structure ----------------------------------------------------------------
    def title(self, s, x=None, y=34, rule_y=48, legend: Sequence[tuple[str, str]] = ()):
        """Figure title on the top rule; optional right-aligned semantic legend [(label, colour)]."""
        x = self.M if x is None else x
        self.text(x, y, s, T.TITLE, 700)
        if legend:
            widths = [len(lab) * 6.6 + 34 for lab, _ in legend]
            lx = self.W - self.M - sum(widths)
            for (lab, c), wdt in zip(legend, widths):
                self.circle(lx + 5, y - 5, 5, c)
                self.text(lx + 14, y - 0.5, lab, 12, fill=C.MUTED)
                lx += wdt
        self.line(self.M, rule_y, self.W - self.M, rule_y, C.INK, 1.2)

    def row_rule(self, y, x0=None, x1=None, heavy=True):
        """Ink rule between rows (heavy) or a grid hairline between columns/sections (light)."""
        self.line(self.M if x0 is None else x0, y, x1 or self.W - self.M, y, C.INK if heavy else C.GRID, 1.2 if heavy else 0.8)

    def col_rule(self, x, y0, y1):
        self.line(x, y0, x, y1, C.GRID, 0.8)

    def panel(self, x, y, letter, title):
        """Bold lowercase panel letter + a title that states the panel's claim."""
        self.text(x, y, letter, T.PANEL, 700)
        self.text(x + 24, y - 2, title, T.PANEL_TITLE, 700)

    def subtitle(self, x, y, s, refs=""):
        if refs:
            self.rich(x, y, [(s, 700, C.INK, False), ("  " + refs, 400, C.MUTED, False)], T.SUB)
        else:
            self.text(x, y, s, T.SUB, 700)

    def track_strip(self, y0, y1, label, c0, c1, x=None, w=20):
        """Narrow vertical gradient strip with a rotated caps label — marks a parallel track/row."""
        x = self.M if x is None else x
        fill = self.linear_gradient([(0, c0), (1, c1)], vertical=True)
        self.rect(x, y0, w, y1 - y0, fill, rx=3)
        self.vtext(x + w * 0.72, (y0 + y1) / 2, label, 11.5, C.WHITE, 700, 'letter-spacing="2.5"')

    def stage_tag(self, x, y, label, color):
        """Small coloured dot + spaced caps tag ('OBSERVED', 'INFERRED', ...) above a sub-panel title."""
        self.circle(x + 4, y - 4, 4, color)
        self.text(x + 12, y, label, 11, 700, C.INK, extra='letter-spacing="1.2"')
        return x + 12 + len(label) * 8.2

    def badge(self, x, y, n, color=C.INK):
        """Filled ink disc with a letter/number for a failure point; explain it once in a key line.
        Use letters (I, E, R …) when the panel already numbers its steps, so the two never collide."""
        self.circle(x, y, 8, color)
        self.text(x, y + 4, str(n), 10.5, 700, C.WHITE, "middle")

    def math(self, x, y, s, size=13, fill=C.INK, anchor="start", weight=400):
        """Italic serif maths. Use <tspan baseline-shift="sub"> via raw() for subscripts if needed."""
        self._track_font(size, s)
        self.raw(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-style="italic" font-family="{MATH}" '
                 f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{esc(s)}</text>')

    def scoped_legend(self, x, y, scope, items: Sequence[tuple[str, str]], open_last=False):
        """Legend that names its scope ('panel a:') — never put a role legend in the figure title row
        when other panels reuse the same hues for other meanings."""
        self.text(x - 8, y, scope, T.CAPTION, 700, C.INK, "end")
        for i, (lab, c) in enumerate(items):
            self.circle(x + 5, y - 4, 5, C.WHITE if (open_last and i == len(items) - 1) else c, c, 1.4)
            self.text(x + 14, y, lab, T.CAPTION, fill=C.MUTED)
            x += 14 + len(lab) * 6.3 + 20

    def check(self, x, y, s, size=T.CAPTION):
        """✓ line: what this item establishes."""
        self.circle(x + 5, y - 4, 5.5, C.REF)
        self.path(f"M{x + 2.2} {y - 4} l2 2.2 l3.6 -4.2", C.WHITE, 1.4, extra='stroke-linecap="round" stroke-linejoin="round"')
        self.text(x + 15, y, s, size)

    def cross(self, x, y, s, size=T.CAPTION):
        """✕ line: what this item does not establish on its own (muted text and symbol — red is a data role)."""
        self.circle(x + 5, y - 4, 5.5, C.WHITE, C.MUTED, 1.1)
        self.path(f"M{x + 2.6} {y - 6.4} l4.8 4.8 M{x + 7.4} {y - 6.4} l-4.8 4.8", C.MUTED, 1.2, extra='stroke-linecap="round"')
        self.text(x + 15, y, s, size, fill=C.MUTED)

    def legend_items(self, x, y, items: Sequence[tuple[str, str, str]], gap=26):
        """Inline legend; items: (label, kind, colour) with kind in {'line','dash','dot','open','box','hatch'}."""
        for lab, kind, c in items:
            if kind in ("line", "dash"):
                self.line(x, y - 4, x + 18, y - 4, c, 1.8, 'stroke-dasharray="5 3"' if kind == "dash" else "")
                tx = x + 24
            elif kind in ("dot", "open"):
                self.circle(x + 4, y - 4, 4, C.WHITE if kind == "open" else c, c, 1.4)
                tx = x + 12
            else:
                self.rect(x, y - 10, 12, 10, "url(#hatchInf)" if kind == "hatch" else c,
                          stroke=C.GRID if c == C.WHITE else "none", rx=1.5)
                tx = x + 17
            self.text(tx, y, lab, T.SMALL, fill=C.MUTED)
            x = tx + len(lab) * 6.1 + gap

    def footer(self, rows: Sequence[str], rule=True):
        """Bottom ink rule + provenance/abbreviation lines (what is schematic vs reported, sources, abbrevs)."""
        y0 = self.H - 12 - 14 * (len(rows) - 1)
        if rule:
            self.line(self.M, y0 - 18, self.W - self.M, y0 - 18, C.INK, 1.2)
        for i, s in enumerate(rows):
            self.text(self.M, y0 + i * 14, s, T.SMALL, fill=C.MUTED)

    # ---- plotting primitives ------------------------------------------------------------
    def axes(self, x, y, w, h, xlim, ylim, xticks=(), yticks=(), xlabel="", ylabel="",
             xfmt: Callable = num, yfmt: Callable = num, grid=False, show_yticklabels=True, xaxis=True, yaxis=True) -> Axes:
        """L-shaped axes (no top/right spines). Returns Axes with data→pixel mappers."""
        ax = Axes(self, x, y, w, h, tuple(xlim), tuple(ylim))
        if xaxis:
            self.line(x, y + h, x + w, y + h, C.INK, 0.9)
            for t in xticks:
                self.line(ax.fx(t), y + h, ax.fx(t), y + h + 4, C.INK, 0.9)
                self.text(ax.fx(t), y + h + 15, xfmt(t), T.TICK, fill=C.MUTED, anchor="middle")
                if grid:
                    self.line(ax.fx(t), y, ax.fx(t), y + h, C.GRID, 0.8)
            if xlabel:
                self.text(x + w / 2, y + h + 29, xlabel, T.LABEL + 0.5, anchor="middle")
        if yaxis:
            self.line(x, y, x, y + h, C.INK, 0.9)
            for t in yticks:
                self.line(x - 4, ax.fy(t), x, ax.fy(t), C.INK, 0.9)
                if show_yticklabels:
                    self.text(x - 7, ax.fy(t) + 4, yfmt(t), T.TICK, fill=C.MUTED, anchor="end")
            if ylabel:
                self.vtext(x - 36, y + h / 2, ylabel, T.LABEL + 0.5)
        return ax

    def hbars(self, x, y, w, rows: Sequence[tuple[str, float, str]], xlim, ticks, xlabel="", row_h=22, bar_h=12,
              label_w=70, fmt: Callable = num, value_fmt: Callable | None = None) -> Axes:
        """Horizontal bars with the value printed at each bar end (ink). rows: (label, value, colour)."""
        n = len(rows)
        ax0 = x + label_w
        ax = Axes(self, ax0, y, w, n * row_h, xlim, (0, 1))
        for t in ticks:
            self.line(ax.fx(t), y, ax.fx(t), y + n * row_h, C.GRID, 0.8)
        for i, (lab, v, c) in enumerate(rows):
            yy = y + i * row_h + row_h / 2
            self.text(ax0 - 8, yy + 4, lab, T.LABEL, anchor="end")
            self.rect(ax.fx(min(0, v)), yy - bar_h / 2, abs(ax.fx(v) - ax.fx(0)), bar_h, c, rx=1.5)
            self.text(ax.fx(max(0, v)) + 5, yy + 4, (value_fmt or fmt)(v), T.SMALL, 700, C.INK)
        self.axes(ax0, y, w, n * row_h, xlim, (0, 1), ticks, (), xlabel, xfmt=fmt, yaxis=False)
        return ax

    def forest(self, x, y, w, rows: Sequence[tuple], xlim, ticks, xlabel="", row_h=28, label_w=0,
               null: float | None = 0.0, fmt: Callable = num) -> Axes:
        """Point estimate ± interval rows. rows: (label, mid, lo, hi, colour, open?). Label above each row if label_w=0."""
        n = len(rows)
        h = n * row_h + 10
        ax0 = x + label_w
        ax = Axes(self, ax0, y, w, h, xlim, (0, 1))
        for t in ticks:
            self.line(ax.fx(t), y, ax.fx(t), y + h, C.GRID, 0.8)
        if null is not None:
            self.line(ax.fx(null), y, ax.fx(null), y + h, C.INK, 1, 'stroke-dasharray="3 2"')
        for i, row in enumerate(rows):
            lab, mid, lo, hi, c = row[:5]
            open_ = row[5] if len(row) > 5 else False
            yy = y + 18 + i * row_h
            if label_w:
                self.text(ax0 - 8, yy + 4, lab, T.LABEL, anchor="end")
            else:
                self.text(ax0 + 2, yy - 8, lab, T.SMALL, fill=C.MUTED)
            self.line(ax.fx(lo), yy, ax.fx(hi), yy, c, 1.6)
            self.circle(ax.fx(mid), yy, 3.6, C.WHITE if open_ else c, c, 1.4)
        self.axes(ax0, y, w, h, xlim, (0, 1), ticks, (), xlabel, xfmt=fmt, yaxis=False)
        return ax

    def range_rows(self, x, y, w, rows: Sequence[tuple], xlim, ticks, xlabel="", row_h=26, label_w=120,
                   fmt: Callable = num, cap="round") -> Axes:
        """Interval/range bars or single points per row, e.g. ICC ranges across vendors.
        rows: (label, lo, hi, colour, comparator_value_or_None, value_text_or_None)."""
        n = len(rows)
        h = n * row_h + 6
        ax0 = x + label_w
        ax = Axes(self, ax0, y, w, h, xlim, (0, 1))
        for t in ticks:
            self.line(ax.fx(t), y, ax.fx(t), y + h, C.GRID, 0.8)
        for i, (lab, lo, hi, c, comp, vt) in enumerate(rows):
            yy = y + 14 + i * row_h
            self.text(ax0 - 8, yy + 4, lab, T.LABEL, anchor="end")
            if comp is not None:  # open marker = comparator, always labelled with its value
                self.line(ax.fx(comp) + 4, yy, ax.fx(lo) - 4, yy, C.GRID, 1)
                self.circle(ax.fx(comp), yy, 4.2, C.WHITE, C.OBS, 1.4)
                self.text(ax.fx(comp) - 7, yy + 4, fmt(comp), T.MIN, fill=C.MUTED, anchor="end")
            if hi > lo:
                self.line(ax.fx(lo), yy, ax.fx(hi), yy, c, 5, f'stroke-linecap="{cap}"')
            else:
                self.circle(ax.fx(lo), yy, 4.2, c)
            label = vt if vt is not None else (f"{fmt(lo)}–{fmt(hi)}" if hi > lo else fmt(lo))
            self.text(ax.fx(max(hi, comp if comp is not None else hi)) + 8, yy + 4, label, T.SMALL, 700, C.INK)
        self.axes(ax0, y + h - 0, w, 0, xlim, (0, 1), ticks, (), xlabel, xfmt=fmt, yaxis=False)
        return ax

    def grouped_bars(self, x, y, w, h, groups: Sequence[str], series: Sequence[tuple[str, str]], values,
                     ylim, yticks, ylabel="", bar_w=12, gap=2, yfmt: Callable = num) -> Axes:
        """Vertical grouped bars around a zero line. values[g][s]."""
        ax = self.axes(x, y, w, h, (0, 1), ylim, (), yticks, "", ylabel, yfmt=yfmt, xaxis=False)
        self.line(x, ax.fy(0), x + w, ax.fy(0), C.INK, 0.8)
        gw = w / len(groups)
        for gi, g in enumerate(groups):
            total = len(series) * bar_w + (len(series) - 1) * gap
            bx = x + gi * gw + (gw - total) / 2
            for si, (_, c) in enumerate(series):
                v = values[gi][si]
                top, bot = (ax.fy(v), ax.fy(0)) if v >= 0 else (ax.fy(0), ax.fy(v))
                self.rect(bx + si * (bar_w + gap), top, bar_w, max(bot - top, 1.2), c)
            self.text(x + gi * gw + gw / 2, y + h + 14, g, T.SMALL, fill=C.MUTED, anchor="middle")
        return ax

    def heatmap(self, x, y, rows: Sequence[str], cols: Sequence[str], M, fills: dict, cell_w=52, cell_h=21,
                label_w=166, totals: Sequence[str] | None = None, totals_label=""):
        """Categorical matrix (e.g. endpoint coverage). M[i][j] keys into fills {key: (fill, stroke)}."""
        gx = x + label_w
        for j, a in enumerate(cols):
            self.text(gx + j * cell_w + cell_w / 2, y - 6, a, 12.5, 700, C.INK, "middle")
        for i, s in enumerate(rows):
            yy = y + i * cell_h
            self.text(gx - 8, yy + cell_h / 2 + 4, s, T.LABEL, anchor="end")
            for j, v in enumerate(M[i]):
                f, st = fills[v]
                self.rect(gx + j * cell_w + 1.5, yy + 1.5, cell_w - 3, cell_h - 3, f, stroke=st, sw=0.9, rx=2)
        ty = y + len(rows) * cell_h + 6
        if totals:
            self.line(gx - label_w + 6, ty - 2, gx + len(cols) * cell_w, ty - 2, C.INK, 0.9)
            self.text(gx - 8, ty + 14, totals_label, T.LABEL, 700, anchor="end")
            for j, s in enumerate(totals):
                self.text(gx + j * cell_w + cell_w / 2, ty + 15, s, 14, 700, C.INK, "middle")
        return ty + (22 if totals else 0)

    def colorbar(self, x, y, h, stops, ticks, label="", w=10, fmt: Callable = num):
        grad = self.linear_gradient([((v - stops[0][0]) / (stops[-1][0] - stops[0][0]), c) for v, c in stops], vertical=True)
        # vertical gradient runs top→bottom; flip by drawing with transform
        self.raw(f'<g transform="translate(0,{2 * y + h}) scale(1,-1)">')
        self.rect(x, y, w, h, grad, stroke=C.GRID, sw=0.8)
        self.raw("</g>")
        for v in ticks:
            yy = y + h - (v - stops[0][0]) / (stops[-1][0] - stops[0][0]) * h
            self.line(x + w, yy, x + w + 4, yy, C.INK, 0.9)
            self.text(x + w + 7, yy + 4, fmt(v), T.SMALL, fill=C.MUTED)
        if label:
            self.text(x - 2, y - 6, label, 11, 700, C.INK, italic=True)

    def kv_table(self, x, y, rows: Sequence[tuple[str, str]], w=124, row_h=19, title=""):
        """Two-column mini table with hairlines (label muted, value bold ink right-aligned)."""
        if title:
            self.text(x, y, title, T.SMALL, 700)
            y += 18
        for i, (k, v) in enumerate(rows):
            yy = y + i * row_h
            self.line(x, yy - 13, x + w, yy - 13, C.GRID, 0.8)
            self.text(x, yy, k, T.SMALL, fill=C.MUTED)
            self.text(x + w, yy, v, 11, 700, C.INK, "end")
        return y + len(rows) * row_h

    # ---- output -------------------------------------------------------------------
    def svg(self) -> str:
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.W}" height="{self.H}" '
                f'viewBox="0 0 {self.W} {self.H}" font-family="{FONT}">')
        return "\n".join([head, "<defs>", *self._defs, "</defs>", *self._out, "</svg>"])

    def audit(self) -> dict:
        """Smallest font on the canvas and its size at the intended print width."""
        size, sample = self._min_font
        res = {"min_px": size, "sample": sample}
        if self.print_width_mm:
            pt = size * self.print_width_mm / self.W * PT_PER_MM
            res["min_pt_at_print"] = round(pt, 2)
            res["ok"] = pt >= 7.0
        return res

    def save(self, path: str | os.PathLike, quiet=False) -> Path:
        p = Path(path)
        p.write_text(self.svg(), encoding="utf-8")
        import xml.dom.minidom
        xml.dom.minidom.parse(str(p))  # fail loudly on malformed SVG (e.g. unescaped text)
        if not quiet:
            a = self.audit()
            msg = f"wrote {p.name}  ({self.W}×{self.H} px; smallest text {a['min_px']} px"
            if "min_pt_at_print" in a:
                pt = a["min_pt_at_print"]
                flag = "" if pt >= 7 else ("  ⚠ below 7 pt body floor" if pt >= 6 else "  ✗ below 6 pt floor")
                msg += f" = {pt} pt at {self.print_width_mm:g} mm{flag}"
            print(msg + ")")
        return p

    @staticmethod
    def render_png(svg_path, png_path, scale=2):
        """Rasterise with headless Chromium via render.cjs (Playwright). Returns the PNG path."""
        node = shutil.which("node")
        if not node:
            raise RuntimeError("node not found; install Node + Playwright, or open the SVG in a browser and export")
        env = dict(os.environ)
        if "PW" not in env:
            root = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
            if root and Path(root, "playwright").exists():
                env["PW"] = str(Path(root, "playwright"))
        if "CHROME" not in env and Path("/opt/pw-browsers").exists():
            cand = sorted(Path("/opt/pw-browsers").glob("chromium-*/chrome-linux/chrome"))
            if cand:
                env["CHROME"] = str(cand[-1])
        subprocess.run([node, str(HERE / "render.cjs"), str(svg_path), str(png_path), str(scale)], check=True, env=env)
        return Path(png_path)

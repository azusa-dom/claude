"""Shared set-up for the v10 figures drawn in the agarwood-scifig house style.

Canvas 800 px = 190 mm double column, so 10.5 px prints at 7.0 pt (README of the house style).
Journal mode (default) leaves out the in-figure title line and footer: the captions in
captions_and_alt_text.md carry the claim, provenance and abbreviations. Set SCIFIG_TITLES=1 to
draw them (house-style poster/preview look); every script passes both texts.

    fig = start(310, "Figure 2 | ...", footer=[...])
    ... draw in local coordinates (y = 0 is the top of the content) ...
    export(fig, "Figure_2_same_contours_analytic")
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
HOUSE = REPO / "design-templates" / "house-style" / "agarwood-scifig"
if not HOUSE.exists():  # standalone copy (e.g. the manuscript's editable_sources) ships the library alongside
    HOUSE = ROOT / "house-style" / "agarwood-scifig"
sys.path.insert(0, str(HOUSE))

from scifig import C, T, Figure, num  # noqa: E402,F401

OUT = ROOT / "out"
QA = ROOT / "qa"
W = 800
WIDTH_MM = 190.0
DPI = 600
TITLES = os.environ.get("SCIFIG_TITLES") == "1"
FONT_DIR = Path("/usr/share/fonts/truetype/liberation")


@lru_cache(maxsize=None)
def _font(size: float, bold: bool):
    from PIL import ImageFont
    name = "LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf"
    return ImageFont.truetype(str(FONT_DIR / name), size=int(round(size * 20)))


def tw(s: str, size: float = T.SMALL, bold: bool = False) -> float:
    """Rendered width in px of a string (Liberation Sans = Arial/Helvetica metrics)."""
    return _font(size, bold).getlength(s) / 20


def wrap(s: str, width: float, size: float = T.SMALL, bold: bool = False) -> list[str]:
    """Greedy word wrap to a pixel width (measured, not estimated)."""
    lines, cur = [], ""
    for word in s.split():
        cand = f"{cur} {word}".strip()
        if cur and tw(cand, size, bold) > width:
            lines.append(cur)
            cur = word
        else:
            cur = cand
    return lines + ([cur] if cur else [])


class Sheet(Figure):
    """scifig Figure whose drawing coordinates start below an optional title band."""

    def __init__(self, height, title, legend=(), footer=(), width=W, width_mm=WIDTH_MM, margin=20):
        self.top = 46 if TITLES else 0
        self.bottom = (18 + 14 * len(footer)) if (TITLES and footer) else 0
        super().__init__(width, height + self.top + self.bottom, print_width_mm=width_mm, margin=margin)
        self.width_mm = width_mm
        self.footer_rows = list(footer)
        if TITLES:
            room = width - 2 * margin - tw(title, T.TITLE, True) - 24
            if sum(len(lab) * 6.6 + 34 for lab, _ in legend) > room:
                legend = ()  # no room beside the title: the panels carry their own keys
            if room < 0:
                print(f"warning: title wider than the canvas: {title}")
            self.title(title, y=26, rule_y=36, legend=legend)
        self.raw(f'<g transform="translate(0,{self.top})">')

    def rich(self, x, y, parts, size=T.BODY, anchor="start"):
        """scifig.rich, but sub/superscripts are audited against the 6 pt script floor, not the 7 pt text floor."""
        from scifig import esc
        spans = []
        for p in parts:
            s, w, f, it = p[:4]
            shift = ""
            if len(p) > 4 and p[4]:
                ssz = size * 0.8
                shift = f' baseline-shift="{p[4]}" font-size="{ssz:.1f}"'
                self.min_script = min(getattr(self, "min_script", 1e9), ssz)
            ital = ' font-style="italic"' if it else ""
            spans.append(f'<tspan font-weight="{w}" fill="{f}"{ital}{shift}>{esc(s)}</tspan>')
        self._track_font(size, "".join(p[0] for p in parts))
        self.raw(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{C.INK}">{"".join(spans)}</text>')

    def pt(self, px):
        return px * self.width_mm / self.W / 0.3528

    # ---- small marks used across the set -------------------------------------------------
    def tick(self, x, y, color=C.SUP, s=4.2, w=1.6):
        """Bare check mark centred at (x, y)."""
        self.path(f"M{x - s:.1f} {y:.1f} L{x - s * 0.3:.1f} {y + s * 0.7:.1f} L{x + s:.1f} {y - s * 0.8:.1f}", color, w,
                  extra='stroke-linecap="round" stroke-linejoin="round"')

    def xmark(self, x, y, color=C.INF, s=3.6, w=1.5):
        self.path(f"M{x - s:.1f} {y - s:.1f} L{x + s:.1f} {y + s:.1f} M{x + s:.1f} {y - s:.1f} L{x - s:.1f} {y + s:.1f}",
                  color, w, extra='stroke-linecap="round"')

    def ring(self, x, y, r=5.5, color=C.MUTED, dashed=False, w=1.2):
        self.circle(x, y, r, C.WHITE, color, w, 'stroke-dasharray="2 1.6"' if dashed else "")

    def verb(self, x, y, s, size=T.SMALL):
        """Italic muted verb written above a flow arrow."""
        self.text(x, y, s, size, fill=C.MUTED, anchor="middle", italic=True)

    def close(self):
        self.raw("</g>")
        if TITLES and self.footer_rows:
            self.footer(self.footer_rows)


def start(height, title, legend=(), footer=(), **kw) -> Sheet:
    return Sheet(height, title, legend, footer, **kw)


def _env():
    env = dict(os.environ)
    if "PW" not in env:
        root = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
        if root and Path(root, "playwright").exists():
            env["PW"] = str(Path(root, "playwright"))
    if "CHROME" not in env:
        cand = sorted(Path("/opt/pw-browsers").glob("chromium-*/chrome-linux/chrome"))
        if cand:
            env["CHROME"] = str(cand[-1])
    return env


def _exact_pdf_box(path: Path, w_mm: float, h_mm: float):
    """Chromium rounds the page to whole CSS px (~0.2 mm); trim the blank excess so the page is exact."""
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import RectangleObject

    page = PdfReader(path).pages[0]
    x0, y0, x1, y1 = (float(v) for v in page.mediabox)
    w_pt, h_pt = w_mm / 25.4 * 72, h_mm / 25.4 * 72
    box = RectangleObject([x0, y1 - h_pt, x0 + w_pt, y1])
    page.mediabox = box
    page.cropbox = box
    writer = PdfWriter()
    writer.add_page(page)
    with open(path, "wb") as fh:
        writer.write(fh)


def export(fig: Sheet, stem: str, dpi: int = DPI):
    """Write out/<stem>.svg (pt-sized, editable text), .pdf (embedded fonts) and .png (dpi stamped)."""
    from PIL import Image

    fig.close()
    OUT.mkdir(exist_ok=True)
    work = QA / "_px"
    work.mkdir(parents=True, exist_ok=True)
    px_svg = fig.save(work / f"{stem}.svg")
    a = fig.audit()
    if not a.get("ok", True):
        raise SystemExit(f"{stem}: smallest text {a['min_pt_at_print']} pt < 7 pt at {fig.width_mm} mm")
    if hasattr(fig, "min_script") and fig.pt(fig.min_script) < 6.0:
        raise SystemExit(f"{stem}: smallest script {fig.pt(fig.min_script):.2f} pt < 6 pt at {fig.width_mm} mm")
    png_w = round(fig.width_mm / 25.4 * dpi)
    node = shutil.which("node") or "node"
    subprocess.run([node, str(ROOT / "style" / "render_outputs.cjs"), str(px_svg), str(OUT / f"{stem}.pdf"),
                    str(OUT / f"{stem}.png"), str(fig.width_mm), str(png_w)], check=True, env=_env())
    _exact_pdf_box(OUT / f"{stem}.pdf", fig.width_mm, fig.width_mm * fig.H / fig.W)
    im = Image.open(OUT / f"{stem}.png")
    im.load()
    im.convert("RGB").save(OUT / f"{stem}.png", dpi=(dpi, dpi))
    # Final SVG: same drawing, physical size in pt so it inserts at 190 mm.
    pt_w = fig.width_mm / 25.4 * 72
    pt_h = pt_w * fig.H / fig.W
    svg = px_svg.read_text(encoding="utf-8").replace(
        f'width="{fig.W}" height="{fig.H}"', f'width="{pt_w:.3f}pt" height="{pt_h:.3f}pt"', 1)
    (OUT / f"{stem}.svg").write_text(svg, encoding="utf-8")
    shutil.rmtree(work, ignore_errors=True)
    print(f"{stem}: {fig.width_mm:g} x {fig.width_mm * fig.H / fig.W:.1f} mm")

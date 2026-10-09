"""Trim empty top/bottom margins and stamp PNG resolution so every export inserts at its true size.

Width is never changed (all figures stay at the 190 mm double-column width). The content
extent is measured on the 600 dpi PNG and the same crop is applied to the PDF and SVG.
"""
import re
from pathlib import Path

import numpy as np
from PIL import Image
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject

OUT = Path(__file__).resolve().parents[1] / "out"
PAD_MM = 1.2
DPI = 600
GA = "Graphical_abstract"
GA_DPI = 254  # 2600 px over a 260 mm page


def content_rows(png):
    arr = np.asarray(png.convert("L"))
    rows = np.where((arr < 245).any(axis=1))[0]
    return rows.min(), rows.max()


def crop_pdf(path, top_frac, bottom_frac):
    reader = PdfReader(path)
    page = reader.pages[0]
    x0, y0, x1, y1 = (float(v) for v in page.mediabox)
    h = y1 - y0
    box = RectangleObject([x0, y0 + bottom_frac * h, x1, y1 - top_frac * h])
    page.mediabox = box
    page.cropbox = box
    writer = PdfWriter()
    writer.add_page(page)
    with open(path, "wb") as fh:
        writer.write(fh)
    return (box[3] - box[1]) / 72 * 25.4


def crop_svg(path, top_frac, bottom_frac):
    text = path.read_text()
    start = text.index("<svg")
    end = text.index(">", start)
    head = text[start:end]
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', head).group(1).split()]
    vh = vb[3]
    new_vb = [vb[0], vb[1] + top_frac * vh, vb[2], vh * (1 - top_frac - bottom_frac)]
    head = re.sub(r'viewBox="[^"]+"', 'viewBox="' + " ".join(f"{v:.4f}" for v in new_vb) + '"', head)
    m = re.search(r'height="([0-9.]+)pt"', head)
    head = head[:m.start(1)] + f"{float(m.group(1)) * (1 - top_frac - bottom_frac):.4f}" + head[m.end(1):]
    path.write_text(text[:start] + head + text[end:])


def main():
    for png_path in sorted(OUT.glob("*.png")):
        stem = png_path.stem
        png = Image.open(png_path)
        png.load()
        if stem == GA:
            png.save(png_path, dpi=(GA_DPI, GA_DPI))
            continue
        w, h = png.size
        pad = round(PAD_MM / 25.4 * DPI)
        top_px, bottom_px = content_rows(png)
        top_cut = max(0, top_px - pad)
        bottom_cut = max(0, h - 1 - bottom_px - pad)
        png.crop((0, top_cut, w, h - bottom_cut)).save(png_path, dpi=(DPI, DPI))
        tf, bf = top_cut / h, bottom_cut / h
        height_mm = crop_pdf(OUT / f"{stem}.pdf", tf, bf)
        crop_svg(OUT / f"{stem}.svg", tf, bf)
        width_mm = w / DPI * 25.4
        print(f"{stem:46s} {width_mm:6.1f} x {height_mm:6.1f} mm  (trimmed {top_cut / DPI * 25.4:.1f} top, "
              f"{bottom_cut / DPI * 25.4:.1f} bottom)")


if __name__ == "__main__":
    main()

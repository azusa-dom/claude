"""Figure 1, poster variant: the author-supplied two-track SVG (1800 x 1105 px canvas), exported to out/poster/.

This is the poster / slide version of Figure 1 (agarwood-scifig poster variant). The manuscript uses the
journal variant drawn by src/fig1_two_track_journal.py. At 190 mm the poster's smallest text is ~3 pt, so it
is exported here for reference only and is not part of the font audit.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
from scifig_common import DPI, OUT, ROOT, WIDTH_MM, _env, _exact_pdf_box  # noqa: E402

SRC = ROOT / "src" / "Figure_1_two_track_poster.svg"
STEM = "Figure_1_two_track_evidence_map_poster"
OUT = OUT / "poster"


def main():
    from PIL import Image
    svg = SRC.read_text(encoding="utf-8")
    w, h = (float(v) for v in re.search(r'<svg[^>]*\swidth="([\d.]+)"\s+height="([\d.]+)"', svg).groups())
    h_mm = WIDTH_MM * h / w
    OUT.mkdir(parents=True, exist_ok=True)
    node = shutil.which("node") or "node"
    subprocess.run([node, str(ROOT / "style" / "render_outputs.cjs"), str(SRC), str(OUT / f"{STEM}.pdf"),
                    str(OUT / f"{STEM}.png"), str(WIDTH_MM), str(round(WIDTH_MM / 25.4 * DPI))], check=True, env=_env())
    _exact_pdf_box(OUT / f"{STEM}.pdf", WIDTH_MM, h_mm)
    im = Image.open(OUT / f"{STEM}.png")
    im.load()
    im.convert("RGB").save(OUT / f"{STEM}.png", dpi=(DPI, DPI))
    pt_w = WIDTH_MM / 25.4 * 72
    out = svg.replace(f'width="{w:g}" height="{h:g}"', f'width="{pt_w:.3f}pt" height="{pt_w * h / w:.3f}pt"', 1)
    (OUT / f"{STEM}.svg").write_text(out, encoding="utf-8")
    sizes = [float(s) for s in re.findall(r'font-size="([\d.]+)"', svg)]
    print(f"{STEM}: {WIDTH_MM:g} x {h_mm:.1f} mm; smallest text {min(sizes)} px = "
          f"{min(sizes) * WIDTH_MM / w / 0.3528:.1f} pt at {WIDTH_MM:g} mm")


if __name__ == "__main__":
    main()

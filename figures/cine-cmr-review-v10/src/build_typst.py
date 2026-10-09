"""Compile the Typst diagrams to PDF, SVG and PNG."""
import sys
from pathlib import Path

import typst

ROOT = Path(__file__).resolve().parents[1]
FONTS = ["/usr/share/fonts/truetype/liberation"]
TARGETS = {
    "fig1_measurement_chain.typ": ("Figure_1_measurement_chain", 600),
    "fig5_validation_programme.typ": ("Figure_5_validation_targets_programme", 600),
    "figS3_training_inference.typ": ("Figure_S3_training_vs_inference_controls", 600),
    "graphical_abstract.typ": ("Graphical_abstract", 254),
}


def build(name):
    stem, ppi = TARGETS[name]
    src = ROOT / "src" / name
    for fmt in ("pdf", "svg", "png"):
        out = ROOT / "out" / f"{stem}.{fmt}"
        kw = {"ppi": ppi} if fmt == "png" else {}
        typst.compile(str(src), output=str(out), root=str(ROOT), font_paths=FONTS, format=fmt, **kw)
    print(f"built {stem}")


if __name__ == "__main__":
    for n in sys.argv[1:] or TARGETS:
        if (ROOT / "src" / n).exists():
            build(n)

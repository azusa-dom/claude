"""Report rendered text sizes in every output PDF and fail on anything below the Elsevier floor.

Elsevier artwork guidance: normal lettering ~7 pt, sub/superscripts no smaller than 6 pt.
Sizes are measured at the PDF's own page size, i.e. the size printed at manuscript text width.
"""
import json
import sys
from collections import Counter
from pathlib import Path

import pdfplumber

FLOOR_PT = 6.0
# Figures knowingly below the floor at 190 mm: reported as WARN, not as a build failure.
KNOWN_UNDERSIZE = {
    "Figure_1_two_track_evidence_map": "poster-scale drawing (1800 px canvas); needs a journal-width layout",
}
OUT = Path(__file__).resolve().parents[1] / "out"
QA = Path(__file__).resolve().parents[1] / "qa"


def audit(pdf_path):
    sizes = Counter()
    small = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for ch in page.chars:
                if not ch["text"].strip():
                    continue
                # pdfminer reports glyph advance as "size" for rotated text; for 90-degree
                # rotation the font size is the bbox extent across the baseline instead.
                size = round(ch["size"] if ch["upright"] else ch["x1"] - ch["x0"], 2)
                sizes[size] += 1
                if size < FLOOR_PT:
                    small.append({"char": ch["text"], "size": size, "font": ch["fontname"]})
    return {"min_pt": min(sizes) if sizes else None, "sizes_pt": dict(sorted(sizes.items())),
            "below_floor": small}


def main():
    QA.mkdir(exist_ok=True)
    report, failed = {}, False
    for pdf in sorted(OUT.glob("*.pdf")):
        r = audit(pdf)
        report[pdf.stem] = r
        known = KNOWN_UNDERSIZE.get(pdf.stem)
        status = ("WARN" if known else "FAIL") if r["below_floor"] else "pass"
        failed |= bool(r["below_floor"]) and not known
        note = f"  ({known})" if known and r["below_floor"] else ""
        print(f"{status}  {pdf.stem:46s} min {r['min_pt']} pt{note}")
    (QA / "font-size-audit.json").write_text(json.dumps(report, indent=2, ensure_ascii=False))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()

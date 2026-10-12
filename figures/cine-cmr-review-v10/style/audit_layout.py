"""Report the layout grid of every exported figure so the set can be aligned by eye and by number.

For each out/*.svg (coordinates are canvas px): canvas size, the (x, y) of every panel letter,
the x of every column rule and the y of every row rule, the first and last text baselines, and the
bottom margin. Run after build; nothing is changed. Exit 1 when a figure breaks the shared grid:
left margin 20 px, first panel letter at y = 24, bottom margin between 4 and 14 px.
"""
import re
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "out"
GRID, INK = "#E8DFD6", "#33261F"
MARGIN, PANEL_Y = 20.0, 24.0


def audit(svg_path):
    s = svg_path.read_text(encoding="utf-8")
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s)
    W, H = float(vb.group(1)), float(vb.group(2))
    texts = re.findall(r'<text x="([\d.]+)" y="([\d.]+)" font-size="([\d.]+)"[^>]*>', s)
    letters = [(float(x), float(y)) for x, y, fs in texts if float(fs) == 24]
    ys = [float(y) for _, y, _ in texts] + [float(y) for y in re.findall(r'translate\([\d.]+,([\d.]+)\) rotate', s)]
    lines = re.findall(r'<line x1="([\d.]+)" y1="([\d.]+)" x2="([\d.]+)" y2="([\d.]+)" stroke="(#[0-9A-F]{6})" stroke-width="([\d.]+)"', s)
    col_rules = sorted({float(x1) for x1, y1, x2, y2, st, w in lines if x1 == x2 and st == GRID and float(w) == 0.8
                        and abs(float(y2) - float(y1)) > 40})
    row_rules = sorted({float(y1) for x1, y1, x2, y2, st, w in lines if y1 == y2 and st == INK and float(w) == 1.2
                        and abs(float(x2) - float(x1)) > W * 0.5})
    first_y = min(ys) if ys else None
    last_y = max(ys) if ys else None
    return {"W": W, "H": H, "letters": letters, "col_rules": col_rules, "row_rules": row_rules,
            "first_text_y": first_y, "last_text_y": last_y, "bottom_margin": H - last_y if last_y else None}


def main():
    bad = False
    for svg in sorted(OUT.glob("*.svg")):
        r = audit(svg)
        flags = []
        if r["letters"] and abs(r["letters"][0][0] - MARGIN) > 0.5:
            flags.append(f"first panel letter x={r['letters'][0][0]} (grid {MARGIN})")
        if r["letters"] and abs(r["letters"][0][1] - PANEL_Y) > 0.5 and svg.stem != "Graphical_abstract":
            flags.append(f"first panel letter y={r['letters'][0][1]} (grid {PANEL_Y})")
        if r["bottom_margin"] is not None and not (2 <= r["bottom_margin"] <= 14):
            flags.append(f"bottom margin {r['bottom_margin']:.1f} px (grid 2–14)")
        bad |= bool(flags)
        print(f"{svg.stem:46s} {r['W']:.0f}x{r['H']:.0f}  letters {[(int(x), int(y)) for x, y in r['letters']]}  "
              f"cols {[int(c) for c in r['col_rules']]}  rows {[int(c) for c in r['row_rules']]}  "
              f"bottom {r['bottom_margin']:.1f}" + (f"  <- {'; '.join(flags)}" if flags else ""))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()

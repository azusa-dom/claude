"""Write qa/contact-sheet.png: every exported figure, scaled to a common width, stacked in two columns."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ORDER = ["Figure_1_two_track_evidence_map", "Figure_2_same_contours_analytic", "Figure_3_method_timeline",
         "Figure_4_attribute_specific_recovery", "Figure_5_validation_targets_programme", "Graphical_abstract",
         "Figure_S1_strain_definition_traps", "Figure_S2_error_attributes_mapping_validity",
         "Figure_S3_training_vs_inference_controls"]
COL_W, GAP, LABEL = 1400, 40, 34


def main():
    font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 24)
    tiles = []
    for stem in ORDER:
        im = Image.open(ROOT / "out" / f"{stem}.png").convert("RGB")
        im = im.resize((COL_W, round(im.height * COL_W / im.width)), Image.LANCZOS)
        tiles.append((stem, im))
    cols, heights = [[], []], [0, 0]
    for t in tiles:
        k = heights.index(min(heights))
        cols[k].append(t)
        heights[k] += t[1].height + LABEL + GAP
    sheet = Image.new("RGB", (2 * COL_W + 3 * GAP, max(heights) + GAP), "white")
    d = ImageDraw.Draw(sheet)
    for k, col in enumerate(cols):
        x, y = GAP + k * (COL_W + GAP), GAP
        for stem, im in col:
            d.text((x, y), stem, fill="#33261F", font=font)
            sheet.paste(im, (x, y + LABEL))
            d.rectangle([x - 1, y + LABEL - 1, x + im.width, y + LABEL + im.height], outline="#CDBFB2")
            y += im.height + LABEL + GAP
    (ROOT / "qa").mkdir(exist_ok=True)
    sheet.save(ROOT / "qa" / "contact-sheet.png")
    print(f"wrote qa/contact-sheet.png ({sheet.width} x {sheet.height})")


if __name__ == "__main__":
    main()

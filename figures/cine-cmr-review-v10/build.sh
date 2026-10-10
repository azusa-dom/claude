#!/usr/bin/env bash
# Rebuild every figure from source into out/ (PDF, SVG, PNG).
# Figures 2-5, S1-S3 and the graphical abstract use the agarwood-scifig house style
# (design-templates/house-style/agarwood-scifig) and render through headless Chromium (Playwright).
# Set SCIFIG_TITLES=1 to add the in-figure title line and provenance footer (poster/preview look).
set -euo pipefail
cd "$(dirname "$0")"
for s in fig2_counterexample fig3_timeline fig4_attributes fig5_validation_programme \
         figS1_strain_definitions figS2_error_attributes figS3_training_inference graphical_abstract; do
  python3 "src/$s.py"
done
# Figure 1 stays in Typst + CeTZ; trim its margins and stamp its PNG resolution.
python3 src/build_typst.py
python3 style/finalize_outputs.py Figure_1_measurement_chain
# QA: rendered font sizes (Elsevier floor 6 pt for scripts, 7 pt text), then a contact sheet.
python3 style/audit_font_sizes.py
python3 style/contact_sheet.py

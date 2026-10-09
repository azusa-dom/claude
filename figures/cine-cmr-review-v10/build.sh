#!/usr/bin/env bash
# Rebuild every figure from source into out/ (PDF, SVG, PNG).
set -euo pipefail
cd "$(dirname "$0")"
for s in fig2_counterexample fig3_timeline fig4_attributes figS1_strain_definitions figS2_error_attributes; do
  python3 "src/$s.py"
done
python3 src/build_typst.py

"""Supplementary Figure S3: training-time versus inference-time controls.

agarwood-scifig journal variant, 190 mm. Conceptual schematic; no study data.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
from scifig_common import C, T, export, start, wrap  # noqa: E402

H = 322
fig = start(H, "Figure S3 | Training-time versus inference-time controls",
            footer=["Conceptual schematic; no study data.", "λ, loss or regularisation weight."])

SM = T.SMALL
X0, X1 = 20, 780
SX = [236, 426, 616]                  # station x positions
fig.panel(X0, 24, "a", "Two ways to vary one setting; only one of them retrains the estimator")

rows = [
    (70, "Training-time control", "the setting lives in the training objective",
     [("Loss weight λ", "changed in the objective"), ("Matched retraining", "same data, splits and schedule"),
      ("Models A, B", "one trained model per setting")], ["retrain", "train"]),
    (146, "Inference-time control", "the setting is exposed at test time",
     [("Exposed parameter", "post-processing or a biomechanical solve"), ("Same trained model", "no retraining"),
      ("Outputs A, B", "one output per setting")], ["apply", "run"]),
]
for cy, name, sub, steps, verbs in rows:
    fig.text(X0, cy + 4, name, T.BODY, 700)
    for k, s in enumerate(wrap(sub, 170, SM)):
        fig.text(X0, cy + 20 + k * 13, s, SM, fill=C.MUTED)
    for i, (head, desc) in enumerate(steps):
        x = SX[i]
        fig.circle(x, cy, 5, C.INK if i == 0 else C.INF)
        fig.text(x + 11, cy + 4, head, T.BODY, 700)
        for k, s in enumerate(wrap(desc, 150, SM)):
            fig.text(x + 11, cy + 20 + k * 13, s, SM, fill=C.MUTED)
        if i < 2:
            x_end = x + 11 + 142
            fig.arrow(x_end, cy, SX[i + 1] - 10, cy, C.MUTED, 1.1, 5)
            fig.verb((x_end + SX[i + 1] - 10) / 2, cy - 6, verbs[i])
    fig.line(SX[2] + 150, cy, 768, cy, C.MUTED, 1.1)
fig.line(768, 70, 768, 146, C.MUTED, 1.1)
fig.arrow(768, 146, 768, 192, C.MUTED, 1.1, 5)
fig.text(762, 184, "compare", SM, fill=C.MUTED, anchor="end", italic=True)
fig.line(X0, 110, 740, 110, C.GRID, 0.8)
fig.cross(X0, 196, "Varying λ only at test time has no effect unless the trained model exposes it.", SM)

# ---- b: shared evaluation ------------------------------------------------------------------------
fig.row_rule(214)
fig.panel(X0, 240, "b", "Both routes are compared under one held-out evaluation contract")
crit = [("held-out cases", "final test cases kept out of model, hyperparameter and rule selection"),
        ("same estimand", "one definition of the reported strain"),
        ("same reference", "one material-sensitive or known-motion reference"),
        ("attribute-specific losses", "magnitude, location, extent, timing, field validity")]
x = X0
for name, desc in crit:
    fig.tick(x + 4, 258, C.SUP)
    fig.text(x + 14, 262, name, T.BODY, 700)
    for k, s in enumerate(wrap(desc, 172, SM)):
        fig.text(x + 14, 277 + k * 13, s, SM, fill=C.MUTED)
    x += 190
fig.legend_items(X0, H - 4, [("control setting", "dot", C.INK), ("estimator state", "dot", C.INF)], gap=26)

export(fig, "Figure_S3_training_vs_inference_controls")

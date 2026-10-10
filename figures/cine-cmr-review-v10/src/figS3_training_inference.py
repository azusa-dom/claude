"""Supplementary Figure S3: training-time versus inference-time controls.

agarwood-scifig house style, 190 mm. Conceptual schematic; no study data.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
from scifig_common import C, T, export, start, wrap  # noqa: E402

H = 352
fig = start(H, "Figure S3 | Training-time versus inference-time controls",
            legend=[("control setting", C.INK), ("estimator state", C.INF), ("evaluation", C.REF)],
            footer=["Conceptual schematic; no study data.",
                    "λ, loss or regularisation weight."])

SX = [232, 418, 604]
tracks = [
    (6, 112, "TRAINING", C.INF, C.PEAR, "Training-time control", "the setting lives in the training objective",
     [("Loss weight λ", "changed in the objective"), ("Matched retraining", "same data, splits and schedule"),
      ("Models A, B", "one trained model per setting")], ["retrain", "train"]),
    (120, 226, "INFERENCE", C.OBS, C.MASK, "Inference-time control", "the setting is exposed at test time",
     [("Exposed parameter", "post-processing or a biomechanical solve"), ("Same trained model", "no retraining"),
      ("Outputs A, B", "one output per setting")], ["apply", "run"]),
]
for y0, y1, tag, c0, c1, name, sub, steps, verbs in tracks:
    fig.track_strip(y0, y1, tag, c0, c1)
    cy = y0 + 38
    fig.text(52, cy + 4, name, T.SUB, 700)
    for k, s in enumerate(wrap(sub, 150, T.CAPTION)):
        fig.text(52, cy + 21 + k * 14, s, T.CAPTION, fill=C.MUTED)
    for i, (head, desc) in enumerate(steps):
        x = SX[i]
        fig.circle(x, cy, 5.5, C.INK if i == 0 else C.INF)
        fig.text(x + 12, cy + 4, head, T.BODY, 700)
        for k, s in enumerate(wrap(desc, 140, T.CAPTION)):
            fig.text(x + 12, cy + 21 + k * 14, s, T.CAPTION, fill=C.MUTED)
        if i < 2:
            ax0 = x + 12 + 128
            fig.arrow(ax0, cy, SX[i + 1] - 12, cy, C.MUTED, 1.2, 6)
            fig.verb((ax0 + SX[i + 1] - 12) / 2, cy - 7, verbs[i])
    fig.line(SX[2] + 140, cy, 772, cy, C.MUTED, 1.2)
fig.line(772, 44, 772, 158, C.MUTED, 1.2)
fig.arrow(772, 158, 772, 242, C.MUTED, 1.2, 6)
fig.text(766, 206, "compare", T.SMALL, fill=C.MUTED, anchor="end", italic=True)
fig.col_rule(206, 10, 226)

# shared evaluation
ey = 248
fig.line(20, ey, 780, ey, C.REF, 1.6)
fig.text(20, ey + 22, "Shared held-out evaluation", T.SUB, 700)
crit = ["held-out cases", "same estimand", "same reference", "attribute-specific losses"]
x = 232
for c in crit:
    fig.tick(x + 4, ey + 18, C.SUP)
    fig.text(x + 14, ey + 22, c, T.BODY)
    x += 14 + len(c) * 6.9 + 24
fig.lines(232, ey + 40, ["losses: magnitude, location, extent, timing, field validity;",
                         "final test cases are kept out of model, hyperparameter and rule selection"], T.SMALL)
fig.cross(20, ey + 80, "Varying λ only at test time has no effect unless the trained model exposes it.", T.CAPTION)
fig.legend_items(20, H - 2, [("control setting", "dot", C.INK), ("estimator state", "dot", C.INF),
                              ("evaluation against a reference", "line", C.REF)], gap=26)

export(fig, "Figure_S3_training_vs_inference_controls")

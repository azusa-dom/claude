#import "../style/diagram.typ": *

#show: setup.with(166mm)

#let W = 166
#let H = 64.0
#let head(t) = text(weight: "bold", size: fs-body, t)
#let sm(t) = text(size: fs-small, t)
#let mut(t) = text(size: fs-small, fill: muted, t)

#canvas(length: 1mm, {
  frame(W, H)
  let lanes = (
    (9.0, [Training-time control], [the setting lives in the training objective], (
      ([Loss weight #m[λ]], [changed in the objective]),
      ([Matched retraining], [same data, splits and schedule]),
      ([Models A, B], [one trained model per setting]),
    )),
    (27.0, [Inference-time control], [the setting is exposed at test time], (
      ([Exposed parameter], [post-processing or a biomechanical solve]),
      ([Same trained model], [no retraining]),
      ([Outputs A, B], [one output per setting]),
    )),
  )
  let sx = (44.0, 85.0, 126.0)
  let joinx = W - 1.0
  for (y, name, sub, steps) in lanes {
    label(0.8, y - 2.4, box(width: 38mm, stack(dir: ttb, spacing: 1.3mm, text(size: fs-title, weight: "bold", name), mut(sub))))
    for (i, (t, d)) in steps.enumerate() {
      let x = sx.at(i)
      draw.circle(P(x, y), radius: 1.2, fill: if i == 0 { ink } else { inf }, stroke: none)
      label(x + 2.4, y - 2.4, box(width: 32mm, stack(dir: ttb, spacing: 1.3mm, head(t), par(leading: 0.5em, mut(d)))))
      if i < 2 {
        arrow((x + 34.0, y), (sx.at(i + 1) - 2.2, y), thick: 0.6pt, paint: muted, head: 1.4)
      }
    }
    seg((sx.at(2) + 36.4, y), (joinx, y), paint: muted, thick: 0.6pt)
  }
  seg((joinx, 9.0), (joinx, 27.0), paint: muted, thick: 0.6pt)
  arrow((joinx, 27.0), (joinx, 41.6), thick: 0.6pt, paint: muted, head: 1.5)

  label(0.8, 36.0, text(size: fs-small, style: "italic", fill: muted)[Varying #m[λ] only at test time has no effect unless the trained model exposes it.])

  let ey = 42.6
  hrule(0.8, W - 0.8, ey, paint: ref, thick: 0.9pt)
  label(0.8, ey + 4.6, anchor: "west", text(size: fs-title, weight: "bold")[Shared held-out evaluation])
  let px = 52.0
  for (w, t) in ((24.0, [held-out cases]), (24.0, [same estimand]), (25.0, [same reference]), (34.0, [attribute-specific losses])) {
    pill(px, ey + 2.3, w, 4.6, t, paint: ref)
    px += w + 2.0
  }
  label(0.8, ey + 9.6, mut[attribute-specific losses: magnitude, location, extent, timing, field validity · final test cases are kept out of model, hyperparameter and rule selection])

  let ky = H - 2.4
  draw.circle(P(1.8, ky), radius: 1.1, fill: ink, stroke: none)
  label(3.8, ky, anchor: "west", mut[control setting])
  draw.circle(P(27.0, ky), radius: 1.1, fill: inf, stroke: none)
  label(29.0, ky, anchor: "west", mut[estimator state])
  seg((50.0, ky), (55.0, ky), paint: ref, thick: 0.9pt)
  label(56.4, ky, anchor: "west", mut[evaluation against a reference])
  label(W - 0.8, ky, anchor: "east", mut[Conceptual schematic; no study data.])
})

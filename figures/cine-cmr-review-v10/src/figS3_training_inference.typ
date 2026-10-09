#import "../style/diagram.typ": *

#show: setup.with(166mm)

#let W = 166
#let H = 69.0
#let head(t) = text(weight: "bold", size: fs-body, t)
#let sm(t) = text(size: fs-small, t)

#canvas(length: 1mm, {
  frame(W, H)
  let colw = 78.0
  let cols = (
    (0.8, [Training-time control], (
      ([Loss weight #m[λ]], [changed in the training objective]),
      ([Matched retraining], [same data, splits and schedule]),
      ([Models A, B], [one trained model per setting]),
    )),
    (W - colw - 0.8, [Inference-time control], (
      ([Exposed parameter], [post-processing or a biomechanical solve]),
      ([Same trained model], [no retraining]),
      ([Outputs A, B], [one output per setting]),
    )),
  )
  let bw = 24.0
  let bh = 23.0
  let by = 7.5
  for (x0, heading, boxes) in cols {
    label(x0, 0.8, text(size: fs-title, weight: "bold", heading))
    for (i, (t, d)) in boxes.enumerate() {
      let x = x0 + i * (bw + 3.0)
      let f = if i == 0 { white } else { teal-t }
      let p = if i == 0 { ink } else { teal }
      node(x, by, bw, bh, fill: f, paint: p, [#head(t)#v(0.8mm)#sm(d)])
      if i < 2 {
        arrow((x + bw + 0.3, by + bh / 2), (x + bw + 2.7, by + bh / 2), thick: 0.8pt, head: 1.4)
      }
    }
    let last = x0 + 2 * (bw + 3.0) + bw / 2
    arrow((last, by + bh + 0.4), (last, 38.6), thick: 0.8pt)
  }
  label(0.8, by + bh + 2.0, width: 2 * bw + 3.0,
    text(size: fs-small, fill: muted)[Varying #m[λ] only at test time has no effect unless the trained model exposes it.])

  node(0.8, 39.0, W - 1.6, 16.0, fill: orange-t, paint: orange, halign: center,
    [#head[Shared held-out evaluation]#v(1.0mm)#sm[held-out cases · same estimand · same reference · attribute-specific losses (magnitude, location, extent, timing, field validity)]#v(0.6mm)#text(size: fs-small, fill: muted)[final test cases kept out of model, hyperparameter and rule selection]])

  let ky = 60.5
  arrow((1.0, ky), (8.0, ky), thick: 0.8pt, head: 1.4)
  label(9.2, ky, sm[produces the input to the next step], anchor: "west")
  swatch(70.0, ky, teal-t, teal, [estimator state])
  swatch(100.0, ky, orange-t, orange, [evaluation against a reference])
  label(W - 0.8, H - 0.6, anchor: "south-east", text(size: fs-small, fill: muted)[Conceptual schematic; no study data.])
})

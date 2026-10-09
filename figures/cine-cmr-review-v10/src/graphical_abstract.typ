#import "../style/diagram.typ": *

// 260 x 100 mm page exported at 254 ppi gives 2600 x 1000 px (13:5).
#set page(width: 260mm, height: 100mm, margin: 0pt, fill: white)
#set text(font: sans, size: 12pt, fill: ink)
#set par(leading: 0.42em)

#let W = 260
#let H = 100
#let big(t) = text(size: 14pt, weight: "bold", t)
#let md(t) = text(size: 12pt, t)
#let sm(t) = text(size: 11pt, t)

#canvas(length: 1mm, {
  frame(W, H)

  // left: routine cine
  let cx = 36.0
  let cy = 44.0
  draw.circle(P(cx, cy), radius: 22.0, fill: grey-t, stroke: (paint: grey, thickness: 1.2pt))
  draw.circle(P(cx, cy), radius: 12.5, fill: white, stroke: (paint: grey, thickness: 1.2pt))
  for (dx, dy) in ((-17, -6), (-15, 7), (-9, 15), (2, 18), (12, 14), (17, 4), (16, -8), (8, -16), (-4, -18), (-13, -13), (-18, 1), (5, 16.5)) {
    draw.circle(P(cx + dx, cy + dy), radius: 0.45, fill: grey, stroke: none)
  }
  label(cx, cy + 25.5, anchor: "north", align(center)[#big[Routine cine CMR]#v(1mm)#sm[boundaries · texture · time]])

  arrow((61.0, cy), (74.0, cy), thick: 1.4pt, head: 3.2)

  // middle: estimator chain and attributes
  let mx = 76.0
  let bw = 34.5
  let bh = 17.0
  let names = ([Estimator #linebreak() + prior], [Material #linebreak() correspondence], [Regional #linebreak() strain])
  for (i, n) in names.enumerate() {
    let x = mx + i * (bw + 4.0)
    node(x, cy - bh / 2, bw, bh, fill: teal-t, paint: teal, thick: 1.0pt, radius: 2.0, inset: 1.0, text(size: 11.5pt, weight: "bold", n))
    if i < 2 {
      arrow((x + bw + 0.4, cy), (x + bw + 3.6, cy), paint: teal, thick: 1.3pt, head: 2.2)
    }
  }
  let ay = cy + bh / 2 + 9.0
  let aw = 24.5
  let ax0 = mx + (3 * bw + 8.0 - (4 * aw + 3 * 2.5)) / 2
  for (i, a) in ([magnitude], [location], [extent], [timing]).enumerate() {
    node(ax0 + i * (aw + 2.5), ay, aw, 9.0, paint: teal, thick: 0.9pt, radius: 4.5, md(a))
  }
  label(mx + (3 * bw + 8.0) / 2, ay + 11.5, anchor: "north",
    sm[tested per attribute, per estimator, per acquisition])

  arrow((mx + 3 * bw + 8.0 + 1.0, cy), (194.5, cy), thick: 1.3pt, dash: "dashed", head: 2.4)

  // right: evidence tiers and conclusions
  let rx = 196.0
  let rw = W - rx - 2.0
  let tiers = ([Known motion], [Paired DENSE / tagging], [Tissue & outcome])
  for (i, t) in tiers.enumerate() {
    node(rx, 9.0 + i * 12.0, rw, 10.0, fill: orange-t, paint: orange, thick: 1.0pt, radius: 1.5, md(t))
  }
  node(rx, 48.0, rw, 21.0, fill: green-t, paint: green, thick: 1.0pt, radius: 1.5, halign: left, inset: 3.0,
    [#text(size: 11pt, weight: "bold", fill: green)[Supported]#linebreak()#sm[whole-slice, global and segmental Ecc under matched definitions]])
  node(rx, 71.5, rw, 21.0, paint: red, thick: 1.0pt, dash: "dashed", radius: 1.5, halign: left, inset: 3.0,
    [#text(size: 11pt, weight: "bold", fill: red)[Weaker]#linebreak()#sm[radial strain; focal boundary, extent and timing, rarely tested]])
})

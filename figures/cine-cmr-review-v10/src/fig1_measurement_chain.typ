#import "../style/diagram.typ": *

#show: setup.with(160mm)

#let W = 160
#let nw = 27.6
#let gap = 5.0
#let nx(i) = 0.8 + i * (nw + gap)
#let ny = 7.5
#let nh = 27.0
#let ty = 44.0
#let th = 29.0
#let H = 98.0

#let head(t) = text(weight: "bold", size: fs-body, t)
#let sub(t) = text(size: fs-small, t)

#canvas(length: 1mm, {
  frame(W, H)
  title(0, 0.8, "a", [From cine images to a regional strain report])

  let nodes = (
    ([Image formation & sampling], [bSSFP cine · spatial and temporal resolution · reconstruction], grey-t, grey),
    ([Correspondence estimation], [contours or dense field · estimator + prior], teal-t, teal),
    ([Representation & regularisation], [voxel · spline · Fourier · finite element · learned], teal-t, teal),
    ([Strain definition & aggregation],
      [#m[E]#mr[ \= ½(]#m[F]#super(m[T])#m[F]#mr[ − ]#m[I]#mr[)] · axes · layer · reference · peak rule], teal-t, teal),
    ([Validation target], [known motion · DENSE/tagging · scan–rescan · LGE · outcome], orange-t, orange),
  )
  for (i, (t, s, f, p)) in nodes.enumerate() {
    node(nx(i), ny, nw, nh, fill: f, paint: p, [#head(t)#v(1.2mm)#sub(s)])
    if i < 4 {
      arrow((nx(i) + nw + 0.4, ny + nh / 2), (nx(i + 1) - 0.4, ny + nh / 2), thick: 0.8pt)
    }
  }

  label(0, 37.0, panel("b"))
  let tests = (
    ([Input sufficiency], [Do the images contain the cue?], [re-image the same motion more finely or with more views]),
    ([Estimation], [Does the optimiser or network recover it?], [vary #m[α] (penalty weight) with images fixed]),
    ([Representation capacity], [Can the basis express the lesion?], [project the known field onto the function space]),
  )
  for (i, (t, q, how)) in tests.enumerate() {
    node(nx(i), ty, nw, th, paint: ink, thick: 0.6pt,
      [#head(t)#v(0.8mm)#sub(q)#v(1.0mm)#text(size: fs-small, fill: muted)[Test: #how]])
    arrow((nx(i) + nw / 2, ty - 0.4), (nx(i) + nw / 2, ny + nh + 0.5), dash: "dashed", thick: 0.7pt)
  }
  node(nx(3), ty, 2 * nw + gap, th, fill: white, paint: rule, halign: left, inset: 2.4,
    [#head[Three failure points, tested separately]#v(1.2mm)#sub[Attribution experiment: when a known focal deficit is under-recovered, hold two factors fixed and vary the third. Recovery after reducing #m[α] points to estimation; failure after projecting the known field points to representation; recovery only after re-imaging points to input information.]])

  node(0.8, 77.0, W - 1.6, 8.0, fill: green-t, paint: green, thick: 0.6pt, halign: left, inset: 2.4,
    [#text(weight: "bold")[c]#h(2.2mm)Validation must follow the finest claimed spatial and temporal scale, not inherit credibility from an upstream task.])

  let ky = 90.0
  arrow((1.0, ky), (8.0, ky), thick: 0.8pt)
  label(9.2, ky, text(size: fs-small)[output feeds the next step], anchor: "west")
  arrow((45.0, ky), (52.0, ky), dash: "dashed", thick: 0.7pt)
  label(53.2, ky, text(size: fs-small)[test targets this link], anchor: "west")
  swatch(82.0, ky, grey-t, grey, [observed in cine])
  swatch(108.0, ky, teal-t, teal, [inferred])
  swatch(125.0, ky, orange-t, orange, [reference / validation])
  label(W - 0.8, ky + 4.2, text(size: fs-small, fill: muted)[Conceptual schematic; no study data.], anchor: "north-east")
})

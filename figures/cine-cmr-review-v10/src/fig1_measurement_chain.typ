#import "../style/diagram.typ": *

#show: setup.with(160mm)

#let W = 160
#let H = 99.0
#let sx(i) = 15.0 + i * 32.5
#let ty = 15.0

#let head(t) = text(weight: "bold", size: fs-body, t)
#let mut(t) = text(size: fs-small, fill: muted, t)

#canvas(length: 1mm, {
  frame(W, H)
  title(0, 0.8, "a", [From cine images to a regional strain report])
  dotkey(103.0, 3.4, obs, [observed in cine])
  dotkey(126.0, 3.4, inf, [inferred])
  dotkey(140.5, 3.4, ref, [reference])

  let steps = (
    ([Image formation\ & sampling], [bSSFP cine\ spatial and temporal\ resolution\ reconstruction], obs),
    ([Correspondence\ estimation], [contours or dense field\ estimator + prior], inf),
    ([Representation\ & regularisation], [voxel · spline · Fourier\ finite element · learned], inf),
    ([Strain definition\ & aggregation],
      [#m[E]#mr[ \= ½(]#m[F]#mr[ᵀ]#m[F]#mr[ − ]#m[I]#mr[)]\ axes · layer · reference\ peak rule], inf),
    ([Validation\ target], [known motion · DENSE/tagging\ scan–rescan · LGE\ outcome], ref),
  )
  for (i, (t, d, c)) in steps.enumerate() {
    let x = sx(i)
    if i < 4 {
      arrow((x + 3.4, ty), (sx(i + 1) - 3.4, ty), thick: 0.7pt, paint: muted, head: 1.6)
    }
    badge(x, ty, str(i + 1), c, r: 2.8)
    label(x, ty + 4.6, anchor: "north", box(width: 30mm, align(center, head(t))))
    label(x, ty + 12.6, anchor: "north", box(width: 30mm, align(center, par(leading: 0.5em, mut(d)))))
  }

  // b: failure points, keyed to the station they test by number
  let by = 47.0
  title(0, by, "b", [Three failure points, each testable on its own])
  let fails = (
    (0, [Input sufficiency], [Do the images contain the cue?], [re-image the same motion more finely or with more views]),
    (1, [Estimation], [Does the optimiser or network recover it?], [vary #m[α] (penalty weight) with images fixed]),
    (2, [Representation capacity], [Can the basis express the lesion?], [project the known field onto the function space]),
  )
  for (k, t, q, how) in fails {
    let fx = sx(k) - 14.0
    let c = steps.at(k).at(2)
    ring(fx + 2.0, by + 9.4, 2.0, c, thick: 0.8pt)
    label(fx + 2.0, by + 9.4, anchor: "center", text(size: 7pt, weight: "bold", fill: c, str(k + 1)))
    label(fx + 5.2, by + 7.9, box(width: 24mm, stack(dir: ttb, spacing: 1.6mm,
      par(leading: 0.45em, head(t)), par(leading: 0.5em, text(size: fs-small, q)),
      par(leading: 0.5em, mut[Test: #how]))))
  }

  // attribution logic as a three-row table
  let lx = 97.0
  label(lx, by + 7.4, head[If a known focal deficit is under-recovered])
  let rh = 6.4
  let rows = (
    ([recovers when #m[α] is reduced], [estimation]),
    ([still fails after projecting the known field], [representation]),
    ([recovers only after re-imaging], [input information]),
  )
  for (i, (cond, cause)) in rows.enumerate() {
    let y0 = by + 12.4 + i * rh
    hrule(lx, W - 0.8, y0)
    let y = y0 + rh / 2
    label(lx, y, anchor: "west", box(width: 33.5mm, par(leading: 0.45em, mut(cond))))
    arrow((lx + 34.6, y), (lx + 38.0, y), thick: 0.6pt, paint: muted, head: 1.3)
    label(lx + 39.2, y, anchor: "west", text(size: fs-small, weight: "bold", cause))
  }
  hrule(lx, W - 0.8, by + 12.4 + 3 * rh)

  // c: conclusion as a pull quote
  let cy = 84.0
  label(0, cy, panel("c"))
  bar(6.0, cy + 0.2, cy + 7.6, sup, thick: 0.9)
  label(9.0, cy + 3.9, anchor: "west", text(size: 8.5pt, style: "italic")[Validation must follow the finest claimed spatial and temporal scale; upstream credibility does not transfer down.])

  let ky = 95.6
  arrow((0.8, ky), (7.0, ky), thick: 0.7pt, paint: muted, head: 1.5)
  label(8.2, ky, anchor: "west", mut[output feeds the next step])
  ring(45.0, ky, 1.9, muted, thick: 0.7pt)
  label(45.0, ky, anchor: "center", text(size: 7pt, weight: "bold", fill: muted)[n])
  label(47.9, ky, anchor: "west", mut[failure point at step n])
})

#import "../style/diagram.typ": *

#show: setup.with(160mm)

#let W = 160
#let H = 128.0
#let head(t) = text(weight: "bold", size: fs-body, t)
#let sm(t) = text(size: fs-small, t)
#let mut(t) = text(size: fs-small, fill: muted, t)

#canvas(length: 1mm, {
  frame(W, H)

  // a: target -> claim, as a three-rule table
  title(0, 0.8, "a", [What each validation target can establish])
  let c0 = 0.8
  let c1 = 47.5
  let c2 = 113.0
  let top = 7.8
  hrule(c0, W - 0.8, top, paint: ink, thick: 0.6pt)
  let hy = top + 3.2
  draw.circle(P(c0 + 1.1, hy), radius: 1.1, fill: ref, stroke: none)
  label(c0 + 3.2, hy, anchor: "west", head[Validation target])
  tick(c1 + 1.2, hy, paint: sup)
  label(c1 + 3.6, hy, anchor: "west", head[Strongest claim it supports])
  cross(c2 + 1.0, hy, paint: muted)
  label(c2 + 3.4, hy, anchor: "west", head[Does not establish on its own])
  let hb = top + 6.4
  hrule(c0, W - 0.8, hb, paint: ink, thick: 0.4pt)
  let rows = (
    ([Known motion (phantom, STRAUS, MRXCAT2.0)], [representation capacity and technical error in the simulated regime], [in-vivo accuracy]),
    ([Paired DENSE or tagging], [material-sensitive agreement under matched definitions], [focal location or extent, unless measured]),
    ([Scan–rescan], [precision, not accuracy], [bias]),
    ([LGE or tissue characterisation], [biological association, not motion error], [pointwise displacement error]),
    ([Outcome], [prognostic association, not clinical utility], [decision impact]),
  )
  let rh = 7.0
  for (i, (tg, est, no)) in rows.enumerate() {
    let y = hb + i * rh + rh / 2
    label(c0, y, anchor: "west", box(width: 44mm, par(leading: 0.45em, sm(tg))))
    label(c1 + 3.6, y, anchor: "west", box(width: 61mm, par(leading: 0.45em, sm(est))))
    label(c2 + 3.4, y, anchor: "west", box(width: 43mm, par(leading: 0.45em, mut(no))))
    if i < 4 { hrule(c0, W - 0.8, hb + (i + 1) * rh) }
  }
  hrule(c0, W - 0.8, hb + 5 * rh, paint: ink, thick: 0.6pt)

  // b: staged programme as a numbered stepper with resources alongside
  let by = 57.0
  title(0, by, "b", [A staged programme for regional or focal claims])
  let lx = 4.0
  let tx = 9.5
  let rx = 67.0
  let rw = 47.0
  let y0 = by + 10.5
  let rowy = (y0, y0 + 13.0, y0 + 30.0, y0 + 47.0)
  seg((lx, rowy.at(0)), (lx, rowy.at(3)), paint: rule, thick: 1.0pt)
  ring(lx, rowy.at(0), 2.6, ink, thick: 0.8pt)
  tick(lx, rowy.at(0), s: 1.1, paint: ink)
  label(tx, rowy.at(0) - 1.9, box(width: 56mm, stack(dir: ttb, spacing: 1.3mm,
    head[Pre-specify the measurement contract], mut[estimand · reference · tolerance · data splits])))
  label(rx, rowy.at(0) - 1.9, mut[Resources (Table 4)])
  let stages = (
    ([Known motion], [vary width, extent, amplitude, timing, resolution and noise],
      ([STRAUS: 3 templates × 6 states], [MRXCAT2.0: programmable generator], [CMAC dynamic phantom])),
    ([Paired material reference], [cine with DENSE or tagging in one session; registered; reference blinded],
      ([Stanford: 51/55 · not file-verified], [CMAC: 15 volunteers, 12 landmarks])),
    ([Tissue and decisions], [LGE, responsiveness, decision impact],
      ([Clinical cohorts with LGE or outcomes],)),
  )
  for (i, (t, d, res)) in stages.enumerate() {
    let y = rowy.at(i + 1)
    badge(lx, y, str(i + 1), ref, r: 2.6)
    label(tx, y - 1.9, box(width: 55mm, stack(dir: ttb, spacing: 1.3mm,
      head[Stage #(i + 1) · #t], par(leading: 0.5em, mut(d)))))
    let ph = 4.6
    for (k, r) in res.enumerate() {
      pill(rx, y - 2.3 + k * (ph + 1.0), rw, ph, r)
    }
  }

  // c: equal-mean counterexample
  let px = 121.0
  let pw = W - px - 0.8
  title(px - 1.0, by, "c", [Equal-mean test])
  let s2y(s) = by + 13.0 + (-s) / 0.25 * 22.0
  let sx(i) = px + 9.0 + i * 5.6
  seg((px + 7.5, s2y(0)), (px + pw - 1.0, s2y(0)), paint: muted, thick: 0.4pt)
  label(px + 6.8, s2y(0), anchor: "east", sm[0])
  label(px + 6.8, s2y(-0.2), anchor: "east", sm[−0.2])
  seg((px + 7.5, s2y(-0.2)), (px + 8.3, s2y(-0.2)), paint: ink, thick: 0.4pt)
  seg((px + 7.5, s2y(0)), (px + 7.5, s2y(-0.25)), paint: ink, thick: 0.5pt)
  let foc = (-0.22, -0.22, -0.06, -0.18, -0.20, -0.20)
  seg((sx(0) - 1.5, s2y(-0.18)), (sx(5) + 1.5, s2y(-0.18)), paint: muted, thick: 0.6pt, dash: "dashed")
  for i in range(5) {
    seg((sx(i), s2y(foc.at(i))), (sx(i + 1), s2y(foc.at(i + 1))), paint: inf, thick: 0.9pt)
  }
  for i in range(6) {
    draw.circle(P(sx(i), s2y(foc.at(i))), radius: 0.7, fill: inf, stroke: none)
    label(sx(i), s2y(-0.25) + 1.2, anchor: "north", sm[#(i + 1)])
  }
  label(sx(2) + 0.9, s2y(-0.06) - 0.4, anchor: "south-west", sm[focal deficit])
  label(px + pw / 2 + 3.0, s2y(-0.25) + 4.6, anchor: "north", mut[segment])
  label(px, by + 44.5, width: pw, par(leading: 0.5em, mut[Uniform (dashed) and focal (solid) fields share a global mean of −0.18. Recovering the mean is not a pass.]))

})

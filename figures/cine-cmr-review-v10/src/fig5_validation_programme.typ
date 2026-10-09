#import "../style/diagram.typ": *

#show: setup.with(160mm)

#let W = 160
#let H = 146.0
#let head(t) = text(weight: "bold", size: fs-body, t)
#let sm(t) = text(size: fs-small, t)

#canvas(length: 1mm, {
  frame(W, H)

  // a: target -> claim table
  title(0, 0.8, "a", [What each validation target can establish])
  let cx = (0.8, 48.8, 109.8)
  let cw = (47.0, 60.0, 49.4)
  let hy = 7.5
  let hh = 6.0
  node(cx.at(0), hy, cw.at(0), hh, fill: orange-t, paint: orange, radius: 0.6, halign: left, head[Validation target])
  node(cx.at(1), hy, cw.at(1), hh, fill: green-t, paint: green, radius: 0.6, halign: left, head[Strongest claim it supports])
  node(cx.at(2), hy, cw.at(2), hh, fill: grey-t, paint: grey, radius: 0.6, halign: left, head[Does not establish on its own])
  let rows = (
    ([Known motion (phantom, STRAUS, MRXCAT2.0)], [representation capacity and technical error in the simulated regime], [in-vivo accuracy]),
    ([Paired DENSE or tagging], [material-sensitive agreement under matched definitions], [focal location or extent, unless measured]),
    ([Scan–rescan], [precision, not accuracy], [bias]),
    ([LGE or tissue characterisation], [biological association, not motion error], [pointwise displacement error]),
    ([Outcome], [prognostic association, not clinical utility], [decision impact]),
  )
  let ry = hy + hh + 0.8
  let rh = 7.4
  for (i, (tg, est, no)) in rows.enumerate() {
    let y = ry + i * (rh + 0.6)
    node(cx.at(0), y, cw.at(0), rh, paint: orange, thick: 0.5pt, radius: 0.6, halign: left, sm(tg))
    node(cx.at(1), y, cw.at(1), rh, paint: green, thick: 0.5pt, radius: 0.6, halign: left, text(size: fs-small, fill: green, est))
    node(cx.at(2), y, cw.at(2), rh, paint: rule, thick: 0.5pt, radius: 0.6, halign: left, text(size: fs-small, fill: muted, no))
  }

  // b: staged programme
  let by = 59.0
  title(0, by, "b", [A staged programme for regional or focal claims])
  let fx = 0.8
  let fw = 62.0
  let mid = fx + fw / 2
  node(fx, by + 7.0, fw, 10.5, paint: ink, halign: center,
    [#head[Pre-specified measurement contract]#v(0.6mm)#sm[estimand · reference · tolerance · data splits]])
  let stages = (
    ([Stage 1 · Known motion], [vary width, extent, amplitude, timing, resolution and noise], 62.0, 57.0),
    ([Stage 2 · Paired material reference], [cine with DENSE or tagging in the same session; registered; reference blinded], 57.0, 52.0),
    ([Stage 3 · Tissue and decisions], [LGE, responsiveness, decision impact], 52.0, 47.0),
  )
  let sy0 = by + 21.5
  let sh = 17.0
  let sg = 3.5
  arrow((mid, by + 17.9), (mid, sy0 - 0.3), thick: 0.8pt)
  for (i, (t, d, wt, wb)) in stages.enumerate() {
    let y = sy0 + i * (sh + sg)
    poly(((mid - wt / 2, y), (mid + wt / 2, y), (mid + wb / 2, y + sh), (mid - wb / 2, y + sh)),
      fill: orange-t, paint: orange)
    label(mid, y + sh / 2, anchor: "center", box(width: (wb - 6) * 1mm, align(center, [#head(t)#v(0.6mm)#sm(d)])))
    if i < 2 {
      arrow((mid, y + sh + 0.4), (mid, y + sh + sg - 0.3), thick: 0.8pt)
    }
  }

  let rx = 66.5
  let rw = 48.5
  label(rx, by + 7.0, text(size: fs-small, fill: muted)[Resources (Table 4)])
  let chips = (
    (([STRAUS: 3 templates × 6 states], 4.8), ([MRXCAT2.0: programmable generator], 4.8), ([CMAC dynamic phantom], 4.8)),
    (([Stanford: 51/55 participants,\ not file-verified], 7.6), ([CMAC: 15 volunteers, 12 landmarks], 4.8)),
    (([Clinical cohorts with LGE or outcomes], 4.8),),
  )
  for (i, cs) in chips.enumerate() {
    let y = sy0 + i * (sh + sg)
    let total = cs.map(c => c.at(1)).sum() + (cs.len() - 1) * 0.9
    let yy = y + (sh - total) / 2
    for (c, ch) in cs {
      chip(rx, yy, rw, ch, c)
      yy += ch + 0.9
    }
    let st = stages.at(i)
    seg((mid + (st.at(2) + st.at(3)) / 4 + 0.3, y + sh / 2), (rx - 0.4, y + sh / 2), paint: rule, thick: 0.5pt)
  }

  // c: equal-mean counterexample beside Stage 1
  let px = 117.5
  let pw = W - px - 0.8
  title(px - 0.3, by, "c", [Equal-mean test])
  node(px, by + 7.0, pw, 47.0, paint: rule, thick: 0.5pt, [])
  let s2y(s) = by + 13.0 + (-s) / 0.25 * 22.0
  let sx(i) = px + 9.0 + i * 5.6
  seg((px + 7.5, s2y(0)), (px + pw - 2.0, s2y(0)), paint: muted, thick: 0.4pt)
  label(px + 6.8, s2y(0), anchor: "east", text(size: fs-small)[0])
  label(px + 6.8, s2y(-0.2), anchor: "east", text(size: fs-small)[−0.2])
  seg((px + 7.5, s2y(-0.2)), (px + 8.3, s2y(-0.2)), paint: ink, thick: 0.4pt)
  seg((px + 7.5, s2y(0)), (px + 7.5, s2y(-0.25)), paint: ink, thick: 0.5pt)
  let uni = (-0.18, -0.18, -0.18, -0.18, -0.18, -0.18)
  let foc = (-0.22, -0.22, -0.06, -0.18, -0.20, -0.20)
  seg((sx(0) - 1.5, s2y(-0.18)), (sx(5) + 1.5, s2y(-0.18)), paint: muted, thick: 0.6pt, dash: "dashed")
  for i in range(5) {
    seg((sx(i), s2y(foc.at(i))), (sx(i + 1), s2y(foc.at(i + 1))), paint: teal, thick: 0.9pt)
  }
  for i in range(6) {
    draw.circle(P(sx(i), s2y(foc.at(i))), radius: 0.7, fill: teal, stroke: none)
    label(sx(i), s2y(-0.25) + 1.2, anchor: "north", text(size: fs-small)[#(i + 1)])
  }
  label(sx(2) + 0.9, s2y(-0.06) - 0.4, anchor: "south-west", text(size: fs-small, fill: teal)[focal deficit])
  label(px + pw / 2 + 3.0, s2y(-0.25) + 4.6, anchor: "north", text(size: fs-small, fill: muted)[segment])
  label(px + 2.0, by + 42.5, width: pw - 4.0, sm[Uniform (dashed) and focal (teal) fields share a global mean of −0.18. Recovering the mean is not a pass.])

  label(0, H - 0.6, anchor: "south-west",
    text(size: fs-small, fill: muted)[Counts denote resource units, not independent test participants. Conceptual synthesis; no study data.])
})

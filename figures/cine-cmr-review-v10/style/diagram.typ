// CeTZ helpers in millimetre units with y measured downward from the top edge.
#import "@preview/cetz:0.4.2": canvas, draw
#import "theme.typ": *

#let P(x, y) = (x, -y)

#let node(x, y, w, h, body, fill: white, paint: ink, thick: 0.6pt, dash: none, radius: 1.2,
          inset: 1.8, halign: center) = {
  draw.rect(P(x, y), P(x + w, y + h), fill: fill, radius: radius,
       stroke: (paint: paint, thickness: thick, dash: dash))
  draw.content(P(x + w / 2, y + h / 2),
          box(width: (w - 2 * inset) * 1mm, align(halign + horizon, body)))
}

#let label(x, y, body, anchor: "north-west", width: none) = {
  draw.content(P(x, y), anchor: anchor, if width == none { body } else { box(width: width * 1mm, body) })
}

#let arrow(a, b, paint: ink, thick: 0.7pt, dash: none, head: 1.7) = {
  let (ax, ay) = a
  let (bx, by) = b
  let d = calc.sqrt(calc.pow(bx - ax, 2) + calc.pow(by - ay, 2))
  let (ux, uy) = ((bx - ax) / d, (by - ay) / d)
  let c = (bx - ux * head, by - uy * head)
  draw.line(P(..a), P(..c), stroke: (paint: paint, thickness: thick, dash: dash))
  draw.line(P(..c), P(..b), stroke: (paint: paint, thickness: thick),
       mark: (end: "stealth", fill: paint, length: head, width: head * 0.75))
}

#let poly(pts, fill: white, paint: ink, thick: 0.6pt, dash: none) = {
  draw.line(..pts.map(q => P(..q)), close: true, fill: fill, stroke: (paint: paint, thickness: thick, dash: dash))
}

#let chip(x, y, w, h, body, fill: white, paint: rule) = node(x, y, w, h, fill: fill, paint: paint, thick: 0.5pt,
  radius: 2.0, inset: 1.6, halign: left, text(size: fs-small, body))

#let seg(a, b, paint: ink, thick: 0.6pt, dash: none) = {
  draw.line(P(..a), P(..b), stroke: (paint: paint, thickness: thick, dash: dash))
}

#let title(x, y, letter, body) = label(x, y, [#panel(letter)#h(2.2mm)#text(size: fs-title, weight: "bold", body)])

#let swatch(x, y, fill, paint, body) = {
  draw.rect(P(x, y - 1.1), P(x + 3.2, y + 1.1), fill: fill, stroke: (paint: paint, thickness: 0.6pt), radius: 0.4)
  draw.content(P(x + 4.2, y), anchor: "west", text(size: fs-small, body))
}

// Invisible rectangle that fixes the canvas to exactly W x H millimetres.
#let frame(w, h) = draw.rect(P(0, 0), P(w, h), stroke: none, fill: none)

// ---- light-weight elements: colour as accent, text on white ----
#let badge(x, y, n, fill, r: 2.6, size: 7.5pt) = {
  draw.circle(P(x, y), radius: r, fill: fill, stroke: none)
  draw.content(P(x, y), text(size: size, weight: "bold", fill: white, n))
}

#let ring(x, y, r, paint, thick: 0.7pt, fill: white) = draw.circle(P(x, y), radius: r, fill: fill,
  stroke: (paint: paint, thickness: thick))

#let hrule(x0, x1, y, paint: rule, thick: 0.4pt) = seg((x0, y), (x1, y), paint: paint, thick: thick)

#let bar(x, y0, y1, paint, thick: 1.0) = draw.rect(P(x, y0), P(x + thick, y1), fill: paint, stroke: none)

#let pill(x, y, w, h, body, paint: rule) = {
  draw.rect(P(x, y), P(x + w, y + h), radius: h / 2, fill: white, stroke: (paint: paint, thickness: 0.5pt))
  draw.content(P(x + h / 2.2, y + h / 2), anchor: "west", text(size: fs-small, body))
}

#let tick(x, y, s: 1.0, paint: sup) = draw.line(P(x - s, y), P(x - s * 0.3, y + s * 0.7), P(x + s, y - s * 0.8),
  stroke: (paint: paint, thickness: 0.9pt, cap: "round", join: "round"))

#let cross(x, y, s: 0.8, paint: muted) = {
  draw.line(P(x - s, y - s), P(x + s, y + s), stroke: (paint: paint, thickness: 0.8pt, cap: "round"))
  draw.line(P(x - s, y + s), P(x + s, y - s), stroke: (paint: paint, thickness: 0.8pt, cap: "round"))
}

#let dotkey(x, y, fill, body) = {
  draw.circle(P(x, y), radius: 1.1, fill: fill, stroke: none)
  draw.content(P(x + 2.2, y), anchor: "west", text(size: fs-small, fill: muted, body))
}

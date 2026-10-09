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

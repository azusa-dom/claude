// Shared Typst theme for the v10 figure set; colours mirror style/figstyle.py
// (derived from 沈香墨 #8D6449, 素绢白 #F8F3E7, 檀木棕 #C0997F, 棠梨绯 #E7A49A).
#let obs = rgb("#8E857D")
#let inf = rgb("#C0584A")
#let ref = rgb("#7A4720")
#let coral = rgb("#CC5F4F")
#let err = rgb("#A33A2E")
#let sup = rgb("#4E7470")
#let ink = rgb("#33261F")
#let muted = rgb("#776A62")
#let rule = rgb("#E3D9CF")

#let obs-t = rgb("#F8F3E7")
#let inf-t = rgb("#F8E0DA")
#let ref-t = rgb("#EFE2D3")
#let coral-t = rgb("#F6DCD6")
#let sup-t = rgb("#E3ECEA")

#let sans = ("Arial", "Liberation Sans")
#let serif = ("Times New Roman", "Liberation Serif")

#let fs-body = 7.5pt
#let fs-small = 7.2pt
#let fs-title = 9pt
#let fs-panel = 10pt

// Math typed as Times text runs (manuscript rule: labels Arial, math Times New Roman).
#let m(body) = text(font: serif, style: "italic", body)
#let mr(body) = text(font: serif, body)

#let panel(letter) = text(size: fs-panel, weight: "bold", fill: ink, letter)

// Figures are composed at the manuscript text width and exported at the Elsevier
// double-column width by uniform scaling, so layout and relative type sizes are unchanged.
#let target-w = 190mm

#let setup(width, height: auto, body) = {
  let s = target-w / width
  set page(width: target-w, height: height, margin: 0pt, fill: white)
  set text(font: sans, size: fs-body, fill: ink, lang: "en", hyphenate: false)
  set par(leading: 0.45em, justify: false)
  scale(x: s * 100%, y: s * 100%, origin: top + left, reflow: true, body)
}

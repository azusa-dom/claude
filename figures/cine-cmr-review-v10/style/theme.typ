// Shared Typst theme for the v10 figure set (colours from the figure plan).
#let grey = rgb("#596052")
#let teal = rgb("#2A7F9E")
#let orange = rgb("#C8702A")
#let red = rgb("#B3261E")
#let green = rgb("#3C7A3E")
#let ink = rgb("#222222")
#let muted = rgb("#6B6F68")
#let rule = rgb("#D9DCD6")

#let grey-t = rgb("#ECEEEA")
#let teal-t = rgb("#E2EFF4")
#let orange-t = rgb("#FAEBDD")
#let green-t = rgb("#E6F0E5")

#let sans = ("Arial", "Liberation Sans")
#let serif = ("Times New Roman", "Liberation Serif")

#let fs-body = 7.5pt
#let fs-small = 7pt
#let fs-title = 9pt
#let fs-panel = 10pt

// Math typed as Times text runs (manuscript rule: labels Arial, math Times New Roman).
#let m(body) = text(font: serif, style: "italic", body)
#let mr(body) = text(font: serif, body)

#let panel(letter) = text(size: fs-panel, weight: "bold", fill: ink, letter)

#let setup(width, height: auto, body) = {
  set page(width: width, height: height, margin: 0pt, fill: white)
  set text(font: sans, size: fs-body, fill: ink, lang: "en")
  set par(leading: 0.45em, justify: false)
  body
}

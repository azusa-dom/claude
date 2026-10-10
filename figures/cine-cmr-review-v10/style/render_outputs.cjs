// Render one agarwood-scifig SVG to a print PDF and a high-resolution PNG with headless Chromium.
//   node render_outputs.cjs figure.svg out.pdf out.png width_mm png_width_px
// The SVG keeps its pixel viewBox; it is laid out at width_mm for the PDF (text stays text,
// fonts are embedded) and rasterised at png_width_px for the PNG.
const fs = require('fs');
const path = require('path');
const { chromium } = require(process.env.PW || 'playwright');

(async () => {
  const [, , src, pdfOut, pngOut, widthMmArg, pngWArg] = process.argv;
  const svg = fs.readFileSync(src, 'utf8');
  const head = svg.slice(0, 2000);
  const W = Number((head.match(/<svg[^>]*\swidth="([\d.]+)"/) || [])[1]);
  const H = Number((head.match(/<svg[^>]*\sheight="([\d.]+)"/) || [])[1]);
  if (!W || !H) throw new Error('SVG root needs numeric width/height attributes');
  const widthMm = Number(widthMmArg);
  const heightMm = widthMm * H / W;
  const browser = await chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});

  // PDF: same SVG, sized in millimetres on a page of exactly that size.
  const page = await browser.newPage();
  const sized = svg.replace(/(<svg[^>]*\s)width="[\d.]+"/, `$1width="${widthMm}mm"`)
                   .replace(/(<svg[^>]*\s)height="[\d.]+"/, `$1height="${heightMm.toFixed(3)}mm"`);
  await page.setContent(`<!doctype html><html><head><style>@page{size:${widthMm}mm ${heightMm.toFixed(3)}mm;margin:0}
    html,body{margin:0;padding:0;background:#fff}svg{display:block}</style></head><body>${sized}</body></html>`);
  await page.pdf({ path: pdfOut, width: `${widthMm}mm`, height: `${heightMm.toFixed(3)}mm`, printBackground: true,
                   margin: { top: 0, right: 0, bottom: 0, left: 0 }, pageRanges: '1' });
  await page.close();

  // PNG: rasterise at the requested pixel width.
  const scale = Number(pngWArg) / W;
  const p2 = await browser.newPage({ viewport: { width: Math.ceil(W), height: Math.ceil(H) }, deviceScaleFactor: scale });
  await p2.goto('file://' + path.resolve(src));
  await p2.screenshot({ path: pngOut, clip: { x: 0, y: 0, width: W, height: H } });
  await browser.close();
  console.log(`rendered ${path.basename(pdfOut)} (${widthMm} x ${heightMm.toFixed(1)} mm) and ${path.basename(pngOut)}`);
})();

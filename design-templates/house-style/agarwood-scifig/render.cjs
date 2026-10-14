// Rasterise an SVG to PNG with headless Chromium (Playwright), at the SVG's own size × scale.
//   node render.cjs figure.svg figure.png [scale=2]
// Env: PW = path to the playwright package (default: require('playwright')),
//      CHROME = Chromium executable (optional).
const fs = require('fs');
const path = require('path');
const { chromium } = require(process.env.PW || 'playwright');
(async () => {
  const [, , src, out, scaleArg] = process.argv;
  const head = fs.readFileSync(src, 'utf8').slice(0, 2000);
  const width = Math.ceil(Number((head.match(/<svg[^>]*\swidth="([\d.]+)/) || [])[1]));
  const height = Math.ceil(Number((head.match(/<svg[^>]*\sheight="([\d.]+)/) || [])[1]));
  if (!width || !height) throw new Error('SVG root needs numeric width/height attributes');
  const browser = await chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: Number(scaleArg || 2) });
  await page.goto('file://' + path.resolve(src));
  await page.screenshot({ path: out, clip: { x: 0, y: 0, width, height } });
  await browser.close();
  console.log(`rendered ${path.basename(out)} (${width * Number(scaleArg || 2)}×${height * Number(scaleArg || 2)} px)`);
})();

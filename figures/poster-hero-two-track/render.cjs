// Render the SVG figure to a 2x PNG: node render.cjs two_track_figure.svg two_track_figure.png
const path = require('path');
const { chromium } = require(process.env.PW || 'playwright');
(async () => {
  const [, , src, out] = process.argv;
  const browser = await chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
  const page = await browser.newPage({ viewport: { width: 1800, height: 1310 }, deviceScaleFactor: 2 });
  await page.goto('file://' + path.resolve(src));
  await page.screenshot({ path: out, clip: { x: 0, y: 0, width: 1800, height: 1310 } });
  await browser.close();
})();

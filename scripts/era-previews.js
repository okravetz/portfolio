// Share previews: one 1200 x 630 screenshot per era, saved as assets/eras/<slug>/og.png and named in each
// era page's <meta property="og:image"> (_includes/era-head.html). Rerun after an era's look changes:
//   bundle exec jekyll build -d /tmp/site && (cd /tmp/site && python3 -m http.server 4000 &)
//   node scripts/era-previews.js http://localhost:4000
// Needs Playwright (npm i playwright). The time-travel bar is hidden so the era itself is what shows.
const { chromium } = require("playwright");
const path = require("path");
const fs = require("fs");

const base = process.argv[2] || "http://localhost:4000";
const eras = ["1969", "1983", "1991", "1996", "2001", "2006", "2013", "future"];

(async () => {
  const browser = await chromium.launch();
  for (const era of eras) {
    const ctx = await browser.newContext({ viewport: { width: 1200, height: 630 }, reducedMotion: "reduce" });
    await ctx.addInitScript(() => {
      try { sessionStorage.setItem("intro-2001", "1"); } catch (e) {}
    });
    const page = await ctx.newPage();
    await page.goto(`${base}/${era}/`);
    await page.evaluate(() => document.fonts.ready);
    await page.addStyleTag({ content: "#time-travel,.tt-open{display:none!important}" });
    await page.waitForTimeout(400);
    const out = path.join(__dirname, "..", "assets", "eras", era, "og.png");
    fs.mkdirSync(path.dirname(out), { recursive: true });
    await page.screenshot({ path: out });
    console.log("wrote", out);
    await ctx.close();
  }
  await browser.close();
})();

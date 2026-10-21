// Exhaustive local document/link/asset audit. Uses the same optional setup as test_portal.cjs.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { createHash } = require('node:crypto');

(async () => {
  const browser = await chromium.launch({
    headless: true,
    ...(process.env.ACADEMY_BROWSER_PATH ? {executablePath: process.env.ACADEMY_BROWSER_PATH} : {})
  });
  try {
    const context = await browser.newContext({viewport: {width: 1440, height: 1000}, acceptDownloads: true});
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    const base = process.env.ACADEMY_TEST_URL || 'http://127.0.0.1:8765';
    const dist = process.env.ACADEMY_DIST_DIR || path.join(__dirname, '../dist');
    await page.goto(base);
    const inventory = await page.evaluate(() => ({
      documents: Object.keys(window.ACADEMY.documents),
      lessons: window.ACADEMY.curriculum.lessons,
      stages: window.ACADEMY.curriculum.stages,
      assets: window.ACADEMY.assets
    }));
    const links = new Set();
    let occurrences = 0;
    for (const doc of inventory.documents) {
      await page.goto(base + '/#doc=' + encodeURIComponent(doc));
      await page.locator('.reading').waitFor();
      await page.waitForFunction(name => document.querySelector('#download-doc')?.dataset.path === name, doc);
      assert.ok((await page.locator('.reading').innerText()).trim().length, doc);
      if(doc.startsWith('content/guide/'))await page.getByText('Keep a question or note · optional',{exact:true}).click();
      const [download] = await Promise.all([
        page.waitForEvent('download').catch(error => { throw Error(`Markdown download failed: ${doc}: ${error.message}`); }),
        page.locator('#download-doc').click()
      ]);
      assert.equal(fs.readFileSync(await download.path(), 'utf8'),
        await page.evaluate(name => window.ACADEMY.documents[name].text, doc),
        `Markdown download differs: ${doc}`);
      // Chromium limits burst downloads; pace this bulk audit like individual saves.
      await page.waitForTimeout(250);
      const hrefs = await page.locator('.reading a').evaluateAll(nodes => nodes.map(n => n.getAttribute('href')));
      for (const href of hrefs) {
        assert.ok(href && href !== '#', `Unresolved link in ${doc}: ${href}`);
        if (!/^https?:/.test(href)) { links.add(href); occurrences++; }
      }
    }
    for (const href of links) {
      if (href.startsWith('#doc=')) {
        await page.goto(base + '/' + href);
        await page.locator('.reading').waitFor();
        const anchor = new URLSearchParams(href.slice(1)).get('section');
        if (anchor) {
          await page.waitForFunction(id => document.activeElement?.id === id, anchor);
          assert.equal(await page.evaluate(id => !!document.getElementById(id), anchor), true, href);
        }
      } else {
        const response = await context.request.get(base + '/' + href);
        assert.equal(response.status(), 200, href);
      }
    }
    for (const lesson of inventory.lessons) {
      await page.goto(base + '/#lesson=' + lesson.id);
      await page.locator('[data-answer]').first().waitFor();
      await page.waitForFunction(id => document.querySelector('#mark-done')?.dataset.id === id, lesson.id);
      assert.equal(await page.locator('.reading h2').filter({hasText: /^Exercise [123]/}).count(), 3, lesson.id);
      for (let answer = 0; answer < lesson.quiz.options.length; answer++) {
        await page.locator(`[data-answer="${answer}"]`).click();
        const expected = answer === lesson.quiz.answer ? 'Correct.' : 'Try again.';
        assert.equal(await page.locator('.quiz-feedback strong').textContent(), expected, lesson.id);
      }
      const index = inventory.lessons.indexOf(lesson);
      const next = index + 1 < inventory.lessons.length ? '#lesson=' + inventory.lessons[index + 1].id : '#capstones';
      assert.equal(await page.locator('.reading-side .side-block').first().locator('a.btn').getAttribute('href'), next);
    }
    for (const stage of inventory.stages) {
      await page.goto(base + '/#stage=' + stage.id);
      await page.locator('.lesson-row').first().waitFor();
      assert.equal(await page.locator('.lesson-row').count(), 3, 'Stage ' + stage.id);
      await page.getByRole('link', {name:'Readings and courses', exact:false}).click();
      await page.locator('#resource-stage').waitFor();
      assert.equal(await page.locator('#resource-stage').inputValue(), String(stage.id));
    }
    for (const asset of [...inventory.assets, 'fieldbook.pdf', 'academy-source.zip', 'academy-portable.zip']) {
      const response = await context.request.get(base + '/' + asset);
      assert.equal(response.status(), 200, asset);
      const local = fs.readFileSync(path.join(dist, asset));
      const hash = bytes => createHash('sha256').update(bytes).digest('hex');
      assert.equal(hash(await response.body()), hash(local), `Download differs: ${asset}`);
    }
    for (const doc of inventory.documents) {
      await page.setViewportSize({width:390, height:844});
      await page.goto(base + '/#doc=' + encodeURIComponent(doc));
      await page.locator('.reading').waitFor();
      await page.waitForFunction(name => document.querySelector('#download-doc')?.dataset.path === name, doc);
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `Mobile overflow: ${doc}`);
    }
    assert.deepEqual(errors, []);
    console.log(JSON.stringify({
      documents: inventory.documents.length,
      markdownDownloads: inventory.documents.length,
      internalLinkOccurrences: occurrences,
      uniqueInternalLinks: links.size,
      lessons: inventory.lessons.length,
      stages: inventory.stages.length,
      quizAnswers: inventory.lessons.reduce((n, l) => n + l.quiz.options.length, 0),
      downloadedAssets: inventory.assets.length + 3,
      mobileDocuments: inventory.documents.length,
      pageErrors: errors.length
    }));
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exit(1); });

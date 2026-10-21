// Optional hosted-mode browser checks. Supply Playwright through NODE_PATH;
// serve dist with a static HTTP server (see docs/MAINTENANCE.md).
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
(async () => {
 const browser = await chromium.launch({headless:true,...(process.env.ACADEMY_BROWSER_PATH?{executablePath:process.env.ACADEMY_BROWSER_PATH}:{})});
 try {
 const context = await browser.newContext({viewport:{width:1440,height:1100},acceptDownloads:true});
 const page = await context.newPage();
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const base=process.env.ACADEMY_TEST_URL||'http://127.0.0.1:8765';
 const response=await page.goto(base);
 assert.equal(response.status(),200,'The configured ACADEMY_TEST_URL must serve the built portal');
 // Accessible whitespace around <br> differs across Chromium builds.
 await page.getByRole('heading',{name:'Learn AI, one clear step at a time.'}).waitFor();
 fs.mkdirSync(path.join(__dirname,'../tmp/qa'),{recursive:true});
 await page.screenshot({path:path.join(__dirname,'../tmp/qa/overview.png'),fullPage:true});
 await page.locator('.skip').focus();await page.keyboard.press('Enter');
 assert.equal(await page.locator('h1').textContent(),'Learn AI, one clear step at a time.');
 await page.getByRole('link',{name:'Start reading',exact:false}).click();
 await page.locator('.beginner-guide h1').waitFor();
 await page.goto(base+'/#lesson=01');
 await page.locator('.reading h1').waitFor();
 await page.locator('#notes').fill('QA note: prediction, observation, next change.');
 await page.locator('#mark-done').click();
 await page.locator('[data-answer="0"]').click();
 assert.equal(await page.locator('.quiz-feedback').count(),1);
 await page.reload();await page.locator('#notes').waitFor();
 assert.equal(await page.locator('#notes').inputValue(),'QA note: prediction, observation, next change.');
 assert.match(await page.locator('#mark-done').textContent(),/Completed/);
 await page.screenshot({path:path.join(__dirname,'../tmp/qa/lesson.png'),fullPage:true});
 await page.goto(base+'/#library');await page.locator('#resource-search').fill('Hugging Face');
 assert.ok(await page.locator('.resource').count()>=3);
 await page.locator('.save').first().click();await page.locator('#saved-only').click();
 assert.equal(await page.locator('.resource').count(),1);
 await page.goto(base+'/#workbench');await page.locator('#scenario').selectOption('injection');await page.locator('#sim-run').click();
 assert.match(await page.locator('#trace').textContent(),/DENY/);
 await page.locator('#scenario').selectOption('duplicate');await page.locator('#sim-run').click();
 assert.match(await page.locator('#trace').textContent(),/1 drafts created/);
 await page.locator('#budget').fill('1');await page.locator('#sim-run').click();
 assert.match(await page.locator('#trace').textContent(),/budget exhausted/);
 await page.goto(base+'/#progress');assert.equal(await page.getByRole('link',{name:/Using another account/}).getAttribute('href'),'#doc=docs%2FNEW-ACCOUNT.md');assert.equal(await page.getByRole('link',{name:/Download portable academy/}).getAttribute('href'),'academy-portable.zip');await page.locator('[data-gate="1"]').check();
 const exported=page.waitForEvent('download');await page.locator('#export').click();const dl=await exported;const file=await dl.path();const state=JSON.parse(fs.readFileSync(file,'utf8'));assert.deepEqual(state.done,['01']);assert.ok(state.gates.includes(1));
 const choosing=page.waitForEvent('filechooser');await page.locator('#import-progress').focus();await page.keyboard.press('Enter');
 const chooser=await choosing;await chooser.setFiles({name:'progress.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify({...state,done:['01','02'],notes:{...state.notes,'content/lessons/01-systems-before-agents.md':'A note from another device.'}}))});
 await page.waitForFunction(()=>document.querySelector('.stat strong').textContent.startsWith('2/'));
 for(const route of ['path','labs','manuals','capstones']) {await page.goto(base+'/#'+route);await page.locator('h1').waitFor();assert.ok(!await page.getByText('That page is not in this edition.').count());}
 await page.goto(base+'/#labs');
 assert.equal(await page.locator('.doc-card').count(),await page.evaluate(()=>Object.keys(window.ACADEMY.documents).filter(p=>/^content\/labs\/\d{2}-[^/]+\.md$/.test(p)).length));
 for(const guide of ['09-real-mcp.md','10-installed-skill.md','11-complete-student-harness.md']) {
  await page.goto(base+'/#doc='+encodeURIComponent('content/labs/'+guide));
  await page.locator('.reading h1').waitFor();
  assert.ok((await page.locator('.reading').innerText()).length>1500,guide);
 }
 await page.screenshot({path:path.join(__dirname,'../tmp/qa/integrated-harness.png'),fullPage:true});
 await page.goto(base+'/#lesson=01');await page.locator('#notes').waitFor();
 assert.match(await page.locator('#notes').inputValue(),/QA note:[\s\S]*Imported backup[\s\S]*another device/);
 await page.goto(base+'/#doc=content%2Flabs%2F08-ship-an-evaluated-policy.md');
 await page.getByRole('link',{name:'Solution discussion',exact:true}).click();
 await page.waitForFunction(()=>document.activeElement?.id==='lab-08');
 assert.match(page.url(),/&section=lab-08$/);
 assert.equal(await page.locator('.reading a[href="content/labs/solutions/reference.py"]').count(),1);
 const solution=await context.request.get(base+'/content/labs/solutions/reference.py');assert.equal(solution.status(),200);assert.match(await solution.text(),/def /);
 await page.goto(base+'/#doc=%');await page.getByRole('heading',{name:'That page is not in this edition.'}).waitFor();
 await page.goto(base+'/#doc=content%2Flibrary%2FREADME.md');
 assert.equal(await page.locator('.reading a[href="content/resources.json"]').count(),1);
 await page.setViewportSize({width:390,height:844});await page.goto(base+'/#overview');
 assert.ok(await page.locator('#export').isVisible());
 assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth));
 await page.screenshot({path:path.join(__dirname,'../tmp/qa/mobile.png'),fullPage:true});
 for(const asset of ['fieldbook.pdf','academy-source.zip','academy-portable.zip','content/resources.json','lab/composed.py','lab/mcp_lab/server.py','content/skill-practice/signal-desk-evidence-review/scripts/check_packet.py']) {const r=await context.request.get(base+'/'+asset);assert.equal(r.status(),200,asset);}
 assert.deepEqual(errors,[]);
 console.log('Browser checks passed: navigation, skip link, quiz, notes persistence, completion, search, bookmarks, simulator, keyboard progress import/export, conflicting notes, solution links and section focus, malformed routes, mobile layout, downloads.');
 } finally { await browser.close(); }
})().catch(e=>{console.error(e);process.exit(1);});

// Learner workflow tests. Serve dist first; NODE_PATH supplies optional Playwright.
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
(async()=>{
 const browser=await chromium.launch({headless:true,...(process.env.ACADEMY_BROWSER_PATH?{executablePath:process.env.ACADEMY_BROWSER_PATH}:{})});
 try{
  const context=await browser.newContext({viewport:{width:1440,height:1100},acceptDownloads:true});
  const page=await context.newPage(),errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  const base=process.env.ACADEMY_TEST_URL||'http://127.0.0.1:8765';
  await page.goto(base);
  await page.getByRole('link',{name:'Start learning',exact:false}).click();
  await page.getByRole('heading',{name:'Prepare for your first attempt.'}).waitFor();
  await page.locator('[name="learning-route"][value="local"]').check();
  await page.locator('[data-prep="diagram"]').check();await page.locator('[data-prep="evidence"]').check();
  await page.getByRole('link',{name:'Try the first relationship'}).click();
  await page.locator('[data-workspace="L01-E1"]').waitFor();
  assert.equal(await page.locator('.requested-hint').count(),0);
  assert.equal(await page.locator('#exercise-step option').count(),5);
  await page.locator('#exercise-attempt').fill('Ticket input → evidence retrieval. The ticket description crosses the boundary.');
  await page.locator('#save-attempt').click();
  await page.locator('#exercise-attempt').fill('Revision: include product version and observed symptoms with the ticket.');
  await page.locator('#exercise-artifacts').fill('worksheet.txt; manually reviewed at first checkpoint');
  await page.locator('#exercise-minutes').fill('12');
  await page.locator('#save-attempt').click();
  await page.locator('#exercise-feedback').fill('Tutor: data label is concrete. Explain which facts remain unknown.');
  await page.locator('#exercise-basis').selectOption('tutor');
  await page.locator('#exercise-misconception').fill('I sometimes treat a proposed action as an executed effect.');
  await page.locator('#exercise-status').selectOption('needs-revision');
  await page.locator('#save-feedback').click();
  await page.reload();await page.locator('#exercise-attempt').waitFor();
  assert.match(await page.locator('#exercise-attempt').inputValue(),/^Revision:/);
  assert.match(await page.locator('#exercise-feedback').inputValue(),/facts remain unknown/);
  assert.equal(await page.locator('#exercise-minutes').inputValue(),'12');
  assert.equal(await page.locator('#exercise-status').inputValue(),'needs-revision');
  const attempts=await page.evaluate(()=>JSON.parse(localStorage.getItem('ai-engineering-academy-v1')).exercises['L01-E1'].history.filter(x=>x.kind==='attempt'));
  assert.equal(attempts.length,2);assert.match(attempts[0].attempt,/Ticket input/);assert.match(attempts[1].attempt,/Revision/);
  await page.locator('#request-hint').click();assert.equal(await page.locator('.requested-hint').count(),1);
  await page.locator('#tutor-packet').click();
  const packet=await page.locator('#packet-text').inputValue();
  assert.match(packet,/Revision:/);assert.match(packet,/Pass criteria/);
  const hints=await page.evaluate(()=>window.ACADEMY.learning.exercises[0].hints);
  for(const hint of hints)assert.ok(!packet.includes(hint));
  const packetDownload=page.waitForEvent('download');await page.locator('#download-packet').click();
  assert.equal(fs.readFileSync(await (await packetDownload).path(),'utf8'),packet);
  await page.locator('#queue-mistake').click();
  await page.locator('#exercise-step').selectOption('L01-E1-2');
  assert.equal(await page.locator('#exercise-attempt').inputValue(),'');
  await page.locator('#exercise-attempt').fill('Second step draft');
  await page.locator('#exercise-step').selectOption('L01-E1-1');
  assert.match(await page.locator('#exercise-attempt').inputValue(),/^Revision:/);
  await page.goto(base+'/#overview');await page.locator('.next-action a').click();
  await page.locator('[data-workspace="L01-E1"]').waitFor();
  await page.goto(base+'/#retention');
  assert.equal(await page.locator('.recall-card').count(),1);
  await page.locator('.recall-card textarea').fill('In a library system, a tool response confirming the saved record establishes the effect; a suggestion does not.');
  await page.locator('[data-outcome="difficult"]').click();
  await page.locator('.recall-card').waitFor();
  assert.match(await page.locator('.recall-card').innerText(),/difficult/);
  await page.locator('#review-intervals').fill('2, 4, 8, 16');await page.locator('#save-intervals').click();
  await page.goto(base+'/#exercise=L01-C1');
  await page.locator('#exercise-attempt').fill('The list was not saved: the tool returned permission_denied.');
  await page.locator('#save-attempt').click();
  await page.locator('#exercise-feedback').fill('Self-review: I grounded completion in the tool result.');
  await page.locator('#exercise-status').selectOption('reviewed');await page.locator('#save-feedback').click();
  const output=page.waitForEvent('download');await page.locator('#export').click();
  const exported=JSON.parse(fs.readFileSync(await (await output).path(),'utf8'));
  assert.equal(exported.version,2);assert.equal(exported.route,'local');
  assert.equal(exported.retention[0].history.length,1);assert.equal(exported.exercises['L01-E1'].history.filter(x=>x.kind==='attempt').length,2);
  const imported=JSON.parse(JSON.stringify(exported));
  imported.exercises['L01-E1'].draft.attempt='A conflicting draft from a second device';
  const choose=page.waitForEvent('filechooser');await page.locator('#import-progress').click();
  await (await choose).setFiles({name:'learning.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(imported))});
  await page.waitForFunction(()=>document.querySelector('#toast').textContent.includes('Progress merged'));
  const restored=await page.evaluate(()=>JSON.parse(localStorage.getItem('ai-engineering-academy-v1')));
  assert.ok(restored.exercises['L01-E1'].history.some(x=>x.attempt==='A conflicting draft from a second device'));
  assert.match(restored.exercises['L01-E1'].draft.attempt,/Revision/);
  assert.deepEqual(restored.retention,exported.retention);
  for(let n=1;n<=8;n++){
   await page.goto(base+'/#doc='+encodeURIComponent(`content/labs/hints/${String(n).padStart(2,'0')}.md`));
   const details=page.locator('details.progressive-hint');await details.first().waitFor();
   assert.equal(await details.count(),3);
   for(let i=0;i<3;i++){assert.equal(await details.nth(i).getAttribute('open'),null);assert.equal(await details.nth(i).locator('p').first().isVisible(),false);}
   await details.first().locator('summary').focus();await page.keyboard.press('Enter');
   assert.equal(await details.first().locator('p').first().isVisible(),true);
   assert.equal(await details.nth(1).locator('p').first().isVisible(),false);
   assert.equal(await details.nth(2).locator('p').first().isVisible(),false);
  }
  const walkthroughs=await page.evaluate(()=>window.ACADEMY.learning.walkthroughs);
  assert.equal(walkthroughs.length,8);
  for(const w of walkthroughs){
   await page.goto(base+'/#walkthrough='+encodeURIComponent(w.id));
   for(let i=0;i<w.steps.length;i++){
    await page.locator('.walkthrough').waitFor();
    if(w.steps[i].pause)await page.locator('#walkthrough-answer').fill('My prediction for this unrelated example.');
    if(i<w.steps.length-1)await page.locator('[data-slide="1"]').click();
   }
  }
  const screenshots=path.join(__dirname,'../tmp/qa');fs.mkdirSync(screenshots,{recursive:true});
  await page.goto(base+'/#exercise=L01-E1');await page.screenshot({path:path.join(screenshots,'learning-workspace.png'),fullPage:true});
  await page.setViewportSize({width:390,height:844});
  for(const route of ['prepare','exercise=L01-E1','retention','progress']){
   await page.goto(base+'/#'+route);await page.locator('h1').waitFor();
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth),route);
  }
  await page.screenshot({path:path.join(screenshots,'learning-mobile.png'),fullPage:true});
  const legacyContext=await browser.newContext();
  await legacyContext.addInitScript(()=>localStorage.setItem('ai-engineering-academy-v1',JSON.stringify({version:1,done:['01'],notes:{'docs/START-HERE.md':'Legacy note'},quiz:{'01':1},gates:[],bookmarks:[]})));
  const legacy=await legacyContext.newPage();await legacy.goto(base+'/#lesson=01');
  assert.match(await legacy.locator('#mark-done').textContent(),/Completed/);
  await legacy.goto(base+'/#doc=docs%2FSTART-HERE.md');
  assert.equal(await legacy.locator('#notes').inputValue(),'Legacy note');
  assert.deepEqual(errors,[]);
  console.log(`Learning browser checks passed: preparation/routes, attempts/revisions/feedback, spoiler-free tutor packet download, step resume, applied check, recall scheduling, full export/import conflict preservation, all 8 keyboard-operated hint pages, ${walkthroughs.length} walkthroughs, mobile layouts, and v1 migration.`);
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1);});

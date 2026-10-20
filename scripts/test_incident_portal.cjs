// Serve dist first. Optional Playwright lives on NODE_PATH in the bundled runtime.
'use strict';
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');

(async()=>{
 const browser=await chromium.launch({headless:true,...(process.env.ACADEMY_BROWSER_PATH?{executablePath:process.env.ACADEMY_BROWSER_PATH}:{})});
 const base=process.env.ACADEMY_TEST_URL||'http://127.0.0.1:8765';
 const errors=[];
 try{
  const context=await browser.newContext({viewport:{width:1440,height:1100},acceptDownloads:true});
  const page=await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base+'/#incidents');
  await page.locator('.incident-card').first().waitFor();
  assert.equal(await page.locator('.incident-card').count(),7);
  const cases=await page.evaluate(()=>window.ACADEMY.incidents.incidents.map(x=>({id:x.id,briefPath:x.briefPath})));
  for(const item of cases){
   await page.goto(base+'/#incident='+item.id);
   await page.locator('[data-workspace="'+item.id+'"]').waitFor();
   assert.equal(await page.locator('#incident-hint').isDisabled(),true,item.id);
   assert.equal(await page.locator('#incident-debrief').isDisabled(),true,item.id);
   assert.equal(await page.locator('.requested-hint,.incident-debrief').count(),0,item.id);
   await page.locator('#tutor-packet').click();
   const packet=await page.locator('#packet-text').inputValue();
   assert.match(packet,/No attempt yet/);
   const guidance=await page.evaluate(id=>{
    const x=window.ACADEMY.incidents.incidents.find(x=>x.id===id);
    return [...x.hints,x.debrief];
   },item.id);
   for(const text of guidance)assert.ok(!packet.includes(text),'Packet leaked guidance: '+item.id);
   await page.goto(base+'/#doc='+encodeURIComponent(item.briefPath));
   await page.locator('article.reading').waitFor();
   assert.equal(await page.locator('.requested-hint,.incident-debrief').count(),0);
  }
  // An encoded direct-document route cannot turn the guidance JSON into a page.
  await page.goto(base+'/#doc=content%2Fincidents.json');
  await page.getByRole('heading',{name:'That page is not in this edition.'}).waitFor();
  await page.goto(base+'/#exercise=INC-01');
  await page.locator('[data-workspace="INC-01"]').waitFor();
  assert.equal(await page.locator('#incident-debrief').isDisabled(),true);
  await page.locator('#exercise-attempt').fill('   ');
  await page.locator('#save-attempt').click();
  assert.match(await page.locator('#toast').textContent(),/substantive incident attempt/);
  assert.equal(await page.locator('#incident-hint').isDisabled(),true);

  const attempt='The report may describe another revision; an alternative is that this environment collected different checks.';
  const evidence='Saved baseline.txt: the command, revision and observed test count remain in the evidence log.';
  const nextCheck='Compare the executed command and its discovered tests against the captured baseline.';
  await page.locator('#exercise-attempt').fill(attempt);
  await page.locator('#exercise-artifacts').fill(evidence);
  await page.locator('#exercise-nextCheck').fill(nextCheck);
  await page.reload();
  await page.locator('#exercise-nextCheck').waitFor();
  assert.equal(await page.locator('#exercise-nextCheck').inputValue(),nextCheck);
  assert.equal(await page.locator('#incident-hint').isDisabled(),true,'Draft alone unlocked hints');
  await page.locator('#exercise-feedback').fill('Self-review: I have a candidate explanation but have not saved an incident attempt.');
  await page.locator('#save-feedback').click();
  assert.equal(await page.locator('#incident-hint').isDisabled(),true,'Feedback alone unlocked hints');
  await page.locator('#save-attempt').click();
  assert.equal(await page.locator('#incident-hint').isDisabled(),false);
  assert.equal(await page.locator('.requested-hint,.incident-debrief').count(),0,'Saving exposed guidance');
  await page.locator('#incident-hint').click();
  assert.equal(await page.locator('[data-incident-hint="1"]').count(),1);
  assert.equal(await page.locator('.incident-debrief').count(),0);
  await page.locator('#incident-hint').click();
  assert.equal(await page.locator('[data-incident-hint="2"]').count(),1);
  assert.equal(await page.locator('.incident-debrief').count(),0);
  await page.locator('#incident-debrief').click();
  assert.equal(await page.locator('.incident-debrief').count(),1);
  await page.locator('#tutor-packet').click();
  const packet=await page.locator('#packet-text').inputValue();
  assert.ok(packet.includes(nextCheck));
  const allGuidance=await page.evaluate(()=>{
   const x=window.ACADEMY.incidents.incidents[0];return [...x.hints,x.debrief,x.transfer];
  });
  for(const text of allGuidance)assert.ok(!packet.includes(text));
  await page.reload();
  await page.locator('#incident-hint').waitFor();
  assert.equal(await page.locator('.requested-hint,.incident-debrief').count(),0,'Reload revealed guidance');
  assert.equal(await page.locator('#incident-hint').isDisabled(),false);
  await page.locator('#incident-debrief').click();
  await page.locator('#exercise-attempt').fill(attempt+' I will preserve the output before rerunning.');
  await page.locator('#save-attempt').click();
  assert.equal(await page.locator('.requested-hint,.incident-debrief').count(),0,'Saving a revision left guidance open');
  await page.locator('#exercise-attempt').fill(attempt+' </textarea><img src=x onerror="window.incidentXss=true">');
  await page.locator('#save-attempt').click();
  assert.equal(await page.locator('.exercise-main img').count(),0);
  assert.equal(await page.evaluate(()=>window.incidentXss),undefined);

  const download=page.waitForEvent('download');
  await page.locator('#export').click();
  const exported=JSON.parse(fs.readFileSync(await (await download).path(),'utf8'));
  assert.equal(exported.version,2);
  assert.equal(exported.exercises['INC-01'].history.filter(x=>x.kind==='attempt').length,3);
  assert.equal(exported.exercises['INC-01'].draft.nextCheck,nextCheck);

  const importedContext=await browser.newContext({viewport:{width:390,height:844}});
  const imported=await importedContext.newPage();
  imported.on('pageerror',e=>errors.push(e.message));
  await imported.goto(base+'/#incident=INC-01');
  await imported.locator('#incident-hint').waitFor();
  assert.equal(await imported.locator('#incident-hint').isDisabled(),true);
  const chooser=imported.waitForEvent('filechooser');
  await imported.locator('#import-progress').click();
  await (await chooser).setFiles({name:'incident-progress.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(exported))});
  await imported.waitForFunction(()=>document.querySelector('#toast').textContent.includes('Progress merged'));
  assert.equal(await imported.locator('#incident-hint').isDisabled(),false);
  assert.equal(await imported.locator('#exercise-nextCheck').inputValue(),nextCheck);
  assert.equal(await imported.locator('.requested-hint,.incident-debrief').count(),0,'Import revealed guidance');
  await imported.locator('#incident-debrief').click();
  await imported.locator('.incident-debrief').waitFor();
  const overflow=await imported.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth+2);
  assert.equal(overflow,false,'Mobile incident view overflows horizontally');
  const screenshot=path.join(__dirname,'../work/incident-portal-mobile.png');
  fs.mkdirSync(path.dirname(screenshot),{recursive:true});
  await imported.screenshot({path:screenshot,fullPage:true});
  await imported.goto(base+'/#incidents');
  await imported.locator('.incident-card').first().waitFor();
  await imported.goto(base+'/#incident=INC-01');
  await imported.locator('#incident-hint').waitFor();
  assert.equal(await imported.locator('.requested-hint,.incident-debrief').count(),0,'Revisiting revealed guidance');
  assert.deepEqual(errors,[]);
  console.log('PASS: 7 incident routes, attempt gates, progressive hints, deliberate debrief, spoiler-free packets, saved revisions, export/import, XSS escaping, and mobile layout.');
 }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});

// Fresh-learner navigation and persistence; isolated browser context only.
'use strict';
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
(async()=>{
 const browser=await chromium.launch({headless:true,...(process.env.ACADEMY_BROWSER_PATH?{executablePath:process.env.ACADEMY_BROWSER_PATH}:{})});
 try{
  const context=await browser.newContext({viewport:{width:1440,height:1000},acceptDownloads:true});
  const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
  const base=process.env.ACADEMY_TEST_URL||'http://127.0.0.1:8792',key='ai-engineering-academy-v1';
  assert.equal((await page.goto(base)).status(),200);
  await page.getByRole('heading',{name:'Learn AI, one clear step at a time.'}).waitFor();
  assert.equal(await page.locator('#nav .nav-stage').count(),8);
  assert.equal(await page.locator('#nav .nav-lesson').count(),24);
  const original=await page.evaluate(k=>localStorage.getItem(k),key);
  await page.goto(base+'/#guide=01');
  await page.locator('.guide-source a').waitFor();
  await page.getByRole('heading',{name:'What AI can do for an SDET',exact:true}).waitFor();
  assert.equal(await page.locator('#exercise-attempt,#mark-done,[data-answer]').count(),0);
  assert.equal(await page.locator('.guide-extra[open]').count(),0);
  assert.equal(await page.locator('.guide-source a').count(),1);
  assert.equal(await page.locator('.guide-source a').getAttribute('target'),'_blank');
  fs.mkdirSync(path.join(__dirname,'../tmp/qa'),{recursive:true});
  await page.screenshot({path:path.join(__dirname,'../tmp/qa/sdet-first-topic.png'),fullPage:true});
  const topics=await page.evaluate(()=>window.ACADEMY.guide.topics);
  for(let i=0;i<topics.length;i++){
   await page.getByRole('heading',{name:topics[i].title,exact:true}).waitFor();
   assert.equal(await page.locator('.guide-source a').getAttribute('href'),topics[i].resource.url);
   const related=page.locator('.guide-extra').filter({has:page.locator('summary',{hasText:'Related material'})});
   await related.locator('summary').click();
   for(const target of topics[i].practice){
    const encoded='#doc='+encodeURIComponent(target);
    assert.equal(await related.locator(`a[href="${encoded}"]`).count(),1,target);
   }
   await related.locator('summary').click();
   if(i<topics.length-1)await page.getByRole('link',{name:'Next topic:',exact:false}).click();
  }
  assert.equal(await page.evaluate(k=>localStorage.getItem(k),key),original,'Reading never writes completion or practice records');
  await page.goto(base+'/#guide=04');await page.locator('#save-reading').click();
  await page.getByText('Keep a question or note · optional',{exact:true}).click();
  await page.locator('#notes').fill('How should a grader be calibrated?');
  await page.goto(base+'/#overview');await page.getByRole('link',{name:'Resume reading',exact:false}).click();
  assert.equal(new URL(page.url()).hash,'#guide=04');
  await page.reload();await page.locator('#save-reading').waitFor();
  await page.getByText('Keep a question or note · optional',{exact:true}).click();
  assert.equal(await page.locator('#notes').inputValue(),'How should a grader be calibrated?');
  const record=await page.evaluate(k=>JSON.parse(localStorage.getItem(k)),key);
  assert.equal(record.reading,'04');assert.deepEqual(record.done,[]);assert.deepEqual(record.exercises,{});
  const [download]=await Promise.all([page.waitForEvent('download'),page.locator('#export').click()]);
  const exported=JSON.parse(fs.readFileSync(await download.path(),'utf8'));assert.equal(exported.reading,'04');
  // Import into a new browser must carry both reading position and notes.
  const second=await browser.newContext(),importPage=await second.newPage();
  await importPage.goto(base);await importPage.getByRole('link',{name:'Start reading',exact:false}).waitFor();
  await importPage.locator('#import').setInputFiles({name:'progress.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(exported))});
  await importPage.getByRole('link',{name:'Resume reading',exact:false}).click();
  assert.equal(new URL(importPage.url()).hash,'#guide=04');await second.close();
  // Existing deep links still show all original material and a route back to the guide.
  await page.goto(base+'/#lesson=01');await page.locator('.beginner-guide').waitFor();
  assert.match(await page.locator('.reading').innerText(),/Exercise 1/);
  await page.goto(base+'/#path');await page.locator('.lesson-row').first().waitFor();
  assert.equal(await page.locator('.lesson-row').count(),24);
  await page.goto(base+'/#labs');await page.locator('.doc-card').first().waitFor();
  assert.equal(await page.locator('.doc-card').count(),15);
  // Keyboard and narrow-screen checks on the new reading flow.
  await page.setViewportSize({width:390,height:844});
  for(const route of ['#overview','#guide',...topics.map(t=>'#guide='+t.id)]){
   await page.goto(base+'/'+route);await page.waitForFunction(()=>document.querySelector('#main h1'));
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth+1),route+' overflows');
  }
  await page.goto(base+'/#guide=01');
  const more=page.locator('.guide-extra summary').first();await more.focus();await page.keyboard.press('Enter');
  assert.notEqual(await page.locator('.guide-extra').first().getAttribute('open'),null);
  await page.screenshot({path:path.join(__dirname,'../tmp/qa/sdet-mobile.png'),fullPage:true});
  assert.deepEqual(errors,[]);
  console.log('PASS: fresh entry, all eight topics, scoped sources, preserved practice indexes, no automatic completion, reading place/notes reload, export/import, keyboard and mobile');
 }finally{await browser.close()}
})().catch(error=>{console.error(error);process.exitCode=1});

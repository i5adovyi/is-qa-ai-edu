// Subject-first learning: fresh start, every track/topic, explicit progress, and mobile.
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
  await page.goto(base);await page.locator('.track-card').first().waitFor();
  const inventory=await page.evaluate(()=>({tracks:ACADEMY.tracks,paths:ACADEMY.paths,documents:ACADEMY.documents}));
  assert.equal(inventory.tracks.length,14);assert.equal(await page.locator('.nav-track').count(),14);
  assert.equal(await page.locator('#main .track-card').count(),14);
  const before=await page.evaluate(()=>JSON.stringify(state));
  await page.locator('#main .first-topic a.btn').first().click();assert.equal(new URL(page.url()).hash,'#start');
  await page.getByRole('link',{name:'Start the first topic',exact:false}).click();await page.locator('#save-topic-reading').waitFor();
  assert.equal(new URL(page.url()).hash,'#topic=foundations-orientation?path=zero');
  // Each path uses its own order, including subject transitions.
  for(const p of inventory.paths){
   await page.goto(base+'/#learn='+p.id);await page.locator('#main .topic-row').first().waitFor();
   assert.equal(await page.locator('#main .topic-row').count(),p.topics.length);
   await page.getByRole('link',{name:'Begin this path',exact:false}).click();
   for(let i=0;i<p.topics.length;i++){
    await page.waitForFunction(id=>document.querySelector('#save-topic-reading')?.dataset.id===id,p.topics[i]);
    assert.equal(await page.locator('#save-topic-reading').getAttribute('data-path'),p.id);
    const next=page.locator('.topic-next').first().locator('a.btn');
    assert.equal(await next.getAttribute('href'),i+1<p.topics.length?'#topic='+p.topics[i+1]+'?path='+p.id:'#path');
    if(i+1<p.topics.length)await next.click();
   }
  }
  // Every subject's level sections, teaching pages, selected source and mobile width.
  const all=inventory.tracks.flatMap(t=>t.lessons);
  for(const t of inventory.tracks){
   await page.goto(base+'/#track='+t.id);await page.locator('.track-level').first().waitFor();
   assert.equal(await page.locator('.track-level').count(),3);assert.equal(await page.locator('#main .topic-row').count(),t.lessons.length);
   assert.equal(await page.locator('.nav-track[aria-current="page"]').getAttribute('data-track'),t.id);
   for(let i=0;i<t.lessons.length;i++){
    const topic=t.lessons[i];await page.goto(base+'/#topic='+topic.id);await page.locator('#save-topic-reading').waitFor();
    assert.equal(await page.locator('.nav-topic[aria-current="page"]').getAttribute('data-topic'),topic.id);
    for(const heading of ['start-here','the-idea-in-plain-language','a-small-example','try-it-with-codex-or-claude-code','what-you-should-see','if-it-goes-wrong','go-deeper','optional-practice'])assert.equal(await page.locator('.beginner-guide #'+heading).count(),1,topic.id+' '+heading);
    assert.equal(await page.locator('.topic-materials .guide-source a').getAttribute('href'),topic.resource.url);
    if(topic.lesson){assert.equal(await page.locator('#original-lesson h2').filter({hasText:/^Exercise [123]/}).count(),3);assert.ok(await page.locator('#reveal-lesson-solution').isDisabled());}
    assert.equal(await page.locator('.topic-next').first().locator('a.btn').getAttribute('href'),i+1<t.lessons.length?'#topic='+t.lessons[i+1].id:'#path');
    await page.setViewportSize({width:390,height:844});assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),topic.id+' mobile overflow');await page.setViewportSize({width:1440,height:1000});
   }
  }
  assert.equal(all.length,84);assert.equal(await page.evaluate(()=>JSON.stringify(state)),before,'Reading must never mutate progress');
  // Contextual detours, source downloads, searchable new terminology and sidebar reset.
  await page.goto(base+'/#topic=mcp-basics?path=builder');
  await page.locator('.reading-side').getByRole('link',{name:'How to use Codex or Claude Code',exact:false}).click();await page.locator('.reading-return').waitFor();
  assert.equal(await page.locator('.reading-return a.btn').getAttribute('href'),'#topic=mcp-basics?path=builder');
  await page.locator('.reading-return a.btn').click();await page.locator('#save-topic-reading').waitFor();
  await page.locator('#site-map-search').fill('cancellation');assert.ok(await page.locator('.nav-topic[data-topic="harness-cancellation"]').isVisible());await page.locator('.nav-topic[data-topic="harness-cancellation"]').click();assert.equal(await page.locator('#site-map-search').inputValue(),'');
  await page.goto(base+'/#materials');await page.locator('#material-search').fill('supply chain');assert.ok(await page.locator('#material-results .material-link').count()>0);
  // Preserve original and primer bookmarks, then explicitly save a subject path.
  await page.goto(base+'/#guide=04');await page.locator('#save-reading').click();
  await page.goto(base+'/#lesson=13');await page.locator('#save-lesson-reading').click();
  await page.goto(base+'/#topic=mcp-basics?path=builder');await page.locator('#save-topic-reading').click();await page.locator('#notes').fill('Where does authorization happen?');
  await page.reload();await page.locator('#notes').waitFor();assert.equal(await page.locator('#notes').inputValue(),'Where does authorization happen?');
  const saved=await page.evaluate(k=>JSON.parse(localStorage.getItem(k)),key);assert.equal(saved.topicReading,'mcp-basics');assert.equal(saved.topicPath,'builder');assert.equal(saved.lessonReading,'13');assert.equal(saved.reading,'04');assert.deepEqual(saved.done,[]);assert.deepEqual(saved.exercises,{});
  const [download]=await Promise.all([page.waitForEvent('download'),page.locator('#export').click()]);const buffer=fs.readFileSync(await download.path());
  const second=await browser.newContext(),imported=await second.newPage();await imported.goto(base);await imported.locator('#import').setInputFiles({name:'progress.json',mimeType:'application/json',buffer});await imported.getByRole('link',{name:'Resume reading',exact:false}).click();assert.equal(new URL(imported.url()).hash,'#topic=mcp-basics?path=builder');assert.equal(await imported.locator('#notes').inputValue(),'Where does authorization happen?');await second.close();
  // A new mobile learner sees the subject map and can select a topic, then close it.
  await page.setViewportSize({width:390,height:844});await page.locator('#nav-toggle').click();await page.locator('#site-map-search').fill('MCP');await page.locator('.nav-track[data-track="mcp"]').click();assert.equal(await page.locator('#nav-toggle').getAttribute('aria-expanded'),'false');await page.getByRole('link',{name:'Begin this subject',exact:false}).click();assert.equal(new URL(page.url()).hash,'#topic=mcp-basics');await page.waitForFunction(()=>document.querySelector('#save-topic-reading')?.dataset.id==='mcp-basics');
  fs.mkdirSync(path.join(__dirname,'../tmp/qa'),{recursive:true});await page.screenshot({path:path.join(__dirname,'../tmp/qa/subject-topic-mobile.png')});await page.locator('#nav-toggle').click();await page.screenshot({path:path.join(__dirname,'../tmp/qa/subject-map-mobile.png')});await page.keyboard.press('Escape');await page.setViewportSize({width:1440,height:1000});await page.goto(base+'/#track=mcp');await page.screenshot({path:path.join(__dirname,'../tmp/qa/subject-track-desktop.png')});await page.goto(base+'/#overview');await page.screenshot({path:path.join(__dirname,'../tmp/qa/subject-overview-desktop.png')});
  assert.deepEqual(errors,[]);console.log('PASS: 14 tracks, 84 teaching topics and mobile layouts, every step of four learning paths, retained originals/answer gates, no implicit progress, contextual detours, search, three bookmark types, reload/export/import, mobile drawer and screenshots');
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});

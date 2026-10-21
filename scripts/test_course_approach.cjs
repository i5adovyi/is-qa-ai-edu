// Whole-course discovery and teaching-first navigation, isolated from learner data.
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
  assert.equal((await page.goto(base+'/#legacy')).status(),200);
  await page.locator('.course-stage').first().waitFor();
  assert.equal(await page.locator('.course-stage').count(),8);
  assert.equal(await page.locator('.course-stage .lesson-row').count(),24);
  assert.equal(await page.locator('#nav a[href="#path"]').count(),1);
  assert.equal(await page.locator('#nav a[href="#materials"]').count(),1);
  const original=await page.evaluate(k=>localStorage.getItem(k),key);
  await page.getByRole('link',{name:'Begin lesson 01',exact:false}).click();
  await page.locator('.beginner-guide').waitFor();assert.equal(new URL(page.url()).hash,'#lesson=01');
  const inventory=await page.evaluate(()=>({lessons:ACADEMY.curriculum.lessons,course:ACADEMY.course,documents:ACADEMY.documents,resources:ACADEMY.resources,tracks:ACADEMY.tracks}));
  assert.equal(inventory.course.length,24);
  for(const l of inventory.lessons){
   await page.goto(base+'/#lesson='+l.id);await page.locator('.beginner-guide h1').waitFor();
   for(const heading of ['start-here','the-idea-in-plain-language','a-small-example','try-it-with-codex-or-claude-code','what-you-should-see','if-it-goes-wrong','go-deeper','optional-practice']){
    assert.equal(await page.locator('.beginner-guide #'+heading).count(),1,l.id+' '+heading);
   }
   assert.equal(await page.locator('#original-lesson h2').filter({hasText:/^Exercise [123]/}).count(),3);
   assert.ok(await page.locator('#reveal-lesson-solution').isDisabled());
   assert.ok(await page.evaluate(()=>!!(document.querySelector('#save-lesson-reading').compareDocumentPosition(document.querySelector('.beginner-guide'))&Node.DOCUMENT_POSITION_FOLLOWING)),'Bookmark belongs before the long article');
   const guide=inventory.course.find(g=>g.lesson===l.id);
   assert.equal(await page.locator('#lesson-materials .material-link').count(),guide.materials.length);
   assert.equal(await page.locator('#lesson-materials .guide-source a').getAttribute('href'),guide.resource.url);
   await page.getByRole('link',{name:'Assistant how-to',exact:true}).click();
   await page.waitForFunction(()=>document.activeElement.id==='try-it-with-codex-or-claude-code');
  }
  assert.equal(await page.evaluate(k=>localStorage.getItem(k),key),original,'Reading must not mutate learning records');
  // Every document and external resource is in the index, not a selected subset.
  await page.goto(base+'/#materials');await page.locator('#material-results .material-link').first().waitFor();
  assert.equal(await page.locator('#material-results .material-link').count(),Object.keys(inventory.documents).length+inventory.resources.length+inventory.tracks.flatMap(t=>t.lessons).filter(t=>t.resource).length);
  for(const term of ['MCP','skills','state machine','context','evaluation']){
   await page.locator('#material-search').fill(term);assert.ok(await page.locator('#material-results .material-link').count()>0,term);
  }
  await page.locator('#material-search').fill('');await page.locator('#material-type').selectOption('Beginner how-to');assert.equal(await page.locator('#material-results .material-link').count(),24);
  await page.locator('#material-type').selectOption('');await page.locator('#material-search').fill('no-such-topic-zzzzz');assert.match(await page.locator('#material-results').innerText(),/No matches/);
  // Old primer saved place and notes survive a new lesson bookmark and export/import.
  await page.goto(base+'/#guide=04');await page.locator('#save-reading').click();
  await page.goto(base+'/#lesson=13');await page.locator('#save-lesson-reading').click();
  await page.locator('#notes').fill('Please explain an allowed state transition again.');
  await page.reload();await page.locator('#notes').waitFor();assert.match(await page.locator('#notes').inputValue(),/allowed state/);
  let state=await page.evaluate(k=>JSON.parse(localStorage.getItem(k)),key);assert.equal(state.lessonReading,'13');assert.equal(state.reading,'04');assert.deepEqual(state.done,[]);assert.deepEqual(state.exercises,{});
  await page.goto(base+'/#overview');assert.equal(await page.getByRole('link',{name:'Resume reading',exact:false}).getAttribute('href'),'#lesson=13');
  const [download]=await Promise.all([page.waitForEvent('download'),page.locator('#export').click()]);const buffer=fs.readFileSync(await download.path());
  const other=await browser.newContext(),p2=await other.newPage();await p2.goto(base);await p2.locator('#import').setInputFiles({name:'progress.json',mimeType:'application/json',buffer});await p2.getByRole('link',{name:'Resume reading',exact:false}).click();assert.equal(new URL(p2.url()).hash,'#lesson=13');await other.close();
  await page.goto(base+'/#guide=04');await page.locator('#save-reading').click();await page.goto(base+'/#overview');assert.equal(await page.getByRole('link',{name:'Resume reading',exact:false}).getAttribute('href'),'#guide=04');assert.equal((await page.evaluate(k=>JSON.parse(localStorage.getItem(k)),key)).lessonReading,'13');
  // All original hints require actual recorded attempts and then explicit disclosure.
  const lesson=inventory.lessons[12];const solution=inventory.documents[lesson.file].text.match(/^## Hints and solution outline[^\n]*\n([\s\S]*?)(?=^## |$(?![\s\S]))/m)[1].trim();
  const needle=solution.split('\n').find(s=>s.trim().length>40).replace(/^[-*] /,'').replace(/\*\*/g,'').slice(0,45);
  await page.goto(base+'/#lesson=13');assert.ok(!(await page.locator('.reading').innerText()).includes(needle));
  for(let n=1;n<=3;n++){await page.goto(base+'/#exercise=L13-E'+n);await page.locator('#exercise-attempt').fill('My initial attempt identifies a bounded transition and one unknown to investigate.');await page.locator('#save-attempt').click();}
  await page.goto(base+'/#lesson=13');assert.ok(await page.locator('#reveal-lesson-solution').isEnabled());assert.ok(!(await page.locator('#lesson-solution').innerText()).includes(needle));
  await page.locator('#reveal-lesson-solution').click();assert.ok((await page.locator('#lesson-solution').innerText()).trim().length>100);
  await page.reload();await page.locator('#reveal-lesson-solution').waitFor();assert.ok(!(await page.locator('#lesson-solution').innerText()).includes(needle),'Reveal is explicit again after reload');
  fs.mkdirSync(path.join(__dirname,'../tmp/qa'),{recursive:true});
  await page.screenshot({path:path.join(__dirname,'../tmp/qa/course-lesson13.png'),fullPage:true});
  await page.goto(base+'/#legacy');await page.locator('.course-stage').first().waitFor();await page.screenshot({path:path.join(__dirname,'../tmp/qa/course-map.png'),fullPage:true});
  await page.setViewportSize({width:390,height:844});
  for(const route of ['#overview','#path','#materials','#doc=docs%2FASSISTANT-QUICKSTART.md',...inventory.lessons.map(l=>'#lesson='+l.id)]){
   await page.goto(base+'/'+route);await page.locator('#main h1').waitFor();assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth+1),route+' overflows');
  }
  await page.goto(base+'/#lesson=13');await page.locator('.beginner-guide').waitFor();await page.screenshot({path:path.join(__dirname,'../tmp/qa/course-mobile.png'),fullPage:true});await page.screenshot({path:path.join(__dirname,'../tmp/qa/course-mobile-top.png')});
  await page.setViewportSize({width:1440,height:1000});await page.goto(base+'/#lesson=13&section=try-it-with-codex-or-claude-code');await page.waitForFunction(()=>document.activeElement.id==='try-it-with-codex-or-claude-code');await page.screenshot({path:path.join(__dirname,'../tmp/qa/course-howto-desktop.png')});
  assert.deepEqual(errors,[]);
  console.log('PASS: all 24 teaching guides, eight visible stages, complete material index/search, scoped sources, anchor navigation, no automatic completion, old/new bookmark export/import/reload, attempt-plus-reveal solutions, mobile layout');
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});

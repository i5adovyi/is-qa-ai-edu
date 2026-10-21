// Read-only first-session navigation, with no inferred progress or solved assignments.
'use strict';
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const path=require('node:path');
const fs=require('node:fs');
(async()=>{
 const browser=await chromium.launch({headless:true,...(process.env.ACADEMY_BROWSER_PATH?{executablePath:process.env.ACADEMY_BROWSER_PATH}:{})});
 try{
  const context=await browser.newContext({viewport:{width:1440,height:1000}}),page=await context.newPage(),errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  const base=process.env.ACADEMY_TEST_URL||'http://127.0.0.1:8792';
  const lesson=async id=>{await page.waitForFunction(id=>document.querySelector('#save-lesson-reading')?.dataset.id===id&&document.querySelector('.nav-lesson.active')?.dataset.lesson===id,id);};
  await page.goto(base);await page.locator('.track-card').first().waitFor();
  const before=await page.evaluate(()=>JSON.stringify(state));
  assert.equal(await page.locator('.nav-start').getAttribute('href'),'#start');
  await page.goto(base+'/#lesson=01');await lesson('01');
  await page.getByRole('link',{name:'making a clear request',exact:true}).click();await lesson('02');
  assert.equal(new URL(page.url()).hash,'#lesson=02','Inline next link must retain the full lesson navigation');
  // Walk the entire course using the action at the end of each beginner guide.
  await page.goto(base+'/#lesson=01');await lesson('01');
  for(let n=1;n<=24;n++){
   const id=String(n).padStart(2,'0'),next=String(n+1).padStart(2,'0');await lesson(id);
   const card=page.locator('.beginner-guide .lesson-next');assert.match(await card.innerText(),n<24?/without completing the optional/:/does not mark the course complete/);
   assert.equal(await page.locator('.beginner-guide a[href^="#doc=content%2Fhow-to"]').count(),0);
   assert.equal(await page.locator('#original-lesson h2').filter({hasText:/^Exercise [123]/}).count(),3);
   assert.ok(await page.locator('#reveal-lesson-solution').isDisabled());
   assert.equal(await card.locator('a.btn').getAttribute('href'),n<24?'#lesson='+next:'#capstones');
   if(n%3===0&&n<24)assert.match(await card.innerText(),new RegExp('Next · Stage '+(n/3+1),'i'));
   await card.locator('a.btn').click();
  }
  await page.locator('.reading-return').waitFor();assert.equal(new URL(page.url()).hash,'#capstones');
  assert.equal(await page.locator('.reading-return a.btn').getAttribute('href'),'#lesson=24');
  for(let stage=1;stage<=8;stage++){
   await page.goto(base+'/#stage='+stage);await page.locator('.stage-start').waitFor();
   assert.equal(await page.locator('.stage-start a').getAttribute('href'),'#lesson='+String((stage-1)*3+1).padStart(2,'0'));
   assert.equal(await page.locator('.lesson-row').count(),3);
  }
  // Selecting a search result restores the map, including the next lesson.
  await page.locator('#site-map-search').fill('state machine');await page.locator('.nav-lesson[data-lesson="13"]').click();await lesson('13');
  assert.equal(await page.locator('#site-map-search').inputValue(),'');assert.equal(await page.locator('.nav-lesson').count(),24);
  await page.locator('.lesson-controls a').click();await lesson('14');assert.ok(await page.locator('.nav-lesson.active[data-lesson="14"]').isVisible());
  // A setup detour has an explicit route back, independent of a saved bookmark.
  await page.goto(base+'/#lesson=13');await lesson('13');
  await page.locator('.reading-side').getByRole('link',{name:'How to use Codex or Claude Code',exact:false}).click();
  await page.waitForFunction(()=>document.querySelector('#download-doc')?.dataset.path==='docs/ASSISTANT-QUICKSTART.md');
  assert.equal(await page.locator('.reading-return a.btn').getAttribute('href'),'#lesson=13');
  await page.locator('.reading-return a.btn').click();await lesson('13');
  // Standalone guide URLs remain downloadable; the normal materials index opens lessons.
  await page.goto(base+'/#doc=content%2Fhow-to%2F02.md');await page.waitForFunction(()=>document.querySelector('#download-doc')?.dataset.path==='content/how-to/02.md');
  assert.equal(await page.locator('.reading-return a.btn').getAttribute('href'),'#lesson=02');
  await page.locator('.reading-return a.btn').click();await lesson('02');
  await page.goto(base+'/#materials');await page.locator('#material-search').fill('state machine');await page.locator('#material-type').selectOption('Beginner how-to');
  await page.locator('#material-results a[href="#lesson=13"]').click();await lesson('13');
  await page.getByRole('link',{name:'Related materials',exact:true}).click();await page.waitForFunction(()=>document.activeElement.id==='lesson-materials');
  await page.locator('#lesson-materials .material-link').first().click();await page.locator('.reading-return').waitFor();
  assert.equal(await page.locator('.reading-return a.btn').getAttribute('href'),'#lesson=13');
  await page.locator('.reading-return a.btn').click();await lesson('13');
  await page.goto(base+'/#lesson=01');await lesson('01');
  await page.locator('.beginner-guide').getByRole('link',{name:'AI basics primer',exact:true}).click();await page.locator('#save-reading').waitFor();
  assert.match(await page.locator('.guide-position').innerText(),/Primer 01/i);
  assert.equal(await page.locator('.reading-return a.btn').getAttribute('href'),'#lesson=01');
  await page.goto(base+'/#guide=08');await page.locator('#save-reading[data-id="08"]').waitFor();assert.equal(await page.locator('.guide-next a.btn').last().getAttribute('href'),'#path');
  // Mobile menu and reading detours retain the same route and fit a narrow screen.
  await page.setViewportSize({width:390,height:844});await page.goto(base+'/#overview');await page.locator('#nav-toggle').click();
  await page.locator('.nav-start').click();await page.getByRole('link',{name:'Start the first topic',exact:false}).waitFor();assert.equal(await page.locator('#nav-toggle').getAttribute('aria-expanded'),'false');
  await page.goto(base+'/#lesson=01');await lesson('01');
  await page.locator('.beginner-guide .lesson-next').scrollIntoViewIfNeeded();
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  const contrast=await page.locator('.beginner-guide .lesson-next a.btn').evaluate(el=>{
   const luminance=color=>color.match(/[\d.]+/g).slice(0,3).map(Number).map(v=>{v/=255;return v<=.04045?v/12.92:((v+.055)/1.055)**2.4}).reduce((n,v,i)=>n+v*[.2126,.7152,.0722][i],0);
   const css=getComputedStyle(el),a=luminance(css.color),b=luminance(css.backgroundColor);return (Math.max(a,b)+.05)/(Math.min(a,b)+.05);
  });
  assert.ok(contrast>=4.5,'The next-lesson button needs readable text contrast');
  fs.mkdirSync(path.join(__dirname,'../tmp/qa'),{recursive:true});await page.screenshot({path:path.join(__dirname,'../tmp/qa/beginner-next-mobile.png')});
  await page.locator('.beginner-guide .lesson-next a.btn').click();await lesson('02');
  await page.locator('.reading-side').getByRole('link',{name:'How to use Codex or Claude Code',exact:false}).click();await page.locator('.reading-return').waitFor();
  assert.equal(await page.locator('.reading-return a.btn').getAttribute('href'),'#lesson=02');assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await page.locator('.reading-return a.btn').click();await lesson('02');
  assert.equal(await page.evaluate(()=>JSON.stringify(state)),before,'Reading, search, and detours must not write learner progress');
  assert.deepEqual(errors,[]);
  console.log('PASS: beginner start, inline next link, all 24 sequential lessons and eight stage entries, optional final capstone, cleared search, contextual return from setup/materials/primers, standalone downloads, mobile journey, unchanged learning record, zero page errors');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});

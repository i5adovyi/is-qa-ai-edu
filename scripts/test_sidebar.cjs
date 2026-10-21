// Sidebar discovery, contextual location, keyboard operation and mobile drawer.
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
  await page.goto(base);await page.locator('.nav-stage').first().waitFor({state:'attached'});
  assert.equal(await page.locator('.nav-stage').count(),8);assert.equal(await page.locator('.nav-lesson').count(),24);
  let state=await page.evaluate(k=>localStorage.getItem(k),key);
  const stages=await page.evaluate(()=>ACADEMY.curriculum.stages);
  await page.locator('.nav-archive>summary').click();
  for(const s of stages){
   const group=page.locator(`.nav-stage[data-stage="${s.id}"]`);await group.locator('summary').focus();await page.keyboard.press('Enter');
   assert.ok(await group.evaluate(el=>el.open));assert.equal(await group.locator('.nav-lesson:visible').count(),3);
   await group.locator('summary').press('Enter');assert.ok(!(await group.evaluate(el=>el.open)));
  }
  await page.locator('#nav-expand').click();assert.equal(await page.locator('.nav-stage[open]').count(),8);
  await page.locator('#nav-expand').click();assert.equal(await page.locator('.nav-stage[open]').count(),0);
  // Every lesson can be reached directly from the sidebar and remains highlighted.
  for(const l of await page.evaluate(()=>ACADEMY.curriculum.lessons)){
   const stage=page.locator(`.nav-stage[data-stage="${l.stage}"]`);
   if(!(await stage.evaluate(el=>el.open)))await stage.locator('summary').click();
   await page.locator(`.nav-lesson[data-lesson="${l.id}"]`).click();
   await page.waitForFunction(id=>location.hash==='#lesson='+id&&document.querySelector('.nav-lesson.active')?.dataset.lesson===id,l.id);
   assert.equal(await page.locator('.nav-lesson[aria-current="page"]').count(),1);
   assert.equal(await page.locator('#nav .nav-page[aria-current="page"]').count(),0);
   assert.ok(await page.locator(`.nav-stage[data-stage="${l.stage}"]`).evaluate(el=>el.open));
  }
  await page.goto(base+'/#doc=content%2Fhow-to%2F13.md');await page.locator('.nav-lesson.active[data-lesson="13"]').waitFor();
  assert.equal(await page.evaluate(k=>localStorage.getItem(k),key),state);
  await page.goto(base+'/#exercise=L13-E2');await page.locator('.nav-lesson[aria-current="location"][data-lesson="13"]').waitFor();
  state=await page.evaluate(k=>localStorage.getItem(k),key); // Entering a workspace deliberately creates its existing empty draft/resume record.
  // Search uses plain titles, technical terminology, and section labels.
  await page.locator('#site-map-search').fill('state machine');
  assert.equal(await page.locator('.nav-lesson').count(),1);assert.equal(await page.locator('.nav-lesson').getAttribute('data-lesson'),'13');
  await page.locator('#site-map-search').fill('MCP');assert.ok(await page.locator('.nav-lesson[data-lesson="08"]').isVisible());
  await page.locator('#site-map-search').fill('books');assert.ok(await page.locator('#nav a[href="#library"]').isVisible());
  await page.locator('#site-map-search').fill('zz-nothing');assert.match(await page.locator('#nav').innerText(),/No matches/);
  await page.locator('#nav-clear').click();assert.equal(await page.locator('.nav-lesson').count(),24);assert.equal(await page.locator('#site-map-search').inputValue(),'');
  for(const id of ['overview','path','materials','labs','progress','guide','library','prepare','incidents','retention','manuals','capstones','workbench','run']){
   await page.locator(`#nav a[href="#${id}"]`).click();await page.waitForFunction(id=>location.hash==='#'+id&&document.querySelector('#nav a[href="#'+id+'"]')?.getAttribute('aria-current')==='page',id);assert.equal(await page.locator(`#nav a[href="#${id}"]`).getAttribute('aria-current'),'page');
  }
  assert.equal(await page.evaluate(k=>localStorage.getItem(k),key),state,'Navigation must not change learning records');
  // Short desktop heights retain independent navigation and reachable backup controls.
  await page.setViewportSize({width:1024,height:600});await page.goto(base+'/#lesson=13');await page.locator('.nav-lesson.active').waitFor();
  assert.ok(await page.evaluate(()=>{const n=document.querySelector('#nav');return n.scrollHeight>n.clientHeight&&n.clientHeight>100;}));
  const backup=await page.locator('#export').boundingBox();assert.ok(backup.y>=0&&backup.y+backup.height<=600);
  fs.mkdirSync(path.join(__dirname,'../tmp/qa'),{recursive:true});
  await page.setViewportSize({width:1440,height:1000});await page.screenshot({path:path.join(__dirname,'../tmp/qa/sidebar-desktop.png')});
  // Mobile: a compact persistent button opens a modal map; focus stays in it.
  await page.setViewportSize({width:390,height:844});await page.goto(base+'/#lesson=13');await page.locator('#nav-toggle').waitFor();
  assert.equal(await page.locator('#nav-toggle').getAttribute('aria-expanded'),'false');assert.ok(!(await page.locator('#nav').isVisible()));
  await page.screenshot({path:path.join(__dirname,'../tmp/qa/sidebar-mobile-closed.png')});
  await page.locator('#nav-toggle').click();assert.equal(await page.locator('#nav-toggle').getAttribute('aria-expanded'),'true');
  assert.equal(await page.locator('.sidebar').getAttribute('role'),'dialog');assert.equal(await page.locator('.sidebar').getAttribute('aria-modal'),'true');
  assert.equal(await page.evaluate(()=>document.activeElement.id),'site-map-search');assert.ok(await page.locator('.shell').evaluate(el=>el.inert));
  await page.locator('#import-progress').focus();await page.keyboard.press('Tab');assert.ok(await page.evaluate(()=>document.activeElement.classList.contains('brand')));
  await page.keyboard.press('Shift+Tab');assert.equal(await page.evaluate(()=>document.activeElement.id),'import-progress');
  await page.locator('#site-map-search').fill('state machine');await page.screenshot({path:path.join(__dirname,'../tmp/qa/sidebar-mobile-open.png')});
  await page.keyboard.press('Escape');assert.equal(await page.evaluate(()=>document.activeElement.id),'nav-toggle');assert.ok(!(await page.locator('.shell').evaluate(el=>el.inert)));
  await page.locator('#nav-toggle').click();await page.locator('.nav-lesson[data-lesson="13"]').click();assert.equal(await page.locator('#nav-toggle').getAttribute('aria-expanded'),'false');
  // A long article does not make the mobile site map disappear.
  await page.evaluate(()=>window.scrollTo(0,document.body.scrollHeight));assert.ok(await page.locator('#nav-toggle').evaluate(el=>{const r=el.getBoundingClientRect();return r.top>=0&&r.bottom<=innerHeight;}));
  await page.locator('#nav-toggle').click();await page.locator('#nav-clear').click();
  await page.locator('#nav a[href="#labs"]').click();await page.waitForFunction(()=>location.hash==='#labs');assert.ok(!(await page.locator('.shell').evaluate(el=>el.inert)));
  await page.locator('#nav-toggle').click();await page.setViewportSize({width:1440,height:1000});await page.waitForFunction(()=>!document.querySelector('.shell').inert&&!document.querySelector('.sidebar').hasAttribute('role'));assert.equal(await page.locator('#nav-toggle').getAttribute('aria-expanded'),'false');
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);assert.deepEqual(errors,[]);
  console.log('PASS: all 24 sidebar lesson links, eight keyboard-operable stages, expand/collapse, contextual deep links, search/clear/empty state, all site sections, unchanged progress, short desktop scrolling, mobile drawer/focus/Escape/navigation/resize');
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});

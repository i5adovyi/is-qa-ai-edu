// Appearance must work without changing the learning record or requiring storage.
'use strict';
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const base=process.env.ACADEMY_TEST_URL||'http://127.0.0.1:8792';
const key='ai-engineering-academy-theme',progressKey='ai-engineering-academy-v1';
const shots=path.join(__dirname,'../tmp/qa');
async function ready(page,route=''){
 console.log('Checking',route||'default');
 await page.goto(base+'/'+route);await page.locator('#main h1').first().waitFor();
 await page.waitForFunction(()=>!document.querySelector('#global-save-status').textContent.includes('Loading'));
}
async function theme(page,value){await page.waitForFunction(v=>document.documentElement.dataset.theme===v,value);}
// Compute WCAG contrast from rendered foreground and ancestor background colors.
async function contrast(page){return page.evaluate(()=>{
 const rgb=s=>(s.match(/[\d.]+/g)||[]).map(Number);
 const lum=a=>a.slice(0,3).map(n=>{n/=255;return n<=.04045?n/12.92:((n+.055)/1.055)**2.4}).reduce((v,n,i)=>v+n*[.2126,.7152,.0722][i],0);
 const failures=[];
 const selectors='#main p,#main li,#main h1,#main h2,#main h3,#main a,#main code,#main .tag,#main .eyebrow,#main .num,#main .stage-id,#main .task,#main input,#main textarea,#main select,#main button,.theme-picker,.theme-picker select,.breadcrumb,.local-label';
 for(const el of document.querySelectorAll(selectors)){
  if(!el.checkVisibility()||el.disabled||!el.textContent.trim()&& !el.value)continue;
  const style=getComputedStyle(el),fg=rgb(style.color);let bg=null,node=el;
  while(node){const c=rgb(getComputedStyle(node).backgroundColor);if(c.length===3||c[3]===1){bg=c;break;}node=node.parentElement;}
  if(!bg)bg=[255,255,255];
  const l1=lum(fg),l2=lum(bg),ratio=(Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05);
  const large=parseFloat(style.fontSize)>=24||(parseFloat(style.fontSize)>=18.66&&Number(style.fontWeight)>=700);
  if(ratio<(large?3:4.5))failures.push({tag:el.tagName,cls:el.className,text:el.textContent.trim().slice(0,60),ratio:Number(ratio.toFixed(2)),fg:style.color,bg});
 }
 return failures;
});}
(async()=>{
 const browser=await chromium.launch({headless:true,...(process.env.ACADEMY_BROWSER_PATH?{executablePath:process.env.ACADEMY_BROWSER_PATH}:{})});
 try{
  const context=await browser.newContext({viewport:{width:1440,height:1000},colorScheme:'dark'});
  context.setDefaultTimeout(10000);
  const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
  await ready(page);await theme(page,'dark');assert.equal(await page.locator('#theme-choice').inputValue(),'system');
  const progress=await page.evaluate(k=>localStorage.getItem(k),progressKey);
  await page.emulateMedia({colorScheme:'light'});await theme(page,'light');
  // Native select supports keyboard operation, including while data loading is independent.
  await page.locator('#theme-choice').focus();await page.keyboard.press('d');await page.keyboard.press('Enter');await theme(page,'dark');
  assert.equal(await page.evaluate(k=>localStorage.getItem(k),key),'dark');
  await page.reload();await page.locator('#main h1').first().waitFor();await theme(page,'dark');
  assert.equal(await page.locator('#theme-choice').inputValue(),'dark');
  assert.equal(await page.evaluate(k=>localStorage.getItem(k),progressKey),progress,'Appearance must not write learning records');
  await page.emulateMedia({colorScheme:'dark'});await page.locator('#theme-choice').selectOption('light');await theme(page,'light');
  await page.reload();await page.locator('#main h1').first().waitFor();await theme(page,'light');
  // Same-origin tabs receive explicit choices and changes back to System.
  const other=await context.newPage();await ready(other);await theme(other,'light');
  await page.locator('#theme-choice').selectOption('dark');await theme(other,'dark');assert.equal(await other.locator('#theme-choice').inputValue(),'dark');
  await page.locator('#theme-choice').selectOption('system');await page.emulateMedia({colorScheme:'light'});await theme(page,'light');await theme(other,'dark');
  assert.equal(await other.locator('#theme-choice').inputValue(),'system');await other.close();
  await page.locator('#theme-choice').selectOption('dark');
  fs.mkdirSync(shots,{recursive:true});
  const routes=['#overview','#start','#tracks','#track=mcp','#topic=mcp-basics','#lesson=13','#library','#materials','#workbench','#progress','#prepare','#incidents','#exercise=L13-E2','#retention','#run'];
  const failures=[];
  for(const route of routes){
   await ready(page,route);await theme(page,'dark');
   failures.push(...(await contrast(page)).map(f=>({route,...f})));
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),route+' desktop overflow');
   if(route==='#topic=mcp-basics')await page.screenshot({path:path.join(shots,'theme-dark-reading.png')});
   if(route==='#overview')await page.screenshot({path:path.join(shots,'theme-dark-overview.png')});
  }
  assert.deepEqual(failures,[],'Dark text must retain WCAG AA contrast');
  // Theme use preserves an existing practice record too.
  const record=await page.evaluate(k=>localStorage.getItem(k),progressKey);
  await page.locator('#theme-choice').selectOption('light');await page.locator('#theme-choice').selectOption('dark');
  assert.equal(await page.evaluate(k=>localStorage.getItem(k),progressKey),record);
  await page.setViewportSize({width:390,height:844});
  for(const route of ['#overview','#topic=mcp-basics','#exercise=L13-E2']){
   await ready(page,route);assert.ok(await page.locator('#theme-choice').isVisible());
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),route+' mobile overflow');
  }
  await ready(page,'#topic=mcp-basics');await page.screenshot({path:path.join(shots,'theme-dark-mobile.png')});
  await page.locator('#nav-toggle').click();assert.ok(await page.locator('.shell').evaluate(el=>el.inert));
  await page.keyboard.press('Escape');await page.locator('#theme-choice').selectOption('light');await theme(page,'light');
  await page.screenshot({path:path.join(shots,'theme-light-mobile.png')});
  // Printing a dark session remains light and legible.
  await page.locator('#theme-choice').selectOption('dark');await page.emulateMedia({media:'print'});
  assert.equal(await page.evaluate(()=>getComputedStyle(document.body).backgroundColor),'rgb(246, 246, 240)');
  assert.equal(await page.locator('.topbar').isVisible(),false);await page.emulateMedia({media:'screen'});
  assert.deepEqual(errors,[]);
  // Invalid stored data falls back to system without clearing other data.
  const invalid=await browser.newContext({colorScheme:'dark'});await invalid.addInitScript(k=>localStorage.setItem(k,'invalid'),key);
  const invalidPage=await invalid.newPage();await ready(invalidPage);await theme(invalidPage,'dark');assert.equal(await invalidPage.locator('#theme-choice').inputValue(),'system');await invalid.close();
  // Read/write failures leave a usable selector and truthful session-only message.
  const blocked=await browser.newContext({colorScheme:'light'});
  await blocked.addInitScript(()=>{Object.defineProperty(window,'localStorage',{get(){throw new DOMException('Blocked','SecurityError');}});});
  const blockedPage=await blocked.newPage(),blockedErrors=[];blockedPage.on('pageerror',e=>blockedErrors.push(e.message));
  await ready(blockedPage);await theme(blockedPage,'light');await blockedPage.locator('#theme-choice').selectOption('dark');await theme(blockedPage,'dark');
  assert.ok(await blockedPage.locator('#theme-status').isVisible());assert.match(await blockedPage.locator('#theme-status').innerText(),/this tab/);
  assert.deepEqual(blockedErrors,[]);await blocked.close();await context.close();
  console.log('PASS: system/default, keyboard selection, saved overrides/reloads, cross-tab preference, unchanged learning records, invalid/blocked storage, 15 dark routes with AA text contrast, mobile layout/drawer and light print styling.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});

// Isolated SQLite + browser integration check. Build dist first.
// Uses only temporary learner data and closes every process it starts.
'use strict';
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const os=require('node:os');
const path=require('node:path');
const net=require('node:net');
const {spawn}=require('node:child_process');
const ROOT=path.resolve(__dirname,'..'),scratch=fs.mkdtempSync(path.join(os.tmpdir(),'academy-local-ui-'));
const processes=[];
const delay=ms=>new Promise(r=>setTimeout(r,ms));
async function port(){const server=net.createServer();await new Promise(r=>server.listen(0,'127.0.0.1',r));const chosen=server.address().port;await new Promise(r=>server.close(r));return chosen;}
async function launch(staticOnly=false){
 const chosen=await port(),base='http://127.0.0.1:'+chosen;
 const args=staticOnly?['-m','http.server',String(chosen),'--bind','127.0.0.1','--directory',path.join(ROOT,'dist')]:[path.join(ROOT,'academy.py'),'local','--no-build','--no-browser','--port',String(chosen),'--data-dir',path.join(scratch,'profile')];
 const child=spawn(process.env.ACADEMY_PYTHON||'python3',args,{cwd:scratch,stdio:['ignore','pipe','pipe']});processes.push(child);let logs='';child.stdout.on('data',x=>{logs+=x});child.stderr.on('data',x=>{logs+=x});
 const until=Date.now()+15000;
 while(Date.now()<until){try{const response=await fetch(base);if(response.ok)return {child,base}}catch{}if(child.exitCode!==null)throw Error('Server exited: '+logs);await delay(50)}
 throw Error('Server startup timeout: '+logs);
}
async function stop(child){if(child.exitCode!==null)return;child.kill('SIGINT');await Promise.race([new Promise(r=>child.once('exit',r)),delay(3000)]);if(child.exitCode===null){child.kill('SIGKILL');await new Promise(r=>child.once('exit',r));}}
async function saved(page){await page.waitForFunction(()=>document.querySelector('#global-save-status')?.textContent==='Saved locally in SQLite');}
async function db(page){return page.evaluate(async()=>(await(await fetch('/api/local-state')).json()).state)}
(async()=>{
 let browser;
 try{
  let server=await launch();browser=await chromium.launch({headless:true,...(process.env.ACADEMY_BROWSER_PATH?{executablePath:process.env.ACADEMY_BROWSER_PATH}:{})});
  const context=await browser.newContext({viewport:{width:1440,height:1000}}),page=await context.newPage(),errors=[];
  page.on('pageerror',e=>errors.push(e.message));page.on('dialog',dialog=>dialog.accept());
  await page.goto(server.base+'/#exercise=L01-E1');await saved(page);
  await page.locator('#exercise-attempt').fill('My rough draft identifies the model and the tool result as separate evidence.');await saved(page);
  await page.getByRole('button',{name:'Save attempt',exact:true}).click();await saved(page);
  await page.goto(server.base+'/#lesson=01');await saved(page);
  await page.locator('#notes').fill('Evidence note saved before closing the whole browser context.');await saved(page);
  await page.getByRole('button',{name:'Mark lesson complete',exact:true}).click();await saved(page);
  const first=await db(page);assert.ok(first.done.includes('01'));assert.ok(first.exercises['L01-E1'].history.some(x=>x.kind==='attempt'));
  await context.close();
  const nextContext=await browser.newContext({viewport:{width:1440,height:1000}}),next=await nextContext.newPage();next.on('dialog',dialog=>dialog.accept());next.on('pageerror',e=>errors.push(e.message));
  await next.goto(server.base+'/#exercise=L01-E1');await saved(next);
  assert.match(await next.locator('#exercise-attempt').inputValue(),/My rough draft/);assert.ok((await db(next)).done.includes('01'));
  // Two contexts share the database but have independent browser caches.
  await next.goto(server.base+'/#lesson=01');await saved(next);
  const staleContext=await browser.newContext(),stale=await staleContext.newPage();stale.on('dialog',dialog=>dialog.accept());
  await stale.goto(server.base+'/#lesson=01');await saved(stale);
  await next.locator('#notes').fill('Newer database note from first browser.');await saved(next);
  await stale.locator('#notes').fill('Concurrent draft from second browser.');
  await stale.locator('#storage-merge').waitFor();
  assert.match(await stale.locator('#storage-notice').innerText(),/Another tab or browser/);
  await stale.locator('#storage-merge').click();await saved(stale);
  const merged=Object.values((await db(stale)).notes).join('\n');assert.match(merged,/Newer database note/);assert.match(merged,/Concurrent draft/);
  // A network failure must retain the pending browser draft and label it unsaved.
  await next.reload();await saved(next);
  await next.route('**/api/local-state',route=>route.request().method()==='PUT'?route.abort('failed'):route.continue());
  await next.locator('#notes').fill('Uncommitted work survives a failed write and a reload.');
  await next.waitForFunction(()=>document.querySelector('#global-save-status').textContent.includes('Unsaved'));
  assert.match(await next.locator('#storage-notice').innerText(),/have not reached/);
  await next.unroute('**/api/local-state');await next.reload();await next.locator('#storage-merge').waitFor();
  assert.match(await next.locator('#storage-notice').innerText(),/Browser work/);
  await next.locator('#storage-merge').click();await saved(next);
  assert.match(Object.values((await db(next)).notes).join('\n'),/Uncommitted work survives/);
  // Neither saved drafts nor reconciliation unlock incident answers.
  await next.goto(server.base+'/#incident=INC-01');
  if(await next.locator('#incident-debrief').count())assert.equal(await next.locator('#incident-debrief').isDisabled(),true);
  await next.goto(server.base+'/#progress');await saved(next);
  assert.match(await next.locator('#main').innerText(),/SQLite/);assert.ok(await next.locator('.recovery-copies').count());
  fs.mkdirSync(path.join(ROOT,'work'),{recursive:true});await next.screenshot({path:path.join(ROOT,'work/local-data-desktop.png'),fullPage:true});
  await next.setViewportSize({width:390,height:844});assert.equal(await next.locator('#global-save-status').isVisible(),true);assert.equal(await next.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);await next.screenshot({path:path.join(ROOT,'work/local-data-mobile.png'),fullPage:true});
  await nextContext.close();await staleContext.close();
  // Restart the process and change port: a fresh context still reads the same SQLite file.
  const oldBase=server.base;await stop(server.child);server=await launch();assert.notEqual(server.base,oldBase);
  const restartedContext=await browser.newContext(),restarted=await restartedContext.newPage();await restarted.goto(server.base+'/#lesson=01');await saved(restarted);
  assert.match(await restarted.locator('#notes').inputValue(),/Uncommitted work survives/);assert.ok((await db(restarted)).done.includes('01'));await restartedContext.close();
  const staticServer=await launch(true),staticContext=await browser.newContext(),preview=await staticContext.newPage();await preview.goto(staticServer.base+'/#lesson=01');
  await preview.waitForFunction(()=>document.querySelector('#global-save-status').textContent.includes('static preview'));
  await preview.locator('#notes').fill('Browser-only static preview');assert.match(await preview.locator('#global-save-status').innerText(),/browser/);assert.match(await preview.locator('#storage-notice').innerText(),/browser storage only/);
  await preview.reload();assert.equal(await preview.locator('#notes').inputValue(),'Browser-only static preview');await staticContext.close();
  assert.deepEqual(errors,[]);
  console.log('PASS: SQLite drafts, history, notes and completion; browser context restart; concurrent revision conflict and explicit merge; failed PUT + reload recovery; server restart + different port; static preview fallback; mobile layout.');
 }finally{if(browser)await browser.close();for(const child of processes)await stop(child);fs.rmSync(scratch,{recursive:true,force:true});}
})().catch(error=>{console.error(error);process.exitCode=1});

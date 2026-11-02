// Serve dist first. Uses the same optional Playwright setup as the other UI checks.
'use strict';
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
  await page.getByRole('link',{name:'Run anywhere',exact:false}).click();
  await page.getByRole('heading',{name:'Run the academy your way.'}).waitFor();
  assert.match(await page.locator('#runtime-mode').innerText(),/local academy/);
  const config=JSON.parse(fs.readFileSync(path.join(__dirname,'../academy.json'),'utf8'));
  assert.equal(await page.getByRole('link',{name:'Open hosted academy'}).getAttribute('href'),config.hostedUrl+'/');
  assert.equal(await page.getByRole('link',{name:'Open GitHub repository'}).getAttribute('href'),config.repositoryUrl);
  assert.equal(await page.getByRole('link',{name:'open the local academy'}).getAttribute('href'),'http://127.0.0.1:8765/');
  const waiting=page.waitForEvent('download');
  await page.getByRole('link',{name:'Download portable academy'}).click();
  const download=await waiting;
  assert.ok(fs.readFileSync(await download.path()).equals(fs.readFileSync(path.join(__dirname,'../dist/academy-portable.zip'))));
  await page.getByRole('link',{name:'Setup, options and publishing guide'}).click();
  await page.locator('.reading h1').waitFor();
  assert.match(await page.locator('.reading').innerText(),/python3 academy.py local/);
  await page.goto(base+'/#run');
  await page.locator('#runtime-mode').waitFor();
  fs.mkdirSync(path.join(__dirname,'../work'),{recursive:true});
  await page.screenshot({path:path.join(__dirname,'../work/run-anywhere-desktop.png'),fullPage:true});
  await page.setViewportSize({width:390,height:844});
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
  await page.screenshot({path:path.join(__dirname,'../work/run-anywhere-mobile.png'),fullPage:true});
  await page.getByRole('link',{name:'Review my progress'}).click();
  await page.getByRole('heading',{name:'Your reading and optional practice.'}).waitFor();
  assert.deepEqual(errors,[]);
  console.log('PASS: run-anywhere navigation, hosted/local/GitHub links, portable download bytes, setup guide, progress navigation, desktop and mobile layout.');
 }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});

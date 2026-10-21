// Run with: node --test tests/test_portal.cjs
// Dependency-free regression tests for routing and the learner's saved records.
'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const ROOT = path.join(__dirname, '..');

function academy() {
  const documents = {};
  for (const root of ['content', 'docs', 'templates', 'capstones', 'lab']) {
    for (const entry of fs.readdirSync(path.join(ROOT, root), {recursive: true, withFileTypes: true})) {
      if (!entry.isFile() || !entry.name.endsWith('.md')) continue;
      const absolute = path.join(entry.parentPath || entry.path, entry.name);
      const relative = path.relative(ROOT, absolute).replaceAll(path.sep, '/');
      const text = fs.readFileSync(absolute, 'utf8');
      documents[relative] = {text, title: text.split('\n')[0].replace(/^# /, '')};
    }
  }
  return {
    tracks: fs.readdirSync(path.join(ROOT,'content/tracks')).filter(n=>/^catalog-.*\.json$/.test(n)).flatMap(n=>JSON.parse(fs.readFileSync(path.join(ROOT,'content/tracks',n),'utf8'))),
    paths: JSON.parse(fs.readFileSync(path.join(ROOT,'content/tracks/paths.json'),'utf8')),
    course: fs.readdirSync(path.join(ROOT,'content/how-to')).filter(n=>/^map-.*\.json$/.test(n)).flatMap(n=>JSON.parse(fs.readFileSync(path.join(ROOT,'content/how-to',n),'utf8'))),
    guide: JSON.parse(fs.readFileSync(path.join(ROOT,'content/sdet-path.json'),'utf8')),
    runtime: JSON.parse(fs.readFileSync(path.join(ROOT,'academy.json'),'utf8')),
    incidents: fs.existsSync(path.join(ROOT,'content/incidents.json')) ? JSON.parse(fs.readFileSync(path.join(ROOT,'content/incidents.json'),'utf8')) : {incidents:[]},
    curriculum: JSON.parse(fs.readFileSync(path.join(ROOT, 'content/curriculum.json'), 'utf8')),
    learning: JSON.parse(fs.readFileSync(path.join(ROOT, 'content/learning.json'), 'utf8')),
    resources: JSON.parse(fs.readFileSync(path.join(ROOT, 'content/resources.json'), 'utf8')),
    documents,
    assets: ['content/resources.json', 'content/labs/solutions/reference.py',
      'content/research/sources.json', 'content/research/cases.json',
      'content/dev-sandbox/router.py', 'content/dev-sandbox/test_router.py'],
  };
}

function portal(options={}) {
  const nodes = {}, handlers = {}, storage = options.storage||{};
  const context = vm.createContext({
    window: {ACADEMY: academy(), scrollTo() {}, addEventListener() {}},
    document: {
      title: '',
      querySelector: selector => nodes[selector] ||= {
        innerHTML: '', textContent: '', style: {}, dataset: {}, focus() {}, click() {this.clicked = true;},
      },
      querySelectorAll: () => [],
      getElementById: () => null,
      addEventListener: (kind, callback) => {handlers[kind] = callback;},
    },
    localStorage: {getItem: key => storage[key] || null, setItem: (key, value) => {storage[key] = value;}, removeItem:key=>{delete storage[key]},key:i=>Object.keys(storage)[i],get length(){return Object.keys(storage).length}},
    location: {hash: '#overview',...(options.location||{})},
    ...(options.fetch?{fetch:options.fetch}:{}),
    URLSearchParams, TextEncoder, setTimeout: () => 0, clearTimeout() {},
  });
  vm.runInContext(fs.readFileSync(path.join(ROOT, 'portal/tracks.js'), 'utf8'), context);
  vm.runInContext(fs.readFileSync(path.join(ROOT, 'portal/app.js'), 'utf8'), context);
  return {run: code => vm.runInContext(code, context), nodes, handlers, context,storage};
}

test('solution code resolves to a whitelisted existing distribution asset', () => {
  const p = portal();
  assert.equal(p.run("resolveHref('reference.py','content/labs/solutions/README.md')"),
    'content/labs/solutions/reference.py');
  assert.equal(p.run("resolveHref('../solutions/reference.py','content/labs/hints/README.md')"),
    'content/labs/solutions/reference.py');
  assert.equal(p.run("resolveHref('../resources.json','content/library/README.md')"), 'content/resources.json');
});

test('links cannot expose arbitrary paths or executable URL schemes', () => {
  const p = portal();
  for (const url of ['javascript:alert(1)', 'file:///etc/passwd', '//evil.example/test',
    '/etc/passwd', '../../../../../content/resources.json', '../../../lab/student.py']) {
    p.context.testURL = url;
    assert.equal(p.run("resolveHref(testURL,'content/labs/README.md')"), '#', url);
  }
});

test('lab solution links retain their section and every target heading exists', () => {
  const p = portal();
  for (let n = 1; n <= 8; n++) {
    const number = String(n).padStart(2, '0');
    p.context.number = number;
    const href = p.run("resolveHref('solutions/README.md#lab-'+number,'content/labs/README.md')");
    assert.equal(href, '#doc=content%2Flabs%2Fsolutions%2FREADME.md&section=lab-' + number);
    assert.match(p.run("markdown(A.documents['content/labs/solutions/README.md'].text,'content/labs/solutions/README.md')"),
      new RegExp('id="lab-' + number + '"'));
  }
  assert.equal(p.run("resolveHref('#lab-08','content/labs/solutions/README.md')"),
    '#doc=content%2Flabs%2Fsolutions%2FREADME.md&section=lab-08');
});

test('duplicate headings get unique IDs, including hidden hints', () => {
  const p = portal();
  const html = p.run("markdown('## Same\\n\\n## Same\\n\\n## Hints\\nA hint.','docs/START-HERE.md')");
  assert.match(html, /id="same"/);
  assert.match(html, /id="same-1"/);
  assert.match(html, /<details id="hints">/);
});

test('malformed encoded routes render an unavailable page without crashing', () => {
  const p = portal();
  for (const route of ['#doc=%', '#__proto__', '#constructor', '#doc=__proto__', '#doc=constructor']) {
    p.context.location.hash = route;
    assert.doesNotThrow(() => p.run('render()'), route);
    assert.match(p.nodes['#main'].innerHTML, /That page is not in this edition/);
  }
  assert.equal(p.run("parseRoute('doc=content%2Flabs%2Fsolutions%2FREADME.md&section=lab-08').anchor"), 'lab-08');
});

test('large notes survive save, export serialization, and restore', () => {
  const p = portal();
  p.run("state.notes['docs/START-HERE.md']='x'.repeat(100001); save()");
  assert.equal(p.run("validateState(JSON.parse(localStorage.getItem(KEY))).notes['docs/START-HERE.md'].length"), 100001);
  assert.equal(p.run("validateState(JSON.parse(JSON.stringify(state))).notes['docs/START-HERE.md'].length"), 100001);
});

test('failed device storage leaves current notes available to the export button', () => {
  const p = portal();
  p.run("localStorage.setItem=()=>{throw Error('Storage is unavailable')};state.notes['docs/START-HERE.md']='Keep this unsaved experiment'");
  assert.equal(p.run('save()'), false);
  assert.match(p.nodes['#toast'].textContent, /Export progress/);
  p.run("var exported='';download=(name,data)=>{exported=data}");
  const button = {id: 'export', dataset: {}};
  p.handlers.click({target: {closest: selector => selector === 'button' ? button : null}});
  assert.equal(p.run("JSON.parse(exported).notes['docs/START-HERE.md']"), 'Keep this unsaved experiment');
});

test('restoring duplicate completion, bookmark and gate IDs does not inflate progress', () => {
  const p = portal();
  assert.equal(p.run("validateState({...fresh(),done:['01','01','missing']}).done.length"), 1);
  assert.equal(p.run("validateState({...fresh(),gates:[1,1,9,'2']}).gates.length"), 1);
  assert.equal(p.run("validateState({...fresh(),bookmarks:[A.resources[0].id,A.resources[0].id]}).bookmarks.length"), 1);
});

test('import preserves both conflicting notes and does not append the same backup twice', () => {
  const p = portal();
  p.run("var old={...fresh(),notes:{'docs/START-HERE.md':'Local experiment'}}; var imported={...fresh(),notes:{'docs/START-HERE.md':'Other device experiment'}}; var merged=mergeProgress(old,imported)");
  assert.equal(p.run('merged.conflicts'), 1);
  assert.equal(p.run("merged.state.notes['docs/START-HERE.md']"),
    'Local experiment\n\n--- Imported backup ---\nOther device experiment');
  assert.equal(p.run('mergeProgress(merged.state,imported).conflicts'), 0);
  assert.equal(p.run("mergeProgress({...fresh(),notes:{'docs/START-HERE.md':''}},imported).state.notes['docs/START-HERE.md']"),
    'Other device experiment');
});

test('import is exposed through a keyboard-operable button', () => {
  const html = fs.readFileSync(path.join(ROOT, 'portal/index.html'), 'utf8');
  assert.match(html, /<button id="import-progress"/);
  const p = portal();
  const button = {id: 'import-progress', dataset: {}};
  p.handlers.click({target: {closest: selector => selector === 'button' ? button : null}});
  assert.equal(p.nodes['#import'].clicked, true);
});

test('all eight component hint pages create three separately closed safe disclosures', () => {
  const p=portal();
  for(let n=1;n<=8;n++){
    p.context.hintPath=`content/labs/hints/${String(n).padStart(2,'0')}.md`;
    const html=p.run("markdown(A.documents[hintPath].text,hintPath)");
    assert.equal((html.match(/<details class="progressive-hint">/g)||[]).length,3);
    assert.equal((html.match(/<\/details>/g)||[]).length,3);
    assert.equal((html.match(/<summary>/g)||[]).length,3);
    assert.doesNotMatch(html,/<details[^>]*\bopen\b|&lt;details/);
  }
});

test('safe disclosure parser never admits attributes, executable HTML, or nested tags in summary',()=>{
  const p=portal();
  p.context.unsafe='<details open onclick="alert(1)"><summary>Bad</summary>\n<script>alert(1)</script>\n</details>\n<details><summary><img src=x onerror=alert(1)></summary>\n<details><summary>Safe & clear</summary>\n<script>alert(2)</script>\n</details>';
  const html=p.run("markdown(unsafe,'docs/example.md')");
  assert.doesNotMatch(html,/<script|<img|<details open|<details onclick/);
  assert.match(html,/Safe &amp; clear/);
  assert.match(html,/&lt;script&gt;/);
});

test('version 1 progress migrates and retains original notes, answers, and completion',()=>{
  const p=portal();
  p.run("var legacy={version:1,done:['01'],notes:{'docs/START-HERE.md':'Before the upgrade'},quiz:{'01':2},bookmarks:[],gates:[1]};var migrated=validateState(legacy)");
  assert.equal(p.run('migrated.version'),2);
  assert.equal(p.run("migrated.notes['docs/START-HERE.md']"),'Before the upgrade');
  assert.equal(p.run("migrated.quiz['01']"),2);
  assert.equal(p.run('migrated.done[0]'),'01');
  assert.equal(p.run('Object.keys(migrated.exercises).length'),0);
});

test('attempts and feedback are snapshots, and blank or unsupported reviews cannot pass',()=>{
  const p=portal();
  p.run("var activity=exercises[0];state.exercises[activity.id]=blankRecord(activity)");
  assert.throws(()=>p.run("appendRecord(activity.id,'attempt')"),/first attempt/);
  p.run("state.exercises[activity.id].draft.attempt='First relationship';appendRecord(activity.id,'attempt');state.exercises[activity.id].draft.attempt='Revised relationship';appendRecord(activity.id,'attempt')");
  assert.equal(p.run("state.exercises[activity.id].history[0].attempt"),'First relationship');
  assert.equal(p.run("state.exercises[activity.id].history[1].attempt"),'Revised relationship');
  assert.throws(()=>p.run("appendRecord(activity.id,'feedback')"),/what was checked/);
  p.run("Object.assign(state.exercises[activity.id].draft,{feedback:'Passed',status:'reviewed',basis:'execution'})");
  assert.throws(()=>p.run("appendRecord(activity.id,'feedback')"),/artifact evidence/);
  p.run("state.exercises[activity.id].draft.artifacts='run.json; command and version';appendRecord(activity.id,'feedback')");
  assert.match(p.run("evidenceLabel(state.exercises[activity.id].draft)"),/not independently verified/);
});

test('tutor packet is an allowlist and excludes hidden hints, solutions, instructor code, and history',()=>{
  const p=portal();
  p.run("var a={...exercises[0],hints:['HIDDEN_HINT'],answer:'SECRET_ANSWER',instructorCode:'INSTRUCTOR_CODE',solutions:'SECRET_SOLUTION'};var r=blankRecord(a);r.draft.attempt='My first try';r.history=[{attempt:'OLD_SECRET'}];var packet=tutorPacket(a,r,'hint')");
  const packet=p.run('packet');
  assert.match(packet,/My first try/);
  assert.match(packet,/Give one small hint/);
  for(const sentinel of ['HIDDEN_HINT','SECRET_ANSWER','INSTRUCTOR_CODE','SECRET_SOLUTION','OLD_SECRET'])assert.ok(!packet.includes(sentinel));
  assert.match(packet,/Pass criteria/);
  assert.match(packet,/Current step/);
});

test('all exercises and checks have one-prompt workspace and starter packets',()=>{
  const p=portal();
  assert.equal(p.run('exercises.length'),72);
  assert.equal(p.run('checks.length'),72);
  for(const id of p.run('activities.map(a=>a.id)')){
    p.context.activityId=id;
    const html=p.run('workspace(activityId)');
    assert.match(html,/id="exercise-attempt"/,id);
    assert.match(html,/id="tutor-packet"/,id);
    assert.doesNotMatch(html,/requested-hint/,id);
    assert.match(p.run('tutorPacket(getActivity(activityId),state.exercises[activityId])'),/Pass criteria/,id);
  }
});

test('full v2 export/restore preserves attempts, feedback, recall evidence, route and preferences',()=>{
  const p=portal();
  p.run("var a=exercises[0];state.route='live';state.intervals=[2,5,10,21];state.onboarding=['diagram','evidence'];state.exercises[a.id]=blankRecord(a);state.exercises[a.id].draft.attempt='Work';state.exercises[a.id].draft.misconception='Confused proposals with effects';appendRecord(a.id,'attempt');var item=addRetention(a,state.exercises[a.id]);recallResult(item.id,'difficult','The tool failed, so the effect is not confirmed');state.resume=a.id;var restored=validateState(JSON.parse(JSON.stringify(state)))");
  assert.equal(p.run('JSON.stringify(restored)'),p.run('JSON.stringify(state)'));
  assert.equal(p.run('mergeProgress(fresh(),restored).state.route'),'live');
  assert.equal(p.run('mergeProgress(fresh(),restored).state.intervals[0]'),2);
});

test('cross-device import retains conflicting drafts and same-ID event versions without duplication',()=>{
  const p=portal();
  p.run("var a=exercises[0],left=fresh(),right=fresh();left.exercises[a.id]=blankRecord(a);right.exercises[a.id]=blankRecord(a);left.exercises[a.id].draft.attempt='Local revision';right.exercises[a.id].draft.attempt='Other device';left.exercises[a.id].history=[{id:'same',at:'now',kind:'attempt',attempt:'Local original'}];right.exercises[a.id].history=[{id:'same',at:'now',kind:'attempt',attempt:'Remote original'}];var merged=mergeProgress(left,right);var again=mergeProgress(merged.state,right)");
  assert.equal(p.run('merged.state.exercises[a.id].draft.attempt'),'Local revision');
  assert.deepEqual(JSON.parse(p.run('JSON.stringify(merged.state.exercises[a.id].history.map(e=>e.attempt))')),['Local original','Remote original','Other device']);
  assert.equal(p.run('again.state.exercises[a.id].history.length'),3);
});

test('future edition records remain exportable and malformed imports fail atomically',()=>{
  const p=portal();
  p.run("var incoming=fresh();incoming.exercises.FutureExercise=blankRecord(exercises[0]);incoming.notes['future/document.md']='Keep me'");
  assert.equal(p.run("validateState(incoming).notes['future/document.md']"),'Keep me');
  assert.equal(p.run("Object.hasOwn(validateState(incoming).exercises,'FutureExercise')"),true);
  assert.throws(()=>p.run("validateState({...incoming,exercises:{broken:{}}})"),/nothing imported/);
  assert.equal(p.run('Object.keys(state.exercises).length'),0);
});

test('retention responds to observed difficulty, preserves evidence, and rejects an empty recall',()=>{
  const p=portal();
  p.run("var a=exercises[0],r=blankRecord(a);r.draft.misconception='Need proof of effects';var item=addRetention(a,r)");
  assert.throws(()=>p.run("recallResult(item.id,'recalled','')"),/attempt/);
  p.run("recallResult(item.id,'recalled','New-case explanation')");
  assert.equal(p.run('item.level'),1);
  assert.equal(p.run('item.history[0].intervalDays'),3);
  p.run("recallResult(item.id,'difficult','I still confused the outcome')");
  assert.equal(p.run('item.level'),0);
  assert.equal(p.run('item.history[1].intervalDays'),1);
  assert.equal(p.run('item.history[0].answer'),'New-case explanation');
});

test('quiz display shuffles positions but original answer identities and evidence labels survive',()=>{
  const p=portal();
  for(const id of ['01','02','03']){
    p.context.lessonId=id;
    assert.deepEqual(JSON.parse(p.run('JSON.stringify(quizOrder(lessons.find(l=>l.id===lessonId)).slice().sort())')),[0,1,2,3]);
    assert.match(p.run('quizHTML(lessons.find(l=>l.id===lessonId))'),/not verified practical mastery/);
    assert.equal((p.run('quizHTML(lessons.find(l=>l.id===lessonId))').match(/try a new case/g)||[]).length,3);
  }
});


function incidentFixture(p) {
  p.run("var inc={id:'INC-TEST',isIncident:true,title:'The next shift',briefPath:'content/incidents/test.md',placement:'After a baseline',minutes:'45',budget:'6 checks',prerequisites:['Keep an evidence log'],prompt:'Inspect the observed symptoms and choose your next check.',steps:[{id:'INC-TEST-1',prompt:'Record a hypothesis and compare it with another explanation.'}],criteria:['Preserve evidence'],deliverables:['An evidence log'],hints:['INCIDENT_HINT_ONE','INCIDENT_HINT_TWO','INCIDENT_HINT_THREE'],debrief:'INCIDENT_DEBRIEF_SECRET',transfer:'INCIDENT_TRANSFER_SECRET'};activities.push(inc);state.exercises[inc.id]=blankRecord(inc)");
}
function attemptedIncident(p) {
  p.run("Object.assign(state.exercises[inc.id].draft,{attempt:'The command may be reading a stale report rather than this checkout.',artifacts:'Captured run.txt: timestamp differs from current commit.',nextCheck:'Run the collection command and compare its source revision.'});appendRecord(inc.id,'attempt')");
}

test('incident guidance requires a saved substantive attempt, not drafts or hint/feedback history',()=>{
  const p=portal();incidentFixture(p);
  assert.throws(()=>p.run("requestIncidentGuidance(inc.id,'hint')"),/Save an incident attempt/);
  assert.throws(()=>p.run("appendRecord(inc.id,'attempt')"),/substantive incident/);
  p.run("Object.assign(state.exercises[inc.id].draft,{attempt:' '.repeat(100),artifacts:'An evidence source',nextCheck:'A sufficiently long next check'});");
  assert.throws(()=>p.run("appendRecord(inc.id,'attempt')"),/substantive incident/);
  p.run("state.exercises[inc.id].history.push({id:'hint',at:'now',kind:'hint-request',hintLevel:3},{id:'review',at:'now',kind:'feedback',attempt:'A long explanation that would qualify otherwise',artifacts:'Observed some evidence',nextCheck:'Compare the report and current revision'})");
  assert.equal(p.run('incidentAttempted(state.exercises[inc.id])'),false);
  p.run("Object.assign(state.exercises[inc.id].draft,{attempt:'A substantive current draft with two alternative explanations.',artifacts:'run.txt observed a failure',nextCheck:'Compare the report revision to the checkout.'})");
  assert.equal(p.run('incidentAttempted(state.exercises[inc.id])'),false);
  assert.throws(()=>p.run("requestIncidentGuidance(inc.id,'debrief')"),/Save an incident attempt/);
  assert.doesNotMatch(p.run('workspace(inc.id)'),/INCIDENT_HINT_|INCIDENT_DEBRIEF_SECRET|INCIDENT_TRANSFER_SECRET/);
});

test('incident attempts unlock only deliberate guidance; save, reload-style render and import keep it closed',()=>{
  const p=portal();incidentFixture(p);attemptedIncident(p);
  assert.equal(p.run('incidentAttempted(state.exercises[inc.id])'),true);
  assert.doesNotMatch(p.run('workspace(inc.id)'),/INCIDENT_HINT_|INCIDENT_DEBRIEF_SECRET/);
  p.run("requestIncidentGuidance(inc.id,'hint')");
  let html=p.run('workspace(inc.id)');
  assert.match(html,/INCIDENT_HINT_ONE/);assert.doesNotMatch(html,/INCIDENT_HINT_TWO|INCIDENT_DEBRIEF_SECRET/);
  p.run("requestIncidentGuidance(inc.id,'hint')");
  html=p.run('workspace(inc.id)');assert.match(html,/INCIDENT_HINT_TWO/);assert.doesNotMatch(html,/INCIDENT_DEBRIEF_SECRET/);
  p.run("requestIncidentGuidance(inc.id,'debrief')");assert.match(p.run('workspace(inc.id)'),/INCIDENT_DEBRIEF_SECRET/);
  p.context.location.hash='#incident=INC-TEST';p.run('render()');
  assert.doesNotMatch(p.nodes['#main'].innerHTML,/INCIDENT_HINT_|INCIDENT_DEBRIEF_SECRET/);
  p.run('var incidentBackup=validateState(JSON.parse(JSON.stringify(state)));state=mergeProgress(fresh(),incidentBackup).state;render()');
  assert.equal(p.run('incidentAttempted(state.exercises[inc.id])'),true);
  assert.equal(p.run('state.exercises[inc.id].history.filter(e=>e.kind==="attempt").length'),1);
  assert.doesNotMatch(p.nodes['#main'].innerHTML,/INCIDENT_HINT_|INCIDENT_DEBRIEF_SECRET/);
  p.run("requestIncidentGuidance(inc.id,'debrief');appendRecord(inc.id,'attempt');render()");
  assert.doesNotMatch(p.nodes['#main'].innerHTML,/INCIDENT_DEBRIEF_SECRET/);
});

test('incident alias routes remain gated and freeform work cannot inject executable markup',()=>{
  const p=portal();incidentFixture(p);
  p.run("state.exercises[inc.id].draft.attempt='<img src=x onerror=alert(1)> and a hypothesis';state.exercises[inc.id].draft.nextCheck='<script>alert(1)</script> is learner text'");
  for(const route of ['#incident=INC-TEST','#exercise=INC-TEST']) {
    p.context.location.hash=route;p.run('render()');
    const html=p.nodes['#main'].innerHTML;
    assert.doesNotMatch(html,/<img|<script|INCIDENT_HINT_|INCIDENT_DEBRIEF_SECRET/);
    assert.match(html,/&lt;img/);assert.match(html,/id="incident-debrief" disabled/);
  }
  assert.throws(()=>p.run("validateState({...state,exercises:{[inc.id]:{...state.exercises[inc.id],draft:{...state.exercises[inc.id].draft,nextCheck:{bad:'shape'}}}}})"),/nothing imported/);
});

test('incident tutor packets include next check but omit guidance, transfer answers, and feedback',()=>{
  const p=portal();incidentFixture(p);attemptedIncident(p);
  p.run("state.exercises[inc.id].draft.feedback='PRIVATE_REVIEW';requestIncidentGuidance(inc.id,'debrief')");
  const packet=p.run('tutorPacket(inc,state.exercises[inc.id])');
  assert.match(packet,/Next discriminating check/);assert.match(packet,/Run the collection command/);
  assert.doesNotMatch(packet,/INCIDENT_HINT_|INCIDENT_DEBRIEF_SECRET|INCIDENT_TRANSFER_SECRET|PRIVATE_REVIEW/);
});

test('import into a just-opened incident adopts its saved draft and step while preserving both histories',()=>{
  const p=portal();incidentFixture(p);attemptedIncident(p);
  p.run("var incidentImport=validateState(JSON.parse(JSON.stringify(state)));incidentImport.exercises[inc.id].step='INC-TEST-review';state=fresh();workspace(inc.id);state.exercises[inc.id].history.push({id:'earlier-local',at:'now',kind:'attempt',step:'INC-TEST-old',attempt:'Earlier local evidence'});var importedIncident=mergeProgress(state,incidentImport);state=importedIncident.state");
  assert.equal(p.run('importedIncident.conflicts'),0);
  assert.equal(p.run("state.exercises[inc.id].step"),'INC-TEST-review');
  assert.equal(p.run("state.exercises[inc.id].draft.nextCheck"),'Run the collection command and compare its source revision.');
  assert.equal(p.run("state.exercises[inc.id].history.filter(e=>e.kind==='attempt').length"),2);
  assert.equal(p.run("incidentAttempted(state.exercises[inc.id])"),true);
  assert.doesNotMatch(p.run('workspace(inc.id)'),/INCIDENT_HINT_|INCIDENT_DEBRIEF_SECRET/);
  p.run("state.exercises[inc.id].draft.nextCheck='My new local check should remain visible';var conflictingImport=mergeProgress(state,incidentImport)");
  assert.equal(p.run("conflictingImport.state.exercises[inc.id].draft.nextCheck"),'My new local check should remain visible');
  assert.equal(p.run("conflictingImport.state.exercises[inc.id].history.filter(e=>e.kind==='imported-draft').length"),1);
});

test('run-anywhere route distinguishes local and hosted copies without changing progress',()=>{
  const p=portal();
  p.context.location.hash='#run';
  p.context.location.hostname='127.0.0.1';
  p.run("state.notes['lesson-note']='Keep my learning record';render()");
  assert.match(p.nodes['#main'].innerHTML,/You are using the local academy/);
  assert.match(p.nodes['#main'].innerHTML,/python3 academy.py local/);
  assert.match(p.nodes['#main'].innerHTML,/academy-portable.zip/);
  assert.match(p.nodes['#main'].innerHTML,/Export and import JSON/);
  assert.match(p.nodes['#nav'].innerHTML,/Run anywhere/);
  p.context.location.hostname='signal-desk-ai-engineering-academy.igor-sadovyi87.chatgpt.site';
  p.run('render()');
  assert.match(p.nodes['#main'].innerHTML,/You are using the OpenAI-hosted academy/);
  assert.equal(p.run("state.notes['lesson-note']"),'Keep my learning record');
  assert.doesNotMatch(p.nodes['#main'].innerHTML,/incident-debrief|requested-hint/);
});

const tick=()=>new Promise(resolve=>setImmediate(resolve));
function localServer(){
 const store={state:null,revision:0,databaseId:'test-db',databasePath:'/private/test/progress.sqlite3',puts:[],fail:false};
 store.fetch=async (url,options={})=>{
  assert.equal(url,'/api/local-state');
  if(options.method==='PUT'){
   if(store.fail)throw Error('Connection lost');
   assert.equal(options.headers['X-Academy-Token'],'token');
   const body=JSON.parse(options.body);store.puts.push(body);
   if(body.revision!==store.revision)return {ok:false,status:409};
   store.state=body.state;store.revision++;
   return {ok:true,status:200,json:async()=>({revision:store.revision})};
  }
  return {ok:true,status:200,json:async()=>({kind:'academy-local',databaseId:store.databaseId,databasePath:store.databasePath,revision:store.revision,state:store.state&&JSON.parse(JSON.stringify(store.state)),csrfToken:'token'})};
 };
 return store;
}
async function localPortal(server,options={}){
 const p=portal({...options,location:{hostname:'127.0.0.1',hash:'#overview',...(options.location||{})},fetch:server.fetch});
 await tick();return p;
}

test('hosted pages never probe or send progress to the local API',async()=>{
 const p=portal({location:{hostname:'academy.example'},fetch:()=>{throw Error('Must not call API')}});
 p.run("state.notes.example='Hosted-only note';save()");
 assert.equal(p.run('persistence.mode'),'browser');assert.equal(p.run('saveStatusText()'),'Saved in this browser');
 assert.equal(p.run("JSON.parse(localStorage.getItem(KEY)).notes.example"),'Hosted-only note');
});

test('local startup blocks editing until the database response is validated',async()=>{
 const server=localServer();let resolve;
 const p=portal({location:{hostname:'127.0.0.1'},fetch:()=>new Promise(r=>{resolve=r})});
 assert.equal(p.run('storageLocked()'),true);assert.match(p.nodes['#main'].innerHTML,/Connect your saved work first/);
 const button={id:'mark-done',dataset:{id:'01'}};
 p.handlers.click({target:{closest:s=>s==='button'?button:null}});
 assert.equal(p.run('state.done.length'),0);
 resolve(await server.fetch('/api/local-state'));await tick();
 assert.equal(p.run('persistence.mode'),'local');assert.equal(p.run('storageLocked()'),false);
});

test('committed local state restores all learning fields in a fresh browser with no cache',async()=>{
 const server=localServer(),p=await localPortal(server);
 p.run("state.notes.example='Retained note';state.done=['01'];state.onboarding=['diagram'];state.quiz['01']=1;state.exercises['L01-E1']=blankRecord(getActivity('L01-E1'));state.exercises['L01-E1'].draft.attempt='A draft before saving history';state.exercises['L01-E1'].draft.misconception='Context boundaries';addRetention(getActivity('L01-E1'),state.exercises['L01-E1']);save()");
 await tick();await p.run('flushLocal()');
 assert.equal(p.run('saveStatusText()'),'Saved locally in SQLite');
 const restored=await localPortal(server);
 assert.deepEqual(JSON.parse(restored.run('JSON.stringify(state)')),JSON.parse(p.run('JSON.stringify(state)')));
 assert.equal(restored.run('state.retention.length'),1);assert.equal(restored.run("state.exercises['L01-E1'].draft.attempt"),'A draft before saving history');
});

test('legacy browser migration requires a choice, preserves both conflicting notes, and provides recovery copies',async()=>{
 const server=localServer(),base=portal();server.state=JSON.parse(base.run('JSON.stringify(fresh())'));server.state.notes.example='Database observation';server.revision=3;
 const old={...server.state,notes:{example:'Older browser observation'}};
 const p=await localPortal(server,{storage:{'ai-engineering-academy-v1':JSON.stringify(old)}});
 assert.equal(p.run('persistence.mode'),'conflict');assert.equal(server.puts.length,0);
 p.run("handleStorageClick({id:'storage-merge',dataset:{}})");await tick();
 assert.match(server.state.notes.example,/Database observation/);assert.match(server.state.notes.example,/Older browser observation/);
 assert.ok(p.run('recoveries.length')>=2);assert.equal(p.run('persistence.mode'),'local');
});

test('a stale tab cannot overwrite newer work and explicit merge keeps both drafts',async()=>{
 const server=localServer(),first=await localPortal(server),second=await localPortal(server);
 first.run("state.exercises['L01-E1']=blankRecord(getActivity('L01-E1'));state.exercises['L01-E1'].draft.attempt='First browser draft';save()");await tick();
 second.run("state.exercises['L01-E1']=blankRecord(getActivity('L01-E1'));state.exercises['L01-E1'].draft.attempt='Second browser draft';save()");await tick();
 assert.equal(second.run('persistence.mode'),'conflict');assert.equal(server.state.exercises['L01-E1'].draft.attempt,'First browser draft');
 second.run("handleStorageClick({id:'storage-merge',dataset:{}})");await tick();
 assert.equal(server.state.exercises['L01-E1'].draft.attempt,'First browser draft');
 assert.ok(server.state.exercises['L01-E1'].history.some(x=>x.kind==='imported-draft'&&x.attempt==='Second browser draft'));
 assert.equal(second.run('saveStatusText()'),'Saved locally in SQLite');
});

test('failed writes remain visibly unsaved, survive reload as pending recovery, and save only after reconciliation',async()=>{
 const server=localServer(),p=await localPortal(server);server.fail=true;
 p.run("state.notes.example='Do not lose this uncommitted draft';save()");await tick();
 assert.match(p.run('saveStatusText()'),/Unsaved/);assert.equal(server.state,null);
 const reloaded=await localPortal(server,{storage:p.storage});
 assert.equal(reloaded.run('persistence.mode'),'conflict');assert.equal(reloaded.run('state.notes.example'),'Do not lose this uncommitted draft');
 server.fail=false;reloaded.run("handleStorageClick({id:'storage-merge',dataset:{}})");await tick();
 assert.equal(server.state.notes.example,'Do not lose this uncommitted draft');assert.equal(reloaded.run('saveStatusText()'),'Saved locally in SQLite');
});

test('local writes are serialized and edits made during a write are included in the next revision',async()=>{
 const server=localServer(),originalFetch=server.fetch;let release;
 server.fetch=async(url,options)=>{if(options.method==='PUT'&&!release)await new Promise(r=>{release=r});return originalFetch(url,options)};
 const p=await localPortal(server);p.run("state.notes.example='First';save()");p.run("state.notes.example='Last';save()");
 assert.match(p.run('saveStatusText()'),/Saving/);release();await tick();await p.run('flushLocal()');
 assert.equal(server.puts.length,2);assert.deepEqual(server.puts.map(x=>x.revision),[0,1]);assert.equal(server.state.notes.example,'Last');
});

test('static preview explicitly reports browser-only storage; server failure never reports a database save',async()=>{
 const p=portal({location:{hostname:'localhost'},fetch:async()=>({ok:false,status:404})});await tick();
 assert.equal(p.run('persistence.mode'),'browser');assert.match(p.nodes['#storage-notice'].innerHTML,/Static preview/);
 p.run("state.notes.example='Static preview';save()");assert.match(p.run('saveStatusText()'),/browser/);
 const broken=portal({location:{hostname:'localhost'},fetch:async()=>{throw Error('Offline')}});await tick();
 assert.equal(broken.run('persistence.mode'),'unavailable');assert.equal(broken.run('storageLocked()'),true);assert.doesNotMatch(broken.run('saveStatusText()'),/Saved locally/);
});

test('a prepared new-account copy points to publishing instructions and not the old Site',()=>{
 const p=portal();p.run('A.runtime.hostedUrl=null');
 assert.match(p.run('runAnywhere()'),/Publish in your new OpenAI account/);
 assert.doesNotMatch(p.run('runAnywhere()'),/href="null|href="#\/|signal-desk-ai-engineering-academy/);
});

test('reconciling a recovered tab copy never removes a newer pending draft from that live tab',async()=>{
 const server=localServer(),first=await localPortal(server);server.fail=true;
 first.run("state.notes.example='Original pending draft';save()");await tick();
 const second=await localPortal(server,{storage:first.storage});assert.equal(second.run('persistence.mode'),'conflict');
 first.run("state.notes.example='Newer pending draft from the still-open tab';save()");await tick();
 const firstKey=first.run('TAB_CACHE');assert.match(first.storage[firstKey],/Newer pending draft/);
 server.fail=false;second.run("handleStorageClick({id:'storage-merge',dataset:{}})");await tick();
 assert.match(first.storage[firstKey],/Newer pending draft/);
 const third=await localPortal(server,{storage:first.storage});assert.equal(third.run('persistence.mode'),'conflict');assert.match(third.run('JSON.stringify(state)'),/Newer pending draft/);
});

test('independent tabs retain immutable recovery archives rather than replacing a shared array',async()=>{
 const server=localServer(),one=await localPortal(server),two=await localPortal(server,{storage:one.storage});
 one.run("state.notes.example='First archived draft';archiveRecovery(state,'First tab')");
 two.run("state.notes.example='Second archived draft';archiveRecovery(state,'Second tab')");
 const reloaded=await localPortal(server,{storage:one.storage});
 assert.equal(reloaded.run("recoveries.filter(x=>x.label==='First tab'||x.label==='Second tab').length"),2);
 assert.match(reloaded.run('JSON.stringify(recoveries)'),/First archived draft/);assert.match(reloaded.run('JSON.stringify(recoveries)'),/Second archived draft/);
});

test('a valid database-sized progress export above the old 5 MB limit can be reimported',async()=>{
 const p=portal();const text=p.run("JSON.stringify({...fresh(),notes:{example:'x'.repeat(5100000)}})");
 const input={id:'import',dataset:{},files:[{size:Buffer.byteLength(text),text:async()=>text}],value:'selected'};
 await p.handlers.change({target:input});assert.equal(p.run('state.notes.example.length'),5100000);
 assert.equal(input.value,'');
});

test('import validates the final merged UTF-8 request size before changing current work',async()=>{
 const p=portal();p.run("state.notes.current='Current observation'");
 const text=p.run("JSON.stringify({...fresh(),notes:{large:'中'.repeat(3000000)}})");
 await p.handlers.change({target:{id:'import',dataset:{},files:[{size:Buffer.byteLength(text),text:async()=>text}],value:'selected'}});
 assert.equal(p.run('state.notes.current'),'Current observation');assert.equal(p.run('state.notes.large'),undefined);
 assert.match(p.nodes['#toast'].textContent,/8 MiB/);
});

test('indented setup fences keep new-account clone and launch commands on separate preformatted lines',()=>{
 const p=portal();
 const html=p.run("markdown(A.documents['docs/NEW-ACCOUNT.md'].text,'docs/NEW-ACCOUNT.md')");
 assert.match(html,/<pre><code>[^<]*git clone[^<]*\n[^<]*cd is-qa-ai-edu[^<]*<\/code><\/pre>/);
 const escaped=p.run("markdown('1. Example\\n\\n   ```sh\\n   echo <safe>\\n   pwd\\n   ```','docs/NEW-ACCOUNT.md')");
 assert.match(escaped,/<pre><code>   echo &lt;safe&gt;\n   pwd<\/code><\/pre>/);
 assert.doesNotMatch(escaped,/<safe>/);
});

test('restoring an older database or changing content at the same revision preserves newer browser work for reconciliation',async()=>{
 for(const restoredRevision of [5,10]){
  const server=localServer(),baseline=portal();server.state=JSON.parse(baseline.run('JSON.stringify(fresh())'));server.state.notes.example='Older restored database copy';server.revision=restoredRevision;
  const newer={...server.state,notes:{example:'Newer previously committed browser copy'}};
  const storage={'ai-engineering-academy-v1-local-cache':JSON.stringify({databaseId:server.databaseId,revision:10,pending:false,state:newer})};
  const p=await localPortal(server,{storage});assert.equal(p.run('persistence.mode'),'conflict');assert.equal(server.puts.length,0);
  assert.equal(p.run('state.notes.example'),'Newer previously committed browser copy');
  p.run("handleStorageClick({id:'storage-merge',dataset:{}})");await tick();
  assert.match(server.state.notes.example,/Newer previously committed/);assert.match(server.state.notes.example,/Older restored/);
 }
});

test('the new entrance offers reading without creating practice or completion records',()=>{
 const p=portal();const before=p.run('JSON.stringify(state)');
 assert.match(p.nodes['#main'].innerHTML,/Start from zero/);
 assert.match(p.nodes['#main'].innerHTML,/href="#start"/);
 assert.equal((p.nodes['#nav'].innerHTML.match(/class="nav-stage"/g)||[]).length,8);
 for(let i=1;i<=8;i++){
  p.context.topic=String(i).padStart(2,'0');
  p.run("location.hash='#guide='+topic;render()");
  assert.match(p.nodes['#main'].innerHTML,/One selected reading/);
  assert.doesNotMatch(p.nodes['#main'].innerHTML,/id="exercise-attempt"|id="mark-done"/);
 }
 assert.equal(p.run('JSON.stringify(state)'),before);
});

test('saved reading location survives export, validation, and merge without awarding completion',()=>{
 const p=portal();
 p.run("state.reading='04';state.notes[A.guide.topics[3].file]='Question about graders';var restored=validateState(JSON.parse(JSON.stringify(state)));var merged=mergeProgress(fresh(),restored).state");
 assert.equal(p.run('restored.reading'),'04');assert.equal(p.run('merged.reading'),'04');
 assert.equal(p.run('merged.done.length'),0);assert.equal(p.run('Object.keys(merged.exercises).length'),0);
 p.run("var old=clone(state);delete old.reading;var legacy=validateState(old)");
 assert.equal(p.run('legacy.reading'),'');
 p.run("state.reading='07';var conflict=mergeProgress(state,restored).state");
 assert.equal(p.run('conflict.reading'),'07');
 assert.match(p.run('overview()'),/href="#guide=07"/);
});

test('guided reading notes and position survive the local database persistence adapter',async()=>{
 const server=localServer(),p=await localPortal(server);
 p.run("state.reading='05';state.notes[A.guide.topics[4].file]='Which source was retrieved?';save()");await tick();
 const resumed=await localPortal(server);
 assert.equal(resumed.run('state.reading'),'05');
 assert.equal(resumed.run('state.notes[A.guide.topics[4].file]'),'Which source was retrieved?');
 assert.equal(resumed.run('state.done.length'),0);
});

test('all original lesson exercises remain available below beginner teaching',()=>{
 const p=portal();
 p.run("location.hash='#lesson=01';render()");
 assert.match(p.nodes['#main'].innerHTML,/Start with the beginner guide/);
 assert.match(p.nodes['#main'].innerHTML,/Exercise 1/);
 assert.match(p.nodes['#main'].innerHTML,/id="original-lesson"/);
 assert.equal((p.run('learningPath()').match(/class="lesson-row"/g)||[]).length,24);
});

test('lesson bookmarks preserve old primer bookmarks and survive local persistence',async()=>{
 const server=localServer(),p=await localPortal(server);
 p.run("state.reading='04';state.lessonReading='13';save()");await tick();
 const resumed=await localPortal(server);
 assert.equal(resumed.run('state.reading'),'04');assert.equal(resumed.run('state.lessonReading'),'13');
 assert.match(resumed.run('overview()'),/href="#lesson=13"/);
 assert.equal(resumed.run('state.done.length'),0);
 p.run("var imported=validateState(JSON.parse(JSON.stringify(state)));var merged=mergeProgress(fresh(),imported).state");
 assert.equal(p.run('merged.lessonReading'),'13');assert.equal(p.run('merged.reading'),'04');
 p.run("var legacy=clone(state);delete legacy.lessonReading;var restored=validateState(legacy)");
 assert.equal(p.run('restored.lessonReading'),'');
});
test('all lessons have a teaching guide, internal materials, and protected original solutions',()=>{
 const p=portal();assert.equal(p.run('course.length'),24);
 assert.equal((p.run('learningPath()').match(/class="lesson-row"/g)||[]).length,24);
 for(let i=1;i<=24;i++){
  p.context.lessonId=String(i).padStart(2,'0');
  p.run("location.hash='#lesson='+lessonId;render()");
  const html=p.nodes['#main'].innerHTML;
  for(const id of ['try-it-with-codex-or-claude-code','what-you-should-see','if-it-goes-wrong','lesson-materials','original-lesson'])assert.ok(html.includes('id="'+id+'"'),p.context.lessonId+' '+id);
  assert.ok(html.includes('id="reveal-lesson-solution" data-id="'+p.context.lessonId+'" disabled'));
 }
 assert.equal(p.run('state.done.length'),0);
});

test('the last explicitly saved kind chooses resume without erasing the other bookmark',()=>{
 const p=portal();p.run("state.reading='04';state.lessonReading='13';state.readingKind='primer'");
 assert.match(p.run('overview()'),/href="#guide=04"/);
 p.run("state.readingKind='lesson'");assert.match(p.run('overview()'),/href="#lesson=13"/);
 p.run("var copy=validateState(clone(state));var combined=mergeProgress(fresh(),copy).state");
 assert.equal(p.run('combined.readingKind'),'lesson');assert.equal(p.run('combined.reading'),'04');assert.equal(p.run('combined.lessonReading'),'13');
});

test('sidebar indexes every stage and lesson and resolves deep-link learning context',()=>{
 const p=portal();const original=p.run('JSON.stringify(state)');
 assert.equal((p.nodes['#nav'].innerHTML.match(/class="nav-lesson /g)||[]).length,24);
 for(const route of ['#lesson=13','#doc=content%2Fhow-to%2F13.md','#exercise=L13-E2']){
  p.context.route=route;p.run("location.hash=route;nav('path')");
  assert.match(p.nodes['#nav'].innerHTML,/class="nav-lesson active" data-lesson="13"/);
  assert.match(p.nodes['#nav'].innerHTML,/data-stage="5" open/);
 }
 assert.equal(p.run('JSON.stringify(state)'),original);
});
test('sidebar search finds technical terminology and sections without changing progress',()=>{
 const p=portal();const original=p.run('JSON.stringify(state)');
 p.run("sidebarQuery='state machine';nav('overview')");
 assert.match(p.nodes['#nav'].innerHTML,/data-lesson="13"/);
 assert.doesNotMatch(p.nodes['#nav'].innerHTML,/data-lesson="01"/);
 p.run("sidebarQuery='books';nav('overview')");assert.match(p.nodes['#nav'].innerHTML,/href="#library"/);
 p.run("sidebarQuery='no-such-zzzz';nav('overview')");assert.match(p.nodes['#nav'].innerHTML,/No matches/);
 p.run("sidebarQuery='';nav('overview')");assert.equal((p.nodes['#nav'].innerHTML.match(/class="nav-lesson /g)||[]).length,24);
 assert.equal(p.run('JSON.stringify(state)'),original);
});

test('reading links stay in the canonical lesson and retain their target sections',()=>{
 const p=portal();
 assert.equal(p.run("resolveHref('02.md','content/how-to/01.md')"),'#lesson=02');
 assert.equal(p.run("resolveHref('13.md#the-idea-in-plain-language','content/how-to/12.md')"),'#lesson=13&section=the-idea-in-plain-language');
 assert.equal(p.run("resolveHref('../lessons/01-systems-before-agents.md','content/how-to/01.md')"),'#lesson=01&section=original-lesson');
 assert.equal(p.run("materialEntries().find(e=>e.kind==='Beginner how-to'&&e.href==='#lesson=01').href"),'#lesson=01');
});

test('all lessons and stages offer an ungated next step including the last lesson',()=>{
 const p=portal(),before=p.run('JSON.stringify(state)');
 for(let n=0;n<24;n++){
  p.context.n=n;const html=p.run('lessonNext(lessons[n])');
  assert.match(html,new RegExp(n===23?'href="#capstones"':'href="#lesson='+String(n+2).padStart(2,'0')+'"'));
  assert.doesNotMatch(html,/disabled|mark-done/);
 }
 assert.match(p.run('lessonNext(lessons[2])'),/Next · Stage 2/);
 assert.match(p.run('stage(1)'),/Begin this stage: lesson 01/);
 assert.match(p.run('lessonNext(lessons[23])'),/optional capstones/);
 assert.equal(p.run('JSON.stringify(state)'),before);
});

test('supporting reading offers a route back without saving inferred progress',()=>{
 const p=portal(),before=p.run('JSON.stringify(state)');
 assert.match(p.run("readingReturn('docs/ASSISTANT-QUICKSTART.md')"),/Start lesson 01/);
 p.run("location.hash='#lesson=13';nav('path')");
 assert.match(p.run("readingReturn('docs/ASSISTANT-QUICKSTART.md')"),/Return to lesson 13/);
 assert.match(p.run("readingReturn('content/how-to/02.md')"),/Open lesson 02/);
 p.run("sidebarQuery='state machine';clearSidebarSearch();nav('path')");
 assert.equal(p.run('sidebarQuery'),'');
 assert.equal((p.nodes['#nav'].innerHTML.match(/class="nav-lesson /g)||[]).length,24);
 assert.equal(p.run('JSON.stringify(state)'),before);
});

test('subject navigation exposes every subject and retains original lesson identities',()=>{
 const p=portal(),before=p.run('JSON.stringify(state)');
 assert.equal(p.run('trackCatalog.length'),14);
 assert.equal(p.run('trackTopics.length'),84);
 assert.equal(p.run('new Set(trackTopics.filter(t=>t.lesson).map(t=>t.lesson)).size'),24);
 assert.equal((p.run('overview()').match(/class="doc-card track-card"/g)||[]).length,14);
 for(const t of p.run('trackTopics')){
  p.context.topic=t;
  const html=p.run('topicPage(topic.id)');
  assert.match(html,/id="save-topic-reading"/);assert.match(html,/id="try-it-with-codex-or-claude-code"/);
  if(t.lesson)assert.match(html,/id="reveal-lesson-solution"[^>]+disabled/);
 }
 assert.equal(p.run('JSON.stringify(state)'),before);
});
test('path navigation follows its own order and rejects unrelated path context',()=>{
 const p=portal();
 for(const path of p.run('learningPaths')){
  p.context.path=path;
  for(let i=0;i<path.topics.length;i++){
   p.context.index=i;
   const html=p.run('topicContinue(getTopic(path.topics[index]),path.id)');
   assert.ok(html.includes(i+1<path.topics.length?'href="#topic='+path.topics[i+1]+'?path='+path.id+'"':'href="#path"'));
  }
 }
 assert.equal(p.run("topicSequence(getTopic('mcp-basics'),'zero').path"),null);
 assert.match(p.run("topicPage('mcp-basics','unknown')"),/data-path=""/);
});
test('subject bookmark and path survive validation/merge alongside old bookmarks and attempts',()=>{
 const p=portal();p.run("state.reading='04';state.lessonReading='13';state.topicReading='mcp-basics';state.topicPath='builder';state.readingKind='topic';var restored=validateState(clone(state));var combined=mergeProgress(fresh(),restored).state");
 assert.equal(p.run('combined.topicReading'),'mcp-basics');assert.equal(p.run('combined.topicPath'),'builder');assert.equal(p.run('combined.lessonReading'),'13');assert.equal(p.run('combined.reading'),'04');
 assert.match(p.run('overview()'),/href="#topic=mcp-basics\?path=builder"/);
 p.run("state.readingKind='primer'");assert.match(p.run('overview()'),/href="#guide=04"/);
 p.run("var old=clone(state);delete old.topicReading;delete old.topicPath;var migrated=validateState(old)");assert.equal(p.run('migrated.topicReading'),'');assert.equal(p.run('migrated.topicPath'),'');
 p.run("var current=fresh();current.topicReading='skills-basics';current.topicPath='sdet';current.readingKind='topic';var merged=mergeProgress(current,restored).state");assert.equal(p.run('merged.topicReading'),'skills-basics');assert.equal(p.run('merged.topicPath'),'sdet');
 assert.equal(p.run('combined.done.length'),0);assert.equal(p.run('Object.keys(combined.exercises).length'),0);
});
test('subject context keeps internal reading links and detour returns in the chosen path',()=>{
 const p=portal();p.run("topicPage('foundations-orientation','zero')");
 assert.equal(p.run("learningLink('content/how-to/02.md')"),'#topic=prompting-task-contract?path=zero');
 assert.match(p.run("readingReturn('docs/ASSISTANT-QUICKSTART.md')"),/href="#topic=foundations-orientation\?path=zero"/);
 p.run("location.hash='#lesson=13';render()");assert.match(p.run("readingReturn('docs/ASSISTANT-QUICKSTART.md')"),/href="#lesson=13"/);
});
test('subject bookmark uses unchanged local database adapter and preserves original lesson notes',async()=>{
 const server=localServer(),p=await localPortal(server);p.run("state.topicReading='mcp-basics';state.topicPath='builder';state.readingKind='topic';state.notes[getTopic('mcp-basics').file]='Protocol question';state.notes[lessons[12].file]='Earlier harness note';save()");await tick();
 const resumed=await localPortal(server);assert.equal(resumed.run('state.topicReading'),'mcp-basics');assert.equal(resumed.run('state.topicPath'),'builder');assert.equal(resumed.run('state.notes[lessons[12].file]'),'Earlier harness note');assert.equal(resumed.run('state.done.length'),0);
});

test('retained inline next suggestions become related reading inside subject paths',()=>{
 const p=portal();p.run("readingTopicId='foundations-orientation';readingPathId='zero'");
 const html=p.run("subjectTeaching(getTopic('foundations-orientation'))");
 assert.match(html,/Related reading:/);assert.doesNotMatch(html,/Proceed to/);assert.doesNotMatch(html,/<h1[^>]*>01 ·/);
 assert.match(p.run("topicContinue(getTopic('foundations-orientation'),'zero')"),/href="#topic=foundations-tokens\?path=zero"/);
});

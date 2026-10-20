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
    curriculum: JSON.parse(fs.readFileSync(path.join(ROOT, 'content/curriculum.json'), 'utf8')),
    learning: JSON.parse(fs.readFileSync(path.join(ROOT, 'content/learning.json'), 'utf8')),
    resources: JSON.parse(fs.readFileSync(path.join(ROOT, 'content/resources.json'), 'utf8')),
    documents,
    assets: ['content/resources.json', 'content/labs/solutions/reference.py',
      'content/research/sources.json', 'content/research/cases.json',
      'content/dev-sandbox/router.py', 'content/dev-sandbox/test_router.py'],
  };
}

function portal() {
  const nodes = {}, handlers = {}, storage = {};
  const context = vm.createContext({
    window: {ACADEMY: academy(), scrollTo() {}, addEventListener() {}},
    document: {
      title: '',
      querySelector: selector => nodes[selector] ||= {
        innerHTML: '', textContent: '', style: {}, focus() {}, click() {this.clicked = true;},
      },
      querySelectorAll: () => [],
      getElementById: () => null,
      addEventListener: (kind, callback) => {handlers[kind] = callback;},
    },
    localStorage: {getItem: key => storage[key] || null, setItem: (key, value) => {storage[key] = value;}},
    location: {hash: '#overview'},
    URLSearchParams, setTimeout: () => 0, clearTimeout() {},
  });
  vm.runInContext(fs.readFileSync(path.join(ROOT, 'portal/app.js'), 'utf8'), context);
  return {run: code => vm.runInContext(code, context), nodes, handlers, context};
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

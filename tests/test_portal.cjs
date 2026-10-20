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

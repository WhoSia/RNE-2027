/* Exercise the standalone exhibit's DOM event handlers without a browser binary. */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");

class Element {
  constructor() { this.children = []; this.listeners = {}; }
  addEventListener(event, run) { this.listeners[event] = run; }
  append(child) { this.children.push(child); }
  replaceChildren(...children) { this.children = children; }
  setAttribute() {}
  insertCell() { const cell = new Element(); this.append(cell); return cell; }
  click() { this.listeners.click(); }
  set textContent(value) { this.valueText = value; this.children = []; }
  get textContent() { return this.valueText ?? ""; }
}

const html = fs.readFileSync(process.argv[2], "utf8");
const elements = new Map([...html.matchAll(/\bid="([a-z]+)"/g)].map(m => [m[1], new Element()]));
const get = id => elements.get(id);
get("experiment").textContent = html.match(/id="experiment">([^<]+)<\/script>/)[1];
get("penalty").value = "60";
get("bypass").value = "0";
vm.runInNewContext(html.match(/<script>([\s\S]+)<\/script>/)[1], {
  document: {querySelector: () => get("experiment"), getElementById: get,
             createElement: () => new Element()},
});
assert.match(get("summary").textContent, /8개/);
get("through").click();
assert.match(get("choice").textContent, /27$/);
for (const index of [1, 2]) get("bins").children[index].click();
assert.match(get("best").textContent, /9$/);
get("bins").children[0].click();
assert.match(get("best").textContent, /좌회전 먼저 · 0$/);
get("penalty").value = "120";
get("penalty").listeners.change();
assert.match(get("best").textContent, /직진 먼저 · 0$/);
get("penalty").value = "60";
get("penalty").listeners.change();
get("next").click();
for (const bin of get("bins").children) bin.click();
assert.match(get("best").textContent, /직진 먼저 · 0$/);
get("bypass").value = "1";
get("bypass").listeners.change();
assert.match(get("summary").textContent, /1개/);
assert.match(get("best").textContent, /좌회전 먼저 · 0$/);
get("bypass").value = "0";
get("bypass").listeners.change();
for (let i = 0; i < 8; i++) {
  get("next").click();
  assert.match(get("summary").textContent, /8개/);
  for (const bin of get("bins").children) bin.click();
  assert.match(get("summary").textContent, /1개/);
}
console.log("Offline exhibit: all 8 cases and the 27 → 9 → 0 reveal sequence passed");

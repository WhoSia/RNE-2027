/* Execute the offline app with a small DOM/Canvas stub to check data-bound behavior. */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");

class Element {
  constructor() { this.value = ""; this.children = []; this.calls = []; }
  add(option) {
    this.children.push(option);
    if (this.children.length === 1) this.value = option.value;
  }
  append(...children) { this.children.push(...children); }
  replaceChildren(...children) { this.children = children; }
  click() { this.calls.push("click"); if (this.onclick) this.onclick(); }
  set textContent(message) { this.message = message; }
  get textContent() { return this.message ?? this.children.map(c=>c.textContent ?? c).join(" "); }
}

const html = fs.readFileSync(process.argv[2], "utf8");
const payload = html.match(/id="observations" type="application\/json">([\s\S]+?)<\/script>/)[1];
const script = html.match(/<script>\s*("use strict";[\s\S]+?)<\/script>/)[1];
const ids = [...html.matchAll(/id="([a-z_]+)"/g)].map(m=>m[1]);
const elements = new Map(ids.map(id=>[id,new Element()]));
const get = id=>elements.get(id);
const renderCalls = [];
const ctx = new Proxy({}, {get(obj,key) {
  return obj[key] ?? ((...args)=>renderCalls.push([key,...args]));
}});
Object.assign(get("map"), {getContext:()=>ctx,width:1080,height:500});
get("observations").textContent = payload;
let savedBlob;
const env = {
  document: {
    getElementById: get,
    createElement: ()=>new Element(),
  },
  Option: class { constructor(label,value) { this.label=label;this.value=value; } },
  clearInterval:()=>{}, setInterval:()=>1, setTimeout:()=>{},
  Blob, URL:{createObjectURL(blob){savedBlob=blob; return "blob:test";},revokeObjectURL(){}}
};
const originalAppend = Element.prototype.append;
Element.prototype.append = function(...children) {
  for (const node of children) if (node?.id) elements.set(node.id,node);
  originalAppend.apply(this,children);
};
vm.runInNewContext(script,env);
assert.equal(get("case").children.length,8);
for(let i=0;i<8;i++) {
  get("case").value=i; get("case").onchange();
  assert.match(get("vehicles").textContent,/A.*m\/s.*B.*m\/s/);
  get("next").click(); assert.match(get("clock").textContent,/\+0\.10/);
  get("focus").click(); assert.match(get("signals").textContent,/헤드 3/);
}
get("case").value=2;get("case").onchange();
get("time").value=5100;get("time").oninput();
assert.match(get("vehicles").children[0].textContent,/관측 없음/);
assert.match(get("vehicles").children[1].textContent,/m\/s/);
get("reviewer").value="QA-test";
for(const key of ["leader_movement","follower_movement","cannot_advance","lead_or_lane_change","downstream_space","signal_for_follower","tracking_gap","judgment"]) get(key).value="unknown";
get("evidence").value="synthetic application check";
get("save").click();
get("case").value=3;get("case").onchange();
get("case").value=2;get("case").onchange();
assert.equal(get("evidence").value,"synthetic application check");
get("download").click();
savedBlob.text().then(text=>{
  const item=JSON.parse(text);
  assert.equal(item.reviewer,"QA-test");
  assert.deepEqual(Object.keys(item.cases),["K047-03"]);
  assert.equal(item.cases["K047-03"].leader_movement,"unknown");
  assert.match(item.review_sheet_sha256,/^[a-f0-9]{64}$/);
  assert.ok(renderCalls.some(call=>call[0]==="fillRect"));
  console.log("8 clips, scrub controls, signal brackets, track disappearance, and JSON export passed");
}).catch(error=>{console.error(error);process.exitCode=1;});

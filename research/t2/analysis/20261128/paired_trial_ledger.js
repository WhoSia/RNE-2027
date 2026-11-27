// Node.js standard-library offline paired trial audit. No traffic control.
function auditTrial(manifest, records) {
  const fail = m => {throw Error(m)};
  const ints = (x, max=1000000) => Number.isInteger(x)&&x>=0&&x<=max;
  const allowed = ["fixed","candidate"];
  const validId = x => typeof x==="string"&&/^[A-Za-z0-9_-]{1,40}$/.test(x);
  if(!Array.isArray(manifest)||!manifest.length||!Array.isArray(records))fail("empty or invalid manifest");
  const blocks=new Map(), tapes=new Map(), sessions=new Map(), source=new Set();
  for(const b of manifest){
    if(!validId(b.id)||!validId(b.session)||!validId(b.tapeId)||!["calibration","evaluation"].includes(b.split)||!["synthetic","teacher_approved_tabletop"].includes(b.source)||!ints(b.initial)||!ints(b.budget)||!Array.isArray(b.arrivals)||b.arrivals.length!==3||!b.arrivals.every(v=>ints(v))||!Array.isArray(b.service)||b.service.length!==3||!b.service.every(v=>ints(v))||!Array.isArray(b.order)||b.order.length!==2||!allowed.every(v=>b.order.includes(v)))fail("invalid manifest block");
    if(blocks.has(b.id))fail("duplicate block");
    const signature=JSON.stringify([b.initial,b.arrivals,b.service]);
    for(const [map,key] of [[tapes,b.tapeId],[sessions,b.session]]){if(map.has(key)&&map.get(key)!==b.split)fail("split leakage");map.set(key,b.split)}
    // Identical aggregate schedules across splits are flagged conservatively.
    // Real movement/order cards and source hash are additional external checks.
    const sk="signature:"+signature;
    if(tapes.has(sk)&&tapes.get(sk)!==b.split)fail("duplicate aggregate tape across splits");tapes.set(sk,b.split);
    blocks.set(b.id,b);source.add(b.source);
  }
  if(source.size!==1)fail("mixed source kinds");
  const grouped=new Map();
  for(const r of records){
    const b=blocks.get(r.block);
    if(!b||!allowed.includes(r.arm)||!Number.isInteger(r.stage)||r.stage<1||r.stage>3||!["ok","missing","invalid","aborted"].includes(r.status))fail("invalid record");
    if(r.order!==b.order.indexOf(r.arm)+1)fail("order mismatch");
    const key=r.block+"/"+r.arm;
    if(!grouped.has(key))grouped.set(key,new Map());
    const g=grouped.get(key);
    if(g.has(r.stage))fail("duplicate stage");
    if(r.status==="ok"){
      if(!["start","arrival","exit","end","credit"].every(k=>ints(r[k])))fail("invalid count");
      if(r.arrival!==b.arrivals[r.stage-1]||r.exit>b.service[r.stage-1]||r.exit>r.start||r.end!==r.start+r.arrival-r.exit)fail("conservation or tape mismatch");
    }else if(["start","arrival","exit","end","credit"].some(k=>r[k]!==null))fail("failed row must not fabricate count");
    g.set(r.stage,r);
  }
  const results=[];
  for(const b of manifest){
    const arms={};
    for(const arm of allowed){
      const g=grouped.get(b.id+"/"+arm)||new Map();
      let prior=b.initial,complete=true,credit=0,cost=0,unobserved=0,failed=0;
      for(let i=1;i<=3;i++){
        const r=g.get(i);
        if(!r||r.status!=="ok"){complete=false;prior=null;if(!r)unobserved++;else failed++;continue}
        if(prior!==null&&r.start!==prior)fail("broken stock continuity");
        prior=r.end;credit+=r.credit;cost+=r.end;
        if(credit>b.budget)fail("credit budget exceeded");
      }
      arms[arm]={complete,cost:complete?cost:null,observedCreditLowerBound:credit,unobserved,failed};
    }
    results.push({id:b.id,split:b.split,session:b.session,arms,delta:arms.fixed.complete&&arms.candidate.complete?arms.candidate.cost-arms.fixed.cost:null});
  }
  const splits={};
  for(const split of ["calibration","evaluation"]){
    const z=results.filter(r=>r.split===split),c=z.filter(r=>r.delta!==null);
    splits[split]={planned:z.length,complete:c.length,incomplete:z.length-c.length,meanCompleteOnly:c.length?c.reduce((s,r)=>s+r.delta,0)/c.length:null,primaryGate:z.length>0&&c.length===z.length?"COMPLETE_LEDGER_ONLY":"HOLD_INCOMPLETE_OR_EMPTY",wins:c.filter(r=>r.delta<0).length,ties:c.filter(r=>r.delta===0).length,losses:c.filter(r=>r.delta>0).length};
  }
  return {sourceKind:[...source][0],sourceVerified:false,splits,results,warning:"Aggregate stock and credits only; not independent physical truth, movement feasibility, timestamp freshness or actual field calibration. Incomplete cases block primary gate."};
}
function tests(){
  const m=[{id:"B1",session:"S1",tapeId:"T1",split:"calibration",source:"synthetic",initial:2,budget:1,arrivals:[1,0,1],service:[1,1,1],order:["fixed","candidate"]},{id:"B2",session:"S2",tapeId:"T2",split:"evaluation",source:"synthetic",initial:3,budget:1,arrivals:[0,1,0],service:[1,1,1],order:["candidate","fixed"]}];
  const records=m.flatMap(b=>b.order.flatMap((arm,o)=>{let start=b.initial;return b.arrivals.map((arrival,i)=>{const exit=arm==="candidate"||i!==0?Math.min(start,1):0;const end=start+arrival-exit;const r={block:b.id,arm,order:o+1,stage:i+1,status:"ok",start,arrival,exit,end,credit:arm==="candidate"&&i===0?1:0};start=end;return r})}));
  let checks=[];
  function check(name,f){if(!f())throw Error(name);checks.push(name)}
  const clone=x=>JSON.parse(JSON.stringify(x));
  function rejects(name,mut){const a=clone(m),b=clone(records);mut(a,b);check(name,()=>{try{auditTrial(a,b);return false}catch(e){return true}})}
  const base=auditTrial(m,records);
  check("complete pairs",()=>base.results.every(r=>r.delta<0)&&base.splits.evaluation.complete===1);
  check("order invariant rows",()=>JSON.stringify(auditTrial(m,[...records].reverse()))===JSON.stringify(base));
  check("missing entire arm retained",()=>auditTrial(m,records.filter(r=>!(r.block==="B2"&&r.arm==="candidate"))).splits.evaluation.primaryGate==="HOLD_INCOMPLETE_OR_EMPTY");
  check("failed row retained",()=>{let b=clone(records);let r=b.find(r=>r.block==="B2"&&r.arm==="candidate");r.status="invalid";for(const k of ["start","arrival","exit","end","credit"])r[k]=null;return auditTrial(m,b).splits.evaluation.incomplete===1});
  rejects("duplicate stage",(a,b)=>b.push(b[0]));
  rejects("duplicate block",(a,b)=>a.push(a[0]));
  rejects("session leakage",(a,b)=>a[1].session=a[0].session);
  rejects("tape id leakage",(a,b)=>a[1].tapeId=a[0].tapeId);
  rejects("aggregate signature leakage",(a,b)=>Object.assign(a[1],{initial:a[0].initial,arrivals:a[0].arrivals,service:a[0].service}));
  rejects("mixed source",(a,b)=>a[1].source="teacher_approved_tabletop");
  rejects("wrong run order",(a,b)=>b[0].order=2);
  rejects("wrong arrival",(a,b)=>b[0].arrival++);
  rejects("nonconservation",(a,b)=>b[0].end++);
  rejects("stock discontinuity",(a,b)=>{b[1].start++;b[1].end++});
  rejects("over budget",(a,b)=>b[0].credit=2);
  rejects("exit above service",(a,b)=>{b[0].exit=2;b[0].end--});
  rejects("fabricated failed value",(a,b)=>b[0].status="missing");
  rejects("unknown block",(a,b)=>b[0].block="B99");
  rejects("invalid stage",(a,b)=>b[0].stage=0);
  return {status:"SYNTHETIC_TESTS_ONLY",checks,fixture:{manifest:m,records},output:base};
}
if(require.main===module){const fs=require('fs');console.log(JSON.stringify(process.argv[2]?auditTrial(JSON.parse(fs.readFileSync(process.argv[2],'utf8')),JSON.parse(fs.readFileSync(process.argv[3],'utf8'))):tests(),null,2))}
module.exports={auditTrial,tests};

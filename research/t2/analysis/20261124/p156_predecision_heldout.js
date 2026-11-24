// P156 fixed grouped held-out synthetic decision audit.
function run(){
 const assert=(x,m)=>{if(!x)throw Error(m)};
 const fresh=()=>({q:[],p:0,d:0,a:0,z:0,j:0});
 function tick(s,t,g,r,pri,P,D,sink,arr){
  const exit=+(s.d>0&&(t+sink)%4<2),space=D-s.d+(r?exit:0);
  const admit=s.q[0]==="L"&&s.p<P,S=s.q[0]==="S"&&g!=="L",L=s.p>0&&g!=="S";
  const m=space>0?(S&&L?pri:S?"S":L?"L":null):null;
  if(m==="S")s.q.shift();if(m==="L")s.p--;
  if(admit){assert(m!=="S","head");s.q.shift();s.p++}
  s.d+=+(m!==null)-exit;s.z+=exit;
  if(arr){s.q.push(arr);s.a++}
  const n=s.q.length+s.p+s.d;s.j+=n;
  assert(s.a-s.z===n&&s.p>=0&&s.p<=P&&s.d>=0&&s.d<=D,"stock");
 }
 const clone=s=>({...s,q:s.q.slice()}),gates={4:"BSBL",8:"BBSSBBLL"};
 const names=["context","total","counts","head","ordered"];
 const rows=[];let arms=0,scenarios=0;
 const clocks=[[0,1,3,5,8,9,12,15],[0,2,4,7,9,11,13,16]];
 for(let mask=0;mask<256;mask++)for(let clock=0;clock<2;clock++)for(const P of [1,2])for(const D of [1,2])for(const sink of [0,2]){
  const tape=Object.fromEntries(clocks[clock].map((t,i)=>[t,mask&(1<<i)?"L":"S"]));
  let pre=fresh();for(let t=0;t<8;t++)tick(pre,t,t%4<2?"S":"L",false,"S",P,D,sink,tape[t]);
  scenarios++;
  for(let pair=0;pair<4;pair++){
   const keys=[[],[pre.q.length+pre.p+pre.d],[pre.q.length,pre.p,pre.d],[pre.q.length,pre.p,pre.d,pre.q[0]||"-"],[pre.q.join(""),pre.p,pre.d]];
   for(const r of [false,true])for(const pri of ["S","L"]){
    let costs=[];for(const period of [4,8]){
     const s=clone(pre),o=period===4?pair:2*pair;
     for(let t=8;t<160;t++){tick(s,t,gates[period][(t+o)%period],r,pri,P,D,sink,tape[t]);if(s.z===8)break}
     assert(s.z===8&&s.a===8,"clearance");arms++;costs.push(s.j);
    }
    rows.push({mask,clock,context:[P,D,sink,pair],keys,delta:costs[0]-costs[1],test:mask%5===0});
   }
  }
 }
 const train=rows.filter(r=>!r.test),test=rows.filter(r=>r.test);
 const trainMasks=new Set(train.map(r=>r.mask));assert(test.every(r=>!trainMasks.has(r.mask)),"group leakage");
 const loss=(a,d)=>Math.max(0,a===4?d:-d);
 function assess(includeClock){
  const maps=names.map(()=>new Map());
  function key(r,i){return JSON.stringify([...r.context,...(includeClock?[r.clock]:[]),...r.keys[i]])}
  for(const r of train)for(let i=0;i<names.length;i++){
   const k=key(r,i);if(!maps[i].has(k))maps[i].set(k,{masks:new Set(),neg:0,pos:0,l4:0,l8:0});
   const s=maps[i].get(k);s.masks.add(r.mask);s.neg+=+(r.delta<0);s.pos+=+(r.delta>0);s.l4+=loss(4,r.delta);s.l8+=loss(8,r.delta);
  }
  const init=()=>({n:0,covered:0,strictHarm:0,coveredRegret:0,coveredWorst:0,allRegret:0,allWorst:0,fallbackHarm:0});
  const stats=names.map(name=>({name,all:init(),clock:[init(),init()]}));
  const baselines={context:0,always4:0,always8:0,contextWorst:0,contextHarm:0};
  for(const r of test){
   const b=maps[0].get(key(r,0));assert(b,"context support");
   const fallback=b.l4<=b.l8?4:8,bl=loss(fallback,r.delta);
   baselines.context+=bl;baselines.contextWorst=Math.max(baselines.contextWorst,bl);baselines.contextHarm+=+(bl>0);baselines.always4+=loss(4,r.delta);baselines.always8+=loss(8,r.delta);
   for(let i=0;i<names.length;i++){
    const s=maps[i].get(key(r,i)),action=s&&s.masks.size>=4&&((s.neg>0)!==(s.pos>0))?(s.neg>0?4:8):null;
    const l=loss(action??fallback,r.delta);
    for(const z of [stats[i].all,stats[i].clock[r.clock]]){
     z.n++;z.allRegret+=l;z.allWorst=Math.max(z.allWorst,l);
     if(action!==null){z.covered++;z.strictHarm+=+(l>0);z.coveredRegret+=l;z.coveredWorst=Math.max(z.coveredWorst,l)}
     else z.fallbackHarm+=+(l>0);
    }
   }
  }
  return {includeClock,baselines,stats};
 }
 return {status:"EXECUTED_JS_ISOLATE_PROSPECTIVE_SYNTHETIC",scenarios,arms,trainWorlds:train.length,testWorlds:test.length,trainMasks:trainMasks.size,testMasks:new Set(test.map(r=>r.mask)).size,primary:assess(false),clockFamilySensitivity:assess(true)};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};

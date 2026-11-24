// P151 independent finite integer movement queue; run: node p151_movement_queue.js
function experiment(){
 const assert=(v,m)=>{if(!v)throw Error(m)};
 function step(s,t,period,reuse,priority,P,D,arr){
  const before=s.q.length+s.p.length+s.d.length, head=s.q[0],ph=t%period<period/2?'S':'L', exit=s.d.length>0&&t%4<2?1:0;
  const pocket=head==='L'&&s.p.length<P, candidates=[];
  if(head==='S'&&ph==='S')candidates.push('S');
  if(s.p.length&&ph==='L')candidates.push('L');
  const move=s.d.length-(reuse?exit:0)<D?(candidates.includes(priority)?priority:candidates[0]):undefined;
  if(exit){s.d.shift();s.z++}
  if(move==='S')s.d.push(s.q.shift());
  if(move==='L')s.d.push(s.p.shift());
  if(pocket)s.p.push(s.q.shift());
  if(arr!==undefined){s.q.push(arr);s.a++}
  const outstanding=s.q.length+s.p.length+s.d.length;
  s.cost+=outstanding;
  assert(s.a===s.z+outstanding && outstanding===before+(arr!==undefined?1:0)-exit,'conservation');
  assert(s.p.length<=P&&s.d.length<=D,'capacity');
  assert(s.d.length>=0&&s.p.length>=0,'stocks');
  assert(!move||move===ph,'red gate');
 }
 const fresh=()=>({q:[],p:[],d:[],a:0,z:0,cost:0});
 const clone=s=>JSON.parse(JSON.stringify(s));
 const rows=[];let arms=0;
 for(let mask=0;mask<64;mask++)for(const interval of [1,2])for(const P of [1,2])for(const D of [1,2])for(const priority of ['S','L']){
  const labels=Array.from({length:6},(_,i)=>mask&(1<<i)?'L':'S');
  const arrivals=Object.fromEntries(labels.map((l,i)=>[interval*i,l]));
  let pre=fresh();for(let t=0;t<8;t++)step(pre,t,4,false,priority,P,D,arrivals[t]);
  let costs={};
  for(const reuse of [false,true])for(const period of [4,8]){
   let s=clone(pre);for(let t=8;t<120;t++)step(s,t,period,reuse,priority,P,D,arrivals[t]);
   assert(s.a===6&&s.z===6,'clearance');costs[`${+reuse}:${period}`]=s.cost;arms++;
  }
  rows.push({mask,interval,P,D,priority,pre,costs,future:Object.entries(arrivals).filter(([t])=>+t>=8)});
 }
 let decreased=0,tied=0,increased=0,reversal=0,tieCreated=0,tieResolved=0,unchanged=0,witness=null,dominanceWitness=null;
 const priorities=new Map();let priorityMismatches=0;
 for(const r of rows){
  for(const p of [4,8]){let d=r.costs[`1:${p}`]-r.costs[`0:${p}`];if(d<0)decreased++;else if(d===0)tied++;else{increased++;dominanceWitness??={...r,period:p,delta:d}}}
  let a=r.costs['0:4']-r.costs['0:8'],b=r.costs['1:4']-r.costs['1:8'];if(a*b<0){reversal++;witness??={...r,deltaOld:a,deltaReuse:b}}else if(a===0&&b!==0)tieResolved++;else if(a!==0&&b===0)tieCreated++;else unchanged++;
  let k=JSON.stringify([r.mask,r.interval,r.P,r.D]);if(priorities.has(k)){if(JSON.stringify(priorities.get(k))!==JSON.stringify(r.costs))priorityMismatches++;}else priorities.set(k,r.costs);
 }
 assert(priorityMismatches===0,'negative control');
 const worlds=rows.flatMap(r=>[0,1].map(rule=>({r,rule,delta:r.costs[`${rule}:4`]-r.costs[`${rule}:8`]})));
 function evaluate(name,features){
  const groups=new Map();for(const w of worlds){let key=JSON.stringify([w.r.P,w.r.D,w.r.interval,...features(w)]);if(!groups.has(key))groups.set(key,[]);groups.get(key).push(w.delta)}
  let conflictCells=0,conflictWorlds=0,sumWorst=0,maxWorst=0,totalRegret=0;
  for(const ds of groups.values()){const a=Math.max(0,...ds),b=Math.max(0,...ds.map(x=>-x)),v=Math.min(a,b);if(a>0&&b>0){conflictCells++;conflictWorlds+=ds.length}sumWorst+=v;maxWorst=Math.max(maxWorst,v);totalRegret+=ds.reduce((s,d)=>s+Math.max(0,a<=b?d:-d),0)}
  return {name,cells:groups.size,conflictCells,conflictWorlds,sumWorst,maxWorst,totalRegret,meanRegret:totalRegret/worlds.length};
 }
 const obs=[
 evaluate('context',()=>[]),
 evaluate('aggregate',({r})=>[r.pre.q.length+r.pre.p.length+r.pre.d.length]),
 evaluate('separate_counts',({r})=>[r.pre.q.length,r.pre.p.length,r.pre.d.length]),
 evaluate('ordered_fifo',({r})=>[r.pre.q,r.pre.p.length,r.pre.d.length]),
 evaluate('oracle',({r,rule})=>[r.pre.q,r.pre.p.length,r.pre.d.length,r.future,rule])
 ];
 for(let i=1;i<obs.length;i++){assert(obs[i].maxWorst<=obs[i-1].maxWorst,'nested max regret');assert(obs[i].conflictWorlds<=obs[i-1].conflictWorlds,'nested ambiguity')}
 assert(obs.at(-1).maxWorst===0,'oracle sufficient');
 return {status:"EXECUTED_JS_ISOLATE_NOT_FIELD",scenarioCells:rows.length,arms,worlds:worlds.length,clearanceFailures:0,negativeControlPairs:priorities.size,priorityMismatches,dominance:{decreased,tied,increased,witness:dominanceWitness},ranking:{reversal,tieCreated,tieResolved,unchanged,witness},observations:obs};
}
console.log(JSON.stringify(experiment(),null,2));

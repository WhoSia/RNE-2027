// MACRO02B preregistered abstract offline benchmark.
function run(){
 const check=(b,m)=>{if(!b)throw Error(m)};
 const policies=[3,4,5].flatMap(g=>[0,2,4,6].map(o=>({g,o})));
 const clocks=["dense","platoon","sparse"];
 const empty=()=>({q:[],p:0,r:0,aS:0,aL:0,zS:0,zL:0,S:0,L:0,denial:0,headBlock:0,emptyPocket:0});
 function step(s,t,g,o,P,R,v,reuse){
  const gs=t%8<g,x=+(s.r>0&&(t+o)%8<4);
  const h=s.q[0],admit=+(h==="L"&&s.p<P);
  const room=s.r<R||(reuse&&x);
  const ms=+(gs&&h==="S"&&room),ml=+(!gs&&s.p>0);
  s.denial+=+(gs&&h==="S"&&!room);
  s.headBlock+=+(gs&&h==="L"&&s.q.includes("S"));
  s.emptyPocket+=+(!gs&&s.p===0&&s.q.includes("L"));
  check(ms+ml<=1&&ms+admit<=1,"old eligibility");
  if(ms||admit)s.q.shift();s.p+=admit-ml;s.r+=ms-x;s.zS+=x;s.zL+=ml;
  if(v){s.q.push(v);s.aS+=+(v==="S");s.aL+=+(v==="L")}
  const nS=s.q.filter(v=>v==="S").length+s.r,nL=s.q.length+s.p+s.r-nS;
  check(s.aS-s.zS===nS&&s.aL-s.zL===nL&&s.p>=0&&s.p<=P&&s.r>=0&&s.r<=R,"conservation");
  s.S+=nS;s.L+=nL;
 }
 function permutation(seed){
  const a=Array.from({length:24},(_,i)=>i);let x=seed+1;
  for(let i=23;i>0;i--){x=(Math.imul(1664525,x)+1013904223)>>>0;let j=x%(i+1);[a[i],a[j]]=[a[j],a[i]]}return a;
 }
 const rows=[];const transfer={decrease:0,tie:0,increase:0,strictRankFlips:0,rankPairs:0,firstIncrease:null,firstFlip:null};
 for(let seed=0;seed<60;seed++)for(const left of [6,12,18])for(const clock of clocks)for(const P of [1,3])for(const R of [1,3]){
  const tape=Object.fromEntries(permutation(seed).map((v,i)=>[clock==="dense"?i:clock==="platoon"?8*Math.floor(i/4)+i%4:4*i,v<left?"L":"S"]));
  const pre=empty();for(let t=0;t<16;t++)step(pre,t,4,0,P,R,tape[t],false);
  const costs=[false,true].map(reuse=>policies.map(({g,o})=>{
   const s={...pre,q:pre.q.slice()};
   for(let t=16;t<240;t++){step(s,t,g,o,P,R,tape[t],reuse);if(s.zS+s.zL===24)break}
   check(s.zS+s.zL===24&&s.aS+s.aL===24,"clearance");
   return {J:s.S+s.L,S:s.S,L:s.L,denial:s.denial,headBlock:s.headBlock,emptyPocket:s.emptyPocket,throughput:24,terminal:0};
  }));
  const [old,reuse]=costs;
  for(let i=0;i<12;i++){let d=reuse[i].J-old[i].J;transfer[d<0?"decrease":d>0?"increase":"tie"]++;if(d>0&&!transfer.firstIncrease)transfer.firstIncrease={seed,left,clock,P,R,policy:policies[i],old:old[i].J,reuse:reuse[i].J}}
  for(let i=0;i<12;i++)for(let j=i+1;j<12;j++){transfer.rankPairs++;if((old[i].J-old[j].J)*(reuse[i].J-reuse[j].J)<0){transfer.strictRankFlips++;if(!transfer.firstFlip)transfer.firstFlip={seed,left,clock,P,R,policies:[policies[i],policies[j]],old:[old[i].J,old[j].J],reuse:[reuse[i].J,reuse[j].J]}}}
  const frac=pre.aS/(pre.aS+pre.aL);
  const demand=policies.findIndex(p=>p.g===(frac>=.75?5:frac<=.25?3:4)&&p.o===0);
  rows.push({seed,left,clock,P,R,counts:[pre.q.length,pre.p,pre.r],head:pre.q[0]||"-",demand,costs:old,best:Math.min(...old.map(c=>c.J))});
 }
 const train=rows.filter(r=>r.seed%5!==0),test=rows.filter(r=>r.seed%5===0);
 const keys=[r=>`${r.P}:${r.R}`,r=>`${r.P}:${r.R}:${r.counts.join(":")}`,r=>`${r.P}:${r.R}:${r.counts.join(":")}:${r.head}`];
 const maps=keys.map(()=>new Map());
 for(const r of train)keys.forEach((key,i)=>{let k=key(r);if(!maps[i].has(k))maps[i].set(k,{sums:Array(12).fill(0),max:Array(12).fill(0),local:Array(12).fill(0),seeds:new Set()});let z=maps[i].get(k);z.seeds.add(r.seed);r.costs.forEach((c,j)=>{z.sums[j]+=c.J;z.max[j]=Math.max(z.max[j],c.J-r.best);z.local[j]+=c.denial})});
 const argmin=a=>a.indexOf(Math.min(...a));
 const selections=Object.fromEntries([...maps[0]].map(([k,v])=>[k,{mean:argmin(v.sums),minimax:argmin(v.max),local:argmin(v.local)}]));
 const names=["fixed","demand","mean","minimax","local","counts","head","oracle"];
 const fresh=()=>({n:0,J:0,S:0,L:0,denial:0,headBlock:0,emptyPocket:0,regret:0,worst:0,miss:0,throughput:0,terminal:0});
 const groups=Object.fromEntries(["all",...clocks].map(k=>[k,{stats:Object.fromEntries(names.map(n=>[n,fresh()])),coverage:{counts:0,head:0},paired:{counts:[0,0,0],head:[0,0,0]},localConflict:0,worldsWithDenial:0,armsWithDenial:0}]));
 for(const r of test){
  const b=selections[keys[0](r)],cells=[1,2].map(i=>maps[i].get(keys[i](r))),ok=cells.map(x=>!!x&&x.seeds.size>=4),acts=cells.map((x,i)=>ok[i]?argmin(x.sums):b.mean);
  const ids=[4,r.demand,b.mean,b.minimax,b.local,...acts,argmin(r.costs.map(c=>c.J))];
  const minDen=Math.min(...r.costs.map(c=>c.denial)),conflict=r.costs.filter(c=>c.denial===minDen).every(c=>c.J>r.best);
  for(const g of [groups.all,groups[r.clock]]){
   g.localConflict+=+conflict;g.worldsWithDenial+=+r.costs.some(c=>c.denial>0);g.armsWithDenial+=r.costs.filter(c=>c.denial>0).length;
   ["counts","head"].forEach((n,i)=>{g.coverage[n]+=+ok[i];g.paired[n][Math.sign(r.costs[acts[i]].J-r.costs[b.mean].J)+1]++});
   names.forEach((name,i)=>{const c=r.costs[ids[i]],s=g.stats[name],d=c.J-r.best;s.n++;for(const k of ["J","S","L","denial","headBlock","emptyPocket","throughput","terminal"])s[k]+=c[k];s.regret+=d;s.worst=Math.max(s.worst,d);s.miss+=+(d>0)});
  }
 }
 check(rows.length===2160&&train.length===1728&&test.length===432,"group denominator");
 return {status:"EXECUTED_JS_ISOLATE_SYNTHETIC_NOT_FIELD",worlds:2160,staticArms:25920,reuseArms:25920,train:1728,test:432,policies,selections,groups,transfer};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};

// MACRO02A fixed offline abstract corridor benchmark.
function run(){
 const assert=(x,m)=>{if(!x)throw Error(m)};
 const clocks=[[0,1,3,5,8,9,12,15],[0,2,4,7,9,11,13,16]];
 const policies=[3,4,5].flatMap(g=>[0,2,4,6].map(o=>({g,o})));
 const fresh=()=>({q:[],p:0,r:0,aS:0,aL:0,zS:0,zL:0,jS:0,jL:0,denial:0});
 const clone=s=>({...s,q:[...s.q]});
 function tick(s,t,g,o,P,R,v){
  const green=t%8<g,down=(t+o)%8<4;
  const x=+(s.r>0&&down),admit=+(s.q[0]==="L"&&s.p<P);
  const ms=+(green&&s.q[0]==="S"&&s.r<R),ml=+(!green&&s.p>0);
  s.denial+=+(green&&s.q[0]==="S"&&s.r===R);
  assert(ms+ml<=1&&ms+admit<=1,"transfer");
  if(ms||admit)s.q.shift();s.p+=admit-ml;s.r+=ms-x;s.zS+=x;s.zL+=ml;
  if(v){s.q.push(v);if(v==="S")s.aS++;else s.aL++}
  const nS=s.q.filter(v=>v==="S").length+s.r,nL=s.q.length+s.p+s.r-nS;
  assert(s.aS-s.zS===nS&&s.aL-s.zL===nL&&s.p>=0&&s.p<=P&&s.r>=0&&s.r<=R,"conservation");
  s.jS+=nS;s.jL+=nL;
 }
 const rows=[];
 for(let mask=0;mask<256;mask++)for(let clock=0;clock<2;clock++)for(const P of [1,2])for(const R of [2,4]){
  const tape=Object.fromEntries(clocks[clock].map((t,i)=>[t,mask&(1<<i)?"L":"S"]));
  const pre=fresh();for(let t=0;t<8;t++)tick(pre,t,4,0,P,R,tape[t]);
  const costs=policies.map(({g,o})=>{const s=clone(pre);for(let t=8;t<160;t++){tick(s,t,g,o,P,R,tape[t]);if(s.zS+s.zL===8)break}assert(s.aS+s.aL===8&&s.zS+s.zL===8,"clearance");return {J:s.jS+s.jL,S:s.jS,L:s.jL,denial:s.denial,terminal:0,throughput:8}});
  const best=Math.min(...costs.map(c=>c.J));const share=pre.aS/(pre.aS+pre.aL);
  const demand=policies.findIndex(p=>p.g===(share>=.75?5:share<=.25?3:4)&&p.o===0);
  rows.push({mask,clock,P,R,obs:[pre.q.length,pre.p,pre.r,pre.q[0]||"-"],demand,costs,best});
 }
 const train=rows.filter(r=>r.mask%5!==0),test=rows.filter(r=>r.mask%5===0);
 const group=r=>`${r.P}:${r.R}`,key=r=>`${group(r)}:${r.obs.join(":")}`;
 const maps=new Map(),fixed=new Map();
 function init(){return {sums:Array(12).fill(0),worst:Array(12).fill(0),masks:new Set()}}
 function add(m,k,r){if(!m.has(k))m.set(k,init());const x=m.get(k);x.masks.add(r.mask);r.costs.forEach((c,i)=>{x.sums[i]+=c.J-r.best;x.worst[i]=Math.max(x.worst[i],c.J-r.best)})}
 for(const r of train){add(fixed,group(r),r);add(maps,key(r),r)}
 const argmin=a=>a.indexOf(Math.min(...a));
 const selections=Object.fromEntries([...fixed].map(([k,v])=>[k,{mean:argmin(v.sums),minimax:argmin(v.worst)}]));
 const names=["fixed","demand","train_mean","train_minimax","observed","oracle"];
 const stats=Object.fromEntries(names.map(n=>[n,{n:0,J:0,S:0,L:0,regret:0,worst:0,strictMiss:0,denial:0,terminal:0,throughput:0}]));
 let covered=0;const paired={better:0,tie:0,worse:0};let localConflict=0;
 for(const r of test){const b=selections[group(r)],m=maps.get(key(r)),obs=m&&m.masks.size>=4?argmin(m.sums):b.mean;covered+=+(m&&m.masks.size>=4);
 const idx=[policies.findIndex(p=>p.g===4&&p.o===0),r.demand,b.mean,b.minimax,obs,argmin(r.costs.map(c=>c.J))];
 const diff=r.costs[obs].J-r.costs[b.mean].J;paired[diff<0?"better":diff>0?"worse":"tie"]++;
 const minDen=Math.min(...r.costs.map(c=>c.denial));if(r.costs.filter(c=>c.denial===minDen).every(c=>c.J>r.best))localConflict++;
 names.forEach((n,i)=>{const c=r.costs[idx[i]],s=stats[n],d=c.J-r.best;s.n++;for(const k of ["J","S","L","denial","terminal","throughput"])s[k]+=c[k];s.regret+=d;s.worst=Math.max(s.worst,d);s.strictMiss+=+(d>0)});
 }
 assert(train.length===1632&&test.length===416,"split");
 return {status:"EXECUTED_JS_ISOLATE_SYNTHETIC_NOT_FIELD",worlds:rows.length,arms:rows.length*12,train:train.length,test:test.length,policies,selections,stats,covered,paired,localConflict};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};

// Synthetic offline observation history benchmark.
function run(){
 const check=(b,m)=>{if(!b)throw Error(m)},known=["dense","platoon","sparse"],shift=["burst","irregular","blocks6"],pol=[3,4,5].flatMap(g=>[0,2,4,6].map(o=>[g,o]));
 const names=["geometry","presence","counts","past_total","past_movement","time_bins","movement_bins","ordered_history"];
 function tape(seed,left,clock){let x=seed+1,a=Array.from({length:24},(_,i)=>i);for(let i=23;i>0;i--){x=(Math.imul(1664525,x)+1013904223)>>>0;let j=x%(i+1);[a[i],a[j]]=[a[j],a[i]]}let ar=Array(240).fill(""),t=0;x=seed+9001;for(let i=0;i<24;i++){if(clock==="dense")t=i;else if(clock==="platoon")t=8*Math.floor(i/4)+i%4;else if(clock==="sparse")t=4*i;else if(clock==="burst")t=24*Math.floor(i/8)+i%8;else if(clock==="blocks6")t=18*Math.floor(i/6)+i%6;else if(i){x=(Math.imul(1664525,x)+1013904223)>>>0;t+=1+x%6}ar[t]=a[i]<left?"L":"S"}return ar}
 function tick(s,t,g,o,P,R,v){let gs=t%8<g,ds=(t+o)%8<4,x=+(gs&&s.q[0]==="S"&&s.r<R),a=+(s.q[0]==="L"&&s.p<P),y=+(!gs&&s.p>0),z=+(ds&&s.r>0);if(x||a)s.q.shift();s.p+=a-y;s.r+=x-z;s.Y+=y;s.Z+=z;if(v){s.q.push(v);s.A++}let stock=s.q.length+s.p+s.r;check(stock+s.Y+s.Z===s.A&&s.p>=0&&s.p<=P&&s.r>=0&&s.r<=R,"conservation");s.J+=stock}
 function features(P,R,s,prefix){check(prefix.length===16,"prefix");let total=[0,0,0,0],L=[0,0,0,0];prefix.forEach((v,i)=>{total[i>>2]+=+(!!v);L[i>>2]+=+(v==="L")});let key=`${P}:${R}`,ks=[key];key+=`|${+(s.q.length>0)+2*(s.p>0)+4*(s.r>0)}`;ks.push(key);key+=`|${s.q.length}:${s.p}:${s.r}`;ks.push(key);key+=`|${total.reduce((a,b)=>a+b,0)}`;ks.push(key);key+=`|${L.reduce((a,b)=>a+b,0)}`;ks.push(key);key+=`|${total.join(",")}`;ks.push(key);key+=`|${L.join(",")}`;ks.push(key);ks.push(key+`|${s.q.join("")}`);return ks}
 let arms=0;
 function row(seed,left,clock,P,R){let ar=tape(seed,left,clock),pre={q:[],p:0,r:0,A:0,Y:0,Z:0,J:0};for(let t=0;t<16;t++)tick(pre,t,4,0,P,R,ar[t]);let keys=features(P,R,pre,ar.slice(0,16));let c=pol.map(([g,o])=>{let s={...pre,q:pre.q.slice()};for(let t=16;t<240;t++)tick(s,t,g,o,P,R,ar[t]);check(s.A===24&&s.Y+s.Z===24,"clearance");arms++;return s.J});return {seed,clock,keys,c}}
 function loop(seeds,clocks,fn){for(let seed of seeds)for(let left of [6,12,18])for(let clock of clocks)for(let P of [1,3])for(let R of [1,3])fn(row(seed,left,clock,P,R))}
 const maps=names.map(()=>new Map()),train=Array.from({length:60},(_,i)=>i).filter(i=>i%5),test=Array.from({length:20},(_,i)=>340+i);
 loop(train,known,r=>r.keys.forEach((k,i)=>{let v=maps[i].get(k);if(!v){v={seeds:new Set(),sum:Array(12).fill(0)};maps[i].set(k,v)}v.seeds.add(r.seed);r.c.forEach((c,j)=>v.sum[j]+=c)}));
 const pick=a=>{let k=0;for(let i=1;i<a.length;i++)if(a[i]<a[k])k=i;return k};
 const all=[];loop(test,[...known,...shift],r=>all.push(r));
 function evaluate(rows){
  const result={n:rows.length,oracle:rows.reduce((s,r)=>s+Math.min(...r.c),0),levels:{}};
  const base=rows.map(r=>r.c[pick(maps[0].get(r.keys[0]).sum)]);
  let prev=Infinity;
  for(let i=0;i<names.length;i++){
   let a={J:0,regret:0,worst:0,supported:0,changed:0,better:0,tie:0,worse:0,maxHarm:0,fallback:Array(names.length).fill(0),groups:0,singletons:0,floor:0,excess:0},groups=new Map();
   rows.forEach((r,j)=>{let k=i;while(k>=0){let v=maps[k].get(r.keys[k]);if(v&&v.seeds.size>=4)break;k--}check(k>=0,"fallback");let act=pick(maps[k].get(r.keys[k]).sum),b=pick(maps[0].get(r.keys[0]).sum),c=r.c[act],d=c-Math.min(...r.c),e=c-base[j];a.J+=c;a.regret+=d;a.worst=Math.max(a.worst,d);a.supported+=+(k===i);a.changed+=+(act!==b);a.fallback[k]++;a[e<0?"better":e>0?"worse":"tie"]++;a.maxHarm=Math.max(a.maxHarm,e);let key=r.keys[i],v=groups.get(key);if(!v){v={sum:Array(12).fill(0),best:0,n:0};groups.set(key,v)}v.n++;v.best+=Math.min(...r.c);r.c.forEach((x,j)=>v.sum[j]+=x)});
   a.groups=groups.size;for(let v of groups.values()){a.singletons+=+(v.n===1);a.floor+=Math.min(...v.sum)-v.best}
   a.excess=a.regret-a.floor;check(a.floor<=prev&&a.excess>=0,"nested decomposition");prev=a.floor;result.levels[names[i]]=a;
  }return result;
 }
 check(arms===38016,"denom");return {status:"EXECUTED_ABSTRACT_OFFLINE",arms,trainingCells:maps.map(m=>({total:m.size,supported:[...m.values()].filter(x=>x.seeds.size>=4).length})),known:evaluate(all.filter(r=>known.includes(r.clock))),shifted:evaluate(all.filter(r=>shift.includes(r.clock))),pooled:evaluate(all)};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};

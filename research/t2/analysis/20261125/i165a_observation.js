// I165A synthetic offline decision information audit.
function run(){
 const check=(x,m)=>{if(!x)throw Error(m)},pol=[3,4,5].flatMap(g=>[0,2,4,6].map(o=>[g,o])),known=["dense","platoon","sparse"],shift=["burst","irregular"],names=["0","1","2","3","4","5","6","7","counts"];
 function tape(seed,left,clock){let x=seed+1,a=Array.from({length:24},(_,i)=>i);for(let i=23;i>0;i--){x=(Math.imul(1664525,x)+1013904223)>>>0;let j=x%(i+1);[a[i],a[j]]=[a[j],a[i]]}let ar=Array(240).fill(""),t=0;x=seed+9001;for(let i=0;i<24;i++){if(clock==="dense")t=i;else if(clock==="platoon")t=8*Math.floor(i/4)+i%4;else if(clock==="sparse")t=4*i;else if(clock==="burst")t=24*Math.floor(i/8)+i%8;else if(i){x=(Math.imul(1664525,x)+1013904223)>>>0;t+=1+x%6}ar[t]=a[i]<left?"L":"S"}return ar}
 function tick(s,t,g,o,P,R,v){let gs=t%8<g,ds=(t+o)%8<4,x=+(gs&&s.q[0]==="S"&&s.r<R),a=+(s.q[0]==="L"&&s.p<P),y=+(!gs&&s.p>0),z=+(ds&&s.r>0);if(x||a)s.q.shift();s.p+=a-y;s.r+=x-z;s.Y+=y;s.Z+=z;if(v){s.q.push(v);s.A++}let stock=s.q.length+s.p+s.r;check(stock+s.Y+s.Z===s.A&&s.p>=0&&s.p<=P&&s.r>=0&&s.r<=R,"conservation");s.J+=stock}
 let arms=0;
 function row(seed,left,clock,P,R){let ar=tape(seed,left,clock),pre={q:[],p:0,r:0,A:0,Y:0,Z:0,J:0};for(let t=0;t<16;t++)tick(pre,t,4,0,P,R,ar[t]);let bits=+(pre.q.length>0)+2*(pre.p>0)+4*(pre.r>0),keys=names.map(n=>n==="counts"?`${P}:${R}:${pre.q.length}:${pre.p}:${pre.r}`:`${P}:${R}:${bits&Number(n)}`);let costs=pol.map(([g,o])=>{let s={...pre,q:pre.q.slice()};for(let t=16;t<240;t++)tick(s,t,g,o,P,R,ar[t]);check(s.A===24&&s.Y+s.Z===24,"clearance");arms++;return s.J});return {seed,clock,keys,costs}}
 const maps=names.map(()=>new Map()),trainSeeds=Array.from({length:60},(_,i)=>i).filter(i=>i%5),valSeeds=Array.from({length:60},(_,i)=>i).filter(i=>i%5===0),testSeeds=Array.from({length:20},(_,i)=>260+i);
 function loop(seeds,clocks,fn){for(let seed of seeds)for(let left of [6,12,18])for(let clock of clocks)for(let P of [1,3])for(let R of [1,3])fn(row(seed,left,clock,P,R))}
 loop(trainSeeds,known,r=>r.keys.forEach((k,i)=>{let v=maps[i].get(k);if(!v){v={seeds:new Set(),sum:Array(12).fill(0)};maps[i].set(k,v)}v.seeds.add(r.seed);r.costs.forEach((c,j)=>v.sum[j]+=c)}));
 const pick=a=>{let j=0;for(let i=1;i<a.length;i++)if(a[i]<a[j])j=i;return j};
 const blank=()=>({n:0,J:0,regret:0,worst:0,support:0,better:0,tie:0,worse:0});
 function evaluate(seeds,clocks){let all=Object.fromEntries(names.map(n=>[n,blank()])),byClock=Object.fromEntries(clocks.map(c=>[c,Object.fromEntries(names.map(n=>[n,blank()]))])),bySeed={},oracle=0;
  loop(seeds,clocks,r=>{let base=maps[0].get(r.keys[0]);check(base.seeds.size>=4,"base support");let ref=r.costs[pick(base.sum)],best=Math.min(...r.costs);oracle+=best;let ss=bySeed[r.seed]??(bySeed[r.seed]=Object.fromEntries(names.map(n=>[n,0])));
  r.keys.forEach((k,i)=>{let v=maps[i].get(k),supported=!!v&&v.seeds.size>=4,J=r.costs[pick((supported?v:base).sum)],d=J-best;ss[names[i]]+=J;for(let s of [all[names[i]],byClock[r.clock][names[i]]]){s.n++;s.J+=J;s.regret+=d;s.worst=Math.max(s.worst,d);s.support+=+supported;s[J<ref?"better":J>ref?"worse":"tie"]++}})});return {all,byClock,bySeed,oracle}}
 const val=evaluate(valSeeds,known),qual=(a,base,full)=>base.J>full.J&&(base.J-a.J)>=.8*(base.J-full.J)&&a.worst<=base.worst&&a.support>=.95*a.n,pop=n=>((n&1)>0)+((n&2)>0)+((n&4)>0);
 let eligible=names.slice(1,8).filter(n=>qual(val.all[n],val.all["0"],val.all["7"])).sort((a,b)=>pop(+a)-pop(+b)||val.all[a].J-val.all[b].J||+a-+b),selected=eligible[0]??"0";
 const same=evaluate(testSeeds,known),shifted=evaluate(testSeeds,shift);
 check(arms===40320,"arms");
 return {status:"EXECUTED_JS_SYNTHETIC_OFFLINE",arms,selected,eligible,criteria:{same:qual(same.all[selected],same.all["0"],same.all["7"]),shift:qual(shifted.all[selected],shifted.all["0"],shifted.all["7"])},trainCells:maps.map(m=>({total:m.size,supported:[...m.values()].filter(v=>v.seeds.size>=4).length})),validation:val,same,shifted};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};

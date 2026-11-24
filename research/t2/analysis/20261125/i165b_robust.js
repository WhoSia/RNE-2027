// I165B offline synthetic risk audit.
function run(){
 const check=(b,m)=>{if(!b)throw Error(m)},known=["dense","platoon","sparse"],shift=["burst","irregular","blocks6"],pol=[3,4,5].flatMap(g=>[0,2,4,6].map(o=>[g,o]));
 function tape(seed,left,clock){let x=seed+1,a=Array.from({length:24},(_,i)=>i);for(let i=23;i>0;i--){x=(Math.imul(1664525,x)+1013904223)>>>0;let j=x%(i+1);[a[i],a[j]]=[a[j],a[i]]}let ar=Array(240).fill(""),t=0;x=seed+9001;for(let i=0;i<24;i++){if(clock==="dense")t=i;else if(clock==="platoon")t=8*Math.floor(i/4)+i%4;else if(clock==="sparse")t=4*i;else if(clock==="burst")t=24*Math.floor(i/8)+i%8;else if(clock==="blocks6")t=18*Math.floor(i/6)+i%6;else if(i){x=(Math.imul(1664525,x)+1013904223)>>>0;t+=1+x%6}ar[t]=a[i]<left?"L":"S"}return ar}
 function tick(s,t,g,o,P,R,v){let gs=t%8<g,ds=(t+o)%8<4,x=+(gs&&s.q[0]==="S"&&s.r<R),a=+(s.q[0]==="L"&&s.p<P),y=+(!gs&&s.p>0),z=+(ds&&s.r>0);if(x||a)s.q.shift();s.p+=a-y;s.r+=x-z;s.Y+=y;s.Z+=z;if(v){s.q.push(v);s.A++}let stock=s.q.length+s.p+s.r;check(stock+s.Y+s.Z===s.A&&s.p>=0&&s.p<=P&&s.r>=0&&s.r<=R,"conservation");s.J+=stock}
 let arms=0;
 function row(seed,left,clock,P,R){let ar=tape(seed,left,clock),pre={q:[],p:0,r:0,A:0,Y:0,Z:0,J:0};for(let t=0;t<16;t++)tick(pre,t,4,0,P,R,ar[t]);let bits=+(pre.q.length>0)+2*(pre.p>0)+4*(pre.r>0),keys=[`${P}:${R}`,`${P}:${R}:${bits}`,`${P}:${R}:${pre.q.length}:${pre.p}:${pre.r}`];let c=pol.map(([g,o])=>{let s={...pre,q:pre.q.slice()};for(let t=16;t<240;t++)tick(s,t,g,o,P,R,ar[t]);check(s.A===24&&s.Y+s.Z===24,"clearance");arms++;return s.J});return {keys,c,seed,clock}}
 const maps=[new Map(),new Map(),new Map()];
 const train=Array.from({length:60},(_,i)=>i).filter(i=>i%5),test=Array.from({length:20},(_,i)=>280+i);
 function loop(seeds,clocks,fn){for(let seed of seeds)for(let left of [6,12,18])for(let clock of clocks)for(let P of [1,3])for(let R of [1,3])fn(row(seed,left,clock,P,R))}
 loop(train,known,r=>{let best=Math.min(...r.c);r.keys.forEach((k,i)=>{let v=maps[i].get(k);if(!v){v={seeds:new Set(),sum:Array(12).fill(0),max:Array(12).fill(0)};maps[i].set(k,v)}v.seeds.add(r.seed);r.c.forEach((c,j)=>{v.sum[j]+=c;v.max[j]=Math.max(v.max[j],c-best)})})});
 const pick=(v,mode,base=0)=>{let inds=Array.from({length:12},(_,i)=>i);if(mode==="guard")inds=inds.filter(i=>v.max[i]<=v.max[base]);inds.sort((a,b)=>(mode==="minimax"?v.max[a]-v.max[b]:0)||v.sum[a]-v.sum[b]||a-b);return inds[0]};
 const names=["geometry_mean","geometry_minimax","presence_mean","presence_minimax","presence_guard","counts_mean","counts_minimax","counts_guard"];
 const fresh=()=>({n:0,J:0,regret:0,worst:0,support:0,better:0,tie:0,worse:0});
 function evalGroup(clocks){let stats=Object.fromEntries(names.map(n=>[n,fresh()])),byClock=Object.fromEntries(clocks.map(c=>[c,Object.fromEntries(names.map(n=>[n,fresh()]))])),seeds={},oracle=0;
 loop(test,clocks,r=>{let g=maps[0].get(r.keys[0]),gm=pick(g,"mean"),gw=pick(g,"minimax"),best=Math.min(...r.c),ref=r.c[gm],ss=seeds[r.seed]??(seeds[r.seed]=Object.fromEntries(names.map(n=>[n,0])));oracle+=best;let choices=[[gm,true],[gw,true]];for(let i=1;i<=2;i++){let v=maps[i].get(r.keys[i]),ok=!!v&&v.seeds.size>=4;choices.push([ok?pick(v,"mean"):gm,ok],[ok?pick(v,"minimax"):gw,ok],[ok?pick(v,"guard",gm):gm,ok]);}
 choices.forEach(([a,ok],i)=>{let n=names[i],c=r.c[a],d=c-best;ss[n]+=c;for(let s of [stats[n],byClock[r.clock][n]]){s.n++;s.J+=c;s.regret+=d;s.worst=Math.max(s.worst,d);s.support+=+ok;s[c<ref?"better":c>ref?"worse":"tie"]++}})});return {stats,byClock,seeds,oracle}}
 let same=evalGroup(known),shifted=evalGroup(shift);check(arms===38016,"arms");return {status:"EXECUTED_JS_SYNTHETIC_OFFLINE",arms,same,shifted};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};

// Offline abstract scenario risk selection.
function run(){
 const check=(b,m)=>{if(!b)throw Error(m)},eps=1e-8,clocks=["dense","platoon","sparse"],pol=[3,4,5].flatMap(g=>[0,2,4,6].map(o=>[g,o]));
 function tape(seed,left,clock){let x=seed+1,a=Array.from({length:24},(_,i)=>i);for(let i=23;i>0;i--){x=(Math.imul(1664525,x)+1013904223)>>>0;let j=x%(i+1);[a[i],a[j]]=[a[j],a[i]]}let ar=Array(240).fill("");a.forEach((v,i)=>ar[clock==="dense"?i:clock==="platoon"?8*Math.floor(i/4)+i%4:4*i]=v<left?"L":"S");return ar}
 function prefix(ar){let S=0,L=0;for(let t=0;t<16;t++){S+=ar[t]==="S";L+=ar[t]==="L"}return [S,L]}
 function tick(s,t,g,o,P,R,v){let gs=t%8<g,down=(t+o)%8<4,x=+(gs&&s.q[0]==="S"&&s.r<R),a=+(s.q[0]==="L"&&s.p<P),y=+(!gs&&s.p>0),z=+(down&&s.r>0);if(x||a)s.q.shift();s.p+=a-y;s.r+=x-z;s.Y+=y;s.Z+=z;if(v){s.A++;s.q.push(v)}let stock=s.q.length+s.p+s.r;check(s.A===stock+s.Y+s.Z&&s.p>=0&&s.p<=P&&s.r>=0&&s.r<=R,"micro");s.J+=stock}
 function micro(pre,ar,P,R,g,o){let s={...pre,q:pre.q.slice()};for(let t=16;t<240;t++)tick(s,t,g,o,P,R,ar[t]);check(s.q.length+s.p+s.r===0,"micro clearance");return s.J}
 function mixed(pre,ar,P,R,g,o){let S=pre.q.filter(x=>x==="S").length,L=pre.q.length-S,p=pre.p,r=pre.r,A=pre.A,Y=pre.Y,Z=pre.Z,J=pre.J;for(let t=16;t<240;t++){let gs=t%8<g,ds=(t+o)%8<4,total=S+L,fs=total?S/total:0,fl=total?L/total:0,x=gs?Math.min(S,fs,Math.max(0,R-r)):0,a=Math.min(L,fl,Math.max(0,P-p)),y=gs?0:Math.min(p,1),z=ds?Math.min(r,1):0;S-=x;L-=a;p+=a-y;r+=x-z;Y+=y;Z+=z;let v=ar[t];if(v){A++;S+=v==="S";L+=v==="L"}let stock=S+L+p+r;check(Math.abs(A-stock-Y-Z)<eps&&Math.min(S,L,p,r)>=-eps&&p<=P+eps&&r<=R+eps,"fluid");J+=stock}check(S+L+p+r<eps,"fluid clearance");return J}
 const lib=[];for(let seed=0;seed<60;seed++)if(seed%5)for(let left of [6,12,18])for(let c of clocks){let ar=tape(seed,left,c);lib.push({ar,prefix:prefix(ar)})}check(lib.length===432,"library");
 const pick=a=>{let k=0;for(let i=1;i<a.length;i++)if(a[i]<a[k]-eps)k=i;return k};
 function choose(mat){let b=Array.from({length:4},(_,j)=>Math.min(...mat.map(a=>a[j])));return [pick(mat.map(a=>a.reduce((s,x)=>s+x,0)/4)),pick(mat.map(a=>Math.max(...a.map((x,j)=>x-b[j]))))]}
 const names=["trained","micro_mean","micro_minimax","mixed_mean","mixed_minimax","oracle"];
 const fresh=()=>({n:0,J:0,regret:0,worst:0,miss:0,vsTrained:[0,0,0]});
 const groups=Object.fromEntries(["all",...clocks].map(k=>[k,{policies:Object.fromEntries(names.map(n=>[n,fresh()])),microRisk:[0,0,0],mixedRisk:[0,0,0]}]));let arms={truth:0,forecast:0},distance={},distinct={},seeds={};
 for(let seed=220;seed<240;seed++)for(let left of [6,12,18])for(let clock of clocks)for(let P of [1,3])for(let R of [1,3]){
  let ar=tape(seed,left,clock),pref=prefix(ar),pre={q:[],p:0,r:0,A:0,Y:0,Z:0,J:0};for(let t=0;t<16;t++)tick(pre,t,4,0,P,R,ar[t]);
  let dmin=Math.min(...lib.map(v=>Math.abs(v.prefix[0]-pref[0])+Math.abs(v.prefix[1]-pref[1]))),matches=lib.filter(v=>Math.abs(v.prefix[0]-pref[0])+Math.abs(v.prefix[1]-pref[1])===dmin);
  let scenarios=Array.from({length:4},(_,j)=>matches[Math.floor((j+.5)*matches.length/4)].ar),uniq=new Set(scenarios.map(a=>a.slice(16).map(v=>v||"-").join(""))).size;
  distance[dmin]=(distance[dmin]||0)+1;distinct[uniq]=(distinct[uniq]||0)+1;
  let truth=pol.map(([g,o])=>{arms.truth++;return micro(pre,ar,P,R,g,o)});
  let ma=[],fa=[];for(let [g,o] of pol){let mm=[],ff=[];for(let ar2 of scenarios){mm.push(micro(pre,ar2,P,R,g,o));ff.push(mixed(pre,ar2,P,R,g,o));arms.forecast+=2}ma.push(mm);fa.push(ff)}
  let [m0,m1]=choose(ma),[f0,f1]=choose(fa),best=Math.min(...truth),trained=truth[P===1?0:4];
  let costs=[trained,truth[m0],truth[m1],truth[f0],truth[f1],best],ss=seeds[seed]??(seeds[seed]=Object.fromEntries(names.map(n=>[n,0])));names.forEach((n,i)=>ss[n]+=costs[i]);
  for(let k of ["all",clock]){let z=groups[k];z.microRisk[Math.sign(costs[2]-costs[1])+1]++;z.mixedRisk[Math.sign(costs[4]-costs[3])+1]++;names.forEach((n,i)=>{let a=z.policies[n],J=costs[i],d=J-best;a.n++;a.J+=J;a.regret+=d;a.worst=Math.max(a.worst,d);a.miss+=d>0;a.vsTrained[Math.sign(J-trained)+1]++})}
 }
 check(arms.truth===8640&&arms.forecast===69120,"denom");return {status:"JS_ISOLATE_ABSTRACT_SYNTHETIC",arms,distance,distinct,groups,seeds};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};

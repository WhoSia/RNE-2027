// I166A: finite-cohort representation ambiguity diagnostic, abstract offline model.
function audit(rows){
 const names=["geometry","presence","counts","ordered"], result={}, eps=0;
 for(const [label,subset] of [["known",rows.filter(r=>["dense","platoon","sparse"].includes(r.clock))],["shifted",rows.filter(r=>!["dense","platoon","sparse"].includes(r.clock))],["pooled",rows]]){
  const stats={};let witness=null;
  for(let i=0;i<4;i++){
   let groups=new Map();for(const r of subset){let k=r.keys[i],v=groups.get(k);if(!v){v=[];groups.set(k,v)}v.push(r)}
   let a={worlds:subset.length,groups:groups.size,singletons:0,ambiguousGroups:0,ambiguousWorlds:0,regretLowerBound:0,maximumGroupRegret:0};
   for(const [k,g] of groups){let sums=Array(12).fill(0),oracle=0,inter=Array(12).fill(true);if(g.length===1)a.singletons++;for(const r of g){let best=Math.min(...r.c);oracle+=best;r.c.forEach((x,j)=>{sums[j]+=x;inter[j]=inter[j]&&x===best})}let loss=Math.min(...sums)-oracle;if(loss<0)throw Error("negative regret");a.regretLowerBound+=loss;a.maximumGroupRegret=Math.max(a.maximumGroupRegret,loss);if(!inter.some(Boolean)){a.ambiguousGroups++;a.ambiguousWorlds+=g.length;if(loss<=eps)throw Error("ambiguous zero bound")}
   if(i===2&&!witness&&g.length>1){outer:for(let u=0;u<g.length;u++)for(let v=u+1;v<g.length;v++){let x=g[u],y=g[v],mx=Math.min(...x.c),my=Math.min(...y.c);if(!x.c.some((c,j)=>c===mx&&y.c[j]===my)){witness={key:k,first:x,second:y,pairMinimumRegret:Math.min(...x.c.map((c,j)=>c+y.c[j]))-mx-my};break outer}}}
   }stats[names[i]]=a;if(i>0&&a.regretLowerBound>stats[names[i-1]].regretLowerBound)throw Error("nested violation");
  }result[label]={stats,witness}
 }return result;
}
function run(){
 const check=(b,m)=>{if(!b)throw Error(m)},known=["dense","platoon","sparse"],shift=["burst","irregular","blocks6"],pol=[3,4,5].flatMap(g=>[0,2,4,6].map(o=>[g,o]));
 function tape(seed,left,clock){let x=seed+1,a=Array.from({length:24},(_,i)=>i);for(let i=23;i>0;i--){x=(Math.imul(1664525,x)+1013904223)>>>0;let j=x%(i+1);[a[i],a[j]]=[a[j],a[i]]}let ar=Array(240).fill(""),t=0;x=seed+9001;for(let i=0;i<24;i++){if(clock==="dense")t=i;else if(clock==="platoon")t=8*Math.floor(i/4)+i%4;else if(clock==="sparse")t=4*i;else if(clock==="burst")t=24*Math.floor(i/8)+i%8;else if(clock==="blocks6")t=18*Math.floor(i/6)+i%6;else if(i){x=(Math.imul(1664525,x)+1013904223)>>>0;t+=1+x%6}ar[t]=a[i]<left?"L":"S"}return ar}
 function tick(s,t,g,o,P,R,v){let gs=t%8<g,ds=(t+o)%8<4,x=+(gs&&s.q[0]==="S"&&s.r<R),a=+(s.q[0]==="L"&&s.p<P),y=+(!gs&&s.p>0),z=+(ds&&s.r>0);if(x||a)s.q.shift();s.p+=a-y;s.r+=x-z;s.Y+=y;s.Z+=z;if(v){s.q.push(v);s.A++}let stock=s.q.length+s.p+s.r;check(stock+s.Y+s.Z===s.A&&s.p>=0&&s.p<=P&&s.r>=0&&s.r<=R,"conservation");s.J+=stock}
 let arms=0;
 function row(seed,left,clock,P,R){let ar=tape(seed,left,clock),pre={q:[],p:0,r:0,A:0,Y:0,Z:0,J:0};for(let t=0;t<16;t++)tick(pre,t,4,0,P,R,ar[t]);let bits=+(pre.q.length>0)+2*(pre.p>0)+4*(pre.r>0),keys=[`${P}:${R}`,`${P}:${R}:${bits}`,`${P}:${R}:${pre.q.length}:${pre.p}:${pre.r}`,`${P}:${R}:${pre.q.join("")}:${pre.p}:${pre.r}`];let c=pol.map(([g,o])=>{let s={...pre,q:pre.q.slice()};for(let t=16;t<240;t++)tick(s,t,g,o,P,R,ar[t]);check(s.A===24&&s.Y+s.Z===24,"clearance");arms++;return s.J});return {keys,c,seed,clock,left,P,R}}
 const rows=[];for(let seed=320;seed<340;seed++)for(let left of [6,12,18])for(let clock of [...known,...shift])for(let P of [1,3])for(let R of [1,3])rows.push(row(seed,left,clock,P,R));check(arms===17280,"denominator");return {status:"RETROSPECTIVE_FINITE_COHORT_BOUND_NOT_PREDICTOR",arms,results:audit(rows)};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};

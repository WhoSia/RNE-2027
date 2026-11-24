// Exact abstract event aggregation, shared-kernel parity.
function run(){
 const check=(x,m)=>{if(!x)throw Error(m)};
 function tape(N,seed,stride){let x=seed+1,a=Array.from({length:N},(_,i)=>i);for(let i=N-1;i>0;i--){x=(Math.imul(1664525,x)+1013904223)>>>0;let j=x%(i+1);[a[i],a[j]]=[a[j],a[i]]}return a.map((v,i)=>[i*stride,v<N/2?"S":"L"])}
 function simulate(N,ar,P,R,g,o,event){
  const horizon=16*N+32,wait=(predicate)=>Array.from({length:8},(_,phase)=>{for(let w=0;w<8;w++)if(predicate((phase+w)%8))return w;throw Error("gate")}),ws=wait(p=>p<g),wl=wait(p=>p>=g),wd=wait(p=>(p+o)%8<4);
  let q="",p=0,r=0,as=0,al=0,zs=0,zl=0,J=0,JS=0,JL=0,t=0,steps=0,skipped=0,trace=[];
  function integrate(k){let s=as-zs,l=al-zl;JS+=k*s;JL+=k*l;J+=k*(s+l)}
  while(t<horizon&&zs+zl<N){
   if(event){let at=ar[as+al]?.[0]??Infinity,when=Math.min(at,q[0]==="L"&&p<P?t:Infinity,q[0]==="S"&&r<R?t+ws[t%8]:Infinity,p>0?t+wl[t%8]:Infinity,r>0?t+wd[t%8]:Infinity,horizon);check(when>=t,"past event");let gap=when-t;integrate(gap);skipped+=gap;t=when;if(t===horizon)break}
   let gs=t%8<g,ds=(t+o)%8<4,x=+(gs&&q[0]==="S"&&r<R),a=+(q[0]==="L"&&p<P),y=+(!gs&&p>0),z=+(ds&&r>0);
   if(x||a)q=q.slice(1);p+=a-y;r+=x-z;zs+=z;zl+=y;
   let v=ar[as+al]?.[0]===t?ar[as+al][1]:"";if(v){q+=v;as+=+(v==="S");al+=+(v==="L")}
   check(as-zs===q.split("S").length-1+r&&al-zl===q.split("L").length-1+p&&p>=0&&p<=P&&r>=0&&r<=R,"stock");
   integrate(1);steps++;
   if(x||a||y||z||v)trace.push([t,q,p,r,as,al,zs,zl].join(":"));
   else check(!event,"spurious event");
   t++;
  }
  check(zs+zl===N&&as+al===N&&J===JS+JL&&steps+skipped===t,"clearance");return {J,JS,JL,t,steps,skipped,trace:trace.join("|")};
 }
 const fresh=()=>({arms:0,ticks:0,events:0,skipped:0,J:0});
 const bySize=Object.fromEntries([24,96,384].map(x=>[x,fresh()])),byStride=Object.fromEntries([1,4,12].map(x=>[x,fresh()])),all=fresh();
 for(let N of [24,96,384])for(let seed=240;seed<244;seed++)for(let stride of [1,4,12])for(let P of [1,3])for(let g of [3,4,5])for(let o of [0,2,4,6]){
  let ar=tape(N,seed,stride),a=simulate(N,ar,P,P,g,o,false),b=simulate(N,ar,P,P,g,o,true);
  for(let k of ["J","JS","JL","t","trace"])check(a[k]===b[k],`parity ${k}`);
  for(let s of [all,bySize[N],byStride[stride]]){s.arms++;s.ticks+=a.steps;s.events+=b.steps;s.skipped+=b.skipped;s.J+=a.J}
 }
 check(all.arms===864&&all.ticks===all.events+all.skipped,"denom");return {status:"EXECUTED_JS_ISOLATE_EXACT_SHARED_KERNEL_PARITY",all,bySize,byStride};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};

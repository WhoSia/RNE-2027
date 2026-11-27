/* node h08h_availability.js */
function h08h(){
 const A=[0,1],H=4,c=1/16,prices=[0,c/4,c],results=[],classes=[];
 for(const K of [[2,2],[3,2]])for(const L of [4,6])for(const schedule of [[1,2,3,4],[1],[1,3]]){
  const words=[""];for(let n=1;n<=L;n++)for(let i=0;i<2**n;i++)words.push(i.toString(2).padStart(n,"0"));
  const states=[],ids=new Map(),tr=new Map(),fullmemo=new Map();
  function id(q,w){let k=q.join(",")+","+w;if(!ids.has(k)){ids.set(k,states.length);states.push({q,w,n0:w.split("0").length-1,n1:w.split("1").length-1});}return ids.get(k);}
  const init=[];for(let s=0;s<=K[0];s++)for(let l=0;l<=K[1];l++)for(const w of words)init.push([id([s,l],w),1]);
  function step(i,a){let k=i*2+a;if(tr.has(k))return tr.get(k);let {q,w}=states[i],old=q[0]+q[1]+w.length;q=q.slice();let d=Math.min(q[a],2);q[a]-=d;for(let j=0;j<2&&w&&q[+w[0]]<K[+w[0]];j++){q[+w[0]]++;w=w.slice(1);}let r=q[0]+q[1]+w.length;if(r!==old-d||q.some((x,j)=>x<0||x>K[j]))throw Error("conservation");let z={r,next:A.map(a=>id(q.slice(),w+a))};tr.set(k,z);return z;}
  function fq(i,h,a){const z=step(i,a);return z.r+(h>1?(fv(z.next[0],h-1)+fv(z.next[1],h-1))/2:0);}
  function fv(i,h){const k=i+"|"+h;if(!fullmemo.has(k))fullmemo.set(k,Math.min(...A.map(a=>fq(i,h,a))));return fullmemo.get(k);}
  const mass=b=>b.reduce((s,p)=>s+p[1],0),key=b=>b.map(x=>x.join(":")).join(","),gcd=(a,b)=>b?gcd(b,a%b):a;
  function norm(d){let b=[...d].sort((a,b)=>a[0]-b[0]),g=b.reduce((z,p)=>gcd(z,p[1]),0);return b.map(([i,n])=>[i,n/g]);}
  function obs(i,m){let s=states[i];return m===0?[...s.q,s.n0,s.n1].join(","):m===1?s.w.slice(0,1):s.w;}
  function part(b,m){const d=new Map();for(let [i,n] of b){let k=obs(i,m);if(!d.has(k))d.set(k,new Map());d.get(k).set(i,n);}const p=[...d].map(([k,v])=>({k,b:norm(v),n:mass([...v])}));if(p.reduce((s,x)=>s+x.n,0)!==mass(b))throw Error("mass");return p;}
  function next(b,a){let d=new Map(),r=0;for(let [i,n] of b){let z=step(i,a);r+=n*z.r;for(let j of z.next)d.set(j,(d.get(j)||0)+n);}let n=mass(b);if(mass([...d])!==2*n)throw Error("transition mass");return {r:r/n,p:part([...d],0),n:2*n};}
  const add=(v,u,p)=>{for(let i=0;i<4;i++)v[i]+=p*u[i];},cost=v=>v[0]+v[1],avgQ=(b,h,a)=>b.reduce((s,[i,n])=>s+n*fq(i,h,a),0)/mass(b);
  const argmin=(xs,score)=>xs.reduce((best,x)=>score(x)<score(best)-1e-10?x:best,xs[0]);
  function surrogate(b,h,m){let n=mass(b),p=m===0?[{b,n}]:part(b,m);return prices[m]+p.reduce((s,z)=>s+z.n/n*Math.min(...A.map(a=>avgQ(z.b,h,a))),0);}
  function solve(policy){
   let sm=new Map(),am=new Map(),first=new Map();
   function sense(b,h){const k=h+"|"+key(b);if(sm.has(k))return sm.get(k);const q=states[b[0][0]].q,n=mass(b);let modes=[0,1,2];
    if(policy==="free"||!schedule.includes(H-h+1))modes=[0];
    else if(policy==="head"||policy==="full"){const m=policy==="head"?1:2;modes=[part(b,m).length>1?m:0];}
    else if(policy==="bothfull"&&!(q[0]===K[0]&&q[1]===K[1]))modes=[0];
    else if(policy==="equalrate"&&q[0]*K[1]!==q[1]*K[0])modes=[0];
    else if(policy==="qmdp"){const m=argmin(modes,x=>surrogate(b,h,x));if(m!==argmin(modes,x=>surrogate(b.map(([i,w])=>[i,w*3]),h,x)))throw Error("scale");modes=[m];}
    let best;
    for(let m of modes){let v=[0,prices[m],+(m===1),+(m===2)];for(const z of (m===0?[{b,n}]:part(b,m)))add(v,act(z.b,h),z.n/n);if(!best||cost(v)<cost(best.v)-1e-10)best={m,v};}
    sm.set(k,best.v);first.set(k,best.m);return best.v;
   }
   function act(b,h){let k=h+"|"+key(b);if(am.has(k))return am.get(k);let actions=policy==="qmdp"?[argmin(A,a=>avgQ(b,h,a))]:A,best;
    for(let a of actions){let z=next(b,a),v=[z.r,0,0,0];if(h>1)for(const g of z.p)add(v,sense(g.b,h-1),g.n/z.n);if(!best||cost(v)<cost(best)-1e-10)best=v;}am.set(k,best);return best;}
   let v=[0,0,0,0],rows=[];for(let g of start){let x=sense(g.b,H);add(v,x,g.n/init.length);rows.push({k:g.k,n:g.n,v:x,m:first.get(H+"|"+key(g.b))});}
   return{v,rows,stats:[sm.size,am.size]};
  }
  const start=part(init,0),policies=["free","adaptive","qmdp"],sol=Object.fromEntries(policies.map(p=>[p,solve(p)]));
  for(const p of policies)if(cost(sol.adaptive.v)>cost(sol[p].v)+1e-9)throw Error("optimality");
  let gain=0,both=0,equal=0,rate=0,mixed=0,positive=0,npositive=0,max=0;
  for(let i=0;i<start.length;i++){let row=sol.free.rows[i],ad=sol.adaptive.rows[i],d=cost(row.v)-cost(ad.v);if(d<-1e-9)throw Error("conditional dominance");let [s,l,n0,n1]=row.k.split(",").map(Number),w=row.n*d;if(d>1e-9){positive++;npositive+=row.n;max=Math.max(max,d);gain+=w;if(s===K[0]&&l===K[1])both+=w;if(s===l)equal+=w;if(s*K[1]===l*K[0])rate+=w;if(n0&&n1)mixed+=w;}
   classes.push({K,L,schedule,k:row.k,n:row.n,gain:d,first:ad.m,qmdpFirst:sol.qmdp.rows[i].m,qmdpLoss:cost(sol.qmdp.rows[i].v)-cost(ad.v)});
  }
  results.push({K,L,schedule,N:init.length,groups:start.length,positive,npositive,max,gain:gain/init.length,shares:{both:both/gain,equal:equal/gain,rate:rate/gain,mixed:mixed/gain},policies:Object.fromEntries(policies.map(p=>[p,{v:sol[p].v,cost:cost(sol[p].v),stats:sol[p].stats}])),states:states.length,transitions:tr.size});
 }
 for(const a of results){let b=results.find(x=>x.K.join()===a.K.join()&&x.L===a.L&&x.schedule.length===4);if(a.policies.adaptive.cost<b.policies.adaptive.cost-1e-9)throw Error("availability dominance");}
 if(Math.abs(results[0].policies.adaptive.cost-3013/279)>1e-9)throw Error("base replay");
 return{results,classes};
}
console.log(JSON.stringify(h08h(),null,2));

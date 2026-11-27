/* H08I rolling truncated belief tree; node h08i_lookahead.js */
function h08i(){
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
   const depth=policy==="adaptive"?H:policy==="qmdp"?1:policy.startsWith("depth")?Number(policy.slice(5)):H;
   const ps=new Map(),pa=new Map(),es=new Map(),ea=new Map();
   function modes(b,h){if(policy==="free"||!schedule.includes(H-h+1))return [0];if(policy==="head"||policy==="full"){const m=policy==="head"?1:2;return [part(b,m).length>1?m:0];}return [0,1,2];}
   function terminal(b,h){return h?b.reduce((s,[i,n])=>s+n*fv(i,h),0)/mass(b):0;}
   function planSense(b,h,d){const k=h+"|"+d+"|"+key(b);if(ps.has(k))return ps.get(k);const n=mass(b);let best=Infinity,mode=0;for(const m of modes(b,h)){let v=prices[m];for(const z of m===0?[{b,n}]:part(b,m))v+=z.n/n*planAct(z.b,h,d).v;if(v<best-1e-10){best=v;mode=m;}}const r={v:best,m:mode};ps.set(k,r);return r;}
   function planAct(b,h,d){const k=h+"|"+d+"|"+key(b);if(pa.has(k))return pa.get(k);let best=Infinity,action=0;for(const a of A){const z=next(b,a);let v=z.r;if(h>1)for(const g of z.p)v+=g.n/z.n*(d>1?planSense(g.b,h-1,d-1).v:terminal(g.b,h-1));if(v<best-1e-10){best=v;action=a;}}const r={v:best,a:action};pa.set(k,r);return r;}
   function evalSense(b,h){const k=h+"|"+key(b);if(es.has(k))return es.get(k);const m=planSense(b,h,Math.min(depth,h)).m,n=mass(b),v=[0,prices[m],+(m===1),+(m===2)];for(const z of m===0?[{b,n}]:part(b,m))add(v,evalAct(z.b,h),z.n/n);es.set(k,v);return v;}
   function evalAct(b,h){const k=h+"|"+key(b);if(ea.has(k))return ea.get(k);const a=planAct(b,h,Math.min(depth,h)).a,z=next(b,a),v=[z.r,0,0,0];if(h>1)for(const g of z.p)add(v,evalSense(g.b,h-1),g.n/z.n);ea.set(k,v);return v;}
   let v=[0,0,0,0],rows=[];for(const g of start){let x=evalSense(g.b,H);add(v,x,g.n/init.length);rows.push({k:g.k,n:g.n,v:x,m:planSense(g.b,H,depth).m});}
   return {v,rows,stats:{planSense:ps.size,planAct:pa.size,evalSense:es.size,evalAct:ea.size,fullMemo:fullmemo.size}};
  }
  const start=part(init,0),policies=["free","adaptive","qmdp","depth2","depth3","head","full"],sol=Object.fromEntries(policies.map(p=>[p,solve(p)]));
  for(const p of policies)if(cost(sol.adaptive.v)>cost(sol[p].v)+1e-9)throw Error("optimality");
  let gain=0,both=0,equal=0,rate=0,mixed=0,positive=0,npositive=0,max=0;
  for(let i=0;i<start.length;i++){let row=sol.free.rows[i],ad=sol.adaptive.rows[i],d=cost(row.v)-cost(ad.v);if(d<-1e-9)throw Error("conditional dominance");let [s,l,n0,n1]=row.k.split(",").map(Number),w=row.n*d;if(d>1e-9){positive++;npositive+=row.n;max=Math.max(max,d);gain+=w;if(s===K[0]&&l===K[1])both+=w;if(s===l)equal+=w;if(s*K[1]===l*K[0])rate+=w;if(n0&&n1)mixed+=w;}
   classes.push({K,L,schedule,k:row.k,n:row.n,gain:d,first:ad.m,qmdpFirst:sol.qmdp.rows[i].m,qmdpLoss:cost(sol.qmdp.rows[i].v)-cost(ad.v),depth2Loss:cost(sol.depth2.rows[i].v)-cost(ad.v),depth3Loss:cost(sol.depth3.rows[i].v)-cost(ad.v),depth2First:sol.depth2.rows[i].m,depth3First:sol.depth3.rows[i].m});
  }
  results.push({K,L,schedule,N:init.length,groups:start.length,positive,npositive,max,gain:gain/init.length,shares:{both:both/gain,equal:equal/gain,rate:rate/gain,mixed:mixed/gain},policies:Object.fromEntries(policies.map(p=>[p,{v:sol[p].v,cost:cost(sol[p].v),stats:sol[p].stats}])),states:states.length,transitions:tr.size});
 }
 for(const a of results){let b=results.find(x=>x.K.join()===a.K.join()&&x.L===a.L&&x.schedule.length===4);if(a.policies.adaptive.cost<b.policies.adaptive.cost-1e-9)throw Error("availability dominance");}
 if(Math.abs(results[0].policies.adaptive.cost-3013/279)>1e-9)throw Error("base replay");
 return{results,classes};
}
console.log(JSON.stringify(h08i(),null,2));

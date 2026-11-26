/* node h08e_conditional_transport.js */
function h08e(){
 const A=[0,1],c=1/16,H=4,words=[""];
 for(let n=1;n<=4;n++)for(let i=0;i<2**n;i++)words.push(i.toString(2).padStart(n,"0"));
 const states=[],ids=new Map(),trans=new Map();let tc=0;
 function id(q,w){const k=[...q,w].join(",");if(!ids.has(k)){ids.set(k,states.length);states.push({q,w,n0:w.split("0").length-1,n1:w.split("1").length-1});}return ids.get(k);}
 const initial=[];for(let s=0;s<=2;s++)for(let l=0;l<=2;l++)for(const w of words)initial.push(id([s,l],w));
 function step(i,a){const k=i*2+a;if(trans.has(k))return trans.get(k);let {q,w}=states[i],old=q[0]+q[1]+w.length;q=q.slice();const d=q[a];q[a]=0;for(let j=0;j<2&&w&&q[+w[0]]<2;j++){q[+w[0]]++;w=w.slice(1);}const r=q[0]+q[1]+w.length;if(r!==old-d||q.some(x=>x<0||x>2))throw Error("conservation");const z={r,next:A.map(a=>id(q.slice(),w+a))};trans.set(k,z);tc++;return z;}
 const gcd=(a,b)=>b?gcd(b,a%b):a;
 const mass=b=>b.reduce((s,p)=>s+p[1],0),key=b=>b.map(p=>p.join(":")).join(",");
 function norm(m){const b=[...m].sort((a,b)=>a[0]-b[0]),g=b.reduce((x,p)=>gcd(x,p[1]),0);return b.map(([i,n])=>[i,n/g]);}
 function obs(i,m){const s=states[i];return m===0?[...s.q,s.n0,s.n1].join(","):m===1?s.w.slice(0,1):s.w;}
 function partition(b,m){const d=new Map();for(const [i,n] of b){const k=obs(i,m);if(!d.has(k))d.set(k,new Map());d.get(k).set(i,n);}return new Map([...d].map(([k,v])=>[k,{b:norm(v),n:[...v.values()].reduce((a,b)=>a+b,0)}]));}
 function next(b,a,p){const d=new Map();let r=0;for(const [i,n] of b){const z=step(i,a);r+=n*z.r;for(const e of A){const k=z.next[e];d.set(k,(d.get(k)||0)+n*p[e]);}}const n=mass(b),m=p[0]+p[1];if([...d.values()].reduce((a,b)=>a+b,0)!==n*m)throw Error("posterior mass");return{r:r/n,parts:partition([...d],0),den:n*m};}
 const laws=[{name:"nominal",p:[1,1],w:"uniform"},{name:"arrivals_S20",p:[1,4],w:"uniform"},{name:"arrivals_S80",p:[4,1],w:"uniform"},{name:"clustered",p:[1,1],w:"clustered"},{name:"alternating",p:[1,1],w:"alternating"},{name:"clustered_S80",p:[4,1],w:"clustered"}];
 function start(law){const b=initial.map(i=>{const w=states[i].w;let n=0;for(let j=1;j<w.length;j++)if(law.w==="clustered"&&w[j]===w[j-1]||law.w==="alternating"&&w[j]!==w[j-1])n++;return[i,2**n];});return{n:mass(b),parts:partition(b,0)};}
 const costs=[0,c/4,c],Z=()=>[0,0,0,0],total=v=>v[0]+v[1],add=(v,u,w)=>{for(let j=0;j<4;j++)v[j]+=w*u[j];};
 function solver(law,policy){
  const sm=new Map(),am=new Map(),fm=new Map();
  function fq(i,h,a){const z=step(i,a);return z.r+(h===1?0:z.next.reduce((s,j,e)=>s+law.p[e]/(law.p[0]+law.p[1])*fv(j,h-1),0));}
  function fv(i,h){const k=i+"|"+h;if(!fm.has(k))fm.set(k,Math.min(...A.map(a=>fq(i,h,a))));return fm.get(k);}
  function modes(b,h){
   if(policy==="free")return[0];
   if(policy==="head"||policy==="full"){const m=policy==="head"?1:2;return[partition(b,m).size>1?m:0];}
   if(policy==="adaptive")return[0,1,2];
   let best=Infinity,bm=0;const n=mass(b);
   for(const m of [0,1,2]){
    const parts=m===0?[{b,n}]:[...partition(b,m).values()];
    let v=costs[m];for(const q of parts){v+=q.n/n*Math.min(...A.map(a=>q.b.reduce((s,[i,w])=>s+w*fq(i,h,a),0)/mass(q.b)));}
    if(v<best-1e-11){best=v;bm=m;}
   }return[bm];
  }
  function sense(b,h){const k=h+"|"+key(b);if(sm.has(k))return sm.get(k);let best;
   for(const m of modes(b,h)){const n=mass(b),v=[0,costs[m],+(m===1),+(m===2)],parts=m===0?[{b,n}]:[...partition(b,m).values()];for(const q of parts)add(v,act(q.b,h).v,q.n/n);
    if(!best||total(v)<total(best.v)-1e-11)best={m,v};}
   sm.set(k,best);return best;}
  function act(b,h){const k=h+"|"+key(b);if(am.has(k))return am.get(k);let best;
   for(const a of A){const z=next(b,a,law.p),v=[z.r,0,0,0];if(h>1)for(const q of z.parts.values())add(v,sense(q.b,h-1).v,q.n/z.den);
    if(!best||total(v)<total(best.v)-1e-11)best={a,v};}am.set(k,best);return best;}
  return{sense,act,stats:()=>[sm.size,am.size,fm.size]};
 }
 function evaluation(model,law,sol){
  const em=new Map();function es(b,t,h){const k=h+"|"+key(b)+"|"+key(t);if(em.has(k))return em.get(k);const m=sol.sense(b,h).m,n=mass(t),v=[0,costs[m],+(m===1),+(m===2)];
   if(m===0)add(v,ea(b,t,h),1);else{const bp=partition(b,m);for(const [k,q] of partition(t,m)){if(!bp.has(k))throw Error("support");add(v,ea(bp.get(k).b,q.b,h),q.n/n);}}
   em.set(k,v);return v;}
  function ea(b,t,h){const a=sol.act(b,h).a,z=next(t,a,law.p),v=[z.r,0,0,0];if(h>1){const bp=next(b,a,model.p).parts;for(const [k,q] of z.parts){if(!bp.has(k))throw Error("support");add(v,es(bp.get(k).b,q.b,h-1),q.n/z.den);}}return v;}
  const mb=start(model),tb=start(law),v=Z(),rows=[];for(const [k,q] of tb.parts){const b=mb.parts.get(k).b,x=es(b,q.b,H);add(v,x,q.n/tb.n);rows.push({k,n:q.n,v:x,first:sol.sense(b,H).m});}
  return{v,rows,evalStates:em.size};
 }
 const policies=["free","head","full","gate","adaptive"],nom=laws[0],sols=Object.fromEntries(policies.map(p=>[p,solver(nom,p)])),results=[],conditional=[];
 for(const law of laws){
  const cases={};for(const p of policies){const x=evaluation(nom,law,sols[p]);cases[p]=x;results.push({law:law.name,policy:p,v:x.v,objective:total(x.v),evalStates:x.evalStates});}
  const optimal=solver(law,"adaptive"),r=evaluation(law,law,optimal);results.push({law:law.name,policy:"reoptimized",v:r.v,objective:total(r.v),evalStates:r.evalStates});
  if(policies.some(p=>total(r.v)>total(cases[p].v)+1e-9))throw Error("reoptimized dominance");
  if(law===nom){for(const p of policies){const st=start(nom),v=Z();for(const q of st.parts.values())add(v,sols[p].sense(q.b,H).v,q.n/st.n);if(v.some((z,i)=>Math.abs(z-cases[p].v[i])>1e-9))throw Error("nominal replay");}
   for(let i=0;i<cases.free.rows.length;i++){const x=cases.free.rows[i],a=cases.adaptive.rows[i],g=cases.gate.rows[i];if(x.k!==a.k||x.k!==g.k)throw Error("class order");const gain=total(x.v)-total(a.v);if(gain< -1e-9)throw Error("conditional dominance");conditional.push({k:x.k,n:x.n,free:total(x.v),adaptive:total(a.v),gate:total(g.v),gain,adaptiveFirst:a.first,gateFirst:g.first,adaptiveAcq:a.v[2]+a.v[3]});}
  }
 }
 return{results,conditional,states:states.length,transitions:tc,nominalStats:Object.fromEntries(policies.map(p=>[p,sols[p].stats()]))};
}
console.log(JSON.stringify(h08e(),null,2));

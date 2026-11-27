/* node h08g_phase_memory.js */
function h08g(){
 const A=[0,1],prices=[0,1/64,1/16],results=[],witnesses=[];
 for(const K of [[2,2],[3,2]])for(const H of [4,5])for(const lambda of [0,.5,1,2]){
  const words=[""];for(let n=1;n<=4;n++)for(let i=0;i<2**n;i++)words.push(i.toString(2).padStart(n,"0"));
  const states=[],ids=new Map(),tr=new Map(),fm=new Map();
  function id(q,w,p){let k=[...q,w,p].join(",");if(!ids.has(k)){ids.set(k,states.length);states.push({q,w,p,n0:w.split("0").length-1,n1:w.split("1").length-1});}return ids.get(k);}
  const init=[];for(let s=0;s<=K[0];s++)for(let l=0;l<=K[1];l++)for(const w of words)for(const p of A)init.push([id([s,l],w,p),1]);
  function step(i,a){let k=i*2+a;if(tr.has(k))return tr.get(k);let {q,w,p}=states[i],old=q[0]+q[1]+w.length;q=q.slice();let d=Math.min(q[a],2);q[a]-=d;for(let j=0;j<2&&w&&q[+w[0]]<K[+w[0]];j++){q[+w[0]]++;w=w.slice(1);}let stock=q[0]+q[1]+w.length;if(stock!==old-d||q.some((x,j)=>x<0||x>K[j]))throw Error("conservation");let z={r:stock+lambda*(a!==p),stock,sw: +(a!==p),next:A.map(e=>id(q.slice(),w+e,a))};tr.set(k,z);return z;}
  function fq(i,h,a){const z=step(i,a);return z.r+(h>1?(fv(z.next[0],h-1)+fv(z.next[1],h-1))/2:0);}
  function fv(i,h){const k=i+"|"+h;if(!fm.has(k))fm.set(k,Math.min(...A.map(a=>fq(i,h,a))));return fm.get(k);}
  const mass=b=>b.reduce((s,p)=>s+p[1],0),key=b=>b.map(x=>x.join(":")).join(","),gcd=(a,b)=>b?gcd(b,a%b):a;
  function norm(d){let b=[...d].sort((a,b)=>a[0]-b[0]),g=b.reduce((z,p)=>gcd(z,p[1]),0);return b.map(([i,n])=>[i,n/g]);}
  function obs(i,m){let s=states[i];return m===0?[...s.q,s.n0,s.n1,s.p].join(","):m===1?s.w.slice(0,1):s.w;}
  function part(b,m){const d=new Map();for(let [i,n] of b){let k=obs(i,m);if(!d.has(k))d.set(k,new Map());d.get(k).set(i,n);}const p=[...d].map(([k,v])=>({k,b:norm(v),n:mass([...v])}));if(p.reduce((s,x)=>s+x.n,0)!==mass(b))throw Error("mass");return p;}
  function next(b,a){let d=new Map(),stock=0,sw=0;for(let [i,n] of b){let z=step(i,a);stock+=n*z.stock;sw+=n*z.sw;for(let j of z.next)d.set(j,(d.get(j)||0)+n);}let n=mass(b);if(mass([...d])!==2*n)throw Error("transition mass");return {stock:stock/n,sw:sw/n,p:part([...d],0),n:2*n};}
  const add=(v,u,p)=>{for(let i=0;i<5;i++)v[i]+=p*u[i];},cost=v=>v[0]+lambda*v[1]+v[2],avgQ=(b,h,a)=>b.reduce((s,[i,n])=>s+n*fq(i,h,a),0)/mass(b);
  const argmin=(xs,score)=>xs.reduce((best,x)=>score(x)<score(best)-1e-10?x:best,xs[0]);
  function surrogate(b,h,m){let n=mass(b),p=m===0?[{b,n}]:part(b,m);return prices[m]+p.reduce((s,z)=>s+z.n/n*Math.min(...A.map(a=>avgQ(z.b,h,a))),0);}
  const start=part(init,0);
  function solve(policy){
   let sm=new Map(),am=new Map();
   function sense(b,h){const k=h+"|"+key(b);if(sm.has(k))return sm.get(k);const n=mass(b);let modes=policy==="free"?[0]:policy==="qmdp"?[argmin([0,1,2],x=>surrogate(b,h,x))]:[0,1,2];let best;
    for(let m of modes){let v=[0,0,prices[m],+(m===1),+(m===2)];for(const z of (m===0?[{b,n}]:part(b,m)))add(v,act(z.b,h).v,z.n/n);if(!best||cost(v)<cost(best.v)-1e-10)best={m,v};}sm.set(k,best);return best;}
   function act(b,h){let k=h+"|"+key(b);if(am.has(k))return am.get(k);let actions=policy==="qmdp"?[argmin(A,a=>avgQ(b,h,a))]:A,best;
    for(let a of actions){let z=next(b,a),v=[z.stock,z.sw,0,0,0];if(h>1)for(const g of z.p)add(v,sense(g.b,h-1).v,g.n/z.n);if(!best||cost(v)<cost(best.v)-1e-10)best={a,v};}am.set(k,best);return best;}
   let v=[0,0,0,0,0],rows=[];for(let g of start){let x=sense(g.b,H);add(v,x.v,g.n/init.length);rows.push({k:g.k,n:g.n,v:x.v,m:x.m});}
   return{v,rows};
  }
  const sol=Object.fromEntries(["free","adaptive","qmdp"].map(p=>[p,solve(p)]));
  let nbad=0,nworld=0,max=0,ex=null;for(let i=0;i<start.length;i++){let a=sol.adaptive.rows[i],q=sol.qmdp.rows[i],f=sol.free.rows[i],loss=cost(q.v)-cost(a.v);if(loss<-1e-9||cost(f.v)-cost(a.v)<-1e-9)throw Error("dominance");if(loss>1e-9){nbad++;nworld+=a.n;if(loss>max){max=loss;ex={k:a.k,n:a.n,adaptive:a,qmdp:q,free:f,loss};}}}
  if(ex)witnesses.push({K,H,lambda,...ex});
  if(lambda===0&&H===4){const expected=K[0]===2?3013/279:11.82997311827957;if(Math.abs(cost(sol.adaptive.v)-expected)>1e-9)throw Error("base replay");}
  results.push({K,H,lambda,worlds:init.length,groups:start.length,nbad,nworld,max,policies:Object.fromEntries(Object.entries(sol).map(([p,x])=>[p,{v:x.v,cost:cost(x.v)}])),states:states.length,transitions:tr.size});
 }
 return{results,witnesses};
}
console.log(JSON.stringify(h08g(),null,2));

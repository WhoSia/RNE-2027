function auditK(){
const A=[0,1],results=[]; // All costs are integer multiples of 1/(64*2^H), posterior means may be rational.
function gcd(a,b){return b===0n?a:gcd(b,a%b)}
class F{
 constructor(n,d=1n){n=BigInt(n);d=BigInt(d);let g=gcd(n<0n?-n:n,d);this.n=n/g;this.d=d/g;}
 add(x){return new F(this.n*x.d+x.n*this.d,this.d*x.d)}
 mul(n,d=1n){return new F(this.n*BigInt(n),this.d*BigInt(d))}
 lt(x){return this.n*x.d<x.n*this.d}
 str(){return this.n+"/"+this.d}
 num(){return Number(this.n)/Number(this.d)}
}
const Z=new F(0),C=[Z,new F(1,64),new F(1,16)];
for(const K of [[2,2],[3,2]])for(const H of [4])for(const L of [4])for(const schedule of [[1,2,3,4],[1]])for(const innovation of ['SORTED','RANDOM']){
 const W=[""];for(let j=1;j<=L;j++)for(let i=0;i<2**j;i++)W.push(i.toString(2).padStart(j,"0"));
 const worlds=[];for(let s=0;s<=K[0];s++)for(let l=0;l<=K[1];l++)for(const w of W)worlds.push([[s,l,w].join("|"),1]);
 const parse=x=>{let [s,l,w]=x.split("|");return [+s,+l,w]};
 const obs=(x,m)=>{const [s,l,w]=parse(x);return m===0?[s,l,w.split("0").length-1,w.split("1").length-1].join(","):m===1?w.slice(0,1):w};
 const sum=b=>b.reduce((a,x)=>a+x[1],0),key=b=>JSON.stringify(b),tm=new Map(),fm=new Map();
 function split(b,m){let groups=new Map();for(let [x,n] of b){let k=obs(x,m);if(!groups.has(k))groups.set(k,new Map());let q=groups.get(k);q.set(x,(q.get(x)||0)+n);}
 return [...groups].map(([k,g])=>{let n=sum([...g]),d=[...g.values()].reduce((a,b)=>Number(gcd(BigInt(a),BigInt(b))),0);return {k,n,b:[...g].sort((a,b)=>a[0]<b[0]?-1:1).map(([x,v])=>[x,v/d])};});}
 function step(x,a){let k=x+";"+a;if(tm.has(k))return tm.get(k);let [s,l,w]=parse(x),q=[s,l],buf=[...w].map(Number),old=s+l+buf.length;
 for(let j=0;j<2;j++)if(q[a])q[a]--;
 for(let j=0;j<2;j++){if(!buf.length||q[buf[0]]===K[buf[0]])break;q[buf.shift()]++;}
 let r=q[0]+q[1]+buf.length;if(r!==old-Math.min(a===0?s:l,2))throw Error("mass");let next=(innovation==="SORTED"?["00","01","01","11"]:["00","01","10","11"]).map(z=>[...q,buf.join("")+z].join("|")),v={r,next};tm.set(k,v);return v;}
 function fv(x,h){if(!h)return Z;let k=x+";"+h;if(fm.has(k))return fm.get(k);let best;for(let a of A){let {r,next}=step(x,a),v=new F(r).add(next.reduce((s,y)=>s.add(fv(y,h-1)),Z).mul(1,4));if(!best||v.lt(best))best=v;}fm.set(k,best);return best;}
 const start=split(worlds,0),policies=H===4?["free","adaptive","qmdp","depth2","depth3","head","full"]:["free","adaptive","qmdp","depth2","depth3","depth4"],sol={};
 for(let policy of policies){let depth=policy==="qmdp"?1:policy.startsWith("depth")?+policy.slice(5):H,ps=new Map(),pa=new Map(),es=new Map(),ea=new Map(),adv=new Map();
 function next(b,a){let k=key(b)+";"+a;if(adv.has(k))return adv.get(k);let m=new Map(),r=0,n=sum(b);for(let [x,w] of b){let s=step(x,a);r+=w*s.r;for(let y of s.next)m.set(y,(m.get(y)||0)+w);}let v={r:new F(r,n),p:split([...m],0),den:4*n};adv.set(k,v);return v;}
 function parts(b,m){return m?split(b,m):[{n:sum(b),b}];}
 function modes(b,h){if(policy==="free"||!schedule.includes(H-h+1))return [0];if(policy==="head"||policy==="full"){let m=policy==="head"?1:2;return split(b,m).length>1?[m]:[0];}return[0,1,2];}
 function tail(b,h){return b.reduce((v,[x,n])=>v.add(fv(x,h).mul(n,sum(b))),Z)}
 function plan(b,h,d){let k=key(b)+";"+h+";"+d;if(ps.has(k))return ps.get(k);let best;for(let m of modes(b,h)){let v=C[m];for(let z of parts(b,m))v=v.add(choose(z.b,h,d).v.mul(z.n,sum(b)));if(!best||v.lt(best.v))best={v,m};}ps.set(k,best);return best;}
 function choose(b,h,d){let k=key(b)+";"+h+";"+d;if(pa.has(k))return pa.get(k);let best;for(let a of A){let z=next(b,a),v=z.r;if(h>1)for(let g of z.p)v=v.add((d>1?plan(g.b,h-1,d-1).v:tail(g.b,h-1)).mul(g.n,z.den));if(!best||v.lt(best.v))best={v,a};}pa.set(k,best);return best;}
 function ev(b,h){let k=key(b)+";"+h;if(es.has(k))return es.get(k);let m=plan(b,h,Math.min(depth,h)).m,v=C[m];for(let z of parts(b,m))v=v.add(ctrl(z.b,h).mul(z.n,sum(b)));es.set(k,v);return v;}
 function ctrl(b,h){let k=key(b)+";"+h;if(ea.has(k))return ea.get(k);let a=choose(b,h,Math.min(depth,h)).a,z=next(b,a),v=z.r;if(h>1)for(let g of z.p)v=v.add(ev(g.b,h-1).mul(g.n,z.den));ea.set(k,v);return v;}
 let rows=start.map(g=>({k:g.k,n:g.n,v:ev(g.b,H),m:plan(g.b,H,depth).m}));sol[policy]={rows,v:rows.reduce((s,x)=>s.add(x.v.mul(x.n,worlds.length)),Z)};
 }
 const rows=start.map((g,i)=>{const a=sol.adaptive.rows[i],f=sol.free.rows[i];let row={k:g.k,n:g.n,gain:f.v.add(a.v.mul(-1)).str(),first:a.m};for(let p of policies){let s=sol[p].rows[i];if(s.v.lt(a.v))throw Error("exact dominance");row[p+"Loss"]=s.v.add(a.v.mul(-1)).str();row[p+"First"]=s.m;}return row;});
 results.push({K,H,L,schedule,innovation,N:worlds.length,policies:Object.fromEntries(policies.map(p=>[p,sol[p].v.str()])),classes:rows});
}
return results;
}
console.log(JSON.stringify(auditK(),null,2));

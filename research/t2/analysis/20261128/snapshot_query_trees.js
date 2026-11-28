// Exact frozen-snapshot query trees; no actual traffic control.
function study(n){
 const U=[[0,0],[0,1],[1,0],[1,1]],pop=x=>x.toString(2).split("1").length-1;
 const trans=(s,u)=>{let [m,a]=s,[g,r]=u,e=+(g&&a===2&&((m>>(n-1))&1));if(e)m&=~(1<<(n-1));let old=m;for(let i=0;i<n-1;i++)if((old>>i&1)&&!(old>>(i+1)&1))m=(m&~(1<<i))|(1<<(i+1));const accept=+(r&&!(m&1));if(accept)m|=1;return [2*e+accept,[m,e?1:Math.min(2,a+1)]]};
 const key=s=>s.join("/"),states=[[0,2]],seen=new Set([key(states[0])]);
 for(let i=0;i<states.length;i++)for(const u of U){const z=trans(states[i],u)[1];if(!seen.has(key(z))){states.push(z);seen.add(key(z))}}
 states.sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
 const ids=new Map(states.map((s,i)=>[key(s),i])),edges=states.map(s=>U.map(u=>{const [o,z]=trans(s,u);return [o,ids.get(key(z))]}));
 const groups=new Map();states.forEach((s,i)=>{const k=pop(s[0])+"/"+s[1];if(!groups.has(k))groups.set(k,[]);groups.get(k).push(i)});
 let sig=states.map(()=>0),results=[],checks=0;
 for(let h=1;h<=4;h++){
  const map=new Map(),prev=sig;sig=edges.map(es=>{const k=es.map(([o,j])=>o+":"+prev[j]).join("|");if(!map.has(k))map.set(k,map.size);return map.get(k)});
  const words=Array.from({length:4**h},(_,w)=>Array.from({length:h},(_,i)=>w>>2*(h-1-i)&3));
  const explicit=states.map((s,i)=>words.map(w=>{let j=i;return w.map(u=>{const [o,k]=edges[j][u];j=k;return o}).join("")}).join("|"));
  const a=new Map(),b=new Map();for(let i=0;i<states.length;i++){if((a.has(sig[i])&&a.get(sig[i])!==explicit[i])||(b.has(explicit[i])&&b.get(explicit[i])!==sig[i]))throw Error("signature mismatch");a.set(sig[i],explicit[i]);b.set(explicit[i],sig[i]);checks++}
  const valid=(g,m)=>{const p=new Map();for(const i of g){const x=states[i][0]&m;if(p.has(x)&&p.get(x)!==sig[i])return false;p.set(x,sig[i])}return true};
  const masks=Array.from({length:1<<n},(_,i)=>i).sort((a,b)=>pop(a)-pop(b)||a-b);
  const global=masks.find(m=>[...groups.values()].every(g=>valid(g,m)));
  const memo=new Map();
  function dp(g){
   const k=g.join(",");if(memo.has(k))return memo.get(k);
   if(g.every(i=>sig[i]===sig[g[0]])){const z={worst:0,sum:0,qw:-1,qe:-1};memo.set(k,z);return z}
   let best={worst:Infinity,sum:Infinity,qw:-1,qe:-1};
   for(let c=0;c<n;c++){const l=g.filter(i=>!(states[i][0]>>c&1)),r=g.filter(i=>states[i][0]>>c&1);if(!l.length||!r.length)continue;const x=dp(l),y=dp(r),w=1+Math.max(x.worst,y.worst),s=g.length+x.sum+y.sum;
   if(w<best.worst){best.worst=w;best.qw=c}if(s<best.sum){best.sum=s;best.qe=c}}
   if(!Number.isFinite(best.worst)||!Number.isFinite(best.sum))throw Error("unresolved");memo.set(k,best);return best
  }
  const detail=[];let worst=0,sum=0,cw=0,cs=0,meanPolicyWorst=0,worstPolicySum=0,zero=0;
  for(const [k,g] of groups){const m=masks.find(m=>valid(g,m)),d=dp(g);cw=Math.max(cw,pop(m));cs+=pop(m)*g.length;worst=Math.max(worst,d.worst);sum+=d.sum;if(d.worst===0)zero+=g.length;
   let s1=0,s2=0,w1=0,w2=0;
   for(const i of g)for(const obj of ["qw","qe"]){let z=g,depth=0;while(dp(z)[obj]>=0){const c=dp(z)[obj];z=z.filter(j=>(states[j][0]>>c&1)===(states[i][0]>>c&1));depth++;if(depth>n)throw Error("cycle")}if(!z.includes(i)||!z.every(j=>sig[j]===sig[i]))throw Error("bad leaf");if(obj==="qw"){s1+=depth;w1=Math.max(w1,depth)}else{s2+=depth;w2=Math.max(w2,depth)}checks++}
   if(w1!==d.worst||s2!==d.sum||d.worst>pop(m)||d.sum>pop(m)*g.length)throw Error("DP verification");
   meanPolicyWorst=Math.max(meanPolicyWorst,w2);worstPolicySum+=s1;
   detail.push({group:k,size:g.length,fixedMask:m,fixed:pop(m),worst:d.worst,sum:d.sum,firstWorst:d.qw,firstMean:d.qe,meanPolicyWorst:w2});
  }
  results.push({h,classes:map.size,globalFixed:pop(global),globalMask:global,conditionedFixedWorst:cw,conditionedFixedSum:cs,adaptiveWorst:worst,adaptiveMeanSum:sum,adaptiveMean:sum/states.length,meanPolicyWorst,worstPolicySum,zeroQueryStates:zero,groups:detail,memo:memo.size});
 }
 return {n,states:states.length,checks,results};
}
const result=[2,4,8].map(study);console.log(JSON.stringify(result,null,2));

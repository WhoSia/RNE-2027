/* node h08d_persistent.js */
function persistent(){
 const A=[0,1],words=[""];for(let n=1;n<=4;n++)for(let k=0;k<2**n;k++)words.push(k.toString(2).padStart(n,"0"));
 const state=[],index=new Map(), cache=new Map();let transitions=0;
 function id(q0,q1,w){const k=q0+","+q1+","+w;if(!index.has(k)){index.set(k,state.length);state.push({q:[q0,q1],w,c:[w.split("0").length-1,w.split("1").length-1]});}return index.get(k);}
 const initial=[];for(let s=0;s<=2;s++)for(let l=0;l<=2;l++)for(const w of words)initial.push(id(s,l,w));
 function step(i,a){const k=i*2+a;if(cache.has(k))return cache.get(k);const {q:old,w:oldw,c}=state[i];const q=old.slice();let w=oldw;const d=Math.min(q[a],2);q[a]-=d;for(let j=0;j<2&&w&&q[+w[0]]<2;j++){q[+w[0]]++;w=w.slice(1);}const r=q[0]+q[1]+w.length;if(r!==old[0]+old[1]+c[0]+c[1]-d||q.some(x=>x<0||x>2))throw Error("conservation");const x={r,next:A.map(b=>id(...q,w+b))};cache.set(k,x);transitions++;return x;}
 const gcd=(a,b)=>b?gcd(b,a%b):a;
 function norm(m){const pairs=[...m.entries()].sort((a,b)=>a[0]-b[0]);const g=pairs.reduce((x,[_,v])=>gcd(x,v),0);return pairs.map(([i,v])=>[i,v/g]);}
 const mass=b=>b.reduce((s,[_,v])=>s+v,0),key=b=>b.map(p=>p.join(":")).join(",");
 const obs=(i,mode)=>{const s=state[i];return mode==="free"?[...s.q,...s.c].join(","):mode==="head"?s.w.slice(0,1):s.w;};
 function groups(b,mode){const g=new Map();for(const [i,n] of b){const k=obs(i,mode);if(!g.has(k))g.set(k,new Map());g.get(k).set(i,n);}return [...g.values()].map(m=>({n:[...m.values()].reduce((a,b)=>a+b,0),b:norm(m)}));}
 const start=groups(initial.map(i=>[i,1]),"free");
 const costs=[0,1/64,1/16,1/4,1],rows=[];
 for(const c of costs)for(const policy of ["free","head","full","adaptive"]){
  const memo=new Map(),actMemo=new Map();let calls=0;
  function select(b,h){
    if(!h)return [0,0,0,0];
    const k=h+"|"+key(b);if(memo.has(k))return memo.get(k);calls++;
    const modes=policy==="adaptive"?["free","head","full"]:[policy];let best;
    for(const mode of modes){const partitions=mode==="free"?[{n:mass(b),b}]:groups(b,mode);const m=mass(b),v=[0,mode==="head"?c/4:mode==="full"?c:0,mode==="head"?1:0,mode==="full"?1:0];
      for(const p of partitions){const z=act(p.b,h);for(let j=0;j<4;j++)v[j]+=p.n/m*z[j];}
      if(!best||v[0]+v[1]<best[0]+best[1]-1e-11)best=v;
    }memo.set(k,best);return best;
  }
  function act(b,h){const k=h+"|"+key(b);if(actMemo.has(k))return actMemo.get(k);const m=mass(b);let best;
    for(const a of A){let r=0;const next=new Map();for(const [i,n] of b){const z=step(i,a);r+=n*z.r;for(const j of z.next)next.set(j,(next.get(j)||0)+n);}
      const v=[r/m,0,0,0];if(h>1)for(const p of groups([...next],"free")){const z=select(p.b,h-1);for(let j=0;j<4;j++)v[j]+=p.n/(2*m)*z[j];}
      if(!best||v[0]+v[1]<best[0]+best[1]-1e-11)best=v;
    }actMemo.set(k,best);return best;
  }
  for(let h=1;h<=4;h++){const v=[0,0,0,0];for(const p of start){const z=select(p.b,h);for(let j=0;j<4;j++)v[j]+=p.n/initial.length*z[j];}rows.push({c,policy,h,traffic:v[0],sensing:v[1],head:v[2],full:v[3],objective:v[0]+v[1],beliefCalls:calls});}
 }
 for(const c of costs)for(let h=1;h<=4;h++){const s=rows.filter(r=>r.c===c&&r.h===h),a=s.find(r=>r.policy==="adaptive"),f=s.find(r=>r.policy==="full");if(s.some(r=>a.objective>r.objective+1e-9)||c===0&&Math.abs(a.objective-f.objective)>1e-9)throw Error("dominance");}
 return{initial:initial.length,freeGroups:start.length,states:state.length,transitions,rows};
}
console.log(JSON.stringify(persistent(),null,2));

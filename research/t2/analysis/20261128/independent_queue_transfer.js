// Independent simplified offline queue model; not a road controller.
function experiment(){
 const seeds=Array.from({length:16},(_,i)=>92801+i),shares=[.25,.5,.75],families=["dispersed","platoon4"],layouts=["shared","separate"],caps=[2,4,8],onsets=["green","red"];
 function tape(seed,share,family){
  let state=seed>>>0;
  const random=n=>{state=(Math.imul(state,1664525)+1013904223)>>>0;return Math.floor(state/4294967296*n)};
  const labels=Array.from({length:48},(_,i)=>i<48*share?"L":"S");
  for(let i=47;i>0;i--){const j=random(i+1);[labels[i],labels[j]]=[labels[j],labels[i]]}
  return labels.map((m,id)=>({id,m,t:family==="dispersed"?id*4+random(4):Math.floor(id/4)*16+random(2)})).sort((a,b)=>a.t-b.t||a.id-b.id);
 }
 function simulate(input,layout,cap,onset,period){
  let q=[],l=[],s=[],receiver=[],index=0,exits=0,stockCost=0,blocked=0;
  const by={L:[],S:[]};
  for(let t=0;t<1000;t++){
   const green=(t%period<period/2)===(onset==="green");
   if(green&&t%2===0&&receiver.length){const v=receiver.shift();by[v.m].push(t-v.t);exits++}
   const move=t%24<12?"L":"S";
   const source=layout==="shared"?q:move==="L"?l:s;
   if(source.length&&source[0].m===move){
    if(receiver.length<cap)receiver.push(source.shift());else blocked++;
   }
   while(index<input.length&&input[index].t===t){const v=input[index++];(layout==="shared"?q:v.m==="L"?l:s).push(v)}
   const stock=q.length+l.length+s.length+receiver.length;
   if(stock!==index-exits||receiver.length>cap)throw Error("conservation");
   stockCost+=stock;
   if(index===input.length&&stock===0){
    const total=by.L.concat(by.S).reduce((a,b)=>a+b,0);
    if(total!==stockCost||exits!==48)throw Error("per-ID cost identity");
    return {cost:stockCost,blocked,clearance:t,L:{sum:by.L.reduce((a,b)=>a+b,0),n:by.L.length,max:Math.max(...by.L)},S:{sum:by.S.reduce((a,b)=>a+b,0),n:by.S.length,max:Math.max(...by.S)}};
   }
  }
  throw Error("uncleared tape");
 }
 const rows=[];
 for(const seed of seeds)for(const share of shares)for(const family of families){
  const input=tape(seed,share,family);
  if(input.filter(v=>v.m==="L").length!==48*share)throw Error("share");
  for(const layout of layouts)for(const cap of caps)for(const onset of onsets){
   const a=simulate(input,layout,cap,onset,30),b=simulate(input,layout,cap,onset,60);
   rows.push({seed,share,family,layout,cap,onset,a,b,d:a.cost-b.cost,choice:onset==="red"&&share===.75?60:30});
  }
 }
 const summarize=rows=>{
  const reg=r=>({fixed30:Math.max(r.d,0),fixed60:Math.max(-r.d,0),frozen:r.choice===30?Math.max(r.d,0):Math.max(-r.d,0)});
  const m={};for(const key of ["fixed30","fixed60","frozen"]){const z=rows.map(r=>reg(r)[key]);m[key]={regret:z.reduce((s,x)=>s+x,0),correct:z.filter(x=>x===0).length,worst:Math.max(...z)}}
  const blocks=seeds.map(seed=>{const z=rows.filter(r=>r.seed===seed);return {seed,delta:z.reduce((s,r)=>s+reg(r).frozen-reg(r).fixed30,0)}});
  return {n:rows.length,win30:rows.filter(r=>r.d<0).length,win60:rows.filter(r=>r.d>0).length,ties:rows.filter(r=>r.d===0).length,metrics:m,beatsBoth:m.frozen.regret<Math.min(m.fixed30.regret,m.fixed60.regret),blocks};
 };
 if(rows.length!==1152)throw Error("cohort");
 return {status:"NEW_OFFLINE_SIMPLIFIED_MODEL_NOT_T2_PARITY",pairs:rows.length,arms:rows.length*2,tapes:96,seedBlocks:16,overall:summarize(rows),byLayoutCapacity:layouts.flatMap(layout=>caps.map(cap=>({layout,cap,...summarize(rows.filter(r=>r.layout===layout&&r.cap===cap))}))),byOnsetShare:onsets.flatMap(onset=>shares.map(share=>({onset,share,...summarize(rows.filter(r=>r.onset===onset&&r.share===share))}))),rows,scope:"All runs cleared; per-tick stock balance, receiver cap, and per-ID sum identity checked. New implementation, not isomorphic T2/SUMO/field evidence."};
}
console.log(JSON.stringify(experiment(),null,2));

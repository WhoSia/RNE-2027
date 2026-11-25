// Abstract periodic CTM mathematical verification.
function run(){
 const states=[];for(let a of [0,2,4,6])for(let b of [0,2,4,6])for(let c of [0,2,4,6])for(let d of [0,2,4,6])states.push([a,b,c,d]);
 const fds=[[1,.5],[.5,1],[.75,.5],[.5,.75]],eps=1e-9,dist=(a,b)=>a.reduce((s,x,i)=>s+Math.abs(x-b[i]),0),le=(a,b)=>a.every((x,i)=>x<=b[i]+eps),sum=a=>a.reduce((s,x)=>s+x,0);
 const result=fds.map(([v,w])=>{
  const C=6*v*w/(v+w),out=states.map(k=>{let f=k.map((x,i)=>Math.min(v*x,C,w*(6-k[(i+1)%4]))),z=k.map((x,i)=>x+f[(i+3)%4]-f[i]);if(z.some(x=>x<-eps||x>6+eps)||Math.abs(sum(z)-sum(k))>eps)throw Error("invariant");return z});
  let r={v,w,C,pairs:0,strict:0,equal:0,violations:0,comparable:0,monotonicityViolations:0,maxRatio:0};
  for(let i=0;i<states.length;i++)for(let j=0;j<states.length;j++){
   let a=dist(states[i],states[j]),b=dist(out[i],out[j]);r.pairs++;r[b>a+eps?"violations":b<a-eps?"strict":"equal"]++;if(a>0)r.maxRatio=Math.max(r.maxRatio,b/a);if(le(states[i],states[j])){r.comparable++;r.monotonicityViolations+=!le(out[i],out[j])}
  }if(r.violations||r.monotonicityViolations)throw Error("failed");return r
 });return {status:"FINITE_SYNTHETIC_CONTRACTION_CHECK",states:states.length,result};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};

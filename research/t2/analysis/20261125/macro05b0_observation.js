// Abstract periodic CTM, observation only.
function run(){
 const check=(x,m)=>{if(!x)throw Error(m)},eps=1e-9,N=4,fd=[[1,.5],[.5,1]],masks=Array.from({length:16},(_,m)=>Array.from({length:4},(_,i)=>m&(1<<i)?1:-1)),common=[[-1,-1,-1,-1],[1,1,1,1]],mean=a=>a.reduce((s,x)=>s+x,0)/a.length;
 const flux=(a,b,v,w)=>Math.min(v*a,2,w*(6-b)),local=(k,v,w)=>mean(k.map((x,i)=>flux(x,k[(i+1)%4],v,w))),hom=(k,v,w)=>flux(mean(k),mean(k),v,w),hist=(k,v,w)=>mean(k.flatMap((a,i)=>k.flatMap((b,j)=>i===j?[]:[flux(a,b,v,w)])));
 function step(k,v,w){let f=k.map((x,i)=>flux(x,k[(i+1)%4],v,w)),z=k.map((x,i)=>x+f[(i+3)%4]-f[i]);check(z.every(x=>x>=-eps&&x<=6+eps)&&Math.abs(mean(z)-mean(k))<eps,"conservation");return z}
 function trajectory(k,v,w){let z=[k];for(let t=0;t<8;t++)z.push(step(z[t],v,w));return z}
 const stats={},add=(key,e)=>{let a=stats[key]??(stats[key]={n:0,signed:0,abs:0,sq:0,max:0});a.n++;a.signed+=e;a.abs+=Math.abs(e);a.sq+=e*e;a.max=Math.max(a.max,Math.abs(e))};
 function record(family,channel,method,t,e){for(let f of [family,"pooled"])for(let epoch of ["all",...(t<=2?["early"]:t>=6?["late"]:[])])add(`${f}/${channel}/${method}/${epoch}`,e)}
 let truth=0,forecasts=0,alternate=0,bounds=0,maxRatio=0;
 for(let a of [0,2,4,6])for(let b of [0,2,4,6])for(let c of [0,2,4,6])for(let d of [0,2,4,6])for(let fi=0;fi<2;fi++){
  let k=[a,b,c,d],[v,w]=fd[fi],family=`fd${fi}`,z=trajectory(k,v,w),other=trajectory(k,...fd[1-fi]);truth++;alternate++;
  z.forEach((x,t)=>{let y=local(x,v,w);check(hom(x,v,w)>=y-eps,"homogeneous upper bound");for(let [m,p] of [["local",y],["mean",hom(x,v,w)],["hist",hist(x,v,w)],["alternate",local(other[t],...fd[1-fi])]])record(family,"exact",m,t,p-y)});
  for(let [channel,ms] of [["independent",masks],["common",common]])for(let mask of ms){
   let obs=k=>k.map((x,i)=>Math.max(0,Math.min(6,x+mask[i]))),pred=trajectory(obs(k),v,w);forecasts++;
   z.forEach((x,t)=>{let y=local(x,v,w),o=obs(x),e=local(o,v,w)-y,B=(v+w)*mean(x.map((n,i)=>Math.abs(n-o[i])));check(Math.abs(e)<=B+eps,"Lipschitz");bounds++;if(B>0)maxRatio=Math.max(maxRatio,Math.abs(e)/B);for(let [m,p] of [["local",local(o,v,w)],["mean",hom(o,v,w)],["hist",hist(o,v,w)],["forecast",local(pred[t],v,w)]])record(family,channel,m,t,p-y)});
  }
 }
 check(truth===512&&forecasts===9216&&alternate===512&&bounds===82944,"denominator");
 for(let a of Object.values(stats)){a.bias=a.signed/a.n;a.MAE=a.abs/a.n;a.RMSE=Math.sqrt(a.sq/a.n)}
 return {status:"EXECUTED_SYNTHETIC_PERIODIC_CTM",truth,forecasts,alternate,bounds,maxRatio,stats};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};

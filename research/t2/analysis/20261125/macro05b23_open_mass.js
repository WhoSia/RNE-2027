// Offline dimensionless model.
function run(){
 const assert=(b,m)=>{if(!b)throw Error(m)},eps=1e-8,K=6,N=4,fd=[[.75,.5],[1,.25]],sum=a=>a.reduce((s,x)=>s+x,0),l1=(a,b)=>sum(a.map((x,i)=>Math.abs(x-b[i]))),le=(a,b)=>a.every((x,i)=>x<=b[i]+eps),sq=(a,b)=>sum(a.map((x,i)=>(x-b[i])**2))/4,clip=x=>Math.max(0,Math.min(6,x));
 const states=vals=>vals.flatMap(a=>vals.flatMap(b=>vals.flatMap(c=>vals.map(d=>[a,b,c,d]))));
 function model(v,w){const C=K*v*w/(v+w),S=x=>Math.min(v*x,C),R=x=>Math.min(C,w*(K-x)),f=(a,b)=>Math.min(S(a),R(b)),meanFlux=x=>sum(x.slice(0,3).map((a,i)=>f(a,x[i+1])))/3;
 function step(x,u,d){let F=[Math.min(u,R(x[0])),...x.slice(0,3).map((a,i)=>f(a,x[i+1])),Math.min(S(x[3]),d)],z=x.map((a,i)=>a+F[i]-F[i+1]);assert(z.every(a=>a>=-eps&&a<=K+eps)&&Math.abs(sum(z)-sum(x)-F[0]+F[4])<eps,"balance");return {z,in:F[0],out:F[4]}}
 return {C,step,meanFlux}}
 const b2=[];
 for(let [v,w] of fd){let {C,step}=model(v,w),xs=states([0,2,4,6]),bc=[0,C/2,C].flatMap(u=>[0,C/2,C].map(d=>[u,d])),out=bc.map(([u,d])=>xs.map(x=>step(x,u,d).z)),r={v,w,C,statePairs:0,strict:0,tie:0,violations:0,comparable:0,monotonicityViolations:0,boundaryPairs:0,boundaryViolations:0,maxRatio:0};
 for(let k=0;k<bc.length;k++)for(let i=0;i<xs.length;i++)for(let j=0;j<xs.length;j++){let a=l1(xs[i],xs[j]),b=l1(out[k][i],out[k][j]);r.statePairs++;r[b>a+eps?"violations":b<a-eps?"strict":"tie"]++;if(le(xs[i],xs[j])){r.comparable++;r.monotonicityViolations+=!le(out[k][i],out[k][j])}if(a)r.maxRatio=Math.max(r.maxRatio,b/a)}
 for(let i=0;i<xs.length;i++)for(let a=0;a<9;a++)for(let b=0;b<9;b++){r.boundaryPairs++;r.boundaryViolations+=l1(out[a][i],out[b][i])>l1(bc[a],bc[b])+eps}
 assert(!r.violations&&!r.monotonicityViolations&&!r.boundaryViolations,"bounds");b2.push(r)}
 const masks=Array.from({length:16},(_,m)=>Array.from({length:4},(_,i)=>m&(1<<i)?1:-1)),stats={},witness={},project=(y,M)=>{let lo=-6,hi=6;for(let k=0;k<48;k++){let mid=(lo+hi)/2;if(sum(y.map(x=>clip(x+mid)))<M)lo=mid;else hi=mid}let z=y.map(x=>clip(x+(lo+hi)/2));assert(Math.abs(sum(z)-M)<eps,"projection");return z};
 const fresh=()=>({n:0,densitySE:0,fluxSE:0,densityBetter:0,densityTie:0,densityWorse:0,fluxBetter:0,fluxTie:0,fluxWorse:0,maxMassResidual:0}),cmp=(a,b)=>a<b-eps?"Better":a>b+eps?"Worse":"Tie";
 let truth=0,snapshots=0;
 for(let [v,w] of fd){let {C,step,meanFlux}=model(v,w);for(let x0 of states([1,3,5]))for(let h=0;h<3;h++){let x=x0.slice(),M=sum(x);truth++;for(let t=0;t<=12;t++){assert(Math.abs(M-sum(x))<eps,"truth ledger");for(let [ch,ms] of [["cellwise",masks],["common",[masks[0],masks[15]]]])for(let m of ms){let y=x.map((a,i)=>clip(a+m[i])),D=sq(y,x),F=(meanFlux(y)-meanFlux(x))**2;snapshots++;for(let [label,z,target] of [["raw",y,sum(y)],...[-1,0,1].map(b=>{let target=Math.max(0,Math.min(24,M+b*.125*t));return [b===0?"exact":b<0?"negative":"positive",project(y,target),target]})]){let s=stats[`${ch}/${label}`]??(stats[`${ch}/${label}`]=fresh()),d=sq(z,x),f=(meanFlux(z)-meanFlux(x))**2;s.n++;s.densitySE+=d;s.fluxSE+=f;s["density"+cmp(d,D)]++;s["flux"+cmp(f,F)]++;s.maxMassResidual=Math.max(s.maxMassResidual,Math.abs(sum(z)-target));if(label==="exact"){assert(d<=D+eps,"projection inequality");if(f>F+eps&&!witness[ch])witness[ch]={v,w,x0,h,t,x,y,z,D,d,F,f,rawFlux:meanFlux(y),projectedFlux:meanFlux(z),trueFlux:meanFlux(x)}}}}
 if(t<12){let u=h===2&&t>=6?0:C,d=h===1&&t<4?0:h===2&&t<6?C/2:C,a=step(x,u,d);M+=a.in-a.out;x=a.z}}}}
 assert(truth===486&&snapshots===113724,"denom");for(let s of Object.values(stats)){s.densityRMSE=Math.sqrt(s.densitySE/s.n);s.fluxRMSE=Math.sqrt(s.fluxSE/s.n)}
 return {status:"DIMENSIONLESS_OFFLINE_OPEN_CTM",b2,b3:{truth,snapshots,projections:3*snapshots,stats,witness}};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};

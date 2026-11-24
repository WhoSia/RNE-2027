// Offline dimensionless network. Initial run failed transfer check; clamp only tiny negative roundoff, bounded and audited.
function run(){
 const eps=1e-7,check=(b,m)=>{if(!b)throw Error(m)};
 const sum=a=>a[0]+a[1],S=a=>Math.max(0,Math.min(sum(a),2)),R=a=>Math.min(2,Math.max(0,(6-sum(a))/2));
 function simulate(input,share,bottleneck,sink,relaxed){
  let n=Array.from({length:10},()=>[0,0]),ext=[0,0],A=[0,0],Z=[0,0],J=[0,0],blocked=0,peak=0,peakExternal=0,divergence=0,roundoff=0;
  for(let t=0;t<128;t++){
   let next=n.map(a=>a.slice()),e=ext.slice(),out=[0,0];
   const transfer=(i,j,f)=>{let from=i===-1?ext:n[i],stock=sum(from);check(f>=-eps&&f<=stock+eps,`transfer ${i} ${j} ${f} ${stock}`);if(stock<=0)return;for(let k=0;k<2;k++){let v=f*(from[k]/stock);if(i===-1)e[k]-=v;else next[i][k]-=v;if(j===-1)out[k]+=v;else next[j][k]+=v}};
   transfer(-1,0,Math.min(sum(ext),R(n[0])));
   for(const [i,j] of [[0,1],[2,3],[4,5],[5,6],[6,7],[8,9]])transfer(i,j,Math.min(S(n[i]),R(n[j])));
   let u=n[1],total=sum(u),d=total>0?u.map(v=>S(u)*(v/total)):[0,0],r=[R(n[2]),R(n[4])];
   let scale=Math.min(1,...d.map((v,i)=>v>0?r[i]/v:1)),f=d.map((v,i)=>relaxed?Math.min(v,r[i]):v*scale);
   for(let k=0;k<2;k++){next[1][k]-=f[k];next[k===0?2:4][k]+=f[k]}
   check(sum(f)<=S(u)+eps&&f.every((v,i)=>v<=r[i]+eps),"diverge");
   blocked+=sum(d)-sum(f);divergence+=sum(f);
   const capA=bottleneck===1&&t>=4&&t<16?.25:bottleneck===2&&t>=8&&t<24?.5:2;
   let demand=[Math.min(S(n[3]),capA),S(n[7])],tot=sum(demand),merge=tot>0?Math.min(1,R(n[8])/tot):0;
   transfer(3,8,demand[0]*merge);transfer(7,8,demand[1]*merge);
   check(tot*merge<=R(n[8])+eps,"merge");
   const cap=sink===1&&t>=8&&t<16?0:sink===2&&t<24?1:2;
   transfer(9,-1,Math.min(S(n[9]),cap));
   let rate=input===0?2*(t<12):input===1?2*(t<4||t>=8&&t<12||t>=16&&t<20):+(t<24);
   let arrivals=[rate*share,rate*(1-share)];
   for(let k=0;k<2;k++){e[k]+=arrivals[k];A[k]+=arrivals[k];Z[k]+=out[k]}
   for(const v of [e,...next])for(let k=0;k<2;k++){check(Number.isFinite(v[k])&&v[k]>=-1e-10,"negative stock");if(v[k]<0){roundoff-=v[k];v[k]=0}}
   for(let k=0;k<2;k++){let stock=e[k]+next.reduce((s,v)=>s+v[k],0);check(Math.abs(stock+Z[k]-A[k])<eps,"commodity");J[k]+=stock}
   check(next.every(v=>sum(v)<=6+eps),"storage");
   check([2,3].every(i=>Math.abs(next[i][1])<eps)&&[4,5,6,7].every(i=>Math.abs(next[i][0])<eps),"route");
   n=next;ext=e;peak=Math.max(peak,n.reduce((s,v)=>s+sum(v),0));peakExternal=Math.max(peakExternal,sum(ext));
  }
  let terminal=sum(ext)+n.reduce((s,v)=>s+sum(v),0);check(Math.abs(sum(A)-24)<eps&&terminal<eps&&roundoff<1e-9,"clearance");
  return {J:sum(J),JA:J[0],JB:J[1],blocked,peak,peakExternal,divergence,terminal,roundoff};
 }
 let rows=[],stat={n:0,fifo:0,relaxed:0,fifoA:0,relaxedA:0,fifoB:0,relaxedB:0,better:0,tie:0,worse:0,blockedFifo:0,blockedRelaxed:0,maxGain:0,maxHarm:0,harmWitness:null,gainWitness:null,maxRoundoff:0};
 for(let i=0;i<3;i++)for(let share of [.25,.5,.75])for(let b=0;b<3;b++)for(let s=0;s<3;s++){
  let a=simulate(i,share,b,s,false),r=simulate(i,share,b,s,true),d=r.J-a.J,ctx={input:i,share,bottleneck:b,sink:s};rows.push({...ctx,fifo:a,relaxed:r});stat.n++;stat.fifo+=a.J;stat.relaxed+=r.J;stat.fifoA+=a.JA;stat.relaxedA+=r.JA;stat.fifoB+=a.JB;stat.relaxedB+=r.JB;stat.blockedFifo+=a.blocked;stat.blockedRelaxed+=r.blocked;stat[d< -eps?"better":d>eps?"worse":"tie"]++;stat.maxRoundoff=Math.max(stat.maxRoundoff,a.roundoff,r.roundoff);if(-d>stat.maxGain){stat.maxGain=-d;stat.gainWitness=ctx}if(d>stat.maxHarm){stat.maxHarm=d;stat.harmWitness=ctx}
 }
 return {status:"EXECUTED_JS_ISOLATE_DIMENSIONLESS_NETWORK",worlds:81,arms:162,stats:stat,rows};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};

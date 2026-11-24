// BE01: finite same-OD congestion game, not field model.
function run(){
 const check=(p,m)=>{if(!p)throw Error(m)};
 const eps=[0,1,3],st=Object.fromEntries(eps.map(e=>[e,{worlds:0,equilibria:0,maxRatio:0,maxWitness:null,asyncRuns:0,asyncMaxSteps:0,syncRuns:0,syncFixed:0,syncCycles:0,maxCycleRatio:0,cycleWitness:null,worseWorstEq:0}]));
 let worlds=0,externality=0,witness=null,edges=0;
 for(const N of [8,12,24])for(const a of [1,5])for(const c of [1,5])for(const b of [0,1,2])for(const d of [0,1,2]){
 if(!b&&!d)continue;worlds++;const param={N,a,b,c,d};
 const A=n=>a+b*n,B=n=>c+d*(N-n),C=n=>n*A(n)+(N-n)*B(n);
 const potential=n=>a*n+b*n*(n+1)/2+c*(N-n)+d*(N-n)*(N-n+1)/2;
 const states=Array.from({length:N+1},(_,i)=>i),opt=Math.min(...states.map(C));
 const gainA=n=>n>0?A(n)-B(n-1):-Infinity,gainB=n=>n<N?B(n)-A(n+1):-Infinity;
 for(const n of states)for(const [next,gain] of [[n-1,gainA(n)],[n+1,gainB(n)]]){
 if(gain>0){edges++;check(potential(n)-potential(next)===gain,"potential");if(C(next)>C(n)){externality++;if(!witness)witness={...param,n,next,gain,costBefore:C(n),costAfter:C(next)}}}
 }
 let previous=null;
 for(const e of eps){
 const s=st[e];s.worlds++;
 const eq=states.filter(n=>gainA(n)<=e&&gainB(n)<=e);check(eq.length,"equilibrium");
 const worst=Math.max(...eq.map(C));s.equilibria+=eq.length;const ratio=worst/opt;
 if(previous!==null){check(worst>=previous,"nested equilibrium");s.worseWorstEq+=+(worst>previous)}previous=worst;
 if(ratio>s.maxRatio){s.maxRatio=ratio;s.maxWitness={...param,epsilon:e,equilibria:eq,opt,worst}}
 for(const start of states){
  s.asyncRuns++;let n=start,k=0;
  while(gainA(n)>e||gainB(n)>e){const next=gainA(n)>e?n-1:n+1;check(potential(next)<potential(n),"strict potential");n=next;k++;check(k<=N,"finite path")}
  check(eq.includes(n),"async eq");s.asyncMaxSteps=Math.max(s.asyncMaxSteps,k);
  s.syncRuns++;n=start;const seen=new Map(),path=[];
  while(!seen.has(n)){seen.set(n,path.length);path.push(n);n=n-(gainA(n)>e?n:0)+(gainB(n)>e?N-n:0);check(n>=0&&n<=N,"state")}
  const cyc=path.slice(seen.get(n));if(cyc.length===1){s.syncFixed++;check(eq.includes(n),"sync eq")}else{s.syncCycles++;const cost=cyc.reduce((a,n)=>a+C(n),0)/cyc.length,rr=cost/opt;if(rr>s.maxCycleRatio){s.maxCycleRatio=rr;s.cycleWitness={...param,epsilon:e,start,cycle:cyc,cost,opt}}}
 }
 }
 }
 return {status:"EXECUTED_JS_ISOLATE_TOY_CONGESTION_GAME_NOT_EMPIRICAL",worlds,strictImprovementEdges:edges,externalityEdges:externality,witness,epsilon:st};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};

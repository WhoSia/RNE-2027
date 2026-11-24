// P158 total resource cap preserving, finite synthetic experiment.
function run(){
 const assert=(x,m)=>{if(!x)throw Error(m)};
 function sim(tape,P,shared,partition,reuse){
  const q=[],qs=[],ql=[],receiver=[];let p=0,a=0,z=0,J=0,stranded=0;
  for(let t=0;t<160;t++){
   const g=t<8?(t%4<2?"S":"L"):"BBSSBBLL"[(t+2)%8],exit=receiver.length>0&&t%4<2,exitLabel=exit?receiver[0]:null;
   const immediate=t>=8&&reuse,cap=m=>partition?1-receiver.filter(v=>v===m).length+(immediate&&exitLabel===m?1:0):2-receiver.length+(immediate&&exit?1:0);
   const hs=shared?q[0]==="S":qs.length>0,hl=shared?q[0]==="L":ql.length>0,enter=hl&&p<P;
   const ws=hs&&g!=="L",wl=p>0&&g!=="S";
   const m=ws&&cap("S")>0?"S":wl&&cap("L")>0?"L":null;
   if(partition&&m===null&&(ws||wl)&&2-receiver.length+(immediate&&exit?1:0)>0)stranded++;
   assert(!(enter&&shared&&m==="S"),"head conflict");
   if(exit){receiver.shift();z++}
   if(m==="S"){(shared?q:qs).shift();receiver.push("S")}
   if(m==="L"){p--;receiver.push("L")}
   if(enter){(shared?q:ql).shift();p++}
   if(tape[t]){const v=tape[t];(shared?q:v==="S"?qs:ql).push(v);a++}
   const n=q.length+qs.length+ql.length+p+receiver.length;J+=n;
   assert(n+z===a&&p>=0&&p<=P&&receiver.length<=2,"conservation");
   assert(!partition||["S","L"].every(m=>receiver.filter(v=>v===m).length<=1),"partition");
   assert(!m||g==="B"||g===m,"red");
  }
  assert(a===z&&a===Object.keys(tape).length,"clearance");return {J,stranded};
 }
 const tape=(n,m)=>Object.fromEntries(Array.from({length:n},(_,i)=>[2*i,m&(1<<i)?"L":"S"]));
 const A=[[82,1],[82,2],[83,1],[83,2],[86,2],[87,2]].map(([m,P])=>({id:m+":"+P,tape:tape(7,m),P}));
 const B=Array.from({length:128},(_,m)=>({id:m,tape:Object.fromEntries(Object.entries(tape(7,82)).filter(([t])=>m&(1<<(+t/2)))),P:1}));
 const C=Array.from({length:128},(_,m)=>({id:m,tape:tape(7,m),P:1}));
 const tops=[true,false].flatMap(shared=>[false,true].map(partition=>({shared,partition})));
 function cohort(entries){
  const results=tops.map(top=>({top,decrease:0,tie:0,increase:0,min:null,witnesses:[],strandedOld:0,strandedReuse:0}));
  const contrasts=tops.slice(1).map(top=>({top,old:[0,0,0],reuse:[0,0,0]}));
  for(const e of entries){
   const costs=tops.map(({shared,partition})=>[false,true].map(reuse=>sim(e.tape,e.P,shared,partition,reuse)));
   for(let i=0;i<tops.length;i++){
    const [old,reuse]=costs[i],r=results[i],d=reuse.J-old.J;r.strandedOld+=old.stranded;r.strandedReuse+=reuse.stranded;
    if(d<0)r.decrease++;else if(d===0)r.tie++;else{r.increase++;const w={id:e.id,n:Object.keys(e.tape).length,P:e.P,old:old.J,reuse:reuse.J};r.witnesses.push(w);if(!r.min||w.n<r.min.n)r.min=w}
    if(i>0)for(let k=0;k<2;k++){const x=costs[i][k].J-costs[0][k].J;contrasts[i-1][k?"reuse":"old"][Math.sign(x)+1]++}
   }
  }
  return {results,contrasts};
 }
 const a=cohort(A),b=cohort(B),c=cohort(C);
 assert(a.results[0].increase===6&&a.results[0].witnesses.every(w=>w.old===37&&w.reuse===40),"old witness");
 assert(b.results[0].increase===2&&b.results[0].min.n===6,"deletion baseline");
 return {status:"EXECUTED_JS_ISOLATE_SYNTHETIC_RESOURCE_CAPS",arms:2096,A:a,B:b,C:c};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};

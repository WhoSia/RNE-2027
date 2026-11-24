// P155 fixed topology factorial; node p155_mechanism_factorial.js
function run(){
 const assert=(x,m)=>{if(!x)throw Error(m)};
 const gates="BBSSBBLL";
 function sim(tape,P,D,shared,staged,common,reuse){
  const q=[],s=[],l=[];let p=0,dS=0,dL=0,a=0,z=0,j=0;
  for(let t=0;t<160;t++){
   const gate=t<8?(t%4<2?"S":"L"):gates[(t+2)%8];
   const exS=+(dS>0&&t%4<2),exL=+(dL>0&&t%4<2);
   const availS=D-dS+ +(t>=8&&reuse)*exS,availL=common?availS:D-dL+ +(t>=8&&reuse)*exL;
   const headS=shared?q[0]==="S":s.length>0,headL=shared?q[0]==="L":l.length>0;
   const admit=staged&&headL&&p<P;
   let moveS=headS&&gate!=="L"&&availS>0,moveL=(staged?p>0:headL)&&gate!=="S"&&availL>0;
   if(common&&moveS&&moveL)moveL=false;
   assert(!(shared&&moveS&&admit)&&!(shared&&!staged&&moveS&&moveL),"head conflict");
   dS-=exS;dL-=exL;z+=exS+exL;
   if(moveS){(shared?q:s).shift();dS++}
   if(moveL){if(staged)p--;else (shared?q:l).shift();if(common)dS++;else dL++}
   if(admit){(shared?q:l).shift();p++}
   if(tape[t]){const v=tape[t];(shared?q:v==="S"?s:l).push(v);a++}
   const n=q.length+s.length+l.length+p+dS+dL;j+=n;
   assert(a-z===n&&p>=0&&p<=P&&dS>=0&&dS<=D&&dL>=0&&dL<=D,"stock");
  }
  assert(a===Object.keys(tape).length&&a===z,"clearance");
  return j;
 }
 const tape=(n,mask)=>Object.fromEntries(Array.from({length:n},(_,i)=>[2*i,mask&(1<<i)?"L":"S"]));
 const tops=[];for(const shared of [true,false])for(const staged of [true,false])for(const common of [true,false])tops.push({shared,staged,common});
 function pair(t,P,D,top){return [false,true].map(r=>sim(t,P,D,top.shared,top.staged,top.common,r))}
 function summarise(entries,top){let decrease=0,tie=0,increase=0,min=null;const witnesses=[];for(const e of entries){const [old,reuse]=pair(e.tape,e.P,e.D,top);if(reuse<old)decrease++;else if(reuse===old)tie++;else{increase++;const w={id:e.id,n:Object.keys(e.tape).length,tape:e.tape,P:e.P,D:e.D,old,reuse};witnesses.push(w);if(!min||w.n<min.n)min=w}}return {top,decrease,tie,increase,min,witnesses}}
 const A=[[82,1],[82,2],[83,1],[83,2],[86,2],[87,2]].map(([m,P])=>({id:m+":"+P,tape:tape(7,m),P,D:2}));
 const B=Array.from({length:128},(_,m)=>({id:m,tape:Object.fromEntries(Object.entries(tape(7,82)).filter(([t])=>m&(1<<(+t/2)))),P:1,D:2}));
 const C=[];for(let n=1;n<=7;n++)for(let m=0;m<2**n;m++)C.push({id:n+":"+m,tape:tape(n,m),P:1,D:2});
 const a=tops.map(t=>summarise(A,t)),b=tops.map(t=>summarise(B,t)),c=summarise(C,tops[0]);
 assert(a[0].increase===6&&a[0].witnesses.every(w=>w.old===37&&w.reuse===40),"P154 reproduction");
 return {status:"EXECUTED_JS_ISOLATE_SYNTHETIC",arms:96+2048+508,A:a,B:b,C:c};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};

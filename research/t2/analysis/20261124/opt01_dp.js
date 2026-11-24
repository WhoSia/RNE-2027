// OPT01: exact offline abstract finite-horizon scheduling.
function run(){
 const pol=[3,4,5].flatMap(g=>[0,2,4,6].map(o=>[g,o])),clocks=[[0,1,3,5,8,10],[0,2,4,7,9,13]];
 const assert=(b,m)=>{if(!b)throw Error(m)};
 function block(state,t,g,o,P,R,tape){
  let [q,p,r,Y,Z]=state;let J=0;
  for(let k=t;k<t+8;k++){
   const gs=k%8<g,ds=(k+o)%8<4,x=+(gs&&q[0]==="S"&&r<R),a=+(q[0]==="L"&&p<P),y=+(!gs&&p>0),z=+(ds&&r>0);
   q=q.slice(x+a)+(tape[k]||"");p+=a-y;r+=x-z;Y+=y;Z+=z;J+=q.length+p+r;
   assert(p>=0&&p<=P&&r>=0&&r<=R,"capacity");
   assert(q.length+p+r+Y+Z===Object.keys(tape).filter(t=>+t<=k).length,"conservation");
  }return {state:[q,p,r,Y,Z],J};
 }
 const fresh=()=>({n:0,fixed:0,dynamic:0,gain:0,strict:0,tie:0,maxGain:0,peakWidth:0,transitions:0,witness:null});
 const groups={all:fresh(),A:fresh(),B:fresh()};
 for(let mask=0;mask<64;mask++)for(let c=0;c<2;c++)for(const P of [1,2])for(const R of [1,2]){
  const tape=Object.fromEntries(clocks[c].map((t,i)=>[t,mask&(1<<i)?"L":"S"]));const pre=block(["",0,0,0,0],0,4,0,P,R,tape);
  let fixed=Infinity,best=null,peak=0,transitions=0;
  for(const [g,o] of pol){let s=pre.state,J=pre.J;for(let t=8;t<96;t+=8){const b=block(s,t,g,o,P,R,tape);s=b.state;J+=b.J}assert(s[3]+s[4]===6,"fixed clear");fixed=Math.min(fixed,J)}
  for(const o of [0,2,4,6]){
   let layer=new Map([[JSON.stringify(pre.state),{state:pre.state,J:pre.J,path:""}]]);
   for(let t=8;t<96;t+=8){const next=new Map();for(const entry of layer.values())for(const g of [3,4,5]){
    const b=block(entry.state,t,g,o,P,R,tape),key=JSON.stringify(b.state),J=entry.J+b.J,path=entry.path+g,old=next.get(key);transitions++;
    if(!old||J<old.J||(J===old.J&&path<old.path))next.set(key,{state:b.state,J,path});
   }layer=next;peak=Math.max(peak,layer.size)}
   for(const e of layer.values())if(e.state[3]+e.state[4]===6&&(!best||e.J<best.J||(e.J===best.J&&(o<best.o||(o===best.o&&e.path<best.path)))))best={...e,o};
  }
  assert(best&&best.J<=fixed,"DP dominance");let s=pre.state,J=pre.J;for(let i=0;i<best.path.length;i++){let b=block(s,8+8*i,+best.path[i],best.o,P,R,tape);s=b.state;J+=b.J}assert(J===best.J&&s[3]+s[4]===6,"replay");
  const gain=fixed-best.J;
  for(const k of ["all",c===0?"A":"B"]){const z=groups[k];z.n++;z.fixed+=fixed;z.dynamic+=best.J;z.gain+=gain;z.strict+=gain>0;z.tie+=gain===0;z.peakWidth=Math.max(z.peakWidth,peak);z.transitions+=transitions;if(gain>z.maxGain){z.maxGain=gain;z.witness={mask,clock:c,P,R,fixed,dynamic:best.J,path:best.path,o:best.o}}}
 }
 assert(groups.all.n===512,"denom");return {status:"EXECUTED_JS_ISOLATE_OFFLINE_FINITE_FAMILY",groups};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};

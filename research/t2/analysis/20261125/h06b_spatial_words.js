// Abstract finite ring; no physical control.
function run(){
 const fds=[[15,10,36],[20,5,24]],sizes=[6,8,10],results=[];
 for(const N of sizes){
  const groups=Array.from({length:6},()=>new Map());let states=0;
  for(let id=0;id<3**N;id++){
   let v=id,a=[];for(let i=0;i<N;i++){a.push(v%3);v=Math.floor(v/3)}
   let values=[];
   for(const [V,W,C] of fds){let x=a.map(z=>3*z),D=1;for(let t=0;t<3;t++){
     let F=x.map((z,i)=>Math.min(V*z,C*D,W*(6*D-x[(i+1)%N])));values.push(F.reduce((s,z)=>s+z,0));
     let y=x.map((z,i)=>20*z+F[(i+N-1)%N]-F[i]);if(y.some(z=>z<0||z>120*D)||y.reduce((s,z)=>s+z,0)!==20*x.reduce((s,z)=>s+z,0))throw Error("conservation");x=y;D*=20;
   }}
   for(let k=1;k<=6;k++){
    let codes=a.map((_,i)=>{let z=0;for(let j=0;j<k;j++)z=3*z+a[(i+j)%N];return z}),key=codes.sort((x,y)=>x-y).join(",");
    let g=groups[k-1].get(key);if(!g){g={n:0,m:Array(6).fill(0),ss:Array(6).fill(0),min:values.slice(),max:values.slice(),lo:Array(6).fill(id),hi:Array(6).fill(id)};groups[k-1].set(key,g)}
    g.n++;values.forEach((z,i)=>{let d=z-g.m[i];g.m[i]+=d/g.n;g.ss[i]+=d*(z-g.m[i]);if(z<g.min[i]){g.min[i]=z;g.lo[i]=id}if(z>g.max[i]){g.max[i]=z;g.hi[i]=id}});
   }states++;
  }
  const decode=id=>Array.from({length:N},(_,i)=>3*(Math.floor(id/3**i)%3));
  let entries=groups.map((m,k)=>{
    let out=Array.from({length:6},(_,i)=>({fd:Math.floor(i/3),t:i%3,floor:0,ambiguousGroups:0,ambiguousStates:0,maxRange:0,witness:null}));
    for(let g of m.values())for(let i=0;i<6;i++){let o=out[i],den=N*20**(1+i%3),gap=g.max[i]-g.min[i];o.floor+=g.ss[i]/(den*den*states);if(gap){o.ambiguousGroups++;o.ambiguousStates+=g.n}if(gap/den>o.maxRange){o.maxRange=gap/den;o.witness={lo:decode(g.lo[i]),hi:decode(g.hi[i]),fluxLo:g.min[i]/den,fluxHi:g.max[i]/den}}}
    for(let o of out)if(k+1>=2*o.t+2&&o.ambiguousGroups)throw Error("locality violation");
    return {k:k+1,groups:m.size,singletons:[...m.values()].filter(g=>g.n===1).length,targets:out}
  });
  for(let i=1;i<6;i++)for(let j=0;j<6;j++)if(entries[i].targets[j].floor>entries[i-1].targets[j].floor+1e-12)throw Error("nested loss");
  results.push({N,states,entries});
 }
 return {status:"EXHAUSTIVE_SYNTHETIC_RING",results,states:results.reduce((s,r)=>s+r.states,0),fdStateTrajectories:2*results.reduce((s,r)=>s+r.states,0)};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};

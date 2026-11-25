/* Exploratory nested-noise and interval audit; node h04a_h08a_nested_audit.js */
function nestedAudit(){
 const X=[];for(let i=0;i<2401;i++){let j=i;X.push(Array.from({length:4},()=>{const v=j%7;j=Math.floor(j/7);return v;}));}
 const F=x=>[0,1,2].map(i=>Math.min(x[i],3,6-x[i+1])).reduce((a,b)=>a+b,0);
 const binom=n=>{let a=[1];for(let i=0;i<n;i++)a=[...a,0].map((v,j)=>v+(a[j-1]||0));return a;};
 const H04=[];
 for(const mode of ["local","common"]){
   let prev=-1;
   for(const n of [0,1,2,4,8]){
     const a=new Map(), weights=binom(n);let sumF2=0,N=0;
     for(const x of X)for(let m=0;m<(mode==="local"?16:2);m++){
       const y=x.map((v,j)=>Math.min(6,Math.max(0,v+((mode==="local"?(m>>j)&1:m)?1:-1))));const f=F(x),M=x.reduce((s,v)=>s+v,0);
       for(let k=0;k<=n;k++){
         const w=weights[k], key=[...y,M+2*k-n].join(",");
         let t=a.get(key);if(!t){t=[0,0];a.set(key,t);}t[0]+=w;t[1]+=w*f;sumF2+=w*f*f;N+=w;
       }
     }
     let explained=0;for(const [w,s] of a.values())explained+=s*s/w;
     const mse=(sumF2-explained)/(9*N);
     if(mse<prev-1e-10)throw Error("nested noise violated");
     prev=mse;H04.push({mode,n,groups:a.size,weightedRows:N,mse});
   }
 }
 // independent set-interval audit of H08 with a different enumeration and costs
 const groups=new Map(), w=[];
 for(let n=0;n<625;n++){
   let j=n;const [qS,qL,cS,cL]=Array.from({length:4},()=>{let k=j%5;j=Math.floor(j/5);return k;});
   let costs=[[],[],[]];
   for(let a=0;a<=4;a++){
     let rs=qS,rl=qL;
     for(let i=0;i<a&&i<cS&&rs>0;i++)rs--;
     for(let i=0;i<4-a&&i<cL&&rl>0;i++)rl--;
     costs[0].push(rs+rl);costs[1].push(Math.max(rs,rl));costs[2].push(rl);
   }
   const opt=costs.map(c=>c.map((v,a)=>v===Math.min(...c)?a:-1).filter(a=>a>=0));
   if(opt.some(a=>a.length!==a.at(-1)-a[0]+1))throw Error("noninterval");
   const e=[Math.min(qS,cS),Math.min(qL,cL)];
   const key=e.join(",");
   if(!groups.has(key))groups.set(key,[]);
   const expected=[];for(let a=0;a<=4;a++)if(a>=Math.min(e[0],4-e[1])&&a<=Math.max(e[0],4-e[1]))expected.push(a);
   if(JSON.stringify(expected)!==JSON.stringify(opt[0]))throw Error("interval formula");
   groups.get(key).push(opt);w.push({qS,qL,cS,cL,e,opt});
 }
 let badMax=0,badTotal=0,badStates=0;
 for(const g of groups.values()){
   if(!g[0][0].some(a=>g.every(o=>o[0].includes(a))))badTotal++;
   if(!g[0][1].some(a=>g.every(o=>o[1].includes(a)))){badMax++;badStates+=g.length;}
 }
 return {H04,H08:{states:w.length,objectiveIntervals:w.length*3,totalFormula:w.length,badTotal,badMax,badStates}};
}
console.log(JSON.stringify(nestedAudit(),null,2));

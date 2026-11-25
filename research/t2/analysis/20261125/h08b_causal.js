/* H08B frozen protocol; node h08b_causal.js */
function h08b(){
 const events=[[0,0],[0,1],[1,0],[1,1]],actions=[0,1,2],objectives=["total","fair","terminal"],K=2;
 const worlds=[];for(let s=0;s<4;s++)for(let l=0;l<4;l++)for(let x=0;x<3;x++)for(let y=0;y<3;y++)worlds.push([s,l,x,y]);
 const reps={total:w=>[w[0]+w[1]],q:w=>w.slice(0,2),e:w=>[Math.min(w[0],K-w[2]),Math.min(w[1],K-w[3])],qe:w=>[...w.slice(0,2),Math.min(w[0],K-w[2]),Math.min(w[1],K-w[3])],qeO:w=>[...w.slice(0,2),Math.min(w[0],K-w[2]),Math.min(w[1],K-w[3]),w[2]+w[3]],full:w=>w};
 let transitions=0;
 function step(w,a,[arrival,exit],order){
   const q=w.slice(0,2),o=w.slice(2),slots=[a,2-a],before=w.reduce((x,y)=>x+y,0);let out=0;
   function drain(){if(o[exit]>0){o[exit]--;out++;}}
   if(order==="DS")drain();
   for(let i=0;i<2;i++){let v=Math.min(q[i],K-o[i],slots[i]);q[i]-=v;o[i]+=v;}
   const residual=q.slice();
   if(order==="SD")drain();
   q[arrival]++;
   const next=[...q,...o];
   if(next.reduce((x,y)=>x+y,0)!==before+1-out||q.some(v=>v<0)||o.some(v=>v<0||v>K))throw Error("conservation/capacity");
   transitions++;
   return {next,residual};
 }
 const results=[],witnesses=[];
 for(const order of ["SD","DS"])for(const objective of objectives){
   const memo=new Map();
   function costs(w,h,acc=[0,0]){
     const key=[...w,h,...(objective==="fair"?acc:[])].join(",");
     if(memo.has(key))return memo.get(key);
     const v=actions.map(a=>events.reduce((sum,event)=>{
       const {next,residual}=step(w,a,event,order);
       const acc2=objective==="fair"?acc.map((x,i)=>x+residual[i]):acc;
       const immediate=objective==="total"?(residual[0]+residual[1])*4**(h-1):0;
       let tail;
       if(h===1)tail=objective==="fair"?Math.max(...acc2):objective==="terminal"?next.reduce((x,y)=>x+y,0):0;
       else tail=Math.min(...costs(next,h-1,acc2));
       return sum+immediate+tail;
     },0));
     memo.set(key,v);return v;
   }
   for(let h=1;h<=3;h++){
     const rows=worlds.map(w=>{const v=costs(w,h);const best=Math.min(...v);return {w,v,opt:actions.filter(a=>v[a]===best),r:v.map(c=>c-best)};});
     for(const [rep,project] of Object.entries(reps)){
       const groups=new Map();for(const row of rows){const k=project(row.w).join(",");if(!groups.has(k))groups.set(k,[]);groups.get(k).push(row);}
       let badGroups=0,badWorlds=0,bayesNumerator=0,worstNumerator=0,witness=null,nonHellyGroups=0;
       for(const [key,g] of groups){
         const common=actions.filter(a=>g.every(r=>r.opt.includes(a)));
         if(!common.length){
           badGroups++;badWorlds+=g.length;
           let pair=null;
           for(const x of g)for(const y of g)if(!x.opt.some(a=>y.opt.includes(a))&&!pair)pair=[x,y];
           if(!pair)nonHellyGroups++;
           if(pair&&!witness)witness={key,pair};
         }
         bayesNumerator+=Math.min(...actions.map(a=>g.reduce((s,r)=>s+r.r[a],0)));
         worstNumerator=Math.max(worstNumerator,Math.min(...actions.map(a=>Math.max(...g.map(r=>r.r[a])))));
       }
       if(rep==="full"&&(badWorlds||bayesNumerator||worstNumerator))throw Error("full representation failure");
       results.push({order,objective,h,rep,groups:groups.size,badGroups,badWorlds,bayesNumerator,worstNumerator,nonHellyGroups});
       if((rep==="qe"||rep==="qeO")&&witness)witnesses.push({order,objective,h,rep,...witness});
     }
   }
 }
 return {worlds:worlds.length,transitions,results,witnesses};
}
console.log(JSON.stringify(h08b(),null,2));

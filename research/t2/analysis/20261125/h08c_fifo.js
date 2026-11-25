/* H08C amended: node h08c_fifo.js */
function h08c(){
 const A=[0,1],Klist=[[2,1],[2,2]],O=["total","fair"],modes=["FIFO","SKIP","FIXED"],words=[""];
 for(let n=1;n<=4;n++)for(let i=0;i<2**n;i++)words.push(i.toString(2).padStart(n,"0"));
 const count=w=>[w.split("0").length-1,w.split("1").length-1];
 const C=w=>[...w.slice(0,2),...count(w[2])];
 const reps={q:w=>w.slice(0,2),C,H1:w=>[...C(w),w[2].slice(0,1)],H2:w=>[...C(w),w[2].slice(0,2)],H3:w=>[...C(w),w[2].slice(0,3)],RUN:w=>[...C(w),w[2].match(/^(0+|1+)/)?.[0]??""],FULL:w=>w};
 let transitions=0;const results=[],witnesses=[];
 for(const K of Klist)for(const mode of modes)for(const obj of O){
 const worlds=[];for(let s=0;s<=K[0];s++)for(let l=0;l<=K[1];l++)for(const word of words)worlds.push([s,l,word]);
 function step(w,a,arr){
  const q=w.slice(0,2),old=count(w[2]),before=q.map((v,i)=>v+old[i]);let word=w[2];
  const d=Math.min(q[a],2);q[a]-=d;
  for(let j=0;j<2&&word.length;j++){
   let k=0;
   if(mode==="SKIP")k=[...word].findIndex(x=>q[+x]<K[+x]);
   if(mode==="FIXED"){k=-1;for(const i of A)if(q[i]<K[i]&&word.includes(String(i))){k=word.indexOf(String(i));break;}}
   if(k<0||q[+word[k]]>=K[+word[k]])break;
   q[+word[k]]++;word=word.slice(0,k)+word.slice(k+1);
  }
  const residual=count(word).map((v,i)=>v+q[i]);word+=arr;const next=[...q,word];
  if(q.some((v,i)=>v<0||v>K[i])||residual.some((v,i)=>v!==before[i]-(i===a?d:0))||count(word).some((v,i)=>v+q[i]!==residual[i]+(i===arr?1:0)))throw Error("conservation");
  transitions++;return{next,residual};
 }
 const memo=new Map();
 function values(w,h,acc=[0,0]){
  const key=JSON.stringify([w,h,obj==="fair"?acc:[]]);if(memo.has(key))return memo.get(key);
  const v=A.map(a=>A.reduce((sum,arr)=>{
   const {next,residual}=step(w,a,arr),acc2=acc.map((v,i)=>v+residual[i]);
   return sum+(h===1?(obj==="fair"?Math.max(...acc2):0):Math.min(...values(next,h-1,acc2)))+(obj==="total"?residual.reduce((s,v)=>s+v,0)*2**(h-1):0);
  },0));memo.set(key,v);return v;
 }
 for(let h=1;h<=4;h++){
  const rows=worlds.map(w=>{const v=values(w,h);return{w,v,r:v.map(c=>c-Math.min(...v)),opt:A.filter(a=>v[a]===Math.min(...v))};});
  for(const [rep,project] of Object.entries(reps)){
   const groups=new Map();for(const row of rows){const key=JSON.stringify(project(row.w));if(!groups.has(key))groups.set(key,[]);groups.get(key).push(row);}
   let badGroups=0,badWorlds=0,bayesNumerator=0,worstNumerator=0,witness=null;
   for(const [key,g] of groups){
    if(!A.some(a=>g.every(r=>r.r[a]===0))){badGroups++;badWorlds+=g.length;if(!witness){const p=g.find(r=>r.opt.length===1&&r.opt[0]===0),q=g.find(r=>r.opt.length===1&&r.opt[0]===1);if(!p||!q)throw Error("binary intersection");witness={key,pair:[p,q]};}}
    bayesNumerator+=Math.min(...A.map(a=>g.reduce((s,r)=>s+r.r[a],0)));
    worstNumerator=Math.max(worstNumerator,Math.min(...A.map(a=>Math.max(...g.map(r=>r.r[a])))));
   }
   if((rep==="FULL"||mode==="FIXED"&&rep==="C")&&(badGroups||bayesNumerator||worstNumerator))throw Error("control failed");
   results.push({K,mode,obj,h,rep,worlds:worlds.length,groups:groups.size,badGroups,badWorlds,bayesNumerator,worstNumerator});
   if(witness&&["C","H1","H2","H3","RUN"].includes(rep))witnesses.push({K,mode,obj,h,rep,...witness});
  }
 }
 }
 return{transitions,results,witnesses};
}
console.log(JSON.stringify(h08c(),null,2));

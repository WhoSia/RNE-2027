// node p87_robust_table.js path/to/P87_RESULT.json
function robust(data) {
 const rows=data.rows,seeds=[...new Set(rows.map(r=>r.seed))],shares=[.25,.5,.75],onsets=["green","red"];
 const idx=(o,s)=>onsets.indexOf(o)*3+shares.indexOf(s);
 const act=(mask,o,s)=>mask&(1<<idx(o,s))?60:30;
 const loss=(x,a)=>a===30?Math.max(x.delta.cost,0):Math.max(-x.delta.cost,0);
 // expectation by bilinear interpolation in independent corruption probabilities
 const expect=(set,mask,a,b)=>set.reduce((sum,x)=>sum+onsets.reduce((so,o)=>so+shares.reduce((ss,s)=>ss+(o===x.onset?1-a:a)*(s===x.share?1-b:b/2)*loss(x,act(mask,o,s)),0),0),0);
 const budgets=[0,.1,.2,.3,.4,.5];
 const test=[0,.1,.2,.3,.4,.5];
 const results=[];
 for(const budget of budgets){
  const corners=[[0,0],[budget,0],[0,budget],[budget,budget]];
  const decisions=seeds.map(seed=>{
   const train=rows.filter(x=>x.seed!==seed);
   const candidates=Array.from({length:64},(_,mask)=>({mask,worst:Math.max(...corners.map(([a,b])=>expect(train,mask,a,b)))})).sort((x,y)=>x.worst-y.worst||x.mask-y.mask);
   return {seed,mask:candidates[0].mask,trainWorst:candidates[0].worst};
  });
  const held=test.flatMap(a=>test.map(b=>({a,b,loss:decisions.reduce((s,d)=>s+expect(rows.filter(x=>x.seed===d.seed),d.mask,a,b),0)})));
  results.push({budget,masks:[...new Set(decisions.map(x=>x.mask))],heldDiag:held.filter(x=>x.a===x.b),heldWorstWithin:Math.max(...held.filter(x=>x.a<=budget&&x.b<=budget).map(x=>x.loss)),held,decisions});
 }
 if(results[0].heldDiag[0].loss!==8723)throw Error("baseline mismatch");
 if(!results.every(r=>r.decisions.length===16))throw Error("fold count");
 return {status:"EXPLORATORY_ROBUST_POLICY_WITH_ASSUMED_ERROR_RECTANGLE",fixed30:43945,sourceRows:rows.length,budgets,results,scope:"Training selects 64 deterministic tables by worst expected loss over rectangle corners; evaluated on excluded seed. Bilinear maximum over rectangle attained at a corner. Synthetic known error model; no real calibration; shared historical cohort."}
}
const fs=require('fs'); console.log(JSON.stringify(robust(JSON.parse(fs.readFileSync(process.argv[2],'utf8'))),null,2));

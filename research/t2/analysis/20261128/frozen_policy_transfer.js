// node frozen_policy_transfer.js P100_RESULT.json P89_RESULT.json
function transfer(p100,p89) {
 const rules={fixed30:r=>30,fixed60:r=>60,frozen:r=>r.onset==="red"&&r.share===.75?60:30};
 const loss=(d,a)=>a===30?Math.max(d,0):Math.max(-d,0);
 function summarize(rows,delta){
  const groups=[...new Set(rows.map(r=>r.seed))];
  const metrics=Object.fromEntries(Object.entries(rules).map(([name,rule])=>{let v=rows.map(r=>loss(delta(r),rule(r)));return [name,{regret:v.reduce((s,x)=>s+x,0),mean:v.reduce((s,x)=>s+x,0)/v.length,correct:v.filter(x=>x===0).length,worst:Math.max(...v)}]}));
  const block=groups.map(seed=>{const z=rows.filter(r=>r.seed===seed);return {seed,deltaVsFixed30:z.reduce((s,r)=>s+loss(delta(r),rules.frozen(r))-loss(delta(r),30),0)}});
  return {n:rows.length,seedBlocks:groups.length,win30:rows.filter(r=>delta(r)<0).length,win60:rows.filter(r=>delta(r)>0).length,ties:rows.filter(r=>delta(r)===0).length,metrics,block,blockWin:block.filter(r=>r.deltaVsFixed30<0).length,blockTie:block.filter(r=>r.deltaVsFixed30===0).length,blockLoss:block.filter(r=>r.deltaVsFixed30>0).length};
 }
 if(p100.rows.length!==384||p89.rows.length!==768)throw Error("unexpected lengths");
 const first=summarize(p100.rows,r=>r.delta.cost);
 if(first.seedBlocks!==32||p100.rows.some(r=>r.seed<86001||r.seed>86032))throw Error("seed range");
 const strata=["green","red"].flatMap(onset=>[.25,.5,.75].map(share=>({onset,share,...summarize(p100.rows.filter(r=>r.onset===onset&&r.share===share),r=>r.delta.cost)})));
 const masks=[0,1,2,3].map(mask=>({mask,...summarize(p89.rows.filter(r=>r.lost_seconds_per_green===mask),r=>r.delta_30_minus_60.cost)}));
 if(masks[0].metrics.frozen.regret!==8723||masks[0].metrics.fixed30.regret!==43945)throw Error("prior result mismatch");
 return {status:"RETROSPECTIVE_TRANSFER_OF_FROZEN_RULE",rule:"60 only red and share .75, else 30",P100:first,P100strata:strata,P89:masks,scope:"P100 distinct route seeds but same simulator; summaries previously known. P89 interventions reuse P87 tapes. No new simulation or real field data."};
}
const fs=require('fs');console.log(JSON.stringify(transfer(JSON.parse(fs.readFileSync(process.argv[2],'utf8')),JSON.parse(fs.readFileSync(process.argv[3],'utf8'))),null,2));

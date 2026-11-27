// node movement_equity.js P101_RESULT.json
function equity(p101){
 const rows=p101.rows.filter(r=>r.onset==="red"&&r.share===.75);
 if(rows.length!==64||!rows.every(r=>r.movement_total.L+r.movement_total.S===r.delta.cost&&r.movement_total.L>0))throw Error("source mismatch");
 const sum=k=>rows.reduce((s,r)=>s+r.movement_total[k],0);
 const thresholds=rows.map(r=>({seed:r.seed,clock:r.clock,threshold:Math.max(0,-r.movement_total.S/r.movement_total.L)}));
 const rates=[0,.025,.05,.1,.2,.5,1,2].map(w=>({leftWeight:w,prefer60:rows.filter(r=>w*r.movement_total.L+r.movement_total.S>0).length,ties:rows.filter(r=>w*r.movement_total.L+r.movement_total.S===0).length,weighted30minus60:w*sum("L")+sum("S")}));
 return {status:"RETROSPECTIVE_MOVEMENT_GROUP_TOTALS",pairs:rows.length,leftGain:sum("L"),throughLoss:-sum("S"),throughWorsened:rows.filter(r=>r.movement_total.S<0).length,throughImproved:rows.filter(r=>r.movement_total.S>0).length,throughTied:rows.filter(r=>r.movement_total.S===0).length,aggregateWeightThreshold:-sum("S")/sum("L"),maxCaseThreshold:Math.max(...thresholds.map(r=>r.threshold)),rates,thresholds,scope:"P101 red high-share synthetic subset; switching 30 to 60. Weighted group totals not per-vehicle fairness, no new engine or field validation."}
}
const fs=require('fs');console.log(JSON.stringify(equity(JSON.parse(fs.readFileSync(process.argv[2],'utf8'))),null,2));

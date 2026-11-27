// node p87_observation_stress.js path/to/P87_RESULT.json
function stress(data){
 const rows=data.rows,seeds=[...new Set(rows.map(r=>r.seed))],shares=[.25,.5,.75],onsets=["green","red"];
 const loss=(x,a)=>a===30?Math.max(x.delta.cost,0):Math.max(-x.delta.cost,0);
 const choices=seeds.map(seed=>({seed,table:Object.fromEntries(onsets.flatMap(onset=>shares.map(share=>{const z=rows.filter(r=>r.seed!==seed&&r.onset===onset&&r.share===share);const a=z.reduce((s,x)=>s+loss(x,30),0),b=z.reduce((s,x)=>s+loss(x,60),0);return [onset+"/"+share,a<b?30:60]})))}));
 const bySeed=new Map(choices.map(x=>[x.seed,x.table]));
 const levels=[0,.05,.1,.2,.3,.4,.5,1];
 const grid=[];
 for(const a of levels)for(const b of levels){
   let total=0,accuracy=0;
   for(const x of rows)for(const onset of onsets)for(const share of shares){
    const w=(onset===x.onset?1-a:a)*(share===x.share?1-b:b/2);
    const act=bySeed.get(x.seed)[onset+"/"+share];
    const l=loss(x,act);total+=w*l;accuracy+=w*+(l===0);
   }
   grid.push({onsetError:a,shareError:b,totalRegret:total,meanRegret:total/rows.length,expectedAccuracy:accuracy/rows.length});
 }
 const fixed=rows.reduce((s,x)=>s+loss(x,30),0);
 const both=grid.find(r=>r.onsetError===0&&r.shareError===0);
 if(both.totalRegret!==8723||fixed!==43945)throw Error("baseline mismatch");
 // Worst loss when at most k records in each fixed cohort have a corrupted observation;
 // not a stochastic model; each row can be altered independently and adversarially.
 const deltas=rows.map(x=>{const t=bySeed.get(x.seed),base=loss(x,t[x.onset+"/"+x.share]);return Math.max(...Object.values(t).map(a=>loss(x,a)))-base}).sort((a,b)=>b-a);
 let sum=both.totalRegret, k=0;while(sum<fixed&&k<deltas.length)sum+=deltas[k++];
 return {status:"SYNTHETIC_FEATURE_CORRUPTION_NOT_SENSOR_CALIBRATION",fixed30:fixed,baseline:both,choices,grid,adversarial:{minCorruptedRowsToEqualOrExceedFixed30:k,totalRegret:sum,share:k/rows.length,scope:"arbitrary adversarial row-specific changes, no claim of real sensor likelihood"},checks:["source baseline verified","error probabilities sum by construction","fixed comparator verified"]};
}
const fs=require('fs'); console.log(JSON.stringify(stress(JSON.parse(fs.readFileSync(process.argv[2],'utf8'))),null,2));

// Synthetic binary channel example; no real sensor calibration.
function audit() {
  const D=20000;
  const joint=(e1,e2)=>{
    const rows=[];
    for(let t=0;t<2;t++)for(let a=0;a<2;a++)for(let b=0;b<2;b++)
      rows.push({t,a,b,w:(a===t?100-e1:e1)*(b===t?100-e2:e2)});
    return rows;
  };
  const obs=rows=>[0,1,2,3].map(k=>rows.filter(r=>2*r.a+r.b===k).reduce((s,r)=>s+r.w,0));
  const target=obs(joint(10,10));
  const worlds=[];
  for(let a=0;a<=50;a++)for(let b=0;b<=50;b++){
    const rows=joint(a,b);
    if(obs(rows).every((v,i)=>v===target[i]))worlds.push({e1:a,e2:b,rows});
  }
  const checks=[];
  const check=(label,condition)=>{if(!condition)throw Error(label);checks.push(label)};
  check("observed joint sums to denominator",target.reduce((s,x)=>s+x,0)===D);
  check("all worlds equal observed distribution",worlds.every(w=>obs(w.rows).every((v,i)=>v===target[i])));
  check("worlds include opposite perfect channels",worlds.some(w=>w.e1===0&&w.e2===18)&&worlds.some(w=>w.e1===18&&w.e2===0));
  const rules=Array.from({length:16},(_,mask)=>{
    const losses=worlds.map(w=>w.rows.reduce((s,r)=>s+(r.t!==((mask>>(2*r.a+r.b))&1)?r.w:0),0));
    return {mask,outputs:[0,1,2,3].map(k=>(mask>>k)&1),losses};
  });
  const oracle=worlds.map((_,i)=>Math.min(...rules.map(r=>r.losses[i])));
  const ranked=rules.map(r=>({...r,regrets:r.losses.map((l,i)=>l-oracle[i]),worstRegret:Math.max(...r.losses.map((l,i)=>l-oracle[i])),worstLoss:Math.max(...r.losses)})).sort((a,b)=>a.worstRegret-b.worstRegret||a.worstLoss-b.worstLoss||a.mask-b.mask);
  check("oracle risk equals better channel",worlds.every((w,i)=>oracle[i]===Math.min(w.e1,w.e2)*D/100));
  check("best deterministic worst regret 0.09",ranked[0].worstRegret===1800);
  check("choose A and B each worst regret 0.18",ranked.filter(r=>r.mask===12||r.mask===10).every(r=>r.worstRegret===3600));
  // Randomized decision in disagreement; symmetric worlds imply lower bound.
  const mixed=worlds.map(w=>w.rows.reduce((s,r)=>s+r.w*(r.a===r.b?(r.t!==r.a?2:0):1),0));
  check("fair disagreement coin attains 0.09 max regret",Math.max(...mixed.map((x,i)=>x-2*oracle[i]))===3600);
  // Independent enumeration of compatible parameter pairs from correlation identity.
  const viaProduct=[];
  for(let a=0;a<=50;a++)for(let b=0;b<=50;b++)if((100-2*a)*(100-2*b)===6400)viaProduct.push([a,b]);
  check("correlation equation matches enumeration",JSON.stringify(viaProduct)===JSON.stringify(worlds.map(w=>[w.e1,w.e2])));
  return {status:"SYNTHETIC_IDENTIFIABILITY_COUNTEREXAMPLE_NOT_FIELD_CALIBRATION",denominator:D,gridPairs:2601,target,worlds:worlds.map(({e1,e2})=>({e1,e2})),oracle,ranked,mixedLossNumerators:mixed,mixedDenominator:2*D,checks};
}
console.log(JSON.stringify(audit(), null, 2));

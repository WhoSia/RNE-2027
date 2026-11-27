function planning(){
  const bin=(n,p,k)=>{
    let prob=(1-p)**n,tail=0;
    for(let i=0;i<=n;i++){if(i>=k)tail+=prob;if(i<n)prob*=((n-i)/(i+1))*(p/(1-p))}
    return tail;
  };
  function critical(n){for(let k=0;k<=n;k++)if(bin(n,.5,k)<=.05)return k;return n+1}
  const sizes=[12,16,20,24,30,40,50,60,80,100];
  const rows=sizes.map(n=>{const k=critical(n);return {independentNonTieBlocks:n,criticalWins:k,typeI:bin(n,.5,k),power:Object.fromEntries([.6,.65,.7,.75,.8].map(p=>[p,bin(n,p,k)]))}});
  const minimum=[.6,.65,.7,.75,.8].map(p=>{let n=1;while(n<=250&&bin(n,p,critical(n))<.8)n++;return {p,n,critical:critical(n),power:bin(n,p,critical(n))}});
  const checks=[Math.abs(bin(4,.5,3)-5/16)<1e-12,Math.abs(bin(4,.5,0)-1)<1e-12,rows.every(r=>r.typeI<=.05+1e-12),minimum.every(r=>r.power>=.8)];
  if(!checks.every(Boolean))throw Error("power check");
  return {status:"DESIGN_SCENARIOS_NOT_EMPIRICAL_EFFECT_ESTIMATE",alpha:.05,alternative:"one-sided probability of paired improvement > 0.5 among independent non-tied blocks",rows,minimum,checks,warning:"Sign test concerns win probability, not mean improvement. Ties excluded; non-tie counts are not total recruited blocks. Independence and common target population required. Plan calibration and evaluation blocks disjoint. Repeated ticks not samples."};
}
console.log(JSON.stringify(planning(),null,2));

'use strict';
// Post-hoc analysis of frozen P150A rows, no new simulations.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const input = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const key = (t,d,p,h,r) => [t,d,p,h,r].join(',');
const rows = new Map(input.rows.map(x => [key(x.tape,x.D,x.p,x.phi,x.reuse),x.cost]));
assert.equal(rows.size,432);
const result = {status:'POSTHOC_MODEL_UNCERTAINTY_NOT_FIELD_EVIDENCE',new_simulations:0,pairs:0,strict_reversals:0,pure_zero_regret:0,pure_minimax_total:0,old_only_total:0,reuse_only_total:0,max_pure_regret:0,witnesses:[]};
for (const tape of ['uniform','pairs','clustered']) for (let D=1;D<=6;D++) {
  for (let h4=0;h4<4;h4++) for (let h8=0;h8<8;h8++) {
    const deltas = [0,1].map(r => rows.get(key(tape,D,4,h4,r))-rows.get(key(tape,D,8,h8,r)));
    assert(deltas.every(Number.isFinite));
    const [old,reuse]=deltas;
    const a=Math.max(0,...deltas), b=Math.max(0,...deltas.map(x=>-x));
    const pure=Math.min(a,b);
    const choose4=a<=b;
    result.pairs++;
    result.pure_minimax_total+=pure;
    result.old_only_total+=old<=0?a:b;
    result.reuse_only_total+=reuse<=0?a:b;
    result.max_pure_regret=Math.max(result.max_pure_regret,pure);
    if (pure===0) result.pure_zero_regret++;
    if (old*reuse<0) {
      result.strict_reversals++;
      // Randomization is a mathematical comparison only; the model is fixed before the draw.
      result.witnesses.push({tape,D,h4,h8,old,reuse,worst_choose4:a,worst_choose8:b,pure_choice:choose4?4:8,pure_regret:pure,randomized_choose4_fraction:[b,a+b],randomized_worst_expected_regret_fraction:[a*b,a+b]});
    }
  }
}
assert.equal(result.pairs,576);
assert.equal(result.strict_reversals,input.totals.strict_reversal);
assert.equal(result.pure_zero_regret+result.strict_reversals,result.pairs);
assert(result.pure_minimax_total<=result.old_only_total && result.pure_minimax_total<=result.reuse_only_total);
console.log(JSON.stringify(result,null,2));

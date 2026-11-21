"""PHYS-04 stage B: runnable matched-state experiment (synthetic, uncalibrated).

Example:
  PYTHONPATH=research/t2 python research/t2/physical_checkpoint_screen.py out.json

Baseline and treatment start from the same exact pre-tick-84 state. The sole
treatment changes the remainder of this cycle to 3s clearance, 4s protected
left-green, then no service until t=120; baseline has the final 4s of
through-green. Both have four active signal ticks during [84,120), but the
movement served differs. This is a MODEL-CONDITIONAL counterfactual, not an
evaluation of compliant real-world signal plan feasibility.
"""
import json
from dataclasses import replace
from itertools import product
from pathlib import Path
from dual_lane_v11 import DualConfig, run
from spatial_v10 import Config, arrivals
from physical_transfer_screen import score

SEEDS=tuple(range(8))
POCKETS_M=(14.,28.,70.)
B_SHARES=(0.,.5)
CHECKPOINT_TICK=84
FUTURE_PLAN=((84,87,'-'),(87,91,'L'),(91,120,'-'))


def experiment():
    rows=[]
    for seed,pocket,share in product(SEEDS,POCKETS_M,B_SHARES):
        base=Config(seed=seed,pocket_length_m=pocket,phase_order='leading',
                    duration_s=240,demand_vph=1800,left_fraction=.5)
        c=DualConfig(base=base,through_B_share=share,
                     allow_lane_changes=True,change_zone_m=100.,
                     receiver_slots=4,receiver_mode='cells')
        tape=arrivals(base)
        cp=run(c,tape,checkpoint_at=CHECKPOINT_TICK)
        reference=run(c,tape)
        resumed=run(c,tape,resume_from=cp)
        if reference!=resumed:
            raise AssertionError(('checkpoint identity failed',seed,pocket,share))
        treated=run(c,tape,resume_from=cp,phase_overrides=FUTURE_PLAN)
        base_cost=score(reference)
        treatment_cost=score(treated)
        rows.append(dict(seed=seed,pocket_m=pocket,b_share=share,
                         generated=reference['generated'],
                         baseline_cost=base_cost,treatment_cost=treatment_cost,
                         treatment_minus_baseline=treatment_cost-base_cost,
                         baseline_out_S=reference['network_out_S'],
                         baseline_out_L=reference['network_out_L'],
                         treatment_out_S=treated['network_out_S'],
                         treatment_out_L=treated['network_out_L'],
                         resumed_identical=True))
    assert len(rows)==48
    changes=[r for r in rows if r['treatment_minus_baseline']!=0]
    return {
      'status':'SYNTHETIC_UNCALIBRATED',
      'claim_scope':'matched full state, same exogenous demand and geometry, model conditional',
      'checkpoint_tick':CHECKPOINT_TICK,
      'intervention':FUTURE_PLAN,
      'note':'Four active ticks remain in both cases, but served movements differ; no field inference',
      'summary':{'conditions':len(rows),'checkpoint_identity_controls':len(rows),
                 'nonzero_cost_effects':len(changes),
                 'baseline_preferred':sum(r['treatment_minus_baseline']>0 for r in rows),
                 'treatment_preferred':sum(r['treatment_minus_baseline']<0 for r in rows),
                 'ties':sum(r['treatment_minus_baseline']==0 for r in rows)},
      'pairs':rows,
    }


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    args.output.write_text(json.dumps(experiment(),ensure_ascii=False,
                                      sort_keys=True,indent=2)+'\n',encoding='utf-8')

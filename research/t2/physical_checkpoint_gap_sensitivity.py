"""PHYS-06: target-lane clearance sensitivity (1,2,3 cells).

Each clearance is a different predecision traffic world. WITHIN a
clearance/seed/pocket/B-share condition, the two future signal policies
are run from one identical checkpoint at tick 84. Changing gap clearance
itself is NEVER presented as a matched-state intervention.

Run:
  PYTHONPATH=research/t2 python research/t2/physical_checkpoint_gap_sensitivity.py out.json
"""
import argparse
import json
from itertools import product
from pathlib import Path

from dual_lane_v11 import DualConfig, run
from spatial_v10 import Config, arrivals
from physical_transfer_screen import score

PLAN = ((84, 87, '-'), (87, 91, 'L'), (91, 120, '-'))
GAPS = (1, 2, 3)
SEEDS = range(8)
POCKETS = (14., 28., 70.)
B_SHARES = (0., .5)


def experiment():
    rows = []
    for gap, seed, pocket, share in product(GAPS, SEEDS, POCKETS, B_SHARES):
        base = Config(seed=seed, pocket_length_m=pocket,
                      phase_order='leading', duration_s=240,
                      demand_vph=1800, left_fraction=.5)
        c = DualConfig(base=base, through_B_share=share,
                       change_zone_m=100., allow_lane_changes=True,
                       receiver_slots=4, receiver_mode='cells',
                       lane_change_target_gap_cells=gap)
        tape = arrivals(base)
        cp = run(c, tape, checkpoint_at=84)
        control = run(c, tape)
        assert control == run(c, tape, resume_from=cp)
        treatment = run(c, tape, resume_from=cp, phase_overrides=PLAN)
        rows.append({
            'gap': gap, 'seed': seed, 'pocket_m': pocket, 'b_share': share,
            'delta': score(treatment, 60) - score(control, 60),
            'baseline_cost': score(control, 60),
            'treated_cost': score(treatment, 60),
            'baseline_changes': control['changes_A_to_B'],
            'treated_changes': treatment['changes_A_to_B'],
            'baseline_denials': control['lane_change_target_gap_denials'],
            'treated_denials': treatment['lane_change_target_gap_denials'],
            'baseline_remaining': control['remaining'],
            'treated_remaining': treatment['remaining'],
            'checkpoint_identity': True,
        })
    summary = {}
    for gap in GAPS:
        cohort = [r for r in rows if r['gap'] == gap]
        summary[str(gap)] = {
            'treatment_better': sum(r['delta'] < 0 for r in cohort),
            'baseline_better': sum(r['delta'] > 0 for r in cohort),
            'ties': sum(r['delta'] == 0 for r in cohort),
            'mean_delta': sum(r['delta'] for r in cohort) / len(cohort),
            'baseline_changes': sum(r['baseline_changes'] for r in cohort),
            'baseline_denials': sum(r['baseline_denials'] for r in cohort),
        }
    flips = []
    for seed, pocket, share in product(SEEDS, POCKETS, B_SHARES):
        group = [next(r for r in rows if r['gap'] == gap and
                      r['seed'] == seed and r['pocket_m'] == pocket and
                      r['b_share'] == share) for gap in GAPS]
        if min(r['delta'] for r in group) < 0 < max(r['delta'] for r in group):
            flips.append({'seed': seed, 'pocket_m': pocket,
                          'b_share': share,
                          'deltas': [r['delta'] for r in group]})
    assert len(rows) == 144
    return {
        'status': 'SYNTHETIC_UNCALIBRATED',
        'note': 'gap is a predecision model parameter, not a matched-state intervention',
        'summary': summary, 'strict_preference_flips': flips, 'pairs': rows,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(experiment(), sort_keys=True,
                                      ensure_ascii=False, indent=2) + '\n',
                           encoding='utf-8')

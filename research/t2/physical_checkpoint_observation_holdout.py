"""PHYS-05 external-seed stress test: train on seed 0..7, test seeds 8..31.

Run after the PHYS-04 canonical capacity screen has generated train.json:
  PYTHONPATH=research/t2 python research/t2/physical_checkpoint_observation_holdout.py train.json holdout.json

Model and feature maps are imported from physical_checkpoint_observation_ablation.
The model is frozen at k=5; no held-out outcome is used for fitting.
The policy experiment remains synthetic and uncalibrated.
"""
import argparse
import json
from itertools import product
from pathlib import Path

from dual_lane_v11 import DualConfig, run, checkpoint_observation
from spatial_v10 import Config, arrivals
from physical_transfer_screen import score
from physical_checkpoint_observation_ablation import LEVELS, predict

PLAN = ((84, 87, '-'), (87, 91, 'L'), (91, 120, '-'))
HOLDOUT_SEEDS = tuple(range(8, 32))


def experiment(training_rows):
    if len(training_rows) != 144 or {r['seed'] for r in training_rows} != set(range(8)):
        raise ValueError("training rows must be all 144 PHYS-04 cases from seeds 0..7")
    rows = []
    for seed, capacity, pocket, share in product(
            HOLDOUT_SEEDS, (2, 4, 8), (14., 28., 70.), (0., .5)):
        base = Config(seed=seed, duration_s=240, demand_vph=1800,
                      left_fraction=.5, pocket_length_m=pocket,
                      phase_order='leading')
        config = DualConfig(base=base, receiver_mode='cells',
                            receiver_slots=capacity, through_B_share=share,
                            allow_lane_changes=True, change_zone_m=100.)
        tape = arrivals(base)
        checkpoint = run(config, tape, checkpoint_at=84)
        control = run(config, tape, resume_from=checkpoint)
        treatment = run(config, tape, resume_from=checkpoint,
                        phase_overrides=PLAN)
        if control != run(config, tape):
            raise AssertionError(('restart mismatch', seed, capacity, pocket, share))
        row = {'seed': seed, 'capacity': capacity, 'pocket_m': pocket,
               'b_share': share,
               'decision_observation': checkpoint_observation(checkpoint),
               'delta_p60': score(treatment, 60) - score(control, 60)}
        row['oracle_best_saved'] = max(-row['delta_p60'], 0)
        row['always_treat_saved'] = -row['delta_p60']
        for level in LEVELS:
            estimate = predict(training_rows, row, level, k=5)
            row[level + '_predicted_delta'] = estimate
            row[level + '_treat'] = estimate < 0
            row[level + '_saved'] = -row['delta_p60'] if estimate < 0 else 0
        rows.append(row)
    summary = {}
    for level in ('always_treat',) + LEVELS:
        key = level + '_saved'
        summary[level] = {
            'total_saved': sum(r[key] for r in rows),
            'per_pair_saved': sum(r[key] for r in rows) / len(rows),
            'regret': sum(r['oracle_best_saved'] - r[key] for r in rows),
            'per_seed_saved': [
                sum(r[key] for r in rows if r['seed'] == seed)
                for seed in HOLDOUT_SEEDS],
        }
    assert len(rows) == 432
    return {
        'status': 'SYNTHETIC_UNCALIBRATED',
        'holdout_seed_range': [8, 31],
        'training_seeds': list(range(8)),
        'holdout_seed_count': len(HOLDOUT_SEEDS),
        'evaluated_pairs': len(rows),
        'model': 'five nearest neighbors, fixed after seed0..7 exploratory screen',
        'summary': summary,
        'oracle_total_saved': sum(r['oracle_best_saved'] for r in rows),
        'cases': rows,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('training_json', type=Path)
    parser.add_argument('output_json', type=Path)
    args = parser.parse_args()
    training = json.loads(args.training_json.read_text(encoding='utf-8'))
    out = experiment(training['pairs'])
    args.output_json.write_text(
        json.dumps(out, sort_keys=True, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8')

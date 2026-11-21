"""Exploratory PHYS-10 audit: cross historical prefixes and future arrival tapes.

This REUSES known seeds 3 and 76: it is NOT held-out confirmatory evidence.
Only matched baseline vs intervention inside each of the four crossed worlds
is a same-state signal-plan causal contrast. Cross-prefix changes also alter
predecision microscopic vehicle arrangement, not just observed counts.
"""
import argparse
import hashlib
import json
import pickle
from pathlib import Path

from dual_lane_v11 import run, checkpoint_observation
from spatial_v10 import arrivals
from physical_transfer_screen import score
from physical_checkpoint_delay_and_shift import make_config, INTERVENTION
from physical_checkpoint_observation_ablation import features

DECISION_TICK = 84
CASES = ((3, .50), (76, .45))


def experiment():
    configs = {seed: make_config(seed, 4, 14., 0., 1800, left) for seed, left in CASES}
    tapes = {seed: arrivals(c.base) for seed, c in configs.items()}
    original = {seed: run(configs[seed], tapes[seed], checkpoint_at=DECISION_TICK)
                for seed, _ in CASES}
    out = []
    for prefix, _ in CASES:
        c = configs[prefix]
        for future, _ in CASES:
            tape = (tuple((t, route) for t, route in tapes[prefix] if t < DECISION_TICK)
                    + tuple((t, route) for t, route in tapes[future] if t >= DECISION_TICK))
            cp = run(c, tape, checkpoint_at=DECISION_TICK)
            if pickle.dumps(cp['state'], protocol=4) != pickle.dumps(original[prefix]['state'], protocol=4):
                raise AssertionError(('history leaked from future', prefix, future))
            control = run(c, tape, resume_from=cp)
            if control != run(c, tape):
                raise AssertionError(('uninterrupted replay mismatch', prefix, future))
            treatment = run(c, tape, resume_from=cp, phase_overrides=INTERVENTION)
            delta = score(treatment, 60) - score(control, 60)
            components = {key: treatment[key] - control[key]
                          for key in ('outside_vehicle_seconds',
                                      'upstream_vehicle_seconds',
                                      'receiver_vehicle_seconds', 'remaining',
                                      'network_out_S', 'network_out_L')}
            out.append({'prefix_seed': prefix, 'future_seed': future,
                        'delta_p60': delta, 'matched_policy_checkpoint': True,
                        'prefix_state_independent_of_future': True,
                        'components': components,
                        'observation': checkpoint_observation(cp)})
    feat = {x['prefix_seed']: features({
                'capacity': 4, 'pocket_m': 14., 'b_share': 0.,
                'decision_observation': x['observation']}, 'counts')
            for x in out if x['prefix_seed'] == x['future_seed']}
    if feat[3] != feat[76]:
        raise AssertionError('aggregate-count alias unexpectedly disappeared')
    return {'status': 'EXPLORATORY_REUSED_SEEDS_NOT_PROSPECTIVE',
            'protocol': 'PHYS-10 predecision-prefix x future-arrival 2x2 audit',
            'original_turn_shares': {'3': .50, '76': .45},
            'observed_count_feature_identical': True,
            'cells': out,
            'not_strict_policy_rank_reversal': True,
            'note': 'one world has ΔJ>0, the other three are exact ties; baseline is weakly best in every cell'}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('output_json', type=Path)
    args = ap.parse_args()
    blob = (json.dumps(experiment(), sort_keys=True, ensure_ascii=False, indent=2) + '\n').encode()
    args.output_json.write_bytes(blob)
    print('SHA256', hashlib.sha256(blob).hexdigest())
    print([(r['prefix_seed'], r['future_seed'], r['delta_p60'])
           for r in json.loads(blob)['cells']])

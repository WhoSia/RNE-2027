"""P16: faithful PHYS-04 decision-time observation audit; NOT RF sensing.

Consumes serializable checkpoint_observation() output and PHYS-04 case rows.
Fails closed rather than reinterpreting occupancy as a causal blockage label.
"""
from __future__ import annotations
from collections import defaultdict
from math import isfinite

COUNTS = ('outside_A','outside_B','approach_A','approach_B','pocket_vehicles','receiver_vehicles')
POSITIONS = ('pocket_positions','approach_A_positions','approach_B_positions','receiver_occupied_cells')


def _count(v, key):
    if type(v) is not int or v < 0:
        raise ValueError(f'{key}: expected nonnegative integer, not bool')
    return v


def summarize_checkpoint(observation, *, receiver_capacity):
    """State proxies only; no claim that either zone is *blocked*.

    Entry-cell occupancy does NOT imply a full link; a full link does
    imply entry occupancy under one-car-per-cell. Blockage needs dynamics.
    """
    if not isinstance(observation, dict):
        raise TypeError('checkpoint observation must be a dict')
    capacity = _count(receiver_capacity, 'receiver_capacity')
    if capacity == 0:
        raise ValueError('positive receiver capacity required for this audit')
    counts = tuple(_count(observation[k],k) for k in COUNTS)
    if counts[-1] > capacity:
        raise ValueError('receiver occupancy exceeds declared capacity')
    shapes = {}
    for key in POSITIONS:
        obj = observation[key]
        if not isinstance(obj, (tuple,list)) or any(type(x) is not int for x in obj):
            raise ValueError(f'{key}: integer position sequence required')
        if len(set(obj)) != len(obj):
            raise ValueError(f'{key}: duplicate occupied cell')
        shapes[key] = tuple(obj)
    for key,idx in [('pocket_positions',4),('approach_A_positions',2),('approach_B_positions',3),('receiver_occupied_cells',5)]:
        if len(shapes[key]) != counts[idx]:
            raise ValueError(f'{key} count differs from checkpoint count')
    if any(i < 0 or i >= capacity for i in shapes['receiver_occupied_cells']):
        raise ValueError('receiver occupied cell outside declared link')
    return {
        'six_counts': counts,
        'pocket_present': counts[4] > 0,
        'receiver_full': counts[5] == capacity,
        'receiver_entry_cell_occupied': 0 in shapes['receiver_occupied_cells'],
        'pocket_vehicles': counts[4],
        'receiver_free_cells': capacity - counts[5],
        'coarse_proxy': (counts[4] > 0, counts[5] == capacity),
        'rf_five_class_label': None,
        'rf_label_status': 'UNIDENTIFIABLE_FROM_SINGLE_CHECKPOINT',
        'scope': 'SIMULATOR_STATE_PROXY_NOT_MEASURED_CSI',
    }


def audit_phys04_pairs(rows, *, penalty=60, epsilon=5):
    """Screen PHYS-04 rows, NOT the actual engine run. Never invent outcomes.

    Observation-equivalence uses the *same six-counts* only, capacity,
    intervention contract and geometry. Distinct seed IDs do not prove
    independent arrival tapes. Full geometries can yield no matches.
    """
    if penalty not in (0,60,120) or type(epsilon) not in (int,float) or not isfinite(epsilon) or epsilon < 0:
        raise ValueError('invalid audit parameters')
    if not isinstance(rows, (list,tuple)):
        raise TypeError('rows must be materialized PHYS-04 result records')
    bins = defaultdict(list)
    for row in rows:
        if not isinstance(row,dict) or row.get('checkpoint_identity') is not True:
            raise ValueError('PHYS-04 row without matched checkpoint')
        if type(row.get('capacity')) is not int:
            raise ValueError('receiver capacity missing')
        obs = summarize_checkpoint(row['decision_observation'],receiver_capacity=row['capacity'])
        delta = row.get(f'delta_p{penalty}')
        if type(delta) not in (int,float) or not isfinite(delta):
            raise ValueError('missing/nonfinite synthetic policy delta')
        if type(row.get('seed')) is not int or row['seed'] < 0:
            raise ValueError('seed provenance missing')
        # Only a PHYS-04 row convention: the intervention is held fixed.
        key = (row['capacity'], row['pocket_m'], row['b_share'], obs['six_counts'])
        bins[key].append((row['seed'],delta,obs['coarse_proxy']))
    out = []
    for (cap,pocket_m,b_share,counts), samples in sorted(bins.items()):
        negative = [(s,d) for s,d,_ in samples if d < -epsilon]
        positive = [(s,d) for s,d,_ in samples if d > epsilon]
        if negative and positive:
            out.append({'capacity':cap,'pocket_m':pocket_m,'b_share':b_share,
                        'six_counts':counts,'rows':len(samples),
                        'seed_groups':len({s for s,_,_ in samples}),
                        'opposite_pairs':len(negative)*len(positive),
                        'kind':'CANDIDATE_SIX_COUNT_ALIAS_NOT_CAUSAL_PROOF',
                        'rf_label':None})
    return tuple(out)

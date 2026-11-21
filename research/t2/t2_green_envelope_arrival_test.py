"""Pre-registered T2 green-duration envelope x arrival-clock robustness (seeds88-95).

These are uncalibrated synthetic model actions. A 3s simulated red/no-service
interval is NOT a yellow indication or a certified controller clearance.
"""
import argparse
import collections
import hashlib
import json
from itertools import product
from pathlib import Path
from dual_lane_v11 import run
from physical_transfer_screen import score
from physical_checkpoint_delay_and_shift import make_config
from t2_arrival_clock_experiment import FAMILIES, generate, tape_hash, time_hash

TEST_SEEDS = tuple(range(88,96))
REGIMES = (('left45', 1800, .45), ('demand1650', 1650, .5))
BAYS = (14., 28., 70.)
B_SHARES = (0., .5)
GREEN_TICKS = (4, 8, 12, 20)
TICK = 84


def signal_plan(green_ticks):
    if type(green_ticks) is not int or green_ticks not in GREEN_TICKS:
        raise ValueError('non-preregistered left green duration')
    return ((TICK, TICK+3, '-'),
            (TICK+3, TICK+3+green_ticks, 'L'),
            (TICK+3+green_ticks, 120, '-'))


def experiment():
    rows=[]
    for family, (regime, demand, left), seed, pocket, share in product(
            FAMILIES, REGIMES, TEST_SEEDS, BAYS, B_SHARES):
        cfg = make_config(seed, 4, pocket, share, demand, left)
        tape = generate(cfg.base, family)
        cp = run(cfg, tape, checkpoint_at=TICK)
        baseline = run(cfg, tape, resume_from=cp)
        if baseline != run(cfg, tape):
            raise AssertionError(('checkpoint replay',family,regime,seed,pocket,share))
        if baseline['generated'] != len(tape):
            raise AssertionError('bad generated count')
        outcomes={}
        for width in GREEN_TICKS:
            branch=run(cfg, tape, resume_from=cp, phase_overrides=signal_plan(width))
            if branch['generated'] != branch['network_out_S'] + branch['network_out_L'] + branch['remaining']:
                raise AssertionError('vehicle conservation')
            outcomes[str(width)]={
                'delta_p60': score(branch,60)-score(baseline,60),
                'out_S': branch['network_out_S'],
                'out_L': branch['network_out_L'],
                'remaining': branch['remaining']}
        per_second = collections.Counter(t for t, _ in tape)
        rows.append({
            'family':family,'regime':regime,'demand_vph':demand,'left_fraction':left,
            'seed':seed,'pocket_m':pocket,'b_share':share,
            'number_of_requests':len(tape),'count_before84':sum(t<TICK for t,_ in tape),
            'max_requests_per_second':max(per_second.values(),default=0),
            'time_hash':time_hash(tape),'tape_hash':tape_hash(tape),
            'baseline_cost':score(baseline,60),
            'baseline_out_S':baseline['network_out_S'],
            'baseline_out_L':baseline['network_out_L'],
            'baseline_remaining':baseline['remaining'],
            'plans':outcomes})
    if len(rows)!=288:
        raise AssertionError('bad preregistered cohort')
    summary={}
    for regime,_,_ in REGIMES:
        summary[regime]={}
        for family in FAMILIES:
            subgroup=[r for r in rows if r['regime']==regime and r['family']==family]
            if len(subgroup)!=48:
                raise AssertionError('bad cohort per family')
            by_green={}
            for width in GREEN_TICKS:
                deltas=[r['plans'][str(width)]['delta_p60'] for r in subgroup]
                by_green[str(width)]={
                    'lower':sum(d<0 for d in deltas),
                    'higher':sum(d>0 for d in deltas),
                    'ties':sum(d==0 for d in deltas),
                    'total_delta':sum(deltas),
                    'mean_delta':sum(deltas)/len(deltas),
                    'min_delta':min(deltas),
                    'max_delta':max(deltas)}
            labels={r['seed']:r['time_hash'] for r in subgroup if r['pocket_m']==14. and r['b_share']==0.}
            if len(labels)!=8:
                raise AssertionError('unexpected distinct-seed cohort')
            summary[regime][family]={
                'count':len(subgroup),
                'distinct_timing_tapes':len(set(labels.values())),
                'mean_requested_vehicles':sum(r['number_of_requests'] for r in subgroup)/len(subgroup),
                'min_requested_vehicles':min(r['number_of_requests'] for r in subgroup),
                'max_requested_vehicles':max(r['number_of_requests'] for r in subgroup),
                'max_requests_in_one_second':max(r['max_requests_per_second'] for r in subgroup),
                'by_green':by_green}
    return {
        'status':'SYNTHETIC_UNCALIBRATED_GREEN_ONLY_NOT_LEGAL_FEASIBILITY',
        'protocol':'T2_GREEN_ENVELOPE_AND_ARRIVAL_CLOCK_PREREG',
        'seed_window':[88,95],
        'note':'across arrival families, states and event tapes differ; only within-world policy branches are identical-state contrasts',
        'summary':summary,'worlds':rows}


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('output',type=Path)
    args=ap.parse_args()
    obj=experiment()
    raw=(json.dumps(obj,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()
    args.output.write_bytes(raw)
    print('SHA256',hashlib.sha256(raw).hexdigest())
    print(json.dumps(obj['summary'],indent=2))

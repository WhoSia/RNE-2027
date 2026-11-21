"""Prespecified seed96–103 synthetic arrival-time-only test.

Same total requests, same ordered route labels, separate timing clocks.
Not a same-predecision-state *across* clocks test, and no field validation.
"""
import argparse
import hashlib
import json
import random
from itertools import product
from pathlib import Path

from dual_lane_v11 import run
from spatial_v10 import arrivals
from physical_transfer_screen import score
from physical_checkpoint_delay_and_shift import make_config
from t2_arrival_clock_experiment import time_hash, tape_hash
from t2_green_envelope_arrival_test import signal_plan, GREEN_TICKS

SEEDS = tuple(range(96,104))
REGIMES = (('left45',1800,.45),('demand1650',1650,.5))
BAYS = (14.,28.,70.)
SHARES = (0.,.5)
CLOCKS = ('legacy', 'randomized_timestamps')


def route_matched_tapes(base):
    legacy=arrivals(base)
    rng=random.Random(1107000+base.seed)
    seconds=sorted(rng.randrange(base.duration_s) for _ in legacy)
    randomized=tuple((second,legacy[i][1]) for i,second in enumerate(seconds))
    if len(legacy)!=len(randomized):
        raise AssertionError('count mismatch')
    if tuple(r for _,r in legacy)!=tuple(r for _,r in randomized):
        raise AssertionError('route sequence mismatch')
    return {'legacy':legacy,'randomized_timestamps':randomized}


def experiment():
    rows=[]
    for regime,demand,left in REGIMES:
        for seed,pocket,share in product(SEEDS,BAYS,SHARES):
            c=make_config(seed,4,pocket,share,demand,left)
            tapes=route_matched_tapes(c.base)
            for clock in CLOCKS:
                tape=tapes[clock]
                cp=run(c,tape,checkpoint_at=84)
                original=run(c,tape)
                baseline=run(c,tape,resume_from=cp)
                if baseline!=original:
                    raise AssertionError(('checkpoint mismatch',regime,seed,pocket,share,clock))
                if original['generated']!=len(tape):
                    raise AssertionError('generated mismatch')
                plans={}
                for width in GREEN_TICKS:
                    result=run(c,tape,resume_from=cp,phase_overrides=signal_plan(width))
                    if result['generated']!=result['remaining']+result['network_out_L']+result['network_out_S']:
                        raise AssertionError('vehicle conservation')
                    plans[str(width)]={
                        'delta_p60':score(result,60)-score(baseline,60),
                        'remaining':result['remaining'],
                        'out_S':result['network_out_S'],
                        'out_L':result['network_out_L']}
                rows.append({
                    'regime':regime,'seed':seed,'pocket_m':pocket,'b_share':share,
                    'clock':clock,'total_requests':len(tape),
                    'route_labels_hash':hashlib.sha256(''.join(r for _,r in tape).encode()).hexdigest(),
                    'timestamp_hash':time_hash(tape), 'full_tape_hash':tape_hash(tape),
                    'count_before84':sum(t<84 for t,_ in tape),
                    'baseline_cost':score(baseline,60),'plans':plans})
    if len(rows)!=192:raise AssertionError('incorrect prespecified grid')
    summary={}
    for regime,_,_ in REGIMES:
        r_rows=[r for r in rows if r['regime']==regime]
        by_clock={}
        for clock in CLOCKS:
            ss=[r for r in r_rows if r['clock']==clock]
            by_width={}
            for width in GREEN_TICKS:
                ds=[r['plans'][str(width)]['delta_p60'] for r in ss]
                by_width[str(width)]={
                    'n':len(ds),'better':sum(x<0 for x in ds),'worse':sum(x>0 for x in ds),
                    'tie':sum(x==0 for x in ds),
                    'mean_delta':sum(ds)/len(ds),'sum_delta':sum(ds)}
            by_clock[clock]={
                'n':len(ss),
                'distinct_timing_sequences':len({r['timestamp_hash'] for r in ss}),
                'mean_before84':sum(r['count_before84'] for r in ss)/len(ss),
                'by_width':by_width}
        contrasts=[]
        for seed,pocket,share in product(SEEDS,BAYS,SHARES):
            matches=[next(r for r in r_rows if r['seed']==seed and r['pocket_m']==pocket
                            and r['b_share']==share and r['clock']==clock) for clock in CLOCKS]
            a,b=matches
            if a['total_requests']!=b['total_requests'] or a['route_labels_hash']!=b['route_labels_hash']:
                raise AssertionError('matched route mismatch')
            contrasts.append({
                'seed':seed,'pocket_m':pocket,'b_share':share,
                'legacy_delta4':a['plans']['4']['delta_p60'],
                'random_delta4':b['plans']['4']['delta_p60'],
                'strict_opposite_sign':a['plans']['4']['delta_p60'] * b['plans']['4']['delta_p60'] < 0,
                'zero_nonzero':(a['plans']['4']['delta_p60']==0) != (b['plans']['4']['delta_p60']==0),
                'legacy_before84':a['count_before84'],
                'random_before84':b['count_before84']})
        summary[regime]={
            'by_clock':by_clock,
            'exact_route_match_all':True,
            'strict_sign_oppositions':sum(c['strict_opposite_sign'] for c in contrasts),
            'zero_nonzero_transitions':sum(c['zero_nonzero'] for c in contrasts),
            'contrasts':contrasts}
    return {'status':'SYNTHETIC_UNCALIBRATED_NOT_FIELD_SIGNAL_FEASIBILITY',
            'protocol':'T2_ROUTE_MATCHED_CLOCK_PREREG',
            'seed_window':[96,103],
            'worlds':rows,'summary':summary}


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('output_json',type=Path)
    args=ap.parse_args()
    d=experiment()
    out=(json.dumps(d,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()
    args.output_json.write_bytes(out)
    print('SHA256',hashlib.sha256(out).hexdigest())
    for regime,s in d['summary'].items():
        print(regime,'strict',s['strict_sign_oppositions'], 'zero↔nonzero', s['zero_nonzero_transitions'])
        for clock,v in s['by_clock'].items():
            print(' ',clock,v['by_width'])

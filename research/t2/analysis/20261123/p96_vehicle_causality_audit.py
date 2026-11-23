"""P96: paired vehicle-delay contributions and event-order divergence for source-locked P88 cases.

This script replays representative *cases*, not 192 independently sampled worlds.
Run: python p96_vehicle_causality_audit.py > P96_RESULT.json
"""
from collections import Counter
from dataclasses import replace
from pathlib import Path
import json

from p85_signal_coordination import build_config, p31, run
from p88_spatial_audit import replay, ZONES

HERE = Path(__file__).resolve().parent
CASES = (
    (85004, .25, 'uniform', 'green'),  # green-onset paradox
    (85001, .50, 'uniform', 'red'),    # low-cost red-onset paradox
    (85001, .75, 'uniform', 'red'),    # high-left-share red-onset paradox
    (85001, .25, 'uniform', 'green'),  # both lower control
    (85001, .25, 'uniform', 'red'),    # both lower control
)


def first_difference(a, b):
    for index in range(max(len(a), len(b))):
        av = a[index] if index < len(a) else None
        bv = b[index] if index < len(b) else None
        if av != bv:
            return {'index': index, 'short_30': av, 'long_60': bv}
    return None


def experiment():
    ref = json.loads((HERE/'P87_RESULT.json').read_text())['rows']
    refmap = {(r['seed'],r['share'],r['clock'],r['onset']):r['delta'] for r in ref}
    rows = []
    for seed, share, family, onset in CASES:
        cfg = build_config(seed, 900, share, 7, 4, .5)
        tape = p31.clock(cfg.base, family)
        cfg = replace(cfg, base=replace(cfg.base,duration_s=1440), downstream_offset_s=0)
        cp = run(cfg, tape, checkpoint_at=84, trace=True)
        short = replay(cfg,tape,cp,30,onset)
        long = replay(cfg,tape,cp,60,onset)
        delta = {k:short[k]-long[k] for k in ('cost','denied','full_red')}
        assert delta == refmap[seed,share,family,onset]
        by_car=[]
        for vid,(t,move) in enumerate(tape):
            a=short['vehicle_zones'].get(vid,{})
            b=long['vehicle_zones'].get(vid,{})
            zones={z:a.get(z,0)-b.get(z,0) for z in ZONES}
            by_car.append({'id':vid,'arrival_s':t,'movement':move,'vehicle_seconds_delta':sum(zones.values()),'zone_delta':zones})
        assert sum(v['vehicle_seconds_delta'] for v in by_car)==delta['cost']
        movement_delta={m:sum(v['vehicle_seconds_delta'] for v in by_car if v['movement']==m) for m in ('L','S')}
        assert sum(movement_delta.values())==delta['cost']
        positive=sorted((v for v in by_car if v['vehicle_seconds_delta']>0),
                        key=lambda v:(-v['vehicle_seconds_delta'],v['id']))
        negative=sorted((v for v in by_car if v['vehicle_seconds_delta']<0),
                        key=lambda v:(v['vehicle_seconds_delta'],v['id']))
        rows.append(dict(seed=seed,share=share,clock=family,onset=onset,delta=delta,
                         movement_total_delta=movement_delta,
                         signed_vehicle_cost_total=sum(v['vehicle_seconds_delta'] for v in by_car),
                         positive_vehicle_count=len(positive),negative_vehicle_count=len(negative),
                         zero_vehicle_count=len(by_car)-len(positive)-len(negative),
                         largest_positive=positive[:8], largest_negative=negative[:8],
                         first_stopline_crossing_divergence=first_difference(short['crossings'],long['crossings']),
                         first_downstream_departure_divergence=first_difference(short['downstream_departures'],long['downstream_departures']),
                         first_15_stopline_short=short['crossings'][:15],
                         first_15_stopline_long=long['crossings'][:15],
                         first_15_receiver_short=short['downstream_departures'][:15],
                         first_15_receiver_long=long['downstream_departures'][:15]))
    return {'source':'P87_RESULT.json','verification':'P87 delta identical for every selected case and per-ID signed vehicle-seconds exactly reconstructs cost',
            'warning':'mechanism-level representative examples only; there is no statistical common-cause proof for all 55 pairs',
            'rows':rows}

if __name__=='__main__':
    print(json.dumps(experiment(),indent=2))

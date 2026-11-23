"""P108 post-hoc mechanistic discriminator: final downstream exits across 1 vs 4-cell pocket.

If exit time and ID match per arm, reallocating queue occupancy between lane A
and turn pocket cannot change total vehicle-seconds for fully-cleared runs.
Exploratory test; P106 outcome and P107 absolute invariance already known.
"""
import json
from collections import Counter
from dataclasses import replace
from itertools import product
from pathlib import Path
from p85_signal_coordination import build_config,p31,run
from p88_spatial_audit import replay,ZONES

HERE=Path(__file__).resolve().parent

def experiment():
    ref=json.loads((HERE/'P107_RESULT.json').read_text())
    look={(r['seed'],r['clock'],r['pocket_slots']):r for r in ref['rows']}
    rows=[];counts=Counter()
    for seed,clock in product(range(87001,87009),p31.FAMILIES):
        per_length={}
        for pocket_length in (7,28):
            c=build_config(seed,900,.75,pocket_length,4,.5)
            tape=p31.clock(c.base,clock)
            c=replace(c,base=replace(c.base,duration_s=1440),downstream_offset_s=0)
            cp=run(c,tape,checkpoint_at=84,trace=True)
            per_length[pocket_length]={period:replay(c,tape,cp,period,'red') for period in (30,60)}
        for period in (30,60):
            a=per_length[7][period];b=per_length[28][period]
            assert a['cost']==b['cost']==look[seed,clock,1][('short' if period==30 else 'long')]['cost']
            events_a=[(e['t'],e['id'],e['movement']) for e in a['downstream_departures']]
            events_b=[(e['t'],e['id'],e['movement']) for e in b['downstream_departures']]
            ordered_identical=events_a==events_b
            per_car_changes=[]
            for vid in set(a['vehicle_zones'])|set(b['vehicle_zones']):
                d=sum(b['vehicle_zones'].get(vid,{}).get(z,0)-a['vehicle_zones'].get(vid,{}).get(z,0) for z in ZONES)
                if d!=0:per_car_changes.append((vid,d))
            counts['n']+=1
            counts['network_cost_identical']+=a['cost']==b['cost']
            counts['all_downstream_exit_events_identical']+=ordered_identical
            counts['all_per_vehicle_cost_identical']+=not per_car_changes
            rows.append(dict(seed=seed,clock=clock,period=period,
                             cost_same=a['cost']==b['cost'],cost=a['cost'],
                             downstream_exit_same=ordered_identical,
                             downstream_departures=len(events_a),
                             per_car_cost_difference_count=len(per_car_changes),
                             per_car_difference_examples=per_car_changes[:12],
                             original_first_exit=events_a[:4],expanded_first_exit=events_b[:4]))
    assert counts['n']==32 and counts['network_cost_identical']==32
    return dict(status='exploratory trace replay',comparison='7m (1 cell) vs 28m (4 cells)',
                unique_tapes=16,period_conditions=2,paired_geometry_comparisons=32,
                simulator_arms=64,counts=dict(counts),rows=rows,
                caveat='Identity inside one deterministic simulator; not a calibrated headway or field observation')

if __name__=='__main__':
    print(json.dumps(experiment(),ensure_ascii=False,indent=2))

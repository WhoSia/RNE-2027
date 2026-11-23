"""P111 frozen input/event contract for future INDEPENDENT T2/SUMO comparison.

This emits T2-side reference behavior and a separate source-neutral arrivals/phase
manifest. It NEVER claims SUMO was installed, geometry-matched, or executed.
"""
import hashlib
import json
from dataclasses import asdict, replace
from pathlib import Path
from itertools import product
from p85_signal_coordination import build_config, p31, run
from p88_spatial_audit import replay
from spatial_v10 import validate

HERE = Path(__file__).resolve().parent
SEEDS=(86001,86002)
FAMILIES=('uniform','platoon4')
ONSETS=('green','red')
PERIODS=(30,60)


def stable_sha(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=True,separators=(',',':')).encode()).hexdigest()


def downstream_green(t,period,onset):
    assert 84<=t<1440
    return ((t-84)%period<period//2)==(onset=='green')


def intervals(period,onset):
    spans=[]
    on=None
    for t in range(84,1440):
        v=downstream_green(t,period,onset)
        if on is None: on=(t,v)
        elif v!=on[1]:
            spans.append(dict(start_s=on[0],end_s=t,green=on[1]))
            on=(t,v)
    spans.append(dict(start_s=on[0],end_s=1440,green=on[1]))
    assert sum(x['end_s']-x['start_s'] for x in spans)==1356
    return spans


def experiment():
    # This is a selected **pilot subset** of P100, not a new random holdout.
    reference=json.loads((HERE/'P101_RESULT.json').read_text())
    lookup={(r['seed'],r['clock'],r['onset']):r for r in reference['rows']}
    tapes=[]
    arms=[]
    for seed,family in product(SEEDS,FAMILIES):
        cfg=build_config(seed,900,.75,7,4,.5)
        n,k=validate(cfg.base)
        assert (n,k)==(20,1)
        tape=p31.clock(cfg.base,family)
        cfg=replace(cfg,base=replace(cfg.base,duration_s=1440),downstream_offset_s=0)
        cp=run(cfg,tape,checkpoint_at=84,trace=True)
        incoming=[{'vehicle_id':i,'enter_time_s':t,'movement':m} for i,(t,m) in enumerate(tape)]
        assert sum(1 for x in incoming if x['movement']=='L')+sum(1 for x in incoming if x['movement']=='S')==len(incoming)
        common=dict(seed=seed,family=family,events=incoming,arrival_sha256=stable_sha(incoming),
                    initial_state=repr(cp['state']['receiver'].snapshot()))
        tapes.append(common)
        for onset in ONSETS:
            one={}
            for period in PERIODS:
                r=replay(cfg,tape,cp,period,onset)
                predecision_exits=[{'t':t,'id':vid,'movement':movement} for t,vid,movement in cp['state']['receiver'].exits]
                exits=predecision_exits+r['downstream_departures']
                assert len(exits)==len(incoming)
                assert len(predecision_exits)==cp['state']['count']['network_out_L']+cp['state']['count']['network_out_S']
                assert len(exits)==len({x['id'] for x in exits})
                assert all(x['movement'] in ('L','S') for x in exits)
                one[period]=r
                signal=intervals(period,onset)
                arms.append(dict(seed=seed,family=family,onset=onset,period_s=period,
                                 t2_cost=r['cost'],t2_receiver_denied=r['denied'],
                                 calendar=signal,calendar_sha256=stable_sha(signal),
                                 terminal_exits=exits,terminal_exit_sha256=stable_sha(exits),
                                 count_terminal_exits=len(exits),
                                 observed_time_reference='T2 integer tick, end-of-receiver event, not SUMO second'))
            d=lookup[seed,family,onset]['delta']
            assert one[30]['cost']-one[60]['cost']==d['cost']
            assert one[30]['denied']-one[60]['denied']==d['denied']
    assert len(tapes)==4 and len(arms)==16
    return dict(status='T2_REFERENCE_ONLY_INDEPENDENT_ENGINE_NOT_RUN',
                source='P101_RESULT.json and unchanged current dual_lane_v11/receiving_cells_v15',
                pilot_seed_blocks=len(SEEDS),unique_arrival_tapes=len(tapes),
                comparator_pairs=8,arms=len(arms),
                model=dict(approach_cells=20,cell_m=7,approach_m=140,pocket_cells=1,pocket_m=7,
                           receiver_cells=4,receiver_nominal_m=28,receiver_exit_headway_s=2,
                           through_B_share=.5,decision_second=84,phase_type='left_first 6-second left',
                           terminal_time_resolution_s=1, postdecision_horizon_s=1356),
                rules=['All vehicle IDs and arrival times must match at network entry',
                       'T2 checkpoint state at t84 cannot be silently interpreted as SUMO state',
                       'A SUMO scenario with realistic car following is not exact cellular geometry',
                       'No policy sign comparison until each simulator network length/phase/route/terminal definition is reconciled',
                       'Only compare identical completed-ID sets; unmatched IDs are failures not dropped data'],
                tapes=tapes,arms_data=arms)


if __name__=='__main__':
    print(json.dumps(experiment(),ensure_ascii=False,indent=2))

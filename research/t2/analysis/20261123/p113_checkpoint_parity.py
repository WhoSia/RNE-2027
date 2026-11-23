"""P113: export the complete *observable* T2 state at the t=84 split.

P111's receiver-only snapshot cannot be used to initialize another engine;
this supplement exports queued approach/pocket/outside identities and movement
with exact T2 cells. Velocities in a car-following engine remain UNKNOWN.
"""
import json
import ast
from dataclasses import replace
from itertools import product
from pathlib import Path
from p85_signal_coordination import build_config,p31,run
from spatial_v10 import validate

HERE=Path(__file__).resolve().parent

def extract(cp,tape):
    st=cp['state']; t=cp['next_tick']
    assert t==84
    groups={}
    for key in ('A','B','pocket'):
        groups[key]=[{'cell':cell,'vehicle_id':v[0],'movement':v[1],
                      'arrived_second':v[2]} for cell,v in sorted(st[key].items())]
    groups['receiver']=[{'cell':i,'vehicle_id':vid,'movement':move} for i,vid,move in st['receiver'].snapshot()]
    groups['outside']=[{'queue':name,'vehicle_id':v[0],'movement':v[1],
                        'arrived_second':v[2]}
                       for name in ('A','B') for v in st['outside'][name]]
    ids=[x['vehicle_id'] for g in groups.values() for x in g]
    assert len(ids)==len(set(ids)), 'duplicate present vehicle ID'
    departed=[{'t':s,'vehicle_id':vid,'movement':move} for s,vid,move in st['receiver'].exits]
    departed_ids=[e['vehicle_id'] for e in departed]
    assert len(departed_ids)==len(set(departed_ids))
    seen=set(ids)|set(departed_ids)
    assert len(seen)==st['index'] and seen==set(range(st['index'])), 'missing predecision ID'
    assert len(ids)+len(departed)==st['index']
    for group in groups.values():
        for x in group:
            vid=x['vehicle_id'];assert vid<len(tape) and x['movement']==tape[vid][1]
    return {'decision_s':t,'processed_tape_arrivals':st['index'],
            'predecision_departed':len(departed),'predecision_active':len(ids),
            'predecision_departures':departed,'occupied_groups':groups,
            'receiver_last_exit_second':st['receiver'].last_exit,
            'last_upstream_stopline':dict(st['last']),
            'last_admission':dict(st['admission']),
            'unobserved_car_following_velocities':True,
            'warning':'A state with cell locations and IDs is NOT a SUMO physical state: velocities, lane-change execution and driver dynamics must be independently specified.'}

def experiment():
    ref=json.loads((HERE/'P111_RESULT.json').read_text())
    source={(t['seed'],t['family']):t for t in ref['tapes']}
    records=[]
    for seed,family in product((86001,86002),('uniform','platoon4')):
        cfg=build_config(seed,900,.75,7,4,.5)
        assert validate(cfg.base)==(20,1)
        tape=p31.clock(cfg.base,family)
        cfg=replace(cfg,base=replace(cfg.base,duration_s=1440))
        cp=run(cfg,tape,checkpoint_at=84,trace=True)
        entry=extract(cp,tape)
        assert len(tape)==len(source[seed,family]['events'])
        assert len(entry['occupied_groups']['receiver'])==len(ast.literal_eval(source[seed,family]['initial_state']))
        records.append({'seed':seed,'family':family,'checkpoint':entry})
    assert len(records)==4
    return {'status':'T2_CHECKPOINT_STATE_EXPORTED_NOT_SUMO_PARITY',
            'tape_states':4,'id_conservation_passed':4,
            'full_predecision_departure_included':True,
            'physically_unobserved_velocity_count':'all present vehicle IDs',
            'records':records}

if __name__=='__main__':
    print(json.dumps(experiment(),ensure_ascii=False,indent=2))

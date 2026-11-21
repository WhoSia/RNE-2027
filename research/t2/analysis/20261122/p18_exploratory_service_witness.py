"""Post-hoc P18 exploratory event-level witness; synthetic simulator only."""
from pathlib import Path
import json
import hashlib
import pickle
from p18_clock_position_action import build_config,arrival_clock_pair,OVERRIDES,PENALTY
from dual_lane_v11 import run
from physical_transfer_screen import score


def witness():
    config=build_config(105,1650,.5,14.,4,.5)
    tape,_=arrival_clock_pair(config.base)
    checkpoint=run(config,tape,checkpoint_at=84,trace=True)
    ck_sha=hashlib.sha256(pickle.dumps(checkpoint,protocol=4)).hexdigest()
    paths={}
    for name,override in [('baseline',()),('left_4s',OVERRIDES['left_4s']),('left_8s',OVERRIDES['left_8s'])]:
        r=run(config,tape,resume_from=checkpoint,phase_overrides=override,trace=True)
        events=[{'tick':e['t'],'reason':e['reason'],'movement':e['movement']}
                for e in r['service_events']
                if 84<=e['t']<=129 and e.get('movement')=='L']
        paths[name]={
            'score':score(r,PENALTY),'generated':r['generated'],
            'network_out_S':r['network_out_S'],'network_out_L':r['network_out_L'],
            'remaining':r['remaining'],
            'outside_vehicle_seconds':r['outside_vehicle_seconds'],
            'upstream_vehicle_seconds':r['upstream_vehicle_seconds'],
            'receiver_vehicle_seconds':r['receiver_vehicle_seconds'],
            'left_turn_service_events_tick84_to129':events,
        }
    assert all(v['generated']==len(tape) for v in paths.values())
    assert hashlib.sha256(pickle.dumps(checkpoint,protocol=4)).hexdigest()==ck_sha
    return {
        'status':'EXPLORATORY_POSTHOC_EVENT_WITNESS_SYNTHETIC_ONLY',
        'case':{'seed':105,'demand_vph':1650,'left_fraction':.5,'pocket_m':14,
                'receiver_capacity':4,'b_share':.5,'clock':'legacy','decision_tick':84},
        'checkpoint_sha256':ck_sha,
        'paths':paths,
        'eight_minus_four_score':paths['left_8s']['score']-paths['left_4s']['score'],
        'caveat':'Temporal event trace shows changed later receiver admission but not isolated causal mediator identification.'
    }


if __name__=='__main__':
    import argparse
    a=argparse.ArgumentParser();a.add_argument('output',type=Path);args=a.parse_args()
    args.output.write_text(json.dumps(witness(),ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')

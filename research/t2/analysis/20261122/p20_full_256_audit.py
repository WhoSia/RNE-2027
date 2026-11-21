"""P20 complete P19-compatible, exact-core event audit. Synthetic only."""
from dataclasses import replace
from itertools import product
import json
from pathlib import Path
from dual_lane_v11 import run
from p19_receiver_service_opportunity import (REGIMES,SEEDS,RECEIVERS,OFFSETS,POCKETS,B_SHARES,ACTION,
    build_config,arrival_clock_pair,tape_hash)
from p20_independent_receiver_ledger import audit_trace
from physical_transfer_screen import score


def experiment():
    records=[]; tapes=set()
    for (demand,turn),seed,capacity,offset,pocket,bshare in product(REGIMES,SEEDS,RECEIVERS,OFFSETS,POCKETS,B_SHARES):
        cfg=replace(build_config(seed,demand,turn,pocket,capacity,bshare),downstream_offset_s=offset)
        _,tape=arrival_clock_pair(cfg.base)
        tapes.add(tape_hash(tape))
        cp=run(cfg,tape,trace=True,checkpoint_at=84)
        control=run(cfg,tape,resume_from=cp,trace=True)
        treatment=run(cfg,tape,resume_from=cp,trace=True,phase_overrides=ACTION)
        shadows=[audit_trace(cfg,tape,r) for r in (control,treatment)]
        records.append(dict(demand_vph=demand,turn_share=turn,seed=seed,pocket_m=pocket,
            capacity=capacity,offset_s=offset,b_share=bshare,tape_sha=tape_hash(tape),
            policy_cost_delta=score(treatment,60)-score(control,60),
            branches=[dict(branch=name,admitted=v['receiver_admissions'],
                receiver_exits=v['receiver_exits'],denials=v['receiver_denials'],
                final_receiver=v['last_tick_conservation']['receiver_size'])
                for name,v in zip(('baseline','treatment'),shadows)]))
    return {'experiment':'P20_COMPLETE_P19_EXACT_SOURCE_SHADOW',
        'status':'INDEPENDENT_CELLULAR_SHADOW_NO_SUMO_NO_REAL_WORLD',
        'worlds':len(records),'paths_audited':2*len(records),
        'ticks':240*2*len(records),'unique_tape_hashes':len(tapes),
        'receiver_admissions':sum(x['admitted'] for r in records for x in r['branches']),
        'receiver_exits':sum(x['receiver_exits'] for r in records for x in r['branches']),
        'receiver_denials':sum(x['denials'] for r in records for x in r['branches']),
        'records':records}

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('output',type=Path);args=parser.parse_args()
    args.output.write_text(json.dumps(experiment(),sort_keys=True,indent=2)+'\n',encoding='utf-8')

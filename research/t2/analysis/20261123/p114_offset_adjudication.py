"""P114 preregistered offset-period 360-arm pilot; no field or SUMO claim."""
import json, statistics, math
from dataclasses import replace
from itertools import product
from collections import Counter
from pathlib import Path
from unittest.mock import patch
from receiving_cells_v15 import ReceivingCells
from p85_signal_coordination import build_config,p31,run,score,phases
from spatial_v10 import phase, validate

OUT=Path(__file__).with_name('P114_RESULT.json')
DURATION=4800
T0=84

def signal(cfg,t):
    return next((v for a,b,v in phases(6,'left_first') if a<=t<b),phase(cfg.base,t))

def overlap(cfg,period,offset,a=84,b=400):
    return sum(signal(cfg,t)=='L' and ((t-T0-offset)%period)<period//2 for t in range(a,b))

def arm(cfg,tape,cp,period,offset):
    def green(self,t):
        if t<84:raise AssertionError('receiver green touched before checkpoint')
        return ((t-T0-offset)%period)<period//2
    with patch.object(ReceivingCells,'green',green):
        r=run(cfg,tape,resume_from=cp,phase_overrides=phases(6,'left_first'))
    return {'period_s':period,'offset_s':offset,'cost':score(r,0),
            'remaining':r['remaining'],'generated':r['generated'],
            'out_L':r['network_out_L'],'out_S':r['network_out_S'],
            'receiver_denied_s':r['receiver_denied_seconds'],
            'left_green_overlap_t84_400':overlap(cfg,period,offset)}

def main():
    rows=[]
    for seed,family in product((86001,86002),('uniform','platoon4')):
        cfg=build_config(seed,900,.75,7,4,.5)
        assert validate(cfg.base)==(20,1)
        tape=p31.clock(cfg.base,family)
        cfg=replace(cfg,base=replace(cfg.base,duration_s=DURATION),downstream_offset_s=0)
        cp=run(cfg,tape,checkpoint_at=T0)
        trials=[]
        for period in (30,60):
            for offset in range(period):
                x=arm(cfg,tape,cp,period,offset)
                assert x['generated']==len(tape)==60
                assert x['remaining']==0 and x['out_L']+x['out_S']==60, (seed,family,x)
                trials.append(x)
        by={p:[r for r in trials if r['period_s']==p] for p in (30,60)}
        summary={str(p):{'mean':statistics.mean(x['cost'] for x in by[p]),
                         'median':statistics.median(x['cost'] for x in by[p]),
                         'min':min(x['cost'] for x in by[p]),
                         'max':max(x['cost'] for x in by[p]),
                         'argmin':[x['offset_s'] for x in by[p] if x['cost']==min(q['cost'] for q in by[p])]} for p in (30,60)}
        g={p:next(x for x in by[p] if x['offset_s']==0) for p in (30,60)}
        red={p:next(x for x in by[p] if x['offset_s']==p//2) for p in (30,60)}
        summary['contrasts_30_minus_60']={
            'green_start':g[30]['cost']-g[60]['cost'],
            'red_start':red[30]['cost']-red[60]['cost'],
            'mean_over_offset':summary['30']['mean']-summary['60']['mean'],
            'minimum_over_offset':summary['30']['min']-summary['60']['min'],
            'exists_30_worse':max(x['cost'] for x in by[30])>min(x['cost'] for x in by[60]),
            'exists_30_better':min(x['cost'] for x in by[30])<max(x['cost'] for x in by[60]),
        }
        rows.append(dict(seed=seed,family=family,arrival_time_vector=tuple(t for t,_ in tape),summary=summary,arms=trials))
        print(f'FINISHED {seed} {family}: {summary["contrasts_30_minus_60"]}',flush=True)
    times={fam:{tuple(r['arrival_time_vector']) for r in rows if r['family']==fam} for fam in ('uniform','platoon4')}
    assert all(len(v)==1 for v in times.values())
    counts=Counter()
    for row in rows:
        c=row['summary']['contrasts_30_minus_60']
        for k in ('green_start','red_start','mean_over_offset','minimum_over_offset'):
            counts[k+'_30_better']+=c[k]<0
            counts[k+'_30_worse']+=c[k]>0
        counts['both_cost_directions_possible']+=c['exists_30_worse'] and c['exists_30_better']
    result={'status':'P114_360_ARM_REPLAY_COMPLETE_SYNTHETIC_ONLY','prereg':'P114_CLAUDE_OFFSET_ADJUDICATION_PREREG.md',
            'seed_blocks':2,'unique_label_tapes':4,'distinct_temporal_arrival_vectors':2,
            'arms':360,'period_offsets':{'30':30,'60':60},'all_clear':True,
            'summary':dict(counts),'rows':rows,
            'caveat':'Phase offset changes initial green/red and periodic overlap; phase period causal effects cannot be isolated from selected onset pairs; 4 label tapes do not test temporal demand variability.'}
    OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('RESULT',json.dumps({'summary':result['summary'],'arms':360},ensure_ascii=False))
if __name__=='__main__':main()

"""P101 preregistered spatial/movement replay of P100 high-left-share held-out cohort."""
from collections import Counter,defaultdict
from dataclasses import replace
from itertools import product
import json
from pathlib import Path
from p85_signal_coordination import build_config,p31,run
from p88_spatial_audit import replay,ZONES

HERE=Path(__file__).resolve().parent

def experiment():
    source=json.loads((HERE/'P100_RESULT.json').read_text())
    ref={(r['seed'],r['share'],r['clock'],r['onset']):r['delta'] for r in source['rows']}
    assert len(ref)==384
    rows=[]; summary=defaultdict(Counter)
    for seed,clock in product(range(86001,86033),p31.FAMILIES):
        share=.75
        cfg=build_config(seed,900,share,7,4,.5)
        tape=p31.clock(cfg.base,clock)
        cfg=replace(cfg,base=replace(cfg.base,duration_s=1440),downstream_offset_s=0)
        cp=run(cfg,tape,checkpoint_at=84,trace=True)
        for onset in ('green','red'):
            short,long=(replay(cfg,tape,cp,p,onset) for p in (30,60))
            delta={k:short[k]-long[k] for k in ('cost','denied','full_red')}
            assert delta==ref[seed,share,clock,onset]
            zones={z:short['zones'][z]-long['zones'][z] for z in ZONES}
            by_move={m:{z:short['by_movement'][m].get(z,0)-long['by_movement'][m].get(z,0) for z in ZONES} for m in ('L','S')}
            move_total={m:sum(by_move[m].values()) for m in ('L','S')}
            assert sum(zones.values())==sum(move_total.values())==delta['cost']
            assert all(sum(by_move[m][z] for m in ('L','S'))==zones[z] for z in ZONES)
            group=summary[onset]
            group['n']+=1
            group['paradox']+=(delta['denied']<0<delta['cost'])
            group['left_cost_positive']+=(move_total['L']>0)
            group['through_cost_negative']+=(move_total['S']<0)
            group['A_positive']+=(zones['approach_A']>0)
            group['B_negative']+=(zones['approach_B']<0)
            group['A_positive_B_negative']+=(zones['approach_A']>0 and zones['approach_B']<0)
            group['outside_positive']+=(zones['outside']>0)
            group['cost_sum']+=delta['cost']
            for z in ZONES:group['zone_sum_'+z]+=zones[z]
            for m in ('L','S'):group['movement_sum_'+m]+=move_total[m]
            rows.append(dict(seed=seed,share=share,clock=clock,onset=onset,delta=delta,
                             zones=zones,movement_zones=by_move,movement_total=move_total))
    assert len(rows)==128 and summary['red']['n']==64 and summary['green']['n']==64
    criteria={'left_58_of_64':summary['red']['left_cost_positive']>=58,
              'A_58_of_64':summary['red']['A_positive']>=58,
              'B_58_of_64':summary['red']['B_negative']>=58}
    return dict(prereg='P101_MECHANISM_PREREG.md',reference='P100_RESULT.json',
                scope='64 held-out synthetic tapes, red and green onsets paired',
                pairs=128,arms=256,zero_remaining=True,identities_passed=128,
                prereg_criteria=criteria,
                summary={k:dict(v) for k,v in summary.items()},rows=rows)

if __name__=='__main__':
    print(json.dumps(experiment(),indent=2))

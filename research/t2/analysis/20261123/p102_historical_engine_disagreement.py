"""P102: independent re-aggregation of archived P71 cross-engine sign disagreement.

This runs on stored P71 outputs; it is not a new SUMO execution. Never use the
same numbers as a transport estimate for P100 or the P87 30s/60s comparison.
"""
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent

def sign(x):
    return int(x>0)-int(x<0)

def experiment():
    rows=json.loads((HERE/'P71_RESULT.json').read_text())
    assert len(rows)==64 and len({r['seed'] for r in rows})==64
    offsets=[]
    for i,offset in enumerate((0,15)):
        t2=[sign(x['t2'][i]) for x in rows]
        sumo=[sign(x['sumo'][i]) for x in rows]
        offsets.append(dict(offset=offset,exact_sign=sum(a==b for a,b in zip(t2,sumo)),
                            strict_opposite_sign=sum(a*b==-1 for a,b in zip(t2,sumo)),
                            t2_ten_better=sum(a<0 for a in t2),
                            sumo_ten_better=sum(a<0 for a in sumo),
                            t2_ten_worse=sum(a>0 for a in t2),
                            sumo_ten_worse=sum(a>0 for a in sumo)))
    offset_contrasts={
        't2_six_better_at_0_ten_better_at_15':sum(x['t2'][0]>0>x['t2'][1] for x in rows),
        'sumo_ten_better_at_0_six_better_at_15':sum(x['sumo'][0]<0<x['sumo'][1] for x in rows),
    }
    assert [o['exact_sign'] for o in offsets]==[13,2]
    assert [o['strict_opposite_sign'] for o in offsets]==[16,40]
    assert offset_contrasts=={
        't2_six_better_at_0_ten_better_at_15':7,
        'sumo_ten_better_at_0_six_better_at_15':34,
    }
    return dict(source='P71_RESULT.json',evidence='re-analysis of PREEXISTING independent-engine SUMO 64-seed comparison, not fresh SUMO runs',
                comparator='left green 10s minus 6s at offset 0 or 15, NOT P87 downstream 30s minus 60s',
                offsets=offsets,offset_contrasts=offset_contrasts,
                caveats=['T2 and SUMO physical lane/receiver geometry were not matched in P71',
                         'no P100/P101 seed or intervention identity with P71',
                         'sign agreement alone cannot establish field fidelity',
                         'P80/P81 real nocturnal trajectories lack physical end-of-link downstream exits'],
                mandatory_next='reconstruct equivalent lane geometry, movement turn paths, downstream clock and storage in independent engine, then sample exactly the P100 tapes')

if __name__=='__main__':
    print(json.dumps(experiment(),indent=2))

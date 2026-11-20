"""Exact two-action minimax regret with binary noisy observations across finite worlds.

Worlds use the already published SYNTHETIC exhibit, not field traffic.
A structural bypass setting is not assumed to be a measured field sensor.
"""
from fractions import Fraction as F
from itertools import combinations
from collections import defaultdict
import argparse
import json
from pathlib import Path

ARRIVALS = (
    (0,0,0),(0,0,1),(0,1,0),(0,1,1),
    (1,0,0),(1,0,1),(1,1,0),(1,1,1),
)
DELTA = {
    0: (109,312,-27,176,145,346,9,210),
    1: (-822,-932,-720,-830,-822,-932,-720,-830),
    3: (-408,-408,-408,-408,-484,-484,-484,-484),
}

def deterministic_regret(values):
    v=tuple(values)
    return min(max(0,max(v)),max(0,-min(v)))

def randomized_regret(values):
    v=tuple(values)
    a=max(0,-min(v));b=max(0,max(v))
    return F(a*b,a+b) if a+b else F(0)

def partitioned_regret(worlds, key):
    partitions=defaultdict(list)
    for mode,bits,d in worlds:
        partitions[key(mode,bits)].append(d)
    return max(randomized_regret(v) for v in partitions.values())

def worlds(modes=(0,1)):
    return [(m,bits,d) for m in modes for bits,d in zip(ARRIVALS,DELTA[m])]

def det3(mat):
    a,b,c=mat
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])

def solve3(rows):
    A=[list(row[:3]) for row in rows]
    d=det3(A)
    if not d:return None
    b=[row[3] for row in rows]
    return tuple(det3([[b[i] if j==k else A[i][j] for j in range(3)] for i in range(3)])/d
                 for k in range(3))

def binary_noisy_regret(worlds, bit, error):
    """LP vertices solve min max over worlds and errors in {0,epsilon}, p0,p1 in [0,1]."""
    e=F(error)
    if not 0<=e<=1:raise ValueError('error must be in [0,1]')
    rows=set()
    for mode,bits,d in worlds:
        label=bit(mode,bits)
        if label not in (0,1):raise ValueError('forecast label must be binary')
        for q in (F(0),e):
            weights=(1-q,q) if label==0 else (q,1-q)
            if d>=0:
                rows.add((F(d)*weights[0],F(d)*weights[1],F(-1),F(0)))
            else:
                a=F(-d)
                rows.add((-a*weights[0],-a*weights[1],F(-1),-a))
    rows.update({(F(1),F(0),F(0),F(1)),(F(-1),F(0),F(0),F(0)),
                 (F(0),F(1),F(0),F(1)),(F(0),F(-1),F(0),F(0)),
                 (F(0),F(0),F(-1),F(0))})
    constraints=sorted(rows)
    best=None
    for chosen in combinations(constraints,3):
        candidate=solve3(chosen)
        if candidate is None or any(sum(a*b for a,b in zip(row[:3],candidate))>row[3]
                                    for row in constraints):continue
        if best is None or candidate[2]<best[2]:best=candidate
    if best is None:raise RuntimeError('binary forecast LP infeasible')
    return best

def as_str(x):return str(x)

def report():
    mixed=worlds((0,1))
    no_bypass=worlds((0,))
    baseline={
        'mode_0_no_bypass':{'deterministic':deterministic_regret(d for _,_,d in no_bypass),
                            'randomized':as_str(randomized_regret(d for _,_,d in no_bypass))},
        'both_modes_unknown':{'deterministic':deterministic_regret(d for _,_,d in mixed),
                              'randomized':as_str(randomized_regret(d for _,_,d in mixed))},
        'true_mode_known':as_str(partitioned_regret(mixed,lambda mode,bits:mode)),
        'future_order_known_but_mode_hidden':as_str(partitioned_regret(mixed,lambda mode,bits:bits)),
        'future_order_and_mode_known':as_str(partitioned_regret(mixed,lambda mode,bits:(mode,bits))),
    }
    observations={}
    for e in (F(0),F(1,10),F(3,10),F(1,2)):
        rows={}
        for name,key in [('physical_mode',lambda m,b:int(m==1)),
                         *[(f'arrival_bit_{i}',lambda m,b,i=i:b[i]) for i in range(3)]]:
            p0,p1,t=binary_noisy_regret(mixed,key,e)
            rows[name]={'regret':as_str(t),'p_left_on_label_0':as_str(p0),
                        'p_left_on_label_1':as_str(p1)}
        observations[str(e)]=rows
    return {'source':'Eight fixed synthetic exhibit arrival worlds; bypass modes 0 and 1',
            'baselines':baseline,'binary_forecast_error_by_actual_world':observations,
            'warning':'Structural bypass mode is a hypothetical pre-decision measurement, not an observed camera classifier.'}

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('output',type=Path);args=a.parse_args()
    args.output.write_text(json.dumps(report(),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

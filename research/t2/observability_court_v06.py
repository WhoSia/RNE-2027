"""T2 v0.6: observational equivalence and hidden-mechanism witness search.

A constructive identifiability audit: two distinct explicit arrival histories
can have the same partial observation while their internal fork-block event
counts differ. This is not a claim about identifiable driver identities or
real-world LPR accuracy. Designed for a small finite, auditable search.
"""
from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass, replace
from itertools import combinations
from spatial_v05 import Config, simulate


@dataclass(frozen=True)
class Observation:
    total_arrivals: int
    total_left: int
    through_exits: int
    left_exits: int


def project(result: dict, n_arrivals: int, n_left: int) -> Observation:
    """Coarse counts with no microscopic space-time paths or vehicle IDs."""
    return Observation(n_arrivals,n_left,
        result['route_exits'].get('S',0),result['route_exits'].get('L',0))


def hidden_signature(result: dict) -> tuple[int,int,int]:
    s=result['stats']
    return (s.get('fork_block_cap_s',0),
            s.get('fork_block_gap_bay_s',0),
            s.get('fork_block_gap_downstream_s',0))


def enumerate_witness(*, n: int=8, left: int=4, duration: int=150,
                       fork: int=-13, cap: int=2,
                       signal_mode: str='leading') -> dict:
    """Exact search on C(n,left) permutations under a fixed timestamp stream.

    Every input is identical in timestamp sequence, total left/through count,
    initial lane assignment and model config; only route-order differs.
    This search is intentionally deterministic and small, and reports when
    no witness is found instead of manufacturing one.
    """
    if not (2 <= n <= 16 and 1 <= left < n):
        raise ValueError('finite bounds 2<=n<=16, 1<=left<n required')
    c=Config(duration=duration,demand_vph=0,left_fraction=0,
             fork_cells=fork,bay_limit=cap,signal_mode=signal_mode,
             clearance_s=3,update_mode='parallel')
    seen={}
    searched=0
    for positions in combinations(range(n),left):
        left_set=set(positions)
        arrivals=tuple((i,'L' if i in left_set else 'S','upstream') for i in range(n))
        result=simulate(c,arrivals,audit=True)
        obs=project(result,n,left)
        hidden=hidden_signature(result)
        searched+=1
        if obs in seen and seen[obs]['signature']!=hidden:
            prev=seen[obs]
            return {
                'status':'WITNESS_FOUND','searched':searched,
                'observation':vars(obs),
                'A':{'routes':prev['routes'],'hidden_signature':prev['signature']},
                'B':{'routes':''.join('L' if i in left_set else 'S' for i in range(n)),
                     'hidden_signature':hidden},
                'config':{'duration':duration,'fork':fork,'cap':cap,
                          'signal_mode':signal_mode,'update_mode':'parallel'},
                'interpretation':'noninjective count projection and differing internal blocking counters'}
        seen.setdefault(obs,{'routes':''.join('L' if i in left_set else 'S' for i in range(n)),
                             'signature':hidden})
    return {'status':'NO_WITNESS_IN_ENUMERATED_DOMAIN',
            'searched':searched,'distinct_observations':len(seen),
            'domain':{'n':n,'left':left,'duration':duration,'fork':fork,'cap':cap}}


if __name__=='__main__':
    import json
    for n,left in ((8,4),(10,5),(12,6)):
        print(json.dumps(enumerate_witness(n=n,left=left),indent=2))

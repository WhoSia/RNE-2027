"""Finite observational-equivalence example; not a traffic controller."""
from fractions import Fraction as F
from itertools import product
import json

WORLDS = [(F(0), F(18,100)), (F(1,10), F(1,10)), (F(18,100), F(0))]


def solve(ratio):
    laws = [[(t,a,b,F(1,2)*(1-ea if a==t else ea)*(1-eb if b==t else eb))
             for t,a,b in product(range(2),repeat=3)] for ea,eb in WORLDS]
    observed = [[sum(w for t,a,b,w in law if 2*a+b==k) for k in range(4)] for law in laws]
    assert all(x == [F(41,100),F(9,100),F(9,100),F(41,100)] for x in observed)
    risks = [[sum(w*(ratio if t==1 else 1) for t,a,b,w in law if t != ((m>>(2*a+b))&1))
              for law in laws] for m in range(16)]
    oracle = [min(r[i] for r in risks) for i in range(3)]
    regrets = [max(r[i]-oracle[i] for i in range(3)) for r in risks]
    best = min(regrets)
    # Compare a randomized disagreement rule against the deterministic optimum.
    p = ratio/(1+ratio)
    randomized = [sum(w*(ratio*(1-(F(a) if a==b else p)) if t else (F(a) if a==b else p))
                      for t,a,b,w in law) for law in laws]
    randomized_regret = max(r-o for r,o in zip(randomized,oracle))
    # In the two opposite perfect-channel worlds, averaging their risks gives
    # a lower bound of 0.09*min(ratio,1), valid even for randomized rules.
    lower = F(9,100)*min(ratio,1)
    assert best == lower
    assert randomized_regret >= lower
    return {'ratio':str(ratio),'best_masks':[m for m,r in enumerate(regrets) if r==best],
            'minimax_regret':str(best),'and':str(regrets[8]),'or':str(regrets[14]),
            'A':str(regrets[12]),'B':str(regrets[10]),'randomized_example':str(randomized_regret)}


if __name__=='__main__':
    print(json.dumps([solve(r) for r in [F(1,4),F(1,2),F(1),F(2),F(4),F(8)]],indent=2))

"""Exact abstract receiver observability, not physical sensor placement."""
from collections import deque
from itertools import product, combinations
from functools import lru_cache
import json
from receiving_cells_v15 import ReceivingCells, LinkConfig

INPUTS=tuple(product((False,True),repeat=2))


def study(n):
    @lru_cache(None)
    def trans(state,u):
        mask,age=state; green,request=u
        # bit i is physical cell i; move after exit, using one occupancy snapshot
        exit=green and age==2 and bool(mask & (1<<(n-1)))
        post=mask & ~(1<<(n-1)) if exit else mask
        moving=post & ~(post>>1) & ((1<<(n-1))-1)
        nextmask=(post & ~moving)|(moving<<1)
        accept=request and not (nextmask&1)
        if accept: nextmask|=1
        return (bool(exit),bool(accept)),(nextmask,1 if exit else min(2,age+1))
    start=(0,2); parent={start:None}; q=deque([start])
    while q:
        s=q.popleft()
        for u in INPUTS:
            _,z=trans(s,u)
            if z not in parent: parent[z]=(s,u);q.append(z)
    states=sorted(parent)
    for s in states:
        for u in INPUTS:
            mask,age=s;green,request=u
            ref=ReceivingCells(LinkConfig(cells=n,downstream_green_s=60 if green else 0))
            ref.occupied={i:(i,'L',0) for i in range(n) if mask&(1<<i)}
            ref.last_exit=10-age
            exit=ref.tick(10) is not None
            accept=ref.accept((n,'S',10)) if request else False
            observed=(sum(1<<i for i in ref.occupied),min(2,11-ref.last_exit))
            assert trans(s,u)==((exit,accept),observed)
    # Canonical signature IDs, using transitions for each possible input.
    signatures={0:{s:0 for s in states}}
    results=[]
    def obs(s,subset):return (s[0].bit_count(),s[1],tuple(bool(s[0]&(1<<i)) for i in subset))
    def valid(subset,sig):
        classes={}
        for s in states:
            k=obs(s,subset)
            if k in classes and classes[k]!=sig[s]:return False
            classes[k]=sig[s]
        return True
    for horizon in range(1,5):
        lookup={}; sig={}
        for s in states:
            key=tuple((out,signatures[horizon-1][z]) for out,z in (trans(s,u) for u in INPUTS))
            sig[s]=lookup.setdefault(key,len(lookup))
        signatures[horizon]=sig
        for k in range(n+1):
            subsets=[list(c) for c in combinations(range(n),k) if valid(c,sig)]
            if subsets:break
        results.append({'horizon':horizon,'behavior_classes':len(lookup),'minimum_cells':k,'minimum_subsets':subsets})
    witness=None
    min1=results[0]['minimum_subsets'][0]
    for a,b in combinations(states,2):
        if obs(a,min1)==obs(b,min1) and signatures[2][a]!=signatures[2][b]:
            def path(s):
                p=[]
                while parent[s] is not None:
                    s,u=parent[s];p.append(list(map(int,u)))
                return p[::-1]
            def display(s):return {'cells':''.join('1' if s[0]&(1<<i) else '0' for i in range(n)),'age':s[1],'reach_inputs':path(s)}
            for us in product(INPUTS,repeat=2):
                def replay(s):
                    o=[]
                    for u in us:
                        v,s=trans(s,u);o.append(list(map(int,v)))
                    return o
                x,y=replay(a),replay(b)
                if x!=y:
                    assert x[0]==y[0]
                    witness={'subset':min1,'a':display(a),'b':display(b),'inputs':[list(map(int,u)) for u in us],'outputs_a':x,'outputs_b':y};break
            if witness:break
    return {'cells':n,'reachable_states':len(states),'source_transition_checks':len(states)*len(INPUTS),'horizons':results,'two_step_witness':witness}

if __name__=='__main__':
    print(json.dumps([study(n) for n in (2,4,8)],indent=2))

from collections import defaultdict, Counter
from functools import lru_cache
from itertools import product
from fractions import Fraction as F
from math import gcd
import json

# Independent tuple-based rational recursion; no JS state identifiers or surrogate.
# Verify free and exact adaptive only, and initial class gain decomposition.
A=(0,1)
C=(F(0),F(1,64),F(1,16))
def audit(K,L):
    worlds=list(product(range(K[0]+1),range(K[1]+1),[w for l in range(L+1) for w in product(A,repeat=l)]))
    def observe(x,m):
        s,l,w=x
        return (s,l,w.count(0),w.count(1)) if m==0 else w[:1] if m==1 else w
    def split(b,m):
        groups=defaultdict(Counter)
        for x,n in b:groups[observe(x,m)][x]+=n
        out=[]
        for k,d in groups.items():
            g=gcd(*d.values());out.append((k,sum(d.values()),tuple(sorted((x,n//g) for x,n in d.items()))))
        assert sum(n for _,n,_ in out)==sum(n for _,n in b)
        return out
    @lru_cache(None)
    def step(x,a):
        q=list(x[:2]); w=list(x[2]); old=sum(q)+len(w)
        for _ in range(2):
            if q[a]:q[a]-=1
        for _ in range(2):
            if not w or q[w[0]]>=K[w[0]]:break
            q[w.pop(0)]+=1
        r=sum(q)+len(w)
        assert r==old-min(x[a],2) and all(0<=q[i]<=K[i] for i in A)
        return r,tuple((*q,tuple(w+[z])) for z in A)
    def solve(adaptive):
        @lru_cache(None)
        def sense(b,h):
            n=sum(v for _,v in b)
            return min(C[m]+sum(F(w,n)*act(g,h) for _,w,g in (split(b,m) if m else [(None,n,b)])) for m in (range(3) if adaptive else (0,)))
        @lru_cache(None)
        def act(b,h):
            n=sum(v for _,v in b); costs=[]
            for a in A:
                future=Counter(); immediate=0
                for x,w in b:
                    r,children=step(x,a); immediate+=w*r
                    for y in children:future[y]+=w
                v=F(immediate,n)
                if h>1:v+=sum(F(w,2*n)*sense(g,h-1) for _,w,g in split(tuple(future.items()),0))
                costs.append(v)
            return min(costs)
        result={k:(n,sense(b,4)) for k,n,b in split(tuple((x,1) for x in worlds),0)}
        sense.cache_clear();act.cache_clear()
        return result
    free=solve(False);adaptive=solve(True);N=len(worlds)
    gains={k:(n,v-adaptive[k][1]) for k,(n,v) in free.items()}
    assert all(d>=0 for n,d in gains.values())
    g=sum(n*d for n,d in gains.values()); pos=[(k,n,d) for k,(n,d) in gains.items() if d>0]
    predicates=[lambda k:k[:2]==K,lambda k:k[0]==k[1],lambda k:k[0]*K[1]==k[1]*K[0],lambda k:k[2]>0 and k[3]>0]
    return dict(K=K,L=L,N=N,groups=len(free),positive=len(pos),npositive=sum(n for k,n,d in pos),gain=str(g/N),max=str(max(d for k,n,d in pos)),shares=[str(sum(n*d for k,n,d in pos if p(k))/g) for p in predicates],free=str(sum(n*v for n,v in free.values())/N),adaptive=str(sum(n*v for n,v in adaptive.values())/N),classes=[{'k':','.join(map(str,k)),'n':n,'gain':str(d)} for k,(n,d) in gains.items()])
if __name__=='__main__':
    print(json.dumps([audit(K,L) for K in ((2,2),(2,1),(1,2),(3,2),(2,3)) for L in (4,6)],indent=2))

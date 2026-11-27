from collections import defaultdict, Counter
from functools import lru_cache
from itertools import product
from fractions import Fraction as F
from math import gcd
import json
A=(0,1); C=(F(0),F(1,64),F(1,16));H=4

def audit(K,L,window):
    worlds=list(product(range(K[0]+1),range(K[1]+1),[w for l in range(L+1) for w in product(A,repeat=l)]))
    def obs(x,m):
        s,l,w=x
        return (s,l,w.count(0),w.count(1)) if m==0 else w[:1] if m==1 else w
    def split(b,m):
        groups=defaultdict(Counter)
        for x,n in b:groups[obs(x,m)][x]+=n
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
    @lru_cache(None)
    def fq(x,h,a):
        r,child=step(x,a)
        return F(r)+ (sum(min(fq(y,h-1,z) for z in A) for y in child)/2 if h>1 else 0)
    def avg(b,h,a):return sum(n*fq(x,h,a) for x,n in b)/sum(n for x,n in b)
    def solve(policy):
        @lru_cache(None)
        def sense(b,h):
            n=sum(v for _,v in b)
            modes=(0,) if policy=='free' or H-h+1 not in window else (0,1,2)
            def parts(m):return split(b,m) if m else [(None,n,b)]
            if policy=='qmdp':modes=(min(modes,key=lambda m:C[m]+sum(F(w,n)*min(avg(g,h,a) for a in A) for _,w,g in parts(m))),)
            values=[(C[m]+sum(F(w,n)*act(g,h) for _,w,g in parts(m)),m) for m in modes]
            return min(values)
        @lru_cache(None)
        def act(b,h):
            n=sum(v for _,v in b); costs=[]
            actions=A if policy!='qmdp' else (min(A,key=lambda a:avg(b,h,a)),)
            for a in actions:
                future=Counter(); immediate=0
                for x,w in b:
                    r,children=step(x,a); immediate+=w*r
                    for y in children:future[y]+=w
                v=F(immediate,n)
                if h>1:v+=sum(F(w,2*n)*sense(g,h-1)[0] for _,w,g in split(tuple(future.items()),0))
                costs.append(v)
            return min(costs)
        result={k:(n,*sense(b,H)) for k,n,b in split(tuple((x,1) for x in worlds),0)}
        sense.cache_clear();act.cache_clear()
        return result
    sol={p:solve(p) for p in ('free','adaptive','qmdp')}
    rows=[]
    for k,(n,f,m) in sol['free'].items():
        _,a,am=sol['adaptive'][k];_,q,qm=sol['qmdp'][k]
        assert a<=f and a<=q
        rows.append(dict(k=','.join(map(str,k)),n=n,gain=str(f-a),qmdpLoss=str(q-a),first=am,qmdpFirst=qm))
    return dict(K=K,L=L,schedule=window,N=len(worlds),policies={p:str(sum(n*v for n,v,m in vals.values())/len(worlds)) for p,vals in sol.items()},classes=rows)
if __name__=='__main__':
    print(json.dumps([audit(K,L,w) for K in ((2,2),(3,2)) for L in (4,6) for w in ((1,2,3,4),(1,),(1,3))],indent=2))

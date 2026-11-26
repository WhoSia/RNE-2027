from itertools import product
from collections import Counter,defaultdict
from functools import lru_cache
from fractions import Fraction as Q
from math import gcd
import json

A=(0,1)
W=[w for n in range(5) for w in product(A,repeat=n)]
initial=list(product(range(3),range(3),W))

def observe(x,mode):
    s,l,w=x
    if mode==0:return s,l,w.count(0),w.count(1)
    if mode==1:return w[:1]
    return w

def normalize(c):
    g=0
    for v in c.values():g=gcd(g,v)
    return tuple(sorted((x,v//g) for x,v in c.items()))

def split(b,mode):
    d=defaultdict(Counter)
    for x,n in b:d[observe(x,mode)][x]+=n
    return [(sum(c.values()),normalize(c)) for c in d.values()]

@lru_cache(None)
def transition(x,a):
    q=list(x[:2]); w=list(x[2]); old=sum(q)+len(w)
    for _ in range(2):
        if q[a]:q[a]-=1
    for _ in range(2):
        if not w or q[w[0]]==2:break
        q[w.pop(0)]+=1
    cost=sum(q)+len(w)
    assert cost==old-min(x[a],2) and all(0<=v<=2 for v in q)
    return cost,tuple((*q,tuple(w+[ar])) for ar in A)

# Tuple is traffic, sensing, head acquisitions, full acquisitions.
Z=(Q(0),)*4

def add(v,u,weight=Q(1)):
    return tuple(x+weight*y for x,y in zip(v,u))

def objective(v):return v[0]+v[1]

rows=[]
for c in (Q(0),Q(1,64),Q(1,16),Q(1,4),Q(1)):
    for policy in ('free','head','full','adaptive'):
        modes={'free':(0,), 'head':(1,), 'full':(2,), 'adaptive':(0,1,2)}[policy]
        @lru_cache(None)
        def sense(b,h):
            if h==0:return Z
            n=sum(v for x,v in b)
            vals=[]
            for mode in modes:
                v=(Q(0),[Q(0),c/4,c][mode],Q(mode==1),Q(mode==2))
                parts=[(n,b)] if mode==0 else split(b,mode)
                for m,bb in parts:v=add(v,control(bb,h),Q(m,n))
                vals.append(v)
            return min(vals,key=objective)
        @lru_cache(None)
        def control(b,h):
            n=sum(v for x,v in b)
            vals=[]
            for a in A:
                nxt=Counter(); immediate=0
                for x,m in b:
                    cost,children=transition(x,a);immediate+=m*cost
                    for xx in children:nxt[xx]+=m
                v=(Q(immediate,n),Q(0),Q(0),Q(0))
                if h>1:
                    for m,bb in split(tuple(nxt.items()),0):v=add(v,sense(bb,h-1),Q(m,2*n))
                vals.append(v)
            return min(vals,key=objective)
        for h in range(1,5):
            v=Z
            for m,b in split(tuple((x,1) for x in initial),0):v=add(v,sense(b,h),Q(m,len(initial)))
            rows.append(dict(c=float(c),policy=policy,h=h,traffic=float(v[0]),sensing=float(v[1]),head=float(v[2]),full=float(v[3]),objective=float(objective(v)),exact=[str(x) for x in v]))
        sense.cache_clear(); control.cache_clear()
print(json.dumps(rows,indent=2))

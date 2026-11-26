from fractions import Fraction as Q
from collections import Counter,defaultdict
from functools import lru_cache
from itertools import product
from math import gcd
import json
A=(0,1); H=4; C=(Q(0),Q(1,64),Q(1,16)); Z=(Q(0),)*4
W=list(product(range(3),range(3),[w for n in range(5) for w in product(A,repeat=n)]))
LAWS=[('nominal',(1,1),'uniform'),('arrivals_S20',(1,4),'uniform'),('arrivals_S80',(4,1),'uniform'),('clustered',(1,1),'clustered'),('alternating',(1,1),'alternating'),('clustered_S80',(4,1),'clustered')]
POLICIES=('free','head','full','gate','adaptive')
def cost(v):return sum(v[:2])
def add(v,u,w=Q(1)):return tuple(x+w*y for x,y in zip(v,u))
def obs(x,m):
    a,b,w=x
    return (a,b,w.count(0),w.count(1)) if m==0 else w[:1] if m==1 else w

def norm(c):
    d=0
    for v in c.values():d=gcd(d,v)
    return tuple(sorted((x,n//d) for x,n in c.items()))
def mass(b):return sum(n for x,n in b)
def split(b,m):
    d=defaultdict(Counter)
    for x,n in b:d[obs(x,m)][x]+=n
    out={k:(sum(c.values()),norm(c)) for k,c in d.items()}
    assert sum(n for n,_ in out.values())==mass(b)
    return out
@lru_cache(None)
def step(x,a):
    q=list(x[:2]);w=list(x[2]);before=sum(q)+len(w)
    d=0
    for _ in A:
        if q[a]:q[a]-=1;d+=1
    for _ in A:
        if not w or q[w[0]]==2:break
        q[w.pop(0)]+=1
    r=sum(q)+len(w)
    assert r==before-d and all(0<=v<=2 for v in q)
    return r,tuple((*q,tuple(w+[i])) for i in A)
def start(law):
    b=tuple((x,2**sum((u==v if law[2]=='clustered' else u!=v if law[2]=='alternating' else False) for u,v in zip(x[2],x[2][1:]))) for x in W)
    return mass(b),split(b,0)
@lru_cache(None)
def advance(b,a,p):
    d=Counter();r=0
    for x,n in b:
        v,ch=step(x,a);r+=n*v
        for y,w in zip(ch,p):d[y]+=w*n
    assert sum(d.values())==mass(b)*sum(p)
    return Q(r,mass(b)),mass(b)*sum(p),split(tuple(d.items()),0)

def build(law,policy):
    p=law[1]
    @lru_cache(None)
    def fullq(x,h,a):
        r,ch=step(x,a)
        return Q(r)+ (sum(Q(n,sum(p))*min(fullq(y,h-1,i) for i in A) for y,n in zip(ch,p)) if h>1 else 0)
    def modes(b,h):
        if policy=='free':return (0,)
        if policy in ('head','full'):
            m=1 if policy=='head' else 2
            return (m if len(split(b,m))>1 else 0,)
        if policy=='adaptive':return (0,1,2)
        # Unnormalized subgroup expectation from original parent weights, avoiding gcd issue.
        vals=[]
        for m in range(3):
            d=defaultdict(list)
            for x,n in b:d[obs(x,m) if m else ()].append((x,n))
            v=C[m]+sum(min(sum(n*fullq(x,h,a) for x,n in g) for a in A) for g in d.values())/mass(b)
            vals.append(v)
        return (min(range(3),key=lambda m:vals[m]),)
    @lru_cache(None)
    def sense(b,h):
        vals=[]
        for m in modes(b,h):
            v=(Q(0),C[m],Q(m==1),Q(m==2))
            for n,bb in ([(mass(b),b)] if m==0 else split(b,m).values()):v=add(v,act(bb,h)[1],Q(n,mass(b)))
            vals.append((m,v))
        return min(vals,key=lambda t:cost(t[1]))
    @lru_cache(None)
    def act(b,h):
        vals=[]
        for a in A:
            r,den,d=advance(b,a,p);v=(r,*Z[1:])
            if h>1:
                for n,bb in d.values():v=add(v,sense(bb,h-1)[1],Q(n,den))
            vals.append((a,v))
        return min(vals,key=lambda t:cost(t[1]))
    return sense,act

def evaluate(model,law,solver):
    sense,act=solver
    @lru_cache(None)
    def es(b,t,h):
        m=sense(b,h)[0];v=(Q(0),C[m],Q(m==1),Q(m==2))
        if m==0:return add(v,ea(b,t,h))
        bp=split(b,m)
        for k,(n,tt) in split(t,m).items():v=add(v,ea(bp[k][1],tt,h),Q(n,mass(t)))
        return v
    @lru_cache(None)
    def ea(b,t,h):
        a=act(b,h)[0];r,den,d=advance(t,a,law[1]);v=(r,*Z[1:])
        if h>1:
            bp=advance(b,a,model[1])[2]
            for k,(n,tt) in d.items():v=add(v,es(bp[k][1],tt,h-1),Q(n,den))
        return v
    total,st=start(law);_,sm=start(model);v=Z;rows={}
    for k,(n,t) in st.items():
        b=sm[k][1];x=es(b,t,H);v=add(v,x,Q(n,total));rows[k]=(n,x,sense(b,H)[0])
    return v,rows

def run():
    nom=LAWS[0];sol={p:build(nom,p) for p in POLICIES};out=[];cond=[]
    for law in LAWS:
        values={p:evaluate(nom,law,s) for p,s in sol.items()};values['reoptimized']=evaluate(law,law,build(law,'adaptive'))
        assert all(cost(values['reoptimized'][0])<=cost(values[p][0]) for p in POLICIES)
        for p,(v,_) in values.items():out.append(dict(law=law[0],policy=p,v=list(map(float,v)),exact=list(map(str,v)),objective=float(cost(v))))
        if law==nom:
            for k,(n,v,_) in values['free'][1].items():
                av=values['adaptive'][1][k];gv=values['gate'][1][k];gain=cost(v)-cost(av[1]);assert gain>=0
                cond.append(dict(k=','.join(map(str,k)),n=n,free=float(cost(v)),adaptive=float(cost(av[1])),gate=float(cost(gv[1])),gain=float(gain),adaptiveFirst=av[2],gateFirst=gv[2],adaptiveAcq=float(sum(av[1][2:])),exactGain=str(gain)))
    return dict(results=out,conditional=cond)
if __name__=='__main__':print(json.dumps(run(),indent=2))

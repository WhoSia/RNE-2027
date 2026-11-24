from collections import deque
from itertools import product
from time import perf_counter
from statistics import median
import json,sys,platform

def tapes(N):
    result=[]
    for seed in range(4):
        a=list(range(N));x=seed+1
        for i in range(N-1,0,-1):
            x=(1664525*x+1013904223)&0xffffffff;j=x%(i+1);a[i],a[j]=a[j],a[i]
        for stride in (1,4):
            ar=[0]*(8*N+16)
            for i,v in enumerate(a):ar[i*stride]=1 if v<N//2 else 2
            result.append(ar)
    return result

def micro(ar,g,o,check):
    q=deque();p=r=A=Z=Y=J=peak=0
    for t,v in enumerate(ar):
        gs=t%8<g;ds=(t+o)%8<4;h=q[0] if q else 0
        x=int(gs and h==1 and r<3);a=int(h==2 and p<3);y=int(not gs and p>0);z=int(ds and r>0)
        if x or a:q.popleft()
        p+=a-y;r+=x-z;Y+=y;Z+=z
        if v:q.append(v);A+=1
        stock=len(q)+p+r;J+=stock
        if check:
            peak=max(peak,len(q));assert stock+Y+Z==A and 0<=p<=3 and 0<=r<=3
    return J,stock,peak

def mixed(ar,g,o,check):
    S=L=p=r=A=Z=Y=J=0.
    for t,v in enumerate(ar):
        gs=t%8<g;ds=(t+o)%8<4;total=S+L
        fs=S/total if total else 0;fl=L/total if total else 0
        x=min(S,fs,max(0.,3-r)) if gs else 0.;a=min(L,fl,max(0.,3-p));y=min(p,1.) if not gs else 0.;z=min(r,1.) if ds else 0.
        S-=x;L-=a;p+=a-y;r+=x-z;Y+=y;Z+=z
        if v:S+=v==1;L+=v==2;A+=1
        stock=S+L+p+r;J+=stock
        if check:assert abs(stock+Y+Z-A)<1e-7 and min(S,L,p,r)>=-1e-8 and max(p,r)<=3+1e-8
    return J,stock,2

def run():
    out={}
    for N in (24,96,384):
        jobs=list(product(tapes(N),(3,4,5),(0,2,4,6)))
        assert len(jobs)==96
        models={'micro':micro,'mixed':mixed};checks={};timing={k:[] for k in models}
        def batch(fn,check):
            J=terminal=peak=0
            for ar,g,o in jobs:
                j,s,p=fn(ar,g,o,check);J+=j;terminal=max(terminal,s);peak=max(peak,p)
            assert terminal<1e-7
            return dict(J=J,terminal=terminal,peak=peak)
        for name,fn in models.items():checks[name]=batch(fn,True);batch(fn,False)
        for rep in range(5):
            for name in (('micro','mixed') if rep%2==0 else ('mixed','micro')):
                start=perf_counter();r=batch(models[name],False);elapsed=perf_counter()-start
                assert abs(r['J']-checks[name]['J'])<1e-7
                timing[name].append(elapsed)
        out[str(N)]={'armsPerModel':len(jobs),'ticksPerPass':len(jobs)*(8*N+16),'checks':checks,'timingSeconds':timing,'medians':{k:median(v) for k,v in timing.items()},'mixedOverMicro':median(timing['mixed'])/median(timing['micro'])}
    return dict(python=sys.version,platform=platform.platform(),results=out)
if __name__=='__main__':print(json.dumps(run(),indent=2))

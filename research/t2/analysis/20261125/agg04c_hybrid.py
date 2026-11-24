from collections import deque
from itertools import product
from statistics import median
from time import perf_counter
import json, platform, sys

def tape(n,seed,family):
    a=list(range(n));x=seed+1
    for i in range(n-1,0,-1):
        x=(1664525*x+1013904223)&0xffffffff;j=x%(i+1);a[i],a[j]=a[j],a[i]
    times=[];t=0;x=seed+10001
    for i in range(n):
        if family=='dense':t=i
        elif family=='sparse':t=12*i
        elif family=='burst':t=40*(i//8)+i%8
        elif i:x=(1664525*x+1013904223)&0xffffffff;t+=1+x%12
        times.append(t)
    return list(zip(times,[1 if v<n//2 else 2 for v in a]))

def sim(ar,P,g,o,mode,verify=False):
    n=len(ar);H=16*n+32;q=deque();p=r=A=B=Y=Z=js=jl=t=steps=0;trace=[]
    ws,wl,wd=([next(w for w in range(8) if fn((phase+w)%8)) for phase in range(8)] for fn in (lambda x:x<g,lambda x:x>=g,lambda x:(x+o)%8<4))
    while t<H and Y+Z<n:
        at=ar[A+B][0] if A+B<n else H
        if mode=='event':
            h=q[0] if q else 0;phase=t%8
            k=min(at,t if h==2 and p<P else H,t+ws[phase] if h==1 and r<P else H,t+wl[phase] if p else H,t+wd[phase] if r else H,H)
            gap=k-t;assert gap>=0;js+=gap*(A-Z);jl+=gap*(B-Y);t=k
        elif mode=='hybrid' and not q and not p and not r:
            t=at
        if t>=H:break
        gs=t%8<g;ds=(t+o)%8<4;h=q[0] if q else 0
        x=int(gs and h==1 and r<P);a=int(h==2 and p<P);y=int(not gs and p>0);z=int(ds and r>0)
        if x or a:q.popleft()
        p+=a-y;r+=x-z;Y+=y;Z+=z
        v=ar[A+B][1] if at==t else 0
        if v:q.append(v);A+=v==1;B+=v==2
        if verify:
            assert A-Z==q.count(1)+r and B-Y==q.count(2)+p and 0<=p<=P and 0<=r<=P
            if x or a or y or z or v:trace.append((t,tuple(q),p,r,A,B,Y,Z))
        js+=A-Z;jl+=B-Y;t+=1;steps+=1
    assert A+B==Y+Z==n
    return js,jl,t,steps,tuple(trace)

def run():
    modes=('tick','event','hybrid');out={}
    for family in ('dense','sparse','burst','irregular'):
        jobs=[(tape(n,seed,family),P,g,o) for n,seed,P,(g,o) in product((24,96,384),range(250,254),(1,3),((3,0),(4,2),(5,4)))]
        checks={m:[0,0,0,0] for m in modes}
        for j in jobs:
            rs=[sim(*j,m,True) for m in modes]
            assert all(r[:3]==rs[0][:3] and r[4]==rs[0][4] for r in rs)
            for m,r in zip(modes,rs):checks[m]=[a+b for a,b in zip(checks[m],r[:4])]
        def batch(m):
            c=[0,0,0,0]
            for j in jobs:c=[a+b for a,b in zip(c,sim(*j,m)[:4])]
            assert c==checks[m]
        for m in modes:batch(m)
        times={m:[] for m in modes}
        for i in range(3):
            for m in modes[i:]+modes[:i]:
                start=perf_counter();batch(m);times[m].append(perf_counter()-start)
        out[family]={'arms':len(jobs),'checks':checks,'seconds':times,'medians':{m:median(times[m]) for m in modes},'ratios':{m:median(times[m])/median(times['tick']) for m in modes}}
    return {'python':sys.version,'platform':platform.platform(),'results':out}
if __name__=='__main__':print(json.dumps(run(),indent=2))

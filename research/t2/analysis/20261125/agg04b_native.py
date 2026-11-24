from collections import deque
from itertools import product
from statistics import median
from time import perf_counter
import json, platform, sys

def tape(n, seed, stride):
    a=list(range(n)); x=seed+1
    for i in range(n-1,0,-1):
        x=(1664525*x+1013904223)&0xffffffff; j=x%(i+1); a[i],a[j]=a[j],a[i]
    return [(i*stride,1 if v<n//2 else 2) for i,v in enumerate(a)]

def sim(ar,pmax,rmax,g,o,event,verify):
    n=len(ar); H=16*n+32; q=deque(); p=r=as_=al=zs=zl=js=jl=t=steps=0
    ws,wl,wd=([next(w for w in range(8) if pred((phase+w)%8)) for phase in range(8)] for pred in (lambda x:x<g,lambda x:x>=g,lambda x:(x+o)%8<4))
    while t<H and zs+zl<n:
        at=ar[as_+al][0] if as_+al<n else H
        if event:
            h=q[0] if q else 0; phase=t%8
            k=min(at,t if h==2 and p<pmax else H,t+ws[phase] if h==1 and r<rmax else H,t+wl[phase] if p else H,t+wd[phase] if r else H,H)
            gap=k-t; js+=gap*(as_-zs); jl+=gap*(al-zl); t=k
            if t==H:break
        gs=t%8<g; ds=(t+o)%8<4; h=q[0] if q else 0
        x=int(gs and h==1 and r<rmax); a=int(h==2 and p<pmax); y=int(not gs and p>0); z=int(ds and r>0)
        if x or a:q.popleft()
        p+=a-y; r+=x-z; zs+=z; zl+=y
        v=ar[as_+al][1] if at==t else 0
        if v:q.append(v);as_+=v==1;al+=v==2
        if verify:
            assert as_-zs==q.count(1)+r and al-zl==q.count(2)+p
            assert 0<=p<=pmax and 0<=r<=rmax
            assert not event or x or a or y or z or v
        js+=as_-zs; jl+=al-zl; steps+=1;t+=1
    assert as_+al==zs+zl==n
    return js,jl,t,steps

def run():
    result={}; expected={1:(11621964,120127,94080),4:(715058,195828,115766),12:(180468,578592,145152)}
    for stride in (1,4,12):
        jobs=[(tape(n,seed,stride),p,p,g,o) for n,seed,p,g,o in product((24,96,384),range(240,244),(1,3),(3,4,5),(0,2,4,6))]
        J=ref=ev=0
        for job in jobs:
            a=sim(*job,False,True); b=sim(*job,True,True); assert a[:3]==b[:3]
            J+=a[0]+a[1];ref+=a[3];ev+=b[3]
        assert (J,ref,ev)==expected[stride]
        def batch(event):
            total=steps=0
            for job in jobs:
                a=sim(*job,event,False);total+=a[0]+a[1];steps+=a[3]
            assert total==J and steps==(ev if event else ref)
        batch(False);batch(True);times={'tick':[],'event':[]}
        for i in range(3):
            for mode in ((False,True) if i%2==0 else (True,False)):
                start=perf_counter();batch(mode);times['event' if mode else 'tick'].append(perf_counter()-start)
        result[str(stride)]={'arms':len(jobs),'J':J,'ticks':ref,'events':ev,'seconds':times,'event_over_tick':median(times['event'])/median(times['tick'])}
    return {'python':sys.version,'platform':platform.platform(),'results':result}

if __name__=='__main__':print(json.dumps(run(),indent=2))

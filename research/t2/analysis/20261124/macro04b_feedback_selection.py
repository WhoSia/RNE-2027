"""MACRO04B abstract offline feedback selection; no road-control interface."""
from collections import defaultdict
from itertools import product
import json
from macro02b_audit import POL,CLOCKS,tape,tick

NAMES=('fixed','demand','mean','minimax','counts12','pressure','head','static_oracle')
EXPECTED=(177215,167885,167279,167279,164253,163086,166125,158142)

def records():
    seeds=[s for s in range(60) if s%5]+list(range(100,140))
    for seed,left,clock,P,R in product(seeds,(6,12,18),CLOCKS,(1,3),(1,3)):
        ar=tape(seed,left,clock); pre=((),)+(0,)*11
        for t in range(16):pre=tick(pre,t,4,0,P,R,ar.get(t),False)
        q,p,r,A,B,*_=pre; frac=A/(A+B)
        dem=POL.index((5 if frac>=.75 else 3 if frac<=.25 else 4,0))
        costs=[]
        for i in range(14):
            s=pre;g,o=POL[i] if i<12 else (4,0)
            for t in range(16,240):
                if i>=12 and t%8==0:
                    q,p,r=s[:3]
                    if i==12:
                        ps=max(0,q.count('S')-r);pl=q.count('L')+p
                        g=5 if ps>pl else 3 if ps<pl else 4
                    else:g=5 if q and q[0]=='S' and r<R else 3 if (q and q[0]=='L') or p==P else 4
                s=tick(s,t,g,o,P,R,ar.get(t),False)
                if s[5]+s[6]==24:break
            assert s[3]+s[4]==s[5]+s[6]==24
            costs.append((s[7]+s[8],s[7],s[8],s[9]))
        q,p,r=pre[:3];obs=(len(q),p,r)
        yield seed,left,clock,(P,R),obs,dem,tuple(costs)

def choose(rows,n,mode='mean'):
    if mode=='minimax':return min(range(n),key=lambda i:max(row[6][i][0]-min(c[0] for c in row[6][:n]) for row in rows))
    return min(range(n),key=lambda i:sum(row[6][i][0] for row in rows))

def run():
    train=defaultdict(list); counts=defaultdict(list); presence=defaultdict(list); noisy=defaultdict(list); audit=[];test=[]
    for row in records():
        seed,left,clock,ctx,obs,dem,cs=row
        if seed<60:
            train[ctx].append(row);counts[ctx+obs].append(row)
            bits=tuple(int(x>0) for x in obs);presence[ctx+bits].append(row)
            noisy[ctx+bits].append((row,7))
            for i in range(3):
                flip=tuple(x^(j==i) for j,x in enumerate(bits));noisy[ctx+flip].append((row,1))
        elif seed<120:audit.append(row)
        else:test.append(row)
    assert sum(map(len,train.values()))==1728 and len(audit)==len(test)==720
    fixed={k:(choose(v,12),choose(v,12,'minimax'),choose(v,14)) for k,v in train.items()}
    supported=lambda rows:len({r[0] for r in rows})>=4
    c12={k:choose(v,12) for k,v in counts.items() if supported(v)}
    c14={k:choose(v,14) for k,v in counts.items() if supported(v)}
    p14={k:choose(v,14) for k,v in presence.items() if supported(v)}
    n14={k:min(range(14),key=lambda i:sum(w*r[6][i][0] for r,w in v)) for k,v in noisy.items() if supported([r for r,w in v])}
    sums=[0]*8
    for _,_,_,ctx,obs,dem,cs in audit:
        mean,mini,_=fixed[ctx]
        ids=(4,dem,mean,mini,c12.get(ctx+obs,mean),12,13,min(range(12),key=lambda i:cs[i][0]))
        for j,i in enumerate(ids):sums[j]+=cs[i][0]
    assert tuple(sums)==EXPECTED,(sums,EXPECTED)
    names=('mean12','minimax12','demand','pressure','head','mean14','counts14','presence_exact','presence_flip','noisy_exact','noisy_flip','static_oracle','oracle14')
    def init():return dict(n=0,covered=0,J=0,S=0,L=0,denial=0,static_diff=0,regret14=0,worst14=0,vs_pressure=[0,0,0],vs_mean14=[0,0,0])
    stats={k:{n:init() for n in names} for k in ('all',*CLOCKS)}
    for seed,left,clock,ctx,obs,dem,cs in test:
        mean,mini,best14=fixed[ctx];P,R=ctx;bits=tuple(int(x>0) for x in obs)
        flip=tuple(x^(j==(seed+left+P+R)%3) for j,x in enumerate(bits))
        s_or=min(range(12),key=lambda i:cs[i][0]);a_or=min(range(14),key=lambda i:cs[i][0]);b=cs[a_or][0]
        ids=(mean,mini,dem,12,13,best14,c14.get(ctx+obs),p14.get(ctx+bits),p14.get(ctx+flip),n14.get(ctx+bits),n14.get(ctx+flip),s_or,a_or)
        for k in ('all',clock):
            for name,i in zip(names,ids):
                z=stats[k][name];z['n']+=1;z['covered']+=i is not None
                J,S,L,d=cs[best14 if i is None else i];z['J']+=J;z['S']+=S;z['L']+=L;z['denial']+=d;z['static_diff']+=J-cs[s_or][0];z['regret14']+=J-b;z['worst14']=max(z['worst14'],J-b)
                for field,ref in (('vs_pressure',12),('vs_mean14',best14)):
                    v=J-cs[ref][0];z[field][(v>0)-(v<0)+1]+=1
    return dict(status='NATIVE_ABSTRACT_OFFLINE_NOT_FIELD',train=1728,audit=720,test=720,arms=3168*14,audit_totals=dict(zip(NAMES,sums)),fixed={str(k):v for k,v in fixed.items()},supported=dict(counts=len(c14),presence=len(p14),noisy=len(n14)),stats=stats)

if __name__=='__main__':print(json.dumps(run(),indent=2))

"""P159-M: fresh seed cohort, bounded count observation uncertainty."""
from collections import defaultdict
from itertools import product
import json
from macro02b_audit import POL,CLOCKS,tape,tick

def run():
    train=defaultdict(list);cells=defaultdict(list);test=[]
    for seed,left,clock,P,R in product(range(80),(6,12,18),CLOCKS,(1,3),(1,3)):
        if seed<60 and seed%5==0:continue
        ar=tape(seed,left,clock);s=((),)+(0,)*11
        for t in range(16):s=tick(s,t,4,0,P,R,ar.get(t),False)
        q,p,r,A,B,*_=s; frac=A/(A+B);dem=POL.index((5 if frac>=.75 else 3 if frac<=.25 else 4,0))
        cs=[]
        for g,o in POL:
            z=s
            for t in range(16,240):
                z=tick(z,t,g,o,P,R,ar.get(t),False)
                if z[5]+z[6]==24:break
            assert z[3]+z[4]==z[5]+z[6]==24
            cs.append(z[7]+z[8])
        ctx=(P,R);obs=(len(q),p,r);row=(seed,left,clock,ctx,obs,dem,tuple(cs),min(cs))
        if seed<60:train[ctx].append(row);cells[ctx+obs].append(row)
        else:test.append(row)
    assert sum(map(len,train.values()))==1728 and len(test)==720
    def select(rows,mode):
        if mode=='mean':return min(range(12),key=lambda i:sum(r[6][i] for r in rows))
        if mode=='minimax':return min(range(12),key=lambda i:max(r[6][i]-r[7] for r in rows))
        return min(range(12),key=lambda i:(max(r[6][i]-r[7] for r in rows),sum(r[6][i]-r[7] for r in rows),i))
    base={k:(select(v,'mean'),select(v,'minimax')) for k,v in train.items()}
    supported={k for k,v in cells.items() if len({r[0] for r in v})>=4}
    nominal={k:select(cells[k],'mean') for k in supported}
    def robust(ctx,obs):
        P,R=ctx;q,p,r=obs
        nbr=[obs]+[tuple(a+(d if i==j else 0) for i,a in enumerate(obs)) for j in range(3) for d in (-1,1)]
        nbr=[ctx+x for x in nbr if x[0]>=0 and 0<=x[1]<=P and 0<=x[2]<=R and sum(x)<=24]
        if not all(k in supported for k in nbr):return None
        return select([row for k in nbr for row in cells[k]],'robust')
    names=('mean','minimax','demand','nominal_exact','robust_exact','nominal_corrupt','robust_corrupt','missing')
    stats={n:dict(n=0,covered=0,J=0,regret=0,worst=0,harm_vs_mean=0,better_vs_mean=0,miss=0) for n in names}
    for seed,left,clock,ctx,obs,dem,cs,best in test:
        mean,mini=base[ctx];P,R=ctx;q,p,r=obs
        if (seed+left+P+R)%2 and r<R and sum(obs)<24:bad=(q,p,r+1)
        else:bad=(q+(1 if sum(obs)<24 else -1),p,r)
        ne=nominal.get(ctx+obs);re=robust(ctx,obs);nc=nominal.get(ctx+bad);rc=robust(ctx,bad)
        for n,a in zip(names,(mean,mini,dem,ne,re,nc,rc,None)):
            z=stats[n];z['n']+=1;z['covered']+=a is not None
            J=cs[mean if a is None else a];d=J-best
            z['J']+=J;z['regret']+=d;z['worst']=max(z['worst'],d);z['harm_vs_mean']+=J>cs[mean];z['better_vs_mean']+=J<cs[mean];z['miss']+=d>0
    return dict(status='NATIVE_SYNTHETIC_FRESH_SEED_NOT_FIELD',train=1728,test=720,arms=29376,supported_cells=len(supported),total_cells=len(cells),stats=stats)

if __name__=='__main__':print(json.dumps(run(),indent=2))

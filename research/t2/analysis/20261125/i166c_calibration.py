from collections import defaultdict
from itertools import product
import json
KNOWN=('dense','platoon','sparse')
SHIFT=('burst','irregular','blocks6')
NAMES=('geometry','presence','counts','past_total','past_movement','time_bins','movement_bins','ordered_history')
POL=list(product((3,4,5),(0,2,4,6)))

def tape(seed,left,clock):
    a=list(range(24)); x=seed+1
    for i in range(23,0,-1):
        x=(1664525*x+1013904223)&0xffffffff; j=x%(i+1); a[i],a[j]=a[j],a[i]
    t=0;x=seed+9001; ar={}
    for i,v in enumerate(a):
        if clock=='dense': t=i
        elif clock=='platoon': t=8*(i//4)+i%4
        elif clock=='sparse': t=4*i
        elif clock=='burst': t=24*(i//8)+i%8
        elif clock=='blocks6': t=18*(i//6)+i%6
        elif clock=='alternating': t=10*(i//2)+i%2
        elif i: x=(1664525*x+1013904223)&0xffffffff; t+=1+x%6
        ar[t]='L' if v<left else 'S'
    return ar

def step(state,t,g,o,P,R,v):
    q,p,r,A,Y,Z,J=state; h=q[:1]; gs=t%8<g; ds=(t+o)%8<4
    x=int(gs and h=='S' and r<R); a=int(h=='L' and p<P); y=int(not gs and p>0); z=int(ds and r>0)
    q=q[x+a:]+v; p+=a-y; r+=x-z; A+=bool(v);Y+=y;Z+=z
    stock=len(q)+p+r
    assert A==stock+Y+Z and 0<=p<=P and 0<=r<=R
    return q,p,r,A,Y,Z,J+stock

def rows(seeds,clocks):
    for seed,left,clock,P,R in product(seeds,(6,12,18),clocks,(1,3),(1,3)):
        ar=tape(seed,left,clock); st=('',0,0,0,0,0,0)
        for t in range(16):st=step(st,t,4,0,P,R,ar.get(t,''))
        q,p,r,*_=st
        bins=tuple(sum(t in ar for t in range(j,j+4)) for j in range(0,16,4))
        lb=tuple(sum(ar.get(t)=='L' for t in range(j,j+4)) for j in range(0,16,4))
        fields=((P,R),(bool(q),bool(p),bool(r)),(len(q),p,r),sum(bins),sum(lb),bins,lb,q)
        keys=tuple(fields[:i+1] for i in range(8)); costs=[]
        for g,o in POL:
            s=st
            for t in range(16,240):s=step(s,t,g,o,P,R,ar.get(t,''))
            assert s[3]==s[4]+s[5]==24; costs.append(s[-1])
        yield seed,clock,keys,costs

def main():
    train=list(rows([i for i in range(60) if i%5],KNOWN)); maps=[defaultdict(list) for _ in NAMES]
    for r in train:
        for m,k in zip(maps,r[2]):m[k].append(r)
    def supported(g):return len({r[0] for r in g})>=4
    def mean(g):return min(range(12),key=lambda j:sum(r[3][j] for r in g))
    bas={k:mean(g) for k,g in maps[0].items()}; fit={mode:[] for mode in ('mean','guard')}
    for i,m in enumerate(maps):
        for mode in fit:
            f={}
            for k,g in m.items():
                if not supported(g):continue
                b=bas[g[0][2][0]]
                allowed=[j for j in range(12) if mode=='mean' or all(r[3][j]<=r[3][b] for r in g)]
                f[k]=min(allowed,key=lambda j:(sum(r[3][j] for r in g),int(j!=b) if mode=='guard' else 0,j)) if i else b
            fit[mode].append(f)
    def evaluate(data,mode,i):
        a=dict(n=len(data),J=0,regret=0,worst=0,supported=0,changed=0,better=0,tie=0,worse=0,maxHarm=0,groups=0,singletons=0,floor=0)
        groups=defaultdict(list)
        for _,_,keys,c in data:
            b=bas[keys[0]]; k=i
            while keys[k] not in fit[mode][k]:k-=1
            j=fit[mode][k][keys[k]]; d=c[j]-min(c); e=c[j]-c[b]
            a['J']+=c[j];a['regret']+=d;a['worst']=max(a['worst'],d);a['supported']+=k==i;a['changed']+=j!=b
            a['better' if e<0 else 'worse' if e>0 else 'tie']+=1;a['maxHarm']=max(a['maxHarm'],e);groups[keys[i]].append(c)
        a['groups']=len(groups);a['singletons']=sum(len(g)==1 for g in groups.values())
        a['floor']=sum(min(map(sum,zip(*g)))-sum(map(min,g)) for g in groups.values());assert a['regret']>=a['floor']
        return a
    def split(data,novel=False):
        result={'known':[r for r in data if r[1] in KNOWN],'shifted':[r for r in data if r[1] in SHIFT],'pooled':data}
        if novel:result['novel']=[r for r in data if r[1]=='alternating']
        return result
    replay=list(rows(range(340,360),KNOWN+SHIFT)); rep={k:[evaluate(d,'mean',i) for i in range(8)] for k,d in split(replay).items()}
    expected={'known':([168263,163658,163273,162559,162234,162234,162355,162355],[10191,5509,4307,3597,1212,1212,595,434],[720,710,665,665,441,441,321,303],[4,26,106,112,306,306,417,447],[0,2,27,27,175,175,303,354]),'shifted':([106248,105670,105975,105413,105248,105248,105248,105248],[7896,6546,6304,5032,3080,2610,1967,1886],[720,674,644,288,223,16,16,16],[4,28,52,123,270,335,409,419],[0,4,8,27,115,198,276,292]),'pooled':([274511,269328,269248,267972,267482,267482,267603,267603],[18489,12705,11189,9000,4979,3953,2693,2451],[1440,1384,1309,953,664,457,337,319],[4,30,118,189,465,633,818,858],[0,0,25,42,213,369,575,642])}
    for k,v in expected.items():assert tuple([r[f] for r in rep[k]] for f in ('J','floor','supported','groups','singletons'))==v
    opts=[('mean',0)]+[(m,i) for i in range(1,8) for m in ('mean','guard')]
    def evaluate_all(data,novel=False):return {k:{f'{m}:{i}':evaluate(d,m,i) for m,i in opts} for k,d in split(data,novel).items()}
    cal=list(rows(range(360,370),KNOWN+SHIFT)); ca=evaluate_all(cal)
    eligible=[]
    for m,i in opts[1:]:
        key=f'{m}:{i}'
        if all(ca[k][key]['J']<=ca[k]['mean:0']['J'] and ca[k][key]['worst']<=ca[k]['mean:0']['worst'] and 20*ca[k][key]['worse']<=ca[k][key]['n'] for k in ('known','shifted')) and ca['pooled'][key]['J']<ca['pooled']['mean:0']['J']:
            eligible.append((ca['pooled'][key]['J'],i,m,key))
    chosen=min(eligible)[-1] if eligible else 'mean:0'
    final=list(rows(range(380,400),KNOWN+SHIFT+('alternating',))); result=evaluate_all(final,True)
    arms=12*sum(map(len,(train,replay,cal,final)));assert arms==66816
    return dict(arms=arms,replayParity=True,chosen=chosen,eligible=sorted(eligible),calibration=ca,final=result)

if __name__=='__main__':print(json.dumps(main(),indent=2))

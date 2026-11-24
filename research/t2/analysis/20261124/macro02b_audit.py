"""Independent native MACRO02B replay. Synthetic abstract ticks only."""
from collections import defaultdict
from itertools import product,combinations
import json

POL=list(product((3,4,5),(0,2,4,6)))
CLOCKS=('dense','platoon','sparse')

def tape(seed,left,clock):
    a=list(range(24)); x=seed+1
    for i in range(23,0,-1):
        x=(1664525*x+1013904223)&0xffffffff; j=x%(i+1); a[i],a[j]=a[j],a[i]
    return {(i if clock=='dense' else 8*(i//4)+i%4 if clock=='platoon' else 4*i):('L' if v<left else 'S') for i,v in enumerate(a)}

def tick(s,t,g,o,P,R,v,reuse):
    q,p,r,A,B,X,Y,js,jl,d,h,e=s
    S=t%8<g; x=int(r>0 and (t+o)%8<4)
    head=q[0] if q else None; a=int(head=='L' and p<P)
    room=r<R or bool(reuse and x)
    ms=int(S and head=='S' and room); ml=int(not S and p>0)
    d+=int(S and head=='S' and not room);h+=int(S and head=='L' and 'S' in q);e+=int(not S and not p and 'L' in q)
    assert ms+ml<=1 and ms+a<=1
    q=q[ms+a:]+((v,) if v else ());p+=a-ml;r+=ms-x
    A+=int(v=='S');B+=int(v=='L');X+=x;Y+=ml
    ns=q.count('S')+r;nl=q.count('L')+p
    assert A-X==ns and B-Y==nl and 0<=p<=P and 0<=r<=R
    return q,p,r,A,B,X,Y,js+ns,jl+nl,d,h,e

def run():
    train=[];test=[];tr=[0,0,0];flips=0;cases=0
    for seed,left,clock,P,R in product(range(60),(6,12,18),CLOCKS,(1,3),(1,3)):
        ar=tape(seed,left,clock);s=((),)+(0,)*11
        for t in range(16):s=tick(s,t,4,0,P,R,ar.get(t),False)
        q,p,r,A,B,*_=s; frac=A/(A+B);dem=POL.index((5 if frac>=.75 else 3 if frac<=.25 else 4,0))
        costs=[]
        for reuse in (False,True):
            out=[]
            for g,o in POL:
                z=s
                for t in range(16,240):
                    z=tick(z,t,g,o,P,R,ar.get(t),reuse)
                    if z[5]+z[6]==24:break
                assert z[3]+z[4]==z[5]+z[6]==24
                out.append((z[7]+z[8],*z[7:12]))
            costs.append(out)
        old,new=costs
        for a,b in zip(old,new):tr[(b[0]>a[0])-(b[0]<a[0])+1]+=1
        for i,j in combinations(range(12),2):
            flips+=int((old[i][0]-old[j][0])*(new[i][0]-new[j][0])<0);cases+=1
        row=(seed,clock,(P,R),(len(q),p,r),q[0] if q else '-',dem,old,min(c[0] for c in old))
        (test if seed%5==0 else train).append(row)
    maps=[defaultdict(list) for _ in range(3)]
    def keys(row):
        _,_,ctx,counts,head,*_=row;return ctx,ctx+counts,ctx+counts+(head,)
    def choose(rows,kind):
        if kind=='mean':return min(range(12),key=lambda i:sum(r[6][i][0] for r in rows))
        if kind=='minimax':return min(range(12),key=lambda i:max(r[6][i][0]-r[7] for r in rows))
        return min(range(12),key=lambda i:sum(r[6][i][3] for r in rows))
    for row in train:
        for m,k in zip(maps,keys(row)):m[k].append(row)
    names=('fixed','demand','mean','minimax','local','counts','head','oracle')
    stat={k:{n:[0,0,0,0,0,0,0,0,0,0] for n in names} for k in ('all',*CLOCKS)}
    cov={k:[0,0] for k in stat};pairs={k:[[0,0,0],[0,0,0]] for k in stat};extra={k:[0,0,0] for k in stat}
    fixed={ctx:tuple(choose(rows,k) for k in ('mean','minimax','local')) for ctx,rows in maps[0].items()}
    for row in test:
        seed,clock,ctx,counts,head,dem,cs,best=row;mean,mini,local=fixed[ctx];ks=keys(row)
        groups=[maps[i].get(ks[i],[]) for i in (1,2)];ok=[len({r[0] for r in g})>=4 for g in groups];acts=[choose(g,'mean') if a else mean for g,a in zip(groups,ok)]
        ids=[4,dem,mean,mini,local,*acts,min(range(12),key=lambda i:cs[i][0])]
        md=min(c[3] for c in cs)
        for k in ('all',clock):
            extra[k][0]+=int(all(c[0]>best for c in cs if c[3]==md));extra[k][1]+=int(any(c[3] for c in cs));extra[k][2]+=sum(c[3]>0 for c in cs)
            for j,(a,v) in enumerate(zip(acts,ok)):
                cov[k][j]+=v;d=cs[a][0]-cs[mean][0];pairs[k][j][(d>0)-(d<0)+1]+=1
            for n,i in zip(names,ids):
                c=cs[i];a=stat[k][n];a[0]+=1
                for j,v in enumerate(c,1):a[j]+=v
                d=c[0]-best;a[7]+=d;a[8]=max(a[8],d);a[9]+=d>0
    return dict(train=len(train),test=len(test),transfer=tr,rankPairs=cases,strictRankFlips=flips,selections={str(k):v for k,v in fixed.items()},stats=stat,coverage=cov,paired=pairs,extra=extra)

if __name__=='__main__':print(json.dumps(run(),indent=2))

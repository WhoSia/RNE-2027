from itertools import product
from collections import defaultdict
import json

CLOCKS=('dense','platoon','sparse','burst','irregular','blocks6')
POL=list(product((3,4,5),(0,2,4,6)))

def tape(seed,left,clock):
    order=list(range(24));x=seed+1
    for i in range(23,0,-1):
        x=(1664525*x+1013904223)&0xffffffff;j=x%(i+1)
        order[i],order[j]=order[j],order[i]
    t=0;x=seed+9001;ar={}
    for i,v in enumerate(order):
        if clock=='dense':t=i
        elif clock=='platoon':t=8*(i//4)+i%4
        elif clock=='sparse':t=4*i
        elif clock=='burst':t=24*(i//8)+i%8
        elif clock=='blocks6':t=18*(i//6)+i%6
        elif i:x=(1664525*x+1013904223)&0xffffffff;t+=1+x%6
        ar[t]='L' if v<left else 'S'
    return ar

def tick(state,t,g,o,P,R,v):
    q,p,r,A,Y,Z,J=state;gs=t%8<g;ds=(t+o)%8<4;head=q[0] if q else ''
    x=int(gs and head=='S' and r<R);a=int(head=='L' and p<P)
    y=int(not gs and p>0);z=int(ds and r>0)
    q=q[x+a:]+v;p+=a-y;r+=x-z;A+=bool(v);Y+=y;Z+=z
    stock=len(q)+p+r
    assert A==stock+Y+Z and 0<=p<=P and 0<=r<=R
    return q,p,r,A,Y,Z,J+stock

def run():
    groups={k:[defaultdict(list) for _ in range(4)] for k in ('known','shifted','pooled')};arms=0
    for seed,left,clock,P,R in product(range(320,340),(6,12,18),CLOCKS,(1,3),(1,3)):
        ar=tape(seed,left,clock);pre=('',0,0,0,0,0,0)
        for t in range(16):pre=tick(pre,t,4,0,P,R,ar.get(t,''))
        q,p,r,*_=pre
        keys=((P,R),(P,R,bool(q),bool(p),bool(r)),(P,R,len(q),p,r),(P,R,q,p,r))
        costs=[]
        for g,o in POL:
            state=pre
            for t in range(16,240):state=tick(state,t,g,o,P,R,ar.get(t,''))
            assert state[3]==state[4]+state[5]==24
            costs.append(state[-1]);arms+=1
        for group in ('known' if clock in CLOCKS[:3] else 'shifted','pooled'):
            for m,key in zip(groups[group],keys):m[key].append(costs)
    result={}
    for name,maps in groups.items():
        rows=[]
        for m in maps:
            loss=amb=worlds=0
            for c in m.values():
                optimum=[min(x) for x in c]
                gap=min(map(sum,zip(*c)))-sum(optimum)
                assert gap>=0
                no_common=not any(all(row[j]==b for row,b in zip(c,optimum)) for j in range(12))
                assert no_common==(gap>0)
                loss+=gap;amb+=no_common;worlds+=len(c)*no_common
            rows.append([len(m),loss,amb,worlds])
        assert all(rows[i][1]>=rows[i+1][1] for i in range(3))
        result[name]=rows
    assert arms==17280
    return {'arms':arms,'columns':['groups','regretLowerBound','ambiguousGroups','ambiguousWorlds'],'results':result}

if __name__=='__main__':print(json.dumps(run(),indent=2))

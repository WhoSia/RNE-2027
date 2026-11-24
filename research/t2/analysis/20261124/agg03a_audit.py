from itertools import product, combinations
import json
EPS=1e-8
POL=list(product((3,4,5),(0,2,4,6)))
CLOCKS=('dense','platoon','sparse')
def tape(seed,left,clock):
    x=seed+1; a=list(range(24))
    for i in range(23,0,-1):
        x=(1664525*x+1013904223)&0xffffffff;j=x%(i+1);a[i],a[j]=a[j],a[i]
    return {(i if clock=='dense' else 8*(i//4)+i%4 if clock=='platoon' else i*4):('L' if v<left else 'S') for i,v in enumerate(a)}
def micro(s,t,g,o,P,R,v):
    q,p,r,A,Y,Z,J=s;green=t%8<g; down=(t+o)%8<4;h=q[0] if q else '-'
    x=int(green and h=='S' and r<R); a=int(h=='L' and p<P); y=int(not green and p>0);z=int(down and r>0)
    q=q[x+a:]+((v,) if v else ()); p+=a-y;r+=x-z; A+=int(v is not None);Y+=y;Z+=z
    assert A==len(q)+p+r+Y+Z and 0<=p<=P and 0<=r<=R
    return q,p,r,A,Y,Z,J+len(q)+p+r
def fluid(s,t,g,o,P,R,v,mixed):
    S,L,p,r,A,Y,Z,J=s;gs=t%8<g;down=(t+o)%8<4;total=S+L
    fs=S/total if total else 0;fl=L/total if total else 0
    x=min(S,fs if mixed else 1,max(0,R-r)) if gs else 0
    a=min(L,fl if mixed else 1,max(0,P-p));y=0 if gs else min(p,1);z=min(r,1) if down else 0
    S+=int(v=='S')-x;L+=int(v=='L')-a;p+=a-y;r+=x-z;A+=int(v is not None);Y+=y;Z+=z
    stock=S+L+p+r;assert abs(A-stock-Y-Z)<EPS and min(S,L,p,r)>=-EPS and p<=P+EPS and r<=R+EPS
    return S,L,p,r,A,Y,Z,J+stock
def pick(a):
    i=0
    for j in range(1,len(a)):
        if a[j]<a[i]-EPS:i=j
    return i
def run():
    names=('fixed','trained','mixed','separate','oracle');models=('mixed','separate')
    groups={k:{'policy':{n:[0,0,0,0] for n in names},'model':{m:[0,0.,0.,0,0] for m in models}} for k in ('all',*CLOCKS)}
    for seed,left,clock,P,R in product(range(180,200),(6,12,18),CLOCKS,(1,3),(1,3)):
        ar=tape(seed,left,clock);pre=((),0,0,0,0,0,0)
        for t in range(16):pre=micro(pre,t,4,0,P,R,ar.get(t))
        q,p,r,A,Y,Z,J=pre;fpre=(q.count('S'),q.count('L'),p,r,A,Y,Z,J);mc=[];fc={m:[] for m in models}
        for g,o in POL:
            s=pre
            for t in range(16,240):s=micro(s,t,g,o,P,R,ar.get(t))
            assert s[3]==s[4]+s[5]==24;mc.append(s[-1])
            for m in models:
                s=fpre
                for t in range(16,240):s=fluid(s,t,g,o,P,R,ar.get(t),m=='mixed')
                assert s[4]==24;fc[m].append((s[-1],sum(s[:4])))
        best=min(mc);ids=(4,0 if P==1 else 4,pick([x[0] for x in fc['mixed']]),pick([x[0] for x in fc['separate']]),pick(mc))
        for k in ('all',clock):
            for n,i in zip(names,ids):
                a=groups[k]['policy'][n];d=mc[i]-best;a[0]+=mc[i];a[1]+=d;a[2]=max(a[2],d);a[3]+=d>0
            for m in models:
                a=groups[k]['model'][m];rs=fc[m];a[0]+=12
                for i,(cost,terminal) in enumerate(rs):
                    d=cost-mc[i];a[1]+=d;a[2]+=abs(d);a[3]+=terminal>EPS
                for i,j in combinations(range(12),2):
                    d=rs[i][0]-rs[j][0];a[4]+=abs(d)>EPS and d*(mc[i]-mc[j])<0
    return {'policy_columns':['J','regret','worst','miss'],'model_columns':['arms','signed','absolute','nonclear','strictFlips'],'groups':groups}
if __name__=='__main__':print(json.dumps(run(),indent=2))

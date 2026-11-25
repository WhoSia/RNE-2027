from itertools import product
from collections import defaultdict
from fractions import Fraction
import json
# Integer lattice flux is represented exactly as F60=60*mean internal flux.
def f60(x):
    return sum(min(15*a,36,10*(6-b)) for a,b in zip(x,x[1:]))
states=list(product(range(7),repeat=4))
masks=list(product((-1,1),repeat=4))
rows=[]; cells=[defaultdict(list),defaultdict(list)]
for x in states:
    f=f60(x); M=sum(x); tv=sum(abs(a-b) for a,b in zip(x,x[1:]))
    for mask in masks:
        y=tuple(max(0,min(6,a+b)) for a,b in zip(x,mask)); keys=(y,(y,M))
        row=(x,y,M,f,tv,mask,keys);rows.append(row)
        for i,k in enumerate(keys):cells[i][k].append((x,f))
# Only compute conditional mean values once per key.
fit=[]
for m in cells:
    fit.append({k:(tuple(Fraction(sum(x[j] for x,f in a),len(a)) for j in range(4)),Fraction(sum(f for x,f in a),len(a)),Fraction(sum(f>=60 for x,f in a),len(a))) for k,a in m.items()})
loss=defaultdict(lambda:[0,0.,0.,0.,0.])
for x,y,M,f,tv,mask,keys in rows:
    for i,k in enumerate(keys):
        mu,ef,p=fit[i][k]; plug=f60(mu)
        assert plug>=ef
        for name,pred,prob in [('state',plug,int(plug>=60)),('flux',ef,p)]:
            for group,w in [('matched',1),('common',int(len(set(mask))==1)),('smooth',19-tv),('heterogeneous',1+tv)]:
                if not w:continue
                s=loss[(group,i,name)];s[0]+=w;s[1]+=w*float((pred-f)**2)/3600;s[2]+=w*float((prob-int(f>=60))**2);s[3]+=w*(int(prob>=Fraction(1,2))!=int(f>=60));s[4]+=w*float((plug-ef)**2)/3600
out={'states':len(states),'rows':len(rows),'keys':[len(m) for m in cells],'stats':{'/'.join(map(str,k)):{'weight':v[0],'fluxMSE':v[1]/v[0],'brier':v[2]/v[0],'classification':v[3]/v[0],'gap':v[4]/v[0]} for k,v in loss.items()}}
parts={}
for name in ['total','histogram','histogram_endpoints','ordered']:
    m=defaultdict(list)
    for x in states:
        key=sum(x) if name=='total' else tuple(sorted(x)) if name=='histogram' else (tuple(sorted(x)),x[0],x[-1]) if name=='histogram_endpoints' else x
        m[key].append(f60(x))
    floor=sum(Fraction(sum(v*v for v in a))-Fraction(sum(a)**2,len(a)) for a in m.values())/len(states)/3600
    parts[name]={'groups':len(m),'floor':float(floor),'range':max(max(a)-min(a) for a in m.values())/60}
out['partition']=parts
print(json.dumps(out,indent=2))

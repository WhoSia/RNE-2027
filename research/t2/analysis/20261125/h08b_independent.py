from itertools import product
from functools import lru_cache
from collections import defaultdict
import json
W=list(product(range(4),range(4),range(3),range(3)))
A=range(3)

def transition(state,a,arr,dep,order):
    s,l,x,y=state
    q=[s,l]; o=[x,y]
    prior=sum(state)
    departed=0
    if order=='DS' and o[dep]:
        o[dep]-=1; departed=1
    # individual transfer operations rather than vector min
    for i,slots in enumerate((a,2-a)):
        for _ in range(slots):
            if q[i] and o[i]<2:
                q[i]-=1; o[i]+=1
    residual=tuple(q)
    if order=='SD' and o[dep]:
        o[dep]-=1; departed=1
    q[arr]+=1
    new=tuple(q+o)
    assert sum(new)==prior+1-departed and min(new)>=0 and max(o)<=2
    return new,residual

out=[]
for order,obj in product(('SD','DS'),('total','fair','terminal')):
    @lru_cache(None)
    def v(w,h,cs=0,cl=0):
        if h==0:
            return max(cs,cl) if obj=='fair' else sum(w) if obj=='terminal' else cs+cl
        return min(qvalues(w,h,cs,cl))
    def qvalues(w,h,cs=0,cl=0):
        result=[]
        for a in A:
            cost=0
            for ar,de in product(range(2),repeat=2):
                nw,(s,l)=transition(w,a,ar,de,order)
                cost+=v(nw,h-1,cs+s,cl+l)
            result.append(cost)
        return result
    def reps(w):
        s,l,x,y=w;e=(min(s,2-x),min(l,2-y))
        return {'total':(s+l,), 'q':(s,l),'e':e,'qe':(s,l,*e),'qeO':(s,l,*e,x+y),'full':w}
    for h in (1,2,3):
        groups={k:defaultdict(list) for k in reps(W[0])}
        for w in W:
            q=qvalues(w,h);r=tuple(c-min(q) for c in q)
            for k,key in reps(w).items():groups[k][key].append(r)
        for k,g in groups.items():
            bad=[rr for rr in g.values() if not any(all(r[a]==0 for r in rr) for a in A)]
            nonhelly=sum(all(any(x[a]==y[a]==0 for a in A) for x,y in product(rr,repeat=2)) for rr in bad)
            out.append(dict(order=order,objective=obj,h=h,rep=k,groups=len(g),badGroups=len(bad),badWorlds=sum(map(len,bad)),bayesNumerator=sum(min(sum(r[a] for r in rr) for a in A) for rr in g.values()),worstNumerator=max(min(max(r[a] for r in rr) for a in A) for rr in g.values()),nonHellyGroups=nonhelly))
    v.cache_clear()
print(json.dumps(out,separators=(',',':')))

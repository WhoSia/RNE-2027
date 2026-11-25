from itertools import product
from functools import lru_cache
from collections import defaultdict
import json
A=(0,1)
WORDS=[w for n in range(5) for w in product(A,repeat=n)]
rows=[]
for K,mode,obj in product(((2,1),(2,2)),('FIFO','SKIP','FIXED'),('total','fair')):
    worlds=list(product(range(K[0]+1),range(K[1]+1),WORDS))
    def step(w,a,arr):
        q=list(w[:2]); buf=list(w[2]); before=[q[i]+buf.count(i) for i in A]
        for _ in range(2):
            if q[a]: q[a]-=1
        for _ in range(2):
            if not buf: break
            eligible=[i for i,x in enumerate(buf) if q[x]<K[x]]
            if mode=='FIFO':
                if 0 not in eligible: break
                j=0
            elif mode=='SKIP':
                if not eligible: break
                j=eligible[0]
            else:
                if not eligible: break
                j=min(eligible,key=lambda j:(buf[j],j))
            q[buf.pop(j)]+=1
        rs=tuple(q[i]+buf.count(i) for i in A)
        assert rs==tuple(before[i]-(min(w[a],2) if i==a else 0) for i in A)
        assert all(0<=q[i]<=K[i] for i in A)
        buf.append(arr)
        return (*q,tuple(buf)),rs
    @lru_cache(None)
    def val(w,h,acc):
        if h==0: return sum(acc) if obj=='total' else max(acc)
        return min(cost(w,h,acc))
    def cost(w,h,acc):
        out=[]
        for a in A:
            value=0
            for arr in A:
                nw,rs=step(w,a,arr)
                value+=val(nw,h-1,tuple(acc[i]+rs[i] for i in A))
            out.append(value)
        return out
    def reps(w):
        q=w[:2]; buf=w[2]; c=(*q,buf.count(0),buf.count(1))
        run=tuple(x for i,x in enumerate(buf) if all(y==x for y in buf[:i+1]))
        return {'q':q,'C':c,'H1':(*c,buf[:1]),'H2':(*c,buf[:2]),'H3':(*c,buf[:3]),'RUN':(*c,run),'FULL':w}
    for h in range(1,5):
        groups={k:defaultdict(list) for k in reps(worlds[0])}
        for w in worlds:
            v=cost(w,h,(0,0)); r=[x-min(v) for x in v]
            for k,p in reps(w).items(): groups[k][p].append(r)
        for k,g in groups.items():
            bad=[rr for rr in g.values() if not any(all(r[a]==0 for r in rr) for a in A)]
            rows.append([len(worlds),len(g),len(bad),sum(map(len,bad)),sum(min(sum(r[a] for r in rr) for a in A) for rr in g.values()),max(min(max(r[a] for r in rr) for a in A) for rr in g.values())])
    val.cache_clear()
# Portable polynomial fingerprint of aggregate integer sequence; also report totals.
h=2166136261
for row in rows:
    for n in row: h=((h^n)*16777619)&0xffffffff
print(json.dumps({'rows':len(rows),'fingerprint':h,'sums':[sum(r[i] for r in rows) for i in range(6)]}))

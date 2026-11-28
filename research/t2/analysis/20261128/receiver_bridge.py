"""Offline receiver-only parity and 2x2 mechanism bridge; no road control."""
from collections import deque, defaultdict
from itertools import product
import json, hashlib
from receiving_cells_v15 import ReceivingCells, LinkConfig
from queue_oracle import make_tape


def step(cells, last, t, green, clock):
    """Independent array implementation: exit, snapshot moves, no admission."""
    out = None
    if green and cells[-1] is not None and (t % 2 == 0 if clock == 'even' else t-last >= 2):
        out, cells[-1], last = cells[-1], None, t
    old = tuple(cells)
    cells = list(old)
    for i, v in enumerate(old[:-1]):
        if v is not None and old[i+1] is None:
            cells[i], cells[i+1] = None, v
    return cells, last, out


def exhaustive():
    ncases = 0
    examples = {}
    for cap in (1,2,4,8):
        groups = defaultdict(set)
        for mask in range(1<<cap):
            initial = [(i,'L',0) if mask & (1<<i) else None for i in range(cap)]
            for green, elapsed, request in product((False,True),range(4),(False,True)):
                ref = ReceivingCells(LinkConfig(cells=cap, downstream_green_s=60 if green else 0))
                ref.occupied = {i:v for i,v in enumerate(initial) if v is not None}
                ref.last_exit = 10-elapsed
                c,last,out = step(initial.copy(),10-elapsed,10,green,'headway')
                assert ref.tick(10)==out
                accept = None
                if request:
                    v=(99,'S',10); accept=c[0] is None
                    if accept: c[0]=v
                    assert ref.accept(v)==accept
                assert ref.occupied=={i:v for i,v in enumerate(c) if v is not None}
                assert ref.last_exit==last and ref.denied_entries==int(request and not accept)
                ncases+=1
                if request:
                    groups[(mask.bit_count(),green,elapsed)].add((out is not None,accept))
        examples[str(cap)] = sum(len(v)>1 for v in groups.values())
    return {'cases':ncases,'count_ambiguous_groups':examples}


def run(tape,layout,cap,onset,period,representation,clock, trace=False):
    arrivals=defaultdict(list)
    for t,i,m in tape: arrivals[t].append((i,m,t))
    queues={k:deque() for k in ('shared','L','S')}
    cells=[None]*cap; fifo=deque(); last=-10**9
    ref=ReceivingCells(LinkConfig(cap,period,period//2,0 if onset=='green' else period//2,2)) if representation=='cell' and clock=='headway' else None
    dep={}; integral=blocked=entered=checks=0; frames=[]
    for t in range(1000):
        green=(t%period<period//2)==(onset=='green')
        if representation=='cell':
            cells,last,out=step(cells,last,t,green,clock)
        else:
            out=None
            if green and fifo and (t%2==0 if clock=='even' else t-last>=2):
                out=fifo.popleft();last=t
        if ref is not None: assert ref.tick(t)==out
        if out is not None:
            i,m,a=out;assert i not in dep;dep[i]=(m,t-a)
        m='L' if t//12%2==0 else 'S';q=queues['shared' if layout=='shared' else m]
        entry=None;denied=False
        if q and q[0][1]==m:
            v=q[0]
            ok=cells[0] is None if representation=='cell' else len(fifo)<cap
            if ref is not None: assert ref.accept(v)==ok
            if ok:
                entry=q.popleft()
                if representation=='cell': cells[0]=entry
                else: fifo.append(entry)
            else: blocked+=1;denied=True
        if ref is not None:
            assert ref.occupied=={i:v for i,v in enumerate(cells) if v is not None}
            assert ref.last_exit==last and ref.denied_entries==blocked
            checks+=1
        for v in arrivals[t]: queues['shared' if layout=='shared' else v[1]].append(v);entered+=1
        receive=[v for v in cells if v is not None] if representation=='cell' else list(fifo)
        ids=[v[0] for q in queues.values() for v in q]+[v[0] for v in receive]+list(dep)
        stock=sum(map(len,queues.values()))+len(receive)
        assert len(ids)==len(set(ids))==entered and stock==entered-len(dep) and len(receive)<=cap
        integral+=stock
        if trace: frames.append({'t':t,'out':out[0] if out else None,'entry':entry[0] if entry else None,'denied':denied,'receiver':[v[0] if v else None for v in cells] if representation=='cell' else [v[0] for v in fifo],'stock':stock})
        if len(dep)==48:
            assert stock==0 and integral==sum(v for _,v in dep.values())
            l=[v for m,v in dep.values() if m=='L'];s=[v for m,v in dep.values() if m=='S']
            return (integral,blocked,sum(l),sum(s),t,max(l),max(s)),checks,frames
    raise RuntimeError('uncleared')


def main():
    audit=exhaustive(); models=list(product(('fifo','cell'),('even','headway'))); rows=[]; parity=0; old=[]
    for seed,share,family in product(range(92801,92817),(.25,.5,.75),('dispersed','platoon4')):
        tape=make_tape(seed,share,family)
        for layout,cap,onset in product(('shared','separate'),(2,4,8),('green','red')):
            vals=[]
            for rep,clock in models:
                a,ac,_=run(tape,layout,cap,onset,30,rep,clock);b,bc,_=run(tape,layout,cap,onset,60,rep,clock);parity+=ac+bc
                vals.append([a[0],b[0]])
                if (rep,clock)==('fifo','even'):old.append([seed,share,family,layout,cap,onset]+[v for pair in zip(a,b) for v in pair])
            rows.append([seed,share,family,layout,cap,onset,vals])
    h=2166136261
    for row in old:
        for x in row:
            v=int(x*100) if isinstance(x,float) else x
            for ch in str(v):h=((h^ord(ch))*16777619)%2**32
            h=((h^124)*16777619)%2**32
    assert h==2944522386
    def summarize(z,j):
        ds=[r[6][j][0]-r[6][j][1] for r in z]
        return {'n':len(z),'win30':sum(d<0 for d in ds),'win60':sum(d>0 for d in ds),'ties':sum(d==0 for d in ds),'fixed30':sum(max(d,0) for d in ds),'fixed60':sum(max(-d,0) for d in ds),'frozen':sum(max(-d,0) if r[5]=='red' and r[1]==.75 else max(d,0) for r,d in zip(z,ds)),'delta_sum':sum(ds)}
    sign=lambda d:(d>0)-(d<0)
    ds=[[a-b for a,b in r[6]] for r in rows]
    edges={f'{a}->{b}':sum(sign(d[a])!=sign(d[b]) for d in ds) for a,b in ((0,1),(0,2),(1,3),(2,3))}
    inter=[d[3]-d[2]-d[1]+d[0] for d in ds]
    # Same occupancy count, different reachable states: cap=2, no departures,
    # a token admitted in previous tick is at 1 now, whereas two adjacent
    # tokens in cap=3 can prevent entry even with vacant last cell before step.
    witnesses=[]
    for mask in range(1<<4):
        init=[(i,'L',0) if mask&(1<<i) else None for i in range(4)]
        c,_,_=step(init.copy(),-99,10,False,'headway')
        if sum(v is not None for v in init)==2:
            witnesses.append({'before': ''.join('1' if v else '0' for v in init),'after':''.join('1' if v else '0' for v in c),'admit':c[0] is None})
    # Reachability with red for 0..3 and arbitrary arrival attempt sequences.
    reachable={}
    for reqs in product((False,True),repeat=4):
        c=[None]*4;last=-99
        for t,request in enumerate(reqs):
            c,last,_=step(c,last,t,False,'headway')
            if request and c[0] is None:c[0]=(t,'L',t)
        mask=''.join('1' if v else '0' for v in c)
        reachable.setdefault(mask,[int(v) for v in reqs])
    reachable_witness=[dict(w,requests=reachable[w['before']]) for w in witnesses if w['before'] in reachable]
    assert {w['admit'] for w in reachable_witness}=={False,True}
    tape=make_tape(92801,.75,'dispersed')
    _,_,a=run(tape,'shared',4,'red',30,'fifo','even',True)
    _,_,b=run(tape,'shared',4,'red',30,'cell','even',True)
    # First observable action difference (not just different spatial representation).
    ix=next(i for i,(x,y) in enumerate(zip(a,b)) if (x['out'],x['entry'],x['denied'])!=(y['out'],y['entry'],y['denied']))
    raw=json.dumps(rows,separators=(',',':')).encode();open('receiver_bridge_rows.json','wb').write(raw)
    result={'status':'RECEIVER_COMPONENT_PARITY_NOT_FULL_T2','models':['/'.join(x) for x in models],'exhaustive':audit,'pairs_per_model':len(rows),'arms':len(rows)*len(models)*2,'actual_source_tick_parity':parity,'baseline_fingerprint':h,'overall':[summarize(rows,j) for j in range(4)],'red_high_share':[summarize([r for r in rows if r[5]=='red' and r[1]==.75],j) for j in range(4)],'strata':{f'{l}/{c}':[summarize([r for r in rows if r[3]==l and r[4]==c],j) for j in range(4)] for l,c in product(('shared','separate'),(2,4,8))},'sign_changes':edges,'interaction':{'nonzero':sum(x!=0 for x in inter),'sum':sum(inter),'min':min(inter),'max':max(inter)},'reachable_witness':reachable_witness,'first_action_difference':{'case':[92801,.75,'dispersed','shared',4,'red',30],'fifo':a[max(0,ix-1):ix+1],'cell':b[max(0,ix-1):ix+1]},'rows_sha256':hashlib.sha256(raw).hexdigest()}
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()

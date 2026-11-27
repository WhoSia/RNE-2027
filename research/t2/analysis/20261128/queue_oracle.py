from collections import deque, defaultdict
from itertools import product
import json


def make_tape(seed, share, family):
    state = seed
    def draw(n):
        nonlocal state
        state = (state * 1664525 + 1013904223) % 2**32
        return state * n // 2**32
    labels = ['L'] * int(48 * share) + ['S'] * (48-int(48*share))
    for i in reversed(range(1,48)):
        j = draw(i+1)
        labels[i], labels[j] = labels[j], labels[i]
    times = [i*4+draw(4) if family=='dispersed' else i//4*16+draw(2) for i in range(48)]
    return sorted(zip(times,range(48),labels))


def run(tape, layout, capacity, onset, period):
    arrivals = defaultdict(list)
    for t,i,m in tape: arrivals[t].append((t,i,m))
    queues = {k:deque() for k in ('shared','L','S')}
    downstream = deque()
    departures = {}
    integral = 0
    blocked = 0
    entered = 0
    for t in range(1000):
        is_green = (t % period < period//2) == (onset=='green')
        if is_green and t%2==0 and downstream:
            a,i,m = downstream.popleft()
            assert i not in departures
            departures[i] = (m,t-a)
        m = 'L' if (t//12)%2==0 else 'S'
        lane = queues['shared' if layout=='shared' else m]
        if lane and lane[0][2]==m:
            if len(downstream)==capacity: blocked += 1
            else: downstream.append(lane.popleft())
        for car in arrivals.get(t,[]):
            queues['shared' if layout=='shared' else car[2]].append(car)
            entered+=1
        stock=sum(map(len,queues.values()))+len(downstream)
        assert stock==entered-len(departures) and len(downstream)<=capacity
        integral+=stock
        if len(departures)==48:
            assert stock==0 and integral==sum(v for _,v in departures.values())
            l=[v for m,v in departures.values() if m=='L']; s=[v for m,v in departures.values() if m=='S']
            return (integral,blocked,sum(l),sum(s),t,max(l),max(s))
    raise RuntimeError('not cleared')


def main():
    rows=[]
    for seed,share,family in product(range(92801,92817),(.25,.5,.75),('dispersed','platoon4')):
        tape=make_tape(seed,share,family)
        for layout,cap,onset in product(('shared','separate'),(2,4,8),('green','red')):
            a=run(tape,layout,cap,onset,30);b=run(tape,layout,cap,onset,60)
            row=[seed,share,family,layout,cap,onset]+[v for z in zip(a,b) for v in z]
            rows.append(row)
    def stats(z):
        ds=[r[6]-r[7] for r in z]
        return [len(z),sum(d<0 for d in ds),sum(d>0 for d in ds),sum(max(d,0) for d in ds),sum(max(-d,0) for d in ds),sum(max(-d,0) if r[5]=='red' and r[1]==.75 else max(d,0) for d,r in zip(ds,z))]
    result={'overall':stats(rows),'by_layout_capacity':{f'{l}/{c}':stats([r for r in rows if r[3]==l and r[4]==c]) for l,c in product(('shared','separate'),(2,4,8))},'first':rows[0],'last':rows[-1]}
    # Deterministic integer fingerprint of entire row-level numeric payload and categories.
    h=2166136261
    for row in rows:
        for x in row:
            v = int(x*100) if isinstance(x,float) else x
            for ch in str(v): h=((h^ord(ch))*16777619)%2**32
            h=((h^124)*16777619)%2**32
    result['row_fingerprint']=h
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()

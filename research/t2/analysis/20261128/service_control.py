"""Matched service opportunity control for the synthetic queue experiment."""
from collections import deque, defaultdict
from itertools import product
import json
from queue_oracle import make_tape, run


def eligible(t, onset, period):
    green = (t % period < period // 2) == (onset == 'green')
    parity = (t // 30) % 2 if period == 30 else 0
    return green and t % 2 == parity


def controlled(tape, layout, cap, onset, period):
    arrivals = defaultdict(list)
    for t, i, m in tape:
        arrivals[t].append((t, i, m))
    queues = {k: deque() for k in ('shared', 'L', 'S')}
    receiver = deque()
    departure = {}
    cost = blocked = entered = 0
    for t in range(1000):
        if eligible(t, onset, period) and receiver:
            a, i, m = receiver.popleft()
            assert i not in departure
            departure[i] = (m, t-a)
        m = 'L' if t // 12 % 2 == 0 else 'S'
        q = queues['shared' if layout == 'shared' else m]
        if q and q[0][2] == m:
            if len(receiver) == cap:
                blocked += 1
            else:
                receiver.append(q.popleft())
        for v in arrivals.get(t, []):
            queues['shared' if layout == 'shared' else v[2]].append(v)
            entered += 1
        stock = sum(map(len, queues.values())) + len(receiver)
        assert stock == entered-len(departure) and len(receiver) <= cap
        cost += stock
        if len(departure) == 48:
            assert stock == 0 and cost == sum(v for _, v in departure.values())
            l = [v for m,v in departure.values() if m == 'L']
            s = [v for m,v in departure.values() if m == 'S']
            return cost, blocked, sum(l), sum(s), t, max(l), max(s)
    raise RuntimeError('not cleared')


def main():
    opportunity = {f'{o}/{p}': sum(eligible(t,o,p) for t in range(60)) for o,p in product(('green','red'),(30,60))}
    assert set(opportunity.values()) == {15}
    rows = []
    for seed, share, family in product(range(92801,92817),(.25,.5,.75),('dispersed','platoon4')):
        tape = make_tape(seed,share,family)
        for layout, cap, onset in product(('shared','separate'),(2,4,8),('green','red')):
            a = controlled(tape,layout,cap,onset,30)
            b = controlled(tape,layout,cap,onset,60)
            assert b == run(tape,layout,cap,onset,60)
            rows.append([seed,share,family,layout,cap,onset,a[0],b[0]])
    def summarize(z):
        d = [r[6]-r[7] for r in z]
        f = [max(-v,0) if r[5]=='red' and r[1]==.75 else max(v,0) for r,v in zip(z,d)]
        return {'n':len(z),'win30':sum(v<0 for v in d),'win60':sum(v>0 for v in d),'ties':sum(v==0 for v in d),'fixed30':sum(max(v,0) for v in d),'fixed60':sum(max(-v,0) for v in d),'frozen':sum(f)}
    report = {'status':'MATCHED_OPPORTUNITY_SENSITIVITY_NOT_INDEPENDENT_SAMPLE','eligible_per_60':opportunity,'pairs':len(rows),'controlled_arms':len(rows)*2,'baseline_60_parity_checks':len(rows),'overall':summarize(rows),'red_high_share':summarize([r for r in rows if r[5]=='red' and r[1]==.75]),'by_layout_capacity':{f'{l}/{c}':summarize([r for r in rows if r[3]==l and r[4]==c]) for l,c in product(('shared','separate'),(2,4,8))}}
    print(json.dumps(report,indent=2))
    with open('service_control_rows.json','w',encoding='utf-8') as f:
        json.dump({'columns':['seed','share','family','layout','cap','onset','cost30','cost60'],'rows':rows},f,separators=(',',':'))
if __name__=='__main__':
    main()

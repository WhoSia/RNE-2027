"""Independent count/ordered-FIFO Python replay of P154, all unique arm costs."""
import hashlib
import itertools
import json
import subprocess
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent
GATES={4:'BSBL',8:'BBSSBBLL'}


def step(state,t,gate,reuse,priority,P,D,sink,arrival):
    q,p,d,a,z,j=state
    release=int(d>0 and (t+sink)%4<2)
    space=D-d+release*reuse
    pocket_in=int(bool(q) and q[0]=='L' and p<P)
    eligible=[]
    if q and q[0]=='S' and gate in 'BS':eligible.append('S')
    if p and gate in 'BL':eligible.append('L')
    move=None
    if space and eligible:move=priority if priority in eligible else eligible[0]
    assert not (pocket_in and move=='S')
    q2=q[pocket_in+int(move=='S'):]+((arrival,) if arrival else ())
    p2=p+pocket_in-int(move=='L');d2=d-release+int(move is not None)
    a2=a+int(arrival is not None);z2=z+release
    n=len(q2)+p2+d2
    assert 0<=p2<=P and 0<=d2<=D and a2-z2==n
    return (q2,p2,d2,a2,z2,j+n),dict(t=t,gate=gate,move=move,pocket_in=pocket_in,release=release,q=''.join(q2),p=p2,d=d2,z=z2,j=j+n)


def simulate(pre,tape,P,D,sink,reuse,priority,period,offset,trace=False):
    state=pre;log=[]
    for t in range(8,160):
        state,event=step(state,t,GATES[period][(t+offset)%period],reuse,priority,P,D,sink,tape.get(t))
        if trace:log.append(event)
        if state[4]==7:break
    assert state[3]==state[4]==7 and not any(state[:3])
    return state[5],log


def run():
    src=(ROOT/'p154_equal_duty_phase_factorial.js').read_text()
    marker='  const rank=()=>';assert src.count(marker)==1
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/'probe.js';p.write_text(src.replace(marker,'  return rows;\n'+marker))
        node_rows=json.loads(subprocess.check_output(['node',str(p)],text=True))
    increases=[];cost_rows=[];witness=None
    keys=itertools.product(range(128),(1,2),(1,2),(1,2),(0,2))
    for key,row in zip(keys,node_rows,strict=True):
        mask,interval,P,D,sink=key
        assert key==tuple(row[k] for k in ('mask','interval','P','D','sink'))
        tape={interval*i:'L' if mask&(1<<i) else 'S' for i in range(7)}
        pre=((),0,0,0,0,0)
        for t in range(8):pre,_=step(pre,t,'S' if t%4<2 else 'L',0,'S',P,D,sink,tape.get(t))
        assert pre==(tuple(row['pre']['q']),len(row['pre']['p']),len(row['pre']['d']),row['pre']['a'],row['pre']['z'],row['pre']['j'])
        arms=[(p,o) for p in (4,8) for o in range(p)]
        costs=[[simulate(pre,tape,P,D,sink,reuse,priority,p,o)[0] for p,o in arms] for reuse in (0,1) for priority in ('S','L')]
        assert costs==row['costs'],key
        cost_rows.append([list(key),costs])
        for i,(p,o) in enumerate(arms):
            for k,priority in enumerate(('S','L')):
                old,new=costs[k][i],costs[k+2][i]
                if new>old:
                    item=dict(mask=mask,interval=interval,P=P,D=D,sink=sink,period=p,offset=o,priority=priority,old=old,reuse=new)
                    increases.append(item)
                    if witness is None:
                        witness=dict(case=item,tape=tape,old_trace=simulate(pre,tape,P,D,sink,0,priority,p,o,True)[1],reuse_trace=simulate(pre,tape,P,D,sink,1,priority,p,o,True)[1])
    assert len(increases)==6
    payload=json.dumps(cost_rows,separators=(',',':')).encode()
    return dict(status='EXACT_COST_PARITY_SYNTHETIC_NOT_FIELD',scenarios=len(cost_rows),compared_costs=len(cost_rows)*48,cost_sha256=hashlib.sha256(payload).hexdigest(),increases=increases,witness=witness)

if __name__=='__main__':print(json.dumps(run(),indent=2))

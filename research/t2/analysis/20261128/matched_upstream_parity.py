"""Independent array implementation of restricted synthetic T2; no road controller."""
from collections import Counter, defaultdict, deque
from itertools import product
from pathlib import Path
import hashlib, json, random, pickle
from dual_lane_v11 import DualConfig, run as canonical
from spatial_v10 import Config

def tape_for(seed, share):
    rng=random.Random(seed); labels=['L']*int(36*share)+['S']*(36-int(36*share));rng.shuffle(labels)
    return tuple((4*i+rng.randrange(4),m) for i,m in enumerate(labels))

def oracle(c,tape):
    b=c.base;n=int(b.approach_length_m/b.cell_m);k=int(b.pocket_length_m/b.cell_m)
    assert c.receiver_mode=='cells' and not c.receiver_split and not c.receiver_closures
    assert not c.downstream_conflict_gap_s and not c.lane_change_windows
    lanes=[[None]*n,[None]*n,[None]*k];rx=[None]*c.receiver_slots;outside=[deque(),deque()]
    arrivals=defaultdict(list);rng=random.Random(b.seed+193)
    for i,(t,m) in enumerate(tape):arrivals[t].append((0 if m=='L' or rng.random()>=c.through_B_share else 1,(i,m,t)))
    last=[-999999]*3;adm=[-999999]*2;last_out=-10**9;streak={};C=Counter();frames=[];service=[];access=[];changes=[];departed=set();created=set()
    def coords(a):return [(i-len(a),v[0],v[1]) for i,v in enumerate(a) if v is not None]
    def occupied(a,i):return 0<=i<len(a) and a[i] is not None
    def forward(a,moved):
        for i in range(len(a)-2,-1,-1):
            if a[i] is not None and a[i+1] is None:moved.add(a[i][0]);a[i+1],a[i]=a[i],None
    def signal(t):
        q=(t+b.signal_offset_s)%b.cycle_s;first,second=('L','S') if b.phase_order=='leading' else ('S','L');w={'L':b.left_green_s,'S':b.through_green_s}
        return first if q<w[first] else '-' if q<w[first]+b.clearance_s else second if q<w[first]+b.clearance_s+w[second] else '-'
    for t in range(b.duration_s):
        for j,v in arrivals.get(t,[]):outside[j].append(v);created.add(v[0])
        if (t+c.downstream_offset_s)%c.downstream_cycle_s<c.downstream_green_s and rx[-1] is not None and t-last_out>=c.receiver_headway_s:
            v=rx[-1];rx[-1]=None;last_out=t;C['network_out_'+v[1]]+=1;departed.add(v[0])
        old=rx[:]
        for i in range(len(old)-1):
            if old[i] is not None and old[i+1] is None:rx[i+1],rx[i]=old[i],None
        light=signal(t);denied=False
        for j in (0,1) if light=='S' else (2,) if light=='L' else ():
            a=lanes[j];v=a[-1] if a else None
            if v is None or v[1]!=light or t-last[j]<b.departure_headway_s:continue
            name=('A','B','pocket')[j]
            if rx[0] is not None:C['receiver_denied_attempts']+=1;denied=True;reason='receiver_entry_cell_busy'
            else:a[-1]=None;rx[0]=v;last[j]=t;C['exit_'+light]+=1;C['time_'+light]+=t-v[2];reason='stopline_cross'
            service.append(dict(t=t,vehicle_id=v[0],lane=name,movement=light,reason=reason))
        C['receiver_denied_seconds']+=int(denied);moved=set();forward(lanes[2],moved)
        for j in (0,1):
            a=lanes[j]
            for i in range(n-1,-1,-1):
                v=a[i];fork=n-k-1
                if v is None:continue
                if j==0 and v[1]=='L' and i==fork:
                    if k and lanes[2][0] is None:a[i]=None;lanes[2][0]=v;moved.add(v[0]);access.append(dict(t=t,vehicle_id=v[0],event='pocket_entry',blocker_id=None))
                    else:C['pocket_block_seconds']+=1;access.append(dict(t=t,vehicle_id=v[0],event='pocket_entry_denied',reason='pocket_entry_cell_busy' if k else 'no_pocket',blocker_id=lanes[2][0][0] if k else None))
                elif i<n-1 and a[i+1] is None and not(j==0 and v[1]=='L' and i>=fork):a[i]=None;a[i+1]=v;moved.add(v[0])
        nxt={}
        if c.allow_lane_changes:
            zone=int(c.change_zone_m/b.cell_m);gap=c.lane_change_target_gap_cells;A,B=lanes[:2]
            for i in range(n-1,-1,-1):
                v=A[i]
                if v is None or v[1]!='S' or v[0] in moved or i>=n-k or i<n-zone:continue
                if occupied(A,i+1) and (A[i+1][1]=='L' or occupied(A,i+2)):
                    if any(occupied(B,h) for h in range(i-gap,i+gap+1)):C['lane_change_target_gap_denials']+=1;continue
                    age=streak.get(v[0],0)+1
                    if age<c.lane_change_gap_confirmation_s:nxt[v[0]]=age;C['lane_change_gap_confirmation_wait_s']+=1
                    else:A[i]=None;B[i]=v;C['changes_A_to_B']+=1;changes.append(dict(t=t,vehicle_id=v[0],**{'from':'A','to':'B','cell':i-n}))
        streak=nxt
        for j in (0,1):
            if outside[j] and lanes[j][0] is None and t-adm[j]>=b.entry_headway_s:lanes[j][0]=outside[j].popleft();adm[j]=t;C['admitted']+=1
        out=sum(map(len,outside));up=sum(v is not None for a in lanes for v in a);nr=sum(v is not None for v in rx)
        C['outside_vehicle_seconds']+=out;C['upstream_vehicle_seconds']+=up;C['receiver_vehicle_seconds']+=nr;C['max_receiver']=max(C['max_receiver'],nr)
        ids=[v[0] for a in lanes for v in a if v is not None]+[v[0] for v in rx if v is not None]+[v[0] for a in outside for v in a]
        assert len(ids)==len(set(ids)) and not departed.intersection(ids) and set(ids)|departed==created,(t,'identity conservation')
        frames.append(dict(t=t,signal=light,A=coords(lanes[0]),B=coords(lanes[1]),pocket=[(i,v) for i,v,_ in coords(lanes[2])],outside=out,receiver=tuple((i,v[0],v[1]) for i,v in enumerate(rx) if v is not None)))
    result={key:C[key] for key in ('admitted','exit_S','exit_L','network_out_S','network_out_L','max_receiver','receiver_denied_attempts','receiver_denied_seconds','outside_vehicle_seconds','upstream_vehicle_seconds','receiver_vehicle_seconds','pocket_block_seconds','changes_A_to_B','lane_change_target_gap_denials','lane_change_gap_confirmation_wait_s','common_exit_denied_s')}
    result.update(generated=len(tape),remaining=len(created)-len(departed),outside=out,receiver_final=nr,frames=frames,service_events=service,access_events=access,lane_change_events=changes)
    for m in ('S','L'):result['mean_time_'+m+'_s']=C['time_'+m]/C['exit_'+m] if C['exit_'+m] else None
    return result

def compare(a,b,key):
    for field in b:
        if a[field]!=b[field]:
            if isinstance(a[field],list) and isinstance(b[field],list):
                for i,(x,y) in enumerate(zip(a[field],b[field])):
                    if x!=y:raise AssertionError((key,field,i,x,y))
                raise AssertionError((key,field,'length',len(a[field]),len(b[field])))
            raise AssertionError((key,field,a[field],b[field]))

def main():
    rows=[];arms=frames=events=checkpoints=0
    for seed,share,pocket,bshare,change,cap,onset in product(range(92821,92825),(.25,.75),(7.,28.),(0.,.5),(0,1,2),(2,4),('green','red')):
        tape=tape_for(seed,share);pair=[]
        for period in (30,60):
            b=Config(seed=seed,duration_s=900,cycle_s=60,left_green_s=12,through_green_s=30,clearance_s=3,pocket_length_m=pocket,approach_length_m=140.,cell_m=7.,demand_vph=0,left_fraction=share)
            c=DualConfig(base=b,through_B_share=bshare,allow_lane_changes=change>0,lane_change_gap_confirmation_s=max(change,1),receiver_slots=cap,receiver_mode='cells',downstream_cycle_s=period,downstream_green_s=period//2,downstream_offset_s=0 if onset=='green' else period//2)
            key=(seed,share,pocket,bshare,change,cap,onset,period);a=canonical(c,tape,trace=True);z=oracle(c,tape);compare(a,z,key)
            if pocket==7 and bshare==0 and change==0 and cap==2 and onset=='green' and period==30:
                cp=canonical(c,tape,trace=True,checkpoint_at=84);before=pickle.dumps(cp);replay=canonical(c,tape,trace=True,resume_from=cp);assert replay==a and pickle.dumps(cp)==before;checkpoints+=1
            arms+=1;frames+=len(a['frames']);events+=sum(len(a[k]) for k in ('service_events','access_events','lane_change_events'))
            m={k:a[k] for k in ('remaining','network_out_L','network_out_S','outside_vehicle_seconds','upstream_vehicle_seconds','receiver_vehicle_seconds','pocket_block_seconds','changes_A_to_B','receiver_denied_attempts','receiver_denied_seconds')};m['cost']=sum(m[k] for k in ('outside_vehicle_seconds','upstream_vehicle_seconds','receiver_vehicle_seconds'));pair.append(m)
        rows.append(dict(seed=seed,share=share,pocket_m=pocket,b_share=bshare,change=change,cap=cap,onset=onset,arms=pair,delta=pair[0]['cost']-pair[1]['cost']))
    def stats(z):
        ds=[r['delta'] for r in z];f=[max(-r['delta'],0) if r['share']==.75 and r['onset']=='red' else max(r['delta'],0) for r in z]
        return dict(pairs=len(z),win30=sum(d<0 for d in ds),win60=sum(d>0 for d in ds),ties=sum(d==0 for d in ds),fixed30_regret=sum(max(d,0) for d in ds),fixed60_regret=sum(max(-d,0) for d in ds),frozen_regret=sum(f),uncleared_arms=sum(a['remaining']>0 for r in z for a in r['arms']))
    result=dict(status='EXACT_RESTRICTED_SYNTHETIC_T2_PARITY',arms=arms,pairs=len(rows),tapes=8,seed_blocks=4,frame_checks=frames,event_records_compared=events,checkpoint_replays=checkpoints,overall=stats(rows),by_geometry={f'{p}/{bs}/{ch}/{cap}':stats([r for r in rows if (r['pocket_m'],r['b_share'],r['change'],r['cap'])==(p,bs,ch,cap)]) for p,bs,ch,cap in product((7.,28.),(0.,.5),(0,1,2),(2,4))},red_high_share=stats([r for r in rows if r['share']==.75 and r['onset']=='red']),rows=rows)
    assert arms==768 and len(rows)==384 and checkpoints==8
    path=Path(__file__).with_name('MATCHED_UPSTREAM_PARITY_RESULT.json');path.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('rows','by_geometry')},indent=2));print('sha256',hashlib.sha256(path.read_bytes()).hexdigest())
if __name__=='__main__':main()

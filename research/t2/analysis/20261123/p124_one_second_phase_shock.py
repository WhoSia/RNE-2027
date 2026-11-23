"""P124 preregistered one-second phase shock, full occupancy stock trace."""
import json
from collections import defaultdict
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch
from receiving_cells_v15 import ReceivingCells
from p85_signal_coordination import build_config,p31,run,score,phases

HERE=Path(__file__).resolve().parent
ZONES=('outside','A','B','pocket','receiver')
WINDOWS=((84,114),(114,144),(144,204),(204,324),(324,4800))

def replay(cfg,tape,cp,phi):
    def green(self,t):
        assert t>=84
        return (t-84-phi)%30<15
    with patch.object(ReceivingCells,'green',green):
        r=run(cfg,tape,resume_from=cp,phase_overrides=phases(6,'left_first'),trace=True)
    assert r['remaining']==0 and r['generated']==60
    frames={f['t']:f for f in r['frames'] if f['t']>=84}
    assert len(frames)==4800-84
    return r,frames

def stock(f):
    return {'outside':f['outside'],'A':len(f['A']),'B':len(f['B']),
            'pocket':len(f['pocket']),'receiver':len(f['receiver'])}

def main():
    cfg=build_config(86001,900,.75,7,4,.5)
    tape=p31.clock(cfg.base,'uniform')
    cfg=replace(cfg,base=replace(cfg.base,duration_s=4800),downstream_offset_s=0)
    cp=run(cfg,tape,checkpoint_at=84,trace=True)
    (a,af),(b,bf)=(replay(cfg,tape,cp,p) for p in (0,1))
    assert score(a,0)==7126 and score(b,0)==7858
    ts={};first_differences=[]
    zone_totals={z:0 for z in ZONES}
    maxgap=(0,None)
    for t in range(84,4800):
        az=stock(af[t]);bz=stock(bf[t]);gap={z:az[z]-bz[z] for z in ZONES}
        for z in ZONES:zone_totals[z]+=gap[z]
        d=sum(gap.values())
        if abs(d)>abs(maxgap[0]):maxgap=(d,t)
        ts[t]={'delta':d,'by_zone':gap}
        if af[t]!=bf[t] and len(first_differences)<10:
            first_differences.append({'tick':t,'stock_delta':d,'by_zone':gap,
                                     'A_ids_a':[x[1] for x in af[t]['A']][:10],
                                     'A_ids_b':[x[1] for x in bf[t]['A']][:10],
                                     'receiver_ids_a':[x[1] for x in af[t]['receiver']],
                                     'receiver_ids_b':[x[1] for x in bf[t]['receiver']]})
    assert sum(zone_totals.values())==score(a,0)-score(b,0)==-732
    windows=[]
    for start,end in WINDOWS:
        summ={z:sum(ts[t]['by_zone'][z] for t in range(start,end)) for z in ZONES}
        windows.append({'start':start,'end':end,'vehicle_seconds':sum(summ.values()),'by_zone':summ})
    assert sum(x['vehicle_seconds'] for x in windows)==-732
    checkpoints=[]
    for t in (84,113,114,143,144,203,204,323,324,400,600):
        checkpoints.append({'t':t,'a':stock(af[t]),'b':stock(bf[t]),'difference':ts[t]['by_zone']})
    # exact completed exit events by ID from physical post-tick snapshots and prior receiver
    exited={}
    for phi,frames in ((0,af),(1,bf)):
        prev={v[1] for v in cp['state']['receiver'].snapshot()}
        byid={e[1]:e[0] for e in cp['state']['receiver'].exits}
        for t in range(84,4800):
            curr={v[1] for v in frames[t]['receiver']}
            for vid in prev-curr:
                assert vid not in byid
                byid[vid]=t
            prev=curr
        assert len(byid)==60
        exited[phi]=byid
    changed_exit=[{'id':i,'exit0':exited[0][i],'exit1':exited[1][i],
                   'delta':exited[0][i]-exited[1][i]} for i in range(60)
                  if exited[0][i]!=exited[1][i]]
    assert sum(x['delta'] for x in changed_exit)==-732
    result={'status':'P124_1S_PHASE_SHOCK_EXACT_QUEUE_STOCK_TRACE','prereg':'P124_ONE_SECOND_PHASE_SHOCK_PREREG.md',
            'cost_phi0':score(a,0),'cost_phi1':score(b,0),'delta':-732,
            'first_differing_tick':first_differences[0]['tick'],
            'first_ten_differing_ticks':first_differences,
            'maximum_abs_occupancy_delta':{'signed':maxgap[0],'tick':maxgap[1]},
            'zone_delta':zone_totals,'windows':windows,'checkpoints':checkpoints,
            'changed_exit_vehicle_count':len(changed_exit),'first_ten_changed_vehicle_ids':changed_exit[:10],
            'vehicle_exit_deltas':changed_exit,'conservation_checks_passed':True,
            'limitation':'Within-model deterministic event reconstruction; five windows preregistered; 4800 ticks include lengthy cleared-tail zeros; an explanatory queue-dynamics theorem is still absent.'}
    (HERE/'P124_RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k in ('status','first_differing_tick','maximum_abs_occupancy_delta','zone_delta','windows','changed_exit_vehicle_count')},ensure_ascii=False,indent=2))
    return result

if __name__=='__main__':main()

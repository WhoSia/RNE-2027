"""Reproduce the archived P11-S event-clock and queue-metric regressions."""
import sys, json, hashlib, zipfile, importlib.util
from pathlib import Path
from dataclasses import asdict
from math import isfinite
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from lane_fifo import Demand, simulate

def load_old():
    source=ROOT/'baseline'/'lane_fifo_S_original.py'
    code=source.read_bytes()
    dest=ROOT/'results'/'original_s_lane_fifo.py'
    dest.write_bytes(code)
    spec=importlib.util.spec_from_file_location('s_lane_original',dest)
    module=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=module
    spec.loader.exec_module(module)
    return module,hashlib.sha256(code).hexdigest()

def main():
    old,old_sha=load_old()
    scenarios={
        'large_clock_small_duration':(1e16,.25),
        'overflowing_exit':(1e308,1e308),
        'normal_clock':(1,.25),
    }
    witnesses=[]
    for name,(t,dur) in scenarios.items():
        before=old.simulate([old.Demand(t,'v','L',('r',),dur)], {'r':1})
        try:
            after=simulate([Demand(t,'v','L',('r',),dur)], {'r':1})
            fixed={'status':'accepted','entry':after.entries['v'],'exit':after.exits['v']}
        except ValueError as e:
            fixed={'status':'rejected','reason':str(e)}
        witnesses.append({'scenario':name,'at_s':t,'duration_s':dur,'old_entry':before.entries['v'],
                          'old_exit':before.exits['v'] if isfinite(before.exits['v']) else 'Infinity',
                          'new':fixed})
    q_old=old.simulate([old.Demand(0,'a','A',('r',),1)],{'r':1})
    q_new=simulate([Demand(0,'a','A',('r',),1)],{'r':1})
    queue={'scenario':'immediate_entry','old_max_waiting':q_old.max_waiting['A'],
           'new_max_waiting':q_new.max_waiting['A']}
    # Comparison of detailed admission/exits for fixed non-pathological inputs.
    obs=[(0,'a','A','ra',10),(.1,'a2','A','ra',1),(.2,'b','B','rb',1)]
    old_run=old.simulate([old.Demand(t,i,l,(r,),dt) for t,i,l,r,dt in obs], {'ra':1,'rb':1})
    new_run=simulate([Demand(t,i,l,(r,),dt) for t,i,l,r,dt in obs], {'ra':1,'rb':1})
    assert old_run.entries==new_run.entries and old_run.exits==new_run.exits and old_run.log==new_run.log
    evidence={'source_sha256_from_sealed_S_zip':old_sha,'witnesses':witnesses,'queue_metric':queue,
              'legacy_vs_patch_event_trace_identical':True,'old_max_waiting_A':old_run.max_waiting.get('A'),
              'new_max_waiting_A':new_run.max_waiting.get('A')}
    (ROOT/'results'/'audit_results.json').write_text(json.dumps(evidence,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
    print(json.dumps(evidence,ensure_ascii=False,indent=2))
if __name__=='__main__':main()

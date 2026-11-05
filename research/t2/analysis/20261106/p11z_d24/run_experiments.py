"""Reproduce synthetic finite storage, handoff, GTFS calendar cases."""
import sys
import json
import datetime as dt
from pathlib import Path
from zipfile import ZipFile
sys.path.insert(0,str(Path(__file__).parent/'src'))
from phase_network import Step,Movement,simulate,DeadlockError
from gtfs_gate import audit_zip
ROOT=Path(__file__).parent
OUT=ROOT/'results'
OUT.mkdir(exist_ok=True)

def m(name,at,lane,*phases):
    return Movement(name,at,lane,'vehicle',tuple(Step(tuple(z),ticks) for z,ticks in phases))

# Physical representation: zone slots, not length-validated or empirical.
scene=[m('ped_B',0,'P',(('B',),3)),m('vehicle',0,'L1',(('A',),2),(('B',),2)),m('follower',1,'L1',(('A',),1))]
results={}
for cap in (1,2):
    z=simulate(scene,{'A':cap,'B':1})
    results[str(cap)]={'starts':z.starts,'finishes':z.finishes,'log':z.log,'max_occupancy':z.max_occupancy,'max_waiting':z.max_waiting}
conflicts=[m('east',0,'E',(('A',),2),(('B',),1)),m('west',0,'W',(('B',),2),(('A',),1))]
try:simulate(conflicts,{'A':1,'B':1})
except DeadlockError as exc:
    deadlock={'cycle':exc.cycle,'blocked':exc.blocked}
else:raise AssertionError('expected circular wait')
with_fixture=ROOT/'raw'/'synthetic_gtfs_fixture.zip'
# test-only fixture, NOT an agency-sourced actual feed.
sys.path.insert(0,str(ROOT/'tests'))
from test_gtfs_gate import fixture
fixture(with_fixture)
calendar={}
for date in (dt.date(2026,11,6),dt.date(2026,11,9)):
    f=audit_zip(with_fixture,date)
    calendar[date.isoformat()]={key:f[key] for key in ('sha256','source_bytes','service_date','timezone','active_service_ids','active_trips','connections')}
out={'scene':results,'deadlock':deadlock,'gtfs_fixture':calendar,'evidence_type':'synthetic_only','policy_track':'P12_FROZEN'}
(OUT/'D24_results.json').write_text(json.dumps(out,indent=2,ensure_ascii=False,default=list),encoding='utf-8')
print(json.dumps({'capacity_one':results['1']['starts'],'capacity_two':results['2']['starts'],'deadlock_cycle':deadlock['cycle'],'gtfs_service_ids':{d:z['active_service_ids'] for d,z in calendar.items()}},ensure_ascii=False,indent=2))

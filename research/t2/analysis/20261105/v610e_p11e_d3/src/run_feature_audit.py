"""Deterministic, entirely synthetic audit of regulatory and geometric constraints."""
import json
from pathlib import Path
from datetime import datetime
from road_ir import RoadLane, LaneConnection, RoadIR
from road_rules import RoadRules,Rule,Window,readiness
from physical_limits import VehicleEnvelope,RoadLimits,audit
from signal_binding import read_programs,inspect_bindings

def run():
    graph=RoadIR((RoadLane('entry',100,10),RoadLane('left',50,10),RoadLane('bridge',80,12)),
                 (LaneConnection('turn_left','entry','left','J','left','J',0),
                  LaneConnection('straight','entry','bridge','J','straight','J',1)),
                 'synthetic-fixture',('geometric_conflicts_unknown',))
    rules=RoadRules(graph,(
       Rule('turn_left','passenger','allow','synthetic_sign_A'),
       Rule('turn_left','passenger','deny','synthetic_peak_restriction', Window(7*60,9*60,frozenset({0,1,2,3,4}))),
       Rule('straight','passenger','allow','synthetic_sign_B')),'Asia/Seoul')
    t=datetime.fromisoformat('2026-11-02T08:20:00+09:00')
    status=readiness(graph,rules,'passenger',t)
    signal_xml='<additional><tlLogic id="J" programID="sample" offset="0"><phase duration="10" state="Gr"/><phase duration="3" state="yr"/><phase duration="10" state="rG"/><phase duration="3" state="ry"/></tlLogic></additional>'
    result={'fixture_only':True,'policy_track':'FROZEN - no new optimization or selection',
            'road':graph.summary(),'regulation':status,
            'time_dependent_turn_left':rules.evaluate('turn_left','passenger',t).__dict__,
            'bridge_height_audit':audit(VehicleEnvelope('example_bus',4.1,2.4,12.,18.),
                                       RoadLimits('bridge',max_height_m=4.0,provenance='synthetic_sign_C')),
            'signal_binding':inspect_bindings(graph,read_programs(signal_xml)),
            'limitations':['No real traffic hardware','No real OSM turn-restriction parser','No SUMO vehicle simulation',
                           'No field calibration','Geometric conflicts unresolved',
                           'Vehicle footprint and bridge load dynamic behavior not modeled']}
    return result

if __name__=='__main__':
    p=Path(__file__).resolve().parents[1]/'results';p.mkdir(exist_ok=True)
    x=run();(p/'feature_audit.json').write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');print(json.dumps(x,indent=2))

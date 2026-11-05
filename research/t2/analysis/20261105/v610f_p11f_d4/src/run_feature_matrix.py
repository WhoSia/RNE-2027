"""Reproducible synthetic structural tests, NOT a traffic simulation or field legality audit."""
from datetime import datetime
from pathlib import Path
from grade_geometry import WayGeometry,TurnPocket,audit_crossing
from osm_relations import ingest,evaluate
from road_rules import Window
from variable_lanes import ReversibleLane,LaneWindow
import json

def example_relation(value,**tags):
 return {'id':'synthetic:123','tags':{'type':'restriction','restriction':value,**tags},'members':[
   {'type':'way','role':'from','ref':10},{'type':'node','role':'via','ref':20},
   {'type':'way','role':'to','ref':30}]}

def run():
 instant=datetime.fromisoformat('2026-11-02T08:30:00+09:00')
 rels=ingest([example_relation('no_left_turn'),example_relation('only_right_turn'),
              {'id':'unsupported-via-way','tags':{'type':'restriction','restriction':'no_left_turn'},'members':[
                 {'type':'way','role':'from','ref':10},{'type':'way','role':'via','ref':20},{'type':'way','role':'to','ref':30}]}])
 road1=WayGeometry('a',((0,0),(10,10)))
 road2=WayGeometry('b',((0,10),(10,0)))
 elevated=WayGeometry('a',road1.points,layer=1,kind='bridge')
 ground=WayGeometry('b',road2.points,layer=0,kind='road')
 pocket=TurnPocket('A','A_left',19.5,frozenset({'left'}),'synthetic:layout')
 reverse=ReversibleLane('center',(
     LaneWindow('forward',Window(7*60,9*60), 'synthetic:forward'),
     LaneWindow('closed',Window(9*60,10*60),'synthetic:closure'),
     LaneWindow('reverse',Window(10*60,12*60),'synthetic:reverse')
 ),'Asia/Seoul')
 return {'data_kind':'entirely synthetic structural witness; no actual road permission',
         'osm_relations':{'accepted':len(rels.relations),'unresolved':list(rels.unresolved),
             'target_prohibition':evaluate((rels.relations[0],),10,20,30,'passenger','left',instant,'Asia/Seoul'),
             'only_turn_non_target':evaluate((rels.relations[1],),10,20,31,'passenger','straight',instant,'Asia/Seoul')},
         'geometry':{'ungraded':audit_crossing(road1,road2),'bridge_crossing':audit_crossing(elevated,ground)},
         'turn_pocket':{'length_m':pocket.length_m,'upper_vehicle_count_6p5m':pocket.capacity_upper_bound(6.5)},
         'reversible_lane':{x:reverse.state_at(datetime.fromisoformat('2026-11-02T'+x+':00+09:00'))
                            for x in ('08:30','09:30','10:30','14:00')},
         'policy_code_changed':False,'sumo_vehicle_executed':False,'field_truth_validated':False}
if __name__=='__main__':
 out=Path(__file__).resolve().parents[1]/'results';out.mkdir(parents=True,exist_ok=True)
 val=run();(out/'feature_matrix.json').write_text(json.dumps(val,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 print(json.dumps(val,indent=2,ensure_ascii=False))

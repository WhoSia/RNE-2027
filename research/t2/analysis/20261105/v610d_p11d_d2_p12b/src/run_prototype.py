"""Run exact, bounded four-track smoke experiments (no SUMO, no field calibration)."""
import csv,json
from pathlib import Path
from road_ir import import_cityflow,import_sumo_net
from controllers import Observation,PhaseController,PhaseGuard

CF={'roads':[{'id':'west','points':[{'x':0,'y':0},{'x':100,'y':0}],'lanes':[{'maxSpeed':12},{'maxSpeed':12}]},
             {'id':'east','points':[{'x':100,'y':0},{'x':150,'y':0}],'lanes':[{'maxSpeed':10}]}],
    'intersections':[{'id':'J','roadLinks':[{'startRoad':'west','endRoad':'east','type':'go_straight',
      'laneLinks':[{'startLaneIndex':0,'endLaneIndex':0},{'startLaneIndex':1,'endLaneIndex':0}]}]}]}
SUMO='''<net><edge id="west"><lane id="west_0" speed="12" length="100"/><lane id="west_1" speed="12" length="100"/></edge>
<edge id="east"><lane id="east_0" speed="10" length="50"/></edge>
<connection from="west" to="east" fromLane="0" toLane="0" dir="s" tl="J" linkIndex="0"/>
<connection from="west" to="east" fromLane="1" toLane="0" dir="s" tl="J" linkIndex="1"/></net>'''

def run(output:Path):
    output.mkdir(exist_ok=True,parents=True)
    network_results={
      'cityflow':import_cityflow(CF,provenance='synthetic CityFlow fixture').summary(),
      'sumo':import_sumo_net(SUMO,provenance='synthetic SUMO net fixture').summary(),
    }
    # Synthetic sensor event series deliberately does NOT claim vehicle discharge.
    obs=[Observation(float(t), 0 if t%11<5 else 5, 5 if t%17<8 else 0, 10, 10) for t in range(0,121)]
    rows=[]
    for policy in ('fixed','actuated','pressure'):
        c=PhaseController(policy,PhaseGuard(min_green_s=4,max_green_s=15,yellow_s=3,all_red_s=1))
        for o in obs:c.observe(o)
        switches=sum(s=='yellow' for t,a,s in c.log)
        rows.append({'policy':policy,'observations':len(obs),'observed_period_s':120,
                     'yellow_starts':switches,'all_red_starts':sum(s=='all_red' for _,_,s in c.log),
                     'stage_transitions':len(c.log)-1,'final_state':c.state,'final_active':c.active})
    with (output/'controller_traces.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    summary={'kind':'internal synthetic contract verification, NOT measured traffic',
             'road_imports':network_results,'controller_telemetry':rows,
             'critical_limit':'controllers not coupled to vehicle simulation; comparison is not travel-time performance',
             'sumo_executed':False,'real_world_prediction_validated':False}
    (output/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    return summary
if __name__=='__main__':print(json.dumps(run(Path(__file__).resolve().parents[1]/'results'),indent=2))

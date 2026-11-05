"""Frozen synthetic experiment generator. Do not tune any signal policy in this script."""
from pathlib import Path
import json,csv,math,sys,unittest,subprocess,hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.micro_network import Link,Network,Demand,Signal,Crossing
from src.experiments import run_pair,generate_od_demand,OD
from src.sumo_export import write_sumo_fixture

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results';OUT.mkdir(exist_ok=True)

link_net=[Link('U',30,8),Link('D',15,8)]
vehicles=[Demand(f'v{i:02}',i*.75,('U','D')) for i in range(22)]
queue_runs=[];traces={}
for block in (0,15,25):
    engine=Network(link_net,dt_s=.5)
    obs=engine.run(vehicles,110,{'U':block} if block else {})
    queue_runs.append({'outlet_closed_until_s':block,'created':len(vehicles),
        'admitted':len(obs.admitted_s),'completed':len(obs.completed_s),
        'max_external_queue_vehicles':max(q for _,q in obs.queues),
        'last_completion_s':max(obs.completed_s.values()),
        'downstream_closed_ticks':obs.blocked.get('downstream_closed',0),
        'no_receiving_space_ticks':obs.blocked.get('no_receiving_space',0)})
    traces[str(block)]={'queue':obs.queues,'occupancy_U':[(t,occ['U']) for t,occ in obs.occupancies],
                      'occupancy_D':[(t,occ['D']) for t,occ in obs.occupancies]}
with (OUT/'queue_comparison.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(queue_runs[0]));w.writeheader();w.writerows(queue_runs)

refinement=[]
for dt in (1.0,.5,.25,.125):
    net=Network(link_net,dt_s=dt)
    ob=net.run(vehicles,120,{'U':20})
    refinement.append({'dt_s':dt,'completed':len(ob.completed_s),
                       'last_completion_s':max(ob.completed_s.values()),
                       'max_external_queue':max(q for _,q in ob.queues)})
with (OUT/'dt_sweep.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(refinement[0]));w.writeheader();w.writerows(refinement)

baseline_replay=ROOT/'results/p10_replayed_stdout.json'
baseline_archived=ROOT/'baselines/P10_original/boundary_mechanism.json'
p10=json.loads(baseline_replay.read_text())
historical=json.loads(baseline_archived.read_text())
assert p10['runs']==historical['runs'] and p10['mechanism']==historical['mechanism']

sumo=write_sumo_fixture(ROOT/'independent_sumo_input')
results={'experiment_date':'2026-11-06','source':'synthetic micro-network + byte-verified original P10',
         'fixed_signal_no_optimization':True,'sensitivity':queue_runs,'dt_refinement':refinement,
         'p10_direct_replay':{'matched_8_historical_runs':True,'runs':p10['runs'],
           'source_corridor_sha256':hashlib.sha256((ROOT/'replay_P10/reference/T2_v69_P2/corridor.py').read_bytes()).hexdigest()},
         'sumo':sumo,'field_validation':'NOT PERFORMED',
         'physical_model_qualified':False,
         'warnings':['Discrete tick transfer holds at least one tick at a stop line','No calibrated reaction delay','Lateral gap checked at one snapshot, not continuous maneuver','Bus dwell is synthetic','CTM and microscopic outputs are different observational grains']}
(OUT/'results.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

plt.figure(figsize=(9,5))
for b in ('0','15','25'):
    t,q=zip(*traces[b]['queue']);plt.step(t,q,where='post',label=f'downstream restriction {b} s')
plt.xlabel('Simulation time (s)');plt.ylabel('External arrival queue (vehicles)')
plt.title('Finite-storage spillback reference — synthetic only')
plt.legend();plt.tight_layout();plt.savefig(OUT/'queue_comparison.png',dpi=160);plt.close()

plt.figure(figsize=(9,4.5))
plt.plot([x['dt_s'] for x in refinement],[x['last_completion_s'] for x in refinement],marker='o')
plt.xlabel('Time step (s)');plt.ylabel('Last completion time (s)')
plt.title('Time-step sensitivity: fixed synthetic demand');plt.tight_layout()
plt.savefig(OUT/'dt_refinement.png',dpi=160);plt.close()

svg='''<!doctype html><html lang="ko"><meta charset="utf-8"><title>T2 D26–D29</title><style>
body{background:#101827;color:#e4e9f2;font-family:system-ui,sans-serif;max-width:860px;margin:32px auto;padding:16px}h1{font-size:26px}
.panel{border:1px solid #37475e;border-radius:15px;padding:18px;margin:12px 0}input{width:100%}small{color:#9db0c8}
.cell{display:inline-flex;align-items:center;justify-content:center;height:85px;border:1px solid #64748b;border-radius:9px;margin:8px;min-width:120px}
button{background:#315b91;color:white;border:0;padding:9px;border-radius:8px;cursor:pointer}
</style><h1>T2 · 유한 저장공간, 외부 혼잡의 발생</h1>
<p>원본 봉인 연구와 별개의 합성 시뮬레이션입니다. 신호 정책 최적화 결과가 아닙니다.</p>
<div class="panel"><label>출구 차단 해제 시각: <b id="key">0초</b></label><input id="chooser" type="range" min="0" max="2" step="1" value="0">
<p id="summary"></p><div id="cells"></div><small>위 점유량은 선택 시각의 링크 내 차량 수이며 차량 등가량 CTM이 아닙니다.</small></div>
<div class="panel"><label>실험 시각: <b id="clock">0초</b></label><input id="time" type="range" min="0" max="110" value="0" step=".5">
<p id="numbers"></p></div>
<div class="panel"><h2>이번 구현의 검증 한계</h2><p>SUMO 입력 XML은 생성했지만 SUMO 실행환경이 없어 독립 비교는 아직 불가합니다. 교통기관 실측도 미보정입니다.</p></div>
<script>const data=__DATA__;const trials=__TRIALS__;const keys=['0','15','25'];
const choose=document.querySelector('#chooser'),time=document.querySelector('#time');
function draw(){let key=keys[+choose.value],rec=data[key],t=+time.value,idx=Math.min(rec.queue.length-1,Math.round(t*2));
document.querySelector('#key').textContent=key+'초';document.querySelector('#clock').textContent=t+'초';
let trial=trials[+choose.value];document.querySelector('#summary').textContent='최대 외부 대기 '+trial.max_external_queue_vehicles+'대 · 마지막 완료 '+trial.last_completion_s+'초';
document.querySelector('#cells').innerHTML='<div class="cell">상류 U<br>'+rec.occupancy_U[idx][1]+'대</div><div class="cell">하류 D<br>'+rec.occupancy_D[idx][1]+'대</div>';
document.querySelector('#numbers').textContent='외부 대기 '+rec.queue[idx][1]+'대';}
choose.oninput=draw;time.oninput=draw;draw();</script></html>'''
(OUT/'interactive_network.html').write_text(svg.replace('__DATA__',json.dumps(traces)).replace('__TRIALS__',json.dumps(queue_runs)),encoding='utf-8')
print(json.dumps({'queue_runs':queue_runs,'dt':refinement,'p10_8_runs_match':True,'sumo_installed':sumo['sumo_available']},indent=2))

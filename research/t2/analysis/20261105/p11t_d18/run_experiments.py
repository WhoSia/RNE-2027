import csv,json,hashlib,zipfile,sys
from dataclasses import replace
from pathlib import Path
from src.cell_link_model import Config, simulate
p=Path(__file__).parent; out=p/'results';out.mkdir(exist_ok=True)
cases={
 'finite_gate_closed_12s':Config(),
 'finite_gate_open':Config(downstream_closed_until_s=0),
 'no_jam_storage_counterfactual':Config(infinite_storage_baseline=True),
 'finite_dt_0p5':Config(dt_s=.5),
 'finite_dt_0p25':Config(dt_s=.25)
}
results={name:simulate(cfg) for name,cfg in cases.items()}
(out/'case_results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2,allow_nan=False).replace('Infinity','null'),encoding='utf8') if False else None
# Numeric infinite capacities are not encoded as strict JSON: store `None` in baseline capacity
results_clean=json.loads(json.dumps(results,default=lambda x:None))
for val in results_clean.values(): val['capacities_veh']=[None if x==float('inf') else x for x in val['capacities_veh']]
(out/'case_results.json').write_text(json.dumps(results_clean,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf8')
with (out/'one_second_trace.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.writer(f);w.writerow(['step_end_s','source_queue_veh','U_veh','P_veh','D_veh','cumulative_arrivals_veh','cumulative_departed_veh','enter_U_veh_per_step','U_to_P_veh_per_step','P_to_D_veh_per_step','D_exit_veh_per_step'])
 for r in results['finite_gate_closed_12s']['rows']:
  w.writerow([r['t_end_s'],r['source_queue_veh'],*r['cells_veh'],r['cumulative_arrivals_veh'],r['cumulative_departed_veh'],*r['flows_veh']])
with (out/'sensitivity.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.writer(f);w.writerow(['scenario','dt_s','arrival_veh_per_s','gate_s','storage_is_finite','first_source_queue_s','max_source_queue_veh','final_departed_veh','max_conservation_abs_error'])
 for n,r in results.items():
  c=r['config'];s=r['summary'];w.writerow([n,c['dt_s'],c['arrival_veh_per_s'],c['downstream_closed_until_s'],not c['infinite_storage_baseline'],s['first_source_blocked_end_s'],s['max_source_queue_veh'],s['final_departures_veh'],s['max_conservation_abs_error']])
print('SUMMARY')
for n,r in results.items():print(n,r['summary'])

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
x=[r['t_end_s'] for r in results['finite_gate_closed_12s']['rows']]
fig,ax=plt.subplots(figsize=(10,4.5))
for label,key in [('Source backlog','source_queue_veh')]:
 ax.plot(x,[r[key] for r in results['finite_gate_closed_12s']['rows']],label='Finite storage: source backlog')
ax.plot(x,[r['source_queue_veh'] for r in results['finite_gate_open']['rows']],label='Same finite storage: gate always open',linestyle='--')
ax.plot(x,[r['source_queue_veh'] for r in results['no_jam_storage_counterfactual']['rows']],label='Unbounded storage counterfactual',linestyle=':')
ax.axvline(12,linestyle='--',alpha=.5,label='Downstream reopens at 12 s')
ax.set(xlabel='Time (s)',ylabel='Unadmitted demand (vehicle-equivalents)',title='Backpressure witness: finite storage and downstream closure')
ax.legend(loc='upper left',fontsize=8);fig.tight_layout();fig.savefig(out/'backpressure_comparison.png',dpi=170);plt.close(fig)
fig,ax=plt.subplots(figsize=(10,4.5))
for i,label in enumerate(['U: upstream','P: pocket','D: downstream']):
 ax.plot(x,[r['cells_veh'][i] for r in results['finite_gate_closed_12s']['rows']],label=f'{label} (cap {[4,2,1][i]})')
ax.axvline(12,linestyle='--',alpha=.5)
ax.set(xlabel='Time (s)',ylabel='Cell occupancy (vehicle-equivalents)',title='Spatial occupancy propagates back through three finite cells')
ax.legend();fig.tight_layout();fig.savefig(out/'three_cell_occupancy.png',dpi=170);plt.close(fig)

# Standalone exploration: fixed recorded steps, no internet/cdn.
trace=[{'t':r['t_end_s'],'cells':[round(v,6) for v in r['cells_veh']],'src':round(r['source_queue_veh'],6),'out':round(r['cumulative_departed_veh'],6)} for r in results['finite_gate_closed_12s']['rows']]
html='''<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>T2 D18 · 유한 링크 역류 탐색기</title><style>body{font-family:system-ui,-apple-system,sans-serif;margin:0;background:#101722;color:#edf3fb}main{max-width:930px;margin:auto;padding:32px}h1{font-size:25px}p{color:#aebbd0;line-height:1.7}.top{display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap}.stage{background:#192433;border-radius:17px;padding:23px;margin-top:20px}.roads{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px}.link{padding:18px 12px;border-radius:13px;background:#293749;min-height:128px}.label{font-weight:700}.meter{height:12px;background:#0e1520;border-radius:99px;overflow:hidden;margin:23px 0 12px}.fill{height:100%;background:#53b5bd;transition:width .15s}.count{font-variant-numeric:tabular-nums;font-size:21px}input[type=range]{width:100%;accent-color:#62bfad}.stat{display:flex;justify-content:space-between;gap:12px;border-top:1px solid #344458;padding-top:14px;margin-top:14px}.value{font-weight:700;font-variant-numeric:tabular-nums}small{color:#aebbd0}@media(max-width:540px){.roads{grid-template-columns:1fr}.link{min-height:60px}}</style></head><body><main><h1>유한 차로 저장공간 — 역류의 진행</h1><p>독립 합성 CTM 실행 기록 24스텝을 움직여 보세요. 하류 출구는 12초까지 닫힙니다. 모든 수치는 연속적인 차량 등가량이며, 실제 차량 한 대의 위치가 아닙니다.</p><div class="stage"><div class="top"><strong>관측 시각 <span id="t"></span></strong><span>외생적 출구 상태: <b id="gate"></b></span></div><input id="seek" type="range" min="0" max="23" value="10" step="1" aria-label="시뮬레이션 시각"><div class="roads"><div class="link"><div class="label">U · 상류</div><div class="meter"><div class="fill" id="b0"></div></div><div class="count"><span id="n0"></span> / 4</div><small>길이 30m</small></div><div class="link"><div class="label">P · 포켓</div><div class="meter"><div class="fill" id="b1"></div></div><div class="count"><span id="n1"></span> / 2</div><small>길이 15m</small></div><div class="link"><div class="label">D · 하류</div><div class="meter"><div class="fill" id="b2"></div></div><div class="count"><span id="n2"></span> / 1</div><small>길이 7.5m</small></div></div><div class="stat"><span>아직 U에 들어오지 못한 수요</span><span class="value" id="src"></span></div><div class="stat"><span>누적 출구 통과량</span><span class="value" id="out"></span></div></div><p><small>이 모델은 시간격자 기반 Cell Transmission Model의 단순 3셀 구현입니다. 신호 최적화·실도로 예측·차량 궤적 재현이 아닙니다. 코드와 전체 검증자료는 같은 ZIP에 포함됩니다.</small></p></main><script>const DATA=__TRACE__;const el=id=>document.getElementById(id);function show(i){const v=DATA[i];el('t').textContent=v.t.toFixed(0)+'초';el('gate').textContent=v.t<=12?'폐쇄':'개방';el('src').textContent=v.src.toFixed(2)+'대 등가';el('out').textContent=v.out.toFixed(2)+'대 등가';const cap=[4,2,1];for(let k=0;k<3;k++){el('n'+k).textContent=v.cells[k].toFixed(2);el('b'+k).style.width=(v.cells[k]/cap[k]*100).toFixed(2)+'%'}}el('seek').addEventListener('input',e=>show(+e.target.value));show(10);</script></body></html>'''
(out/'interactive_backpressure.html').write_text(html.replace('__TRACE__',json.dumps(trace)),encoding='utf8')

"""Reproduce D19 paired-closure audit using only standard Python and Matplotlib."""
import csv
import json
from dataclasses import asdict, replace
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from src.cell_link_model import Config
from src.paired_backpressure import compare

out = Path(__file__).resolve().parent / 'results'
out.mkdir(exist_ok=True)
settings = {
    'default': Config(),
    'open_gate_high_demand': Config(downstream_closed_until_s=0, arrival_veh_per_s=1.5),
    'closed_gate_high_demand': Config(arrival_veh_per_s=1.5),
}
for dt in (1., .5, .25, .125, .0625):
    settings[f'closed_dt_{dt:g}'] = Config(dt_s=dt)

results = {}
for name, config in settings.items():
    summary, rows = compare(config)
    results[name] = {'config': asdict(config), 'summary': asdict(summary), 'rows': rows}
(out / 'paired_audit.json').write_text(json.dumps(results, indent=2, ensure_ascii=False, allow_nan=False), encoding='utf-8')
with (out / 'paired_audit_summary.csv').open('w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['scenario', 'dt_s', 'arrival_veh_per_s', 'closure_until_s', 'first_any_queue_s', 'first_excess_queue_s', 'max_excess_queue_vehicle_equiv', 'final_departure_deficit_vehicle_equiv', 'mass_balance_residual'])
    for name, item in results.items():
        c, s = item['config'], item['summary']
        w.writerow([name, c['dt_s'], c['arrival_veh_per_s'], c['downstream_closed_until_s'], s['first_any_source_queue_s'], s['first_excess_source_queue_s'], s['max_excess_source_queue_veh'], s['final_departure_deficit_veh'], s['max_flow_conservation_residual']])

fig, ax = plt.subplots(figsize=(10, 5))
for key, label in [('default', 'Closed gate: total source queue'), ('open_gate_high_demand', 'Open gate, oversaturated demand')]:
    rows = results[key]['rows']
    ax.plot([r['t_end_s'] for r in rows], [r['source_queue_closed_veh'] for r in rows], label=label)
rows = results['default']['rows']
ax.plot([r['t_end_s'] for r in rows], [r['excess_source_queue_veh'] for r in rows], linestyle='--', label='Closed-gate EXCESS relative to open')
ax.set(xlabel='End of step (s)', ylabel='Unadmitted vehicle equivalents', title='Queue presence is not necessarily downstream spillback')
ax.axvline(12, linestyle=':', alpha=.45)
ax.legend(fontsize=9)
fig.tight_layout()
fig.savefig(out / 'queue_vs_excess.png', dpi=180)
plt.close(fig)

series = [{'id': key, 'title': key, 'summary': val['summary'], 'rows': [
    {k: round(r[k], 8) if isinstance(r[k], (int, float)) else r[k] for k in ('t_end_s', 'source_queue_closed_veh', 'source_queue_open_veh', 'excess_source_queue_veh', 'departure_deficit_veh')}
    for r in val['rows']]} for key, val in results.items() if key in ('default', 'open_gate_high_demand', 'closed_gate_high_demand')]
script = json.dumps(series, ensure_ascii=False, allow_nan=False)
html = '''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>R&E 2027 D19 — 교통 대기열 인과 귀속</title><style>body{font:16px system-ui,sans-serif;background:#101a28;color:#f1f5fb;margin:0}main{max-width:950px;margin:auto;padding:30px 18px}h1{font-size:26px;line-height:1.3}p{color:#b9c8dc;line-height:1.6}.panel{background:#1d2d42;border:1px solid #35495e;border-radius:14px;padding:20px;margin-top:16px}.controls{display:flex;gap:15px;flex-wrap:wrap;align-items:center}select,input{padding:10px;border:1px solid #65809b;background:#102036;color:#f1f5fb;border-radius:8px}input{flex:1;min-width:220px}.metrics{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}.metric{background:#283b54;padding:13px;border-radius:9px}.metric strong{font-size:24px;display:block}.metric small{color:#b9c8dc}.bar{height:14px;background:#112136;border-radius:9px;overflow:hidden;margin-top:10px}.fill{height:100%;background:#67bba9;transition:width .18s}.split{display:grid;grid-template-columns:1fr 1fr;gap:12px}.callout{border-left:4px solid #d2aa5d;padding-left:12px}@media(max-width:600px){.metrics,.split{grid-template-columns:1fr}}</style></head><body><main><h1>대기열은 왜 생겼는가?</h1><p>공학 연구 D19 · 같은 CTM에서 하류 출구 폐쇄 조건만 바꿔 비교합니다. 이 그래프는 합성 차량 등가량이며 실제 도시의 대기시간·교통신호 최적화가 아닙니다.</p><div class="panel controls"><label>검증 조건 <select id="scenario"></select></label><input id="seek" type="range" min="0" step="1" value="10"><b id="clock"></b></div><div class="panel metrics"><div class="metric"><small>조건의 전체 유입 대기</small><strong id="total"></strong></div><div class="metric"><small>출구 개방 반사실의 유입 대기</small><strong id="open"></strong></div><div class="metric"><small>출구 폐쇄의 추가 유입 대기</small><strong id="extra"></strong></div></div><div class="panel"><h2>추가 대기 = 폐쇄 조건 대기 − 개방 조건 대기</h2><div class="bar"><div class="fill" id="share"></div></div><p id="status"></p><div class="split"><div>폐쇄에 따른 누적 유출 감소: <strong id="departure"></strong></div><div>모형 간 보존식 잔차: <strong id="mass"></strong></div></div></div><div class="panel callout"><strong>해석 한계</strong><p>대기열이 관측되었다는 것만으로 downstream spillback이라고 부를 수 없습니다. 수요가 포화 유량을 넘는 경우에는 출구가 항상 열려도 대기가 발생합니다. 모델상 추가 대기는 인과적 반사실 비교의 결과이지만, 현실 교통에 대한 인과 추정은 아닙니다.</p></div></main><script>const series=__DATA__;const pick=document.getElementById('scenario'),seek=document.getElementById('seek');for(const item of series){const opt=document.createElement('option');opt.value=item.id;opt.textContent=item.title;pick.append(opt)}function draw(){const s=series.find(v=>v.id===pick.value),r=s.rows[+seek.value];document.getElementById('clock').textContent=r.t_end_s+'s';const fmt=x=>x.toFixed(3)+' 대 등가';for(const [id,key] of [['total','source_queue_closed_veh'],['open','source_queue_open_veh'],['extra','excess_source_queue_veh'],['departure','departure_deficit_veh'],['mass','excess_source_queue_veh']]){document.getElementById(id).textContent=fmt(r[key])}document.getElementById('mass').textContent=s.summary.max_flow_conservation_residual.toExponential(2);document.getElementById('share').style.width=(r.source_queue_closed_veh>1e-10?Math.max(0,Math.min(100,100*r.excess_source_queue_veh/r.source_queue_closed_veh)):0)+'%';document.getElementById('status').textContent=r.excess_source_queue_veh>1e-9?'하류 폐쇄로 추가된 유입 대기가 양수입니다.':'이 시각에는 출구 폐쇄에 귀속되는 추가 유입 대기가 관측되지 않습니다.'}pick.addEventListener('change',()=>{seek.max=series.find(v=>v.id===pick.value).rows.length-1;seek.value=Math.min(+seek.value,+seek.max);draw()});seek.addEventListener('input',draw);pick.value='default';pick.dispatchEvent(new Event('change'));</script></body></html>'''
(out / 'interactive_causal_queue.html').write_text(html.replace('__DATA__', script), encoding='utf-8')
print(json.dumps({k: v['summary'] for k, v in results.items()}, ensure_ascii=False, indent=2))

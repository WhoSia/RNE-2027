"""Visualize auditable synthetic stress runs; only outputs, no new simulations."""
from pathlib import Path
import json,html
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
rows=json.loads((ROOT/'results/d33_stress.json').read_text())['cohorts']
p10=json.loads((ROOT/'results/d31_p10_bridge.json').read_text())

fig,ax=plt.subplots(figsize=(10,5.4))
for policy in ('fixed10','actuated'):
    group=sorted([r for r in rows if r['cohort']=='holdout' and r['policy']==policy],key=lambda r:int(r['demand_label'].split('_')[0][1:]))
    ax.plot([int(r['demand_label'].split('_')[0][1:]) for r in group], [r['mean_s'] for r in group],marker='o',label=policy)
ax.set(title='Synthetic HOLDOUT: arrival-duration by demand',xlabel='Vehicles per scenario',ylabel='Mean completed-trip duration (seconds)')
ax.legend();ax.grid(alpha=.25);fig.tight_layout()
fig.savefig(ROOT/'results/d33_holdout.png',dpi=170);plt.close(fig)

fig,ax=plt.subplots(figsize=(9,4.7))
ax.plot([r['dt_s'] for r in p10],[r['vehicle_8_entry_s'] for r in p10],marker='o',label='Vehicle 8 entry')
ax.plot([r['dt_s'] for r in p10],[r['phase_boundary_s'] for r in p10],linestyle='--',label='Last feasible entry')
ax.set(title='P10 ORIGINAL, source-replayed: grid/phase discontinuity',xlabel='Discrete timestep (seconds)',ylabel='Time (seconds)')
ax.legend();ax.grid(alpha=.25);fig.tight_layout()
fig.savefig(ROOT/'results/d31_p10_boundary.png',dpi=170);plt.close(fig)

serialized=json.dumps({'summaries':rows,'p10':p10},ensure_ascii=False).replace('</','<\\/')
page='''<!DOCTYPE html><html lang="ko"><meta charset="utf-8"><title>T2 D31-D33 · Research evidence viewer</title>
<style>body{font:15px system-ui, sans-serif;background:#101a26;color:#edf2fa;max-width:880px;margin:auto;padding:34px}h1{font-size:26px}select{padding:9px;background:#213247;color:white;border:1px solid #64738e;border-radius:8px}section{background:#172638;border:1px solid #405169;padding:20px;border-radius:14px;margin:16px 0}table{border-collapse:collapse;width:100%}td,th{padding:11px;border-bottom:1px solid #465369;text-align:left}small{color:#bac8d8}.warning{color:#ffcf8f}strong{color:#a6e6ca}</style>
<h1>T2 — 시공간 사건 감사 · 감응형 정책 비교</h1>
<p>2026-11-06. 모든 결과는 합성 시뮬레이션입니다. 실제 SUMO 실행 및 현장 검증은 아직 완료되지 않았습니다.</p>
<section><label>수요 수준 <select id="demand"><option value="n18_h3">18대 · 간격 3초</option><option selected value="n28_h2">28대 · 간격 2초</option><option value="n40_h1">40대 · 간격 1초</option></select></label>
<label> 평가 집합 <select id="cohort"><option value="train">개발</option><option value="holdout" selected>홀드아웃</option></select></label><table><thead><tr><th>정책</th><th>통행시간(초)</th><th>A/C 차이(초)</th><th>미완주 조건</th></tr></thead><tbody id="table"></tbody></table><small>통행시간은 해당 집합의 모든 차량이 도착한 경우에만 확정. 신호 시간은 실제 추천값이 아닙니다.</small></section>
<section><h2>P10 원본 사건 감사</h2><table><thead><tr><th>Δt</th><th>차량 8 진입</th><th>공간 소급(초)</th></tr></thead><tbody id="p10"></tbody></table></section>
<section><h2>검증 게이트</h2><p><strong>완료:</strong> P10 원본 반례 재현, 신규 합성 테스트, 요구시점 차량 점유 프록시를 사용하는 제한적 감응형 비교.</p><p class="warning"><b>미완료:</b> 원본 T2 미시 엔진과 운동 상태 통합, dt 수렴, SUMO 독립 차량 실행, GTFS 실측 보정, 실제 감응 신호 검증.</p></section>
<script>const DATA=__DATA__;const root=document.querySelector('#table');function draw(){const rows=DATA.summaries.filter(r=>r.cohort===document.querySelector('#cohort').value&&r.demand_label===document.querySelector('#demand').value);root.innerHTML=rows.map(r=>`<tr><td>${r.policy}</td><td>${r.mean_s===null?'검열 / 미완주':r.mean_s.toFixed(2)}</td><td>${r.approach_gap_s===null?'미확정':r.approach_gap_s.toFixed(2)}</td><td>${r.censored_scenarios}/${r.seeds}</td></tr>`).join('')}document.querySelectorAll('select').forEach(e=>e.addEventListener('change',draw));draw();document.querySelector('#p10').innerHTML=DATA.p10.map(r=>`<tr><td>${r.dt_s}</td><td>${r.vehicle_8_entry_s}</td><td>${r.retroactive_seconds.toFixed(3)}</td></tr>`).join('');</script></html>'''.replace('__DATA__',serialized)
(ROOT/'results/dashboard.html').write_text(page,encoding='utf-8')

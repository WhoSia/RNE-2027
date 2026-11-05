"""Reproduce tables and offline visualizations. No real SUMO or field data asserted."""
from __future__ import annotations
import sys,csv,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'src'))
from od_and_policy import court
from micro_world import Road,Vehicle,FixedSignal,run
ROOT=Path(__file__).parent; OUT=ROOT/'results';OUT.mkdir(exist_ok=True)
policy=court(); (OUT/'policy_court.json').write_text(json.dumps(policy,indent=2,ensure_ascii=False)+'\n')
with (OUT/'policy_court.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['green_s','cohort','status','mean_duration_s','mean_source_queue','approach_disparity_s'])
    w.writeheader();w.writerows(policy['train']+policy['holdout'])

source=ROOT/'d26_p10'
historical=json.loads((source/'boundary_mechanism.json').read_text())
ablation=json.loads((source/'ablation_stdout.json').read_text())
replay={'original_sha256':{'P10_zip':'9fa06146b781bcbbd1f5e19dc25b277e1e98c695b13e61fc0b291b58cd53b59c','P9_zip':'3f5dbf4d81756208e1a5c46e4906a32b95fe50ac0a61e4f142ba39097c2139bd','P2_corridor':'12987786fb36409a272a50233c12c006d0a23d5f75a5487be68d51392c4614cc'},'case':historical['source_case'],'mechanism':historical['mechanism'],'grid':historical['runs'],'ablation':ablation,'archive_replay_byte_matches':{}}
from zipfile import ZipFile
with ZipFile(ROOT/'sources'/'P10_20261104_original.zip') as z:
    for name in ['boundary_trace.csv','boundary_mechanism.json','capacity_gate_ablation.csv']:
        replay['archive_replay_byte_matches'][name]=(z.read(name)==(source/name).read_bytes())
(OUT/'p10_replay.json').write_text(json.dumps(replay,indent=2)+'\n')

# Geometry and dynamic-road snapshots for a small reproducible cohort.
roads={'A':Road('A',22,1,9,('S',)),'C':Road('C',22,1,9,('S',)),'S':Road('S',24,1,9)}
vs=[Vehicle('a'+str(i),('A','S'),i*2,desired_mps=8,accel_mps2=2) for i in range(6)]
vs +=[Vehicle('c'+str(i),('C','S'),i*3+1,desired_mps=8,accel_mps2=2) for i in range(6)]
sig={'A':FixedSignal(24,10,0),'C':FixedSignal(24,12,12)}
z=run(roads,vs,horizon_s=100,signals=sig)
snapshots={'input':{'roads':{k:vars(v) for k,v in roads.items()},'vehicles':[vars(v) for v in vs]},'summary':{'admitted':len(z.admissions),'finished':len(z.finishes),'unadmitted':len(vs)-len(z.admissions),'collision_violations':z.collision_violations},'states':z.states,'events':z.events}
(OUT/'micro_snapshots.json').write_text(json.dumps(snapshots,ensure_ascii=False)+'\n')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(7.2,4.2))
train=policy['train'];hold=policy['holdout'];xs=[x['green_s'] for x in train]
ax.plot(xs,[x['mean_duration_s'] for x in train],'-o',label='Development (4 seeds)')
ax.plot(xs,[x['mean_duration_s'] for x in hold],'-s',label='Held-out (2 seeds)')
ax.set(xlabel='Approach A green time [s]',ylabel='Mean trip time [s]',title='Two-approach synthetic fixed-signal court')
ax.legend();ax.grid(alpha=.25);fig.tight_layout();fig.savefig(OUT/'policy_holdout.png',dpi=155);plt.close(fig)
fig,ax=plt.subplots(figsize=(7.2,3.8))
for row in replay['grid']:
    ax.scatter(row['dt_s'],row['vehicle_8_enters_j0_at_s'],s=70)
ax.axhline(47.1625,ls='--',lw=1,label='Last admissible side entry, 47.1625s')
ax.set(xlabel='Time grid dt [s]',ylabel='Vehicle 8 admission [s]',title='Historical P10: re-executed grid discontinuity')
ax.legend();ax.grid(alpha=.25);fig.tight_layout();fig.savefig(OUT/'p10_replay.png',dpi=155);plt.close(fig)

payload=json.dumps({'policy':policy['train']+policy['holdout'],'states':z.states,'events':z.events},separators=(',',':'))
html='''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>T2 D26–30 · 검증 현황과 차량 사건 탐색</title>
<style>body{font-family:system-ui,sans-serif;background:#0d1824;color:#e7f0f8;margin:0 auto;padding:28px;max-width:1040px}h1{font-size:25px}h2{font-size:19px;margin-top:28px}.muted{color:#a9bbca}.panel{background:#182c3c;border:1px solid #345367;border-radius:12px;padding:18px;margin:14px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:10px}.stat{background:#284356;padding:15px;border-radius:10px}input{width:100%}svg{max-width:100%;height:auto}.row{display:flex;align-items:center;justify-content:space-between;gap:8px}table{border-collapse:collapse;width:100%}td,th{padding:9px;text-align:left;border-bottom:1px solid #39556b}code{color:#e4d399}</style>
<h1>T2 · P11-AB / D26–D30</h1><p class="muted">연구용 합성 시뮬레이터. 실측 및 SUMO 검증 전, 현장 신호운영에 사용 금지.</p>
<div class="grid"><div class="stat"><b>원본 P10 재실행</b><p>8/8 테스트 · 기록과 바이트 일치</p></div><div class="stat"><b>신규 미시 엔진</b><p>위치·속도·차로·보행·버스·수요</p></div><div class="stat"><b>외부 실측</b><p>실제 SUMO / 현장: 미실행</p></div></div>
<div class="panel"><h2>합성 차량의 시간별 링크 점유</h2><div class="row"><span>시각 <strong id="tick">0</strong>초</span><span class="muted">차량 위치는 단순화된 후방 좌표</span></div><input type="range" min="0" max="100" value="0" id="time"><svg id="road" viewBox="0 0 960 245" aria-label="도로 A, C, S에서 차량의 진행 위치"></svg></div>
<div class="panel"><h2>신호정책 후보 비교</h2><table id="pol"><thead><tr><th>A 녹색(초)</th><th>집합</th><th>완주 여부</th><th>평균 통행시간(초)</th><th>접근로 격차(초)</th></tr></thead><tbody></tbody></table></div>
<div class="panel"><h2>해석 제한</h2><p>시간격자 1초 고정. 실제 차로변경 궤적, 차량추종 보정, 정교한 보행자 행동, 회전교차로 양보, SUMO 독립 검증, 국내 실측은 완료되지 않았습니다. P10 원본의 단일 사건 역행 반례만 원본 코드로 재현했습니다.</p></div>
<script>const D=__DATA__;let tick=document.querySelector('#time'),out=document.querySelector('#road');const names=['A','C','S'];const ys=[38,117,196];function draw(){let t=+tick.value;document.querySelector('#tick').textContent=t;let state=D.states[t]||{};let svg='';for(let i=0;i<3;i++){let name=names[i],y=ys[i];svg+=`<text x="12" y="${y+16}" fill="#dfeaf2" font-size="16">${name}</text><rect x="90" y="${y}" width="800" height="44" rx="6" fill="#2b465c" stroke="#6489a8"/>`;for(const [id,x] of Object.entries(state)){if(x[0]!==name)continue;let len=name==='S'?24:22;let px=92+x[2]/len*720;svg+=`<rect x="${px}" y="${y+8}" width="56" height="26" rx="5" fill="${id.startsWith('a')?'#e2ad59':'#67b7c4'}"/><text x="${px+28}" y="${y+25}" text-anchor="middle" fill="#10202b" font-size="12">${id}</text>`}}}out.innerHTML=svg}tick.addEventListener('input',draw);draw();const tbody=document.querySelector('#pol tbody');for(let x of D.policy){let tr=document.createElement('tr');for(const k of ['green_s','cohort','status','mean_duration_s','approach_disparity_s']){let td=document.createElement('td');td.textContent=typeof x[k]==='number'?x[k].toFixed(2):String(x[k]);tr.append(td)}tbody.append(tr)}</script></html>'''.replace('__DATA__',payload)
(OUT/'interactive_dashboard.html').write_text(html,encoding='utf-8')
print(json.dumps({'p10_replayed_dt':len(replay['grid']),'p10_archive_matches':replay['archive_replay_byte_matches'],'policy_train':train,'policy_holdout':hold,'micro_snapshots':len(z.states),'micro_finished':len(z.finishes)},indent=2))

"""Generate reproducible offline diagnostic artifacts (no image scraping)."""
import json
from pathlib import Path
import matplotlib.pyplot as plt
ROOT=Path(__file__).parent
OUT=ROOT/'results'
data=json.loads((OUT/'D24_results.json').read_text())
fig,axs=plt.subplots(2,1,figsize=(10,6),sharex=True,layout='constrained')
for i,(cap,result) in enumerate(data['scene'].items()):
    ax=axs[i]
    starts=result['starts']; finishes=result['finishes']
    labels=['ped_B','vehicle','follower']
    for y,name in enumerate(labels):
        ax.barh(y,finishes[name]-starts[name],left=starts[name],height=.55,alpha=.8)
        ax.text(starts[name]+.05,y,name,va='center',fontsize=9)
    ax.set_yticks(range(len(labels)),labels)
    ax.set_title('Zone A capacity = '+cap+', zone B capacity = 1')
    ax.set_xlim(0,6)
    ax.grid(axis='x',alpha=.25)
axs[-1].set_xlabel('Abstract time ticks (not calibrated seconds)')
fig.suptitle('Integrated phase-zone occupancy and finite slot sensitivity')
fig.savefig(OUT/'finite_zone_timeline.png',dpi=145)
plt.close(fig)

# No remote scripts/fonts; keep functional offline slider over event snapshots.
recs=data['scene']
app='''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>D24 시간별 공간 점유</title>
<style>body{font:15px system-ui,sans-serif;max-width:850px;margin:35px auto;padding:0 18px;background:#111827;color:#e5e7eb}.pane{background:#1f2937;padding:18px;border-radius:12px;margin:12px 0}input{width:100%}.zone{display:flex;gap:8px;margin:10px 0}.cell{flex:1;padding:18px;text-align:center;background:#374151;border-radius:8px}.filled{background:#275f75}.small{color:#9ca3af;font-size:13px}h1{font-size:24px}#notes{white-space:pre-wrap}</style>
<h1>T2 D24 · 순차 점유·유한 저장공간</h1><p class="small">합성 사건모형. 시간 단위는 추상 정수 틱이며 실제 도로·신호·안전 결과가 아닙니다.</p>
<div class="pane"><label>시각 <strong id="time">0</strong> 틱<input id="seek" type="range" min="0" max="6" step="1" value="0"></label></div><div id="cases"></div>
<script>const scenarios=DATA_JSON;
function render(){const t=Number(document.querySelector('#seek').value);document.querySelector('#time').textContent=t;
const html=[];for(const [cap,rec] of Object.entries(scenarios)){const occ={A:[],B:[]};for(const [at,action,id,zones] of rec.log){if(at>t)break;if(action==='transition'){for(const k of Object.keys(occ))occ[k]=occ[k].filter(x=>x!==id);for(const z of zones)occ[z].push(id)}else if(action==='exit'){for(const k of Object.keys(occ))occ[k]=occ[k].filter(x=>x!==id)}}
const after=['ped_B','vehicle','follower'].filter(id=>!(id in rec.starts) || rec.starts[id]>t);
html.push('<div class="pane"><h2>Zone A capacity '+cap+' / Zone B capacity 1</h2><div class="zone">'+Object.entries(occ).map(([z,ids])=>'<div class="cell '+(ids.length?'filled':'')+'">'+z+'<p>'+ (ids.join(', ')||'empty')+'</p></div>').join('')+'</div><p class="small">아직 진입하지 않은 요청: '+(after.join(', ')||'없음')+'</p></div>');}
document.querySelector('#cases').innerHTML=html.join('')}
document.querySelector('#seek').addEventListener('input',render);render()</script></html>'''
(OUT/'interactive_zone_capacity.html').write_text(app.replace('DATA_JSON',json.dumps(recs,ensure_ascii=False)),encoding='utf-8')
print('visualization files written')

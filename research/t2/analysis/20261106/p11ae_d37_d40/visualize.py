"""Static and interactive descriptive plots; does not display real-time signals."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
ROOT=Path(__file__).resolve().parent
r=json.loads((ROOT/'data/cats_16_derived.json').read_text())['records']
groups={'Stopping segments':r[:8],'Through-movement segments':r[8:]}
fig,ax=plt.subplots(figsize=(11,5.8),layout='constrained')
for i,(name,items) in enumerate(groups.items()):
 xs=[i*9+j for j in range(8)]
 ax.bar(xs,[x['frames_below_0p5_mps']/x['frames'] for x in items],alpha=.83,label=name)
ax.axhline(0.5,ls=':',color='gray',lw=1)
ax.set_xticks([*range(8),*range(9,17)])
ax.set_xticklabels([x['filename'].split('-')[-1].replace('.csv','') for x in r[:8]] + [x['filename'].split('-')[-1].replace('.csv','') for x in r[8:]])
ax.set_ylabel('Fraction of 0.1 s frames with AV speed < 0.5 m/s')
ax.set_xlabel('Public source segment identifier (two label-selected groups)')
ax.yaxis.set_major_formatter(PercentFormatter(1))
ax.set_ylim(0,1.07)
ax.legend(loc='upper right')
ax.set_title('Observed AV stop fractions: sixteen source-verified Waymo-derived signal encounters')
fig.savefig(ROOT/'results/cats_16_real_observed_stop_fraction.png',dpi=175)
plt.close(fig)

def esc(s):
 return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
data=json.dumps(r,ensure_ascii=False)
html='''<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>T2 D37 / actual traffic-signal encounters</title><style>
:root{color-scheme:dark}body{font:15px system-ui;max-width:1060px;margin:25px auto;padding:18px;background:#101722;color:#eef3f9}h1{font-size:27px}.sub{color:#a9b8cb}select{background:#223149;color:white;padding:9px;border-radius:7px}.note{border:1px solid #57697c;padding:12px;border-radius:9px;margin-top:16px}#chart{width:100%;height:360px;background:#172434;border-radius:12px}.line{stroke:#56697b;stroke-width:1}a{color:#91caf9}.axis{fill:#bccddd;font-size:12px}</style></head>
<body><h1>T2 D37: 실제 신호등 접근 궤적 16개</h1><p class="sub">원본 GitHub CSV 16개를 직접 읽어 얻은 파생 통계입니다. 각 구간 91프레임 × 0.1초. 원본 자체는 이 HTML에 포함하지 않습니다.</p><p>구분: <select id="group"><option value="all">전체 16구간</option><option value="stop">정지 구간 8개</option><option value="go">직진 통과 구간 8개</option></select></p><svg id="chart" viewBox="0 0 1000 360"></svg><div id="detail" class="note"></div><p class="sub">높이 = 차량 속도 0.5m/s 미만인 관측 프레임의 비율. 정지 vs 통과는 원본에서 이미 선별된 라벨입니다. 표본 대표성, 신호정책의 인과 효과, 교차로 대기열 길이를 뜻하지 않습니다.</p><script>
const records=DATA;const svg=document.getElementById('chart'), detail=document.getElementById('detail');const NS='http://www.w3.org/2000/svg';function el(t,p={},str=''){const v=document.createElementNS(NS,t);for(let k in p)v.setAttribute(k,p[k]);v.textContent=str;return v;}function render(){const g=document.getElementById('group').value;let xs=records.filter((x,i)=>g==='all'||(g==='stop'?i<8:i>=8));svg.replaceChildren();const base=300, max=245,dx=940/xs.length;for(let pct=0;pct<=1;pct+=.25){let y=base-max*pct;svg.appendChild(el('line',{x1:45,y1:y,x2:990,y2:y,stroke:'#3f5369'}));svg.appendChild(el('text',{x:5,y:y+4,class:'axis'},Math.round(pct*100)+'%'));}xs.forEach((x,i)=>{let v=x.frames_below_0p5_mps/x.frames,b=el('rect',{x:55+dx*i,y:base-v*max,width:Math.max(9,dx*.7),height:v*max,rx:3,fill:x.category.startsWith('stops')?'#5f9ad9':'#e9ab59'});b.style.cursor='pointer';b.onclick=()=>show(x);svg.appendChild(b);svg.appendChild(el('text',{x:55+dx*i+dx*.35,y:325,'text-anchor':'middle',class:'axis'},x.filename.split('-').at(-1).replace('.csv','')));});if(xs.length)show(xs[0]);}function show(x){detail.innerHTML=`<b>${esc(x.filename)}</b><p>원본 Git blob: <code>${esc(x.github_blob_sha1)}</code></p><p>평균 속도 ${x.mean_speed_mps.toFixed(3)} m/s | 정지 ${x.frames_below_0p5_mps}/${x.frames}프레임 | 빨간 신호 코드 프레임 ${x.red_or_red_arrow_frames} | 녹색 ${x.green_or_green_arrow_frames}</p><a href="${esc(x.url)}">GitHub에서 원본 보기</a>`;}document.getElementById('group').addEventListener('change',render);render();</script></body></html>'''.replace('DATA',data)
(ROOT/'results/interactive_real_episodes.html').write_text(html)

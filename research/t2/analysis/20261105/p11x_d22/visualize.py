import json
from pathlib import Path
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
r=json.loads((ROOT/'results'/'paired_partial_overlap.json').read_text(encoding='utf-8'))
fig,ax=plt.subplots(figsize=(9,4))
ids=['car_A','ped_B','car_C']
for idx,(name,record) in enumerate(r['cases'].items()):
    for i,ident in enumerate(ids):
        start=record['entries'][ident]
        stop=record['exits'][ident]
        ax.broken_barh([(start,stop-start)],(idx*4+i,.7),label=ident if idx==0 else None)
ax.set_yticks([0.35,1.35,2.35,4.35,5.35,6.35], ['W / car_A','W / ped_B','W / car_C','X / car_A','X / ped_B','X / car_C'])
ax.set_xlim(0,7.5);ax.set_xlabel('Synthetic event time (seconds)')
ax.set_title('Multi-zone overlap: equality vs set intersection')
ax.grid(axis='x',alpha=.3);fig.tight_layout()
fig.savefig(ROOT/'results'/'multi_zone_timeline.png',dpi=170);plt.close(fig)
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>R&E 2027 · P11-X overlap witness</title><style>body{font:16px system-ui;margin:20px auto;max-width:800px;color:#172437;padding:0 18px}h1{font-size:1.4rem}.wrap{display:grid;grid-template-columns:110px 1fr;gap:12px;align-items:center;margin:12px 0}.track{position:relative;background:#e8edf4;height:30px;border-radius:5px}.bar{position:absolute;height:24px;top:3px;border-radius:4px;background:#517ba6}.waiting{background:#b77848}.grid{display:grid;gap:24px;grid-template-columns:1fr 1fr}section{padding:16px;border:1px solid #dae2eb;border-radius:12px}input{width:100%}.legend{font-size:.85rem;color:#546477}</style><h1>P11-X: Shared conflict zone</h1><p>Same synthetic requests. W compares whole zone labels; X intersects zone sets. Entry is allowed only when the required zone has no conflicting movement.</p><label for="clock">Event time: <output id="stamp">0.0</output> s</label><input id="clock" type="range" min="0" max="7" step="0.1" value="0" oninput="draw()"><div class="grid"><section><strong>W · equality bug</strong><div id="w"></div></section><section><strong>X · intersect zones</strong><div id="x"></div></section></div><p class="legend">Blue = occupying. Orange = pending. White = not yet arrived/finished. All activity times are synthetic.</p><p class="legend">Limit: every declared conflict zone is held for the entire synthetic movement duration. This is not a validated physical trajectory simulation or signal policy.</p><script>
const data='''+json.dumps(r['cases'],ensure_ascii=False)+''';const names=['car_A','ped_B','car_C'];function draw(){let t=+document.querySelector('#clock').value;document.querySelector('#stamp').textContent=t.toFixed(1);for(const [key,id] of [['W_existing','w'],['X_multi_zone','x']]){let s='';names.forEach((name,i)=>{let entry=data[key].entries[name],exit=data[key].exits[name],request=name==='car_A'?0:1;let status=t<request?'not arrived':t<entry?'waiting':t<exit?'occupying':'finished';s+='<div class="wrap"><span>'+name+'</span><div class="track" style="display:grid;place-items:center;background:'+(status==='waiting'?'#f2d7c1':status==='occupying'?'#c0d5e7':'#e8edf4')+'">'+status+'</div></div>'});document.querySelector('#'+id).innerHTML=s}}draw();</script></html>'''
(ROOT/'results'/'interactive_multi_zone.html').write_text(html,encoding='utf-8')

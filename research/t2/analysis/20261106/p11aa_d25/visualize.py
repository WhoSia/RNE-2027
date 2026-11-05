"""Plain research figure; no live external sources."""
import csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).parent/'results'
rows=list(csv.DictReader((P/'length_gap_sweep.csv').open(encoding='utf-8')))
fig,ax=plt.subplots(figsize=(8.0,4.8))
for gap in (1000,2000,3000):
    a=[r for r in rows if int(r['gap_mm'])==gap]
    ax.step([int(r['zone_length_mm'])/1000 for r in a],
            [int(r['second_entry_tick']) for r in a],where='post',label=f'Gap {gap/1000:g} m')
ax.set(title='Synthetic link packing: when can the following car enter?',xlabel='Zone length (m)',ylabel='Following car entry (integer tick)')
ax.set_ylim(.1,4.8)
ax.grid(alpha=.25)
ax.legend()
fig.tight_layout()
fig.savefig(P/'length_gap_sweep.png',dpi=170)
plt.close(fig)
# Self-contained HTML canvas-free with table and slider for local inspection.
import json
serialized=json.dumps(rows)
html='''<!DOCTYPE html><html lang="en"><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>D25 synthetic packing audit</title>
<style>body{font:16px system-ui;margin:5vh auto;max-width:780px;padding:0 16px;background:#f8fafc;color:#1b293a}main{background:white;border:1px solid #d7e0ea;border-radius:16px;padding:26px}input{width:100%}.result{font-size:26px;font-weight:650;margin:18px 0}small{color:#556879}.track{height:58px;background:#e5eaf0;border:1px solid #aabaca;display:flex;align-items:center;padding:3px;gap:2px;border-radius:8px}.vehicle{height:37px;border-radius:5px;display:grid;place-items:center;color:white;font-size:12px;background:#4d77b1;flex-shrink:0}.bus{background:#af874a}.gap{height:1px;background:#8d9bad;flex-shrink:0}</style><main><h2>D25 — Fixed geometry, synthetic vehicles</h2><p>One 11 m bus arrives at tick 0; one 4.5 m car requests entry at tick 1. Both occupy the zone for four ticks. The bus leaves at tick 4.</p><label>Zone length <strong id="length"></strong><input id="len" type="range" min="12" max="20" step="0.5" value="15"></label><label>Requested separation <strong id="gapv"></strong><input id="gap" type="range" min="1" max="3" step="0.5" value="2"></label><div class="result" id="result"></div><div class="track" id="track"></div><p><small>Length-budget model only: does not simulate acceleration, reaction time, pedestrian behavior, geometry of turn pockets, or actual traffic.</small></p></main><script>
const len=document.querySelector('#len'),gap=document.querySelector('#gap');function update(){const L=+len.value,g=+gap.value,required=11+g+4.5;document.querySelector('#length').textContent=L+' m';document.querySelector('#gapv').textContent=g+' m';document.querySelector('#result').textContent=`Car enters at tick ${L>=required?1:4} (two-vehicle required length: ${required} m)`;document.querySelector('#track').innerHTML=`<div class="vehicle bus" style="width:${11/L*100}%">bus 11 m</div>${L>=required?`<div class="gap" style="width:${g/L*100}%"></div><div class="vehicle" style="width:${4.5/L*100}%">car</div>`:''}`;}len.oninput=gap.oninput=update;update();</script></html>'''
(P/'interactive_storage.html').write_text(html,encoding='utf-8')

"""Create stand-alone explanatory figure and offline timeline."""
import csv,html,json
from pathlib import Path
root=Path(__file__).resolve().parent
r=list(csv.DictReader((root/'results/spatial_conflict_witness.csv').open()))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(9,3.6))
labels=['Legacy global','Separate intersections','Same intersection']
for i,x in enumerate(r):
    v=float(x['ped_wait_s'])
    ax.barh(i,v,color=['#b45450','#2d9784','#b45450'][i],height=.55)
    ax.text(v+.08,i,f'{v:g} s',va='center')
ax.set_yticks(range(3),labels);ax.invert_yaxis();ax.set_xlim(0,5.5)
ax.set_xlabel('Synthetic pedestrian request wait (s)')
ax.set_title('Conflict graph scope: global vs intersection-local')
ax.grid(axis='x',alpha=.15);fig.tight_layout()
fig.savefig(root/'results/spatial_conflict_witness.png',dpi=160);plt.close(fig)
rows=''.join(f'<tr><td>{html.escape(x["case"])}</td><td>{x["ped_request_s"]}</td><td>{x["ped_entry_s"]}</td><td>{x["ped_wait_s"]}</td></tr>' for x in r)
page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>T2 — Scoped conflict witness</title><style>body{font:16px system-ui;background:#111923;color:#e5edf5;padding:2rem;max-width:900px;margin:auto}table{width:100%;border-collapse:collapse}th,td{padding:.8rem;border-bottom:1px solid #46515c;text-align:left} .box{padding:1rem;border:1px solid #485867;border-radius:12px;margin:1rem 0} .track{height:24px;background:#34404a;position:relative;border-radius:4px;margin:.6rem 0}.bar{position:absolute;height:24px;background:#d9915c;border-radius:4px}p{line-height:1.6}small{color:#aac0d1}</style></head><body><h1>Spatial scope of conflict rules</h1><p>Synthetic independent zones. <b>No real-world safety or traffic performance claim.</b> Car A occupies zone A from 0–5 s. Pedestrian B requests zone B at 1 s. Same-kind collision rule is applied globally in the legacy case but only within a named zone in the patched case.</p><h2>Timelines (0–6 s)</h2><div class="box"><b>Legacy global: B waits 4 s</b><div class="track"><div class="bar" style="left:0;width:83.33%"></div></div><small>car A occupancy, 0–5 s; pedestrian B admitted 5 s</small></div><div class="box"><b>Explicit separate zones: B enters immediately</b><div class="track"><div class="bar" style="left:0;width:83.33%"></div><div class="bar" style="left:16.67%;width:16.67%;top:0;background:#55bca5"></div></div><small>car A 0–5 s; pedestrian B 1–2 s on another intersection</small></div><table><thead><tr><th>Configuration</th><th>Request</th><th>Entry</th><th>Wait (s)</th></tr></thead><tbody>'''+rows+'''</tbody></table><h2>Interpretation</h2><p>Scope bugs can create false network coupling. The default zone stays global for historical compatibility. Multi-zone movement paths and geometric conflict detection are not implemented. P12 signal optimization remains frozen.</p></body></html>'''
(root/'results/spatial_conflict_witness.html').write_text(page,encoding='utf8')

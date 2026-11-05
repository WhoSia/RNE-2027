from pathlib import Path
import json
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parent
r=json.loads((R/'results'/'audit_results.json').read_text())
fig,ax=plt.subplots(figsize=(9.5,4.5))
labels=['Uncontended lane: old','Uncontended lane: corrected','Blocked lane: corrected']
vals=[r['queue_metric']['old_max_waiting'],r['queue_metric']['new_max_waiting'],1]
bars=ax.barh(labels,vals)
for i,v in enumerate(vals):ax.text(v+.03,i,str(v),va='center')
ax.set_xlim(0,1.5);ax.set_xlabel('Max pending requests after event batch (count)')
ax.set_title('S → V queue metric audit: phantom waiting eliminated')
ax.grid(axis='x',alpha=.2)
fig.tight_layout()
fig.savefig(R/'results'/'queue_metric_audit.png',dpi=160)
plt.close(fig)
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>T2 D20 Code Audit</title>
<style>body{font:15px/1.55 system-ui,sans-serif;max-width:880px;margin:30px auto;padding:0 18px;background:#111923;color:#e9f0f7}h1{font-size:27px}p{color:#b6c5d6}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}.card{border:1px solid #46576b;border-radius:12px;padding:17px;background:#1b2937}button{cursor:pointer;border:1px solid #7699b7;padding:11px 14px;background:#283d50;color:white;border-radius:8px;margin:3px}button.active{background:#4a7193}.value{font-size:28px;font-weight:700}.error{color:#ef9999}.good{color:#81ddb5}code{background:#243747;padding:2px 4px;border-radius:4px}small{color:#acbac9}#output{white-space:pre-wrap}a{color:#bce1ff}</style>
<h1>T2 · P11-V / D20</h1><p>Independent audit of the sealed S-stage lane-event queue. Results are synthetic and are <b>not real-traffic measurements</b>. P12 remains frozen.</p>
<div><button id="a" onclick="show(0)">Clock rounding</button><button id="b" onclick="show(1)">Clock overflow</button><button id="c" onclick="show(2)">Phantom queue</button><button id="d" onclick="show(3)">Normal event</button></div>
<div class="grid"><div class="card"><small>Original S-stage</small><div class="value error" id="old"></div><div id="oldDesc"></div></div><div class="card"><small>Audited D20</small><div class="value good" id="new"></div><div id="newDesc"></div></div></div>
<section class="card" style="margin-top:12px"><b id="heading"></b><p id="explain"></p><div id="output"></div></section><small>Reproduce from ZIP: python -m unittest discover -s tests -v; python run_audit.py. Original sealed source SHA-256: be12e18f44d80a86b0360b14c8a80b511653fd4e1ae4f564305076dcad4626cc</small>
<script>const cases=[
{title:'Positive duration collapsed to zero',old:'0 s occupancy',new:'Rejected',od:'at=1e16 s; duration=0.25 s; old exit=entry.',nd:'Raises ValueError; use integer time ticks or rescale clock.',ex:'IEEE-754 binary64 spacing at 1e16 seconds exceeds 0.25 seconds. A synthetic resource can appear to release instantaneously despite a declared positive duration.'},
{title:'Nonfinite release timestamp',old:'Infinity',new:'Rejected',od:'at=1e308 s; duration=1e308 s.',nd:'Raises ValueError instead of putting infinite time into event log.',ex:'The original code checked input finiteness but not the result of timestamp addition.'},
{title:'Peak queue measurement semantics',old:'1 phantom waiter',new:'0 pending',od:'An immediately admitted vehicle was counted as waiting.',nd:'Pending requests measured after admissions at the event batch.',ex:'This corrects the definition of the reported metric. It does not improve car-following or field prediction.'},
{title:'Normal timestamp stays unchanged',old:'Exit 1.25 s',new:'Exit 1.25 s',od:'at=1 s; duration=0.25 s.',nd:'Event trace is preserved on the normal synthetic witness.',ex:'The patch is deliberately fail-fast, and a representative normal event trace is identical. This is not a proof of equivalence for all inputs.'}
];function show(i){const v=cases[i];for(let k=0;k<4;k++)document.querySelectorAll('button')[k].classList.toggle('active',k===i);document.getElementById('old').textContent=v.old;document.getElementById('new').textContent=v.new;document.getElementById('oldDesc').textContent=v.od;document.getElementById('newDesc').textContent=v.nd;document.getElementById('heading').textContent=v.title;document.getElementById('explain').textContent=v.ex;}show(0)</script></html>'''
(R/'results'/'interactive_audit.html').write_text(html)

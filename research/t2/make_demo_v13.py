"""Build an offline exhibit selector from the exact JSON means of v1.3.

No external libraries or CDNs in the resulting HTML. Inputs and all numbers
come from receiver_summary_v13.json; this script never fetches a website.
"""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent/"results"

def build(source=ROOT/"receiver_summary_v13.json",
          output=ROOT/"T2_receiver_demo_v13.html"):
    data=json.loads(Path(source).read_text())
    html='''<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>T2 v1.3 — turn pocket and receiving link</title>
<style>
body{font:16px system-ui,sans-serif;max-width:1020px;margin:32px auto;padding:15px;background:#f5f7f9;color:#152939}
main{background:white;padding:20px;border-radius:14px}
label{display:inline-block;margin:10px;padding:10px}select{padding:9px}
table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}
td,th{padding:12px;border-bottom:1px solid #ddd;text-align:right}
th:first-child,td:first-child{text-align:left}
svg{width:100%}.warn{font-weight:bold;color:#9b3800}
</style></head><body><main>
<h1>T2 — 좌회전 포켓과 하류 저장공간</h1>
<p class="warn">가상 교통모형 결과 · 실제 교차로 미보정 · 정책 권고 아님</p>
<p>720초 동안 8개 시드를 짝지어 실행한 평균. 표는 정지선 통과가 아닌 최종 하류 배출량입니다.</p>
<label>좌회전 비율<select id="turn"><option value=".3">30%</option><option value=".5">50%</option></select></label>
<label>직진차 B차로 배정<select id="b"><option value=".5">50%</option><option value="1">100%</option></select></label>
<label>하류 저장대수<select id="slots"><option>1</option><option selected>2</option><option>4</option></select></label>
<label>하류 배출 간격<select id="head"><option>2</option><option selected>4</option><option>8</option></select>초</label>
<svg id="chart" viewBox="0 0 900 380"></svg>
<table><thead><tr><th>포켓 길이</th><th>직진 완료</th><th>좌회전 완료</th><th>합계</th><th>수용공간 차단(초)</th></tr></thead><tbody id="rows"></tbody></table>
<p>포켓 0m는 좌회전 포켓에 진입할 수 없는 극단적인 대조군입니다. 하류 FIFO는 속도·가속·실제 합류를 단순화합니다.</p>
</main><script id="data" type="application/json">__DATA__</script>
<script>
const dataset=JSON.parse(document.getElementById('data').textContent);
const el=id=>document.getElementById(id);
function node(tag,attrs,text){let n=document.createElementNS('http://www.w3.org/2000/svg',tag);
 for(const [k,v] of Object.entries(attrs))n.setAttribute(k,v);
 if(text!==undefined)n.textContent=text;return n;}
function render(){
 let turn=+el('turn').value,b=+el('b').value,slots=+el('slots').value,head=+el('head').value;
 let rows=dataset.filter(r=>r.turn_share===turn&&r.B_share===b&&
 r.receiver_slots===slots&&r.receiver_headway_s===head).sort((x,y)=>x.pocket_m-y.pocket_m);
 if(rows.length!==4)throw Error('Missing scenario');
 let svg=el('chart');svg.replaceChildren();
 let cap=1.1*Math.max(...rows.flatMap(r=>[r.mean_network_S,r.mean_network_L]));
 svg.append(node('line',{x1:65,y1:320,x2:880,y2:320,stroke:'#677b8b'}));
 for(let i=0;i<4;i++){let r=rows[i],x=110+205*i;
  for(let [j,key,color] of [[0,'mean_network_S','#3667a4'],[1,'mean_network_L','#cb7932']]){
   let v=r[key],height=260*v/cap;
   svg.append(node('rect',{x:x+j*72,y:320-height,width:58,height,fill:color}));
   svg.append(node('text',{x:x+j*72+28,y:312-height,'text-anchor':'middle','font-size':15},v.toFixed(1)));}
  svg.append(node('text',{x:x+57,y:350,'text-anchor':'middle'},r.pocket_m+'m'));}
 el('rows').replaceChildren(...rows.map(r=>{let tr=document.createElement('tr');
  for(const value of [r.pocket_m+'m',r.mean_network_S.toFixed(2),r.mean_network_L.toFixed(2),
   (r.mean_network_S+r.mean_network_L).toFixed(2),r.mean_receiver_full_denied_s.toFixed(2)]){
   let td=document.createElement('td');td.textContent=value;tr.append(td);}return tr;}));
}
for(const id of ['turn','b','slots','head'])el(id).addEventListener('change',render);
render();
</script></body></html>'''
    output.parent.mkdir(exist_ok=True,parents=True)
    output.write_text(html.replace("__DATA__",json.dumps(data,separators=(",",":"))),encoding="utf8")
    return output

if __name__=="__main__":
    print(build())

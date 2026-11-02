from pathlib import Path
import csv,json
R=Path(__file__).parent
P=["fixed_32","coordinated_32","main_priority_38"]
data={p:{} for p in P}
with (R/'trace_vehicles.csv').open(encoding='utf-8-sig') as f:
 for r in csv.DictReader(f):
    t=str(round(float(r['t_s']),1));p=r['policy']
    data[p].setdefault(t,[]).append([int(r['id']),r['link'],round(float(r['x_m']),1),round(float(r['speed_mps']),1)])
queues={p:{} for p in P}
with (R/'trace_queues.csv').open(encoding='utf-8-sig') as f:
 for r in csv.DictReader(f):
    p=r['policy'];t=str(round(float(r['t_s']),1));queues[p][t]=[int(r['completed']),int(r['inside']),int(r['upstream_pending'])]
plans={p.__dict__['name']:{'offset':p.offset,'green':p.main_green,'cycle':p.cycle,'lost':p.lost} for p in __import__('network').PLANS if p.name in P}
source=(r'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>T2 v4.9 전람회 시뮬레이션 시연</title>
<style>:root{font-family:system-ui,'Malgun Gothic',sans-serif;background:#eff5f8;color:#163954}*{box-sizing:border-box}body{margin:0}header{padding:23px 32px;background:#153c5c;color:#fff}header h1{font-size:25px;margin:0 0 6px}header p{margin:0;color:#c2dde7}main{max-width:1130px;margin:auto;padding:22px}section{background:#fff;border-radius:16px;box-shadow:0 2px 13px #19395512;padding:18px 22px;margin:0 0 16px}.tag{display:inline-block;color:#8a4325;background:#fff3e8;border-radius:22px;padding:5px 9px;font-size:12px;font-weight:750}.controls{display:flex;flex-wrap:wrap;gap:15px;align-items:center}button,select{font:inherit;padding:9px 16px;border:1px solid #8faebd;border-radius:9px;background:#fff;color:#163954}button{background:#156e84;color:#fff;font-weight:700;cursor:pointer;border:0}input[type=range]{width:min(430px,100%)}.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.stat{background:#f0f5f9;border-radius:9px;padding:11px;font-size:12px}.stat b{font-size:22px;display:block;margin-bottom:4px}.note{color:#52697a;font-size:13px;line-height:1.7}#map{width:100%;height:auto;background:linear-gradient(#f7fafc,#f1f6f9);border-radius:12px}.grid{display:grid;grid-template-columns:2fr 1fr;gap:15px}@media(max-width:700px){.grid{grid-template-columns:1fr}.stats{grid-template-columns:1fr 1fr}}.mini{font-size:12px;color:#667c8d}footer{text-align:center;color:#6b7c88;padding:8px 20px 30px}</style></head><body>
<header><h1>T2 v4.9 | 개별 차량이 움직이는 3교차로 실험</h1><p>경남과학전람회 연구용 인터랙티브 시연 · 2026-11-02</p></header><main>
<section><span class="tag">합성 교통망 · 실제 창원 도로망/교통량이 아님 · SUMO 실행 아님</span><h2>모형을 직접 움직여 보기</h2><div class="controls"><button id="play">▶ 재생</button><label>신호정책 <select id="policy"><option value="fixed_32">고정 32초</option><option value="coordinated_32">오프셋 연동 32초</option><option value="main_priority_38">본선 우선 38초</option></select></label><label><span id="time">0</span>초 <input id="seek" type="range" min="0" max="578" step="2" value="0"></label></div><p class="mini">동일한 차량 유입 목록(seed=41, 균형 수요). 초록색 차량은 비교적 빠르게, 주황색은 느리게, 붉은색은 거의 정지한 상태를 의미해.</p>
<svg id="map" viewBox="0 0 800 315" role="img" aria-label="3개 신호교차로와 움직이는 차량들의 도로망"><g id="roads"></g><g id="signals"></g><g id="cars"></g></svg></section>
<div class="grid"><section><h3>현재 시점의 차량 흐름</h3><div class="stats"><div class="stat"><b id="n">0</b>도로 내부 차량</div><div class="stat"><b id="done">0</b>완료 통행</div><div class="stat"><b id="pending">0</b>경계 진입 대기</div></div><p class="note">도로 내부 차량 숫자는 2초 간격 궤적 스냅샷 기준이야. 완료 통행·경계 대기는 5초 간격 계측값을 사용해.</p></section><section><h3>실험 시 읽어야 할 것</h3><p class="note">차량이 출발지에서 만들어지는 시각은 정책마다 같고, 신호 현시만 달라져. 정지선에서 대기하는 차량과 각 교차로의 녹색 현시가 차이를 만들어.</p><p class="note">여기에는 보행자, 버스 정차, 차로변경, 실제 차로별 회전 충돌이 아직 구현되어 있지 않아.</p></section></div>
<section><h3>정책 효과의 평가 방법</h3><p class="note">전람회 정량 그래프는 3개 수요 조건 × 4개 신호계획 × 5개 시드 = 60회 독립 합성 실행에서 얻었어. 완료된 차량의 통행시간만 제시하면 종료 시 남아 있는 차량이 평가에서 빠질 수 있으므로 <b>총 차량·초(시스템 체류량)</b> 및 미완료 대수를 함께 보고해. 단지 동작하는 애니메이션만으로 실측 정확성·교통개선 효과가 입증되는 것은 아니야.</p></section></main><footer>독립 실행 HTML · 로컬 브라우저에서 인터넷 없이 작동 · T2 R&E 2027</footer>
<script>
const frames=__FRAMES__;const queues=__QUEUES__;const plans=__PLANS__;
const NS='http://www.w3.org/2000/svg';const svg=document.querySelector('#map');const road=svg.querySelector('#roads'),sig=svg.querySelector('#signals'),cars=svg.querySelector('#cars');
const nodes=[262,478,694];function el(tag,attrs,parent=svg){const e=document.createElementNS(NS,tag);for(const k in attrs)e.setAttribute(k,attrs[k]);parent.appendChild(e);return e;}
function txt(x,y,t,sz=13){const e=el('text',{x,y,'text-anchor':'middle','font-size':sz,fill:'#365168'},road);e.textContent=t;}
el('rect',{x:65,y:108,width:630,height:19,rx:4,fill:'#9cafbb'},road);for(let j=0;j<3;j++){const x=nodes[j];el('rect',{x:x-8,y:117,width:16,height:156,rx:4,fill:'#bccbd5'},road);el('circle',{cx:x,cy:118,r:21,fill:'#315c80'},road);const z=el('text',{x,y:124,'text-anchor':'middle',fill:'#fff','font-size':14,'font-weight':700},road);z.textContent='J'+(j+1);txt(x,290,'측면 S'+(j+1),12);}
txt(110,89,'M0',13);txt(361,89,'M1',13);txt(578,89,'M2',13);
for(let j=0;j<3;j++){let s=el('text',{x:nodes[j]+16,y:70,'text-anchor':'middle','font-size':12,fill:'#3b5673'},sig);s.textContent='';s.id='stage'+j;}
const seek=document.querySelector('#seek'),policy=document.querySelector('#policy'),clock=document.querySelector('#time');let timer=null;
function phase(p,j,t){let z=(t-p.offset[j])%p.cycle; if(z<0)z+=p.cycle;if(z<p.green[j])return '본선 녹색';if(z<p.green[j]+p.lost)return '전환';if(z<p.cycle-p.lost)return '측면 녹색';return '전환';}
function draw(){const t=Number(seek.value),p=policy.value;clock.textContent=t;cars.replaceChildren();let a=frames[p][String(t)]||[];
for(let j=0;j<3;j++){const stage=phase(plans[p],j,t);const e=document.querySelector('#stage'+j);e.textContent=stage;e.setAttribute('fill',stage==='전환'?'#ad683d':'#23836e');}
for(let v of a){const [id,link,x,speed]=v;let cx,cy;if(link[0]==='M'){const i=Number(link[1]);cx=65+[0,197,413][i]+x*1.19;cy=118;}else{cx=nodes[Number(link[1])];cy=270-x*(151/85);}const col=speed<0.8?'#db5755':speed<6?'#ef9c45':'#2f9e83';const dot=el('rect',{x:cx-4,y:cy-4,width:8,height:8,rx:2,fill:col,stroke:'#fff','stroke-width':0.8},cars);const title=el('title',{},dot);title.textContent='차량 '+id+' | '+link+' | '+speed+' m/s';}
document.querySelector('#n').textContent=a.length;const nearest=Object.keys(queues[p]).map(Number).filter(x=>x<=t).pop();const q=queues[p][String(nearest??0)]||[0,0,0];document.querySelector('#done').textContent=q[0];document.querySelector('#pending').textContent=q[2];}
seek.addEventListener('input',draw);policy.addEventListener('change',draw);
document.querySelector('#play').addEventListener('click',()=>{let b=document.querySelector('#play');if(timer){clearInterval(timer);timer=null;b.textContent='▶ 재생';return;}b.textContent='⏸ 일시정지';timer=setInterval(()=>{const n=Number(seek.value)+2;if(n>578){clearInterval(timer);timer=null;b.textContent='▶ 재생';return;}seek.value=n;draw();},115);});draw();
</script></body></html>''')
source=source.replace('__FRAMES__',json.dumps(data,separators=(',',':'),ensure_ascii=False)).replace('__QUEUES__',json.dumps(queues,separators=(',',':'))).replace('__PLANS__',json.dumps(plans,separators=(',',':')))
out=R/'T2_v49_exhibition_live_demo.html';out.write_text(source,encoding='utf-8');print(out,out.stat().st_size)

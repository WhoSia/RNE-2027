'use strict';
// P153 frozen prospective synthetic model; no real control or calibration.
const assert=(v,m)=>{if(!v)throw Error(m)};
const fresh=()=>({q:[],p:[],d:[],a:0,z:0,cost:0,competition:0});
const clone=s=>JSON.parse(JSON.stringify(s));
function step(s,t,period,reuse,priority,P,D,arrival,pre=false){
  const oldQ=s.q.length,oldP=s.p.length,oldD=s.d.length,head=s.q[0];
  const phase=t%period,half=period/2;
  const greenS=pre?phase<half:phase<=half;
  const greenL=pre?phase>=half:phase===0||phase>=half;
  const exit=oldD>0&&t%4<2?1:0;
  const supply=D-oldD+(reuse?exit:0);
  const admit=head==='L'&&oldP<P;
  const wantsS=greenS&&head==='S',wantsL=greenL&&oldP>0;
  if(wantsS&&wantsL&&supply>0)s.competition++;
  const move=supply<=0?null:wantsS&&wantsL?priority:wantsS?'S':wantsL?'L':null;
  assert(!(admit&&move==='S'),'shared head double use');
  if(exit){s.d.shift();s.z++}
  if(move==='S'){assert(wantsS,'S red');s.d.push(s.q.shift())}
  if(move==='L'){assert(wantsL,'L red');s.d.push(s.p.shift())}
  if(admit)s.p.push(s.q.shift());
  if(arrival!==undefined){s.q.push(arrival);s.a++}
  const n=s.q.length+s.p.length+s.d.length;
  s.cost+=n;
  assert(n===oldQ+oldP+oldD-exit+(arrival!==undefined?1:0),'stock delta');
  assert(s.z+n===s.a&&s.p.length<=P&&s.d.length<=D,'conservation/capacity');
}
function run(){
  const rows=[];let arms=0,competitionTicks=0,competitionArms=0,competitionScenarios=0;
  const storage={decrease:0,tie:0,increase:0,firstIncrease:null},priorityChange={different:0,tie:0};
  const rank={strict:0,tieCreated:0,tieResolved:0,unchanged:0,firstStrict:null};
  const priorityRank={strict:0,tieCreated:0,tieResolved:0,unchanged:0,firstStrict:null};
  function compare(a,b,stats,w){if(a*b<0){stats.strict++;stats.firstStrict??=w}else if(a===0&&b!==0)stats.tieResolved++;else if(a!==0&&b===0)stats.tieCreated++;else stats.unchanged++}
  for(let mask=0;mask<256;mask++)for(const interval of [1,2])for(const P of [1,2])for(const D of [1,2]){
    const tape=Object.fromEntries(Array.from({length:8},(_,i)=>[interval*i,mask&(1<<i)?'L':'S']));
    let pre=fresh();for(let t=0;t<8;t++)step(pre,t,4,false,'S',P,D,tape[t],true);
    const costs={},competition={};
    for(const reuse of [0,1])for(const priority of ['S','L'])for(const period of [4,8]){
      const s=clone(pre);for(let t=8;t<160;t++)step(s,t,period,!!reuse,priority,P,D,tape[t]);
      assert(s.a===8&&s.z===8,'clearance');const k=`${reuse}:${priority}:${period}`;
      costs[k]=s.cost;competition[k]=s.competition;arms++;competitionTicks+=s.competition;competitionArms+=+(s.competition>0);
    }
    if(Object.values(competition).some(n=>n>0))competitionScenarios++;
    const r={mask,interval,P,D,pre,future:Object.entries(tape).filter(([t])=>+t>=8),costs,competition};rows.push(r);
    for(const p of ['S','L']){
      for(const period of [4,8]){const a=costs[`0:${p}:${period}`],b=costs[`1:${p}:${period}`];if(b<a)storage.decrease++;else if(b===a)storage.tie++;else{storage.increase++;storage.firstIncrease??={...r,priority:p,period,delta:b-a}}}
      const a=costs[`0:${p}:4`]-costs[`0:${p}:8`],b=costs[`1:${p}:4`]-costs[`1:${p}:8`];compare(a,b,rank,{...r,priority:p,deltaOld:a,deltaReuse:b});
    }
    for(const reuse of [0,1]){
      for(const period of [4,8]){const a=costs[`${reuse}:S:${period}`],b=costs[`${reuse}:L:${period}`];if(a===b)priorityChange.tie++;else priorityChange.different++}
      const a=costs[`${reuse}:S:4`]-costs[`${reuse}:S:8`],b=costs[`${reuse}:L:4`]-costs[`${reuse}:L:8`];compare(a,b,priorityRank,{...r,reuse,deltaS:a,deltaL:b});
    }
  }
  const worlds=rows.flatMap(r=>[0,1].flatMap(reuse=>['S','L'].map(priority=>({r,reuse,priority,delta:r.costs[`${reuse}:${priority}:4`]-r.costs[`${reuse}:${priority}:8`]}))));
  function score(name,feature){
    const groups=new Map();for(const w of worlds){const {r}=w;const k=JSON.stringify([r.P,r.D,r.interval,r.pre.q,r.pre.p.length,r.pre.d.length,...feature(w)]);if(!groups.has(k))groups.set(k,[]);groups.get(k).push(w.delta)}
    let conflictCells=0,ambiguousWorlds=0,maxWorst=0,minimaxTotal=0,meanOptimalTotal=0;
    for(const ds of groups.values()){
      const a=Math.max(0,...ds),b=Math.max(0,...ds.map(x=>-x));
      const sa=ds.reduce((s,d)=>s+Math.max(0,d),0),sb=ds.reduce((s,d)=>s+Math.max(0,-d),0);
      if(a>0&&b>0){conflictCells++;ambiguousWorlds+=ds.length}maxWorst=Math.max(maxWorst,Math.min(a,b));minimaxTotal+=a<=b?sa:sb;meanOptimalTotal+=Math.min(sa,sb);
    }
    return {name,cells:groups.size,conflictCells,ambiguousWorlds,maxWorst,minimaxTotal,meanOptimalTotal,meanMinimax:minimaxTotal/worlds.length,meanOptimal:meanOptimalTotal/worlds.length};
  }
  const obs=[score('ordered',()=>[]),score('plus_convention',w=>[w.reuse]),score('plus_priority',w=>[w.priority]),score('plus_both_rules',w=>[w.reuse,w.priority]),score('plus_future',w=>[w.r.future]),score('oracle',w=>[w.r.future,w.reuse,w.priority])];
  for(const [a,b] of [[0,1],[0,2],[1,3],[2,3],[0,4],[3,5],[4,5]]){assert(obs[b].maxWorst<=obs[a].maxWorst,'nested worst');assert(obs[b].meanOptimal<=obs[a].meanOptimal,'nested mean');assert(obs[b].ambiguousWorlds<=obs[a].ambiguousWorlds,'nested ambiguity')}
  assert(obs[5].maxWorst===0,'oracle sufficient');
  return {status:'SYNTHETIC_PROSPECTIVE_NOT_FIELD',scenarios:rows.length,arms,worlds:worlds.length,clearanceFailures:0,competition:{ticks:competitionTicks,arms:competitionArms,scenarios:competitionScenarios},storage,rank,priorityChange,priorityRank,observations:obs};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};

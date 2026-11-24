'use strict';
// P154 prospective finite synthetic factorial; not a field-control policy.
const assert=(v,m)=>{if(!v)throw Error(m)};
const fresh=()=>({q:[],p:[],d:[],a:0,z:0,j:0,competition:0});
function tick(s,t,gate,reuse,priority,P,D,sink,arrival){
  const q=s.q.length,p=s.p.length,d=s.d.length;
  const exit=+(d>0&&(t+sink)%4<2),supply=D-d+(reuse?exit:0);
  const admit=s.q[0]==='L'&&p<P;
  const S=(gate==='S'||gate==='B')&&s.q[0]==='S',L=(gate==='L'||gate==='B')&&p>0;
  if(S&&L&&supply>0)s.competition++;
  const move=supply<=0?null:S&&L?priority:S?'S':L?'L':null;
  if(exit){s.d.shift();s.z++}
  if(move==='S'){assert(S&&!admit,'S eligibility');s.d.push(s.q.shift())}
  if(move==='L'){assert(L,'L eligibility');s.d.push(s.p.shift())}
  if(admit)s.p.push(s.q.shift());
  if(arrival!==undefined){s.q.push(arrival);s.a++}
  const n=s.q.length+s.p.length+s.d.length;s.j+=n;
  assert(n===q+p+d-exit+(arrival!==undefined?1:0)&&s.a===s.z+n&&s.p.length<=P&&s.d.length<=D,'conservation/capacity');
}
const gates={4:'BSBL',8:'BBSSBBLL'};
function run(){
  const rows=[];let arms=0,competitionArms=0,competitionTicks=0;
  const storage={decrease:0,tie:0,increase:0,firstIncrease:null},priority={different:0,tie:0};
  for(let mask=0;mask<128;mask++)for(const interval of [1,2])for(const P of [1,2])for(const D of [1,2])for(const sink of [0,2]){
    const tape=Object.fromEntries(Array.from({length:7},(_,i)=>[interval*i,mask&(1<<i)?'L':'S']));
    const pre=fresh();for(let t=0;t<8;t++)tick(pre,t,t%4<2?'S':'L',0,'S',P,D,sink,tape[t]);
    const costs=[];
    for(const reuse of [0,1])for(const pri of ['S','L']){
      const c=[];for(const period of [4,8])for(let o=0;o<period;o++){
        const s=JSON.parse(JSON.stringify(pre));for(let t=8;t<160;t++)tick(s,t,gates[period][(t+o)%period],reuse,pri,P,D,sink,tape[t]);
        assert(s.a===7&&s.z===7,'clearance');arms++;competitionArms+=+(s.competition>0);competitionTicks+=s.competition;c.push(s.j);
      }costs.push(c);
    }
    const r={mask,interval,P,D,sink,pre,future:Object.entries(tape).filter(([t])=>+t>=8),costs};rows.push(r);
    for(let i=0;i<12;i++)for(let p=0;p<2;p++){
      const a=costs[p][i],b=costs[p+2][i];if(b<a)storage.decrease++;else if(b===a)storage.tie++;else{storage.increase++;storage.firstIncrease??={...r,arm:i,priority:p,delta:b-a}}
      if(costs[2*p][i]===costs[2*p+1][i])priority.tie++;else priority.different++;
    }
  }
  const rank=()=>({strict:0,tieCreated:0,tieResolved:0,unchanged:0,firstStrict:null});
  const storageRank=rank(),priorityRank=rank(),delta={negative:0,zero:0,positive:0};
  const names=['context','ordered','plus_convention','plus_priority','plus_both_rules','plus_future','oracle'];
  const obs=names.map(name=>({name,cells:0,conflictCells:0,ambiguousWorlds:0,maxWorst:0,minimaxTotal:0,meanOptimalTotal:0}));
  function cmp(a,b,stat,w){if(a*b<0){stat.strict++;stat.firstStrict??=w}else if(a===0&&b!==0)stat.tieResolved++;else if(a!==0&&b===0)stat.tieCreated++;else stat.unchanged++}
  for(let o4=0;o4<4;o4++)for(let o8=0;o8<8;o8++){
    const maps=names.map(()=>new Map());
    function add(map,key,d){let a=map.get(key);if(!a){a=[0,0,0,0,0];map.set(key,a)}a[0]=Math.max(a[0],d);a[1]=Math.max(a[1],-d);a[2]+=Math.max(0,d);a[3]+=Math.max(0,-d);a[4]++}
    for(const r of rows){
      const ds=r.costs.map(c=>c[o4]-c[4+o8]);
      for(let i=0;i<2;i++){
        cmp(ds[i],ds[i+2],storageRank,{mask:r.mask,interval:r.interval,P:r.P,D:r.D,sink:r.sink,o4,o8,priority:i,deltaOld:ds[i],deltaReuse:ds[i+2],costs:r.costs.map(c=>[c[o4],c[4+o8]])});
        cmp(ds[2*i],ds[2*i+1],priorityRank,{mask:r.mask,interval:r.interval,P:r.P,D:r.D,sink:r.sink,o4,o8,reuse:i,deltaS:ds[2*i],deltaL:ds[2*i+1],costs:r.costs.map(c=>[c[o4],c[4+o8]])});
      }
      const context=[r.P,r.D,r.interval,r.sink],state=[...context,r.pre.q,r.pre.p.length,r.pre.d.length];
      for(let i=0;i<4;i++){
        const d=ds[i],reuse=i>>1,pri=i%2;
        if(d<0)delta.negative++;else if(d>0)delta.positive++;else delta.zero++;
        const keys=[context,state,[...state,reuse],[...state,pri],[...state,reuse,pri],[...state,r.future],[...state,r.future,reuse,pri]];
        for(let k=0;k<keys.length;k++)add(maps[k],JSON.stringify(keys[k]),d);
      }
    }
    for(let i=0;i<maps.length;i++){
      const z=obs[i];z.cells+=maps[i].size;
      for(const [a,b,sa,sb,n] of maps[i].values()){
        if(a>0&&b>0){z.conflictCells++;z.ambiguousWorlds+=n}z.maxWorst=Math.max(z.maxWorst,Math.min(a,b));z.minimaxTotal+=a<=b?sa:sb;z.meanOptimalTotal+=Math.min(sa,sb);
      }
    }
  }
  const worlds=rows.length*4*32;
  for(const z of obs){z.meanMinimax=z.minimaxTotal/worlds;z.meanOptimal=z.meanOptimalTotal/worlds}
  for(const [a,b] of [[0,1],[1,2],[1,3],[2,4],[3,4],[1,5],[4,6],[5,6]])assert(obs[b].maxWorst<=obs[a].maxWorst&&obs[b].meanOptimal<=obs[a].meanOptimal&&obs[b].ambiguousWorlds<=obs[a].ambiguousWorlds,'nested refinement');
  assert(obs[6].maxWorst===0&&delta.negative+delta.zero+delta.positive===worlds,'oracle/counts');
  return {status:'PROSPECTIVE_EQUAL_DUTY_SYNTHETIC_NOT_FIELD',scenarios:rows.length,arms,worlds,clearanceFailures:0,competition:{arms:competitionArms,ticks:competitionTicks},storage,priority,storageRank,priorityRank,delta,observations:obs};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};

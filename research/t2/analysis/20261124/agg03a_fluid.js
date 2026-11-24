// AGG03A: conservative fractional fluid closure, offline synthetic only.
function run(){
 const assert=(x,m)=>{if(!x)throw Error(m)}, eps=1e-8;
 const pol=[3,4,5].flatMap(g=>[0,2,4,6].map(o=>[g,o])),clocks=["dense","platoon","sparse"];
 function tape(seed,left,clock){let x=seed+1,a=Array.from({length:24},(_,i)=>i);for(let i=23;i>0;i--){x=(Math.imul(1664525,x)+1013904223)>>>0;const j=x%(i+1);[a[i],a[j]]=[a[j],a[i]]}return Object.fromEntries(a.map((v,i)=>[clock==="dense"?i:clock==="platoon"?8*Math.floor(i/4)+i%4:4*i,v<left?"L":"S"]))}
 function micro(s,t,g,o,P,R,v){const green=t%8<g,down=(t+o)%8<4,x=+(green&&s.q[0]==="S"&&s.r<R),a=+(s.q[0]==="L"&&s.p<P),y=+(!green&&s.p>0),z=+(down&&s.r>0);if(x||a)s.q.shift();s.p+=a-y;s.r+=x-z;s.Y+=y;s.Z+=z;if(v){s.q.push(v);s.A++}const stock=s.q.length+s.p+s.r;assert(s.A===stock+s.Y+s.Z&&s.p>=0&&s.p<=P&&s.r>=0&&s.r<=R,"micro conservation");s.J+=stock;}
 function fluid(s,t,g,o,P,R,v,m){const gs=t%8<g,down=(t+o)%8<4,total=s.S+s.L,fs=total>0?s.S/total:0,fl=total>0?s.L/total:0;const x=gs?Math.min(s.S,m==="mixed"?fs:1,Math.max(0,R-s.r)):0,a=Math.min(s.L,m==="mixed"?fl:1,Math.max(0,P-s.p)),y=gs?0:Math.min(s.p,1),z=down?Math.min(s.r,1):0;s.S-=x;s.L-=a;s.p+=a-y;s.r+=x-z;s.Y+=y;s.Z+=z;if(v){s.A++;if(v==="S")s.S++;else s.L++}const stock=s.S+s.L+s.p+s.r;assert(Math.abs(s.A-stock-s.Y-s.Z)<eps&&Math.min(s.S,s.L,s.p,s.r)>=-eps&&s.p<=P+eps&&s.r<=R+eps,"fluid conservation");s.J+=stock;}
 const fresh=()=>({n:0,J:0,regret:0,worst:0,miss:0,vsFixed:[0,0,0],vsTrained:[0,0,0]});
 const modelFresh=()=>({arms:0,signed:0,absolute:0,squared:0,maxAbsolute:0,terminal:0,maxTerminal:0,nonclear:0,rankPairs:0,strictFlips:0,oracleSetMiss:0});
 const groups=Object.fromEntries(["all",...clocks].map(k=>[k,{policy:Object.fromEntries(["fixed","trained","mixed","separate","oracle"].map(n=>[n,fresh()])),model:{mixed:modelFresh(),separate:modelFresh()}}]));
 const seeds={};let arms=0;
 const pick=a=>{let i=0;for(let j=1;j<a.length;j++)if(a[j]<a[i]-eps)i=j;return i};
 for(let seed=180;seed<200;seed++)for(const left of [6,12,18])for(const clock of clocks)for(const P of [1,3])for(const R of [1,3]){
  const ar=tape(seed,left,clock),pre={q:[],p:0,r:0,Y:0,Z:0,A:0,J:0};for(let t=0;t<16;t++)micro(pre,t,4,0,P,R,ar[t]);
  const mc=[],results={mixed:[],separate:[]};
  for(const [g,o] of pol){let s={...pre,q:pre.q.slice()};for(let t=16;t<240;t++)micro(s,t,g,o,P,R,ar[t]);assert(s.A===24&&s.Y+s.Z===24,"micro clear");mc.push(s.J);arms++;
   for(const m of ["mixed","separate"]){const S=pre.q.filter(v=>v==="S").length;let f={S,L:pre.q.length-S,p:pre.p,r:pre.r,Y:pre.Y,Z:pre.Z,A:pre.A,J:pre.J};for(let t=16;t<240;t++)fluid(f,t,g,o,P,R,ar[t],m);assert(f.A===24,"arrival");results[m].push({J:f.J,terminal:f.S+f.L+f.p+f.r});arms++}
  }
  const oi=pick(mc),best=mc[oi],trained=P===1?0:4,ids={fixed:4,trained,mixed:pick(results.mixed.map(x=>x.J)),separate:pick(results.separate.map(x=>x.J)),oracle:oi};
  const sd=seeds[seed]??(seeds[seed]={n:0,mixedRegret:0,separateRegret:0,trainedRegret:0});sd.n++;sd.mixedRegret+=mc[ids.mixed]-best;sd.separateRegret+=mc[ids.separate]-best;sd.trainedRegret+=mc[trained]-best;
  for(const k of ["all",clock]){const group=groups[k];for(const [name,i] of Object.entries(ids)){const z=group.policy[name],cost=mc[i],d=cost-best;z.n++;z.J+=cost;z.regret+=d;z.worst=Math.max(z.worst,d);z.miss+=d>0;z.vsFixed[Math.sign(cost-mc[4])+1]++;z.vsTrained[Math.sign(cost-mc[trained])+1]++}
   for(const m of ["mixed","separate"]){const s=group.model[m],rs=results[m];s.oracleSetMiss+=mc[ids[m]]>best;
    for(let i=0;i<12;i++){const d=rs[i].J-mc[i];s.arms++;s.signed+=d;s.absolute+=Math.abs(d);s.squared+=d*d;s.maxAbsolute=Math.max(s.maxAbsolute,Math.abs(d));s.terminal+=rs[i].terminal;s.maxTerminal=Math.max(s.maxTerminal,rs[i].terminal);s.nonclear+=rs[i].terminal>eps;
     for(let j=i+1;j<12;j++){s.rankPairs++;const dm=mc[i]-mc[j],df=rs[i].J-rs[j].J;s.strictFlips+=(Math.abs(df)>eps&&dm*df<0)}
    }
   }
  }
 }
 assert(arms===25920,"denom");return {status:"EXECUTED_JS_ISOLATE_ABSTRACT_OFFLINE",worlds:720,arms,policies:pol,groups,seeds};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};

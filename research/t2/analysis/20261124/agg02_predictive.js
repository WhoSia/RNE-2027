// AGG02: preblock conditional transfer prediction, offline synthetic.
function run(){
 const assert=(b,m)=>{if(!b)throw Error(m)};
 const clocks=["dense","platoon","sparse"];
 function tape(seed,left,clock){let x=seed+1,a=Array.from({length:24},(_,i)=>i);for(let i=23;i>0;i--){x=(Math.imul(1664525,x)+1013904223)>>>0;const j=x%(i+1);[a[i],a[j]]=[a[j],a[i]]}return Object.fromEntries(a.map((v,i)=>[clock==="dense"?i:clock==="platoon"?8*Math.floor(i/4)+i%4:4*i,v<left?"L":"S"]));}
 const maps=[new Map(),new Map(),new Map()];
 const names=["context","count_independent","count_joint","movement_joint"];
 const blank=()=>({n:0,actual:0,signed:0,absolute:0,squared:0});
 const stats=Object.fromEntries(["all","active_at_start",...clocks].map(k=>[k,Object.fromEntries(names.map(n=>[n,blank()]))]));
 const seedStats={},coverage={count:0,movement:0,total:0},trainCoverage={blocks:0,active:0};let trainArms=0,testArms=0;
 function add(map,k,seed,d,b,x){let a=map.get(k);if(!a){a={n:0,d:0,b:0,x:0,seeds:new Set()};map.set(k,a)}a.n++;a.d+=d;a.b+=b;a.x+=x;a.seeds.add(seed)}
 const supported=a=>a&&a.seeds.size>=4;
 function score(seed,clock,keys,active,d,b,x){
  const a=maps[0].get(keys[0]),b0=maps[1].get(keys[1]),c0=maps[2].get(keys[2]);assert(supported(a),"context support");const b1=supported(b0)?b0:a,c=supported(c0)?c0:b1;
  coverage.total++;coverage.count+=+supported(b0);coverage.movement+=+supported(c0);
  const pred=[a.x/a.n,b1.d*b1.b/(8*b1.n*b1.n),b1.x/b1.n,c.x/c.n];
  for(const p of pred)assert(p>=0&&p<=8,"prediction range");
  const ks=["all",clock];if(active)ks.push("active_at_start");
  const ss=seedStats[seed]??(seedStats[seed]={n:0,absolute:Array(4).fill(0),activeN:0,activeAbsolute:Array(4).fill(0)});ss.n++;ss.activeN+=+active;
  names.forEach((name,i)=>{const err=pred[i]-x;for(const k of ks){const s=stats[k][name];s.n++;s.actual+=x;s.signed+=err;s.absolute+=Math.abs(err);s.squared+=err*err}ss.absolute[i]+=Math.abs(err);if(active)ss.activeAbsolute[i]+=Math.abs(err)});
 }
 for(const seed of [...Array.from({length:60},(_,i)=>i).filter(i=>i%5!==0),...Array.from({length:20},(_,i)=>160+i)])for(const left of [6,12,18])for(const clock of clocks)for(const P of [1,3])for(const R of [1,3])for(const g of [3,4,5])for(const o of [0,2,4,6]){
  const train=seed<60;train?trainArms++:testArms++;
  const ar=tape(seed,left,clock),q=[];let p=0,r=0,A=0,Y=0,Z=0,d=0,b=0,x=0,keys=[],active=false;
  for(let t=0;t<240;t++){
   if(t>=16&&t%8===0){const k=`${P}:${R}:${g}:${o}:${t/8}`;const nS=q.filter(v=>v==="S").length;keys=[k,`${k}:${q.length}:${p}:${r}`,`${k}:${q.length}:${p}:${r}:${nS}:${q.length-nS}:${q[0]||"-"}`];active=q.length>0;d=b=x=0}
   const gs=t%8<(t<16?4:g),down=(t+(t<16?0:o))%8<4,D=+(q[0]==="S"&&gs),B=+(r<R),X=D*B,ad=+(q[0]==="L"&&p<P),ml=+(!gs&&p>0),z=+(r>0&&down);
   if(X||ad)q.shift();p+=ad-ml;r+=X-z;Y+=ml;Z+=z;if(ar[t]){A++;q.push(ar[t])}
   assert(A===q.length+p+r+Y+Z&&p>=0&&p<=P&&r>=0&&r<=R,"conservation");
   if(t>=16){d+=D;b+=B;x+=X;if(t%8===7){assert(x<=Math.min(d,b),"bound");if(train){keys.forEach((k,i)=>add(maps[i],k,seed,d,b,x));trainCoverage.blocks++;trainCoverage.active+=+active}else score(seed,clock,keys,active,d,b,x);}}
  }assert(A===24&&Y+Z===24,"clear");
 }
 assert(trainArms===20736&&testArms===8640,"denom");
 const paired={};
 for(const [a,b] of [[1,0],[2,1],[3,2],[3,0]])for(const active of [false,true]){const dif=Object.values(seedStats).map(s=>{const v=active?s.activeAbsolute:s.absolute;return v[a]-v[b]});paired[`${names[a]}_minus_${names[b]}_${active?"active":"all"}`]={better:dif.filter(x=>x< -1e-9).length,tie:dif.filter(x=>Math.abs(x)<=1e-9).length,worse:dif.filter(x=>x>1e-9).length,min:Math.min(...dif),max:Math.max(...dif),mean:dif.reduce((a,b)=>a+b,0)/dif.length};}
 return {status:"EXECUTED_JS_ISOLATE_SYNTHETIC_PREDICTION_NOT_FIELD",trainWorlds:1728,testWorlds:720,trainArms,testArms,trainCoverage,coverage,cells:maps.map(m=>({all:m.size,supported:[...m.values()].filter(supported).length})),stats,paired,seedStats};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};

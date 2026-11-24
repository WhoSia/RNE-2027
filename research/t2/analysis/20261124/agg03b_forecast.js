// AGG03B synthetic offline scenario selection.
function run(){
 const assert=(b,m)=>{if(!b)throw Error(m)},eps=1e-8,clocks=["dense","platoon","sparse"],pol=[3,4,5].flatMap(g=>[0,2,4,6].map(o=>[g,o]));
 function tape(seed,left,clock){let x=seed+1,a=Array.from({length:24},(_,i)=>i);for(let i=23;i>0;i--){x=(Math.imul(1664525,x)+1013904223)>>>0;let j=x%(i+1);[a[i],a[j]]=[a[j],a[i]]}let ar=Array(240).fill("");a.forEach((v,i)=>ar[clock==="dense"?i:clock==="platoon"?8*Math.floor(i/4)+i%4:4*i]=v<left?"L":"S");return ar}
 function prefix(ar){let S=0,L=0;for(let t=0;t<16;t++){S+=ar[t]==="S";L+=ar[t]==="L"}return [S,L]}
 function tick(s,t,g,o,P,R,v){let gs=t%8<g,down=(t+o)%8<4,x=+(gs&&s.q[0]==="S"&&s.r<R),a=+(s.q[0]==="L"&&s.p<P),y=+(!gs&&s.p>0),z=+(down&&s.r>0);if(x||a)s.q.shift();s.p+=a-y;s.r+=x-z;s.Y+=y;s.Z+=z;if(v){s.A++;s.q.push(v)}let stock=s.q.length+s.p+s.r;assert(s.A===stock+s.Y+s.Z&&s.p>=0&&s.p<=P&&s.r>=0&&s.r<=R,"micro");s.J+=stock}
 function micro(pre,ar,P,R,g,o,feedback=false){let s={...pre,q:pre.q.slice()};for(let t=16;t<240;t++){if(feedback&&t%8===0){let qs=s.q.filter(x=>x==="S").length,ps=Math.max(0,qs-s.r),pl=s.q.length-qs+s.p;g=ps>pl?5:ps<pl?3:4}tick(s,t,g,o,P,R,ar[t]);}return {J:s.J,terminal:s.q.length+s.p+s.r}}
 function fluid(pre,ar,P,R,g,o,mixed){let S=pre.q.filter(x=>x==="S").length,L=pre.q.length-S,p=pre.p,r=pre.r,A=pre.A,Y=pre.Y,Z=pre.Z,J=pre.J;for(let t=16;t<240;t++){let gs=t%8<g,ds=(t+o)%8<4,total=S+L,fs=total?S/total:0,fl=total?L/total:0,x=gs?Math.min(S,mixed?fs:1,Math.max(0,R-r)):0,a=Math.min(L,mixed?fl:1,Math.max(0,P-p)),y=gs?0:Math.min(p,1),z=ds?Math.min(r,1):0;S-=x;L-=a;p+=a-y;r+=x-z;Y+=y;Z+=z;let v=ar[t];if(v){A++;S+=v==="S";L+=v==="L"}let stock=S+L+p+r;assert(Math.abs(A-stock-Y-Z)<eps&&Math.min(S,L,p,r)>=-eps&&p<=P+eps&&r<=R+eps,"fluid");J+=stock}return {J,terminal:S+L+p+r}}
 const lib=[];for(let seed=0;seed<60;seed++)if(seed%5)for(let left of [6,12,18])for(let c of clocks){let ar=tape(seed,left,c);lib.push({ar,prefix:prefix(ar)})}assert(lib.length===432,"library");
 const pick=a=>{let k=0;for(let i=1;i<a.length;i++)if(a[i]<a[k]-eps)k=i;return k};
 const names=["fixed","trained","demand","forecast_micro","forecast_mixed","forecast_separate","feedback","oracle"];
 const blank=()=>({n:0,J:0,staticGap:0,worstGap:null,aboveStatic:0,vsTrained:[0,0,0],vsMicroForecast:[0,0,0]});
 const stats=Object.fromEntries(["all",...clocks].map(k=>[k,Object.fromEntries(names.map(n=>[n,blank()]))]));let arms={truth:0,forecast:0,feedback:0},distance={},distinct={},terminal={micro:0,mixed:0,separate:0},seeds={};
 for(let seed=200;seed<220;seed++)for(let left of [6,12,18])for(let clock of clocks)for(let P of [1,3])for(let R of [1,3]){
  let ar=tape(seed,left,clock),pref=prefix(ar),pre={q:[],p:0,r:0,A:0,Y:0,Z:0,J:0};for(let t=0;t<16;t++)tick(pre,t,4,0,P,R,ar[t]);
  let dmin=Math.min(...lib.map(v=>Math.abs(v.prefix[0]-pref[0])+Math.abs(v.prefix[1]-pref[1]))),matches=lib.filter(v=>Math.abs(v.prefix[0]-pref[0])+Math.abs(v.prefix[1]-pref[1])===dmin);
  let scenarios=Array.from({length:4},(_,j)=>matches[Math.floor((j+.5)*matches.length/4)].ar);
  let uniq=new Set(scenarios.map(a=>a.slice(16).map(v=>v||"-").join(""))).size;distance[dmin]=(distance[dmin]||0)+1;distinct[uniq]=(distinct[uniq]||0)+1;
  let truth=pol.map(([g,o])=>{arms.truth++;let s=micro(pre,ar,P,R,g,o);assert(s.terminal===0,"true clear");return s.J});
  let forecasts=[[],[],[]];for(let [g,o] of pol){let sums=[0,0,0];for(let scenario of scenarios){let rs=[micro(pre,scenario,P,R,g,o),fluid(pre,scenario,P,R,g,o,true),fluid(pre,scenario,P,R,g,o,false)];arms.forecast+=3;rs.forEach((v,i)=>{sums[i]+=v.J;terminal[["micro","mixed","separate"][i]]+=+(v.terminal>eps)})}sums.forEach((v,i)=>forecasts[i].push(v))}
  let best=Math.min(...truth),trained=truth[P===1?0:4],share=pref[0]/(pref[0]+pref[1]),demand=truth[share>=.75?8:share<=.25?0:4],m=truth[pick(forecasts[0])],f=truth[pick(forecasts[1])],s=truth[pick(forecasts[2])];let fb=micro(pre,ar,P,R,4,0,true);arms.feedback++;assert(!fb.terminal,"feedback clear");
  let costs=[truth[4],trained,demand,m,f,s,fb.J,best];let ss=seeds[seed]??(seeds[seed]=Object.fromEntries(names.map(n=>[n,0])));names.forEach((n,i)=>ss[n]+=costs[i]);
  for(let k of ["all",clock])names.forEach((n,i)=>{let a=stats[k][n],J=costs[i],gap=J-best;a.n++;a.J+=J;a.staticGap+=gap;a.worstGap=a.worstGap===null?gap:Math.max(a.worstGap,gap);a.aboveStatic+=gap>0;a.vsTrained[Math.sign(J-trained)+1]++;a.vsMicroForecast[Math.sign(J-m)+1]++});
 }
 assert(arms.truth===8640&&arms.forecast===103680&&arms.feedback===720,"denom");
 return {status:"JS_ISOLATE_SYNTHETIC_OFFLINE",library:lib.length,arms,distance,distinct,terminal,stats,seeds};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};

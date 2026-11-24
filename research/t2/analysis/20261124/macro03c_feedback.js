// MACRO03C abstract offline feedback comparison, not road control.
function run(){
 const check=(x,m)=>{if(!x)throw Error(m)};
 const pol=[3,4,5].flatMap(g=>[0,2,4,6].map(o=>({g,o}))), clocks=["dense","platoon","sparse"];
 function tape(seed,left,clock){let x=seed+1,a=Array.from({length:24},(_,i)=>i);for(let i=23;i>0;i--){x=(Math.imul(x,1664525)+1013904223)>>>0;const j=x%(i+1);[a[i],a[j]]=[a[j],a[i]]}return Object.fromEntries(a.map((v,i)=>[clock==="dense"?i:clock==="platoon"?8*Math.floor(i/4)+i%4:4*i,v<left?"L":"S"]))}
 function step(s,t,g,o,P,R,v){const gs=t%8<g,x=+(s.r>0&&(t+o)%8<4),h=s.q[0],ad=+(h==="L"&&s.p<P),ms=+(gs&&h==="S"&&s.r<R),ml=+(!gs&&s.p>0);s.denial+=+(gs&&h==="S"&&s.r===R);check(ms+ml<=1&&ms+ad<=1,"eligibility");if(ms||ad)s.q.shift();s.p+=ad-ml;s.r+=ms-x;s.zS+=x;s.zL+=ml;if(v){s.q.push(v);s.aS+=+(v==="S");s.aL+=+(v==="L")}const ns=s.q.filter(v=>v==="S").length+s.r,nl=s.q.length+s.p+s.r-ns;check(s.aS-s.zS===ns&&s.aL-s.zL===nl&&s.p>=0&&s.p<=P&&s.r>=0&&s.r<=R,"conservation");s.S+=ns;s.L+=nl;}
 function cost(pre,ar,P,R,policy){let s={...pre,q:pre.q.slice()},g=policy.g,o=policy.o;for(let t=16;t<240;t++){if(t%8===0&&policy.kind){if(policy.kind==="pressure"){const qs=s.q.filter(x=>x==="S").length,ps=Math.max(0,qs-s.r),pl=s.q.length-qs+s.p;g=ps>pl?5:ps<pl?3:4;}else g=s.q[0]==="S"&&s.r<R?5:s.q[0]==="L"||s.p===P?3:4;}step(s,t,g,o,P,R,ar[t]);if(s.zS+s.zL===24)break}check(s.zS+s.zL===24,"clear");return {J:s.S+s.L,S:s.S,L:s.L,denial:s.denial}}
 const rows=[];for(const seed of [...Array.from({length:60},(_,i)=>i).filter(i=>i%5!==0),...Array.from({length:20},(_,i)=>100+i)])for(const left of [6,12,18])for(const clock of clocks)for(const P of [1,3])for(const R of [1,3]){
 const ar=tape(seed,left,clock),pre={q:[],p:0,r:0,aS:0,aL:0,zS:0,zL:0,S:0,L:0,denial:0};for(let t=0;t<16;t++)step(pre,t,4,0,P,R,ar[t]);const cs=pol.map(p=>cost(pre,ar,P,R,p)),b=Math.min(...cs.map(c=>c.J)),frac=pre.aS/(pre.aS+pre.aL);
 rows.push({seed,clock,ctx:`${P}:${R}`,obs:`${P}:${R}:${pre.q.length}:${pre.p}:${pre.r}`,demand:pol.findIndex(p=>p.g===(frac>=.75?5:frac<=.25?3:4)&&p.o===0),cs,b,feedback:seed>=100?["pressure","head"].map(kind=>cost(pre,ar,P,R,{g:4,o:0,kind})):[]});
 }
 const train=rows.filter(r=>r.seed<60),test=rows.filter(r=>r.seed>=100);check(train.length===1728&&test.length===720,"denom");
 const group=(rs,k)=>{let m=new Map();for(const r of rs){const key=r[k];if(!m.has(key))m.set(key,[]);m.get(key).push(r)}return m};
 const choose=(rs,minimax=false)=>{let scores=pol.map((_,i)=>minimax?Math.max(...rs.map(r=>r.cs[i].J-r.b)):rs.reduce((s,r)=>s+r.cs[i].J,0));return scores.indexOf(Math.min(...scores))};
 const ctx=group(train,"ctx"),obs=group(train,"obs");const fixes=Object.fromEntries([...ctx].map(([k,rs])=>[k,[choose(rs),choose(rs,true)]]));const picks=new Map([...obs].filter(([k,rs])=>new Set(rs.map(r=>r.seed)).size>=4).map(([k,rs])=>[k,choose(rs)]));
 const names=["fixed","demand","mean","minimax","counts","pressure","head","static_oracle"];const stats=Object.fromEntries(["all",...clocks].map(k=>[k,Object.fromEntries(names.map(n=>[n,{n:0,J:0,S:0,L:0,denial:0,regret:0,worst:null,vsDemand:[0,0,0],vsMean:[0,0,0]}]))]));
 let covered=0;
 for(const r of test){const [mean,mini]=fixes[r.ctx],a=picks.get(r.obs);covered+=+(a!==undefined);const cs=[r.cs[4],r.cs[r.demand],r.cs[mean],r.cs[mini],r.cs[a??mean],...r.feedback,r.cs[r.cs.findIndex(c=>c.J===r.b)]];for(const group of ["all",r.clock])names.forEach((n,i)=>{const c=cs[i],s=stats[group][n],d=c.J-r.b;s.n++;for(const k of ["J","S","L","denial"])s[k]+=c[k];s.regret+=d;s.worst=s.worst===null?d:Math.max(s.worst,d);s.vsDemand[Math.sign(c.J-r.cs[r.demand].J)+1]++;s.vsMean[Math.sign(c.J-r.cs[mean].J)+1]++});}
 return {status:"EXECUTED_JS_ISOLATE_ABSTRACT_OFFLINE",train:train.length,test:test.length,staticArms:rows.length*12,feedbackArms:test.length*2,fixes,covered,stats};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};

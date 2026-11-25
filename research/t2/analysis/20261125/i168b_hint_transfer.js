// Offline abstract synthetic train-only decision comparison.
function run(){
const assert=(b,m)=>{if(!b)throw Error(m)},pol=[3,4,5].flatMap(g=>[0,2,4,6].map(o=>[g,o])),A=Array.from({length:12},(_,i)=>i),pairs=A.flatMap(a=>A.map(b=>[a,b])),nom=[2,2,2],verts=[[4,1,1],[1,4,1],[1,1,4]],priors=[nom,...verts],pure=[[6,0,0],[0,6,0],[0,0,6]];
function labels(seed,left){let a=Array.from({length:24},(_,i)=>i),x=seed+1;for(let i=23;i>0;i--){x=(Math.imul(1664525,x)+1013904223)>>>0;let j=x%(i+1);[a[i],a[j]]=[a[j],a[i]]}return a.map(v=>v<left?"L":"S")}
function tick(s,t,g,o,P,R,v){let gs=t%8<g,ds=(t+o)%8<4,x=+(gs&&s.q[0]==="S"&&s.r<R),a=+(s.q[0]==="L"&&s.p<P),y=+(!gs&&s.p>0),z=+(ds&&s.r>0);if(x||a)s.q.shift();s.p+=a-y;s.r+=x-z;s.Y+=y;s.Z+=z;if(v){s.q.push(v);s.A++}let stock=s.q.length+s.p+s.r;assert(stock+s.Y+s.Z===s.A&&s.p>=0&&s.p<=P&&s.r>=0&&s.r<=R,"mass");s.J+=stock}
let arms=0;
function rows(seeds){let out=[];for(let seed of seeds)for(let left of [6,12,18])for(let P of [1,3])for(let R of [1,3]){
let lab=labels(seed,left),pre={q:[],p:0,r:0,A:0,Y:0,Z:0,J:0};for(let t=0;t<16;t++)tick(pre,t,4,0,P,R,t%4===0?lab[t/4]:"");
let c=[[16,4],[16,1],[32,1]].map(([start,stride])=>{let ar=Array(240).fill("");for(let j=0;j<20;j++)ar[start+j*stride]=lab[4+j];return pol.map(([g,o])=>{let s={...pre,q:pre.q.slice()};for(let t=16;t<240;t++)tick(s,t,g,o,P,R,ar[t]);assert(s.A===24&&s.Y+s.Z===24,"clear");arms++;return s.J})});
let mins=c.map(r=>Math.min(...r));out.push({seed,geo:`${P}:${R}`,key:`${P}:${R}:${lab.slice(0,4).join("")}`,c,r:c.map((row,i)=>row.map(x=>x-mins[i]))})}return out}
const train=rows(Array.from({length:60},(_,i)=>i).filter(i=>i%5)),cal=rows(Array.from({length:10},(_,i)=>480+i));
function fitGroups(key){let m=new Map();for(let r of train){let k=r[key];if(!m.has(k))m.set(k,[]);m.get(k).push(r)}return m}
const geo=fitGroups("geo"),prefix=fitGroups("key");
function weighted(matrix,w,err,[a,b]){let q=[4-err,err,err];return w.reduce((s,v,u)=>s+v*(q[u]*matrix[u][a]+(4-q[u])*matrix[u][b]),0)}
function agg(rows){return [0,1,2].map(u=>A.map(a=>rows.reduce((s,r)=>s+r.r[u][a],0)))}
function choose(matrix,cands,robust=false){let best=null,v=Infinity,n=Infinity;for(let p of cands){let nominal=weighted(matrix,nom,1,p),value=robust?Math.max(...verts.map(w=>weighted(matrix,w,1,p))):nominal;if(value<v||(value===v&&nominal<n)){best=p;v=value;n=nominal}}assert(best!==null,"feasible");return best}
const baseline=new Map([...geo].map(([k,r])=>[k,choose(agg(r),A.map(a=>[a,a]))]));
const names=["geometry","prefix_mean","prefix_robust","hint_mean","hint_robust","hint_guard","prefix_guard"],fits=new Map();
for(let [key,g] of prefix){if(new Set(g.map(r=>r.seed)).size<4)continue;let base=baseline.get(g[0].geo)[0],matrix=agg(g),allowed=A.filter(a=>g.every(r=>r.c.every(row=>row[a]<=row[base])));assert(allowed.includes(base),"base");let single=A.map(a=>[a,a]),guard=allowed.map(a=>[a,a]),guardPairs=allowed.flatMap(a=>allowed.map(b=>[a,b]));
fits.set(key,[baseline.get(g[0].geo),choose(matrix,single),choose(matrix,single,true),choose(matrix,pairs),choose(matrix,pairs,true),choose(matrix,guardPairs),choose(matrix,guard)])}
function evaluate(data,w,err){let s=Object.fromEntries(names.map(n=>[n,{groups:data.length,support:0,J:0,regret:0,worst:0,changed:0,harm:0,benefit:0,delta:0,maxHarm:0}]));
for(let r of data){let base=baseline.get(r.geo),opts=fits.get(r.key)??names.map(()=>base);for(let [i,n] of names.entries()){let v=s[n],p=opts[i],q=[4-err,err,err],d=0;v.support+=+(i===0||fits.has(r.key));for(let u=0;u<3;u++)for(let h=0;h<2;h++){let weight=w[u]*(h===0?q[u]:4-q[u]);if(!weight)continue;let a=p[h],b=base[0],cost=r.c[u][a],ex=cost-r.c[u][b];v.J+=weight*cost;d+=weight*r.r[u][a];v.changed+=weight*(a!==b);v.harm+=weight*(ex>0);v.benefit+=weight*(ex<0);v.delta+=weight*ex;v.maxHarm=Math.max(v.maxHarm,ex)}v.regret+=d;v.worst=Math.max(v.worst,d)}}return s}
const gate=(s,n)=>{let v=s[n],b=s.geometry;return v.J<=b.J&&v.worst<=b.worst&&v.harm*20<=v.groups*24&&v.harm*5<=v.changed};
const ca=priors.map(w=>({w,err:1,stats:evaluate(cal,w,1)})),rank=names.slice(1).map(n=>({n,gain:-ca.reduce((s,r)=>s+r.stats[n].delta,0),pass:ca.every(r=>gate(r.stats,n))})).filter(x=>x.pass&&x.gain>0).sort((a,b)=>b.gain-a.gain||names.indexOf(a.n)-names.indexOf(b.n)),selected=rank[0]?.n??"geometry";
const final=rows(Array.from({length:20},(_,i)=>500+i)),results=[];for(let w of priors)for(let err=0;err<4;err++){let stats=evaluate(final,w,err);results.push({w,err,stats,pass:gate(stats,selected)})}for(let w of pure){let stats=evaluate(final,w,1);results.push({w,err:1,stats,pass:gate(stats,selected)})}
assert(arms===33696,"denom");return {status:"EXECUTED_SYNTHETIC_TRAIN_ONLY_HINT",arms,train:train.length,calibration:cal.length,final:final.length,denominator:24,trainingKeys:prefix.size,supportedKeys:fits.size,selected,rank,ca,results};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};

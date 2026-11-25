// Offline abstract finite decision-cost analysis.
function run(){
 const assert=(x,m)=>{if(!x)throw Error(m)}, pol=[3,4,5].flatMap(g=>[0,2,4,6].map(o=>[g,o]));
 function labels(seed,left){let a=Array.from({length:24},(_,i)=>i),x=seed+1;for(let i=23;i>0;i--){x=(Math.imul(1664525,x)+1013904223)>>>0;let j=x%(i+1);[a[i],a[j]]=[a[j],a[i]]}return a.map(v=>v<left?"L":"S")}
 function tick(s,t,g,o,P,R,v){let gs=t%8<g,ds=(t+o)%8<4,x=+(gs&&s.q[0]==="S"&&s.r<R),a=+(s.q[0]==="L"&&s.p<P),y=+(!gs&&s.p>0),z=+(ds&&s.r>0);if(x||a)s.q.shift();s.p+=a-y;s.r+=x-z;s.Y+=y;s.Z+=z;if(v){s.q.push(v);s.A++}let stock=s.q.length+s.p+s.r;assert(stock+s.Y+s.Z===s.A&&s.p>=0&&s.p<=P&&s.r>=0&&s.r<=R,"mass");s.J+=stock}
 const priors=[];for(let i=0;i<=6;i++)for(let j=0;j<=6-i;j++)priors.push([i,j,6-i-j]);
 const modes=["none","binary","noisy"],nom=[2,2,2],verts=[[4,1,1],[1,4,1],[1,1,4]],test=[nom,...verts],grid=priors.map(w=>({w,none:0,binary:0,noisy:0,perfect:0}));
 const stat=()=>({sum:0,max:0}),audit=Object.fromEntries(modes.map(m=>[m,Object.fromEntries(["nominal","robust","knownPrior"].map(s=>[s,test.map(stat)]))]));
 const choices=Object.fromEntries(modes.map(m=>[m,{different:0,robustBetter:0,robustTie:0,robustWorse:0}]));
 const actions=Array.from({length:12},(_,i)=>i),pairs=actions.flatMap(a=>actions.map(b=>[a,b]));
 function candidates(m){return m==="none"?actions.map(a=>[a,a]):pairs}
 function risk(r,w,m,[a,b]){let q=m==="binary"?[4,0,0]:m==="noisy"?[3,1,1]:[4,4,4];return w.reduce((s,v,u)=>s+v*(q[u]*r[u][a]+(4-q[u])*r[u][b]),0)}
 function pick(m,r,w){let c=candidates(m),best=c[0],min=risk(r,w,m,best);for(let a of c){let v=risk(r,w,m,a);if(v<min){best=a;min=v}}return {a:best,v:min}}
 function robust(m,r){let c=candidates(m),best=c[0],vmax=Infinity,vnom=Infinity;for(let a of c){let v=Math.max(...verts.map(w=>risk(r,w,m,a))),n=risk(r,nom,m,a);if(v<vmax||(v===vmax&&n<vnom)){best=a;vmax=v;vnom=n}}return {a:best,v:vmax}}
 let arms=0,groups=0,ambiguous=0,witness=null,groupOracle=0;
 for(let seed=460;seed<480;seed++)for(let left of [6,12,18])for(let P of [1,3])for(let R of [1,3]){
   let lab=labels(seed,left),pre={q:[],p:0,r:0,A:0,Y:0,Z:0,J:0};for(let t=0;t<16;t++)tick(pre,t,4,0,P,R,t%4===0?lab[t/4]:"");
   let costs=[[16,4],[16,1],[32,1]].map(([start,stride])=>{let ar=Array(240).fill("");for(let j=0;j<20;j++)ar[start+j*stride]=lab[4+j];return pol.map(([g,o])=>{let s={...pre,q:pre.q.slice()};for(let t=16;t<240;t++)tick(s,t,g,o,P,R,ar[t]);assert(s.A===24&&s.Y+s.Z===24,"clear");arms++;return s.J})});
   let mins=costs.map(c=>Math.min(...c)),r=costs.map((c,i)=>c.map(v=>v-mins[i]));groupOracle+=mins.reduce((a,b)=>a+b,0);groups++;
   let eq=pick("none",r,nom).v;ambiguous+=+(eq>0);
   for(let i=0;i<priors.length;i++){let w=priors[i],a=pick("none",r,w).v,b=pick("binary",r,w).v,c=pick("noisy",r,w).v;assert(0<=b&&b<=c&&c<=a,"information order");if(w.includes(6))assert(a===0&&b===0&&c===0,"vertex");grid[i].none+=a;grid[i].binary+=b;grid[i].noisy+=c;}
   for(let m of modes){let n=pick(m,r,nom),b=robust(m,r),nv=Math.max(...verts.map(w=>risk(r,w,m,n.a)));assert(b.v<=nv,"robust");let z=choices[m];z.different+=+(n.a.join()!==b.a.join());z[b.v<nv?"robustBetter":b.v>nv?"robustWorse":"robustTie"]++;for(let i=0;i<test.length;i++){for(let [kind,v] of [["nominal",risk(r,test[i],m,n.a)],["robust",risk(r,test[i],m,b.a)],["knownPrior",pick(m,r,test[i]).v]]){let s=audit[m][kind][i];s.sum+=v;s.max=Math.max(s.max,v)}}}
   if(!witness&&eq>0){witness={group:{seed,left,P,R},regretMatrix:r,nominal:modes.map(m=>({mode:m,...pick(m,r,nom)})),robust:modes.map(m=>({mode:m,...robust(m,r)}))}}
 }
 assert(arms===8640&&groups===240&&grid.length===28,"denom");
 return {status:"RETROSPECTIVE_SYNTHETIC_SIGNAL_VALUE",arms,groups,ambiguous,groupOracle,denominator:24,grid,test,audit,choices,witness};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};

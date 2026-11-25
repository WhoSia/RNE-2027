// Offline matched-prefix synthetic uncertainty diagnostic.
function run(){
 const check=(b,m)=>{if(!b)throw Error(m)},pol=[3,4,5].flatMap(g=>[0,2,4,6].map(o=>[g,o])),names=["sparse","early","late"];
 function labels(seed,left){let a=Array.from({length:24},(_,i)=>i),x=seed+1;for(let i=23;i>0;i--){x=(Math.imul(1664525,x)+1013904223)>>>0;let j=x%(i+1);[a[i],a[j]]=[a[j],a[i]]}return a.map(v=>v<left?"L":"S")}
 function tick(s,t,g,o,P,R,v){let gs=t%8<g,ds=(t+o)%8<4,x=+(gs&&s.q[0]==="S"&&s.r<R),a=+(s.q[0]==="L"&&s.p<P),y=+(!gs&&s.p>0),z=+(ds&&s.r>0);if(x||a)s.q.shift();s.p+=a-y;s.r+=x-z;s.Y+=y;s.Z+=z;if(v){s.q.push(v);s.A++}let stock=s.q.length+s.p+s.r;check(stock+s.Y+s.Z===s.A&&s.p>=0&&s.p<=P&&s.r>=0&&s.r<=R,"mass");s.J+=stock}
 let arms=0,groups=0,ambiguous=0,maxGroup=0,witness=null,meanRegret=0,minimaxRegret=0,oracle=0,meanJ=0,minimaxJ=0,maxMean=0,maxMinimax=0;let byVariant=Object.fromEntries(names.map(n=>[n,{oracle:0,mean:0,minimax:0,meanRegret:0,minimaxRegret:0}]));
 for(let seed=440;seed<460;seed++)for(let left of [6,12,18])for(let P of [1,3])for(let R of [1,3]){
  let lab=labels(seed,left),pre={q:[],p:0,r:0,A:0,Y:0,Z:0,J:0};for(let t=0;t<16;t++)tick(pre,t,4,0,P,R,t%4===0?lab[t/4]:"");
  let costs=names.map(n=>{let ar=Array(240).fill("");for(let j=0;j<20;j++)ar[n==="sparse"?16+4*j:n==="early"?16+j:32+j]=lab[4+j];return pol.map(([g,o])=>{let s={...pre,q:pre.q.slice()};for(let t=16;t<240;t++)tick(s,t,g,o,P,R,ar[t]);check(s.A===24&&s.Y+s.Z===24,"clear");arms++;return s.J})});
  let mins=costs.map(c=>Math.min(...c)),sum=pol.map((_,j)=>costs.reduce((s,c)=>s+c[j],0)),mx=pol.map((_,j)=>Math.max(...costs.map((c,k)=>c[j]-mins[k])));let a=pol.map((_,i)=>i).sort((i,j)=>sum[i]-sum[j]||i-j)[0],b=pol.map((_,i)=>i).sort((i,j)=>mx[i]-mx[j]||sum[i]-sum[j]||i-j)[0],m=mins.reduce((s,v)=>s+v,0),gap=sum[a]-m;groups++;ambiguous+=+(gap>0);oracle+=m;meanJ+=sum[a];minimaxJ+=sum[b];meanRegret+=gap;minimaxRegret+=sum[b]-m;maxMean=Math.max(maxMean,mx[a]);maxMinimax=Math.max(maxMinimax,mx[b]);maxGroup=Math.max(maxGroup,gap);
  if(gap>0&&!witness)witness={seed,left,P,R,prefix:lab.slice(0,4).join(""),state:{q:pre.q.join(""),p:pre.p,r:pre.r},costs,mins,minimumGroupRegret:gap};
  names.forEach((n,k)=>{let s=byVariant[n];s.oracle+=mins[k];s.mean+=costs[k][a];s.minimax+=costs[k][b];s.meanRegret+=costs[k][a]-mins[k];s.minimaxRegret+=costs[k][b]-mins[k]});
 }
 check(arms===8640&&groups===240&&meanJ-oracle===meanRegret&&minimaxJ-oracle===minimaxRegret,"denom");return {status:"SYNTHETIC_MATCHED_PREFIX_RETROSPECTIVE",arms,groups,ambiguous,maxGroup,oracle,meanJ,minimaxJ,meanRegret,minimaxRegret,maxMean,maxMinimax,byVariant,witness};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};

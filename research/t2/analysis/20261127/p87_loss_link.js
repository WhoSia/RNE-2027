// Reproduce: node p87_loss_link.js path/to/P87_RESULT.json
function analyze(data) {
  const rows=data.rows, seeds=[...new Set(rows.map(x=>x.seed))], mean=a=>a.reduce((s,x)=>s+x,0)/a.length, sum=a=>a.reduce((s,x)=>s+x,0), med=a=>{let b=[...a].sort((x,y)=>x-y);return (b[Math.floor((b.length-1)/2)]+b[Math.ceil((b.length-1)/2)])/2};
  const d=x=>x.delta.cost, loss=(x,act)=>act===30?Math.max(d(x),0):Math.max(-d(x),0);
  const checks=[];const check=(name,ok)=>{if(!ok)throw Error(name);checks.push(name)};
  check("192 rows, 16 blocks x12",rows.length===192&&seeds.length===16&&seeds.every(s=>rows.filter(x=>x.seed===s).length===12));
  check("96 matched demand tapes",new Set(rows.map(x=>[x.seed,x.share,x.clock].join("/"))).size===96);
  for(const onset of ["green","red"]){const z=rows.filter(x=>x.onset===onset);check(onset+" source sum/sign",sum(z.map(d))===data.summary[onset].cost_sum&&z.filter(x=>d(x)<0).length===data.summary[onset].cost_lower)}
  const strata=["all","green","red"].map(onset=>{const z=rows.filter(x=>onset==="all"||x.onset===onset), a=z.filter(x=>d(x)<0).map(x=>-d(x)), b=z.filter(x=>d(x)>0).map(d);return {onset,n:z.length,win30:a.length,win60:b.length,ties:z.length-a.length-b.length,wrong60:{sum:sum(a),mean:mean(a),median:med(a),max:Math.max(...a)},wrong30:{sum:sum(b),mean:mean(b),median:med(b),max:Math.max(...b)},meanCostRatio:mean(a)/mean(b)}});
  const rules=[["fixed30",()=>30],["fixed60",()=>60],...["onset","onset_share"].flatMap(key=>["majority","loss"].map(obj=>[key+"_"+obj,(x,train)=>{const z=train.filter(y=>y.onset===x.onset&&(key==="onset"||y.share===x.share));const a=sum(z.map(y=>obj==="majority"?+(d(y)>0):loss(y,30))),b=sum(z.map(y=>obj==="majority"?+(d(y)<0):loss(y,60)));return a<b?30:60}]))];
  const predictions=rules.map(([name,rule])=>({name,rows:rows.map(x=>{const train=rows.filter(y=>y.seed!==x.seed), act=rule(x,train);return {seed:x.seed,onset:x.onset,share:x.share,clock:x.clock,act,regret:loss(x,act),correct:loss(x,act)===0}})}));
  const metrics=predictions.map(p=>({name:p.name,correct:p.rows.filter(x=>x.correct).length,totalRegret:sum(p.rows.map(x=>x.regret)),meanRegret:mean(p.rows.map(x=>x.regret)),maxRegret:Math.max(...p.rows.map(x=>x.regret)),act30:p.rows.filter(x=>x.act===30).length}));
  check("fixed regret exact",metrics[0].totalRegret===strata[0].wrong30.sum&&metrics[1].totalRegret===strata[0].wrong60.sum);
  const base=predictions[0].rows;
  let state=20261127;function rand(n){state=(Math.imul(state,1664525)+1013904223)>>>0;return Math.floor(state/4294967296*n)}
  const interval=a=>{a.sort((x,y)=>x-y);return [a[249],a[9749]]};
  const compare=predictions.slice(1).map(p=>{
    const deltas=p.rows.map((x,i)=>x.regret-base[i].regret);
    const blocks=seeds.map(s=>mean(deltas.filter((_,i)=>rows[i].seed===s)));
    const blockRes=[],rowRes=[];
    for(let i=0;i<10000;i++){let b=0,r=0;for(let j=0;j<blocks.length;j++)b+=blocks[rand(blocks.length)];for(let j=0;j<deltas.length;j++)r+=deltas[rand(deltas.length)];blockRes.push(b/blocks.length);rowRes.push(r/deltas.length)}
    return {name:p.name,comparison:"candidate minus fixed30, vehicle-seconds per arm",delta:mean(deltas),blockInterval:interval(blockRes),naiveRowInterval:interval(rowRes),blocks};
  });
  check("fold predictions count",predictions.every(p=>p.rows.length===192));
  return {status:"RETROSPECTIVE_SIMULATOR_REANALYSIS_NOT_FIELD_VALIDATION",strata,metrics,compare,checks,seedBlocks:seeds.length,bootstrapDraws:10000};
}
const fs=require('fs'); console.log(JSON.stringify(analyze(JSON.parse(fs.readFileSync(process.argv[2],'utf8'))),null,2));

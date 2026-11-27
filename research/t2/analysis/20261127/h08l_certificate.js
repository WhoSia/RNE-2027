/* Run from this directory: node h08l_certificate.js */
const fs=require('node:fs');
function instrument(src,letter){
 const a='rows.push({k:g.k,n:g.n,v:x,m:planSense(g.b,H,depth).m});';
 const b='rows.push({k:g.k,n:g.n,v:x,m:planSense(g.b,H,depth).m,lower:planSense(g.b,H,depth).v});';
 const c='classes.push({';
 if(!src.includes(a)||!src.includes(c))throw Error("instrumentation marker");
 src=src.replace(a,b).replace(c,'classes.push({bounds:Object.fromEntries(["qmdp","depth2","depth3",...(sol.depth4?["depth4"]:[]),"adaptive"].map(p=>[p,{lower:sol[p].rows[i].lower,upper:cost(sol[p].rows[i].v)}])),');
 const end=`console.log(JSON.stringify(h08${letter}(),null,2));`;
 if(!src.includes(end))throw Error("terminal marker");
 return new Function(src.replace(end,`return h08${letter}();`))();
}
function summarize(all){
 const out=[];let checks=0,maxViolation=0;
 for(const [letter,r] of all){
  for(const ctx of r.results){
   const rows=r.classes.filter(x=>x.K.join()===ctx.K.join()&&x.L===ctx.L&&x.schedule.join()===ctx.schedule.join()&&x.innovation===ctx.innovation);
   if(rows.length!==ctx.groups)throw Error("group mismatch");
   const ds=Object.keys(rows[0].bounds);
   const sums=Object.fromEntries(ds.map(p=>[p,{classes:0,worlds:0,meanGap:0,maxGap:0,meanRegret:0}]));
   function le(x,y){checks++;maxViolation=Math.max(maxViolation,x-y);if(x>y+1e-9)throw Error("bound violation "+x+" "+y);}
   for(const row of rows){
    const v=row.bounds.adaptive.upper;le(v,row.bounds.adaptive.lower);le(row.bounds.adaptive.lower,v);
    for(let i=0;i<ds.length;i++){
     let p=ds[i],{lower,upper}=row.bounds[p];le(lower,v);le(v,upper);if(i)le(row.bounds[ds[i-1]].lower,lower);
     let gap=upper-lower,regret=upper-v,s=sums[p];
     if(gap<=1e-9){s.classes++;s.worlds+=row.n;}
     s.meanGap+=row.n*gap/ctx.N;s.meanRegret+=row.n*regret/ctx.N;s.maxGap=Math.max(s.maxGap,gap);
    }
   }
   out.push({letter,K:ctx.K,L:ctx.L,schedule:ctx.schedule,innovation:ctx.innovation,N:ctx.N,groups:ctx.groups,summary:sums});
  }
 }
 return {checks,maxViolation,contexts:out};
}
const files={"i":"h08i_lookahead.js","j":"h08j_lookahead.js","k":"h08k_innovation.js"};
console.log(JSON.stringify(summarize(Object.entries(files).map(([l,p])=>[l,instrument(fs.readFileSync(__dirname+'/'+p,'utf8'),l)])),null,2));

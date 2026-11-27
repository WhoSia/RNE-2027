const fs=require('node:fs');
function exactCert(src,name){
 const old='let rows=start.map(g=>({k:g.k,n:g.n,v:ev(g.b,H),m:plan(g.b,H,depth).m}));';
 const rep='let rows=start.map(g=>({k:g.k,n:g.n,v:ev(g.b,H),m:plan(g.b,H,depth).m,lower:plan(g.b,H,depth).v}));';
 const old2='r[p+"First"]=s.m;'; // exact reference uses row, not r
 const term=`console.log(JSON.stringify(${name}(),null,2));`;
 if(!src.includes(old)||!src.includes('row[p+"First"]=s.m;')||!src.includes(term))throw Error("marker");
 src=src.replace(old,rep).replace('row[p+"First"]=s.m;','row[p+"First"]=s.m;row[p+"Lower"]=s.lower.str();row[p+"Upper"]=s.v.str();');
 return new Function(src.replace(term,`return ${name}();`))();
}
function certify(rows){
 function f(s){return s.split("/").map(BigInt);}
 function cmp(a,b){const [n,d]=f(a),[m,e]=f(b);let z=n*e-m*d;return z<0n?-1:z>0n?1:0;}
 let count=0,cert=0,checks=0,worlds=0;
 const summary=[];
 for(const r of rows){let c=0,w=0,ds=["qmdp","depth2","depth3",...(r.H===6?["depth4"]:[]),"adaptive"];for(const x of r.classes){
  count++;worlds+=x.n;
  for(let i=0;i<ds.length;i++){let p=ds[i];if(cmp(x[p+"Lower"],x.adaptiveUpper)>0||cmp(x.adaptiveUpper,x[p+"Upper"])>0)throw Error("bounds");checks+=2;if(i){if(cmp(x[ds[i-1]+"Lower"],x[p+"Lower"])>0)throw Error("monotonicity");checks++;}}
  if(cmp(x.depth2Lower,x.depth2Upper)===0){c++;w+=x.n;cert++;}
 }summary.push({K:r.K,H:r.H,L:r.L,schedule:r.schedule,innovation:r.innovation,classes:r.classes.length,certified:c,worlds:r.N,certifiedWorlds:w});}
 return{count,cert,checks,worlds,summary};
}
const files=[["h08ij_exact_audit.js","audit"],["h08k_exact_audit.js","auditK"]];
console.log(JSON.stringify(certify(files.flatMap(([p,n])=>exactCert(fs.readFileSync(__dirname+'/'+p,'utf8'),n))),null,2));

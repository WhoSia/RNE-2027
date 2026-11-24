"use strict";
function audit(){
  const fields=["discharge","demand","pocket_block","downstream_block"], worlds=[];
  for(let d=0;d<2;d++)for(let p=0;p<2;p++)for(let b=0;b<2;b++)worlds.push({demand:d,pocket_block:p,downstream_block:b,discharge:Number(d&&!p&&!b),label:d?["free","downstream","pocket","both"][2*p+b]:"no_demand"});
  const dist=(a,b)=>a.reduce((n,v,i)=>n+Number(v!==b[i]),0);
  function readings(code,mode,r){
    const out=[code];
    if(r===0)return out;
    for(let i=0;i<code.length;i++){
      const x=code.slice(); x[i]=mode==="erasure"?"?":1-x[i];out.push(x);
    }
    return out;
  }
  function measure(fs,mode,r,common=false){
    const codes=worlds.map(w=>fs.map(f=>w[f])), labels=worlds.map(w=>w.label);
    const allowed=codes.map(c=>common?[c,...[...new Set(fs)].map(f=>c.map((v,i)=>fs[i]===f?1-v:v))]:readings(c,mode,r));
    const m=new Map();
    allowed.forEach((set,i)=>set.forEach(v=>{const k=v.join(",");if(!m.has(k))m.set(k,new Set());m.get(k).add(labels[i]);}));
    let min=Infinity;
    for(let i=0;i<codes.length;i++)for(let j=i+1;j<codes.length;j++)if(labels[i]!==labels[j])min=Math.min(min,dist(codes[i],codes[j]));
    const unique=[...m.values()].filter(s=>s.size===1).length;
    const guaranteed=allowed.filter(vs=>vs.every(v=>m.get(v.join(",")).size===1)).length;
    const robust=guaranteed===worlds.length;
    if(!common && robust!==(min>(mode==="erasure"?r:2*r)))throw Error("distance theorem disagreement");
    return {fields:fs,mode,r,common_mode:common,min_cross_label_distance:min,reachable_readings:m.size,unique_label_readings:unique,guaranteed_worlds:guaranteed,robust};
  }
  const subsets=[];
  for(let mask=0;mask<16;mask++){
    const fs=fields.filter((_,i)=>(mask>>i)&1);
    for(const [mode,r] of [["flip",0],["flip",1],["erasure",1]])subsets.push(measure(fs,mode,r));
  }
  const replicas=[];
  for(let n=1;n<=3;n++){
    const fs=["demand","pocket_block","downstream_block"].flatMap(f=>Array(n).fill(f));
    replicas.push(measure(fs,"flip",1),measure(fs,"erasure",1),measure(fs,"flip",1,true));
  }
  return {status:"P149_EXACT_FINITE_CODE_BENCHMARK_NOT_SENSOR_DATA",worlds:worlds.length,subsets,replicas};
}
if (typeof require!=="undefined" && require.main===module) console.log(JSON.stringify(audit(),null,2));

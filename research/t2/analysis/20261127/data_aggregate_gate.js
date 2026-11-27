/* Pure aggregate function, source CSV supplied by caller; no network or trajectory records. */
function aggregate(s,window){
 const lines=s.trim().split(/\r?\n/),headers=lines.shift().split(","),[hh,mm]=window.split(":").map(Number),start=Date.parse(`2023-09-24T${window}:00Z`),rows=lines.map(l=>{let [t,...cells]=l.split(",");let sec=(Date.parse(t)-start)/1000;if(!Number.isInteger(sec)||sec<0||sec>=900||cells.length!==headers.length-1||cells.some(x=>!/^\d+$/.test(x)))throw Error("invalid row");return {sec,counts:cells.map(Number),total:cells.reduce((a,x)=>a+Number(x),0)}});
 if(new Set(rows.map(r=>r.sec)).size!==rows.length||rows.some((r,i)=>i&&r.sec<=rows[i-1].sec))throw Error("time order");
 const observed=rows.reduce((a,r)=>a+r.total,0),bins={};
 for(const w of [5,15,60]){const bs=Array.from({length:900/w},()=>({observedSeconds:0,observedCount:0}));for(const r of rows){let b=bs[Math.floor(r.sec/w)];b.observedSeconds++;b.observedCount+=r.total;}if(bs.reduce((a,b)=>a+b.observedCount,0)!==observed)throw Error("conservation");bins[w]={complete:bs.filter(b=>b.observedSeconds===w).length,partial:bs.filter(b=>b.observedSeconds>0&&b.observedSeconds<w).length,empty:bs.filter(b=>b.observedSeconds===0).length,observedSum:observed,counts:bs};}
 const thinning={};for(const k of [2,5,10]){const counts=Array(k).fill(0);rows.forEach((r,i)=>counts[i%k]+=r.total);if(counts.reduce((a,b)=>a+b,0)!==observed)throw Error("thinning conservation");thinning[k]={counts,mean:observed/k,minimum:Math.min(...counts),maximum:Math.max(...counts)};}
 return {window,headers:headers.slice(1),rows:rows.length,missingSeconds:900-rows.length,observedCount:observed,explicitZeroRows:rows.filter(r=>r.total===0).length,first:rows[0].sec,last:rows.at(-1).sec,internalMissing:rows.at(-1).sec-rows[0].sec+1-rows.length,bins,thinning};
}
if(typeof module!=='undefined')module.exports={aggregate};

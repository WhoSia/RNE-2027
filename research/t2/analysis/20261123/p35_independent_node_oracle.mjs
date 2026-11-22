/** Independent Node 22 oracle: exact-microsecond CSV-to-join vs Python P35.
 * No P34 or P35 Python imports and no signal-controller/lane attribution.
 */
import fs from 'node:fs';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';

const [crossingsFile, signalsFile, volumeFile, resultFile] = process.argv.slice(2);
if (![crossingsFile,signalsFile,volumeFile,resultFile].every(Boolean)) {
  throw new Error('usage: node p35_independent_node_oracle.mjs p34_result.json traffic-lights.csv traffic-volume.csv p35_result.json');
}
const want = {
  crossing: 'ea0eaae72afd8e82547a5f0b278765e27a871d86cdabeb34a2e4bf4e0a646c72',
  signals: '95802b0c00f1232572279fed62668dfb484d8ea2303c4d3eb4a88339d41a8f0c',
  volume: '00f6f29b2be6c2fa517077de3b7accbbfc75edddc92332534f00ad6b62312798',
};
for (const [file, key] of [[crossingsFile,'crossing'],[signalsFile,'signals'],[volumeFile,'volume']]) {
  assert.equal(crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex'),want[key]);
}
const crossings=JSON.parse(fs.readFileSync(crossingsFile,'utf8')).crossings;
const output=JSON.parse(fs.readFileSync(resultFile,'utf8'));
assert.equal(crossings.length,17);
function micros(s) {
  const clean=s.replace(' ','T');
  const m=/^(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d)(?:\.(\d{1,6}))?(Z|\+00:00)$/.exec(clean);
  if (!m) throw new Error('unexpected UTC date '+s);
  return BigInt(Date.parse(m[1]+'Z'))*1000n+BigInt((m[2]||'').padEnd(6,'0'));
}
function csv(file) {
  const lines=fs.readFileSync(file,'utf8').trimEnd().split(/\r?\n/);
  const head=lines.shift().split(',');
  return [head, lines.map(l=>Object.fromEntries(l.split(',').map((v,i)=>[head[i],v])))];
}
const [signalHead,signals]=csv(signalsFile);
assert.deepEqual(signalHead,['timestamp','id','state']);
assert.equal(signals.length,26970);
const heads=new Map();
for(const row of signals){
  const id=Number(row.id); if(!heads.has(id)) heads.set(id,[]);
  heads.get(id).push([micros(row.timestamp),Number(row.state)]);
}
assert.equal(heads.size,30);
for(const entries of heads.values()) {
  entries.sort((a,b)=>a[0]<b[0]?-1:a[0]>b[0]?1:0);
  assert.equal(entries.length,899);
}
const sorted=heads.get(1).map(v=>v[0]);
for(const entries of heads.values()) assert.deepEqual(entries.map(v=>v[0]),sorted);
const lowerOrEqual=(arr, t)=>{
  let lo=0, hi=arr.length;
  while(lo<hi){const mid=Math.floor((lo+hi)/2);if(arr[mid]<=t)lo=mid+1;else hi=mid;}
  return lo-1;
};
let nearestFuture=0,nearestAfter=0,insideBracket=0,disagreeEvents=0,disagreePairs=0,gapCrossings=0;
const freshThresholds=[250000n,500000n,1000000n,1500000n,2500000n];
const fresh=new Array(freshThresholds.length).fill(0),ageValues=[];
const gStart=micros('2023-09-24T23:31:44.010Z');
const gEnd=micros('2023-09-24T23:31:46.014Z');
for(const ev of crossings){
  const a=micros(ev.bracket_start_utc),b=micros(ev.bracket_end_utc),t=micros(ev.crossing_time_utc);
  assert(a<=t && t<=b && b-a===50000n);
  const pi=lowerOrEqual(sorted,a), ni=lowerOrEqual(sorted,b)+1, at=lowerOrEqual(sorted,t);
  assert(pi>=0 && ni<sorted.length && at>=0 && at+1<sorted.length);
  const age=b-sorted[pi];ageValues.push(Number(age)/1000000);
  freshThresholds.forEach((th,i)=>{if(age<=th)fresh[i]++});
  const near=(t-sorted[at]<=sorted[at+1]-t)?sorted[at]:sorted[at+1];
  if(near>t)nearestFuture++;
  if(near>b)nearestAfter++;
  if(ni-pi-1>0)insideBracket++;
  if(a<gEnd && b>gStart)gapCrossings++;
  let disagreements=0;
  for(const entries of heads.values()) if(entries[pi][1]!==entries[ni][1]) disagreements++;
  if(disagreements)disagreeEvents++;
  disagreePairs+=disagreements;
}
const [volumeHeader,volume]=csv(volumeFile);
assert.equal(volume.length,893);
const official=[];
for(const row of volume) for(const col of volumeHeader.slice(1)){
  const count=Number(row[col]);
  if(!Number.isSafeInteger(count)||count<0)throw new Error('invalid derived counter');
  for(let k=0;k<count;k++)official.push({arm:col.match(/^(East|West|South|North)/)?.[0],t:micros(row.timestamp)});
}
assert.equal(official.length,17);
function matchArm(arm,windowUs){
 const A=crossings.filter(x=>x.source_arm===arm).map(x=>micros(x.crossing_time_utc)).sort((a,b)=>a<b?-1:1);
 const B=official.filter(x=>x.arm===arm).map(x=>x.t).sort((a,b)=>a<b?-1:1);
 const dp=Array.from({length:A.length+1},()=>Array.from({length:B.length+1},()=>[0,0n]));
 const better=(a,b)=>a[0]>b[0] || (a[0]===b[0] && a[1]<b[1]);
 for(let i=1;i<=A.length;i++)for(let j=1;j<=B.length;j++){
   let best=dp[i-1][j]; if(better(dp[i][j-1],best))best=dp[i][j-1];
   const abs=A[i-1]>B[j-1]?A[i-1]-B[j-1]:B[j-1]-A[i-1];
   if(abs<=windowUs){const v=[dp[i-1][j-1][0]+1,dp[i-1][j-1][1]+abs];if(better(v,best))best=v;}
   dp[i][j]=best;
 }
 return dp[A.length][B.length][0];
}
const windows=[250000n,500000n,750000n,1000000n,1500000n];
const matching=windows.map(w=>['East','West','South','North'].reduce((s,a)=>s+matchArm(a,w),0));
assert.deepEqual(matching,output.matched_tolerance_sensitivity.map(r=>r.matched));
assert.equal(nearestFuture,output.crossings_with_nearest_hindsight_sample_future);
assert.equal(nearestAfter,output.crossings_with_nearest_hindsight_sample_after_bracket);
assert.equal(insideBracket,output.crossing_brackets_containing_signal_sample);
assert.equal(disagreeEvents,output.crossings_with_any_head_discordant_between_sample_bounds);
assert.equal(disagreePairs,output.signal_head_event_pairs_with_discordant_samples);
assert.equal(gapCrossings,output.crossings_overlapping_common_gap);
assert.deepEqual(fresh,freshThresholds.map(t=>output.freshness_at_bracket_end[(Number(t)%1000000===0? (Number(t)/1000000).toFixed(1):String(Number(t)/1000000))].causally_fresh_crossings));
const info={protocol:'P35_INDEPENDENT_NODE_EXACT_MICROSECOND_ORACLE',sources:{event:want.crossing,signals:want.signals,volume:want.volume},
  checks:13,matched:matching,latest_age_fresh:fresh,nearest_future:nearestFuture,nearest_after_bracket:nearestAfter,
  inside_bracket:insideBracket,discordant_events:disagreeEvents,discordant_pairs:disagreePairs,gap_crossings:gapCrossings,
  use:'independent parser and DP matcher; NO signal-to-lane mapping'};
console.log(JSON.stringify(info,null,2));

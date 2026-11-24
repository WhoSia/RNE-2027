// P148 independently expressed integer oracle, no physical calibration.
'use strict';
const assert=require('node:assert/strict');
function advance([e,u,d,z],U,D,a,sink,green) {
  const available=e+a;
  const entry=Math.min(available,2,U-u);
  const discharge=Math.min(d,2,sink);
  const transfer=green ? Math.min(u,2,D-d) : 0;
  const next=[available-entry,u+entry-transfer,d+transfer-discharge,z+discharge];
  assert(next.every(Number.isInteger));
  assert(next.every(x=>x>=0));
  assert(next[1]<=U && next[2]<=D);
  assert.equal(next.reduce((x,y)=>x+y,0),e+u+d+z+a);
  assert(transfer===0 || (green && d<D));
  assert(discharge<=sink && discharge<=d);
  return [next,entry,transfer,discharge];
}
let digest=14695981039346656037n, count=0;
for(let U=1;U<=6;U++)for(let D=1;D<=6;D++)
for(let e=0;e<=3;e++)for(let u=0;u<=U;u++)for(let d=0;d<=D;d++)
for(let a=0;a<=2;a++)for(let sink=0;sink<=2;sink++)for(let g=0;g<=1;g++){
  const [n,i,m,o]=advance([e,u,d,0],U,D,a,sink,g);
  const row=[U,D,e,u,d,a,sink,g,...n,i,m,o].join(',')+'\n';
  for(const byte of Buffer.from(row,'ascii'))digest=BigInt.asUintN(64,(digest^BigInt(byte))*1099511628211n);
  count++;
}
console.log(`invariants,${count},${digest}`);
for(let D=1;D<=6;D++)for(const p of [4,8])for(let phi=0;phi<p;phi++){
  let s=[0,0,0,0],cost=0,denied=0;
  for(let t=0;t<200;t++){
    const g=Number((t+phi)%p<p/2);
    denied+=Number(g&&s[1]>0&&s[2]===D);
    [s]=advance(s,6,D,Number(t<24),t%8<4?2:0,g);
    cost+=s[0]+s[1]+s[2];
  }
  assert.deepEqual(s,[0,0,0,24]);
  console.log(['run',D,p,phi,cost,denied,s[3]].join(','));
}

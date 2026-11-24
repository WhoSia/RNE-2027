// Dimensionless abstract CTM verification, no deployment.
function run(){
 const check=(b,m)=>{if(!b)throw Error(m)},eps=1e-8;
 const fd=k=>Math.min(k,.5*(6-k)),S=k=>Math.min(k,2),R=k=>Math.min(2,.5*(6-k));
 const profiles=[[0,0,0,0],[0,0,4,4],[4,4,0,0],[2,2,2,2]],inputs=["dense","platoon","sparse"],sinks=["open","closed_interval","limited_interval"];
 function input(t,k){return k==="dense"?2*(t<12):k==="platoon"?2*(t<4||(t>=8&&t<12)||(t>=16&&t<20)):1*(t<24)}
 function cap(t,k){return k==="open"?2:k==="closed_interval"?(t>=4&&t<12?0:2):t<16?1:2}
 function sim(N,profile,inp,sink,control=false,ring=false){
  const dx=4/N,dt=dx;let n=Array.from({length:N},(_,i)=>profile[Math.floor(i*4/N)]*dx),ext=0,initial=n.reduce((a,b)=>a+b,0),arr=0,z=0,J=0,peakE=0,peakI=initial,exit={},steps=64/dt;
  if(ring)steps=10;
  check(Math.max(1,.5)*dt/dx<=1,"CFL");
  for(let i=0;i<steps;i++){
   let t=i*dt,prev=ext+n.reduce((a,b)=>a+b,0),send=n.map(x=>dt*S(x/dx)),recv=n.map(x=>dt*R(x/dx)),f=Array(N+1).fill(0);
   for(let j=1;j<N;j++)f[j]=Math.min(send[j-1],recv[j]);
   if(ring)f[0]=f[N]=Math.min(send[N-1],recv[0]);
   else {f[0]=Math.min(ext,recv[0]);f[N]=Math.min(send[N-1],dt*cap(t,sink));}
   n=n.map((v,j)=>v+f[j]-f[j+1]);
   if(!ring){let a=control?0:dt*input(t,inp);arr+=a;ext+=a-f[0];z+=f[N]}
   let stock=n.reduce((a,b)=>a+b,0),total=stock+ext;
   check(n.every(v=>v>=-eps&&v<=6*dx+eps)&&ext>=-eps&&Math.abs(initial+arr-z-total)<eps,"mass");
   if(ring)check(n.every(v=>Math.abs(v-profile[0]*dx)<eps),"uniform equilibrium");
   J+=(prev+total)*dt/2;peakE=Math.max(peakE,ext);peakI=Math.max(peakI,stock);
   if([4,8,12,16,24,32,64].includes(t+dt))exit[t+dt]=z;
  }
  return {J,arr,z,terminal:ext+n.reduce((a,b)=>a+b,0),peakE,peakI,exit};
 }
 let controls=0;for(let N of [4,8,16]){let a=sim(N,profiles[0],"dense","open",true);check(a.J===0&&a.z===0,"empty");controls++;for(let k of [0,1,2,4,6]){sim(N,[k,k,k,k],"dense","open",false,true);controls++}}
 const stats={};let pairs=[],nonclear=0;for(let i=0;i<4;i++)for(let inp of inputs)for(let sink of sinks){let a=[4,8,16].map(N=>sim(N,profiles[i],inp,sink));for(let x of a){check(Math.abs(x.arr-24)<eps,"arrivals");nonclear+=+(x.terminal>eps)}pairs.push({profile:i,input:inp,sink,r:a});}
 for(let j=0;j<3;j++){let a=pairs.map(p=>p.r[j]);stats[[4,8,16][j]]={runs:a.length,J:a.reduce((s,v)=>s+v.J,0),peakE:Math.max(...a.map(v=>v.peakE)),peakI:Math.max(...a.map(v=>v.peakI)),maxTerminal:Math.max(...a.map(v=>v.terminal))}}
 const diffs=[0,1].map(j=>{let d=pairs.map(p=>p.r[j].J-p.r[2].J);return {signed:d.reduce((s,x)=>s+x,0),absolute:d.reduce((s,x)=>s+Math.abs(x),0),maxAbs:Math.max(...d.map(Math.abs)),positive:d.filter(x=>x>eps).length,negative:d.filter(x=>x< -eps).length,tie:d.filter(x=>Math.abs(x)<=eps).length}});
 const snap={open:[0,0,0],ring:[0,0,0],ranges:{},maxGap:0,witness:null};
 for(let a of [0,2,4,6])for(let b of [0,2,4,6])for(let c of [0,2,4,6])for(let d of [0,2,4,6]){let k=[a,b,c,d],mean=(a+b+c+d)/4,hom=fd(mean),flows=k.map((v,i)=>Math.min(S(v),R(k[(i+1)%4]))),open=(flows[0]+flows[1]+flows[2])/3,ring=flows.reduce((s,x)=>s+x,0)/4;
 for(let [name,val] of [["open",open],["ring",ring]])snap[name][val<hom-eps?0:val>hom+eps?2:1]++;
 check(ring<=hom+eps,"Jensen");let r=snap.ranges[mean]??(snap.ranges[mean]={min:ring,max:ring,hom,n:0});r.min=Math.min(r.min,ring);r.max=Math.max(r.max,ring);r.n++;if(hom-ring>snap.maxGap){snap.maxGap=hom-ring;snap.witness={k,mean,hom,ring}}}
 return {status:"JS_ISOLATE_DIMENSIONLESS_CTM",worlds:pairs.length,arms:pairs.length*3,controls,nonclear,stats,diffs,snapshot:snap,pairs};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};

// AGG01 offline statistical closure audit.
function run(){
 const check=(b,m)=>{if(!b)throw Error(m)};
 const clocks=["dense","platoon","sparse"];
 const fresh=()=>({blocks:0,active:0,variable:0,actual:0,indepNumerator:0,indepAbsNumerator:0,minUpper:0,indepPositive:0,indepNegative:0,indepEqual:0,activeActual:0,activeIndepNumerator:0,activeIndepAbsNumerator:0,variableActual:0,variableIndepNumerator:0,variableIndepAbsNumerator:0});
 const out=Object.fromEntries(["all",...clocks].map(k=>[k,fresh()]));
 function tape(seed,left,clock){let x=seed+1,a=Array.from({length:24},(_,i)=>i);for(let i=23;i>0;i--){x=(Math.imul(1664525,x)+1013904223)>>>0;let j=x%(i+1);[a[i],a[j]]=[a[j],a[i]]}return Object.fromEntries(a.map((v,i)=>[clock==="dense"?i:clock==="platoon"?8*Math.floor(i/4)+i%4:4*i,v<left?"L":"S"]));}
 let arms=0;
 for(let seed=140;seed<160;seed++)for(const left of [6,12,18])for(const clock of clocks)for(const P of [1,3])for(const R of [1,3])for(const g of [3,4,5])for(const o of [0,2,4,6]){
  const ar=tape(seed,left,clock),q=[];let p=0,r=0,A=0,Z=0,Y=0,ds=0,bs=0,xs=0;arms++;
  for(let t=0;t<240;t++){const green=t%8<(t<16?4:g),down=(t+(t<16?0:o))%8<4;
   const D=+(q[0]==="S"&&green),B=+(r<R),X=D*B,ad=+(q[0]==="L"&&p<P),ml=+(!green&&p>0),z=+(r>0&&down);
   if(X||ad)q.shift();p+=ad-ml;r+=X-z;Y+=ml;Z+=z;if(ar[t]){q.push(ar[t]);A++}
   check(A===q.length+p+r+Y+Z&&p>=0&&p<=P&&r>=0&&r<=R,"conservation");
   if(t>=16){ds+=D;bs+=B;xs+=X;
    if(t%8===7){const err=ds*bs-8*xs;check(xs<=Math.min(ds,bs),"upper");check(8*xs-ds*bs===-err,"covariance");
     for(const k of ["all",clock]){const a=out[k];a.blocks++;a.actual+=xs;a.indepNumerator+=err;a.indepAbsNumerator+=Math.abs(err);a.minUpper+=Math.min(ds,bs);a[err>0?"indepPositive":err<0?"indepNegative":"indepEqual"]++;if(ds>0){a.active++;a.activeActual+=xs;a.activeIndepNumerator+=err;a.activeIndepAbsNumerator+=Math.abs(err)}if(ds>0&&ds<8&&bs>0&&bs<8){a.variable++;a.variableActual+=xs;a.variableIndepNumerator+=err;a.variableIndepAbsNumerator+=Math.abs(err)}}
     ds=bs=xs=0;
    }
   }
  }check(A===24&&Y+Z===24,"clearance");
 }
 check(arms===8640,"arms");return {status:"EXECUTED_JS_ISOLATE_SYNTHETIC",arms,worlds:720,blockTicks:8,groups:out};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};

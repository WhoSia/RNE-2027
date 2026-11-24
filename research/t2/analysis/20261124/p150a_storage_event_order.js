'use strict';
function experiment(){
  const fail=(v,msg)=>{if(!v)throw Error(msg)};
  const tapes={uniform:t=>Number(t<24),pairs:t=>t<24&&t%2===0?2:0,clustered:t=>t<36&&t%6<2?2:0};
  const rows=[];
  for(const [tape,arrival] of Object.entries(tapes)){
    fail(Array.from({length:200},(_,t)=>arrival(t)).reduce((a,b)=>a+b,0)===24,"tape count");
    for(let D=1;D<=6;D++)for(const p of [4,8])for(let phi=0;phi<p;phi++)for(const reuse of [0,1]){
      let e=0,u=0,d=0,z=0,cost=0,denied=0;
      for(let t=0;t<200;t++){
        const a=arrival(t),g=(t+phi)%p<p/2,sink=t%8<4?2:0;
        const before=e+u+d+z,exit=Math.min(d,sink,2),entry=Math.min(e+a,6-u,2);
        const supply=D-d+reuse*exit,move=g?Math.min(u,supply,2):0;
        denied+=Number(g&&u>0&&supply===0);
        fail(entry<=e+a&&entry<=6-u&&exit<=d&&exit<=sink&&move<=u&&move<=supply&&(g||move===0),"old-stock boundary");
        e+=a-entry;u+=entry-move;d+=move-exit;z+=exit;
        fail(e>=0&&u>=0&&u<=6&&d>=0&&d<=D&&z>=0&&e+u+d+z===before+a,"conservation/capacity");
        cost+=e+u+d;
      }
      fail(z===24&&e+u+d===0,"clearance");
      rows.push({tape,D,p,phi,reuse,cost,denied,z});
    }
  }
  const keyed=new Map(rows.map(r=>[[r.tape,r.D,r.p,r.phi,r.reuse].join(","),r]));
  const get=(t,D,p,ph,r)=>keyed.get([t,D,p,ph,r].join(","));
  const groups=[];let witness=null;
  for(const tape of Object.keys(tapes))for(let D=1;D<=6;D++){
    const s={tape,D,matched:0,cost_lower:0,cost_equal:0,cost_higher:0,strict_reversal:0,tie_created:0,tie_resolved:0,unchanged_sign:0,delta_min:Infinity,delta_max:-Infinity};
    for(const p of [4,8])for(let phi=0;phi<p;phi++){
      const delta=get(tape,D,p,phi,1).cost-get(tape,D,p,phi,0).cost;
      s.matched++;s[delta<0?"cost_lower":delta>0?"cost_higher":"cost_equal"]++;
      s.delta_min=Math.min(s.delta_min,delta);s.delta_max=Math.max(s.delta_max,delta);
    }
    for(let a=0;a<4;a++)for(let b=0;b<8;b++){
      const x=get(tape,D,4,a,0).cost-get(tape,D,8,b,0).cost;
      const y=get(tape,D,4,a,1).cost-get(tape,D,8,b,1).cost;
      if(x*y<0){s.strict_reversal++;if(!witness)witness={tape,D,phi4:a,phi8:b,old_delta:x,reuse_delta:y,arms:[get(tape,D,4,a,0),get(tape,D,8,b,0),get(tape,D,4,a,1),get(tape,D,8,b,1)]};}
      else if(x!==0&&y===0)s.tie_created++;
      else if(x===0&&y!==0)s.tie_resolved++;
      else s.unchanged_sign++;
    }
    fail(s.strict_reversal+s.tie_created+s.tie_resolved+s.unchanged_sign===32,"pair count");
    groups.push(s);
  }
  fail(rows.length===432&&keyed.size===432,"arms");
  const totals={};
  for(const key of ["matched","cost_lower","cost_equal","cost_higher","strict_reversal","tie_created","tie_resolved","unchanged_sign"])totals[key]=groups.reduce((a,g)=>a+g[key],0);
  fail(totals.matched===216&&totals.strict_reversal+totals.tie_created+totals.tie_resolved+totals.unchanged_sign===576,"totals");
  return {status:"P150A_SYNTHETIC_EVENT_ORDER_SENSITIVITY",arms:rows.length,totals,groups,witness,rows};
}
if (typeof require !== 'undefined' && require.main === module) console.log(JSON.stringify(experiment(),null,2));

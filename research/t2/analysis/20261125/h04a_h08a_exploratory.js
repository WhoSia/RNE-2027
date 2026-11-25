/* Exploratory H04A/H08A finite toy audit, not field evidence. Run: node h04a_h08a_exploratory.js */
function experiment(){
  const flux=x=>x.slice(0,-1).reduce((s,v,i)=>s+Math.min(v,3,6-x[i+1]),0)/3;
  const states=[];for(let a=0;a<=6;a++)for(let b=0;b<=6;b++)for(let c=0;c<=6;c++)for(let d=0;d<=6;d++)states.push([a,b,c,d]);
  const masks=Array.from({length:16},(_,i)=>Array.from({length:4},(_,j)=>i>>j&1?1:-1));
  const H04=[];
  for(const mode of ["local","common"])for(const err of [0,1,2,4,8]){
    const rows=[], tables=new Map(),base=new Map();
    const add=(m,k,x,f)=>{let a=m.get(k);if(!a){a={n:0,x:[0,0,0,0],f:0};m.set(k,a);}a.n++;for(let j=0;j<4;j++)a.x[j]+=x[j];a.f+=f;};
    for(const x of states)for(const mask of (mode==="local"?masks:[[-1,-1,-1,-1],[1,1,1,1]])){
      const y=x.map((v,j)=>Math.max(0,Math.min(6,v+mask[j]))), M=x.reduce((a,b)=>a+b,0), f=flux(x), k=y.join(",");
      for(const e of err===0?[0]:[-err,err]){const z=M+e,key=k+"|"+z;rows.push({x,y,z,f,k,key});add(tables,key,x,f);add(base,k,x,f);}
    }
    const out={raw:0,baseDirect:0,anchorDirect:0,anchorPlugin:0,naiveShift:0,baseState:0,anchorState:0};
    let worse=0;
    for(const {x,y,z,f,k,key} of rows){
      const a=tables.get(key),b=base.get(k), ax=a.x.map(v=>v/a.n), bx=b.x.map(v=>v/b.n);
      const shift=(z-y.reduce((s,v)=>s+v,0))/4, naive=y.map(v=>Math.max(0,Math.min(6,v+shift)));
      const sq=v=>v*v;
      out.raw+=sq(flux(y)-f);out.baseDirect+=sq(b.f/b.n-f);out.anchorDirect+=sq(a.f/a.n-f);out.anchorPlugin+=sq(flux(ax)-f);out.naiveShift+=sq(flux(naive)-f);
      out.baseState+=x.reduce((s,v,j)=>s+sq(v-bx[j]),0)/4;out.anchorState+=x.reduce((s,v,j)=>s+sq(v-ax[j]),0)/4;
      if(sq(a.f/a.n-f)>sq(b.f/b.n-f)+1e-12)worse++;
    }
    for(const k of Object.keys(out))out[k]/=rows.length;
    if(out.anchorDirect>out.baseDirect+1e-10||out.anchorDirect>out.anchorPlugin+1e-10||out.anchorState>out.baseState+1e-10)throw Error("conditional optimum");
    H04.push({mode,err,rows:rows.length,groups:tables.size,worse,...out});
  }
  const W=[], objectives=["total","max","left"], actions=[0,1,2,3,4];
  for(let s=0;s<=4;s++)for(let l=0;l<=4;l++)for(let ds=0;ds<=4;ds++)for(let dl=0;dl<=4;dl++){
    const values=objectives.map(o=>actions.map(a=>{const rs=s-Math.min(s,ds,a),rl=l-Math.min(l,dl,4-a);return o==="total"?rs+rl:o==="max"?Math.max(rs,rl):rl;}));
    const masks=values.map(v=>v.reduce((m,c,i)=>m|(c===Math.min(...v)?1<<i:0),0));
    const cause=(s>ds?1:0)|(l>dl?2:0);
    W.push({s,l,ds,dl,cause,values,masks});
  }
  const reps={total:w=>[w.s+w.l],queue:w=>[w.s,w.l],queueCause:w=>[w.s,w.l,w.cause],queueTotalSupply:w=>[w.s,w.l,w.ds+w.dl],effectiveDemand:w=>[Math.min(w.s,w.ds),Math.min(w.l,w.dl)],effectiveDemandQueue:w=>[w.s,w.l,Math.min(w.s,w.ds),Math.min(w.l,w.dl)],full:w=>[w.s,w.l,w.ds,w.dl]};
  const H08=[];
  for(const [name,fn] of Object.entries(reps)){
    const G=new Map();for(const w of W){const k=fn(w).join(",");if(!G.has(k))G.set(k,[]);G.get(k).push(w);}
    let all=0,causePure=0, pairwiseOnly=0;const per=objectives.map(()=>({badGroups:0,badStates:0,bayesRegret:0,worstRegret:0}));let witness=null;
    for(const [k,g] of G){
      if(new Set(g.map(w=>w.cause)).size===1)causePure+=g.length;
      let ok=true;
      for(let o=0;o<objectives.length;o++){
        const common=g.reduce((m,w)=>m&w.masks[o],31);
        if(!common){ok=false;per[o].badGroups++;per[o].badStates+=g.length;
          if(g.every(w=>g.every(v=>w.masks[o]&v.masks[o])))pairwiseOnly++;
        }
        const reg=actions.map(a=>g.map(w=>w.values[o][a]-Math.min(...w.values[o])));
        per[o].bayesRegret+=Math.min(...reg.map(r=>r.reduce((s,v)=>s+v,0)));
        per[o].worstRegret=Math.max(per[o].worstRegret,Math.min(...reg.map(r=>Math.max(...r))));
      }
      if(ok)all+=g.length;
      if(!witness && g.reduce((m,w)=>m&w.masks[0],31) && !g.reduce((m,w)=>m&w.masks[1],31)){
        let pair=null;for(const a of g)for(const b of g)if(!(a.masks[1]&b.masks[1]))pair=[a,b];
        if(pair)witness={key:k,pair};
      }
    }
    for(const p of per)p.bayesRegret/=W.length;
    H08.push({name,groups:G.size,causePure,all,pairwiseOnly,per,witness});
  }
  return {H04,H08,stateCount:W.length,objectives};
}
console.log(JSON.stringify(experiment(),null,2));

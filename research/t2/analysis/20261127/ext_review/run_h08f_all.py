import sys,json,time
from ext_h08f import *
GEOS=[(2,2),(2,1),(1,2),(3,2),(2,3)]
POL=('free','head_if','full_if','adaptive','adaptive_full','adaptive_eq','qmdp')
Ls=[int(a) for a in sys.argv[1:]] or [4]
res=[]
for L in Ls:
    for g in GEOS:
        t=time.time(); C=Ctx(g,L); row=dict(caps=g,L=L,nworlds=len(C.support)); cvs={}
        for p in POL:
            cvs[p]=C.evaluate(p); v=summarize(cvs[p])
            row[p]=dict(obj=float(obj(v)),traffic=float(v[0]),sens=float(v[1]),head=float(v[2]),full=float(v[3]),exact=[str(x) for x in v])
        N=row['nworlds']; gains=[]
        for k,(n,fv) in cvs['free'].items():
            av=cvs['adaptive'][k][1]; gains.append((k,n,obj(fv)-obj(av)))
        tot=sum(Q(n,N)*gn for k,n,gn in gains); row['gain_total']=float(tot)
        row['neg_classes']=sum(1 for k,n,gn in gains if gn<0)
        row['pos_classes']=sum(1 for k,n,gn in gains if gn>0); row['nclasses']=len(gains)
        row['max_class_gain']=float(max(gn for k,n,gn in gains))
        def share(pred): 
            s=sum(Q(n,N)*gn for k,n,gn in gains if pred(k,g)); return float(s/tot) if tot else None
        row['share_both_full']=share(lambda k,g:k[0]==g[0] and k[1]==g[1])
        row['share_equal_abs']=share(lambda k,g:k[0]==k[1])
        row['share_equal_rel']=share(lambda k,g:Q(k[0],g[0])==Q(k[1],g[1]))
        row['share_mixed_queue']=share(lambda k,g:k[2]>0 and k[3]>0)
        row['weight_both_full']=float(sum(Q(n,N) for k,n,_ in gains if k[0]==g[0] and k[1]==g[1]))
        row['secs']=round(time.time()-t,1); res.append(row)
        print(g,L,'free',round(row['free']['obj'],6),'head_if',round(row['head_if']['obj'],6),'adapt',round(row['adaptive']['obj'],6),'qmdp',round(row['qmdp']['obj'],6),'gain',round(row['gain_total'],6),'sharefull',row['share_both_full'],'secs',row['secs'],flush=True)
json.dump(res,open('ext_h08f_L%s.json'%'_'.join(map(str,Ls)),'w'),indent=1)

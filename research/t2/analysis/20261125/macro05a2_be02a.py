"""Dimensionless offline spatial conservation experiment; no real road control."""
from itertools import product
import json
EPS=1e-7

def sim(inp,share,b,s,relaxed=False):
    n=[[0.,0.] for _ in range(10)]; ext=[0.,0.]; a=[0.,0.]; z=[0.,0.]; J=[0.,0.]; correction=0.;blocked=0.
    for t in range(128):
        stock=list(map(sum,n)); send=[min(v,2.) for v in stock]; recv=[min(2.,max(0.,(6-v)/2)) for v in stock]
        delta=[[0.,0.] for _ in n]; ed=[0.,0.]; exitflow=[0.,0.]
        def flow(src,dst,mass):
            srcstock=ext if src==-1 else n[src];total=sum(srcstock)
            assert -EPS<=mass<=total+EPS
            if total<=0:return
            for k in range(2):
                f=(srcstock[k]/total)*mass
                if src==-1:ed[k]-=f
                else:delta[src][k]-=f
                if dst==-1:exitflow[k]+=f
                else:delta[dst][k]+=f
        flow(-1,0,min(sum(ext),recv[0]))
        for i,j in ((0,1),(2,3),(4,5),(5,6),(6,7),(8,9)):flow(i,j,min(send[i],recv[j]))
        demands=[send[1]*(v/stock[1]) if stock[1]>0 else 0. for v in n[1]]
        bound=[recv[2],recv[4]];scale=min([1.]+[r/d for d,r in zip(demands,bound) if d>0]);f=[min(d,r) if relaxed else d*scale for d,r in zip(demands,bound)]
        assert sum(f)<=send[1]+EPS and all(v<=r+EPS for v,r in zip(f,bound))
        for k,dst in enumerate((2,4)):delta[1][k]-=f[k];delta[dst][k]+=f[k]
        blocked+=sum(demands)-sum(f)
        ca=.25 if b==1 and 4<=t<16 else .5 if b==2 and 8<=t<24 else 2.
        da,db=min(send[3],ca),send[7];factor=min(1.,recv[8]/(da+db)) if da+db>0 else 0.
        flow(3,8,da*factor);flow(7,8,db*factor)
        cap=0. if s==1 and 8<=t<16 else 1. if s==2 and t<24 else 2.
        flow(9,-1,min(send[9],cap))
        rate=(2*(t<12),2*(t<4 or 8<=t<12 or 16<=t<20),int(t<24))[inp]
        incoming=[rate*share,rate*(1-share)]
        n=[[v+d for v,d in zip(row,drow)] for row,drow in zip(n,delta)]
        ext=[ext[k]+ed[k]+incoming[k] for k in range(2)]
        for k in range(2):a[k]+=incoming[k];z[k]+=exitflow[k]
        for row in [ext]+n:
            for k,v in enumerate(row):
                assert v>=-1e-10
                if v<0:correction-=v;row[k]=0.
        assert all(sum(row)<=6+EPS for row in n)
        assert all(abs(n[i][1])<EPS for i in (2,3)) and all(abs(n[i][0])<EPS for i in (4,5,6,7))
        for k in range(2):
            total=ext[k]+sum(row[k] for row in n);assert abs(total+z[k]-a[k])<EPS;J[k]+=total
    assert abs(sum(a)-24)<EPS and sum(ext)+sum(map(sum,n))<EPS and correction<1e-9
    return dict(J=sum(J),JA=J[0],JB=J[1],blocked=blocked,correction=correction)

def run():
    audit={'fifo':[0.,0.,0.],'relaxed':[0.,0.,0.],'counts':[0,0,0],'maxCorrection':0.,'adverse':[]}
    for inp,share,b,s in product(range(3),(.25,.5,.75),range(3),range(3)):
        a,c=sim(inp,share,b,s),sim(inp,share,b,s,True)
        for name,r in [('fifo',a),('relaxed',c)]:
            for k,f in enumerate(('J','JA','JB')):audit[name][k]+=r[f]
            audit['maxCorrection']=max(audit['maxCorrection'],r['correction'])
        d=c['J']-a['J'];audit['counts'][0 if d<-EPS else 2 if d>EPS else 1]+=1
        if d>EPS:audit['adverse'].append({'context':[inp,share,b,s],'fifo':a,'relaxed':c,'delta':d})
    expected={'fifo':[20860.47815954347,10254.076043037001,10606.402116506464],'relaxed':[20852.844324698395,10267.495336923583,10585.348987774812]}
    for k in expected:assert all(abs(a-b)<1e-6 for a,b in zip(audit[k],expected[k]))
    assert audit['counts']==[3,77,1]
    rows=[]
    for inp,b,s in product(range(3),repeat=3):
        curve=[]
        for i in range(1,20):
            share=i/20;v=sim(inp,share,b,s);ca=v['JA']/(24*share);cb=v['JB']/(24*(1-share));curve.append(dict(share=share,J=v['J'],ca=ca,cb=cb,gap=abs(ca-cb)))
        opt=next(x for x in curve if x['J']<=min(y['J'] for y in curve)+EPS);near=next(x for x in curve if x['gap']<=min(y['gap'] for y in curve)+EPS)
        rows.append(dict(context=[inp,b,s],opt=opt,near=near,delta=near['J']-opt['J'],minCost=min(x['J'] for x in curve),maxCost=max(x['J'] for x in curve),curve=curve))
    return dict(audit=audit,landscape=dict(worlds=len(rows),arms=len(rows)*19,optJ=sum(r['opt']['J'] for r in rows),nearJ=sum(r['near']['J'] for r in rows),strict=sum(r['delta']>EPS for r in rows),nearContexts=sum(r['near']['gap']<=.1 for r in rows),nearStrict=sum(r['near']['gap']<=.1 and r['delta']>EPS for r in rows),maxGap=max(r['delta'] for r in rows),maxWitness=max(rows,key=lambda r:r['delta']),rows=rows))
if __name__=='__main__': print(json.dumps(run(),indent=2))

from itertools import product
import json

def sim(N,profile,inp,sink):
    dx=4/N;dt=dx;n=[profile[i*4//N]*dx for i in range(N)]
    initial=sum(n);ext=A=Z=J=0.
    for step in range(int(64/dt)):
        t=step*dt;old=ext+sum(n)
        send=[dt*min(x/dx,2) for x in n]
        recv=[dt*min(2,(6-x/dx)/2) for x in n]
        rate=(2*(t<12),2*(t<4 or 8<=t<12 or 16<=t<20),1*(t<24))[inp]
        cap=(2,0 if 4<=t<12 else 2,1 if t<16 else 2)[sink]
        flows=[min(ext,recv[0])]+[min(send[i],recv[i+1]) for i in range(N-1)]+[min(send[-1],dt*cap)]
        n=[v+flows[i]-flows[i+1] for i,v in enumerate(n)]
        A+=dt*rate;ext+=dt*rate-flows[0];Z+=flows[-1];stock=ext+sum(n)
        assert min(n)>=-1e-8 and max(n)<=6*dx+1e-8 and ext>=-1e-8
        assert abs(initial+A-Z-stock)<1e-8
        J+=dt*(old+stock)/2
    assert abs(A-24)<1e-8 and stock<1e-8
    return J

def run():
    profiles=((0,0,0,0),(0,0,4,4),(4,4,0,0),(2,2,2,2))
    costs=[[sim(N,p,i,s) for N in (4,8,16)] for p,i,s in product(profiles,range(3),range(3))]
    totals=[sum(a[j] for a in costs) for j in range(3)]
    diffs=[[a[j]-a[2] for a in costs] for j in range(2)]
    snap=[[0,0,0],[0,0,0]]
    for k in product((0,2,4,6),repeat=4):
        m=sum(k)/4;hom=min(m,(6-m)/2)
        f=[min(k[i],2,(6-k[(i+1)%4])/2) for i in range(4)]
        for j,val in enumerate((sum(f[:3])/3,sum(f)/4)):
            d=val-hom;snap[j][0 if d<-1e-8 else 2 if d>1e-8 else 1]+=1
        assert sum(f)/4<=hom+1e-8
    return dict(totals=totals,diffs=[dict(signed=sum(d),absolute=sum(map(abs,d)),maxAbs=max(map(abs,d)),positive=sum(x>1e-8 for x in d),negative=sum(x< -1e-8 for x in d),tie=sum(abs(x)<=1e-8 for x in d)) for d in diffs],snap=snap)
if __name__=='__main__':print(json.dumps(run(),indent=2))

"""DLR K047 StVO-294 lane-validity crossing audit (standard-library-only).

Read the original 20 Hz CSV and original OpenDRIVE locally. This outputs *candidate*
road-reference-line center crossings, NOT human-verified stopline truth.
"""
import argparse,csv,math,xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime
def reference_xy(road,s):
    geoms=[g for g in road.findall("./planView/geometry") if float(g.get("s"))<=s+1e-8]
    if not geoms:raise ValueError("no matching OpenDRIVE geometry")
    g=max(geoms,key=lambda z:float(z.get("s")))
    ds=s-float(g.get("s"))
    if ds<-1e-7 or ds>float(g.get("length"))+1e-5:raise ValueError("out of geometry bounds")
    x,y,heading=(float(g.get(k)) for k in ("x","y","hdg"))
    if g.find("line") is not None:return x+ds*math.cos(heading),y+ds*math.sin(heading)
    arc=g.find("arc")
    if arc is None:raise ValueError("unsupported geometry (spiral/poly3)")
    curvature=float(arc.get("curvature"))
    if abs(curvature)<1e-12:return x+ds*math.cos(heading),y+ds*math.sin(heading)
    angle=curvature*ds
    return (x+2*math.sin(angle/2)/curvature*math.cos(heading+angle/2),
            y+2*math.sin(angle/2)/curvature*math.sin(heading+angle/2))


def poly(node,u):
    return sum(float(node.get(k,"0"))*u**j for j,k in enumerate("abcd"))

def lane_ranges(road,s):
    ss=[x for x in road.findall("./lanes/laneSection") if float(x.get("s"))<=s+1e-7]
    section=max(ss,key=lambda x:float(x.get("s")))
    local=s-float(section.get("s"))
    offsets=[x for x in road.findall("./lanes/laneOffset") if float(x.get("s"))<=s+1e-7]
    offset=poly(max(offsets,key=lambda x:float(x.get("s"))),s-float(max(offsets,key=lambda x:float(x.get("s"))).get("s"))) if offsets else 0.0
    out={}
    for sign,side in [(-1,"right"),(1,"left")]:
        total=0.
        for lane in sorted(section.findall(f"./{side}/lane"),key=lambda x:abs(int(x.get("id")))):
            widths=[w for w in lane.findall("./width") if float(w.get("sOffset"))<=local+1e-7]
            if not widths: continue
            w=max(widths,key=lambda x:float(x.get("sOffset")))
            size=poly(w,local-float(w.get("sOffset")))
            if size<0:raise ValueError("negative lane width")
            lo,hi=sorted((offset+sign*total,offset+sign*(total+size)))
            out[int(lane.get("id"))]=(lo,hi,lane.get("type"))
            total+=size
    return out

def sites(xodr):
    root=ET.parse(xodr).getroot()
    out=[]
    for road in root.findall("./road"):
        succ=road.find("./link/successor")
        if road.get("junction")!="-1" or succ is None or succ.get("elementType")!="junction":continue
        for signal in road.findall("./signals/signal"):
            if signal.get("type")!="294" or signal.get("dynamic")!="no":continue
            s=float(signal.get("s"));x,y=reference_xy(road,s)
            px,py=reference_xy(road,s-.05)
            dx,dy=x-px,y-py;norm=math.hypot(dx,dy)
            if not norm:raise ValueError("zero tangent")
            dx/=norm;dy/=norm
            envelopes=lane_ranges(road,s)
            allowed=[]
            for item in signal.findall("./laneValidity"):
                a,b=int(item.get("fromLane")),int(item.get("toLane"))
                for j in range(min(a,b),max(a,b)+1):
                    if j in envelopes and envelopes[j][2]=="driving":allowed.append(envelopes[j][:2])
            out.append((road.get("id"),x,y,dx,dy,allowed))
    return out

def audit(xodr,trajectory_csv,gap=.25,prob=.5):
    tracks=defaultdict(list)
    with open(trajectory_csv,encoding="utf-8-sig",newline="") as f:
        for row in csv.DictReader(f):
            t=datetime.fromisoformat(row["timestamp"])
            if t.tzinfo is None:raise ValueError("UTC offset required")
            q=sum(float(row[f"classifications_{k}"]) for k in ("car","van","truck"))
            tracks[row["id"]].append((t,float(row["center_easting"])-604763,
                float(row["center_northing"])-5792795,q))
    out=[]
    for trackid,seq in tracks.items():
        seq.sort()
        for road,x,y,dx,dy,allowed in sites(xodr):
            for a,b in zip(seq,seq[1:]):
                dt=(b[0]-a[0]).total_seconds()
                if not 0<dt<=gap:continue
                before=(a[1]-x)*dx+(a[2]-y)*dy
                after=(b[1]-x)*dx+(b[2]-y)*dy
                if not before<=0<after:continue
                alpha=-before/(after-before)
                xx=a[1]+alpha*(b[1]-a[1])-x
                yy=a[2]+alpha*(b[2]-a[2])-y
                lateral=-xx*dy+yy*dx
                if abs(lateral)>20:continue
                strict=any(lo-1e-6<=lateral<=hi+1e-6 for lo,hi in allowed)
                is_vehicle=max(a[3],b[3])>=prob
                when=a[0]+(b[0]-a[0])*alpha
                out.append(dict(road_id=road,track_id=trackid,time_utc=when.isoformat(),
                    lateral_m=round(lateral,3),lane_validity_pass=strict,vehicle_pass=is_vehicle))
    return sorted(out,key=lambda v:v["time_utc"])

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--xodr",required=True)
    p.add_argument("--trajectories",required=True)
    p.add_argument("--output",required=True)
    args=p.parse_args()
    events=audit(args.xodr,args.trajectories)
    with open(args.output,"w",newline="",encoding="utf8") as f:
        w=csv.DictWriter(f,fieldnames=["road_id","track_id","time_utc","lateral_m","lane_validity_pass","vehicle_pass"])
        w.writeheader();w.writerows(events)
    print("wide",len(events),"lane-valid candidate",sum(e["lane_validity_pass"] and e["vehicle_pass"] for e in events))

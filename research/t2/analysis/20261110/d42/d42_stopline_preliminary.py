"""DLR UT preliminary reference-plane crossing detector; NOT lane counts."""
import csv,math,sys,xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime

def reference_pose(road,s):
    matches=[g for g in road.findall('./planView/geometry') if float(g.get('s'))<=s+1e-8]
    if not matches:raise ValueError('s lacks plan geometry')
    g=matches[-1];ds=s-float(g.get('s'))
    if ds < -1e-7 or ds>float(g.get('length'))+1e-6:raise ValueError('s exceeds geometry')
    x,y,h=[float(g.get(k)) for k in ('x','y','hdg')]
    child=next((z for z in g if z.tag in ('arc','line')),None)
    if child is None:raise NotImplementedError('line and arc only')
    k=float(child.get('curvature')) if child.tag=='arc' else 0.
    if abs(k)<1e-12:x+=ds*math.cos(h);y+=ds*math.sin(h)
    else:x+=(math.sin(h+k*ds)-math.sin(h))/k;y-=(math.cos(h+k*ds)-math.cos(h))/k
    return x,y,h+k*ds

def candidates(root):
    for road in root.findall('road'):
        for signal in road.findall('./signals/signal'):
            if signal.get('type')!='294':continue
            s=float(signal.get('s'));x,y,h=reference_pose(road,s)
            yield {'road_id':road.get('id'),'signal_id':signal.get('id'),
                   'junction':road.get('junction'),'s':s,'x':x,'y':y,'heading':h}

def transitions(samples,x,y,h,half_width=16.,max_distance=6.,min_speed=1.):
    """Sign changes across infinitely extended normal; invalid as field stopline alone."""
    u,v=math.cos(h),math.sin(h)
    traces=defaultdict(list)
    for tid,t,px,py,vx,vy in samples:
        longitudinal=(px-x)*u+(py-y)*v
        lateral=-(px-x)*v+(py-y)*u
        if abs(longitudinal)<=max_distance and abs(lateral)<=half_width:
            traces[tid].append((t,longitudinal,vx*u+vy*v))
    forward=reverse=0
    for track in traces.values():
        track.sort()
        for a,b in zip(track,track[1:]):
            if not 0<b[0]-a[0]<=.07500001:continue
            if a[1]<=0<b[1] and b[2]>=min_speed:forward+=1
            if a[1]>=0>b[1] and b[2]<=-min_speed:reverse+=1
    return forward,reverse

def scan(csv_path,xodr_path,output_path):
    traces=[]
    with open(csv_path,encoding='utf8',newline='') as f:
        for r in csv.DictReader(f):
            traces.append((r['id'],datetime.fromisoformat(r['timestamp']).timestamp(),
                           float(r['center_easting'])-604763,
                           float(r['center_northing'])-5792795,
                           float(r['velocity_easting']),float(r['velocity_northing'])))
    rows=[]
    for z in candidates(ET.parse(xodr_path).getroot()):
        pos,neg=transitions(traces,z['x'],z['y'],z['heading'])
        rows.append({**z,'candidate_forward':pos,'candidate_reverse':neg,'status':'NOT_LANE_VALIDATED'})
    with open(output_path,'w',encoding='utf8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    return rows

if __name__=='__main__':
    if len(sys.argv)!=4:raise SystemExit('usage: python d42_stopline_preliminary.py trajectory.csv map.xodr out.csv')
    result=scan(*sys.argv[1:])
    print(len(result),sum(z['candidate_forward'] for z in result),sum(z['candidate_reverse'] for z in result))

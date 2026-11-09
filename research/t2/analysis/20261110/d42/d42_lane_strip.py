"""DLR OpenDRIVE lane strip crossing *candidate* detector. Not publisher counts."""
import csv,math,xml.etree.ElementTree as ET,sys
from datetime import datetime
from collections import defaultdict
from d42_stopline_preliminary import reference_pose

def cubic_at(knots,s):
    z=[p for p in knots if float(p.get('sOffset',p.get('s')))<=s+1e-8]
    if not z:return 0.
    p=z[-1];t=s-float(p.get('sOffset',p.get('s')))
    return sum(float(p.get(k,0))*t**i for i,k in enumerate(('a','b','c','d')))

def driving_lane_strips(road,station):
    sections=[s for s in road.findall('./lanes/laneSection') if float(s.get('s'))<=station+1e-8]
    if not sections:raise ValueError('no laneSection')
    sec=sections[-1];ds=station-float(sec.get('s'))
    if road.findall('./lanes/laneOffset'):raise NotImplementedError('laneOffset needs correction')
    out=[]
    for side,sign in [('right',-1),('left',1)]:
        offset=0.
        for lane in sorted(sec.findall('./'+side+'/lane'),key=lambda l:abs(int(l.get('id')))):
            widths=lane.findall('width')
            if not widths:raise NotImplementedError('lane width missing')
            other=offset+sign*cubic_at(widths,ds)
            if lane.get('type')=='driving':out.append((lane.get('id'),min(offset,other),max(offset,other)))
            offset=other
    return out

def scan_lane_crossings(samples,x,y,h,strips,tolerance=.1):
    ca,sa=math.cos(h),math.sin(h);by=defaultdict(list)
    for tid,t,px,py,vx,vy in samples:
        longitudinal=(px-x)*ca+(py-y)*sa
        lateral=-(px-x)*sa+(py-y)*ca
        if abs(longitudinal)<4 and any(lo-.5<=lateral<=hi+.5 for _,lo,hi in strips):
            by[tid].append((t,longitudinal,lateral,vx*ca+vy*sa))
    out=[]
    for tid,trace in by.items():
        trace.sort()
        for a,b in zip(trace,trace[1:]):
            if not (0<b[0]-a[0]<=.07500001) or a[1]*b[1]>0 or a[1]==b[1]:continue
            direction=('forward' if a[1]<=0<b[1] and b[3]>1 else 'reverse' if a[1]>=0>b[1] and b[3]<-1 else None)
            if direction is None:continue
            alpha=abs(a[1])/(abs(a[1])+abs(b[1]))
            lateral=a[2]+(b[2]-a[2])*alpha
            lanes=[lane for lane,lo,hi in strips if lo-tolerance<=lateral<=hi+tolerance]
            if len(lanes)!=1:continue
            out.append((tid,a[0]+alpha*(b[0]-a[0]),direction,lanes[0],lateral))
    return out

def main(raw,mapfile,outfile):
    samples=[]
    with open(raw,newline='',encoding='utf8') as f:
        for row in csv.DictReader(f):
            samples.append((row['id'],datetime.fromisoformat(row['timestamp']).timestamp(),
             float(row['center_easting'])-604763.,float(row['center_northing'])-5792795.,
             float(row['velocity_easting']),float(row['velocity_northing'])))
    records=[]
    for road in ET.parse(mapfile).getroot().findall('road'):
        for sig in road.findall('./signals/signal'):
            if sig.get('type')!='294':continue
            station=float(sig.get('s'));x,y,h=reference_pose(road,station)
            for tid,t,d,lane,lat in scan_lane_crossings(samples,x,y,h,driving_lane_strips(road,station)):
                records.append({'road_id':road.get('id'),'signal_id':sig.get('id'),
                    'track_id':tid,'epoch_s':f'{t:.6f}','direction':d,'lane_id':lane,
                    'lateral_offset_m':f'{lat:.4f}','status':'EXPLORATORY_NOT_PUBLISHER_VALIDATED'})
    with open(outfile,'w',encoding='utf8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['road_id','signal_id','track_id','epoch_s','direction','lane_id','lateral_offset_m','status'])
        w.writeheader();w.writerows(records)
    return records

if __name__=='__main__':
    if len(sys.argv)!=4:raise SystemExit('usage: lane_strip.py trajectories.csv map.xodr out.csv')
    print('unvalidated candidates',len(main(*sys.argv[1:])))

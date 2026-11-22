"""P24 passive road-reference proximity diagnostic: NOT a lane or signal assignment."""
import csv, math, json, xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from scipy.spatial import cKDTree
from pyproj import CRS, Transformer
from p24_dlr_map_join_gate import locked,XODR_SHA,TRAJ_SHA,pdf_vehicle_heads

def run(xodr,pdf,traj):
    r=ET.parse(locked(xodr,XODR_SHA)).getroot()
    pts=[];roads=[]
    for road in r.findall('./road'):
        for seg in road.findall('./planView/geometry'):
            x0=float(seg.get('x'));y0=float(seg.get('y'));h=float(seg.get('hdg'))
            L=float(seg.get('length'))
            shape=seg.find('arc')
            if shape is not None:k=float(shape.get('curvature'))
            elif seg.find('line') is not None:k=0
            else:raise ValueError('unsupported XODR geometry')
            for q in range(max(1,int(math.ceil(L)))):
                t=min(L,q+0.5)
                if k==0:x=x0+t*math.cos(h);y=y0+t*math.sin(h)
                else:
                    x=x0+(math.sin(h+k*t)-math.sin(h))/k
                    y=y0-(math.cos(h+k*t)-math.cos(h))/k
                pts.append((x,y));roads.append(road.get('id'))
    tree=cKDTree(pts)
    proj=Transformer.from_crs(CRS.from_epsg(32632),CRS.from_proj4(r.findtext('./header/geoReference')),always_xy=True)
    with locked(traj,TRAJ_SHA).open(newline='',encoding='utf-8') as f:
        rr=list(csv.DictReader(f))
    xy=[proj.transform(float(x['center_easting']),float(x['center_northing'])) for x in rr]
    d,idx=tree.query(xy)
    heads=[proj.transform(e,n) for _,e,n in pdf_vehicle_heads(pdf)]
    head_d,_=tree.query(heads)
    ds=sorted(float(x) for x in d)
    def q(p):return round(ds[round(p*(len(ds)-1))],3)
    return {'status':'PROXIMITY_DIAGNOSTIC_NOT_LANE_ASSIGNMENT',
        'road_reference_polyline_samples':len(pts),'source_trajectory_centers':len(rr),
        'reference_line_distance_m':{'min':q(0),'median':q(.5),'p90':q(.9),'p95':q(.95),'p99':q(.99),'max':q(1)},
        'fraction_within_10_m':sum(x<=10 for x in d)/len(d),
        'nearest_reference_road_by_sample_counts':dict(Counter(roads[i] for i in idx)),
        'published_head_nearest_reference_line_distances_m':[round(float(x),3) for x in head_d],
        'warning':'Road reference line proximity does not identify a lane, stopline or controlling traffic signal; repeated within-track points are not independent.'}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('map');p.add_argument('pdf');p.add_argument('trajectory');p.add_argument('output')
    x=p.parse_args()
    Path(x.output).write_text(json.dumps(run(x.map,x.pdf,x.trajectory),sort_keys=True,indent=2)+'\n')

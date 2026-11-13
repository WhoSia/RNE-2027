"""Extract OpenDRIVE StVO 294 static stop-line candidates. No dynamic-head mapping."""
from __future__ import annotations
import argparse
import csv
import math
import xml.etree.ElementTree as ET

FIELDS=['road_id','sign_id','type','dynamic','orientation','junction','s_m','end_gap_m','x_ref_m','y_ref_m','active_driving_lanes','lane_validity','classification','warnings']

def reference_xy(road,s):
    geoms=[g for g in road.findall('./planView/geometry') if float(g.get('s')) <= s+1e-8]
    if not geoms:raise ValueError('no geometry at s')
    g=geoms[-1]
    ds=s-float(g.get('s'))
    if ds < -1e-7 or ds > float(g.get('length'))+1e-5:raise ValueError('invalid geometry interval')
    x,y,h=map(float,(g.get('x'),g.get('y'),g.get('hdg')))
    if g.find('line') is not None:return x+ds*math.cos(h),y+ds*math.sin(h)
    arc=g.find('arc')
    if arc is None:raise ValueError('unsupported geometry')
    k=float(arc.get('curvature'))
    if abs(k)<1e-12:return x+ds*math.cos(h),y+ds*math.sin(h)
    return (x+2*math.sin(k*ds/2)/k*math.cos(h+k*ds/2),
            y+2*math.sin(k*ds/2)/k*math.sin(h+k*ds/2))

def at_lane_section(road,s):
    sections=[x for x in road.findall('./lanes/laneSection') if float(x.get('s'))<=s+1e-8]
    if not sections:raise ValueError('missing lane section')
    return {int(l.get('id')):l.get('type') for l in sections[-1].findall('./left/lane')+sections[-1].findall('./right/lane')}

def extract(path):
    root=ET.parse(path).getroot()
    if root.tag!='OpenDRIVE':raise ValueError('unexpected XML root')
    rows=[]
    for road in root.findall('road'):
        rid=road.get('id')
        length=float(road.get('length'))
        junction=road.get('junction')
        successor=road.find('./link/successor')
        incoming=successor is not None and successor.get('elementType')=='junction' and successor.get('elementId')=='300000'
        for sign in road.findall('./signals/signal'):
            if sign.get('type')!='294':continue
            s=float(sign.get('s'))
            if not 0<=s<=length+1e-6:raise ValueError('marking is outside road')
            x,y=reference_xy(road,s)
            lanes=at_lane_section(road,s)
            validity=sign.findall('laneValidity')
            covered=[]
            if len(validity)==1:
                lower=int(validity[0].get('fromLane'));upper=int(validity[0].get('toLane'))
                covered=list(range(min(lower,upper),max(lower,upper)+1))
            cls='approach_endpoint_candidate' if incoming else ('junction_connector_candidate' if junction!='-1' else 'other_static_road_marking')
            warnings=[]
            if not incoming:warnings.append('not_incoming_road_endpoint')
            if not validity:warnings.append('no_validity')
            if any(lanes.get(n)!='driving' for n in covered):warnings.append('non_driving_validity')
            if sign.get('dynamic')!='no':warnings.append('not_static')
            rows.append(dict(zip(FIELDS,[rid,sign.get('id'),sign.get('type'),sign.get('dynamic'),
                sign.get('orientation'),junction,round(s,6),round(length-s,6),
                round(x,5),round(y,5),';'.join(map(str,sorted(k for k,v in lanes.items() if v=='driving'))),
                ';'.join(f'{n}:{lanes.get(n,"ABSENT")}' for n in covered),cls,';'.join(warnings)])))
    return rows

def main():
    p=argparse.ArgumentParser()
    p.add_argument('xodr')
    p.add_argument('--out',required=True)
    a=p.parse_args()
    rows=extract(a.xodr)
    with open(a.out,'w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)
    print('static_294_candidates',len(rows),'unique_ids',len(set(x['sign_id'] for x in rows)))

if __name__=='__main__':main()

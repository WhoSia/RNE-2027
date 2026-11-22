"""P24: passive, SHA-locked DLR-UT map/measurement join gate.

Does not assign physical lane permissions or operate any real controller.
"""
import csv
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
import fitz
from pyproj import CRS, Transformer

XODR_SHA='256115a13cd29cb1d36cbbf110a4dbfa104ec2bdb680e3af1505a53f4ded30c4'
PDF_SHA='94fd9ebd32d04a9c35b02be526fbd11a8d5a613933d7961fde800386853b34f3'
TRAJ_SHA='6ba8920caa839dc20e2fd7f2fe2dedd553aeb4c27e4be3ea453054de0b09af50'
VOLUME_SHA={'12:00':'98e4e0a593702188c2d134cef1346cbc7501067c9ad421ddb9e72a1e6d9d1d15','18:00':'62bc193f77d7e54e761855ea7c8a82229d4a8a924a4b622de228588eb3b4bcfe','23:30':'00f6f29b2be6c2fa517077de3b7accbbfc75edddc92332534f00ad6b62312798'}
MOVEMENT_RE=re.compile(r'^(East|West|North|South)(\d+)(East|West|North|South)(\d+)$')

def locked(p, expected):
    p=Path(p)
    if hashlib.sha256(p.read_bytes()).hexdigest()!=expected:
        raise ValueError('source bytes mismatch: '+p.name)
    return p

def pdf_vehicle_heads(pdf):
    doc=fitz.open(locked(pdf,PDF_SHA))
    text='\n'.join(doc[x].get_text() for x in (11,12))
    found=[(int(a),float(b),float(c)) for a,b,c in re.findall(
        r'(?m)^\s*(\d{1,2})\s*\n\s*(\d{6}\.\d{3})\s*\n\s*(\d{7}\.\d{3})',text)]
    veh=[row for row in found if 1<=row[0]<=9]
    if len(veh)!=18 or {x[0] for x in veh}!=set(range(1,10)):
        raise ValueError('publisher vehicle-signal Table 3 unexpectedly changed')
    return veh

def audit_map(map_path,pdf,trajectory,volume_paths):
    root=ET.parse(locked(map_path,XODR_SHA)).getroot()
    raw=locked(trajectory,TRAJ_SHA)
    geo=root.findtext('./header/geoReference')
    if not geo:raise ValueError('OpenDRIVE missing CRS')
    transformer=Transformer.from_crs(CRS.from_epsg(32632),CRS.from_proj4(geo),always_xy=True)
    roads=root.findall('./road')
    map_signals=[{'road_id':road.get('id'),'map_id':s.get('id'),'type':s.get('type'),
                  'dynamic':s.get('dynamic'),'orientation':s.get('orientation'),
                  's_m':float(s.get('s')),'t_m':float(s.get('t'))}
                 for road in roads for s in road.findall('./signals/signal')]
    pub=pdf_vehicle_heads(pdf)
    heads=[{'id':id,'easting':e,'northing':n,'map_local_x':round(transformer.transform(e,n)[0],3),
            'map_local_y':round(transformer.transform(e,n)[1],3)} for id,e,n in pub]
    ext=root.find('header').attrib
    for head in heads:
        if not(float(ext['west'])<=head['map_local_x']<=float(ext['east']) and
               float(ext['south'])<=head['map_local_y']<=float(ext['north'])):
            raise ValueError('published traffic signal outside map geographic extent')
    with raw.open(encoding='utf-8',newline='') as f:
        tr=csv.DictReader(f)
        first=next(tr)
        samples=[first]+list(tr)
    xy=[transformer.transform(float(row['center_easting']),float(row['center_northing'])) for row in samples]
    inside=sum(float(ext['west'])<=x<=float(ext['east']) and float(ext['south'])<=y<=float(ext['north']) for x,y in xy)
    volumes={}
    for win,(fname,sha) in volume_paths.items():
        with locked(fname,sha).open(encoding='utf-8',newline='') as f:
            reader=csv.reader(f);header=next(reader)
        cols=header[1:]
        parsed=[]
        for col in cols:
            m=MOVEMENT_RE.fullmatch(col)
            if not m:
                raise ValueError('unknown route label: '+col)
            parsed.append({'from_approach':m.group(1),'from_lane_token':int(m.group(2)),
                           'to_approach':m.group(3),'to_lane_token':int(m.group(4))})
        volumes[win]={'movement_columns':len(cols),'route_labels':cols,
                      'approach_tokens':dict(Counter(p['from_approach'] for p in parsed)),
                      'source_sha256':sha}
    published_ids={str(row['id']) for row in heads}
    map_ids={s['map_id'] for s in map_signals}
    return {'status':'P24_GEO_REFERENCING_PASS_SIGNAL_TO_MOVEMENT_MAP_UNKNOWN',
        'source_hashes':{'xodr':XODR_SHA,'documentation':PDF_SHA,'night_trajectory':TRAJ_SHA},
        'open_drive':{'header':{key:ext[key] for key in ('name','date','west','east','south','north')},
                      'geo_reference':geo,'road_count':len(roads),
                      'junction_count':len(root.findall('./junction')),
                      'map_signal_count':len(map_signals),'map_signals':map_signals,
                      'unique_map_signal_ids':sorted(map_ids),
                      'dynamic_controller_count':len(root.findall('.//controller')),
                      'map_signal_reference_count':len(root.findall('.//signalReference'))},
        'official_publisher_vehicle_heads':heads,
        'publisher_vehicle_head_instances':len(heads),
        'distinct_publisher_vehicle_ids':len(published_ids),
        'direct_numeric_signal_identifier_matches':sorted(published_ids & map_ids),
        'night_trajectory_positions_within_map_bbox':{'inside':inside,'observations':len(xy)},
        'published_volume_route_tokens':volumes,
        'gates':{'published_signal_coordinates_in_map_CRS':True,
                 'sample_trajectory_positions_in_map_extent':inside==len(xy),
                 'published_vehicle_head_to_map_signal_ID':bool(published_ids & map_ids),
                 'movement_token_to_openDRIVE_lane_id':False,
                 'controlling_signal_head_per_movement':False,
                 'matched_vehicle_stopline_crossings':False},
        'warning':'The seven static OpenDRIVE type-294 map signals are not the 30 field signal state channels. Spatial proximity or a shared number does not prove traffic control or a route-lane mapping.'}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument('map');p.add_argument('doc');p.add_argument('trajectory')
    p.add_argument('noon');p.add_argument('evening');p.add_argument('night');p.add_argument('output')
    a=p.parse_args()
    v={'12:00':(a.noon,VOLUME_SHA['12:00']),'18:00':(a.evening,VOLUME_SHA['18:00']),
       '23:30':(a.night,VOLUME_SHA['23:30'])}
    Path(a.output).write_text(json.dumps(audit_map(a.map,a.doc,a.trajectory,v),sort_keys=True,indent=2)+'\n')

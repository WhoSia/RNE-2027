"""P23: SHA-locked DLR observed trajectories -> OpenDRIVE centerline alignment.

No traffic-signal head mapping, calibrated lane matching, or causal discharge inference.
"""
import argparse
import csv
import hashlib
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median
import xml.etree.ElementTree as ET
from pyproj import CRS, Transformer
from shapely.geometry import LineString, MultiLineString, Point

SOURCES = {
    'map':'256115a13cd29cb1d36cbbf110a4dbfa104ec2bdb680e3af1505a53f4ded30c4',
    'trajectories':'6ba8920caa839dc20e2fd7f2fe2dedd553aeb4c27e4be3ea453054de0b09af50',
    'volume':'00f6f29b2be6c2fa517077de3b7accbbfc75edddc92332534f00ad6b62312798',
}


def seal(path, kind):
    if hashlib.sha256(Path(path).read_bytes()).hexdigest() != SOURCES[kind]:
        raise ValueError(f'WRONG SOURCE SHA256: {kind}')


def map_geometry(path, spacing_m=1.0):
    seal(path,'map')
    root=ET.parse(path).getroot()
    geo=root.find('header/geoReference')
    if geo is None or not geo.text:raise ValueError('OpenDRIVE lacks coordinate reference')
    proj=geo.text.strip()
    if '+lon_0=9' not in proj or '+units=m' not in proj:
        raise ValueError('unsupported OpenDRIVE projection')
    transform=Transformer.from_crs(CRS.from_epsg(32632),CRS.from_proj4(proj),always_xy=True)
    lines=[];road_count=0;geom_types=Counter()
    for road in root.findall('road'):
        road_count+=1
        for g in road.findall('planView/geometry'):
            x0,y0,head,length=(float(g.get(n)) for n in ('x','y','hdg','length'))
            kids=list(g)
            if len(kids)!=1 or kids[0].tag not in ('line','arc'):
                raise ValueError('unsupported centerline geometry')
            kind=kids[0].tag;geom_types[kind]+=1
            curve=float(kids[0].get('curvature')) if kind=='arc' else 0.0
            count=max(1,math.ceil(length/spacing_m))
            coords=[]
            for i in range(count+1):
                s=length*i/count
                if abs(curve)<1e-12:
                    xy=(x0+s*math.cos(head),y0+s*math.sin(head))
                else:
                    xy=(x0+(math.sin(head+curve*s)-math.sin(head))/curve,
                        y0-(math.cos(head+curve*s)-math.cos(head))/curve)
                coords.append(xy)
            lines.append(LineString(coords))
    signals=root.findall('.//road/signals/signal')
    return MultiLineString(lines),transform,{'roads':road_count,'geometry_elements':sum(geom_types.values()),
        'geometry_types':dict(geom_types),'static_signal_elements':len(signals),
        'static_signal_unique_ids':len({a.get('id') for a in signals}),
        'projection':proj, 'reference_raw_source_crs':'EPSG:32632'}


def observed(path,kind):
    seal(path,kind)
    with Path(path).open(encoding='utf8',newline='') as stream:
        r=csv.DictReader(stream)
        if not r.fieldnames:raise ValueError('missing source CSV headers')
        rows=list(r)
    if not rows:raise ValueError('empty source')
    return rows


def inspect(map_path,trajectory_path,volume_path,stride=1):
    if type(stride) is not int or stride<1:raise ValueError('stride must be positive integer')
    lines,transform,geo=map_geometry(map_path)
    tracks=observed(trajectory_path,'trajectories')
    bins=observed(volume_path,'volume')
    readings=[]; shifted_100m=[]; per_id=defaultdict(list)
    for r in tracks[::stride]:
        e,n=(float(r[k]) for k in ('center_easting','center_northing'))
        x,y=transform.transform(e,n)
        d=lines.distance(Point(x,y))
        readings.append(d)
        shifted_100m.append(lines.distance(Point(x+100,y)))
        per_id[r['id']].append(d)
    crossed=Counter(); times=[]
    movement_columns=[c for c in bins[0] if c!='timestamp']
    for r in bins:
        times.append(r['timestamp'])
        for c in movement_columns:
            if r[c] not in ('0','1'):raise ValueError('non-binary volume row')
            crossed[c]+=int(r[c])
    if len(times)!=len(set(times)):raise ValueError('duplicate volume timestamp')
    reading_summary={
        'n':len(readings),'min_m':min(readings),'median_m':median(readings),
        'p90_m':sorted(readings)[math.ceil(.9*len(readings))-1],
        'max_m':max(readings),
        'within_5m':sum(d<=5 for d in readings),
        'within_10m':sum(d<=10 for d in readings),
        'within_20m':sum(d<=20 for d in readings),
    }
    return {'protocol':'P23_DLR_GEOSPATIAL_AND_OFFICIAL_STOPLINE_BINS',
        'scope':'REAL_SOURCE_GEOMETRY_MATCHING_NOT_SIGNAL_HEAD_MAPPING_NOT_SUMO',
        'source_sha256':SOURCES,
        'map':geo,
        'trajectory_rows_all':len(tracks),'sample_stride':stride,
        'observed_ids_all':len({r['id'] for r in tracks}),
        'centerline_distance':reading_summary,
        'exploratory_negative_control_shift_easting_100m':{
            'median_distance_m':median(shifted_100m),
            'within_10m':sum(d<=10 for d in shifted_100m),
            'n':len(shifted_100m),
            'interpretation':'Diagnostic deliberate coordinate corruption; not an independent published validation'},
        'volume':{'seconds':len(bins),'first_timestamp':times[0],
            'last_timestamp':times[-1], 'movement_columns':len(movement_columns),
            'crossing_bins':sum(crossed.values()),
            'active_movement_columns':sum(v>0 for v in crossed.values()),
            'counts_by_movement':dict(sorted(crossed.items()))},
        'limitations':['Centerline proximity not a verified lane, stopline, turn or signal assignment',
                       'Static OpenDRIVE road signal IDs are not proven to match 30 dynamic CSV signal IDs',
                       'Volume CSV contains one-second crossing indicators, not sub-second vehicle headway',
                       'Source data are one site and one 15-minute night window',
                       'Some trajectories are vulnerable road users, not cars']}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('map',type=Path);p.add_argument('trajectories',type=Path)
    p.add_argument('volume',type=Path);p.add_argument('output',type=Path)
    p.add_argument('--stride',type=int,default=1)
    x=p.parse_args()
    x.output.write_text(json.dumps(inspect(x.map,x.trajectories,x.volume,x.stride),indent=2,sort_keys=True)+'\n',encoding='utf-8')

"""P25: independently detect measured center-point crossings, then reconcile with
DLR-UT *derived-from-same-trajectories* traffic-volume CSV.

Source hashes lock a specific 15-minute, 2023-09-24 23:30Z DLR-UT v1.3.1
sample and its older OpenDRIVE map. No traffic-light-to-lane mapping or
independent field validation is claimed. The geometric stopline is a
local tangent-plane approximation to the OpenDRIVE type=294 marking.
"""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import NamedTuple
import csv
import hashlib
import json
import math
import xml.etree.ElementTree as ET

from pyproj import CRS, Transformer
from p24_xodr_static_signal_audit import pose

SHA = {
    'map': '256115a13cd29cb1d36cbbf110a4dbfa104ec2bdb680e3af1505a53f4ded30c4',
    'trajectory': '6ba8920caa839dc20e2fd7f2fe2dedd553aeb4c27e4be3ea453054de0b09af50',
    'traffic_volume': '00f6f29b2be6c2fa517077de3b7accbbfc75edddc92332534f00ad6b62312798',
}
MOTOR_COLUMNS = ('classifications_car', 'classifications_van',
                 'classifications_truck', 'classifications_motorbike')
ALL_CLASSES = ('classifications_pedestrian','classifications_bicycle',
               'classifications_motorbike','classifications_car',
               'classifications_van','classifications_truck')
MAX_ADJACENT_GAP_S = 0.20
MAX_MATCH_ERROR_S = 1.0
MAX_LATERAL_M = 20.5


def verify_sha(path: Path, expected: str) -> None:
    current = hashlib.sha256(path.read_bytes()).hexdigest()
    if current != expected:
        raise ValueError(f'unexpected SHA256 for {path.name}: {current}')


def source_arm(heading):
    # Road tangent points TOWARD junction (positive OpenDRIVE s).
    dx, dy = -math.cos(heading), -math.sin(heading)
    if abs(dx) > abs(dy):
        return 'East' if dx > 0 else 'West'
    return 'North' if dy > 0 else 'South'


def poly_at(width, d_s):
    u=d_s-float(width.attrib['sOffset'])
    return sum(float(width.attrib[k])*u**i for i,k in enumerate('abcd'))


def lane_spans(road,s):
    section=max((a for a in road.findall('lanes/laneSection')
                 if float(a.attrib['s']) <= s+1e-7),
                key=lambda x:float(x.attrib['s']))
    offset=s-float(section.attrib['s'])
    neg=0.0
    spans=[]
    for lane in section.findall('right/lane'):
        widths=[v for v in lane.findall('width') if float(v.attrib['sOffset'])<=offset+1e-8]
        if not widths:
            raise ValueError('uncovered width segment')
        w=max(widths,key=lambda v:float(v.attrib['sOffset']))
        val=poly_at(w,offset)
        if not math.isfinite(val) or val < -1e-5:
            raise ValueError('non-physical lane width')
        spans.append({'lane_id':int(lane.attrib['id']),
                      'type':lane.attrib['type'],
                      't_min':-(neg+val),'t_max':-neg})
        neg+=val
    return spans


def markers_from_map(path):
    root=ET.parse(path).getroot()
    if root.tag!='OpenDRIVE':raise ValueError('unknown map')
    header=root.find('header')
    local_crs=CRS.from_proj4(header.findtext('geoReference'))
    transform=Transformer.from_crs(local_crs,CRS.from_epsg(32632),always_xy=True)
    markers=[]
    for road in root.findall('road'):
        link=road.find('link/successor')
        if link is None or link.attrib.get('elementType')!='junction':
            continue
        for sig in road.findall('signals/signal'):
            s=float(sig.attrib['s'])
            if (float(road.attrib['length'])-s)>1.0:continue
            if sig.attrib.get('type')!='294' or sig.attrib.get('dynamic')!='no':
                raise ValueError('unrecognized stopline marker')
            x,y,heading=pose(road,s)
            east,north=transform.transform(x,y)
            bounds=[]
            for v in sig.findall('laneValidity'):
                lo,hi=sorted([int(v.attrib['fromLane']),int(v.attrib['toLane'])])
                bounds.append((lo,hi))
            if not bounds:raise ValueError('no laneValidity: do not guess')
            markers.append({'road_id':road.attrib['id'],'feature_id':sig.attrib['id'],
                            'source_arm':source_arm(heading),
                            'easting':east,'northing':north,'heading':heading,
                            'lane_validity_ranges':bounds,'lane_spans':lane_spans(road,s),
                            's':s})
    if len(markers)!=4 or set(a['source_arm'] for a in markers)!=set(('East','West','North','South')):
        raise ValueError('inbound marker census/arm allocation differs')
    return markers


def lateral_lane(marker,t):
    candidates=[x for x in marker['lane_spans']
                if x['t_min']-1e-6 <= t <= x['t_max']+1e-6]
    if len(candidates)!=1:return None
    return candidates[0]


def projected(marker,pt):
    dx=float(pt['center_easting'])-marker['easting']
    dy=float(pt['center_northing'])-marker['northing']
    h=marker['heading']
    return (dx*math.cos(h)+dy*math.sin(h),
            -dx*math.sin(h)+dy*math.cos(h))


def rows_from_csv(path):
    with path.open(newline='',encoding='utf-8') as f:
        return list(csv.DictReader(f))


def is_motor(row):
    cls=max(ALL_CLASSES,key=lambda k:float(row[k]))
    return cls in MOTOR_COLUMNS,cls.replace('classifications_','')


def trajectory_crossings(markers,trajectory_rows):
    by_id=defaultdict(list)
    for row in trajectory_rows:by_id[row['id']].append(row)
    events=[]
    gaps=[]
    initial=[]
    for oid,rows in sorted(by_id.items()):
        track=sorted(rows,key=lambda r:r['timestamp'])
        motor,category=is_motor(track[0])
        if not motor:continue
        for marker in markers:
            d0,t0=projected(marker,track[0])
            if 0<=d0<=2 and -MAX_LATERAL_M<=t0<=0:
                initial.append({'id':oid,'road_id':marker['road_id'],
                    'source_arm':marker['source_arm'],
                    'first_observed':track[0]['timestamp'],
                    'first_signed_dist_m':round(d0,3),
                    'first_lateral_m':round(t0,3),
                    'type':'ALREADY_DOWNSTREAM_AT_FIRST_SAMPLED_FRAME'})
            for a,b in zip(track,track[1:]):
                s0,t0=projected(marker,a)
                s1,t1=projected(marker,b)
                if not s0<0<=s1:continue
                at=datetime.fromisoformat(a['timestamp'])
                bt=datetime.fromisoformat(b['timestamp'])
                dt=(bt-at).total_seconds()
                if dt<=0:raise ValueError('nonmonotone trajectory timestamp')
                alpha=-s0/(s1-s0)
                lateral=t0+alpha*(t1-t0)
                if not -MAX_LATERAL_M<=lateral<=0:continue
                lane=lateral_lane(marker,lateral)
                if lane is None or lane['type']!='driving':continue
                if dt > MAX_ADJACENT_GAP_S:
                    gaps.append({'id':oid,'road_id':marker['road_id'],'dt_s':round(dt,3),
                                 'status':'UNOBSERVED_CROSSING_IN_TEMPORAL_GAP'})
                    continue
                if a['interpolated']=='True' or b['interpolated']=='True':
                    # Source itself says a row was filled by smoothing; distinguish direct readings.
                    gaps.append({'id':oid,'road_id':marker['road_id'],
                                 'status':'INTERPOLATED_SAMPLE_NOT_DIRECT_EVIDENCE'})
                    continue
                when=at+(bt-at)*alpha
                valid=any(lo<=lane['lane_id']<=hi
                          for lo,hi in marker['lane_validity_ranges'])
                events.append({'road_id':marker['road_id'],'id':oid,
                    'source_arm':marker['source_arm'],'class':category,
                    'crossing_time_utc':when.isoformat(),
                    'bracket_start_utc':at.isoformat(),
                    'bracket_end_utc':bt.isoformat(),
                    'bracket_width_ms':round(dt*1000,3),
                    'lateral_m':round(lateral,3),
                    'map_lane_id':lane['lane_id'],
                    'map_lane_validity_agrees':valid,
                    'vehicle_movement':None,
                    'controlling_signal_id':None,
                    'evidence':'20HZ_DIRECT_CENTER_CROSSING_ESTIMATED_TIME',
                    'note':'2015 geometry; point estimate is linearly interpolated within the sample interval'})
    events.sort(key=lambda x:(x['crossing_time_utc'],x['road_id'],x['id']))
    return events,gaps,initial,by_id


def reference_volume_events(volume_rows):
    events=[]
    for row in volume_rows:
        ts=row['timestamp']
        for route,value in row.items():
            if route=='timestamp':continue
            count=int(value or 0)
            if count<0:raise ValueError('negative official volume')
            for _ in range(count):
                prefix=next((a for a in ('East','West','North','South') if route.startswith(a)),None)
                if prefix is None:raise ValueError('unknown route column')
                events.append({'route':route,'source_arm':prefix,'time_utc':ts})
    return sorted(events,key=lambda x:(x['time_utc'],x['route']))


def _optimal_ordered_matching(crossings, volume_events, cross_indices, volume_indices):
    """Exact lexicographic max-cardinality then min-|time| matching for one arm.

    For sorted points on a 1D timeline with absolute time distance, an optimal
    non-crossing matching exists. Dynamic programming checks all three choices
    at (i,j): skip a crossing, skip a counter, or match within ±1 second.
    Unlike globally greedy nearest-neighbor pairing, this cannot sacrifice a
    second feasible match to get one shorter first match.
    """
    cidx=sorted(cross_indices,key=lambda i:(crossings[i]['crossing_time_utc'],i))
    vidx=sorted(volume_indices,key=lambda i:(volume_events[i]['time_utc'],i))
    n,m=len(cidx),len(vidx)
    dp=[[(0,0.0) for _ in range(m+1)] for _ in range(n+1)]
    action=[[None]*(m+1) for _ in range(n+1)]
    for i in range(1,n+1):action[i][0]='skip_crossing'
    for j in range(1,m+1):action[0][j]='skip_volume'
    for i in range(1,n+1):
        for j in range(1,m+1):
            options=[(dp[i-1][j],'skip_crossing'),
                     (dp[i][j-1],'skip_volume')]
            ct=datetime.fromisoformat(crossings[cidx[i-1]]['crossing_time_utc'])
            vt=datetime.fromisoformat(volume_events[vidx[j-1]]['time_utc'])
            delta=abs((ct-vt).total_seconds())
            if delta<=MAX_MATCH_ERROR_S+1e-9:
                count,cost=dp[i-1][j-1]
                options.append(((count+1,cost+delta),'match'))
            best,operation=max(options,key=lambda op:(op[0][0],-op[0][1],op[1]=='match'))
            dp[i][j]=best
            action[i][j]=operation
    i,j=n,m
    pairs=[]
    while i>0 or j>0:
        operation=action[i][j]
        if operation=='match':
            ci,vi=cidx[i-1],vidx[j-1]
            d=abs((datetime.fromisoformat(crossings[ci]['crossing_time_utc'])-
                   datetime.fromisoformat(volume_events[vi]['time_utc'])).total_seconds())
            pairs.append({'crossing_index':ci,'volume_index':vi,
                          'abs_time_difference_s':round(d,4),
                          'match_criteria':'same_approach_UTC_within_1s_max_cardinality_min_cost'})
            i-=1;j-=1
        elif operation=='skip_crossing':i-=1
        elif operation=='skip_volume':j-=1
        else:raise RuntimeError('missing matching backpointer')
    return pairs


def reconcile(crossings,volume_events):
    """Crossing detection precedes matching; route destination is never inferred."""
    matched=[]
    for arm in ('East','West','North','South'):
        ci=[i for i,c in enumerate(crossings) if c['source_arm']==arm]
        vi=[i for i,v in enumerate(volume_events) if v['source_arm']==arm]
        matched.extend(_optimal_ordered_matching(crossings,volume_events,ci,vi))
    matched.sort(key=lambda item:(item['crossing_index'],item['volume_index']))
    used_c={x['crossing_index'] for x in matched}
    used_v={x['volume_index'] for x in matched}
    return (matched,[i for i in range(len(crossings)) if i not in used_c],
            [i for i in range(len(volume_events)) if i not in used_v])


def plausible_left_censors(unmatched_volumes,volume_events,initial):
    evidence=[]
    for index in unmatched_volumes:
        v=volume_events[index]
        t=datetime.fromisoformat(v['time_utc'])
        matches=[]
        for c in initial:
            if c['source_arm']!=v['source_arm']:continue
            delta=(datetime.fromisoformat(c['first_observed'])-t).total_seconds()
            if 0<=delta<=1.0:
                matches.append({**c,'offset_from_reported_second_s':round(delta,4)})
        evidence.append({'volume_index':index,'route':v['route'],
                         'time_utc':v['time_utc'],
                         'candidate_first_observation_after_line':matches,
                         'conclusion':'UNCERTAIN_LEFT_CENSOR_NOT_CONFIRMED_CROSSING'})
    return evidence


def audit(map_path,trajectory_path,traffic_volume_path):
    for name,path in [('map',map_path),('trajectory',trajectory_path),('traffic_volume',traffic_volume_path)]:
        verify_sha(Path(path),SHA[name])
    markers=markers_from_map(map_path)
    tracks=rows_from_csv(trajectory_path)
    volume=rows_from_csv(traffic_volume_path)
    crossings,uncertain,initial,by_id=trajectory_crossings(markers,tracks)
    official=reference_volume_events(volume)
    matched,unmatched_c,unmatched_v=reconcile(crossings,official)
    return {'protocol':'P25_REAL_CENTER_POINT_CROSSINGS_VERSUS_DERIVED_OFFICIAL_COUNTERS',
        'sources_sha256':SHA,'sampling':'20 Hz nominal trajectory, 1 s derived volume',
        'observations':{'trajectory_rows':len(tracks),'object_ids':len(by_id),
                        'volume_rows':len(volume),
                        'official_route_columns':len(volume[0])-1,
                        'inbound_markers':len(markers)},
        'markers':[{k:v for k,v in m.items() if k!='lane_spans'} for m in markers],
        'crossings':crossings,
        'counts':{'trajectory_crossings_direct':len(crossings),
                  'official_center_point_crossings':len(official),
                  'one_to_one_approach_time_matches':len(matched),
                  'trajectory_only':len(unmatched_c),
                  'volume_only':len(unmatched_v),
                  'within_2015_marker_laneValidity':sum(c['map_lane_validity_agrees'] for c in crossings),
                  'excluded_interpolation_or_large_gaps':len(uncertain)},
        'matched_pairs':matched,
        'unmatched_trajectory_crossings':[crossings[i] for i in unmatched_c],
        'unmatched_official_volume':[official[i] for i in unmatched_v],
        'left_censor_candidates':plausible_left_censors(unmatched_v,official,initial),
        'large_gap_or_interpolated_crossings':uncertain,
        'gates':{'publisher_source_bytes_verified':True,
                 'motor_trajectory_crossing_brackets_verified':True,
                 'official_metadata_reconciliation_attempted':True,
                 'movement_specific_crossings_verified':False,
                 'controlling_signal_id_verified':False,
                 'independent_real_world_truth_verified':False,
                 'signal_policy_effect_validated':False},
        'caveat':'Published traffic-volume is derived from the SAME DLR trajectories and counts center points at lanes. Agreement is not external validation. 2015 map static laneValidity is not a 2023 lane-flow truth source.'}


if __name__=='__main__':
    import argparse
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--map',type=Path,required=True)
    a.add_argument('--trajectories',type=Path,required=True)
    a.add_argument('--volume',type=Path,required=True)
    a.add_argument('--out',type=Path,required=True)
    v=a.parse_args()
    v.out.write_text(json.dumps(audit(v.map,v.trajectories,v.volume),indent=2,sort_keys=True)+'\n')

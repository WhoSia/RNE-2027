"""D42: publisher-count independent topology gate, using unadjusted candidate events.

Research only: reconstructed approach direction is a geographic inference from
OpenDRIVE road approach location, not publisher-certified movement assignment.
"""
import argparse
import collections
import csv
import json
import xml.etree.ElementTree as ET
from pathlib import Path

INCOMING = {"100000":"East", "179000":"South", "201000":"West", "280000":"North"}
EXPECTED_OUTGOING = frozenset({"101000", "180000", "200000", "279000"})

def read_network(map_path):
    root=ET.parse(map_path).getroot()
    roads={r.get('id'):r for r in root.findall('road')}
    junctions=root.findall('junction')
    if len(junctions)!=1 or junctions[0].get('id')!='300000':
        raise ValueError('unexpected junction count/ID')
    connections=[]
    for c in junctions[0].findall('connection'):
        incoming=c.get('incomingRoad'); connector=c.get('connectingRoad')
        if incoming not in roads or connector not in roads:raise ValueError('unknown road')
        cr=roads[connector]
        pred=cr.find('./link/predecessor');succ=cr.find('./link/successor')
        if pred is None or succ is None or pred.get('elementId')!=incoming or succ.get('elementType')!='road':
            raise ValueError('broken connector predecessor/successor')
        outgoing=succ.get('elementId')
        if outgoing not in roads:raise ValueError('unknown outgoing road')
        links=c.findall('laneLink')
        if not links:raise ValueError('empty laneLink')
        if c.get('contactPoint')!='start':raise ValueError('unsupported contactPoint')
        a_sections=roads[incoming].findall('./lanes/laneSection')
        b_sections=cr.findall('./lanes/laneSection')
        source_lanes={lane.get('id') for lane in a_sections[-1].findall('.//lane')}
        sink_lanes={lane.get('id') for lane in b_sections[0].findall('.//lane')}
        pairs=[]
        for l in links:
            a,b=l.get('from'),l.get('to')
            if a not in source_lanes or b not in sink_lanes:raise ValueError('dangling laneLink')
            pairs.append([a,b])
        connections.append({'connection_id':c.get('id'), 'incoming_road':incoming,
            'connecting_road':connector,'outgoing_road':outgoing,'lane_links':pairs})
    incoming_set={c['incoming_road'] for c in connections}
    outgoing_set={c['outgoing_road'] for c in connections}
    if incoming_set!=set(INCOMING) or outgoing_set!=EXPECTED_OUTGOING:
        raise ValueError('unexpected approach roads')
    routes={(c['incoming_road'],c['outgoing_road']) for c in connections}
    if len(connections)!=16 or len(routes)!=16:raise ValueError('not exactly 16 routes')
    return connections

def published_counts(volume_file):
    with open(volume_file,encoding='utf-8',newline='') as f:
        rd=csv.DictReader(f)
        if rd.fieldnames is None:raise ValueError('missing traffic volume header')
        keys=[k for k in rd.fieldnames if k!='timestamp']
        totals=collections.Counter({name:0 for name in INCOMING.values()})
        rows=0
        for line in rd:
            rows+=1
            for k in keys:
                direction=next((p for p in totals if k.startswith(p)),None)
                if direction is None:raise ValueError('unmapped movement column: '+k)
                value=int(line[k]);
                if value<0:raise ValueError('negative count')
                totals[direction]+=value
    if len(keys)!=32 or rows!=900:raise ValueError('unexpected field/time dimensions')
    return dict(totals),rows,len(keys)

def candidate_counts(csv_file):
    approach=collections.Counter({key:0 for key in INCOMING})
    by_track=collections.defaultdict(set)
    by_road=collections.Counter()
    with open(csv_file,encoding='utf-8',newline='') as f:
        for row in csv.DictReader(f):
            road=row['road_id'];by_road[road]+=1
            if road in INCOMING:
                if row['direction']!='forward':raise ValueError('unexpected reverse approach')
                approach[road]+=1
                by_track[row['track_id']].add(road)
    duplicate_tracks=sum(len(v)>1 for v in by_track.values())
    return dict(approach),dict(by_road),len(by_track),duplicate_tracks

def audit(map_path,event_file,volume_file):
    links=read_network(map_path)
    actual,seconds,movements=published_counts(volume_file)
    candidate,by_road,tracks,duplicates=candidate_counts(event_file)
    per_approach=[]
    for road,direction in INCOMING.items():
        per_approach.append({'incoming_road':road,'inferred_direction':direction,
            'candidate_crossings':candidate[road], 'publisher_movement_cells':actual[direction],
            'difference':candidate[road]-actual[direction],
            'status':'COMPARISON_NOT_INDEPENDENT_VALIDATION'})
    return {'routes':links,'n_routes':len(links), 'n_lane_links':sum(len(c['lane_links']) for c in links),
            'published_count_cells':sum(actual.values()),'published_movement_columns':movements,
            'published_seconds':seconds,'approach':per_approach, 'candidate_total':sum(candidate.values()),
            'candidate_tracks':tracks,'candidate_multi_approach_tracks':duplicates,
            'candidate_all_by_road':by_road,
            'status':'HOLD_UNVALIDATED_GEOMETRIC_EVENTS',
            'limit':'inferred cardinal labels; no certified lane-specific stopline or 30-head mapping'}

def main():
    p=argparse.ArgumentParser();p.add_argument('map');p.add_argument('candidate_csv');p.add_argument('published_volume_csv');p.add_argument('output_prefix')
    args=p.parse_args();result=audit(args.map,args.candidate_csv,args.published_volume_csv)
    Path(args.output_prefix+'.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    with open(args.output_prefix+'.csv','w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=list(result['approach'][0]));w.writeheader();w.writerows(result['approach'])
    print(json.dumps({k:v for k,v in result.items() if k!='routes'},indent=2))

if __name__=='__main__':main()

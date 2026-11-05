"""Regenerate the time-dependent travel and staged-resource outputs, no optimizer."""
from dataclasses import asdict
from pathlib import Path
import json, csv, sys
sys.path.insert(0, str(Path(__file__).resolve().parent/'src'))
from transit_schedule import earliest_arrival, shortest_distance, scenario
from zone_phases import Movement, simulate, DeadlockError

out=Path(__file__).parent/'results';out.mkdir(exist_ok=True)
cs=scenario()
dist,path=shortest_distance(cs,'O','D')
all_results=[]
for start in range(0,61):
    for margin in [1,2,4]:
        chosen=earliest_arrival(cs,'O','D',start,transfer_min=margin)
        near=earliest_arrival([c for c in cs if c.origin!='F' and c.destination!='F'],'O','D',start,transfer_min=margin)
        far=earliest_arrival([c for c in cs if c.origin!='N' and c.destination!='N'],'O','D',start,transfer_min=margin)
        all_results.append({'departure_min':start,'transfer_margin_min':margin,
                            'near_arrival':near['arrival'] if near else None,
                            'far_arrival':far['arrival'] if far else None,
                            'winner':'F' if chosen and any(x.destination=='F' for x in chosen['legs']) else ('N' if chosen else 'unreachable'),
                            'arrival_min':chosen['arrival'] if chosen else None,
                            'distance_km':chosen['distance_km'] if chosen else None,
                            'transfers':chosen['transfers'] if chosen else None})
with (out/'departure_sweep.csv').open('w',newline='',encoding='utf-8') as fh:
    writer=csv.DictWriter(fh,fieldnames=list(all_results[0]));writer.writeheader();writer.writerows(all_results)
example=earliest_arrival(cs,'O','D',0)
near=earliest_arrival([c for c in cs if 'F' not in (c.origin,c.destination)],'O','D',0)
zone=simulate([Movement('ped',0,(('B',3),)),Movement('car',0,(('A',2),('B',2))),Movement('follower',1,(('A',1),))])
try:
    simulate([Movement('car1',0,(('A',2),('B',1))),Movement('car2',0,(('B',2),('A',1)))])
    deadlock=False
except DeadlockError:
    deadlock=True
counts={str(m):{'far':sum(x['winner']=='F' for x in all_results if x['transfer_margin_min']==m),'near':sum(x['winner']=='N' for x in all_results if x['transfer_margin_min']==m),'unreachable':sum(x['winner']=='unreachable' for x in all_results if x['transfer_margin_min']==m)} for m in [1,2,4]}
report={'scope':'synthetic fixed timetable, independent prototype; no GTFS, H3 indexing, controller or actual SUMO run',
        'shortest_distance_km':dist,'shortest_distance_stops':path,
        'earliest_arrival_start0':{'arrival_min':example['arrival'],'distance_km':example['distance_km'],'transfers':example['transfers'],'trips':[x.trip for x in example['legs']]},
        'near_route_start0':{'arrival_min':near['arrival'],'distance_km':near['distance_km']},
        'transfer_margin2_start0_arrival':earliest_arrival(cs,'O','D',0,transfer_min=2)['arrival'],
        'time_window_winners':counts,'time_query_points':len(all_results),
        'phase_events':zone['log'],'hold_duration_A_extra':1,'mutual_hold_deadlock_detected':deadlock}
(out/'analysis.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))

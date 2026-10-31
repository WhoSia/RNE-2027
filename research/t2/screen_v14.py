"""One-factor-at-a-time screening of 9 levers (3 levels x 6 seeds).

Changes within each lever reuse one fixed arrival stream for its seed.
This is descriptive local sensitivity; never interpret as Sobol index
or a universal variable importance ranking across traffic networks.
"""
from dataclasses import replace
from collections import defaultdict
from pathlib import Path
from statistics import mean
import csv,json
from spatial_v10 import Config
from dual_lane_v11 import DualConfig,run
from arrival_design_v14 import ArrivalProfile,make_arrivals

LEVELS={'pocket_m':(14.,28.,70.),'B_share':(.2,.5,.8),
 'change_zone_m':(35.,70.,110.),'signal_offset_s':(0,20,40),
 'departure_headway_s':(1,2,3),'receiver_slots':(1,2,4),
 'receiver_headway_s':(2,4,8),'through_green_s':(40,50,60),
 'left_green_s':(25,35,45)}

def config_for(seed,lever,value):
    b=Config(duration_s=720,seed=seed,pocket_length_m=28.,
             departure_headway_s=2,through_green_s=50,left_green_s=35)
    c=DualConfig(base=b,through_B_share=.5,change_zone_m=70.,
         allow_lane_changes=True,receiver_slots=2,receiver_headway_s=4)
    if lever=='pocket_m':b=replace(b,pocket_length_m=value)
    elif lever=='B_share':c=replace(c,through_B_share=value)
    elif lever=='change_zone_m':c=replace(c,change_zone_m=value)
    elif lever=='receiver_slots':c=replace(c,receiver_slots=value)
    elif lever=='receiver_headway_s':c=replace(c,receiver_headway_s=value)
    else:b=replace(b,**{lever:value})
    return replace(c,base=b)

def evaluate():
    rows=[]
    for seed in range(6):
        stream=make_arrivals(ArrivalProfile(seed=seed))
        for lever,levels in LEVELS.items():
            for level in levels:
                z=run(config_for(seed,lever,level),stream)
                rows.append({'seed':seed,'lever':lever,'level':level,
                    'generated':z['generated'],'S':z['network_out_S'],
                    'L':z['network_out_L'],
                    'total':z['network_out_S']+z['network_out_L'],
                    'outside':z['outside']})
    return rows

def summarize(rows):
    groups=defaultdict(list)
    for r in rows:groups[(r['lever'],r['level'])].append(r)
    output=[]
    for lever,levels in LEVELS.items():
        values=[]
        for level in levels:
            g=groups[(lever,level)]
            if len(g)!=6:raise AssertionError('missing seeds')
            values.append({'level':level,'S':mean(r['S'] for r in g),
                           'L':mean(r['L'] for r in g),
                           'total':mean(r['total'] for r in g)})
        output.append({'lever':lever,'levels':values,
            'range_S':max(x['S'] for x in values)-min(x['S'] for x in values),
            'range_L':max(x['L'] for x in values)-min(x['L'] for x in values),
            'range_total':max(x['total'] for x in values)-min(x['total'] for x in values)})
    return sorted(output,key=lambda x:x['range_total'],reverse=True)

if __name__=='__main__':
    root=Path(__file__).resolve().parent/'results';root.mkdir(exist_ok=True)
    rows=evaluate()
    with (root/'sensitivity_screen_162_v14.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (root/'sensitivity_rank_v14.json').write_text(json.dumps(summarize(rows),indent=2)+'\n')
    print('runs',len(rows))

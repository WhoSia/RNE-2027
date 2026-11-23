"""P125: departure-curve mass balance from frozen P124 exits, without replay."""
import json
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent

def main():
    source=json.loads((HERE/'P124_RESULT.json').read_text())
    events_a=Counter(x['exit0'] for x in source['vehicle_exit_deltas'])
    events_b=Counter(x['exit1'] for x in source['vehicle_exit_deltas'])
    # IDs departing identically under both policies can be omitted because they cancel.
    signed_by_tick={};departures_a=0;departures_b=0
    for t in range(84,4800):
        departures_a+=events_a[t];departures_b+=events_b[t]
        signed_by_tick[t]=departures_b-departures_a
    reconstructed=[]
    for w in source['windows']:
        x=sum(signed_by_tick[t] for t in range(w['start'],w['end']))
        assert x==w['vehicle_seconds'],(w['start'],w['end'],x,w['vehicle_seconds'])
        reconstructed.append(dict(start=w['start'],end=w['end'],delta=x))
    assert sum(signed_by_tick.values())==source['delta']==-732
    different=[t for t,v in signed_by_tick.items() if v]
    assert min(different)==source['first_differing_tick']==114
    maxmag=max(abs(v) for v in signed_by_tick.values())
    extrema=[t for t,v in signed_by_tick.items() if abs(v)==maxmag]
    assert maxmag==3 and source['maximum_abs_occupancy_delta']['signed']==-3
    assert 204 in extrema
    assert sum(x['delta'] for x in source['vehicle_exit_deltas'])==-732
    result={'status':'P125_CUMULATIVE_DEPARTURE_IDENTITY_RECONSTRUCTED',
            'prereg':'P125_CUMULATIVE_DEPARTURE_IDENTITY_PREREG.md',
            'source':'P124_RESULT.json','replayed_t2_arms':0,
            'changed_identity_count':len(source['vehicle_exit_deltas']),
            'first_cumulative_departure_difference_tick':min(different),
            'max_absolute_cumulative_departure_difference':maxmag,
            'extremum_first_tick':extrema[0], 'extremum_tick_204':204 in extrema,
            'windows':reconstructed,'total_delta':sum(signed_by_tick.values()),
            'proof':'For identical arrivals A(t), after-tick occupancy N_p(t)=A(t)-D_p(t). So N_a(t)-N_b(t)=D_b(t)-D_a(t), and its time integral equals total vehicle-seconds difference. With full clearing and matched IDs, total difference also equals sum_i(exit_a(i)-exit_b(i)).',
            'limits':'Known queueing mass-balance identity; not a novel finding or independently validated causal mechanism.'}
    (HERE/'P125_RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()

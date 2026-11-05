"""Deterministic source-declared geometric counterexample audit (no vehicle run)."""
from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from lane_boundary import audit_boundary_seams,sample_lane_strip
from road_integrity import full_audit


def road(name,x,y,z,hdg,width):
    return f'<road id="{name}" length="10" junction="-1"><planView><geometry s="0" x="{x}" y="{y}" hdg="{hdg}" length="10"><line/></geometry></planView><elevationProfile><elevation s="0" a="{z}" b="0" c="0" d="0"/></elevationProfile><lanes><laneSection s="0"><right><lane id="-1" type="driving"><width sOffset="0" a="{width}" b="0" c="0" d="0"/></lane></right></laneSection></lanes></road>'

def document(x=10,z=0,heading=0,width=3.5):
    return '<OpenDRIVE><header revMajor="1" revMinor="8"/>'+road('A',0,0,0,0,3.5)+road('B',x,0,z,heading,width)+'<junction id="j"><connection incomingRoad="A" connectingRoad="B" contactPoint="start"><laneLink from="-1" to="-1"/></connection></junction></OpenDRIVE>'


def main():
    cases={'continuous_reference':document(),
           'xy_disconnected':document(x=12),
           'vertical_disconnected':document(z=2),
           'heading_kink':document(heading=.4),
           'lane_width_mismatch':document(width=2.5)}
    result={key:audit_boundary_seams(value) for key,value in cases.items()}
    old={key:full_audit(value) for key,value in cases.items()}
    witness={key:r['findings'][0]['code'] for key,r in result.items()}
    assert witness['continuous_reference']=='GEOMETRIC_SEAM_MATCH_ONLY'
    assert 'VERTICAL_GAP' in witness['vertical_disconnected']
    assert 'HEADING_KINK_OR_REVERSE' in witness['heading_kink']
    assert 'WIDTH_MISMATCH' in witness['lane_width_mismatch']
    assert 'BOUNDARY_GAP' in witness['xy_disconnected']
    output={'date':'2026-11-05','study':'T2 v6.10-J P11-J',
            'kind':'SYNTHETIC_SOURCE_DECLARED_GEOMETRY_AUDIT',
            'scenario_count':len(cases),'witness_codes':witness,'outcomes':result,
            'matched_previous_I_audit':old,
            'previous_I_failure_counts':{k:v['fail_count'] for k,v in old.items()},
            'new_J_failure_counts':{k:sum(f['status']=='FAIL' for f in v['findings']) for k,v in result.items()},
            'strip_25':sample_lane_strip(cases['continuous_reference'],'A',-1,n=25),
            'actual_opendrive_original_input_used':False,
            'independent_sumo_vehicle_simulation':False,
            'traffic_policy_executed':False,
            'physical_or_legal_clearance_certified':False}
    (ROOT/'results'/'boundary_audit.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'scenarios':len(cases),'codes':witness,'source_original':False},ensure_ascii=False,indent=2))

if __name__=='__main__':main()

"""Deterministic synthetic OpenDRIVE structural audit. No traffic-policy execution."""
import json
from pathlib import Path
from opendrive_ir import parse_xodr

SAMPLE='''<OpenDRIVE><header revMajor="1" revMinor="8"/>
<road id="A" length="20" junction="-1"><planView><geometry s="0" x="0" y="0" hdg="0" length="20"><line/></geometry></planView><elevationProfile><elevation s="0" a="3" b="0.02" c="0" d="0"/></elevationProfile><lanes><laneSection s="0"><right><lane id="-1" type="driving"><width sOffset="0" a="3.5" b="0" c="0" d="0"/></lane></right></laneSection></lanes></road>
<road id="B" length="10" junction="1"><planView><geometry s="0" x="20" y="0" hdg="0" length="10"><arc curvature="0.05"/></geometry></planView><elevationProfile><elevation s="0" a="3.4" b="0" c="0" d="0"/></elevationProfile><lanes><laneSection s="0"><right><lane id="-1" type="driving"><width sOffset="0" a="3.5" b="0" c="0" d="0"/></lane></right></laneSection></lanes></road>
<junction id="1"><connection id="0" incomingRoad="A" connectingRoad="B" contactPoint="start"><laneLink from="-1" to="-1"/></connection></junction></OpenDRIVE>'''

def run():
    a=parse_xodr(SAMPLE)
    return {'audit_kind':'synthetic OpenDRIVE reference-line and explicit junction lane link',
            'summary':a.summary(), 'A_start':a.roads[0].reference_at(0),
            'A_end':a.roads[0].reference_at(20),
            'B_end':a.roads[1].reference_at(10),
            'width_m_A_at_s10':a.roads[0].lane_at(10,-1).width_at(10),
            'unresolved':list(a.unresolved),'sumo_executed':False,'policy_frozen':True}
if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]; (root/'results').mkdir(exist_ok=True)
    result=run();(root/'results'/'audit.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(result,indent=2,ensure_ascii=False))

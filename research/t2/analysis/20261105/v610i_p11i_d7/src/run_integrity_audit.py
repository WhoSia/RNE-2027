"""Independent synthetic counterexample suite; does not simulate vehicles."""
import json
from pathlib import Path
from road_integrity import full_audit

X='''<OpenDRIVE><header revMajor="1" revMinor="8"/><road id="A" length="10" junction="-1"><planView><geometry s="0" x="0" y="0" hdg="0" length="10"><line/></geometry></planView><elevationProfile><elevation s="0" a="0" b="0" c="0" d="0"/></elevationProfile><lanes><laneSection s="0"><right><lane id="-1" type="driving"><width sOffset="0" a="3.5" b="0" c="0" d="0"/></lane></right></laneSection></lanes></road><road id="B" length="10" junction="j"><planView><geometry s="0" x="10" y="0" hdg="0" length="10"><line/></geometry></planView><elevationProfile><elevation s="0" a="0" b="0" c="0" d="0"/></elevationProfile><lanes><laneSection s="0"><right><lane id="-1" type="driving"><width sOffset="0" a="3.5" b="0" c="0" d="0"/></lane></right></laneSection></lanes></road><junction id="j"><connection id="c" incomingRoad="A" connectingRoad="B" contactPoint="start"><laneLink from="-1" to="-1"/></connection></junction></OpenDRIVE>'''

def main():
    normal=full_audit(X)
    hidden=full_audit(X.replace('a="3.5" b="0" c="0" d="0"','a="24" b="-10" c="1" d="0"',1))
    distant=full_audit(X.replace('x="10" y="0"','x="30" y="0"',1))
    assert normal['fail_count']==0 and normal['unknown_count']==1
    assert any(q['code']=='WIDTH_NONPOSITIVE' for q in hidden['width_findings'])
    assert any(q['code']=='ROAD_REFERENCE_GAP' for q in distant['link_findings'])
    result={'date':'2026-11-05','engine':'OpenDRIVE subset, synthetic input only','policy_executed':False,'actual_source_xodr_tested':False,
            'normal':normal,'interior_negative_width':hidden,'distant_but_declared_connected':distant}
    target=Path(__file__).resolve().parents[1]/'results'/'integrity_audit.json'
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('PASS synthetic reference and two discriminating counterexamples',target)
if __name__=='__main__':main()

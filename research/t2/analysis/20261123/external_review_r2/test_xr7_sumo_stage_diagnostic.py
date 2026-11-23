"""Synthetic arithmetic tests only, NOT an actual SUMO parity test."""
from xr7_sumo_stage_diagnostic import analyze

def test_stage_identity_all_ids():
    tape=[(0,'L'),(1,'S')]
    ref={'admit':{0:5,1:4},'cross':{0:10,1:12},'exit':{0:20,1:22}}
    depart={'v00':6,'v01':4}
    crossing={'v00':13,'v01':14}
    exits={'v00':25,'v01':29}
    r=analyze(tape,ref,depart,crossing,exits)
    assert r['status']=='XR7_PER_ID_DIAGNOSTIC_COMPLETE'
    assert r['matched_vehicles']==2
    assert r['rows'][0]['admission_error_s']==1
    assert r['rows'][0]['upstream_segment_error_s']==2
    assert r['rows'][0]['receiver_segment_error_s']==2
    assert r['rows'][0]['exit_error_s']==5
    assert r['rows'][1]['exit_error_s']==7
    assert not r['policy_sign_comparison_allowed']

def test_missing_ids_hard_fail():
    tape=[(0,'L'),(1,'S')]
    ref={'admit':{0:5,1:4},'cross':{0:10,1:12},'exit':{0:20,1:22}}
    r=analyze(tape,ref,{'v00':6,'v01':4},{'v00':13,'v01':14},{'v00':25})
    assert r['status']=='XR7_MISSING_ID_TIMESTAMPS'
    assert r['missing_per_id']=={'v01':['sumo_exit']}
    assert not r['gates']['D1_all_ids_have_all_timestamps']
    assert not r['policy_sign_comparison_allowed']

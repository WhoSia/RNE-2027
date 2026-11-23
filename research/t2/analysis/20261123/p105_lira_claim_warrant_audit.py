"""P105 LIRA: evidence-bound claim adoption register over P35/P36/P37/P38/P101/P102.

LIRA is CURRENT RECOMMENDATION TO RETAIN A SCOPED CLAIM (0..1), NOT
probability of truth, probability of acceptance or an author's probability.
Any source modification fails before scoring. Run in this folder:
  python p105_lira_claim_warrant_audit.py > P105_LIRA_RESULT.json
"""
import json
from pathlib import Path
from collections import Counter

BASE = Path(__file__).resolve().parent
KEEP = 0.80


def load(name):
    return json.loads((BASE / name).read_text(encoding='utf8'))


def claim(id, statement, decision, score, priority, evidence, warrant,
          rival, failure_gate, scope):
    assert 0 <= score <= 1 and priority in ('P0', 'P1', 'P2', 'P3')
    assert decision in ('KEEP', 'HOLD', 'REJECT')
    if decision == 'KEEP':
        assert score >= KEEP, (id, score)
    else:
        assert score < KEEP, (id, score)
    return dict(id=id, claim=statement, lira=score, decision=decision,
                defect_severity=priority, evidence=evidence, warrant=warrant,
                rival=rival, change_to_reassess=failure_gate, scope=scope)


def experiment():
    a=load('P35_FORWARD_ONLY_TIMING_FULL_20261123.json')
    b=load('P36_CROSSWALK_RESULT.json')
    c=load('P37_NIGHT_ROUTE_RESULT.json')
    d=load('P38_GREEN_OBSERVATION_RESULT.json')
    p101=load('P101_RESULT.json')
    p102=load('P102_RESULT.json')
    assert a['crossings']==17 and len(a['event_records'])==17
    assert sum(x['status']=='UNMAPPED_SIGNAL_HEAD_TO_MOVEMENT' for x in a['event_records'])==17
    assert a['crossings_with_nearest_hindsight_sample_future']==11
    assert a['freshness_at_bracket_end']['1.0']['causally_fresh_crossings']==16
    assert (b['group_3_candidates'],b['group_4_candidates'],b['unmapped'])==(4,1,12)
    assert c['groups']['3']['windows_seconds']['40']['expected_only']==3
    assert c['groups']['4']['windows_seconds']['40']['expected_only']==1
    assert (d['green_bracket_slots'],d['frame_without_detected_crossing'],d['no_selected_frame'])==(292,114,176)
    assert (p101['summary']['red']['paradox'],p101['summary']['red']['n'])==(64,64)
    assert p101['summary']['red']['left_cost_positive']==64
    assert (p102['offsets'][1]['exact_sign'],p102['offsets'][1]['strict_opposite_sign'])==(2,40)

    claims=[
      claim('OBS01','There are 17 map-derived 50ms geometric stopline-center crossing candidates.',
            'KEEP',.96,'P2',['P35 event_records=17; each bracket 50ms'],
            'P34 geometry/P35 independent time-join source checks support exactly the candidate count.',
            '2015 map stripe need not equal 2023 physical paint.','Require independent surveyed 2023 line before upgrading to physical ground truth.','same-source geometric candidates'),
      claim('OBS02','At least one prior signal sample is no older than 1s at bracket end for 16/17 candidates.',
            'KEEP',.94,'P2',['P35 freshness_at_bracket_end[1.0]=16/17'],
            'Causally eligible sample at or before start of each 50ms bracket.',
            'Sampled code may change between observations.','Reassess with exact clock drift and controller event timestamps.','past sample freshness only'),
      claim('OBS03','Nearest-time matching can leak future information: 11/17 P35 candidates.',
            'KEEP',.95,'P1',['P35 crossings_with_nearest_hindsight_sample_future=11'],
            'Compare retrospective nearest timestamp to crossing time.',
            'Future time sample is not necessarily a different signal code.','Reassess with event-synchronous signal feed.','sampling leakage only'),
      claim('MAP01','A physical 2023 signal-head-to-movement mapping is established for 5 eastern candidates.',
            'REJECT',.12,'P0',['P36 five hypothetical lane-group candidates','P35 status unmapped 17/17'],
            'Lane-group hypotheses are not official controller head ownership.',
            'Historical daytime map transfer might be correct but is unverified.','Require independently surveyed controller-phase/approach mapping.','real controller mapping'),
      claim('PATH01','Four of five hypothesized eastern candidates follow expected ordered receiver-entry routes.',
            'KEEP',.86,'P2',['P37 3/4 group3; 1/1 group4, windows 10/20/40s'],
            'Sequential map-cell path support within same tracking source, not independent physical exit.',
            'Mapping and detection from the same map/tracking data create correlated errors.','Reassess using independent camera or verified end-of-link detections.','same-source route plausibility'),
      claim('EXIT01','Four route-compatible trajectories prove their final downstream segment exit times.',
            'REJECT',.06,'P0',['P37 route entry only','P80/P81 downstream terminal unobserved'],
            'Entry to receiver is not terminal departure.',
            'Fragmented track may be caused by capture boundaries, not blockage.','Acquire terminal crossing ID and synchronized end-of-link observation.','physical terminal event'),
      claim('GREEN01','All 292 observed green-bracket slots have valid classified simultaneous upstream/receiver frames.',
            'REJECT',.07,'P0',['P38 only 114 selected non-crossing frames; 176 none'],
            'Observed screen has missing and ambiguous intervals.',
            'Absence of one tracked center is not absence of traffic.','Create synchronized complete occupancy ground truth for denominator.','field blockage prevalence'),
      claim('GREEN02','No concurrently slow upstream and receiver center seen in 114 selected frames proves no blockage.',
            'REJECT',.04,'P0',['P38 4 slow-upstream-only, 0 both in 114 selected frames'],
            'Failure to detect is not a false-negative-bounded ground-truth classification.',
            'Field of view and timing selection are incomplete.','Calibrate detection sensitivity and label upstream/downstream occupancy.','field congestion diagnosis'),
      claim('SIM01','The P101 red-onset high-left-share 64/64 left-delay pattern is reproducible within the T2 model.',
            'KEEP',.92,'P2',['P101 64/64 red onset; 128/128 source-locked spatial identity'],
            'Matched P100 cohort, all 256 replay arms clear; same engine.',
            'Vehicle priority and 4-slot geometry may structurally generate pattern.','Reassess if physical geometry or independent-engine replication breaks it.','conditional simulator result'),
      claim('SIM02','P101 constitutes a fresh independent replication of P100.',
            'REJECT',.03,'P0',['P101 same 64 P100 tapes, explicit P101 prereg'],
            'Nested mechanism analysis does not create new independent sampling units.',
            'Separate tracing adds explanatory resolution, not independent sampling.','Use independent engine and distinct held-out locations.','evidence independence'),
      claim('EXT01','P71 SUMO comparisons directly falsify P100 downstream 30s vs 60s results.',
            'REJECT',.09,'P1',['P102 says P71 compares upstream left green 10s vs 6s'],
            'Treatment, downstream offset and physical geometry differ.',
            'P71 nonetheless motivates cross-engine concern.','Run P100 exact intervention with isomorphic independent simulation.','cross-engine transport'),
      claim('EXT02','Geometry-matched independent engine and mapped field exits are needed before real policy claims.',
            'KEEP',.96,'P1',['P102 P71 SUMO rank agreement 2/64 at offset15 under different intervention','P35 head ownership unknown'],
            'Current evidence does not identify physical policy causal impact.',
            'Independent engine alone would still not establish real intersection benefit.','Update after verified geometry parity and field head/end crossing.','research decision'),
      claim('TIME01','P99 identical signed costs after extending a fully-cleared horizon validates physical delay mechanisms.',
            'REJECT',.14,'P1',['P99 768/768 exact signed pair match after t1440→1464'],
            'No remaining vehicles means additional empty ticks add zero occupancy.',
            'It checks horizon bookkeeping, not physical fidelity.','Construct active-arrival near-horizon stress with terminal censor rules.','model validation strength'),
      claim('LIRA01','LIRA 0..1 is a present recommendation to retain the scope-limited claim, not a Bayesian probability.',
            'KEEP',.99,'P2',['research method: LIRA kept >=0.80'],
            'Scores are explicit editorial research judgments with rival and change trigger.',
            'No calibration claims.','Revise interpretation if original LIRA protocol changes.','research governance'),
    ]
    decisions=Counter(x['decision'] for x in claims)
    return dict(artifact='P105_LIRA_RESULT.json',protocol='P104 observational funnel + LIRA claim-warrant register',
                scores_are='current claim-adoption recommendation, NOT truth probabilities',
                retain_threshold=KEEP,source_files=['P35_FORWARD_ONLY_TIMING_FULL_20261123.json','P36_CROSSWALK_RESULT.json','P37_NIGHT_ROUTE_RESULT.json','P38_GREEN_OBSERVATION_RESULT.json','P101_RESULT.json','P102_RESULT.json'],
                field_counts={'crossings':17,'prior_1s':16,'east_hypotheses':5,'route_compatible':4,
                              'official_head_ownership':0,'confirmed_downstream_final_exits':0,
                              'green_slots':292,'no_selected_frame':176,'selected_noncrossing_frames':114},
                decision_counts=dict(decisions),claims=claims)

if __name__=='__main__':
    print(json.dumps(experiment(),indent=2,ensure_ascii=False))

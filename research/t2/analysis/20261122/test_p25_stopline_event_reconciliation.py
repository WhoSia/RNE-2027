"""P25 verified-source regression and adversarial counterexamples.
Run: python -m unittest -v test_p25_stopline_event_reconciliation.py
"""
import copy
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from datetime import datetime, timezone
from p25_stopline_event_reconciliation import (
    SHA,audit,markers_from_map,reference_volume_events,trajectory_crossings,
    reconcile,lane_spans,source_arm,lateral_lane,projected,
)

ROOT=Path('/mnt/data')
MAP=ROOT/'bs-inner-ring-road-ut.xodr.xml'
TRJ=ROOT/'trajectories_230924-233000_230924-234500.csv'
VOL=ROOT/'traffic-volume_230924-233000_230924-234500.csv'

class P25RealSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.res=audit(MAP,TRJ,VOL)
    def test_provenance_hashes(self):
        self.assertEqual(self.res['sources_sha256'],SHA)
    def test_source_row_and_marker_counts(self):
        self.assertEqual(self.res['observations'],{
            'trajectory_rows':8624,'object_ids':37,'volume_rows':893,
            'official_route_columns':12,'inbound_markers':4})
    def test_inbound_cardinal_source_arm(self):
        self.assertEqual({x['road_id']:x['source_arm'] for x in self.res['markers']},
            {'100000':'East','179000':'South','201000':'West','280000':'North'})
    def test_17_events_each_but_not_equal(self):
        c=self.res['counts']
        self.assertEqual((c['trajectory_crossings_direct'],c['official_center_point_crossings']),(17,17))
        self.assertEqual((c['one_to_one_approach_time_matches'],c['trajectory_only'],c['volume_only']),(16,1,1))
        self.assertEqual(len(set(x['crossing_index'] for x in self.res['matched_pairs'])),16)
        self.assertEqual(len(set(x['volume_index'] for x in self.res['matched_pairs'])),16)
    def test_unmatched_official_is_south_23_36_10(self):
        self.assertEqual(self.res['unmatched_official_volume'],[{
            'route':'South1West1','source_arm':'South','time_utc':'2023-09-24 23:36:10+00:00'}])
    def test_unmatched_cross_is_east_23_32_16(self):
        a=self.res['unmatched_trajectory_crossings']
        self.assertEqual(len(a),1)
        self.assertEqual((a[0]['road_id'],a[0]['id']),('100000','1695598300234044'))
        self.assertTrue(a[0]['crossing_time_utc'].startswith('2023-09-24T23:32:16.50'))
    def test_left_censor_candidate_not_counted_as_crossing(self):
        x=self.res['left_censor_candidates']
        self.assertEqual(len(x),1)
        self.assertEqual(x[0]['conclusion'],'UNCERTAIN_LEFT_CENSOR_NOT_CONFIRMED_CROSSING')
        self.assertEqual(x[0]['candidate_first_observation_after_line'][0]['id'],'1695598569934245')
        self.assertTrue(x[0]['candidate_first_observation_after_line'][0]['first_signed_dist_m']>0)
    def test_lane_validity_rejects_real_consistent_events(self):
        self.assertEqual(self.res['counts']['within_2015_marker_laneValidity'],7)
        agree=[x for x in self.res['crossings'] if x['map_lane_validity_agrees']]
        self.assertEqual(len(agree),7)
        self.assertEqual(sum(self.res['crossings'][x['crossing_index']]['map_lane_validity_agrees'] for x in self.res['matched_pairs']),6)
    def test_real_brackets_and_motor_status(self):
        self.assertEqual(self.res['counts']['excluded_interpolation_or_large_gaps'],0)
        self.assertTrue(all(abs(x['bracket_width_ms']-50)<0.0001 for x in self.res['crossings']))
        self.assertEqual(set(x['class'] for x in self.res['crossings']),{'car','truck','van'})
        self.assertTrue(all(x['map_lane_id'] < 0 for x in self.res['crossings']))
    def test_same_sensor_not_field_truth(self):
        self.assertFalse(self.res['gates']['independent_real_world_truth_verified'])
        self.assertFalse(self.res['gates']['controlling_signal_id_verified'])
        self.assertTrue(all(x['vehicle_movement'] is None for x in self.res['crossings']))
        self.assertTrue(all(x['controlling_signal_id'] is None for x in self.res['crossings']))
    def test_source_sha_reject_wrong_trajectory(self):
        with self.assertRaises(ValueError):audit(MAP,VOL,VOL)
    def test_source_sha_reject_wrong_volume(self):
        with self.assertRaises(ValueError):audit(MAP,TRJ,TRJ)
    def test_source_sha_reject_wrong_map(self):
        with self.assertRaises(ValueError):audit(VOL,TRJ,VOL)

class P25SyntheticAdversarialTests(unittest.TestCase):
    @staticmethod
    def mini(microtime,x,y,interpolated='False',person=False):
        return {'timestamp':'2023-09-24T23:30:'+microtime+'+00:00',
            'id':'vehicle1','center_easting':str(x),'center_northing':str(y),
            'classifications_car':'0' if person else '1',
            'classifications_truck':'0','classifications_van':'0',
            'classifications_motorbike':'0','classifications_pedestrian':'1' if person else '0',
            'classifications_bicycle':'0','interpolated':interpolated}
    @staticmethod
    def marker():
        return {'road_id':'1','feature_id':'5','source_arm':'West',
            'easting':0.0,'northing':0.0,'heading':0.0,
            'lane_validity_ranges':[(-1,-1)],
            'lane_spans':[{'lane_id':-1,'type':'driving','t_min':-4,'t_max':0}]}
    @staticmethod
    def cc(t,arm='West'):
        return {'crossing_time_utc':'2023-09-24T23:30:'+t+'+00:00','source_arm':arm}
    @staticmethod
    def vv(t,arm='West'):
        return {'time_utc':'2023-09-24T23:30:'+t+'+00:00','source_arm':arm}
    def test_no_reverse_crossing(self):
        a,b=self.mini('00.000000',1,-2),self.mini('00.050000',-1,-2)
        x,_,_,_=trajectory_crossings([self.marker()],[a,b])
        self.assertEqual(x,[])
    def test_nominal_forward_crossing(self):
        a,b=self.mini('00.000000',-1,-2),self.mini('00.050000',1,-2)
        x,gaps,_,_=trajectory_crossings([self.marker()],[a,b])
        self.assertEqual(len(x),1)
        self.assertEqual(gaps,[])
        self.assertEqual(x[0]['map_lane_id'],-1)
        self.assertEqual(x[0]['bracket_width_ms'],50.)
    def test_no_pedestrian_in_vehicle_counts(self):
        a,b=self.mini('00.000000',-1,-2,person=True),self.mini('00.050000',1,-2,person=True)
        x,_,_,_=trajectory_crossings([self.marker()],[a,b])
        self.assertFalse(x)
    def test_gaps_are_uncertain_not_events(self):
        a,b=self.mini('00.000000',-1,-2),self.mini('01.000000',1,-2)
        x,gaps,_,_=trajectory_crossings([self.marker()],[a,b])
        self.assertFalse(x)
        self.assertEqual(gaps[0]['status'],'UNOBSERVED_CROSSING_IN_TEMPORAL_GAP')
    def test_interpolated_observation_excluded(self):
        a,b=self.mini('00.000000',-1,-2),self.mini('00.050000',1,-2,'True')
        x,gaps,_,_=trajectory_crossings([self.marker()],[a,b])
        self.assertFalse(x)
        self.assertEqual(gaps[0]['status'],'INTERPOLATED_SAMPLE_NOT_DIRECT_EVIDENCE')
    def test_lateral_outside_drivable_bounds(self):
        a,b=self.mini('00.000000',-1,-7),self.mini('00.050000',1,-7)
        x,_,_,_=trajectory_crossings([self.marker()],[a,b])
        self.assertFalse(x)
    def test_maximum_cardinality_not_greedy_nearest(self):
        # A naive greedy min delta pairs 00.8 -> 01.2 and loses 01.5.
        c=[self.cc('00.800000'),self.cc('01.500000')]
        v=[self.vv('00.000000'),self.vv('01.200000')]
        matches,uc,uv=reconcile(c,v)
        self.assertEqual(len(matches),2)
        self.assertFalse(uc)
        self.assertFalse(uv)
        self.assertEqual({(x['crossing_index'],x['volume_index']) for x in matches},{(0,0),(1,1)})
    def test_source_arm_prevents_false_near_match(self):
        c=[self.cc('00.200000','East')]
        v=[self.vv('00.300000','West')]
        match,uc,uv=reconcile(c,v)
        self.assertEqual((len(match),uc,uv),(0,[0],[0]))
    def test_one_to_one_matching_even_for_identical_times(self):
        c=[self.cc('00.500000') for _ in range(3)]
        v=[self.vv('00.500000') for _ in range(2)]
        match,uc,uv=reconcile(c,v)
        self.assertEqual((len(match),len(uc),len(uv)),(2,1,0))
    def test_far_apart_no_match(self):
        match,uc,uv=reconcile([self.cc('00.000000')],[self.vv('02.000000')])
        self.assertEqual((len(match),uc,uv),(0,[0],[0]))

if __name__=='__main__':unittest.main()

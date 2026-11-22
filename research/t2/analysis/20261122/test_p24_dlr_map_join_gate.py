import hashlib
import os
import unittest
from pathlib import Path
from p24_dlr_map_join_gate import audit_map, locked, pdf_vehicle_heads, MOVEMENT_RE, VOLUME_SHA

B=Path(os.environ.get('P24_RAW_DIR','/mnt/data'))
MAP=B/'bs-inner-ring-road-ut.xodr.xml'
PDF=B/'DLR-Urban-Traffic-dataset_v1-3-1_documentation.pdf'
TRAJ=B/'trajectories_230924-233000_230924-234500.csv'
V={'12:00':(B/'traffic-volume_230924-120000_230924-121500.csv',VOLUME_SHA['12:00']),
   '18:00':(B/'traffic-volume_230924-180000_230924-181500.csv',VOLUME_SHA['18:00']),
   '23:30':(B/'traffic-volume_230924-233000_230924-234500.csv',VOLUME_SHA['23:30'])}

class PhysicalMapJoinGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.missing=[str(p) for p in [MAP,PDF,TRAJ]+[v[0] for v in V.values()] if not p.is_file()]
        if not cls.missing:cls.result=audit_map(MAP,PDF,TRAJ,V)
    def require(self):
        if self.missing:self.skipTest('Not mounted: '+','.join(self.missing))
    def test_official_18_vehicle_heads_and_9_ids(self):
        self.require()
        heads=pdf_vehicle_heads(PDF)
        self.assertEqual(len(heads),18)
        self.assertEqual({r[0] for r in heads},set(range(1,10)))
    def test_correct_PDF_sha(self):
        self.require()
        self.assertEqual(hashlib.sha256(PDF.read_bytes()).hexdigest(),
                         '94fd9ebd32d04a9c35b02be526fbd11a8d5a613933d7961fde800386853b34f3')
    def test_no_false_join_to_static_map_signs(self):
        self.require()
        r=self.result
        self.assertEqual(r['direct_numeric_signal_identifier_matches'],[])
        self.assertEqual((r['open_drive']['map_signal_count'],r['open_drive']['dynamic_controller_count']),(7,0))
        self.assertFalse(r['gates']['controlling_signal_head_per_movement'])
    def test_all_trajectory_points_inside_map_bbox_only(self):
        self.require()
        self.assertEqual(self.result['night_trajectory_positions_within_map_bbox'],{'inside':8624,'observations':8624})
        self.assertFalse(self.result['gates']['matched_vehicle_stopline_crossings'])
    def test_variable_movement_schema(self):
        self.require()
        self.assertEqual([self.result['published_volume_route_tokens'][k]['movement_columns'] for k in V],[32,27,12])
        self.assertFalse(self.result['gates']['movement_token_to_openDRIVE_lane_id'])
    def test_same_direction_route_can_exist(self):
        self.require()
        self.assertIn('West0West1',self.result['published_volume_route_tokens']['12:00']['route_labels'])
        self.assertIsNotNone(MOVEMENT_RE.fullmatch('West0West1'))
    def test_unknown_route_name_rejected(self):
        self.assertIsNone(MOVEMENT_RE.fullmatch('EastABC'))
        self.assertIsNone(MOVEMENT_RE.fullmatch('Fake2West3'))
    def test_byte_mismatch_rejected(self):
        self.require()
        with self.assertRaises(ValueError):locked(PDF,'0'*64)
        with self.assertRaises(ValueError):locked(MAP,'0'*64)
    def test_UTM_offset_validated(self):
        self.require()
        h=self.result['official_publisher_vehicle_heads'][0]
        self.assertAlmostEqual(h['map_local_x'],h['easting']-604763,3)
        self.assertAlmostEqual(h['map_local_y'],h['northing']-5792795,3)
if __name__=='__main__':unittest.main(verbosity=2)

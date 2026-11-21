import csv
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from p23_map_volume_alignment import inspect, map_geometry, observed, seal

BASE=Path(os.environ.get('P23_SOURCE_DIR','/mnt/data'))
MAP=BASE/'bs-inner-ring-road-ut.xodr.xml'
TRACK=BASE/'trajectories_230924-233000_230924-234500.csv'
VOL=BASE/'traffic-volume_230924-233000_230924-234500.csv'

class MapVolumeTest(unittest.TestCase):
    def test_full_real_source_alignment(self):
        if not all(x.is_file() for x in (MAP,TRACK,VOL)):
            self.skipTest('Three exact Drive originals not mounted')
        r=inspect(MAP,TRACK,VOL)
        self.assertEqual((r['trajectory_rows_all'],r['observed_ids_all']),(8624,37))
        self.assertEqual(r['centerline_distance']['within_10m'],8389)
        self.assertEqual(r['centerline_distance']['within_5m'],6962)
        self.assertEqual(r['centerline_distance']['within_20m'],8624)
        self.assertEqual(r['volume']['crossing_bins'],17)
        self.assertEqual(r['volume']['seconds'],893)
        self.assertEqual(r['volume']['movement_columns'],12)
        self.assertEqual(r['map']['roads'],28)
    def test_negative_control_breaks_near_centerline(self):
        if not all(x.is_file() for x in (MAP,TRACK,VOL)):
            self.skipTest('Originals missing')
        r=inspect(MAP,TRACK,VOL,stride=10)
        self.assertGreater(r['centerline_distance']['within_10m'],r['exploratory_negative_control_shift_easting_100m']['within_10m'])
    def test_map_signal_ids_not_real_time_ids(self):
        if not MAP.is_file():self.skipTest('Map missing')
        _,_,info=map_geometry(MAP)
        self.assertEqual(info['static_signal_elements'],7)
        self.assertEqual(info['static_signal_unique_ids'],6)
    def test_epsg32632_transform_landmark(self):
        if not MAP.is_file():self.skipTest('Map missing')
        _,t,_=map_geometry(MAP)
        x,y=t.transform(604746.796,5792790.916)
        self.assertAlmostEqual(x,-16.204,places=4)
        self.assertAlmostEqual(y,-4.084,places=4)
    def test_invalid_sampling_stride(self):
        for stride in (0,-1,True,1.5):
            with self.assertRaises(ValueError):inspect(MAP,TRACK,VOL,stride)
    def test_raw_source_wrong_hash_rejected(self):
        if not VOL.is_file():self.skipTest('Volume missing')
        with patch('p23_map_volume_alignment.SOURCES',{'volume':'0'*64}):
            with self.assertRaises(ValueError):observed(VOL,'volume')
    def test_volume_no_traffic_junction_link_claim(self):
        if not all(x.is_file() for x in (MAP,TRACK,VOL)):
            self.skipTest('Originals missing')
        r=inspect(MAP,TRACK,VOL,stride=20)
        self.assertIn('Static OpenDRIVE road signal IDs are not proven to match 30 dynamic CSV signal IDs',r['limitations'])
        self.assertEqual(r['volume']['active_movement_columns'],12)

if __name__=='__main__':unittest.main()

"""Deterministic tests. Run python -m unittest -v in this directory."""
import tempfile
from pathlib import Path
import unittest
from datetime import datetime
from audit_dlr_case import nearest_second, audit_signals, audit_xodr, audit_volume

class AuditTests(unittest.TestCase):
    def test_nearest_second_not_floor(self):
        x=datetime.fromisoformat("2023-09-24T12:00:00.991+00:00")
        self.assertEqual(nearest_second(x).second,1)
        self.assertEqual(x.replace(microsecond=0).second,0)

    def test_signal_collision_floor_vs_nearest(self):
        with tempfile.TemporaryDirectory() as p:
            fn=Path(p)/"signals.csv"
            lines=["timestamp,id,state"]
            for t in ["2023-09-24T12:00:01.001+00:00","2023-09-24T12:00:01.998+00:00"]:
                lines += [f"{t},{i},3" for i in range(1,31)]
            fn.write_text("\n".join(lines)+"\n")
            r=audit_signals(fn)
            self.assertEqual(r["floor_colliding_second_buckets"],1)
            self.assertEqual(r["nearest_second_colliding_buckets"],0)

    def test_signal_reject_partial_30(self):
        with tempfile.TemporaryDirectory() as p:
            f=Path(p)/"t.csv"
            f.write_text("timestamp,id,state\n2023-09-24 12:00:00+00:00,1,3\n")
            with self.assertRaises(ValueError):audit_signals(f)

    def test_volume_reject_short_and_unsorted(self):
        with tempfile.TemporaryDirectory() as p:
            f=Path(p)/"v.csv"
            f.write_text("timestamp,A\n2023-09-24 12:00:00+00:00,2\n")
            with self.assertRaises(ValueError):audit_volume(f)

    def test_volume_900_and_schema(self):
        with tempfile.TemporaryDirectory() as p:
            f=Path(p)/"v.csv"
            rows=["timestamp,A,B"]+[f"2023-09-24 12:{i//60:02}:{i%60:02}+00:00,{i%2},0" for i in range(900)]
            f.write_text("\n".join(rows)+"\n")
            r=audit_volume(f)
            self.assertEqual(r["total_publisher_volume"],450)
            self.assertEqual(r["movement_columns"],2)

    def test_xodr_schema(self):
        with tempfile.TemporaryDirectory() as p:
            f=Path(p)/"r.xodr"
            f.write_text('<OpenDRIVE><header version="1"/><road id="1"/><junction id="2"><connection/></junction></OpenDRIVE>')
            r=audit_xodr(f)
            self.assertEqual((r["roads"],r["junctions"],r["junction_connections"]),(1,1,1))
if __name__=="__main__":
    unittest.main()

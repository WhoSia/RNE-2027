import csv,io,unittest
from jinju_audit import audit,HEADER

def fixture(*rows):
    s=io.StringIO(); w=csv.writer(s);w.writerow(HEADER);w.writerows(rows);return s.getvalue().encode('cp949')

def row(a='2025-11-01 00:00:01',b='2025-11-01 00:00:58',v='1/2/3/4/5/6',t='10/0/0/0/0/0/0'):
    return [a,b,'synthetic', '1',v,t]+['']*10

class AuditTest(unittest.TestCase):
    def test_semantic_sums(self):
        r=audit(fixture(row())); self.assertEqual(r['counts']['movement_type_agree'],1);self.assertEqual(r['counts']['all_six_type_agree'],0);self.assertEqual(r['arithmetic_sums_not_unique_vehicle_counts']['movement_subtotal'],10)
    def test_duplicate(self):
        r=audit(fixture(row(),row()));self.assertEqual(r['counts']['duplicate_rows'],1);self.assertEqual(r['same_site_interval_relations']['overlap'],1)
    def test_zero_duration(self):
        r=audit(fixture(row(b='2025-11-01 00:00:01')));self.assertEqual(r['same_site_interval_relations']['zero_duration'],1)
    def test_missing_and_extra(self):
        a=row(v='');a[6]='0/0/0/0/0/0';r=audit(fixture(a));self.assertEqual(r['counts']['missing_declared_pair'],1);self.assertEqual(r['counts']['unexpected_populated_unused'],1)
    def test_bad_vector(self):
        for v in ('1/2','1/2/3/4/-1/6','1/2/3/4/5/x'):
            with self.assertRaises(ValueError):audit(fixture(row(v=v)))
    def test_reversed(self):
        with self.assertRaises(ValueError):audit(fixture(row(b='2025-10-31 00:00:00')))
    def test_mismatch(self):
        r=audit(fixture(row(t='9/0/0/0/0/0/0')));self.assertEqual(r['movement_minus_type_histogram'],{1:1})
    def test_bad_header(self):
        with self.assertRaises(ValueError):audit(b'x,y\n')
if __name__=='__main__':unittest.main()

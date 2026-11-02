import csv,os,tempfile,unittest
from field_v40 import FIELDS,read,audit,holdout
class Tests(unittest.TestCase):
 def setUp(self):
  self.f=tempfile.NamedTemporaryFile('w',delete=False,newline='',encoding='utf-8');w=csv.writer(self.f);w.writerow(FIELDS)
  self.keys=[('C','2026-11-01','AM','J1','N','TH'),('C','2026-11-02','AM','J1','N','TH')]
  w.writerow([*self.keys[0],0,300,8,6,1,3]);w.writerow([*self.keys[0],300,600,7,8,3,2]);w.writerow([*self.keys[1],0,300,9,6,2,5]);self.f.close()
 def tearDown(self):os.unlink(self.f.name)
 def test_read(self):self.assertEqual(len(read(self.f.name)[0]),3)
 def test_balance(self):self.assertEqual([x['queue_residual'] for x in audit(read(self.f.name)[0])],[0,0,0])
 def test_holdout(self):
  k=(*self.keys[1],0,300);self.assertEqual(holdout({k:7},read(self.f.name)[0],'2026-11-02')['MAE_vehicles_per_window'],1)
 def test_missing(self):
  with self.assertRaises(ValueError):holdout({},read(self.f.name)[0],'2026-11-02')
 def test_duplicate(self):
  with open(self.f.name) as f:s=f.readlines()[-1]
  with open(self.f.name,'a') as f:f.write(s)
  with self.assertRaises(ValueError):read(self.f.name)
 def test_overlap(self):
  with open(self.f.name,'a') as f:f.write(','.join(self.keys[1])+',100,400,1,1,0,0\n')
  with self.assertRaises(ValueError):read(self.f.name)
 def test_boundary(self):
  with open(self.f.name) as f:s=f.read().replace('300,600,7,8,3,2','300,600,7,8,7,6')
  with open(self.f.name,'w') as f:f.write(s)
  self.assertEqual(len(read(self.f.name)[1]),1)
 def test_nonnumeric(self):
  with open(self.f.name) as f:s=f.read().replace('0,300,8,6,1,3','0,300,abc,6,1,3')
  with open(self.f.name,'w') as f:f.write(s)
  with self.assertRaises(ValueError):read(self.f.name)
 def test_no_zero_division(self):
  k=(*self.keys[1],0,300);self.assertEqual(holdout({k:6},read(self.f.name)[0],'2026-11-02')['WAPE'],0)
if __name__=='__main__':unittest.main()

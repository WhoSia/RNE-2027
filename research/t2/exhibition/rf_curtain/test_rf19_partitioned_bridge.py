import unittest
from rf19_partitioned_bridge import aggregate, domains, expected, join_training, load_streams, LABELS, WIRE


def fixture(partition):
    plan=[]; windows=[]; streams={}; truth=[]
    for s in ('S1','S2','S3'):
        for p in ('P1','P2'):
            for i in range(1,51):
                tid=f'{s}_{p}_{i:03d}'
                plan.append(dict(trial_id=tid,session_id=s,placement_id=p))
    ids=expected(plan,partition)
    for tid,cell in ids.items():
        i=int(tid[-3:]); k=(i-1)%5; start=10*i
        truth.append(dict(trial_id=tid,label=LABELS[k],ground_truth_source='manual_model_state'))
        for lid in ('1','2'):
            windows.append(dict(trial_id=tid,session_id=cell[0],placement_id=cell[1],trial_origin='synthetic_test_fixture',link_id=lid,start_us=start,stop_us=start+5))
            streams.setdefault((*cell,lid),[]).extend(dict(timestamp_us=start+j,rssi=-60,mean_amplitude=a) for j,a in enumerate((20-k,20+k),1))
    return plan,windows,streams,truth


class RF19Tests(unittest.TestCase):
    def test_training_and_holdout_same_formula(self):
        for partition,n in [('train',100),('holdout',150)]:
            plan,w,s,t=fixture(partition); rows=aggregate(plan,w,s,partition)
            self.assertEqual(len(rows),n)
            for r in rows:
                self.assertEqual(set(r),set(WIRE))
                self.assertEqual(r['csi_1_amp_dispersion'],(int(r['trial_id'][-3:])-1)%5)
            if partition=='train':self.assertEqual(len(join_training(plan,rows,t)),100)
    def test_missing_domain_preserves_denominator(self):
        p,w,s,t=fixture('holdout');s['S3','P2','1']=[]
        rows=aggregate(p,w,s,'holdout');self.assertEqual(sum(r['quality']=='missing' for r in rows),50)
    def test_clock_reset_within_domain_rejected(self):
        p,w,s,t=fixture('train');s['S1','P1','1'].reverse()
        with self.assertRaises(ValueError):aggregate(p,w,s,'train')
    def test_overlap_and_wrong_partition(self):
        p,w,s,t=fixture('train');w[2]['start_us']=w[0]['start_us'];w[2]['stop_us']=w[0]['stop_us']
        with self.assertRaises(ValueError):aggregate(p,w,s,'train')
        p,w,s,t=fixture('train');w[0]['trial_id']='S3_P2_001'
        with self.assertRaises(ValueError):aggregate(p,w,s,'train')
    def test_truth_leak_and_wrong_truth_denominator(self):
        p,w,s,t=fixture('train');rows=aggregate(p,w,s,'train')
        for bad in (t[:-1],t+[t[0]],[dict(t[0],label='free')]+t[1:],[dict(t[0],secret='free')]+t[1:]):
            with self.assertRaises(ValueError):join_training(p,rows,bad)
        w[0]['label']='free'
        with self.assertRaises(ValueError):aggregate(p,w,s,'train')
    def test_path_reuse_and_permission(self):
        p,w,s,t=fixture('train');ids=expected(p,'train');paths=dict.fromkeys(domains(ids),'same.csv')
        def loader(*args,**kw):self.fail('invalid contract invoked parser')
        with self.assertRaises(ValueError):load_streams(paths,ids,authorized_lab=True,loader=loader)
        with self.assertRaises(PermissionError):load_streams(paths,ids,authorized_lab=False,loader=loader)
    def test_explicit_missing_loader(self):
        p,w,s,t=fixture('train');ids=expected(p,'train');paths=dict.fromkeys(domains(ids),None)
        self.assertEqual(load_streams(paths,ids,authorized_lab=True,loader=lambda *a,**k:self.fail('missing invoked parser')),dict.fromkeys(domains(ids),[]))

if __name__=='__main__':unittest.main()

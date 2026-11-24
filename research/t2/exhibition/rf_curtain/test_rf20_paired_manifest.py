import json
import tempfile
import unittest
from pathlib import Path
from rf20_paired_manifest import DOMAINS, digest, snapshots, run_pair

class RF20Tests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup);self.root=Path(self.t.name)
        def put(name):
            p=self.root/name;p.write_bytes(name.encode());return {'path':name,'sha256':digest(p.read_bytes())}
        self.doc={k:put(k) for k in ('plan','train_windows','holdout_windows','train_truth')}
        self.doc['raw']={k:put(k.replace('/','_')) for k in sorted(DOMAINS)}
        self.manifest=self.root/'manifest.json';self.out=self.root/'out'
    def seal(self):
        b=json.dumps(self.doc).encode();self.manifest.write_bytes(b);return digest(b)
    def verify(self):
        h=self.seal();return snapshots(self.root,self.manifest.read_bytes(),h)
    def test_complete_and_missing(self):
        self.assertEqual(len(self.verify()['raw']),10)
        self.doc['raw'][sorted(DOMAINS)[0]]=None
        self.assertEqual(sum(v is None for v in self.verify()['raw'].values()),1)
    def test_cross_partition_reuse(self):
        a,b=sorted(DOMAINS)[0],sorted(DOMAINS)[-1]
        self.doc['raw'][b]=dict(self.doc['raw'][a])
        with self.assertRaises(ValueError):self.verify()
        self.doc['raw'][b]['path']='clone';(self.root/'clone').write_bytes((self.root/self.doc['raw'][a]['path']).read_bytes())
        with self.assertRaises(ValueError):self.verify()
    def test_digest_and_schema(self):
        h=self.seal();(self.root/'plan').write_bytes(b'changed')
        with self.assertRaises(ValueError):snapshots(self.root,self.manifest.read_bytes(),h)
        with self.assertRaises(ValueError):snapshots(self.root,self.manifest.read_bytes(),'0'*64)
        self.doc['holdout_truth']=self.doc['train_truth']
        with self.assertRaises(ValueError):self.verify()
    def test_duplicate_key(self):
        b=b'{"raw":{},"raw":{}}'
        with self.assertRaises(ValueError):snapshots(self.root,b,digest(b))
    def test_path_escape(self):
        self.doc['plan']['path']='../not_allowed'
        with self.assertRaises(ValueError):self.verify()
    def test_snapshot_adapter_doubles(self):
        h=self.seal();calls=[]
        def builder(plan,windows,streams,out,*,partition,**kwargs):
            self.assertEqual(plan.read_bytes(),b'plan');self.assertEqual(len(streams),4 if partition=='train' else 6)
            self.assertEqual('truth_path' in kwargs,partition=='train');calls.append(partition);out.write_bytes(partition.encode())
            # Mutate original after snapshot; staged plan is unchanged.
            (self.root/'plan').write_bytes(b'changed')
        def predictor(plan,train,test,out,**kw):
            self.assertEqual((plan.read_bytes(),train.read_bytes(),test.read_bytes()),(b'plan',b'train',b'holdout'));out.write_bytes(b'{}')
        r=run_pair(self.root,self.manifest,self.out,expected_sha256=h,authorized_lab=True,builder=builder,predictor=predictor)
        self.assertEqual(calls,['train','holdout']);self.assertEqual(r['prediction_sha256'],digest(b'{}'))
        self.assertEqual({p.name for p in self.out.iterdir()},{'predictions.json','receipt.json'})
    def test_no_publish_on_failure(self):
        h=self.seal()
        def fail(*a,**k):raise ValueError('fixture failure')
        with self.assertRaises(ValueError):run_pair(self.root,self.manifest,self.out,expected_sha256=h,authorized_lab=True,builder=fail,predictor=fail)
        self.assertFalse(self.out.exists())
        with self.assertRaises(PermissionError):run_pair(self.root,self.manifest,self.out,expected_sha256=h,builder=fail,predictor=fail)

if __name__=='__main__':unittest.main()

"""Synthetic offline file-chain test; not a sensor experiment or real blind trial."""
import csv
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from rf17_feature_only_bridge import PLAN, WINDOW, WIRE, bridge_files, predict_files, read_exact
from rf_pilot_evaluator import REQUIRED, LABELS
from rf14_blind_contract import score_sealed

RAW = ('type','rssi','local_timestamp','len','first_word','data')


def write(path, fields, rows):
    with path.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)


def fixture(root):
    plan=[]; train=[]; truth=[]; windows=[]; packets={'1':[],'2':[]}
    for s in ('S1','S2','S3'):
        for p in ('P1','P2'):
            cell=s,p
            part=('train' if cell in {('S1','P1'),('S2','P1')} else 'sealed_unused_reserve' if cell==('S1','P2') else 'primary_blind_holdout' if cell==('S3','P2') else 'secondary_holdout')
            for i in range(1,51):
                tid=f'{s}_{p}_{i:03d}';k=(i-1)%5
                base=dict(trial_id=tid,session_id=s,placement_id=p)
                plan.append(dict(base,reset_index=i,partition=part))
                if part=='train':
                    train.append(dict(base,trial_origin='synthetic_test_fixture',label=LABELS[k],ground_truth_source='fixture',quality='ok',rssi_1_dbm=-90+10*k,rssi_2_dbm=-85+10*k,csi_1_amp_dispersion=k,csi_2_amp_dispersion=k))
                elif part!='sealed_unused_reserve':
                    start=10*len(truth);truth.append(dict(trial_id=tid,label=LABELS[k]))
                    for lid in ('1','2'):
                        windows.append(dict(base,trial_origin='synthetic_test_fixture',link_id=lid,start_us=start,stop_us=start+5))
                        if tid=='S3_P2_050' and lid=='2':continue
                        for j,a in enumerate((20-k,20+k),1):
                            packets[lid].append(dict(type='CSI_DATA',rssi=(-90 if lid=='1' else -85)+10*k,local_timestamp=start+j,len=8,first_word=0,data=str([a,0]*4)))
    paths={k:root/(k+'.csv') for k in ('plan','train','windows','1','2','features','truth')}
    for k,fields,rows in [('plan',PLAN,plan),('train',REQUIRED,train),('windows',WINDOW,windows),('1',RAW,packets['1']),('2',RAW,packets['2']),('truth',('trial_id','label'),truth)]:write(paths[k],fields,rows)
    return paths,hashlib.sha256(paths['plan'].read_bytes()).hexdigest(),plan,truth


class FileChainTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.p,self.digest,self.plan,self.truth=fixture(self.root)
        self.pred=self.root/'predictions.json'
    def bridge(self,link2=True,**kw):
        return bridge_files(self.p['plan'],self.p['windows'],self.p['1'],self.p['2'] if link2 else None,self.p['features'],expected_plan_sha256=self.digest,**kw)
    def predict(self):
        return predict_files(self.p['plan'],self.p['train'],self.p['features'],self.pred,expected_plan_sha256=self.digest)
    def test_complete_chain(self):
        rows=self.bridge(authorized_lab=True)
        self.assertEqual((len(rows),sum(r['quality']=='missing' for r in rows)),(150,1))
        self.assertEqual(set(read_exact(self.p['features'],WIRE)[0]),set(WIRE))
        result=self.predict();self.assertEqual((result['train_n'],result['test_n']),(100,150))
        stored=json.loads(self.pred.read_text());self.assertEqual(result,stored)
        for name,m in stored['models'].items():
            score=score_sealed(self.plan,m['payload'],m['sha256'],self.truth)
            self.assertEqual((score['n'],score['abstain']), (150,1))
            self.assertEqual(score['correct'],30 if name=='majority' else 149)
            with self.assertRaises(ValueError):score_sealed(self.plan,m['payload']+' ',m['sha256'],self.truth)
        with self.assertRaises(FileExistsError):self.predict()
    def test_missing_link(self):
        self.bridge(link2=False,authorized_lab=True)
        for m in self.predict()['models'].values():
            self.assertEqual(score_sealed(self.plan,m['payload'],m['sha256'],self.truth)['abstain'],150)
    def test_invalid_raw_no_output(self):
        write(self.p['2'],RAW,[dict(type='CSI_DATA',rssi=-60,local_timestamp=1,len=8,first_word=0,data='[1,2]')])
        with self.assertRaises(ValueError):self.bridge(authorized_lab=True)
        self.assertFalse(self.p['features'].exists())
    def test_no_permission_no_output(self):
        with self.assertRaises(PermissionError):self.bridge()
        self.assertFalse(self.p['features'].exists())
    def test_truth_in_feature_file_no_prediction(self):
        self.bridge(authorized_lab=True)
        rows=read_exact(self.p['features'],WIRE)
        write(self.p['features'],WIRE+('label',),[dict(r,label='free') for r in rows])
        with self.assertRaises(ValueError):self.predict()
        self.assertFalse(self.pred.exists())
    def test_mutated_plan_no_output(self):
        self.p['plan'].write_bytes(self.p['plan'].read_bytes()+b'\n')
        with self.assertRaises(ValueError):self.bridge(authorized_lab=True)
        self.assertFalse(self.p['features'].exists())

if __name__=='__main__':unittest.main()

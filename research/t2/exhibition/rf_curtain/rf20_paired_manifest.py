"""RF20: verified offline input snapshots; external custody remains necessary."""
import hashlib
import json
import shutil
import tempfile
from pathlib import Path
from rf19_partitioned_bridge import TRAIN, TEST

DOMAINS = {f'{s}/{p}/{lid}' for s,p in TRAIN | TEST for lid in ('1','2')}
KEYS = {'plan','train_windows','holdout_windows','train_truth','raw'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def unique_object(pairs):
    out = {}
    for k,v in pairs:
        if k in out: raise ValueError('duplicate manifest key')
        out[k] = v
    return out


def snapshots(root, manifest_bytes, expected_sha256):
    if digest(manifest_bytes) != expected_sha256:
        raise ValueError('manifest digest mismatch')
    doc = json.loads(manifest_bytes, object_pairs_hook=unique_object)
    if set(doc) != KEYS or set(doc['raw']) != DOMAINS:
        raise ValueError('manifest schema or domain mismatch')
    root = Path(root).resolve(); paths=set(); raw_hashes=set()
    def read(spec, raw=False):
        if not isinstance(spec,dict) or set(spec) != {'path','sha256'}:
            raise ValueError('file descriptor schema')
        p = (root/spec['path']).resolve()
        if not p.is_relative_to(root) or p in paths:
            raise ValueError('path escape or reuse')
        paths.add(p); data=p.read_bytes(); h=digest(data)
        if h != spec['sha256']: raise ValueError('input digest mismatch')
        if raw and h in raw_hashes: raise ValueError('duplicate raw content')
        if raw: raw_hashes.add(h)
        return data
    result={k:read(doc[k]) for k in sorted(KEYS-{'raw'})}
    result['raw']={k:None if v is None else read(v,True) for k,v in sorted(doc['raw'].items())}
    return result


def run_pair(root, manifest_path, output_dir, *, expected_sha256, authorized_lab=False, builder=None, predictor=None):
    if not authorized_lab: raise PermissionError('authorized first-party offline input only')
    if builder is None:
        from rf19_partitioned_bridge import build_files as builder
    if predictor is None:
        from rf17_feature_only_bridge import predict_files as predictor
    raw_manifest=Path(manifest_path).read_bytes()
    data=snapshots(root,raw_manifest,expected_sha256)
    output_dir=Path(output_dir)
    if output_dir.exists(): raise FileExistsError(output_dir)
    with tempfile.TemporaryDirectory() as tmp:
        tmp=Path(tmp)
        def stage(name, b):
            p=tmp/name;p.write_bytes(b);return p
        plan=stage('plan.csv',data['plan']);truth=stage('train_truth.csv',data['train_truth'])
        train_win=stage('train_windows.csv',data['train_windows']);test_win=stage('holdout_windows.csv',data['holdout_windows'])
        streams={tuple(k.split('/')):None if v is None else stage('raw_'+k.replace('/','_')+'.csv',v) for k,v in data['raw'].items()}
        train=tmp/'train.csv';test=tmp/'holdout.csv';pred=tmp/'predictions.json'
        kwargs=dict(expected_plan_sha256=digest(data['plan']),authorized_lab=True)
        builder(plan,train_win,{k:v for k,v in streams.items() if k[:2] in TRAIN},train,partition='train',truth_path=truth,**kwargs)
        builder(plan,test_win,{k:v for k,v in streams.items() if k[:2] in TEST},test,partition='holdout',**kwargs)
        predictor(plan,train,test,pred,expected_plan_sha256=kwargs['expected_plan_sha256'])
        # Publish predictions only; training/holdout files remain in private staging.
        receipt={'status':'OFFLINE_INPUT_INTEGRITY_NOT_CUSTODY_PROOF','manifest_sha256':expected_sha256,'plan_sha256':kwargs['expected_plan_sha256'],'train_sha256':digest(train.read_bytes()),'holdout_sha256':digest(test.read_bytes()),'prediction_sha256':digest(pred.read_bytes()),'missing_domains':sum(v is None for v in streams.values())}
        output_dir.mkdir(exist_ok=False)
        try:
            shutil.copyfile(pred,output_dir/'predictions.json')
            (output_dir/'receipt.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n',encoding='utf-8')
        except BaseException:
            shutil.rmtree(output_dir);raise
    return receipt

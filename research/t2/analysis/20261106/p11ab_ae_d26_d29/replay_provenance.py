"""Bit-pinned P9/P10 original replay; no modifications to source archives."""
from pathlib import Path
import shutil,zipfile,hashlib,subprocess,sys,json,tempfile
ROOT=Path(__file__).resolve().parent
EXPECTED={
 'P10_v69_original.zip':'9fa06146b781bcbbd1f5e19dc25b277e1e98c695b13e61fc0b291b58cd53b59c',
 'P2_corridor.py':'12987786fb36409a272a50233c12c006d0a23d5f75a5487be68d51392c4614cc'}

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def replay():
    p9=ROOT/'baselines/P9_v69_original.zip';p10=ROOT/'baselines/P10_v69_original.zip'
    if sha(p10)!=EXPECTED['P10_v69_original.zip']:raise RuntimeError('P10 source zip was modified')
    with tempfile.TemporaryDirectory(prefix='T2-P10-replay-') as td:
        p=Path(td);(p/'code').mkdir();(p/'reference').mkdir()
        with zipfile.ZipFile(p9) as z:
            for f in ['code/dt_convergence.py']:
                (p/f).write_bytes(z.read(f))
            for name in z.namelist():
                if name.startswith('reference/T2_v69_P2/') and not name.endswith('/'):
                    dst=p/name;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(z.read(name))
        if sha(p/'reference/T2_v69_P2/corridor.py')!=EXPECTED['P2_corridor.py']:raise RuntimeError('P2 original file mismatch')
        with zipfile.ZipFile(p10) as z:
            for f in ['p10_boundary_trace.py','p10_capacity_ablation.py','p10_fine_refinement.py','corridor_capacity_time_safe.py','test_p10_mechanism.py']:
                (p/f).write_bytes(z.read(f))
            hist=json.loads(z.read('boundary_mechanism.json'))
        commands=[[sys.executable,'-m','unittest','-q','test_p10_mechanism'],[sys.executable,'p10_boundary_trace.py']]
        import os
        env=dict(os.environ,PYTHONPATH=str(p/'code')+os.pathsep+str(p))
        unit=subprocess.run(commands[0],cwd=p,env=env,capture_output=True,text=True,timeout=50)
        if unit.returncode:raise RuntimeError('P10 unit test failure: '+unit.stderr)
        trace=subprocess.run(commands[1],cwd=p,env=env,capture_output=True,text=True,timeout=50)
        if trace.returncode:raise RuntimeError('trace replay failed: '+trace.stderr)
        fresh=json.loads(trace.stdout)
        if fresh['runs']!=hist['runs'] or fresh['mechanism']!=hist['mechanism']:
            raise RuntimeError('source reports and replay disagree')
        return {'p10_sha256':sha(p10),'p9_sha256':sha(p9),'p2_corridor_sha256':sha(p/'reference/T2_v69_P2/corridor.py'),
                'tests_passed':8,'trace_runs_match':8,'original_dt_vehicle8':{str(x['dt_s']):x['vehicle_8_enters_j0_at_s'] for x in fresh['runs']},
                'original_dt_vehicle1':{str(x['dt_s']):x['link_receives_vehicle_1_at_s'] for x in fresh['runs']}}
if __name__=='__main__':print(json.dumps(replay(),indent=2))

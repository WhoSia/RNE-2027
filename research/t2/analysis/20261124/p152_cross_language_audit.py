"""Compare every unique P151 policy cost against P152 without editing frozen sources."""
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from p152_independent_observation import cohort

ROOT=Path(__file__).resolve().parent


def run():
    source=(ROOT/'p151_movement_queue.js').read_text(encoding='utf-8')
    marker=' let decreased=0,tied=0,increased=0,'
    assert source.count(marker)==1
    probe=source.replace(marker,' return rows;\n'+marker)
    with tempfile.TemporaryDirectory() as d:
        script=Path(d)/'probe.js';script.write_text(probe,encoding='utf-8')
        raw=subprocess.check_output(['node',str(script)],text=True)
    js={}
    for row in json.loads(raw):
        key=(row['mask'],row['interval'],row['P'],row['D'])
        values=tuple(row['costs'][f'{r}:{p}'] for r in (0,1) for p in (4,8))
        if key in js:assert js[key]==values
        js[key]=values
    import itertools
    py={}
    for key,(context,state,future,costs) in zip(itertools.product(range(64),(1,2),(1,2),(1,2)),cohort(),strict=True):
        assert context==(key[2],key[3],key[1])
        py[key]=tuple(costs[r,p] for r in (False,True) for p in (4,8))
    assert js==py
    payload=json.dumps([[list(k),list(v)] for k,v in sorted(js.items())],separators=(',',':')).encode()
    return dict(status='EXACT_UNIQUE_POLICY_COST_PARITY_NOT_FIELD',unique_cells=len(js),compared_costs=4*len(js),
                sha256=hashlib.sha256(payload).hexdigest(),node=subprocess.check_output(['node','--version'],text=True).strip())

if __name__=='__main__':print(json.dumps(run(),indent=2))

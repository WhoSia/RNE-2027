"""Deterministic research ZIP. Filesystem caches and dynamic timestamps excluded."""
from pathlib import Path
from hashlib import sha256
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED
import json
ROOT=Path(__file__).resolve().parent
IGNORED={'__pycache__','.DS_Store','.pytest_cache'}

def selected():
    files=[]
    for path in ROOT.rglob('*'):
        if not path.is_file() or any(part in IGNORED for part in path.parts):continue
        rel=path.relative_to(ROOT)
        if rel.parts[0] in ('replay_P10','work'):continue
        if rel.parts[:2] in (('baselines','P9_original'),('baselines','P10_original'),('baselines','D25_extracted')):continue
        if rel.name in ('SHA256_MANIFEST.json',):continue
        files.append(rel)
    return sorted(files,key=str)

def seal():
    files=selected()
    manifest={str(p):{'sha256':sha256((ROOT/p).read_bytes()).hexdigest(),'size':(ROOT/p).stat().st_size} for p in files}
    (ROOT/'SHA256_MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    output=ROOT.parent/'T2_20261106_D26_D29_Integrated_Replay.zip'
    with ZipFile(output,'w',ZIP_DEFLATED,compresslevel=9) as archive:
        for p in files+[Path('SHA256_MANIFEST.json')]:
            zi=ZipInfo(str(p),date_time=(2026,11,6,0,0,0))
            zi.compress_type=ZIP_DEFLATED
            zi.external_attr=(0o644<<16)
            archive.writestr(zi,(ROOT/p).read_bytes())
    with ZipFile(output) as archive:
        assert archive.testzip() is None
        for file,info in manifest.items():
            assert sha256(archive.read(file)).hexdigest()==info['sha256']
    return {'zip':str(output),'sha256':sha256(output.read_bytes()).hexdigest(),'file_count':len(files),'bytes':output.stat().st_size}
if __name__=='__main__':print(json.dumps(seal(),indent=2))

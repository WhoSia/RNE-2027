"""Deterministic research package: source bytes and fixed ZIP metadata."""
from pathlib import Path
from hashlib import sha256
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
import json
ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'T2_P11AA_D25_20261106.zip'
entries=sorted(p for p in ROOT.rglob('*') if p.is_file()
               and not any(x in {'__pycache__','.pytest_cache'} for x in p.parts)
               and p.name!='SHA256_MANIFEST.json' and p.suffix != '.pyc')
manifest={str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in entries}
(ROOT/'SHA256_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n',encoding='utf-8')
with ZipFile(OUT,'w') as zf:
    for p in sorted([*entries,ROOT/'SHA256_MANIFEST.json']):
        info=ZipInfo(str(p.relative_to(ROOT)),(2026,11,6,0,0,0))
        info.compress_type=ZIP_DEFLATED
        info.external_attr=0o644<<16
        zf.writestr(info,p.read_bytes())
print(json.dumps({'file':str(OUT),'sha256':sha256(OUT.read_bytes()).hexdigest(),'members':len(entries)+1,'manifest_records':len(entries)},indent=2))

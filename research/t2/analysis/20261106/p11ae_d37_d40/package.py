"""Deterministic source-and-derived-data archive; excludes caches and raw external CSV."""
import hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
OUTPUT=ROOT.parent/'T2_D37_D40_20261106_RELEASE.zip'
files=sorted(p for p in ROOT.rglob('*') if p.is_file() and p.name!='SHA256_MANIFEST.json' and not any(x in p.parts for x in ('__pycache__','.pytest_cache','.git')))
manifest={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
(ROOT/'SHA256_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
files.append(ROOT/'SHA256_MANIFEST.json')
with zipfile.ZipFile(OUTPUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(files):
  info=zipfile.ZipInfo(p.relative_to(ROOT).as_posix(),date_time=(2026,11,6,0,0,0))
  info.compress_type=zipfile.ZIP_DEFLATED
  info.external_attr=0o644<<16
  z.writestr(info,p.read_bytes())
with zipfile.ZipFile(OUTPUT) as z:
 assert z.testzip() is None
 print(json.dumps({'zip':str(OUTPUT),'sha256':hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),'files':len(z.namelist()),'bytes':OUTPUT.stat().st_size}))

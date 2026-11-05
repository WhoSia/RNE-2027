"""Cache-free deterministic archive and file SHA256 inventory."""
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
root=Path(__file__).resolve().parent
files=sorted((p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='pyc' and p.name!='SHA256_MANIFEST.json'),key=lambda x:str(x.relative_to(root)))
manifest={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
(root/'SHA256_MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
archive=root.parent/'T2_P11Z_D24_20261106.zip'
with ZipFile(archive,'w',ZIP_DEFLATED,compresslevel=7) as z:
    for p in files+[root/'SHA256_MANIFEST.json']:
        z.write(p,arcname=str(p.relative_to(root)))
with ZipFile(archive) as z:
    assert z.testzip() is None
print(archive,archive.stat().st_size,hashlib.sha256(archive.read_bytes()).hexdigest(),len(manifest))

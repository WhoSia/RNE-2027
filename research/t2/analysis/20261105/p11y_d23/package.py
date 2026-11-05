from pathlib import Path
import hashlib,json,zipfile
root=Path(__file__).parent
paths=sorted(p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name not in ('SHA256_MANIFEST.json','package.py'))
manifest={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
(root/'SHA256_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
name=root.parent/'T2_P11Y_D23_20261105.zip'
with zipfile.ZipFile(name,'w',zipfile.ZIP_DEFLATED) as z:
    for p in paths+[root/'SHA256_MANIFEST.json',root/'package.py']:
        z.write(p,arcname=str(p.relative_to(root)))
with zipfile.ZipFile(name) as z:
    assert z.testzip() is None
print('ZIP',name,'files',len(paths)+2,'sha256',hashlib.sha256(name.read_bytes()).hexdigest())

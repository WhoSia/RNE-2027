from pathlib import Path
import zipfile,hashlib,json,sys
root=Path(__file__).resolve().parent
out=root.parent/'T2_D31_D33_20261106_RELEASE.zip'
files=sorted([p for p in root.rglob('*') if p.is_file() and p.relative_to(root).parts[0] in ('src','tests','docs','results','references') and '__pycache__' not in p.parts and p.suffix!='.pyc'] +[root/'README.md',root/'run_study.py',root/'stress_study.py',root/'visualize.py',root/'package.py'])
manifest={'date':'20261106','scope':'P11-AC D31-D33','files':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'external_sumo_execution':'NOT_EXECUTED','p10_replay_type':'ORIGINAL_SOURCE_REPLAY'}
(root/'SHA256_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
files.append(root/'SHA256_MANIFEST.json')
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
 for p in sorted(files):
  info=zipfile.ZipInfo(str(p.relative_to(root)),date_time=(2026,11,6,0,0,0))
  info.compress_type=zipfile.ZIP_DEFLATED
  info.external_attr=0o644<<16
  archive.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
print(json.dumps({'zip':str(out),'files':len(files),'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))

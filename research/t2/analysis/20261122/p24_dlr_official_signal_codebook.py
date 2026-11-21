"""DLR-UT 1.3.1 official PDF codebook+coordinates reconciled with raw signal IDs.

This is descriptive sensor-metadata validation, not a live signal operation.
"""
import argparse
import csv
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

SHA={
 'official_pdf':'3c733b677ee63fd2cb282946f415f649d23954ac420d5bc37e0af545f7293849',
 'traffic_lights':'95802b0c00f1232572279fed62668dfb484d8ea2303c4d3eb4a88339d41a8f0c',
}

def check(path,kind):
    if hashlib.sha256(Path(path).read_bytes()).hexdigest()!=SHA[kind]:
        raise ValueError('mismatched official DLR source '+kind)


def parse_pdf_text(text):
    if 'Version 1.3.1' not in text and '1.3.1' not in text:
        raise ValueError('wrong version codebook')
    section=text.split('Table 3: Traffic light coordinates',1)[1].split('4.2.3.',1)[0]
    records=[{'id':int(i),'easting':float(e),'northing':float(n)} for i,e,n in re.findall(
        r'^\s*(\d{1,2})\s+(604\d{3}\.\d+)\s+(5792\d{3}\.\d+)\s*$',section,re.M)]
    states_section=text.split('Table 4: Traffic light states',1)[1].split('4.3.',1)[0]
    states={int(i):desc.strip() for i,desc in re.findall(r'^\s*([0-9])\s+([^\n]+)',states_section,re.M)}
    if len(records)!=35 or len({r['id'] for r in records})!=26 or set(states)!=set(range(10)):
        raise ValueError('incomplete or drifted official PDF extraction')
    return records,states


def parse_pdf(path):
    check(path,'official_pdf')
    proc=subprocess.run(['pdftotext','-layout',str(path),'-'],check=True,
         stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    return parse_pdf_text(proc.stdout)


def describe(pdf,lights):
    records,states=parse_pdf(pdf)
    check(lights,'traffic_lights')
    with Path(lights).open(encoding='utf8',newline='') as f:
        rows=list(csv.DictReader(f))
    per_id=defaultdict(list);code_totals=Counter()
    for r in rows:
        idx=int(r['id']);code=int(r['state']);t=datetime.fromisoformat(r['timestamp'])
        if t.tzinfo is None or code not in states:raise ValueError('unknown state/time')
        per_id[idx].append((t,code));code_totals[code]+=1
    if set(per_id)!=set(range(1,31)):
        raise ValueError('not the expected 30 live signal IDs')
    changes=0
    for observations in per_id.values():
        observations.sort()
        if len({t for t,_ in observations})!=len(observations):
            raise ValueError('duplicate timestamp for a signal ID')
        changes+=sum(a[1]!=b[1] for a,b in zip(observations,observations[1:]))
    positioned={r['id'] for r in records}
    return {'protocol':'P24_DLR_OFFICIAL_V1_3_1_SIGNAL_CODEBOOK_GATE',
      'status':'VERIFIED_OFFICIAL_STATIC_SIGNAL_COORDINATES_AND_STATE_LABELS_NOT_CONTROLLED_LANES',
      'source_sha256':SHA,
      'official_states':{str(i):states[i] for i in sorted(states)},
      'official_signal_pole_coordinate_rows':len(records),
      'official_signal_ids_with_coordinates':len(positioned),
      'live_signal_ids':len(per_id),
      'live_ids_missing_coordinates':sorted(set(per_id)-positioned),
      'live_signal_state_readings':len(rows),
      'observed_changes_across_live_ids':changes,
      'observed_code_readings':{str(i):code_totals[i] for i in sorted(code_totals)},
      'observed_label_readings':{states[i]:code_totals[i] for i in sorted(code_totals)},
      'coordinates':records,
      'limitations':['Signal-head positions do not identify the exact controlled lane/turn or stopline; figure must be cross-checked manually',
        'IDs 10–13 appear in live observations but have no coordinates in official PDF table 3',
        'Phase sample counts are not exact durations or legally permitted control plans',
        '1 Hz sampling misses subsecond change instants and traffic safety transients',
        'OpenDRIVE static signal IDs are not the live signal IDs']}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('pdf',type=Path);p.add_argument('traffic_signals',type=Path);p.add_argument('out',type=Path)
    a=p.parse_args();a.out.write_text(json.dumps(describe(a.pdf,a.traffic_signals),sort_keys=True,indent=2)+'\n',encoding='utf8')

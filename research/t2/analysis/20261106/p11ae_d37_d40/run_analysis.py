"""Reproduce descriptive metrics from independently checked public GitHub excerpts.

This does NOT reconstruct or distribute third-party raw trajectories. Do not
interpret the conditional label differences as a traffic-signal policy effect.
"""
import csv
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'src'))
from empirical_summary import load_manifest,describe

ROOT=Path(__file__).resolve().parent
manifest=ROOT/'data/cats_16_derived.json'
entries=load_manifest(manifest)
summary=describe(entries)
(ROOT/'results').mkdir(exist_ok=True)
(ROOT/'results/cats_episode_descriptive.json').write_text(json.dumps({
 'provenance':'Only source-connector-derived metadata; original CSV bytes not locally stored',
 'summary':summary,'risk_flag':'Selected episodes from Waymo Motion-derived samples; not one stable intersection; no queue, full signal cycle or independent traffic-policy evaluation'
},indent=2)+'\n')
with (ROOT/'results/cats_episode_descriptive.csv').open('w',newline='') as f:
 wr=csv.DictWriter(f,fieldnames=['category','sample_id','source_git_blob','frames','mean_speed_mps','stop_fraction','red_state_fraction','green_state_fraction','undocumented_state_present'])
 wr.writeheader()
 for e in entries:
  wr.writerow({'category':e['category'],'sample_id':e['filename'].rsplit('-',1)[-1].replace('.csv',''),
  'source_git_blob':e['github_blob_sha1'],'frames':e['frames'],'mean_speed_mps':round(e['mean_speed_mps'],6),
  'stop_fraction':round(e['frames_below_0p5_mps']/e['frames'],6),
  'red_state_fraction':round(e['red_or_red_arrow_frames']/e['frames'],6),
  'green_state_fraction':round(e['green_or_green_arrow_frames']/e['frames'],6),
  'undocumented_state_present':-1 in e['observed_state_codes']})
print(json.dumps(summary,ensure_ascii=False,indent=2))

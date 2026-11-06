"""D31-D33 reproduce research outputs from pinned code and synthetic inputs."""
from __future__ import annotations
import json,csv,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from policy_audit import compare,aggregate
from sumo_gate import run_if_available
from event_bridge import capacity_witness

def main():
    result=ROOT/'results';result.mkdir(exist_ok=True)
    p10=json.loads((ROOT/'references/p10_replay.json').read_text())
    audit=capacity_witness({'source_case':p10['case'],'mechanism':p10['mechanism'],'runs':p10['grid']})
    (result/'d31_p10_bridge.json').write_text(json.dumps(audit,indent=2)+'\n')
    status=run_if_available(result/'sumo_scenario')
    (result/'d32_sumo_status.json').write_text(json.dumps(status,indent=2)+'\n')
    rows,traces=compare();summary=aggregate(rows)
    (result/'d33_policy_summary.json').write_text(json.dumps({'summary':summary,'per_seed':rows,'actuated_phase_logs':traces,'status':'SYNTHETIC_ONLY'},indent=2)+'\n')
    with (result/'d33_policy_court.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=summary[0].keys());w.writeheader();w.writerows(summary)
    print(json.dumps({'D31':audit,'D32':status['independent_sumo_run'],'D33':summary},indent=2))
if __name__=='__main__':main()

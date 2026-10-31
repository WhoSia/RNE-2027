"""Offline local checkout audit. No GitHub Actions, commits, pushes or network.

Run from an actual checked-out repository branch. Records SHA256 of
source files and local unittest status. A non-Git directory cannot claim
checkout parity, even if tests pass.
"""
from pathlib import Path
import hashlib,json,re,subprocess,sys

ROOT=Path(__file__).resolve().parent
SOURCES=("spatial_v10.py","dual_lane_v11.py","site_v11.py","run_site_v11.py",
         "downstream_sweep_v12.py","receiver_sweep_v13.py","pareto_receiver_v13.py")

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def git_info():
    def run(*args):
        r=subprocess.run(["git",*args],cwd=ROOT,capture_output=True,
                         text=True,timeout=10,check=False)
        return r.stdout.strip() if r.returncode==0 else None
    return {"head":run("rev-parse","HEAD"),
            "branch":run("branch","--show-current"),
            "dirty_status":run("status","--porcelain")}

def audit():
    files={n:sha256(ROOT/n) if (ROOT/n).is_file() else None for n in SOURCES}
    cmd=[sys.executable,"-m","unittest","discover","-s",str(ROOT),
         "-p","test_*v1*.py","-v"]
    r=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,
                     timeout=180,check=False)
    output=r.stdout+"\n"+r.stderr
    match=re.search(r"Ran\s+(\d+)\s+tests?",output)
    git=git_info()
    return {"audit_type":"OFFLINE_ONLY_NO_ACTIONS",
        "git":git,"source_sha256":files,"test_command":cmd,
        "test_count":int(match.group(1)) if match else None,
        "test_exit_code":r.returncode,"test_output_tail":output[-2000:],
        "exact_checkout_tested":bool(git["head"] and git["dirty_status"]=="")
            and r.returncode==0,
        "field_calibrated":False}

if __name__=="__main__":
    dest=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/"results"/"offline_audit_v13.json"
    report=audit()
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
    print("tests",report["test_count"],"exit",report["test_exit_code"],
          "git",report["git"]["head"],"checkout",report["exact_checkout_tested"])
    if report["test_exit_code"]:sys.exit(report["test_exit_code"])

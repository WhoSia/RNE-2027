import json
from pathlib import Path

base='https://github.com/CATS-Lab/Data-AV-Traffic-Light-Stop-Sign/blob/main/interactions_with_traffic_light/'
raw={
'stops_at_traffic_light':[
('106','3deb2be0f1bde940f994beda24ad395bd5e1c4de',0.9305322013527045,55,11,72,[4,0,6]),
('190','a59bf71c989c1e8cd2f5d43d0a88d505dce2e016',0.6661541420991333,57,91,0,[4]),
('207','2780637b92572d5529eb30c04dd7a5da5a9d77da',0.31901370829547265,73,61,0,[4,0]),
('255','8642aafc5ea3e1631347d535178d51940e461767',0.7363162802894994,57,54,0,[4,0]),
('285','7cbf0005759286f712dce9dd0ef8fca48d85fcf0',4.236959013618416,30,18,28,[6,5,4]),
('306','6f13b47492419355b795ef45823eb49d2786e402',4.572469286866241,0,87,0,[4,0]),
('309','ecfb301c49c885169736d901578e895f5cc747c6',4.215794725404991,3,91,0,[4]),
('71','15b189a9b61267675cf7daa49f89f24f57b0b139',1.8635728000418956,53,63,0,[5,4])],
'straight_proceeds_at_traffic_light':[
('137','3e18ad307822efd8abc92f67218516aff047b882',7.493831165926787,11,49,42,[4,6]),
('141','e9b1e6facac423b6cbdd92dea4ae3805f5646295',9.072959321213293,2,82,9,[4,6]),
('146','07e56a92d34fec9a75e6ad75e8ae517531e8ac1d',19.898574305104685,0,13,16,[6,-1,0,4]),
('16','33d112d50ca6582208599b79c712be4c0b64d00e',4.384276166005293,17,8,82,[6,4,-1]),
('17','5d592b1385cfa232e54927184e630640b7a0f5fd',5.035996811719967,27,57,34,[4,6]),
('178','659a5f8b4e991cbad1665cbbafcb39ddcad6f1b6',9.317361960044273,0,60,31,[4,6]),
('263','dcafc06e3e71e6f7ba0e4e8451c308e272d9070f',11.578108567457933,0,29,40,[6,0,4]),
('299','ace020434d629d952cd5b7a6f4226c8227e06678',2.9477191160427876,30,20,25,[4,3,0])]
}
records=[]
for category,items in raw.items():
 for suffix,sha,speed,stop,red,green,states in items:
  prefix='stop_before_light' if category.startswith('stops_') else 'go_through'
  file=f'{prefix}-training_tfexample.tfrecord-00001-of-01000-{suffix}.csv'
  records.append({'category':category,'filename':file,'url':base+category+'/'+file,'github_blob_sha1':sha,'frames':91,'sample_period_s':0.1,'mean_speed_mps':speed,'frames_below_0p5_mps':stop,'red_or_red_arrow_frames':red,'green_or_green_arrow_frames':green,'observed_state_codes':sorted(states),'malformed_rows':0})
out={'dataset':'CATS-Lab/Data-AV-Traffic-Light-Stop-Sign (Waymo Motion derived)','source_repo':'https://github.com/CATS-Lab/Data-AV-Traffic-Light-Stop-Sign','provenance':'Each of 16 CSV files read via GitHub connector in this conversation on 2026-11-06; derived statistics only; original CSV bytes NOT downloaded or redistributed in local archive. Git blobs from GitHub API.','selection':'first eight names listed in each of two preexisting labeled folders; not a random sample, different locations possible','phase_codes':'README: 1 arrow red; 2 arrow yellow; 3 arrow green; 4 circular red; 5 circular yellow; 6 circular green; 7 flashing red; 8 flashing yellow; 0 unknown; -1 observed in raw samples and treated as undocumented unknown','speed_stopped_definition':'AV_speed < 0.5 m/s in an observed frame, not queue length','sample_size_qualification':'91 samples/segment at 10Hz (~9.1s recording window); 16 segments, not 1456 independent road traffic experiments','records':records}
Path(__file__).with_name('cats_16_derived.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')

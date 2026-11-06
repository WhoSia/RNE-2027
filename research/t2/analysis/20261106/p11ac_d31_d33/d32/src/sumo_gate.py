"""D32 build auditable SUMO scenario and optionally run locally installed SUMO.
No independent result is invented when executables are missing.
"""
from __future__ import annotations
from pathlib import Path
import shutil,subprocess,hashlib,json
from xml.etree import ElementTree as E
from validation import sumo_tripinfo, file_receipt


def prepare(outdir: str|Path):
    out=Path(outdir);out.mkdir(parents=True,exist_ok=True)
    # A minimal two-in/one-out junction. SUMO network geometry is NOT T2 lane geometry parity.
    nodes=E.Element('nodes')
    for name,x,y in [('a',-100,0),('c',0,100),('j',0,0),('s',100,0)]:
        E.SubElement(nodes,'node',id=name,x=str(x),y=str(y),type='priority' if name=='j' else 'dead_end')
    edges=E.Element('edges')
    for name,frm,to in [('A','a','j'),('C','c','j'),('S','j','s')]:
        E.SubElement(edges,'edge',id=name,**{'from':frm,'to':to},numLanes='1',speed='8.0')
    routes=E.Element('routes')
    E.SubElement(routes,'vType',id='car',length='4.5',accel='2.0',decel='3.0',minGap='2.0',maxSpeed='10')
    for i in range(12):
        e=E.SubElement(routes,'vehicle',id=f'v{i}',type='car',depart=str(i*2))
        E.SubElement(e,'route',edges='A S' if i%2==0 else 'C S')
    for name,element in [('nodes.nod.xml',nodes),('edges.edg.xml',edges),('demand.rou.xml',routes)]:
        E.ElementTree(element).write(out/name,encoding='utf-8',xml_declaration=True)
    return {name:file_receipt(out/name) for name in ['nodes.nod.xml','edges.edg.xml','demand.rou.xml']}


def run_if_available(outdir: str|Path):
    out=Path(outdir); receipts=prepare(out)
    netconvert=shutil.which('netconvert');sumo=shutil.which('sumo')
    status={'netconvert_installed':bool(netconvert),'sumo_installed':bool(sumo),
            'scenario_receipts':receipts,'independent_sumo_run':'NOT_EXECUTED'}
    if not netconvert or not sumo:return status
    cmd=[netconvert,'--node-files',str(out/'nodes.nod.xml'),'--edge-files',str(out/'edges.edg.xml'),'--output-file',str(out/'network.net.xml')]
    p=subprocess.run(cmd,text=True,capture_output=True,timeout=90)
    if p.returncode:status['error']='netconvert failed: '+p.stderr[-800:];return status
    cmd=[sumo,'-n',str(out/'network.net.xml'),'-r',str(out/'demand.rou.xml'),
         '--tripinfo-output',str(out/'tripinfo.xml'),'--tripinfo-output.write-unfinished','true',
         '--end','240','--no-step-log','true']
    p=subprocess.run(cmd,text=True,capture_output=True,timeout=150)
    if p.returncode:status['error']='sumo failed: '+p.stderr[-800:];return status
    status['independent_sumo_run']='EXECUTED';status['tripinfo_receipt']=file_receipt(out/'tripinfo.xml')
    status['finished_trip_count']=len(sumo_tripinfo(out/'tripinfo.xml'))
    return status

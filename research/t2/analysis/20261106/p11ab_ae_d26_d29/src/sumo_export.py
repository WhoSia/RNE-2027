"""Produce reviewable SUMO input files. Requires EXTERNAL netconvert+sumo for true comparison."""
from xml.etree.ElementTree import Element, SubElement, ElementTree, parse
from pathlib import Path
import shutil

def write_sumo_fixture(folder):
    root=Path(folder);root.mkdir(parents=True,exist_ok=True)
    nodes=Element('nodes')
    for name,x in [('n0',0),('n1',30),('n2',45),('n3',85)]:
        SubElement(nodes,'node',id=name,x=str(x),y='0',type='priority')
    ElementTree(nodes).write(root/'corridor.nod.xml',encoding='utf-8',xml_declaration=True)
    edges=Element('edges')
    for name,a,b,length in [('u','n0','n1',30),('p','n1','n2',15),('d','n2','n3',40)]:
        SubElement(edges,'edge',id=name,**{'from':a,'to':b},numLanes='1',speed='8')
    ElementTree(edges).write(root/'corridor.edg.xml',encoding='utf-8',xml_declaration=True)
    routes=Element('routes')
    SubElement(routes,'vType',id='passenger',length='4.5',minGap='2',maxSpeed='8',accel='2',decel='3')
    SubElement(routes,'route',id='path',edges='u p d')
    for i in range(10):
        SubElement(routes,'vehicle',id=f'v{i}',type='passenger',route='path',depart=f'{i*2}')
    ElementTree(routes).write(root/'corridor.rou.xml',encoding='utf-8',xml_declaration=True)
    config=Element('configuration')
    input_node=SubElement(config,'input')
    SubElement(input_node,'net-file',value='corridor.net.xml')
    SubElement(input_node,'route-files',value='corridor.rou.xml')
    time=SubElement(config,'time')
    SubElement(time,'begin',value='0');SubElement(time,'end',value='180')
    SubElement(time,'step-length',value='0.5')
    outputs=SubElement(config,'output')
    SubElement(outputs,'tripinfo-output',value='corridor.tripinfo.xml')
    ElementTree(config).write(root/'corridor.sumocfg',encoding='utf-8',xml_declaration=True)
    for fname in ['corridor.nod.xml','corridor.edg.xml','corridor.rou.xml','corridor.sumocfg']:
        parse(root/fname)
    command=['netconvert','--node-files','corridor.nod.xml','--edge-files','corridor.edg.xml','--output-file','corridor.net.xml']
    return {'files':sorted(x.name for x in root.glob('*.xml'))+['corridor.sumocfg'],
            'netconvert_available':bool(shutil.which('netconvert')),
            'sumo_available':bool(shutil.which('sumo')),
            'build_command':command,
            'run_command':['sumo','-c','corridor.sumocfg']}

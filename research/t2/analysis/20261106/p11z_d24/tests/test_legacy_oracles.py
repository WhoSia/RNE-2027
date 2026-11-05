"""Independent reference-oracle comparisons: exact archived X/Y source copies."""
import importlib.util
import random
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from phase_network import Step,Movement,simulate


def load(name,path):
    # Python dataclasses need their defining module registered during exec.
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    sys.modules[name]=mod
    spec.loader.exec_module(mod)
    return mod

X=load('sealed_X',ROOT/'baselines'/'x_lane_fifo.py')
Y=load('sealed_Y',ROOT/'baselines'/'y_zone_phases.py')

class LegacyOracles(unittest.TestCase):
    def test_random_single_step_X_model(self):
        rng=random.Random(20261106)
        for trial in range(100):
            data=[]
            for i in range(12):
                at=rng.randint(0,10)
                duration=rng.randint(1,4)
                zone=f'Z{rng.randint(0,3)}'
                data.append((str(i),at,zone,duration))
            old=[X.Demand(at,ident,f'L{ident}',(zone,),duration,'vehicle',zone) for ident,at,zone,duration in data]
            new=[Movement(ident,at,f'L{ident}','vehicle',(Step((zone,),duration),)) for ident,at,zone,duration in data]
            cap={f'Z{k}':1 for k in range(4)}
            xx=X.simulate(old,cap)
            zz=simulate(new,cap)
            self.assertEqual((xx.entries,xx.exits),(zz.starts,zz.finishes), f'trial={trial}')
    def test_sequential_Y_hold_and_wait_model(self):
        src=[Y.Movement('ped',0,(('B',3),)), Y.Movement('car',0,(('A',2),('B',2))), Y.Movement('follower',1,(('A',1),))]
        dst=[Movement(q.identity,q.at,q.identity,'vehicle',tuple(Step((zone,),ticks) for zone,ticks in q.phases)) for q in src]
        baseline=Y.simulate(src)
        integrated=simulate(dst,{'A':1,'B':1})
        self.assertEqual((baseline['starts'],baseline['finishes']),(integrated.starts,integrated.finishes))

if __name__=='__main__':unittest.main()

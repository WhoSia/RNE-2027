import copy
import unittest
from dataclasses import replace
from p19_receiver_service_opportunity import build_config, arrival_clock_pair, ACTION
from dual_lane_v11 import run
from p20_independent_receiver_ledger import audit_trace, LedgerViolation


class P20Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases=[]
        for seed in (112,113):
            for capacity,offset in ((2,0),(2,15),(4,0),(4,15)):
                cfg=replace(build_config(seed,1650,.5,14.,capacity,0.),downstream_offset_s=offset)
                _,tape=arrival_clock_pair(cfg.base)
                for action in ('baseline','treatment'):
                    kwargs={} if action=='baseline' else {'phase_overrides':ACTION}
                    if kwargs:
                        cp=run(cfg,tape,checkpoint_at=84,trace=True)
                        result=run(cfg,tape,resume_from=cp,trace=True,**kwargs)
                    else:
                        result=run(cfg,tape,trace=True)
                    cls.cases.append((cfg,tape,result,action))

    def test_16_native_traces_shadow_match(self):
        self.assertEqual(len(self.cases),16)
        for i,(cfg,tape,res,action) in enumerate(self.cases):
            with self.subTest(i=i):
                ledger=audit_trace(cfg,tape,res)
                self.assertEqual(ledger['generated'],res['generated'])
                self.assertEqual(ledger['receiver_exits'],res['network_out_L']+res['network_out_S'])

    def test_tamper_receiver_cell_rejected(self):
        cfg,tape,res,_=self.cases[0]
        bad=copy.deepcopy(res)
        bad['frames'][200]['receiver']=()
        with self.assertRaises(LedgerViolation):audit_trace(cfg,tape,bad)

    def test_tamper_outside_count_rejected(self):
        cfg,tape,res,_=self.cases[0]
        bad=copy.deepcopy(res)
        bad['frames'][100]['outside']+=1
        with self.assertRaises(LedgerViolation):audit_trace(cfg,tape,bad)

    def test_tamper_service_crossing_rejected(self):
        cfg,tape,res,_=self.cases[0]
        bad=copy.deepcopy(res)
        bad['service_events']=[x for x in bad['service_events'] if x['reason']!='stopline_cross']
        with self.assertRaises(LedgerViolation):audit_trace(cfg,tape,bad)

    def test_tamper_road_jump_rejected(self):
        cfg,tape,res,_=self.cases[0]
        bad=copy.deepcopy(res)
        for t in range(1,len(bad['frames'])):
            if bad['frames'][t]['A'] and bad['frames'][t-1]['A']:
                ids_prev={v[1] for v in bad['frames'][t-1]['A']}
                for j,v in enumerate(bad['frames'][t]['A']):
                    if v[1] in ids_prev:
                        bad['frames'][t]['A'][j]=(v[0]+10,v[1],v[2])
                        with self.assertRaises(LedgerViolation):audit_trace(cfg,tape,bad)
                        return
        self.fail('no suitable A-road position found')

    def test_tamper_network_exit_count_rejected(self):
        cfg,tape,res,_=self.cases[0]
        bad=copy.deepcopy(res)
        bad['network_out_S']+=1
        with self.assertRaises(LedgerViolation):audit_trace(cfg,tape,bad)

    def test_tamper_receiver_denied_count_rejected(self):
        cfg,tape,res,_=self.cases[0]
        bad=copy.deepcopy(res)
        bad['receiver_denied_attempts']+=1
        with self.assertRaises(LedgerViolation):audit_trace(cfg,tape,bad)

    def test_tamper_bad_frame_order_rejected(self):
        cfg,tape,res,_=self.cases[0]
        bad=copy.deepcopy(res)
        bad['frames'][25]['t']=24
        with self.assertRaises(LedgerViolation):audit_trace(cfg,tape,bad)

    def test_non_cell_rejected(self):
        cfg,tape,res,_=self.cases[0]
        cfg=replace(cfg,receiver_mode='fifo')
        with self.assertRaises(ValueError):audit_trace(cfg,tape,res)


if __name__=='__main__':unittest.main()

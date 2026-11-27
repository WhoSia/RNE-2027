"""Observation-only laboratory API; no actuators or real road connection.
Protocol violations and unsupported observations fail closed. Stage numbers are
causal sequence IDs, not calibrated timestamps. A request reserves credits.
"""
from model import CREDITS

class DecisionSession:
    def __init__(self,planner,belief):
        self.planner=planner;self.b=belief;self.stage=1
        self.h=planner.model.c.horizon;self.remaining=planner.model.c.budget
        self.phase='READY';self.mode=None;self.action_id=None;self.reason=None
    def _fail(self,reason):
        self.phase='ABSTAINED';self.reason=reason
        return {'status':'ABSTAINED','reason':reason,'remaining':self.remaining}
    def _require(self,stage,phase):
        if self.phase in ('ABSTAINED','DONE'):return False
        if stage!=self.stage or self.phase!=phase:self._fail('PROTOCOL_ORDER');return False
        return True
    def status(self):return {'status':self.phase,'reason':self.reason,'remaining':self.remaining,'stage':self.stage}
    def request(self,stage):
        if not self._require(stage,'READY'):return self.status()
        self.mode=self.planner.sense(self.b,self.h,self.remaining,min(self.h,self.planner.depth))[1]
        credit=CREDITS[self.mode]
        if credit>self.remaining:return self._fail('BUDGET')
        self.remaining-=credit;self.phase='WAIT_MEASUREMENT' if credit else 'CAN_DECIDE'
        return {**self.status(),'mode':self.mode,'reserved':credit}
    def supply(self,stage,value):
        if not self._require(stage,'WAIT_MEASUREMENT'):return self.status()
        parts=self.planner.model.partition(self.b,self.mode)
        if not isinstance(value,str) or value not in parts:return self._fail('UNSUPPORTED_PAID_OBSERVATION')
        self.b=parts[value][1];self.phase='CAN_DECIDE';return self.status()
    def decide(self,stage):
        if not self._require(stage,'CAN_DECIDE'):return self.status()
        self.action_id=self.planner.control(self.b,self.h,self.remaining,min(self.h,self.planner.depth))[1]
        self.phase='WAIT_NEXT';return {**self.status(),'action':self.action_id}
    def receive_next(self,stage,observation):
        if not self._require(stage,'WAIT_NEXT'):return self.status()
        if self.h==1:self.phase='DONE';return self.status()
        _,parts=self.planner.model.predict(self.b,self.action_id)
        if not isinstance(observation,(tuple,list)) or len(observation)!=4:return self._fail('INVALID_FREE_OBSERVATION')
        key=tuple(observation)
        try: entry=parts.get(key)
        except TypeError:return self._fail('INVALID_FREE_OBSERVATION')
        if entry is None:return self._fail('UNSUPPORTED_FREE_OBSERVATION')
        self.b=entry[1];self.h-=1;self.stage+=1;self.mode=None;self.action_id=None;self.phase='READY';return self.status()

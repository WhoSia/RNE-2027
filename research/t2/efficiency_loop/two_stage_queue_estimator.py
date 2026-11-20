"""A minimal *adaptation* of Shafik & Rakha (2025) two-stage state estimation.

Stage I: movement fraction from a sparse probe sample + process prior.
Stage II: queue from detector arrival totals, estimated turn share,
         observed service and optional noisy queue measurement.

This is NOT the authors' full adaptive Kalman estimator, and the observation
variances are synthetic teaching parameters, not fitted detector errors.
It deliberately has no signal-actuation API and is not a field estimator.
"""
from dataclasses import dataclass
import math


@dataclass
class ScalarFilter:
    mean: float
    variance: float

    def predict(self, drift=0., process_variance=0.):
        if not math.isfinite(drift) or not math.isfinite(process_variance) or process_variance<0:
            raise ValueError('invalid process parameters')
        self.mean+=drift
        self.variance+=process_variance
        return self.mean

    def observe(self, measurement, observation_variance):
        if not math.isfinite(measurement) or not math.isfinite(observation_variance) or observation_variance<=0:
            raise ValueError('invalid measurement variance or value')
        if self.variance<0:raise ValueError('negative covariance')
        gain=self.variance/(self.variance+observation_variance)
        self.mean+=gain*(measurement-self.mean)
        self.variance=(1-gain)*self.variance
        return gain


class TwoStageQueueEstimator:
    def __init__(self, prior_turn_fraction=.5,turn_variance=.05,prior_queue=0.,queue_variance=4.):
        if not 0<=prior_turn_fraction<=1 or min(turn_variance,prior_queue,queue_variance)<0:
            raise ValueError('invalid initial state')
        self.turn=ScalarFilter(float(prior_turn_fraction),float(turn_variance))
        self.queue=ScalarFilter(float(prior_queue),float(queue_variance))
        self.tick=-1

    def update(self, tick, *, detector_total, probe_left, probe_total, left_discharge,
               queue_measurement=None, queue_measurement_variance=4.):
        if type(tick) is not int or tick<=self.tick:
            raise ValueError('updates require strictly increasing capture ticks')
        if any(type(x) is not int or x<0 for x in (detector_total,probe_left,probe_total,left_discharge)):
            raise ValueError('invalid count')
        if probe_left>probe_total or probe_total>detector_total:
            raise ValueError('probe observations cannot exceed observed arrivals')
        # Preflight all user-supplied measurements before mutating either filter.
        if queue_measurement is not None and (not math.isfinite(queue_measurement) or queue_measurement<0):
            raise ValueError('negative or nonfinite observed queue')
        if queue_measurement is not None and (not math.isfinite(queue_measurement_variance) or queue_measurement_variance<=0):
            raise ValueError('invalid queue measurement variance')
        self.tick=tick
        self.turn.predict(process_variance=.0025)
        if probe_total:
            ratio=probe_left/probe_total
            # Nonzero floor prevents illusory certainty from 0/n or n/n.
            self.turn.observe(ratio,max(.01,ratio*(1-ratio)/probe_total))
        self.turn.mean=min(1.,max(0.,self.turn.mean))
        estimated_left=detector_total*self.turn.mean
        # Propagate uncertain movement split into queue prediction variance.
        self.queue.predict(drift=estimated_left-left_discharge,
                           process_variance=1.+detector_total**2*self.turn.variance)
        self.queue.mean=max(0.,self.queue.mean)
        if queue_measurement is not None:
            self.queue.observe(float(queue_measurement),queue_measurement_variance)
            self.queue.mean=max(0.,self.queue.mean)
        return {'tick':tick,'estimated_left_arrivals':estimated_left,
                'estimated_turn_fraction':self.turn.mean,'turn_variance':self.turn.variance,
                'estimated_queue':self.queue.mean,'queue_variance':self.queue.variance}


def synthetic_example():
    """Preselected synthetic 8-cycle illustration, no empirical calibration."""
    filter=TwoStageQueueEstimator(prior_turn_fraction=.4)
    raw_probes=[5,6,6,7,5,6,7,6]
    # True 60% of 20 arrivals are turning; 7 discharge in each cycle.
    # A noisy independent queue reader is treated as another observation.
    queue_readings=[6,9,17,19,26,29,36,39]
    series=[]
    for t,(pl,q) in enumerate(zip(raw_probes,queue_readings)):
        obs=filter.update(t,detector_total=20,probe_left=pl,probe_total=10,
                          left_discharge=7,queue_measurement=q,queue_measurement_variance=4.)
        obs['true_queue']=5*(t+1)
        obs['raw_probe_turn_fraction']=pl/10
        series.append(obs)
    return series

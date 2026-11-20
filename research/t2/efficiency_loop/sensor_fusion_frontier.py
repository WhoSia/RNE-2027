"""Numerical sensitivity frontier; evidence only for the published synthetic 16 worlds."""
from fractions import Fraction as F
import json
from sensor_fusion_decision import Channel, optimize
from sensor_cost_policy import Source, pick


def regret(mode_error,arrival_error):
    structure=optimize(Channel(mode=True),F(mode_error)).worst_regret
    fusion=optimize(Channel(mode=True,arrival=True),F(mode_error),F(arrival_error)).worst_regret
    return structure,fusion


def incremental_value(mode_error,arrival_error):
    s,f=regret(mode_error,arrival_error)
    return max(0.,s-f)  # protect floating-point cancellation


def boundary(arrival_error, *, lower=0.,upper=.5, tolerance=1e-7):
    """Largest mode-error bound for which arrival information has >tolerance gain.

    Binary search relies on monotone *empirically verified* switch in this
    fixed example. It is not a theorem for arbitrary traffic domains.
    """
    if incremental_value(lower,arrival_error)<=tolerance:
        return lower
    if incremental_value(upper,arrival_error)>tolerance:
        return upper
    for _ in range(35):
        middle=(lower+upper)/2
        if incremental_value(middle,arrival_error)>tolerance:
            lower=middle
        else:
            upper=middle
    return (lower+upper)/2


def report():
    arrival_error=F(1,10)
    quality=[]
    for percent in (0,1,2,2.5,3,5,10,20,30):
        mode_error=F(str(percent))/100
        s,f=regret(mode_error,arrival_error)
        quality.append({'mode_error_bound':float(mode_error),
                        'arrival_error_bound':float(arrival_error),
                        'mode_only_worst_regret':round(s,9),
                        'mode_and_arrival_worst_regret':round(f,9),
                        'incremental_arrival_value':round(max(0.,s-f),9)})
    sensors={
      'structure':Source('structure',False,80,81,81,F(1,100),F(1)),
      'forecast':Source('arrival',True,80,81,88,F(1,10),F(1)),
      'too_late':Source('arrival',True,80,85,88,F(1,10),F(1))
    }
    scenarios={
      'both_predecision':pick([sensors['structure'],sensors['forecast']],84,3),
      'forecast_late':pick([sensors['structure'],sensors['too_late']],84,3),
      'cost_budget_one':pick([sensors['structure'],sensors['forecast']],84,1),
      'no_budget':pick([sensors['structure'],sensors['forecast']],84,0)
    }
    return {'status':'synthetic-only',
            'assumptions':'independent conditional channel errors; uniformly distributed wrong future-arrival labels; two whole-simulator bypass modes',
            'frontier':quality,
            'arrival_error_10pct_mode_error_breakpoint_approx':round(boundary(arrival_error),8),
            'availability_and_cost_examples':scenarios}


if __name__=='__main__':
    from pathlib import Path
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('output',type=Path);args=ap.parse_args()
    args.output.write_text(json.dumps(report(),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

"""Predict held-out trials before receiving truth; custody is external."""
from math import isfinite
from rf14_blind_contract import active_plan, exact, seal_predictions
from rf_pilot_evaluator import REQUIRED, MODELS, validate, fit_predict

FEATURE_KEYS = set(REQUIRED) - {'label', 'ground_truth_source'}
TRAIN_CELLS = {('S1', 'P1'), ('S2', 'P1')}


def predict_blind(plan, train, holdout):
    active = active_plan(plan)
    training = {k:r for k,r in active.items() if (r['session_id'],r['placement_id']) in TRAIN_CELLS}
    testing = {k:r for k,r in active.items() if k not in training}
    train = list(exact(training, train).values())
    holdout = list(exact(testing, holdout).values())
    if not train or not holdout:
        raise ValueError('empty split')
    validate(train)
    for row in holdout:
        if set(row) != FEATURE_KEYS:
            raise ValueError('holdout schema must contain features only')
        if row['trial_origin'] != train[0]['trial_origin'] or row['quality'] not in ('ok','missing'):
            raise ValueError('invalid holdout provenance or quality')
        for field in REQUIRED[7:]:
            if row[field] not in ('',None):
                try:
                    valid = isfinite(float(row[field]))
                except (TypeError, ValueError):
                    valid = False
                if not valid:
                    raise ValueError('invalid telemetry')
    for row in train + holdout:
        expected = active[row['trial_id']]
        if any(row[f] != expected[f] for f in ('session_id','placement_id')):
            raise ValueError('cell mismatch')
    results = {}
    for name, fields in MODELS.items():
        predictions, fit = fit_predict(train, holdout, fields)
        payload, digest = seal_predictions(plan, [
            {'trial_id':r['trial_id'], 'prediction':p}
            for r,p in zip(holdout,predictions)])
        results[name] = {'payload':payload, 'sha256':digest, 'fit':fit}
    return {'status':'PREDICTIONS_ONLY_CUSTODY_EXTERNAL', 'train_n':len(train),
            'test_n':len(holdout), 'models':results}

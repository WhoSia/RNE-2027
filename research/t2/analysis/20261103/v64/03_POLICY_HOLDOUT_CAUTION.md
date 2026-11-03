# T2 v6.4-P0 — A synthetic train/holdout warning-penalty counterexample

Source: v6.3 144 matched vehicle-simulation scenario×seed cases (3 demand×3 brake×2 lateral×8 seeds). Train seeds 400-403 (72 cases); holdout seeds 404-407 (72 cases). True demand/brake/lateral parameters assumed available as group labels, so this is NOT a feasible field policy-learning study.
Action: guard 0s vs 1s. Cost = vehicle-seconds relative to zero guard + λ * 1{simulation had >=1 braking-warning time step}; λ in 0,25,100,500 *arbitrary* vehicle-second equivalents. Warning indicators are diagnostic, not accidents.
For λ=0/25/100, training policy chooses guard0 for all 72 holdout scenarios. For λ=500 it chooses guard1 in 4/72, yet two holdout warning-positive cases remain. Mean holdout cost=18.872 (fitted) vs 13.889 (always guard0) vs 3.8125 (per-case clairvoyant oracle), under the study's artificial penalty. Average excess cost vs clairvoyant=15.059.
Observed warning cases concentrate in seed 407, which was not in training, while a seed 400 warning led to a group choice with no holdout benefit. With only 4 distinct holdout seeds, this is a *diagnostic failure of generalization*, not population inference.
Do not optimize real-road policies with these toy weights. Real signal clearance must follow grounded operational constraints and relevant authority rather than synthetic optimization.

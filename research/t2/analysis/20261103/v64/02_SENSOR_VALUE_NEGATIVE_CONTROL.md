# T2 v6.4-P0 — More accurate sensing need not reduce policy regret

Data source: v6.3 15 post-selected baseline-aggregate-identical synthetic seeds; candidate models brake=2 and brake=3 m/s²; exact synthetic mean entry speed for each candidate and seed, equal prior, independent additive Gaussian measurement error.
30,000 synthetic sensor draws per sigma (15 seeds×2 candidate truths×1,000 draws). Noise sigma 0/.05/.1/.25/.5 m/s: model classification accuracy 1.000/.912/.757/.611/.554.
Under objective J=total vehicle-seconds **only**, zero extra guard weakly dominates the 1-second guard in this selected data, for both candidate models. All classifications therefore select zero extra guard and measured regret relative to the known model's best of these two options is ZERO at all noise levels.
This is an important **negative result**, not a successful new signal controller. The sensor model uses true candidate-specific synthetic expectations from each seed (oracle feature knowledge) and is not field-trained or implementable as-is. Selected matching cases are not an independently sampled population. Correctly identifying model parameters is not sufficient for a *strict* decision-value improvement if the optimal policy is shared by all candidate models.
Do not claim real-world sensor effectiveness or optimal traffic-signal design.

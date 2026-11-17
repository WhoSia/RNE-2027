# What each source licenses us to test

- [Geroliminis and Skabardonis (2011)](https://doi.org/10.1109/TITS.2011.2141991)
  suggests detector occupancy and weak upstream discharge during green as
  a joint spillover indicator. Add observed upstream demand to distinguish
  blocked service from low demand, and audit startup loss independently.
- [Cao et al. (2019)](https://doi.org/10.1177/0361198119837178) tests
  penetration, bay length and turn ratio in a simulation-based spillback
  estimator. Pair equal turn fractions with different arrival orders and
  score adjacent-through obstruction separately. The completed cycle’s
  queue composition is not a prospective signal input.
- [Christofa et al. (2013)](https://doi.org/10.1177/0361198113235600108)
  contrasts last-observed-vehicle and upstream-signal inputs. Compare
  observations under the same latent worlds and account for the time at
  which each input is available. The paper's forecast of queue growth
  through the cycle can overstate risk.
- [Ashqer et al. (2022 preprint)](https://arxiv.org/abs/2207.08025)
  estimates lane-specific queues from aerial trajectories. Label queue
  position and censoring in addition to speed; compare independent
  labels before using them as a reference for the simulator.
- [Xu et al. (2019)](https://doi.org/10.1155/2019/3149275) provides
  a comparator that modulates inflow when space is limited. Its cycle
  and phase order are fixed. Use a complete small catalogue and common
  input worlds before attributing gains to an optimizer or phase order.
- [Varaiya (2013)](https://doi.org/10.1016/j.trc.2013.08.014) establishes
  stability subject to its point-queue assumptions.
  [Grégoire et al. (2015)](https://doi.org/10.1109/TCNS.2014.2378871)
  motivates a finite-capacity pressure comparator and records possible
  starvation with queue-length-only priorities. Add maximum individual
  wait and compare at matched feasibility.
- [Han et al. (2024)](https://doi.org/10.1111/mice.13144) validates
  a controller with field spillover indicators. Preserve indicator
  definitions and specify the before/after comparability independently.
  [Tan et al. (2025), open preprint](https://arxiv.org/abs/2406.14108)
  motivates uncertainty sets for demand and measurement errors. Our
  finite-support ex post oracle bounds the regret of a fixed feasible
  choice and does not reproduce their controller or loss.

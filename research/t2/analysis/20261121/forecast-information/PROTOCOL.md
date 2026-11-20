# Forecast error and phase-order regret

Reuse the 768 synthetic streams, all four storage combinations,
decision tick 84 and the two actions from the storage experiment.
Use the complete varied arrival prefix and east pocket/receiver counts
as the no-forecast baseline. Group worlds by that information before
any forecast is added. Account separately for terminal penalties
0, 60 (primary) and 120.

Test a single binary forecast for each of the three future two-tick bins.
The message predicts which east movement arrives first. For every
compatible world, allow the conditional error probability to range
from zero up to the same bound e. Score worst-case *expected* regret
over worlds and error probabilities. Enumerate the four deterministic
maps from the binary message to a phase order, including both constant
maps. Compute exact rational break-even error and report a small grid
as a check. A site-wide average accuracy does not imply the per-world
guarantee used here. Report the best bin as a hindsight design comparison,
not a field deployment result. No real forecast or holdout data is used.

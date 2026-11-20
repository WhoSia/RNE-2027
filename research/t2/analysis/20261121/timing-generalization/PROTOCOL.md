# New-seed test of the scarce bypass timing effect

Freeze a new synthetic evaluation panel of seeds 211, 337, 479, 613,
with all six existing demand contexts per seed. The resulting RNG inputs
are distinct from those in the original 17/83 panel. No demand context
is selected or dropped after calculation. Use the original two seeds as
a reconstruction control. This is an independent seed panel inside
the same generator, not a new traffic model or a field validation.

Retain the pocket-only condition, horizon 336, decision 84, bounded
depth-one bypass and matched arrivals and calendars from the previous
experiment. Compare early and late schedules with 1, 2 and 6 eligible
ticks inside [84,96). For each matched waveform retain area and terminal
unfinished-weight differences, so alternative terminal penalties do not
require new simulations. The primary cost is penalty 60; report also
0 and 120, and require the same strict reversal orientation throughout
[30,90] for the robustness check. Report cases by demand context as well
as arrival stream. Do not retune the exhibit or open the K047 holdout
based on sign counts.

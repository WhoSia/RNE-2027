# Offset choices with partial corridor information

Reuse D48's two-junction, straight-only finite-storage model and enumerate
every integer offset of junction B in a 60 s cycle. The downstream light and
vehicles already stored on the link determine whether the upstream light can
admit a vehicle. The simulator uses start-of-tick storage and positive travel.

Across 24 synthetic situations, vary directional counts (12/6, 9/9, 6/12 per
cycle), relative west platoon onset (0 or 14 s), directional storage
(3 east and 12 west, or the reverse), and link travel (8 or 16 s). Reuse each
arrival sequence for all 60 offsets, using three arrival cycles, a 20 s common
green and a 1,200 s horizon. Count the two directions together for total delay.
Demand ends early enough for all arms to clear. Any unfinished arm invalidates
the single-metric comparison, since completed-only delay would be selective.

Compare the fixed zero offset, one global minimax-cost offset, one global
minimax-regret offset, minimax regret with directional counts, with counts and
link storage, and with counts, storage and west platoon onset. For each, report
worst absolute total delay, worst regret against the world-specific best
offset, and worst blocked green time. The directional count regime is a
measurement abstraction; exact storage is a design input in this experiment.
The platoon onset describes a forecast feature at decision time. No actual
Jinju lane record, measured platoon clock, or real road claim enters here.
Policies and scores use the same finite support to describe value under that
support. Subsequent predictive evaluation will need independent time blocks.

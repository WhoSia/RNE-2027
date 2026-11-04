# Protocol, failed pilot, and bounded interpretation

## Independent audit model
Two serial intersections, discrete single-step movement, fixed 12-step signal cycle, main green 4/6/8 steps per intersection, B offset 0/3/6 steps. 27 exhaustive candidates. Demand modes: balanced, platoon and side_peak; intermediate buffer 1/3/8 integer vehicle slots; fixed travel lag 3 steps. Arrivals before step120; evaluate 180 steps. Three training seeds (101,103,107) and 24 unused test seeds (201..224). Same arrivals for all tested policies. 216 paired scenario-seed blocks and 648 evaluation runs for fixed/coordinate/exhaustive strategies.

## Negative diagnostic
Initial model (preserved in ZIP) had zero link travel delay AND lower demand rates. Storage 1/3/8 produced identical optimal decisions. It was an uninformative model, not evidence that storage has no physical value. Never attribute the cross-version difference to travel time alone because demand was also changed.

## Controlled ablation
Within the revised model, same arrivals/seed, same (6,6,0) policy, same capacity; change only travel lag 0→3. At buffer1 the increase in 180-step incomplete-vehicle exposure is +5220.42 (balanced), +5493.75 (platoon), +5177.58 (side_peak), each averaged across 24 seeds; approximately 59 additional blocked time steps per run. At capacity3 or8, no extra blocked steps from travel lag in those test conditions. **Capacity is integer slots, not meters.**

## End-of-horizon censoring
The objective is summed unfinished-vehicle exposure across t=0..179 (vehicle-steps), not completed all-vehicle trip time. For balanced buffer1 under exhaustive policy, average 40.54 vehicles remain unfinished. The queue may be artificial and grossly unrealistic, so these magnitudes have no field interpretation.

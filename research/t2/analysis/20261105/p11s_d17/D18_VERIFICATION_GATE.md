# D18 validation gate (P12 stays frozen)
1. Implement finite **physical storage** K=floor(L/(vehicle_length+gap)) with units in m and no arbitrary transport/storage equivalence. Specify edge boundary, blocking, transfer, and the minimum travel time between stop lines.
2. Distinguish *exit of an occupied road section* from *new space availability at its upstream entry*. Event propagation must not be backwards in time or instantaneous unless mathematically justified.
3. A three-link motif (upstream U -> pocket P -> output D) with finite P and blocked D; identify exact queue spillback start and buffer-full condition.
4. Compare no finite storage, FIFO global, FIFO per lane, and a physically appropriate SUMO meso-LTM/micro baseline under matching demand and fixed signal schedule.
5. Obtain independent observation of real queue length; Jinju traffic counts alone do not measure full bumper-to-bumper queues. Demand from detector counts is not automatically arrivals.
6. Formalize separate article (causality/consistency) and student exhibition (observable physical queue spillback), with competition disclosure/duplicate work rules checked before publication.
7. Policy track: ideas/concept notes only, no objective tuning, optimization, reinforcement learning controller or live/field actuation.

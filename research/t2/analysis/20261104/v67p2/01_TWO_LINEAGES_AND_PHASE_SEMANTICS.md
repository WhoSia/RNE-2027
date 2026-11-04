# T2 v6.7-P2: both actual P1 source trees reviewed (20261104)

P1a source: T2_v67_P1_mixed_fleet_storage_pedestrians_20261104.zip, Drive ID 1tHw8BxV1BKnZOElQlKT5JEo1mab7wQru; file network_v67.py. P1b source: T2_v67_P1b_comparison_integrated_20261104.zip; file network_v67_p1.py. Both source trees preserved unchanged in new P2 ZIP.

At common 60s cycle, 30s main, 3s lost, 24s side green, 3s lost: P1a vehicle turn [33,49), pedestrian-exclusive WALK [49,57) when block=8s. P1b does not create pedestrian WALK, but prohibits side-turn entry [33,41) then permits turn [41,57). These are not the same policy.

Further differences include truck length P1a 10m vs P1b 11m, fixed P1a IDM time gap 1.7s vs P1b class-specific 1.3/1.9s, P1a acceleration-based earliest-reach admission vs P1b constant-speed conservative arrival gate, as well as receiving-link and discharge model differences. Even walk=0 is not an aligned-physics contrast. No claims of traffic policy superiority.
# P9 complete-horizon grid results

All 864 runs report zero simulation integrity issues and full vehicle completion at horizon 1200s.

For 16 demand x storage x seed blocks, the best of 27 policies changed in 0/16 on dt .5 -> .25. Among 5616 possible unordered pairs, 5611 were strictly ordered at both step sizes, and 19 reversed; affected blocks: 6/16. There are 432 directly paired policy comparisons: mean absolute objective difference 121.1712963 vehicle-seconds, maximum 1304.0, 97/432 exceed 1% relative difference, 49/432 exceed 5%, 18/432 exceed 10%. Maximum relative difference 15.277%. This is simulation-numerical sensitivity, NOT road performance.

The invariance of the global winner in 16 blocks does NOT prove a robust optimum on another input distribution, SUMO, or real intersections. The pairwise inversions cannot be attributed to finite horizon censoring because all corresponding vehicles completed.

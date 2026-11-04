# P8 SUMO execution and safety-to-claim gates

Local code in Drive ZIP: code/sumo_preflight.py and code/sumo_benchmark_runner.py. Source unchanged.

Checks before running SUMO: run.sumocfg dependency closure, missing/empty files, no absolute/traversal path, parseability, network lane IDs, signal connection linkIndex contiguous unique indices, signal-state width against controlled connections, detector positions within lanes, valid route XML, source SHA256 receipts. Supports identifying effective last-loaded tls program when no WAUT.

Official SUMO Traffic Lights documentation: additional signal programs override baseline when last loaded, unless WAUT. Bologna net has default programID 0, separate additional programID utopia; do not assume which is active without runtime check. Source: https://sumo.dlr.de/docs/Simulation/Traffic_Lights.html

If a complete scenario and SUMO executable become available, runner uses --tripinfo-output.write-unfinished true, --tripinfo-output.write-undeparted true, summary and statistics, logs, run manifest outside immutable source folder. SUMO TripInfo docs: https://sumo.dlr.de/docs/Simulation/Output/TripInfo.html

P8 self-tests 11/11; previous T2 P2 tests 28/28. Applied preflight to present 670-byte config only and got BLOCKED_INCOMPLETE_SCENARIO listing seven missing referenced files. No code shall convert a failed preflight into a claimed run.

# Practice: Multi-Robot Systems

1. **A third robot.** Extend `multi_robot_sim.launch.py` to spawn a
   `robot3` alongside `robot1`/`robot2`, and update
   `fleet_coordinator.py` to command and log all three — confirm the
   namespacing pattern scales cleanly to N robots, not just 2.

2. **Break TF namespacing on purpose.** Remove the `frame_prefix`
   parameter from one robot's `robot_state_publisher` in
   `make_robot_group()`, re-launch, and use `ros2 run tf2_tools
   view_frames` to confirm you see the collision DEEP_DIVE.md warns
   about — then fix it and confirm two clean separate trees again.

3. **Relative task assignment.** Modify `fleet_coordinator.py` so
   instead of hardcoded different commands, it assigns robot1 and robot2
   goals based on which one is currently closer to a fixed target point
   (using their odometry) — a tiny, centralized task-allocation rule,
   foreshadowing more sophisticated multi-robot coordination.

4. **Shared map, independent AMCL.** Bring up Chapter 11's Nav2 stack
   twice, once per robot namespace, both pointed at the same map file —
   confirm each robot localizes independently and can be sent
   independent `NavigateToPose` goals without interfering with the
   other's localization.

5. **Stretch:** with both robots running Nav2 (per #4), drive them
   toward each other's starting positions and observe whether either
   robot's costmap picks up the other as an obstacle via lidar (per
   DEEP_DIVE.md's note that Nav2 has no built-in inter-robot
   coordination beyond what each robot's own sensors see) — confirm or
   refute that claim experimentally.

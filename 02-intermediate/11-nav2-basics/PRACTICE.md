# Practice: Nav2 Basics

1. **Multiple goals in sequence.** Modify `send_goal.py` to accept a
   list of (x, y) waypoints and drive through all of them in order,
   waiting for each `NavigateToPose` result before sending the next.

2. **Tune the costmap on purpose.** Halve `robot_radius` in
   `nav2_params.yaml` and confirm the robot's planned paths pass closer
   to the map edge/obstacles than before; then double it and confirm
   Nav2 refuses to plan through gaps it previously handled fine — a
   hands-on look at DEEP_DIVE.md's inflation pitfall in both directions.

3. **No initial pose, on purpose.** Skip the "2D Pose Estimate" step and
   immediately send a goal via `send_goal.py`. Observe what happens
   (AMCL's particle filter starting from a broad/undefined guess) and
   write one sentence on why this matters for a real robot that can't
   rely on a human clicking in RViz2 every startup.

4. **A real obstacle.** Add a static box to `empty_world.sdf` between the
   spawn point and a goal you send. Confirm Nav2's global plan routes
   around it rather than through it, and that the local controller
   reacts if you also move the box during a run (if your Gazebo version
   supports moving a spawned model at runtime).

5. **Stretch:** write a node that subscribes to `/amcl_pose` and
   `/plan`, and periodically logs the straight-line distance between the
   robot's current pose and its final goal vs. the *remaining path
   length* along the plan — the difference between them is a rough
   measure of how much the planned route detours around obstacles.

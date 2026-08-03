# Practice: Gazebo Basics

1. **Drive a shape.** Change `simple_diffdrive.urdf.xacro`'s chassis
   from a box to a cylinder, re-launch, and confirm it still drives
   correctly (this is really a test of whether you understand which
   parts of the file are visual-only vs. physically load-bearing).

2. **Add an obstacle.** Edit `empty_world.sdf` to add a second static
   `<model>` (a box) a couple of meters in front of the spawn point.
   Drive toward it with `ros2 topic pub` and confirm the robot's
   collision geometry actually stops it (or, at low speed, that you can
   see the collision in Gazebo even without a controller reacting to
   it yet — Nav2's obstacle avoidance is Chapter 11's job, not this
   chapter's).

3. **Tune the real-time factor.** Deliberately shrink the physics engine's
   step size in `empty_world.sdf` (or increase the number of obstacles)
   until you see the real-time factor drop below 1.0 in Gazebo's stats,
   confirming you can recognize DEEP_DIVE.md's RTF pitfall when it
   actually happens, not just read about it.

4. **A square path.** Write a small Python node (not `ros2 topic pub`)
   that publishes a sequence of `Twist` commands to drive the robot in
   roughly a 1m square: forward, turn 90°, forward, turn 90°, ×4 — timing
   each leg rather than using real feedback (Chapter 11's Nav2 will do
   this properly; this is about getting comfortable commanding motion
   from code first).

5. **Stretch:** bridge and log `/odom` to a file while driving the
   square from #4, then plot the resulting X/Y trajectory (e.g. with
   matplotlib) and see how far the ending position drifts from a
   perfect square — first-hand look at open-loop dead-reckoning error.

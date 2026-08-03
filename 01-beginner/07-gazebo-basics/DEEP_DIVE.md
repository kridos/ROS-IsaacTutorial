# Chapter 7 Deep Dive: Gazebo Basics

## Gazebo Harmonic architecture

Modern Gazebo (`gz-sim`, what "Gazebo Harmonic" ships) is a separate
program from ROS2 — it has no idea what a ROS2 node or topic is on its
own. It simulates:

- **Worlds**, described in **SDF** (Simulation Description Format) — an
  XML format similar in spirit to URDF but describing an entire scene:
  ground plane, lighting, physics engine settings, and the models placed
  in it. `empty_world.sdf` in this chapter's demo is a minimal SDF world.
- **Models**, which can be authored in SDF directly, or — as this
  chapter does — a URDF/Xacro robot description (from Chapter 5) with
  Gazebo-specific `<gazebo>` extension tags added, telling Gazebo which
  plugins to load for that model (e.g. a differential-drive controller).

Since Gazebo and ROS2 are separate programs, something has to translate
between Gazebo's internal topics and ROS2 topics — that's the
**ROS2↔Gazebo bridge**.

## The ROS2↔Gazebo bridge (`ros_gz_bridge`)

`ros_gz_bridge` is a node that translates specific topics bidirectionally
between Gazebo's transport layer and ROS2's, based on a config you supply
mapping Gazebo topic/type pairs to ROS2 topic/type pairs. It does **not**
auto-bridge everything — you list exactly which topics to bridge and in
which direction, which keeps you in control of what crosses the boundary
(and avoids flooding ROS2 with every internal Gazebo topic you don't
care about).

This chapter's demo bridges two topics:
- `/cmd_vel` (ROS2 → Gazebo): velocity commands you publish get forwarded
  into the simulated diff-drive plugin.
- `/odom` (Gazebo → ROS2): the diff-drive plugin's estimated odometry
  gets forwarded out to ROS2 so you (or later, Nav2) can read it.

## The diff-drive plugin

A `<gazebo>` block in the URDF (specifically, inside `<gazebo><plugin
filename="gz-sim-diff-drive-system" ...>`) attaches Gazebo's built-in
differential-drive controller to the two wheel joints. Given a linear and
angular velocity command, it computes the individual wheel speeds needed
to achieve that motion and applies the corresponding torques in the
physics simulation — you don't have to hand-write the differential-drive
kinematics yourself; the plugin implements the standard formulas.

## Spawning a robot into a running world

`ros_gz_sim create` (used inside this chapter's launch file) takes a
robot description (from the `/robot_description` topic, following the
same `robot_state_publisher` pattern as Chapter 5) and spawns it as a
model into an already-running Gazebo world, at a given pose. This is why
`robot_state_publisher` appears again in this chapter's launch file even
though nothing here uses RViz2 directly — Gazebo spawning depends on the
same `robot_description` parameter mechanism.

## Common pitfalls

- **Physics step size / real-time factor**: Gazebo simulates physics in
  fixed small time steps (commonly 1ms) and reports a "real-time factor"
  (RTF) showing how its simulated time compares to wall-clock time. An
  RTF well below 1.0 means the simulation is running slower than
  real-time — often caused by an underpowered machine, too many/complex
  collision shapes, or too small a step size for the scene's complexity.
  A robot that looks "sluggish" or physically unstable (jittering,
  sinking through the floor) is very often a step-size/RTF problem, not
  a bug in your URDF.
- **ROS_DOMAIN_ID / bridge topic name mismatches**: if `/cmd_vel`
  commands seem to go nowhere, check that the bridge's configured ROS2
  topic name matches exactly what you're publishing to (`ros2 topic
  list` should show `/cmd_vel` with a subscriber count > 0 once the
  bridge is running) — a mismatched name here silently does nothing, the
  same class of bug as Chapter 2's topic name pitfall, just crossing a
  process boundary this time.

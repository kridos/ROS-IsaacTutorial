# Tier 2 — Intermediate

Goal: go beyond single-node basics into the systems real robots run —
transforms, real sensor data, the communication layer underneath ROS2,
and two of the field's standard stacks (Nav2 for navigation, MoveIt2 for
manipulation) — then take your first steps into NVIDIA Isaac Sim.

Assumes Tier 1 complete. Chapters 13-14 additionally require Isaac Sim
installed on a machine with an NVIDIA GPU (see Chapter 13's DEEP_DIVE.md
for prerequisites) — everything before that only needs what Tier 1
already set up.

## Chapters

8. [TF2](08-tf2/OVERVIEW.md) — transforms and coordinate frames.
9. [Simulated sensors](09-simulated-sensors/OVERVIEW.md) — camera,
   lidar, and IMU in Gazebo.
10. [ROS2 architecture deep dive](10-ros2-architecture-dds-qos/OVERVIEW.md)
    — DDS and QoS.
11. [Nav2 basics](11-nav2-basics/OVERVIEW.md) — mapping, localization,
    path planning.
12. [MoveIt2 basics](12-moveit2-basics/OVERVIEW.md) — arm motion
    planning.
13. [Isaac Sim intro](13-isaac-sim-intro/OVERVIEW.md) — Omniverse, USD,
    importing a robot.
14. [ROS2 <-> Isaac Sim bridge](14-ros2-isaac-sim-bridge/OVERVIEW.md) —
    driving an Isaac Sim robot from ROS2.

Start with Chapter 8 if you've just finished Tier 1.

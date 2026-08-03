# Demo: Nav2 Basics

## Prerequisites

```bash
sudo apt install ros-jazzy-navigation2 ros-jazzy-nav2-bringup
```

Plus everything Chapter 9's demo needed (Gazebo, ros_gz_bridge, xacro).

## Generate the map (one-time)

```bash
python3 generate_empty_map.py
```

Creates `empty_map.pgm` and `empty_map.yaml` in this directory — a
trivial all-free-space map matching the empty Gazebo world (see
DEEP_DIVE.md and the script's own comments for why a hand-generated
empty map is used instead of a SLAM-built one for this basics chapter).

## How to run

```bash
ros2 launch nav2_sim.launch.py
```

This starts Gazebo, spawns the robot, bridges `/cmd_vel`/`/odom`/`/scan`,
brings up the full Nav2 stack via `nav2_bringup`, and opens RViz2 with
Nav2's default navigation display.

## Give AMCL an initial pose (required first step)

In the RViz2 window: click the **"2D Pose Estimate"** button in the
toolbar, then click-and-drag on the map at roughly where the robot
spawned (near the origin) — this publishes to `/initialpose` and lets
AMCL start localizing (see DEEP_DIVE.md — without this, Nav2 won't know
where the robot starts).

## Send a navigation goal (RViz2)

Click **"Nav2 Goal"** in the RViz2 toolbar, then click-and-drag on the
map to set a target position and facing direction.

Expected: a path appears drawn on the costmap, and the robot (visible in
the separate Gazebo window) drives along it, stopping at the goal.

## Send a navigation goal (programmatically)

```bash
python3 send_goal.py 1.5 1.5
```

Expected output:

```
[INFO] [send_goal_client]: Sending navigation goal: x=1.5, y=1.5
[INFO] [send_goal_client]: Goal accepted, navigating...
[INFO] [send_goal_client]: Distance remaining: 2.05m
[INFO] [send_goal_client]: Distance remaining: 1.72m
...
[INFO] [send_goal_client]: Navigation finished with status: 4
```

(status `4` = `STATUS_SUCCEEDED`, per `action_msgs/msg/GoalStatus`.)

## Inspect what's running

```bash
ros2 lifecycle get /amcl
ros2 topic echo /amcl_pose --once
```

Expected: `/amcl` reports lifecycle state `active`, and `/amcl_pose`
shows a pose roughly matching where you set the initial pose estimate
(before moving) or the robot's current estimated position (after).

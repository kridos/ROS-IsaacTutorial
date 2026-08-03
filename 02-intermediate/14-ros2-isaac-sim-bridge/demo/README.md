# Demo: ROS2 <-> Isaac Sim Bridge

## Prerequisites

Same as Chapter 13 (Isaac Sim 4.x, NVIDIA GPU, `xacro` on PATH). No
additional ROS2 packages needed beyond a standard ROS2 install — Isaac
Sim's ROS2 Bridge extension brings its own DDS integration.

## How to run

Terminal 1 (Isaac Sim's own Python environment, same as Chapter 13):

```bash
~/.local/share/ov/pkg/isaac-sim-<version>/python.sh ros2_bridge_sim.py
```

This opens the Isaac Sim GUI window (not headless this time) showing the
robot on a ground plane.

Terminal 2 (plain system ROS2 — source `/opt/ros/jazzy/setup.bash` first):

```bash
python3 drive_and_log_odom.py
```

## Expected result

The Isaac Sim GUI window shows the robot driving forward in a straight
line. Terminal 2 logs:

```
[INFO] [drive_and_log_odom]: odom: x=0.012, y=0.000
[INFO] [drive_and_log_odom]: odom: x=0.045, y=0.000
[INFO] [drive_and_log_odom]: odom: x=0.089, y=0.000
...
```

`x` should increase steadily while the robot drives, `y` should stay
near zero (straight line, no angular velocity commanded) — the same
shape of result as Chapter 7's Gazebo `/odom` echo, now coming from
Isaac Sim instead.

## Sanity-check the bridge is actually up

```bash
ros2 topic list
ros2 topic info /cmd_vel -v
```

Expected: `/cmd_vel` and `/odom` both appear, with `/cmd_vel` showing at
least one subscriber (Isaac Sim's OmniGraph node) — if these topics
don't appear at all while `ros2_bridge_sim.py` is running, see
DEEP_DIVE.md's "extension not enabled" pitfall first.

## Compare with Chapter 7

Run Chapter 7's `gazebo_sim.launch.py` and this chapter's
`ros2_bridge_sim.py` side by side (different terminals — they use
different simulators, no conflict) and drive both with the same
`drive_and_log_odom.py`-style Twist commands. The ROS2-side experience
— topics, message types, how you'd write a consuming node — should feel
identical, even though the simulators underneath are completely
different pieces of software.

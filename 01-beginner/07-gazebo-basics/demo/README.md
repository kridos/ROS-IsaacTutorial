# Demo: Drive a robot in Gazebo

## Prerequisites

```bash
sudo apt install ros-jazzy-ros-gz ros-jazzy-ros-gz-bridge ros-jazzy-ros-gz-sim ros-jazzy-xacro
```

## How to run

```bash
ros2 launch gazebo_sim.launch.py
```

This starts, in order: the Gazebo GUI with the empty world, a
`robot_state_publisher` publishing the diff-drive robot's description,
a spawn step that adds the robot to the running world, and the
`ros_gz_bridge` connecting `/cmd_vel` and `/odom`.

## Expected result

The Gazebo window opens showing an orange box chassis with two black
wheels and a caster, sitting on a gray ground plane. It should sit still
and not sink through the floor or twitch — if it does, see DEEP_DIVE.md's
physics step size / real-time factor pitfall.

## Drive it

In another terminal:

```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.3}, angular: {z: 0.0}}" --rate 10
```

Expected: the robot drives forward in a straight line in the Gazebo view.
Try `angular: {z: 0.5}` (with `linear: {x: 0.2}`) to see it curve.

Or install `teleop_twist_keyboard` for interactive control:

```bash
sudo apt install ros-jazzy-teleop-twist-keyboard
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

## Check odometry

While driving, in a third terminal:

```bash
ros2 topic echo /odom
```

Expected: the `pose.pose.position` values change as the robot moves,
roughly matching the direction and distance you drove it.

## Sanity-check the bridge

```bash
ros2 topic list
ros2 topic info /cmd_vel -v
```

Expected: `/cmd_vel` shows at least one subscriber (the bridge) once
`gazebo_sim.launch.py` is running — if it shows zero subscribers, the
bridge isn't connected and `ros2 topic pub` commands won't reach the
robot (see DEEP_DIVE.md's bridge topic name mismatch pitfall).

# Demo: MoveIt2 Basics

## Prerequisites

```bash
sudo apt install ros-jazzy-moveit ros-jazzy-moveit-py ros-jazzy-joint-state-publisher ros-jazzy-xacro
```

## How to run

```bash
ros2 launch moveit_planning.launch.py
```

This starts `robot_state_publisher`, a plain `joint_state_publisher`
(non-GUI — MoveIt2 drives the arm, unlike Chapter 5's manual sliders),
`move_group`, and RViz2. In RViz2, add the **MotionPlanning** display
(Displays panel -> Add -> By display type -> MotionPlanning) if it
isn't already shown.

In another terminal:

```bash
python3 move_to_pose.py 0.3 0.0 0.5
```

## Expected result

Terminal output:

```
Requesting plan to pose: x=0.3, y=0.0, z=0.5
Planning succeeded, executing...
Execution complete.
```

In RViz2's MotionPlanning display, you should see the arm animate from
its starting (all-zero) configuration to a new configuration with the
gripper positioned near `(0.3, 0.0, 0.5)` in the `base_link` frame.

## Try a target that's likely unreachable

```bash
python3 move_to_pose.py 5.0 5.0 5.0
```

Expected: `Planning FAILED` — the target is far outside the arm's total
reach (link1 + link2 + link3 length is well under 1m, per
`arm_with_gripper.urdf.xacro`'s properties). Check RViz2's
MotionPlanning display for the goal-state coloring DEEP_DIVE.md
describes.

## Inspect the planning group

```bash
ros2 param get /move_group robot_description_semantic
```

Expected: prints the SRDF content loaded from `arm_with_gripper.srdf`,
confirming the "arm" planning group (joint1, joint2, joint3) was loaded
correctly.

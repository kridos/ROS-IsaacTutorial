# Demo: Visualize a simple arm in RViz2

## Prerequisites

```bash
sudo apt install ros-jazzy-joint-state-publisher-gui ros-jazzy-xacro ros-jazzy-rviz2
```

## How to run

```bash
ros2 launch display.launch.py
```

This starts three programs at once:
- `robot_state_publisher` — expands `simple_arm.urdf.xacro` and publishes
  TF for the current joint positions.
- `joint_state_publisher_gui` — a small window with two sliders (one per
  joint) that publishes `JointState` messages as you move them.
- `rviz2` — opens with `rviz_config.rviz` pre-loaded, showing the
  `RobotModel` and `TF` frames.

## Expected result

Two windows open: a slider panel (`joint1`, `joint2`) and the RViz2 3D
view showing a small gray base with a blue segment (link1) and a green
segment (link2) sticking up from it. Moving the `joint1` slider rotates
the whole blue+green assembly around the vertical axis; moving `joint2`
bends the green segment relative to the blue one.

## Verify the description directly (no GUI)

```bash
xacro simple_arm.urdf.xacro | head -30
```

Expected: well-formed URDF XML with `${...}` expressions replaced by
their computed numeric values (e.g. `link1_length/2` becomes `0.15`).

```bash
ros2 run tf2_tools view_frames
```

(while `display.launch.py` is running) generates `frames.pdf` showing the
full `base_link -> link1 -> link2` transform tree — useful for confirming
there's no disconnected link (see DEEP_DIVE.md's common pitfall).

# Demo: Multi-Robot Systems

## Prerequisites

Same as Chapter 7 (`ros-jazzy-ros-gz`, `ros-jazzy-ros-gz-bridge`,
`ros-jazzy-ros-gz-sim`, `ros-jazzy-xacro`).

## How to run

```bash
ros2 launch multi_robot_sim.launch.py
```

In another terminal:

```bash
python3 fleet_coordinator.py
```

## Expected result

Two robots visible in the Gazebo window, spawned 1m apart. `robot1`
drives forward in a straight line; `robot2` spins in place — confirming
each responds only to its own command.

`fleet_coordinator.py` logs, once a second:

```
[INFO] [fleet_coordinator]: robot1: x=0.412, y=0.000
[INFO] [fleet_coordinator]: robot2: x=0.500, y=0.000
```

`robot1`'s `x` should increase steadily (driving forward); `robot2`'s
position should stay roughly fixed (turning in place, not translating) —
the two robots behaving independently and differently confirms
namespacing is working, not accidentally sharing state.

## Confirm topic namespacing

```bash
ros2 topic list | grep -E "robot1|robot2"
```

Expected: `/robot1/cmd_vel`, `/robot1/odom`, `/robot2/cmd_vel`,
`/robot2/odom` — four distinct, clearly-namespaced topics, not a shared
`/cmd_vel`.

## Confirm TF namespacing

```bash
ros2 run tf2_tools view_frames
```

Expected: `frames.pdf` shows two separate frame trees rooted at
`robot1/base_link` and `robot2/base_link` — not a single shared
`base_link` both robots would otherwise collide on (see DEEP_DIVE.md's
common pitfall — this is the check that would catch it if
`frame_prefix` had been forgotten).

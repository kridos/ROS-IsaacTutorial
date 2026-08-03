# Demo: Capstone — Autonomous Mobile Manipulator

## Prerequisites

Everything Chapters 7, 9, 11, and 12 needed (Gazebo, ros_gz_bridge,
xacro, Nav2, MoveIt2). Generate Chapter 11's map once first if you
haven't already:

```bash
python3 ../../../02-intermediate/11-nav2-basics/demo/generate_empty_map.py
```

Also set up the same planning-scene collision objects Chapter 18 used
(table + target_block), so the pick/place stages have something real to
interact with:

```bash
python3 ../../../03-advanced/18-advanced-moveit2-pick-place/demo/planning_scene_setup.py
```

(Run this *after* `capstone_sim.launch.py` is up and `move_group` is
running, same order Chapter 18 used.)

## How to run

```bash
ros2 launch capstone_sim.launch.py
```

Give AMCL an initial pose in RViz2 (Chapter 11's "2D Pose Estimate"
step) — same as every earlier Nav2 chapter.

Then, in another terminal:

```bash
python3 mission_coordinator.py
```

## Expected output

```
=== Mission start ===
[stow] Moving arm to 'home' configuration before any navigation
[navigate-to-pickup] Navigating to (1.5, 0.0)
[navigate-to-pickup] Navigation finished
[detect] Simulated detection: object at (0.35, 0.0, 0.28)
[pick] Picking up object at (0.35, 0.0, 0.28)
[pick] Attached target_block to gripper
[stow] Moving arm to 'home' configuration before any navigation
[navigate-to-dropoff] Navigating to (1.5, 1.0)
[navigate-to-dropoff] Navigation finished
[place] Placing object at (0.2, 0.25, 0.28)
[place] Detached target_block from gripper
[stow] Moving arm to 'home' configuration before any navigation
=== Mission complete ===
```

Watching the Gazebo and RViz2 windows through this run, you should see:
the arm tuck to its home position, the robot drive to the first
waypoint, the arm reach down and "pick up" the block (it moves with the
gripper through the retreat), the robot drive to the second waypoint
with the arm safely stowed the whole time, and the arm place the block
at the second location.

## Try it: remove the stow-before-navigate step

Comment out one of the `self._stow_arm()` calls in
`mission_coordinator.py` — the one before `_navigate_to(*DROPOFF_NAV_GOAL,
...)` — leaving the arm extended (holding the block) while the robot
navigates. Re-run. Expected: depending on your `nav2_params.yaml`
inflation settings (Chapter 11), you may see the robot's planned path
graze closer to obstacles than expected, or in a tighter space, Nav2
may report planning failures for gaps that would actually be blocked by
the extended arm — a direct, hands-on look at DEEP_DIVE.md's
footprint-mismatch pitfall, the culminating example of the "components
correct in isolation, integration needs explicit coordination" lesson
this curriculum has built toward since Chapter 19.

## What's next

You've now built and integrated every major system this curriculum
covers. Natural extensions from here: swap the simulated `_detect_object`
step for a real perception pipeline (Chapters 15/16/27), add a dynamic
footprint that adjusts with arm configuration instead of relying on the
stow-before-navigate rule, or take the whole mission into Isaac Sim
(Chapters 13/14) instead of Gazebo for higher-fidelity simulation.

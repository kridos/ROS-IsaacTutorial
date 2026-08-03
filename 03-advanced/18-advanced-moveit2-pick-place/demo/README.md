# Demo: Advanced MoveIt2 — Pick and Place

## Prerequisites

Same as Chapter 12. Start Chapter 12's launch file (this chapter reuses
that arm/move_group setup rather than duplicating it):

```bash
ros2 launch ../../../02-intermediate/12-moveit2-basics/demo/moveit_planning.launch.py
```

## Set up the scene

```bash
python3 planning_scene_setup.py
```

Expected: `Added 'table' and 'target_block' to the planning scene`. In
RViz2's MotionPlanning display (with "Scene Robot" / planning scene
visualization enabled), you should see a flat table box and a small
block appear in front of the arm.

## Run the pick-and-place sequence

```bash
python3 pick_and_place.py
```

## Expected output

```
[pre-grasp] Planning succeeded, executing...
[grasp approach] Cartesian path 100% complete, executing...
[grasp] Closing gripper (logical step — see comment above)
[grasp] Attached target_block to gripper
[post-grasp retreat] Cartesian path 100% complete, executing...
[pre-place] Planning succeeded, executing...
[place approach] Cartesian path 100% complete, executing...
[place] Opening gripper (logical step)
[place] Detached target_block from gripper
[post-place retreat] Cartesian path 100% complete, executing...
Pick-and-place sequence complete.
```

In RViz2, you should see the arm move down to the block, then (since
`target_block` is now attached) the block should visually move together
with the gripper through the retreat/transport/place motions, and remain
at the place location afterward, independent again.

## Try it: watch the attach/detach effect directly

```bash
ros2 topic echo /planning_scene --once
```

Run once right after the grasp step and again after the place step.
Expected: the first shows `target_block` under `robot_state.attached_collision_objects`
(attached to `gripper`); the second shows it back under `world.collision_objects`
(a free-standing object again) — a direct look at exactly what
attach/detach changes in MoveIt2's scene model.

## Try it: skip the attach step

Comment out the `apply_attached_collision_object` call in
`pick_and_place.py` and re-run. Expected: the post-grasp retreat still
"succeeds" (MoveIt2 doesn't know to object), but watch RViz2's scene —
the block stays behind at its original position while the gripper moves
away, visually demonstrating DEEP_DIVE.md's common pitfall.

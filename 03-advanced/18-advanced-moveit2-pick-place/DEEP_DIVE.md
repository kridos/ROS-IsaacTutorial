# Chapter 18 Deep Dive: Advanced MoveIt2 — Pick-and-Place

## The Planning Scene Interface

Chapter 12's DEEP_DIVE.md mentioned the planning scene (MoveIt2's model
of "what does the world look like") without using it. This chapter does:
the **Planning Scene Interface** lets you add/remove **collision
objects** — simple geometric obstacles (boxes, cylinders, meshes) with a
name and a pose — that every subsequent planning call must avoid. This
chapter's demo adds a table (a box) and a target block (a smaller box) to
the scene before planning anything, so the planner treats them as real
obstacles from the start rather than the empty-scene assumption Chapter
12's demo made.

## Cartesian path planning

Chapter 12's `set_pose_target()` + `plan()` produces *some* valid
collision-free path to a target pose — the sampling-based planner (OMPL)
doesn't guarantee, or even try for, a straight line. For most moves
that's fine or even desirable (a curved path can avoid obstacles a
straight line wouldn't). But the final approach to a grasp, and the
initial retreat after grasping, specifically benefit from a controlled,
predictable straight-line motion — approaching an object from an
unexpected curved angle risks knocking it over before the gripper even
closes.

**`compute_cartesian_path()`** solves this differently: instead of
sampling toward a single target pose, you give it a list of waypoints,
and it computes a path that moves the end-effector through them in a
straight line between each consecutive pair, returning both the
trajectory and a fraction (0.0-1.0) indicating how much of the requested
path it actually managed to compute without hitting a problem (joint
limits, collision) — worth checking that fraction is close to 1.0 before
trusting the result, rather than assuming success just because the call
returned.

## Attaching and detaching objects

Once the gripper closes around the target block, that block should be
treated as part of the arm for collision-checking purposes during the
retreat and transport motion — otherwise the planner, still thinking the
block is a separate stationary obstacle sitting where it was originally
picked up, would either plan an unnecessarily awkward path around it
(not knowing it's actually moving with the gripper) or, worse, not
realize the now-moving block could collide with something else in the
scene during transport.

**`attach_object(object_name, link_name)`** tells the planning scene "this
collision object now moves rigidly with this link" (typically the
gripper link) — subsequent planning treats it accordingly.
**`detach_object(object_name)`** reverses this at the place location,
returning the object to being an independent, stationary collision object
at wherever it was released.

## The full pick-and-place sequence

1. Move to a **pre-grasp pose** (above/near the object, free-form plan —
   Chapter 12's approach is fine here, no straight-line requirement yet).
2. **Cartesian approach**: straight-line move down to the actual grasp
   pose.
3. Close the gripper (in this chapter's simplified demo, without real
   finger joints per Chapter 12's simplification, this is represented as
   a logical step rather than an actuated one — noted explicitly in the
   demo).
4. **Attach** the object to the gripper link.
5. **Cartesian retreat**: straight-line move back up/away from the grasp
   pose.
6. Move to a **pre-place pose** near the destination (free-form plan).
7. **Cartesian approach** down to the place pose.
8. Open the gripper, **detach** the object.
9. **Cartesian retreat** away from the place pose.

## Common pitfall

Forgetting to call `attach_object()` before planning the retreat/transport
motion is the single most consequential mistake in this sequence — the
planner will plan as if the gripper is empty, and while the plan will
often *look* fine in simulation (nothing in MoveIt2's model actually
represents the true, now-moving block), it can produce a trajectory that
would genuinely collide the real, physically-attached block with
something in the scene, since MoveIt2's collision checking was never told
to account for it moving too. Always attach before any motion is planned
with the object in hand, not just before executing.

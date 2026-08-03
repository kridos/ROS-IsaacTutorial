# Chapter 28 Deep Dive: Capstone — Autonomous Mobile Manipulator

## Mobile manipulation architecture

Combining Chapter 7's diff-drive chassis with Chapter 12's arm means the
arm's `base_link` (the root of its own kinematic chain, per Chapter 5's
tree structure) becomes a **fixed-joint child of the mobile chassis**,
not a separately-rooted frame fixed to the world. This is a direct,
concrete consequence of TF's tree structure from Chapter 8: as the
chassis navigates and its `odom -> base_link` transform changes (Chapter
7's diff-drive plugin publishing this, same as every mobile-robot
chapter since), the *entire arm subtree* moves along with it
automatically, because TF composes transforms down the tree — nothing
about the arm's own joints needs to know or care that its root is now
moving through the world, exactly the same "TF2 composes automatically"
property Chapter 8's demo first demonstrated on a toy orbiting frame,
now doing real work.

## Running Nav2 and MoveIt2 simultaneously

Chapter 11 and Chapter 12 each configured their own stack (costmaps;
planning scene) assuming they were the only thing reasoning about the
robot's space. Running both at once on one robot surfaces a genuine
integration requirement neither chapter needed alone: **the arm's
current configuration affects the robot's effective footprint for
navigation purposes**. An arm extended forward changes what counts as
"the robot" for Nav2's obstacle-avoidance costmap (Chapter 11's
`robot_radius`/`footprint` parameters) — a fixed circular footprint
sized for the stowed arm doesn't account for an extended arm potentially
clipping something Nav2's planner didn't know to route around. Real
mobile manipulator systems handle this either by using a dynamic
footprint that changes with arm configuration, or — the simpler approach
this chapter's demo takes — by enforcing a rule: **the arm is stowed to
a known-safe, tucked configuration before any navigation action begins**,
so the fixed footprint used for navigation stays valid.

## The mission coordinator pattern

A single top-level node sequences the mission's stages, each stage
itself built from patterns earlier chapters already established:

1. **Stow the arm** (MoveIt2 `set_goal_state` to a named "home"
   configuration, Chapter 12's SRDF group-state pattern).
2. **Navigate to the pickup location** (Nav2's `NavigateToPose` action,
   Chapter 11's pattern).
3. **Detect and localize the target object** — in this capstone,
   simplified to a hardcoded/simulated "object is at this known pose"
   step rather than running a real perception pipeline; Chapters
   15/16/27 are where genuine object detection belongs, and re-deriving
   that here would shift this chapter's focus away from integration,
   which is its actual point.
4. **Pick up the object** (Chapter 18's full pick sequence: pre-grasp,
   Cartesian approach, attach, Cartesian retreat).
5. **Stow the arm again** before navigating.
6. **Navigate to the drop-off location** (Nav2 again).
7. **Place the object** (Chapter 18's place sequence).

This sequencing is itself a simple state machine/behavior-tree-like
structure — the same compositional idea Chapter 17 covered for Nav2's
*internal* navigation logic, now applied one level up, at the whole
*mission's* level, coordinating across systems (Nav2, MoveIt2) rather
than within just one of them.

## Common pitfall: skipping the stow-before-navigate step

Forgetting to stow the arm before triggering navigation is this
capstone's culminating version of a lesson that's been building since
Chapter 19's multi-robot namespacing and Chapter 21/22's container/
cluster networking pitfalls: **a component that works correctly in
isolation can still break once integrated, because integration
introduces coordination requirements neither component alone needed to
satisfy.** Nav2 in isolation (Chapter 11) has no bug — it correctly
avoids obstacles within the footprint it's configured with. MoveIt2 in
isolation (Chapter 12/18) has no bug either — it correctly plans arm
motions within its own planning scene. The failure mode only exists at
the *seam* between them: Nav2's costmap footprint and MoveIt2's actual
arm configuration silently disagreeing about what "the robot" currently
occupies in space, unless something (this chapter's mission coordinator,
explicitly) enforces that they stay consistent.

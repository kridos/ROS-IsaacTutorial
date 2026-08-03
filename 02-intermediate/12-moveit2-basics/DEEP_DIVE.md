# Chapter 12 Deep Dive: MoveIt2 Basics

## Architecture

- **move_group** — the central coordinator node. Everything (planning
  requests, execution, scene updates) goes through it; you don't talk to
  individual planners or controllers directly.
- **Planning scene** — MoveIt2's internal model of "what does the world
  look like right now": the arm's current joint state plus any known
  obstacles (added via the Planning Scene Interface, not used in this
  chapter's simple demo but essential once you're planning around real
  objects).
- **Motion planning plugin** — the actual algorithm that searches for a
  valid trajectory. This chapter uses **OMPL** (Open Motion Planning
  Library), MoveIt2's default — a family of sampling-based planners that
  build up a tree/graph of randomly-sampled valid configurations until
  they find a path from start to goal, rather than solving the geometry
  in closed form. Sampling-based planning is why planning isn't
  instantaneous and isn't perfectly deterministic between runs (retrying
  a failed plan can succeed since a different set of samples gets
  attempted).

## Forward vs. inverse kinematics

- **Forward kinematics (FK)**: given every joint's current angle, where
  is the end-effector? Straightforward — walk the kinematic chain
  (exactly the URDF joint chain from Chapter 5) applying each joint's
  transform in sequence.
- **Inverse kinematics (IK)**: given a *desired* end-effector pose, what
  joint angles achieve it? Much harder — often multiple valid solutions
  exist (an arm can frequently reach the same point with its elbow up or
  down), or none exist (the pose is out of reach or would require
  self-collision). This chapter's demo specifies a target *pose*, not
  target joint angles, so MoveIt2 solves IK internally (via a configured
  IK plugin — commonly KDL for a simple arm like this chapter's) before
  planning ever starts.

## SRDF: planning groups and named states

The **SRDF** (Semantic Robot Description Format) is a companion file to
the URDF, adding information the URDF alone doesn't have: which joints
count as one **planning group** (e.g. "arm" = joint1, joint2, joint3, as
one unit MoveIt2 plans over together), which links can safely be
excluded from self-collision checking (adjacent links that always
overlap slightly at their joint aren't a real collision), and named
**group states** (e.g. a "home" configuration you can request by name
instead of specifying every joint angle). This chapter's demo includes a
minimal SRDF defining one planning group ("arm") covering the three arm
joints.

## The MoveGroupInterface

The Python client API (`moveit_py`'s `MoveGroupInterface` in recent
MoveIt2 versions — check DEEP_DIVE.md's exact import against your
installed MoveIt2 version, as this API changed from the older
`moveit_commander` package) is how your own code requests plans and
execution:

```python
arm = MoveGroupInterface("arm", ...)
arm.set_pose_target(target_pose)
success = arm.go(wait=True)
```

Underneath, this is built on the same request/track-to-completion shape
you've now seen twice — Chapter 3's actions, Chapter 11's
`NavigateToPose` — MoveIt2's `move_group` exposes a `MoveGroup` action
that `MoveGroupInterface` wraps for you, so you don't write action-client
boilerplate by hand for the common case.

## Common pitfall: unreachable or in-collision targets fail without one obvious cause

A `set_pose_target()` + `go()` call returning failure can mean several
different things: the pose is outside the arm's physical reach (no IK
solution exists), the pose is reachable but every IK solution collides
with the arm itself or a known obstacle, or the sampling-based planner
simply didn't find a valid path within its allotted time/sample budget
(worth just retrying once before concluding the target is actually
infeasible). RViz2's **MotionPlanning** display is the standard way to
tell these apart — it visually shows the start and (attempted) goal
state, colored red where the goal state itself is in collision, which
narrows down "unreachable/colliding target" vs. "planner didn't find it
in time" far faster than guessing from the failure alone.

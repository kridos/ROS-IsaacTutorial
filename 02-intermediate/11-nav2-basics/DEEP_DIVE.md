# Chapter 11 Deep Dive: Nav2 Basics

## The pieces, and how they fit together

Nav2 is a set of cooperating nodes, each solving one part of "get to this
goal safely":

- **map_server** — loads a pre-built occupancy grid map (a 2D image
  where each pixel means "free," "occupied," or "unknown") and serves it
  on the `/map` topic with transient-local durability (Chapter 10) so any
  node that starts later still gets it.
- **AMCL** (Adaptive Monte Carlo Localization) — estimates the robot's
  pose *on* that map by comparing live lidar scans (Chapter 9) against
  what the map predicts should be seen from candidate poses, using a
  particle filter (many guessed poses, weighted by how well they match
  sensor data, resampled over time toward the best matches).
- **Costmap** (local and global) — a 2D grid derived from the map plus
  live sensor data, marking obstacles and "inflating" them outward by
  roughly the robot's radius, so the planner naturally avoids paths that
  would clip an obstacle rather than needing separate collision checks
  layered on top.
- **Global planner** (e.g. NavFn or Smac Planner) — plans a path across
  the *global* costmap from current pose to goal pose, ignoring
  short-term dynamics.
- **Local controller** (e.g. DWB or MPPI) — follows that global path
  while reacting to the *local* costmap in real time (newly-seen
  obstacles the global plan didn't know about), producing actual
  `/cmd_vel` commands.
- **Behavior tree** (via `bt_navigator`) — sequences all of the above
  into the `NavigateToPose` action: get a plan, follow it, recover if
  stuck, retry, and so on — this is the same goal/feedback/result action
  pattern from Chapter 3, now driving something real.

## Lifecycle-managed nodes

Most Nav2 nodes are **lifecycle nodes** — they don't just start running
the instant the process launches. They start `unconfigured`, then a
`lifecycle_manager` node transitions them through `configuring` →
`inactive` → `activating` → `active` in a coordinated order. This exists
because Nav2 has many interdependent nodes (AMCL needs the map to
already exist; the planner needs AMCL's pose) — lifecycle management is
how Nav2 guarantees things start up in the right order instead of racing
each other. `ros2 lifecycle get /amcl` shows a node's current state if
something seems stuck at startup.

## AMCL needs an initial pose

A freshly-started AMCL has no idea where the robot is on the map — its
particle filter needs an **initial pose estimate** before it can
converge. This is normally provided by clicking "2D Pose Estimate" in
RViz2 (which publishes to `/initialpose`), or programmatically by
publishing a `PoseWithCovarianceStamped` to that topic. Without it, AMCL
either doesn't localize at all or (if configured with a very broad
initial spread) takes much longer to converge than necessary — "the
robot on the map doesn't match reality" immediately after launch is
almost always a missing initial pose, not a broken AMCL.

## Common pitfall: costmap inflation misconfiguration

The costmap's `robot_radius` (or a full `footprint` polygon for
non-circular robots) and `inflation_radius` together determine how much
buffer space the planner keeps around obstacles. Too small a
`robot_radius` relative to the *actual* robot lets planned paths clip
real obstacles (the planner thinks it fits somewhere it doesn't); too
large an `inflation_radius` makes the costmap treat narrow-but-passable
corridors as fully blocked, and Nav2 will report planning failures for
paths that should exist. This is the single most common Nav2 tuning
mistake for a new robot — always double check these two numbers against
the robot's real dimensions first when navigation behaves oddly.

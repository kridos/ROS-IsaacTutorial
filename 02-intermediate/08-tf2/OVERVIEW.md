# Chapter 8: TF2 — Transforms & Coordinate Frames

## What this is

**TF2** is ROS2's system for tracking where things are relative to each
other, over time, as a live tree of named **frames** (like `base_link`,
`camera_link`, `map`). Instead of every node doing its own geometry math
to figure out "where is the camera relative to the base," TF2 maintains
the whole tree centrally and lets any node ask "where is frame A relative
to frame B" and get an answer, even if A and B aren't directly connected.

## Why it matters

You already produced TF data without necessarily noticing — Chapter 5's
`robot_state_publisher` was publishing transforms the whole time.
Everything spatial from here on (sensor fusion, navigation, manipulation)
is built on querying this tree rather than hardcoding offsets, because a
robot's frames move (wheels turn, arms articulate, the whole robot drives
around) and hardcoded math would need updating everywhere, constantly.

## Where this fits

Directly follows up on Chapter 5's URDF/robot_state_publisher work
(which produces TF) and Chapter 7's Gazebo simulation (whose diff-drive
plugin also publishes `odom -> base_link` TF). This chapter finally
opens up what TF actually is and how to use it in your own nodes, rather
than just letting `robot_state_publisher` and RViz2 handle it invisibly.

## What the demo shows

Two frames published independently — a static one and one that rotates
over time — plus a third node that looks up the transform between them
even though neither is the other's direct parent, demonstrating TF2
composing a path across the tree automatically.

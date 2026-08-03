# Chapter 14: ROS2 <-> Isaac Sim Bridge

## What this is

Isaac Sim's **ROS2 Bridge** extension publishes and subscribes ROS2
topics from inside a running Isaac Sim scene — the same role Chapter 7's
`ros_gz_bridge` played for Gazebo, letting you drive a simulated robot
with `/cmd_vel` and read `/odom` back, just implemented differently
under the hood (Chapter 13 gave you the vocabulary — extensions, the
Python API — this chapter uses both to wire ROS2 into the picture).

## Why it matters

This closes the loop: everything you've built ROS2-side since Chapter 2
(nodes, topics, the tools in Chapter 6) now works against Isaac Sim
exactly as it did against Gazebo. From here on, which simulator is
running underneath is a choice based on what you need (speed and
simplicity vs. rendering fidelity and scale), not a reason to relearn
your ROS2 workflow.

## Where this fits

Directly parallels Chapter 7's Gazebo demo — same robot, same
`/cmd_vel`-in `/odom`-out shape — deliberately, so you can compare the
two simulators doing the identical task side by side.

## What the demo shows

The Chapter 13 robot, now wired via OmniGraph to accept `/cmd_vel` and
publish `/odom`, driven by a plain ROS2 node (no Isaac Sim imports at
all) exactly the way you drove the Gazebo robot in Chapter 7.

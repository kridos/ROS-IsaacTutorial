# Chapter 11: Nav2 Basics

## What this is

**Nav2** is ROS2's standard navigation stack: given a map and a goal
pose, it drives a robot there while localizing itself and avoiding
obstacles along the way. It's not one program — it's a coordinated set
of ROS2 nodes (localization, path planning, obstacle avoidance) that
together answer "how do I get from here to there safely."

## Why it matters

Autonomous navigation is one of the most common real robotics tasks, and
Nav2 is what almost everyone actually uses for it rather than writing
their own from scratch — it's mature, configurable, and handles a huge
number of edge cases (dynamic obstacles, replanning, recovery behaviors)
that are easy to underestimate if you haven't built a navigation stack
before.

## Where this fits

Uses everything so far: Chapter 3's action pattern (navigation goals are
actions), Chapter 8's TF2 (localization output is a transform), Chapter 9's
simulated lidar (what AMCL and the costmap use to sense the world), and
Chapter 10's QoS conventions (map data uses transient-local durability).
This is the first chapter where all of Tier 1 and the earlier parts of
Tier 2 visibly come together into one working system.

## What the demo shows

The Chapter 9 sensored robot, in Gazebo, running the full Nav2 stack
with a small pre-built map. You'll send it a navigation goal (both from
RViz2's GUI and programmatically) and watch it plan a path and drive
there while avoiding obstacles.

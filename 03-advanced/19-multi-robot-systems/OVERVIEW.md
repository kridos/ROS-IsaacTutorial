# Chapter 19: Multi-Robot Systems

## What this is

Everything so far has been one robot. This chapter covers what changes
with more than one: **namespacing** so multiple robots' identical topic
names (`/cmd_vel`, `/odom`, `/tf`) don't collide, and basic
**coordination** so a fleet of robots can be given different tasks from
one place.

## Why it matters

Real deployments are frequently fleets, not single robots — warehouse
robots, delivery robots, swarms. Getting namespacing right is what makes
"one robot's code, running N times" actually work as N independent
robots instead of N robots fighting over the same topics.

## Where this fits

Directly extends Chapter 7's diff-drive robot (spawned twice, under two
namespaces) and revisits Chapter 2's topic-naming rules, which the
leading-slash-vs-relative distinction from that chapter now genuinely
matters for.

## What the demo shows

Two Chapter 7 robots spawned into the same Gazebo world under separate
namespaces (`robot1`, `robot2`), each independently controllable, plus a
coordinator node that sends each robot a different velocity command and
logs both robots' odometry side by side to confirm they don't cross-talk.

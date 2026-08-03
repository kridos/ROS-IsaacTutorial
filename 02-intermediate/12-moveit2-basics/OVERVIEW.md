# Chapter 12: MoveIt2 Basics

## What this is

**MoveIt2** is the standard ROS2 motion-planning framework for arms and
manipulators: given a target position for the end of an arm (or a target
joint configuration), it computes a safe, collision-free trajectory to
get there and can execute it.

## Why it matters

Manipulation — picking things up, placing them, opening doors — needs
motion planning that accounts for the arm's joint limits, self-collision,
and any known obstacles. Like Nav2 for navigation, MoveIt2 is what nearly
everyone actually uses for this rather than solving inverse kinematics
and collision checking from scratch.

## Where this fits

Extends Chapter 5's URDF arm with a third joint and a gripper, and reuses
the same action-based execution model Nav2 (Chapter 11) uses underneath
— once you've seen Nav2 send a goal and track feedback to completion,
MoveIt2's execution model will look very familiar even though the domain
(arm joints vs. robot base) is completely different.

## What the demo shows

A 3-joint arm with a simple gripper, running MoveIt2's `move_group` node.
You'll request a plan to a target end-effector pose and execute it,
watching the arm move in RViz2's MotionPlanning display.

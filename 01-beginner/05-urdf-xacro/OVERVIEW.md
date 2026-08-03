# Chapter 5: Robot Description (URDF/Xacro)

## What this is

**URDF** (Unified Robot Description Format) is an XML format describing
a robot's physical structure: its rigid parts (**links**) and how they're
connected and allowed to move relative to each other (**joints**).
**Xacro** is a macro language layered on top of URDF so you can use
variables, math, and reusable macros instead of hand-writing (and
copy-pasting) raw XML numbers.

## Why it matters

Everything spatial in ROS2 depends on this description existing: knowing
where a robot's camera is relative to its base, visualizing the robot in
RViz2, simulating it in Gazebo, planning arm motions in MoveIt2 — all of
it needs an accurate URDF. This is the one chapter where getting the
model right pays off in almost every later chapter.

## Where this fits

Standalone conceptually, but the `robot_state_publisher` node introduced
here is what turns joint positions into the coordinate-frame tree covered
properly in Chapter 8 (TF2) — this chapter builds the object TF2 operates
on.

## What the demo shows

A simple 2-joint robot arm (base → link1 → link2), written in Xacro,
visualized live in RViz2 with slider controls (`joint_state_publisher_gui`)
so you can move the joints and watch the arm move.

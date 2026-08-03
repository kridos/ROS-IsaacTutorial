# Chapter 6: Debugging & Visualization Tools

## What this is

Three tools you'll reach for constantly once a system has more than one
or two nodes: **RViz2** (3D visualization — you've already used it in
Chapter 5), **rqt** (a collection of introspection GUIs — graph viewer,
log filter, live plotter), and **ros2 bag** (record topic data to disk
and replay it later, exactly as it happened).

## Why it matters

When something's wrong on a real robot, "add a print statement and
re-run" often isn't practical — the bug might only show up after 20
minutes of driving around, or only on hardware you don't have in front of
you right now. These tools let you see what a running system is actually
doing (not what you assume it's doing), and capture problematic runs so
you can replay and debug them offline, repeatedly, without needing the
robot or simulator running again.

## Where this fits

Uses only what you already have from Chapters 2-4 (nodes, topics,
parameters) — no new ROS2 concepts, just the tools professionals actually
use to look inside a running system. You'll reach for these constantly
starting Chapter 7 onward.

## What the demo shows

A node publishing noisy sensor-like data, which you'll inspect with
`rqt_graph` (see the node/topic connections), `rqt_plot` (watch the value
live), and `ros2 bag` (record a run, then replay it and confirm the
replayed data matches what was recorded).

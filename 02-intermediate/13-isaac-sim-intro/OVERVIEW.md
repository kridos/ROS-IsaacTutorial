# Chapter 13: Isaac Sim Intro — Omniverse, USD, Importing a Robot

## What this is

**Isaac Sim** is NVIDIA's GPU-accelerated robotics simulator, built on
**Omniverse** (NVIDIA's platform for real-time 3D collaboration and
simulation, originally built for visual effects and design workflows).
Where Gazebo (Chapters 7 and 9) prioritizes speed and simplicity, Isaac
Sim prioritizes photorealistic rendering and physical accuracy, at the
cost of needing a more capable GPU.

## Why it matters

This is the entry point to everything NVIDIA-specific in the rest of the
curriculum: Isaac ROS (Chapter 15), synthetic data generation (Chapter
16), Isaac Lab reinforcement learning (Chapter 22+), and Isaac GR00T
(Chapter 25) are all built on Isaac Sim. Getting comfortable with what
it is and how it differs from Gazebo — same underlying concepts, a
different, more powerful tool — is what makes those later chapters
approachable instead of a completely fresh start.

## Where this fits

You already know URDF (Chapter 5) and what a robot description needs to
contain. This chapter is about getting that same description *into* a
different simulator, and understanding the new vocabulary (USD, stage,
prim, extension) that comes with it — not re-learning robot description
from scratch.

## What the demo shows

A script that starts Isaac Sim headlessly, imports the Chapter 7
diff-drive robot's URDF via the URDF Importer extension, spawns it into
an empty stage, and steps physics for a few seconds — printing the
robot's pose each step to confirm the import and physics are both
working, without needing the full GUI.

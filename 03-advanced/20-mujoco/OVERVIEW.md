# Chapter 20: MuJoCo

## What this is

**MuJoCo** is a fast, accurate physics engine originally built for
robotics and biomechanics research, now open-source and widely used as
the physics backend for reinforcement learning research. Unlike Gazebo
and Isaac Sim, it isn't ROS2-native — it's a physics library you drive
directly from Python (or C++), without a built-in ROS2 bridge.

## Why it matters

MuJoCo's speed is what makes it valuable: it can simulate physics fast
enough to run thousands of parallel environments for RL policy training,
which is a fundamentally different use case than "simulate one robot for
a human to watch." Understanding this now sets up Chapter 22's Isaac Lab
smoothly — a different, GPU-parallelized engine (PhysX) solving the same
underlying "simulation needs to be fast enough to train on" problem.

## Where this fits

A deliberate change of pace from Gazebo/Isaac Sim's node-and-topic
programming model — MuJoCo's lower-level, call-a-function-yourself style
is worth experiencing directly rather than only reading about, since
Isaac Lab (Chapter 22+) uses a similarly direct style.

## What the demo shows

A simple arm, described in MuJoCo's own MJCF format, loaded and stepped
through physics directly via the `mujoco` Python package's `mj_step()` —
no ROS2 involved at all, applying a simple oscillating joint torque and
printing joint positions each step.

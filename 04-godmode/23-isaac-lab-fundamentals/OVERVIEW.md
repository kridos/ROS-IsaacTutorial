# Chapter 23: Isaac Lab Fundamentals — RL Environments

## What this is

**Isaac Lab** is NVIDIA's reinforcement learning framework, built on
Isaac Sim and PhysX — its defining feature is running thousands of
simulated environment instances in parallel on a single GPU, rather than
one simulation at a time.

## Why it matters

Chapter 20 introduced MuJoCo partly because RL training needs a lot of
simulated experience — often millions of steps — to learn anything.
MuJoCo gets there through raw CPU speed and running many instances in
parallel processes; Isaac Lab solves the same problem differently:
GPU-parallelizing the physics simulation itself, so one GPU simulates
thousands of environments in lockstep in a single call.

## Where this fits

Builds on Chapter 13/14's Isaac Sim fundamentals (stage, prims, the
Python API) and revisits Chapter 20's "why fast simulation matters for
RL" framing with NVIDIA's own answer to that problem.

## What the demo shows

Isaac Lab's built-in CartPole task — a standard RL benchmark — run with
a small number of parallel environments and random actions, printing the
shapes and sample values of the batched observation/reward tensors each
step, to make the "many environments at once, as one batched tensor"
mental model concrete.

# ROS2 + NVIDIA Isaac Robotics Curriculum

A hands-on curriculum for going from "comfortable programmer, robotics
novice" to research/industry-ready in ROS2, Gazebo, NVIDIA Isaac
(Sim/ROS/Lab/GR00T), Nav2, MoveIt2, and MuJoCo.

## Who this is for

You can already write code (Python and/or C++), but robotics, simulators,
and ROS2 concepts are new. Every chapter explains ideas from scratch,
in plain language, before showing the code.

## Prerequisites

- Linux (Ubuntu 22.04 or 24.04) with an NVIDIA GPU. This is required from
  Tier 2 onward (Isaac Sim needs a CUDA-capable GPU); Tier 1 (ROS2 +
  Gazebo) works on CPU-only Ubuntu too, but the curriculum as a whole
  assumes the GPU is there.
- No prior ROS/robotics experience assumed. Chapter 1 walks through
  installing everything.

## How to use this repo

Work through the tiers in order. Within a tier, work through the chapters
in order — later chapters build on earlier ones. Each chapter lives in its
own directory and contains:

- `OVERVIEW.md` — the gist: what it is, why it matters, in ~5-10 minutes.
- `DEEP_DIVE.md` — the full technical detail, still explained simply.
- `demo/` — runnable, heavily-commented code demonstrating the concept,
  with a `demo/README.md` explaining how to run it and what to expect.

## Curriculum map

### [Tier 1 — Beginner](01-beginner/README.md) — complete
ROS2 fundamentals: nodes, topics, services, actions, parameters, launch
files, robot description, debugging tools, and your first Gazebo
simulation.

### Tier 2 — Intermediate (in progress)
Transforms, simulated sensors, ROS2 architecture (DDS/QoS), Nav2 and
MoveIt2 basics, and your first steps into NVIDIA Isaac Sim.

### Tier 3 — Advanced (in progress)
Isaac ROS GPU perception, synthetic data generation, advanced Nav2/MoveIt2,
multi-robot systems, MuJoCo, containerized robotics (Docker), and
orchestrating robot fleets with Kubernetes.

### Tier 4 — God Mode (in progress)
Isaac Lab reinforcement learning, sim-to-real transfer, Isaac GR00T
foundation models, GPU-accelerated custom perception, and a capstone
project tying it all together.

## Design notes

See `docs/superpowers/specs/2026-08-02-ros2-isaac-curriculum-design.md`
for the full design rationale (structure, language policy, chapter list).

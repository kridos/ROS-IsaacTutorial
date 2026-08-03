# ROS2 / NVIDIA Isaac Robotics Curriculum — Design

## Purpose

A self-contained, project-based curriculum taking someone comfortable with
general programming but new to robotics from zero to research/industry-ready
competence in ROS2, Gazebo, NVIDIA Isaac Sim/ROS/Lab/GR00T, MoveIt2, Nav2,
and MuJoCo. The reader will follow it solo, so every chapter must be legible
without an instructor.

## Audience & Assumptions

- Comfortable programmer (Python and/or C++), robotics/simulation novice.
- Runs Linux with an NVIDIA GPU (native Ubuntu + CUDA support assumed —
  this is required for Isaac Sim/ROS/Lab; alternatives are not covered).
- Wants both conceptual understanding (for research) and hands-on fluency
  (for industry work).

## Structure

```
<tier>/<chapter>-<topic-slug>/
  OVERVIEW.md      # the gist: what this is, why it matters, plain language
  DEEP_DIVE.md      # full technical detail, still explained in simple terms
  demo/              # runnable, heavily-commented demo code for this topic
```

Tiers are top-level directories, numerically prefixed:

- `01-beginner/`
- `02-intermediate/`
- `03-advanced/`
- `04-godmode/`

Chapters are numbered continuously across the whole curriculum (01–27), not
reset per tier, so ordering is unambiguous when browsing.

Each `OVERVIEW.md` is short (5–10 min read): what the topic is, why it
matters, where it fits relative to neighboring chapters, and what the demo
will show. Each `DEEP_DIVE.md` goes through the real technical mechanics —
architecture, data flow, key APIs/config, common pitfalls — in plain
language, aimed at someone who has never seen the topic before but wants to
actually understand it, not just copy code.

Each `demo/` is runnable in isolation (given the prerequisite software from
that chapter's setup instructions), with comments explaining *why* each
non-obvious line exists, not just what it does. Demos favor the smallest
example that clearly shows the concept working, with a note on how to verify
it worked (expected output, what to see in RViz/Isaac Sim, etc).

## Language Policy

Python is the default for all demos (matches Isaac Sim scripting, Nav2,
MoveIt2, and RL tooling, and is more approachable for a newcomer). C++ demos
are added alongside Python specifically for:

- Chapter 2 (ROS2 core: nodes/pub-sub) — C++ is the real-world default for
  performance-critical ROS2 nodes and the reader needs to recognize both.
- Chapter 3 (Services & Actions) — same reasoning.
- Chapter 15 (Isaac ROS perception nodes) — production perception pipelines
  are predominantly C++/NITROS.
- Chapter 26 (GPU perception w/ TensorRT) — same reasoning.

All other chapters are Python-only; DEEP_DIVE.md notes where the underlying
tool differs in C++ without a full parallel demo.

## Full Chapter List

**01-beginner**
1. Dev environment (Ubuntu, ROS2 install, workspaces, colcon)
2. ROS2 core concepts (nodes, topics, publish/subscribe) — Python + C++
3. Services & Actions — Python + C++
4. Parameters & Launch files
5. Robot description (URDF/Xacro)
6. Debugging & visualization tools (RViz2, rqt, ros2 bag)
7. Gazebo basics (spawn a robot, basic physics sim)

**02-intermediate**
8. TF2 (transforms & coordinate frames)
9. Simulated sensors (camera, lidar, IMU in Gazebo)
10. ROS2 architecture deep dive (DDS, QoS, middleware)
11. Nav2 basics (mapping, localization, path planning)
12. MoveIt2 basics (arm motion planning)
13. Isaac Sim intro (Omniverse, USD, importing a robot)
14. ROS2 ↔ Isaac Sim bridge

**03-advanced**
15. Isaac ROS (GPU-accelerated perception, NITROS, VSLAM) — Python + C++
16. Synthetic data generation (Isaac Sim Replicator)
17. Advanced Nav2 (custom planners, behavior trees)
18. Advanced MoveIt2 (pick-and-place pipelines)
19. Multi-robot systems
20. MuJoCo (fast physics/RL-style sim, compared to Gazebo/Isaac)
21. Containerized robotics (Docker for reproducible dev/deploy)

**04-godmode**
22. Isaac Lab fundamentals (RL environments for robots)
23. Training a locomotion/manipulation policy in Isaac Lab
24. Sim-to-real transfer techniques
25. Isaac GR00T foundation models
26. GPU-accelerated custom perception (TensorRT pipelines) — Python + C++
27. Capstone: autonomous mobile manipulator (integrates nav, manipulation,
    perception, and sim built up across all prior chapters)

## Root-Level Files

- `README.md` — curriculum map, prerequisites, how to use the repo, links
  into each tier.
- Each tier directory gets its own short `README.md` index listing its
  chapters and what the reader should know before starting the tier.

## Build Order & Delivery

Given the size (27 chapters × up to 2 markdown files + demo code each),
content is built and committed tier-by-tier: 01-beginner first end-to-end,
then 02-intermediate, then 03-advanced, then 04-godmode. Each chapter is
committed as it's completed so partial progress is always usable.

## Out of Scope (for this spec)

- Non-Linux / non-GPU setup paths.
- Full production deployment/fleet-management topics (beyond a single
  Docker chapter).
- Any simulator/tool not listed above (e.g. Unity Robotics, PX4/ArduPilot)
  — can be added as a later addendum if wanted.

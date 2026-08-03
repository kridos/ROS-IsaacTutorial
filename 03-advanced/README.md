# Tier 3 — Advanced

Goal: GPU-accelerated perception, synthetic training data, tuning Nav2
and MoveIt2 beyond their defaults, coordinating more than one robot, a
second physics engine built for RL, and the infrastructure (Docker,
Kubernetes) real deployments run on.

Assumes Tier 2 complete. Chapters 15-16 additionally need Isaac
ROS/Isaac Sim on an NVIDIA GPU (Chapter 15 also needs the Isaac ROS dev
container — see its DEEP_DIVE.md). Chapters 21-22 need Docker, and
Chapter 22 additionally needs a local Kubernetes tool (`kind` or
`minikube`). Chapters 17-20 only need what Tier 1/2 already set up.

## Chapters

15. [Isaac ROS](15-isaac-ros-perception/OVERVIEW.md) — GPU perception,
    NITROS, Visual SLAM.
16. [Synthetic data generation](16-synthetic-data-replicator/OVERVIEW.md)
    — Isaac Sim Replicator.
17. [Advanced Nav2](17-advanced-nav2/OVERVIEW.md) — custom behavior
    trees.
18. [Advanced MoveIt2](18-advanced-moveit2-pick-place/OVERVIEW.md) —
    pick-and-place pipelines.
19. [Multi-robot systems](19-multi-robot-systems/OVERVIEW.md) —
    namespacing and fleet coordination.
20. [MuJoCo](20-mujoco/OVERVIEW.md) — a second physics engine, built for
    RL-scale simulation.
21. [Containerized robotics](21-containerized-robotics-docker/OVERVIEW.md)
    — Docker.
22. [Kubernetes robot fleets](22-kubernetes-robot-fleets/OVERVIEW.md) —
    orchestrating containers across a cluster.

Start with Chapter 15 if you've just finished Tier 2.

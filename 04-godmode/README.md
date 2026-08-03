# Tier 4 — God Mode

Goal: reinforcement learning at scale (Isaac Lab), closing the gap
between simulation and reality, NVIDIA's foundation-model approach to
robot control (GR00T), hand-building GPU-optimized perception, and a
capstone integrating navigation, manipulation, perception, and
simulation from across the entire curriculum.

Assumes Tier 3 complete. Chapters 23-26 need Isaac Sim/Isaac Lab/GR00T
on an NVIDIA GPU with substantial VRAM. Chapter 27 needs TensorRT.
Chapter 28's capstone only needs what Tiers 1-3 already set up
(Gazebo, Nav2, MoveIt2) — no new GPU-specific install beyond those.

## Chapters

23. [Isaac Lab fundamentals](23-isaac-lab-fundamentals/OVERVIEW.md) —
    GPU-parallelized RL environments.
24. [Training a policy](24-training-a-policy/OVERVIEW.md) — PPO, from
    random actions to a working policy.
25. [Sim-to-real transfer](25-sim-to-real-transfer/OVERVIEW.md) —
    closing the reality gap, deploying a policy as a ROS2 node.
26. [Isaac GR00T](26-isaac-groot/OVERVIEW.md) — foundation models for
    robot manipulation.
27. [GPU-accelerated custom perception](27-gpu-perception-tensorrt/OVERVIEW.md)
    — TensorRT.
28. [Capstone: autonomous mobile manipulator](28-capstone-mobile-manipulator/OVERVIEW.md)
    — everything, integrated.

Chapter 28 is the final chapter of the curriculum — start with Chapter
23 if you've just finished Tier 3, or jump straight to Chapter 28 if
you want to see everything come together first and work backward.

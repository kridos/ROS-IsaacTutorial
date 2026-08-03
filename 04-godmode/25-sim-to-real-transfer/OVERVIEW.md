# Chapter 25: Sim-to-Real Transfer Techniques

## What this is

A policy trained purely in simulation (Chapter 24) usually performs
worse — sometimes fails outright — the first time it runs on a real
robot, because simulation is never a perfect physical match to reality.
This gap is called the **reality gap**, and this chapter covers the
standard techniques for closing it.

## Why it matters

Training in simulation (Chapters 23-24) only pays off if the result
actually works on real hardware. Without deliberately addressing the
reality gap, a well-trained simulated policy can be functionally useless
the moment it meets a real robot — these techniques are what make
sim-trained policies a practical real-world tool rather than a simulation
curiosity.

## Where this fits

Directly follows Chapter 24's training pipeline — same CartPole task,
now trained with additional robustness techniques, plus a look at how a
trained policy actually gets deployed as a ROS2 node, tying the RL
chapters back into the node/topic model every earlier chapter used.

## What the demo shows

Chapter 24's CartPole training extended with randomized physical
parameters (pole mass, cart friction) each episode, plus a plain ROS2
node that loads a trained policy checkpoint and runs it against
sensor-topic input, publishing commands — the deployment pattern that
turns a training-time checkpoint into something a real robot could
actually run.

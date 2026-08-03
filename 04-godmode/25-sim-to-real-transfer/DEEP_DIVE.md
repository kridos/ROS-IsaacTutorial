# Chapter 25 Deep Dive: Sim-to-Real Transfer

## Domain randomization for dynamics

Chapter 16 covered domain randomization for *visual* variety (lighting,
texture) so a perception model wouldn't overfit to one exact rendered
appearance. The same idea applies to *physical* simulation parameters
during RL training: randomize friction coefficients, object/link mass,
motor strength, and sensor noise/latency across training episodes,
rather than training against one fixed, precisely-known set of physics
values. A policy trained this way learns to be robust to *not knowing*
the real robot's exact physical parameters, rather than implicitly
depending on simulation's exact (and necessarily imperfect) physics
being correct. This is the direct RL-training analogue of Chapter 16's
"quantity without diversity" pitfall — randomizing only some relevant
physical variables while leaving others fixed leaves the policy
similarly overfit to whatever wasn't randomized, just in physics-space
instead of pixel-space.

## System identification

Domain randomization alone is a brute-force robustness strategy — cover
a wide enough range of possible physical parameters that the real
robot's actual values fall somewhere inside it. **System identification**
is the complementary, more targeted approach: actually measuring your
real robot's physical parameters (motor response curves, real friction,
true masses) and calibrating simulation to match them more precisely.
The two techniques work well together: system identification narrows
simulation toward reality, and domain randomization around that
better-calibrated center covers the remaining uncertainty — neither
technique alone is usually as effective as combining both.

## Observation and action space matching

A trained policy's inputs (observations) and outputs (actions) are fixed
by what the *training* environment provided — if training assumed
perfect, noiseless joint position feedback at a specific rate, and the
real robot's actual encoders are noisier, lower-resolution, or update
less often, the policy is being fed something subtly different from what
it learned on. Getting the real robot's sensor/actuator interface to
match the training environment's assumptions as closely as possible
(or, per the section above, training with realistic noise added so the
mismatch itself becomes something the policy is robust to) is a
prerequisite for a trained policy to behave anything like it did in
simulation.

## Deploying a trained policy as a ROS2 node

A trained policy (Chapter 24's checkpoint) is, underneath, a neural
network taking an observation tensor and returning an action tensor —
nothing about running that network at inference time requires Isaac Lab,
Isaac Sim, or any simulator at all. This chapter's
`deploy_policy_ros2_node.py` demonstrates the pattern: a plain `rclpy`
node loads the checkpoint once at startup, subscribes to whatever ROS2
topic carries the real (or, in this demo, simulated-for-illustration)
sensor data the policy expects as observations, runs one inference step
per incoming message, and publishes the resulting action as a command
topic — the same node/topic shape as literally every earlier chapter's
demos, with a trained neural network standing in for what was previously
hand-written control logic.

## Common pitfall: control frequency mismatch

A policy is trained assuming actions are applied at a specific control
rate (Chapter 24's environment stepped at a fixed simulated rate) — it
implicitly learns "this action, held for this much simulated time,
produces this much effect." Deploying the same policy at a different
real-world control loop rate (faster, slower, or — often worse —
irregular/jittery due to real system timing variance) changes that
implicit relationship, and the policy's learned behavior can degrade
noticeably even though nothing about the policy's weights changed.
Matching training and deployment control rates as closely as possible
is a real requirement, not a minor tuning knob — a surprisingly common
cause of "the policy worked great in simulation but is unstable on the
real robot" reports that turns out to have nothing to do with the reality
gap's more commonly-discussed causes (friction, sensor noise) at all.

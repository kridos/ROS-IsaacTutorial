# Chapter 23 Deep Dive: Isaac Lab Fundamentals

## Vectorized environments

Every simulator in this curriculum so far has simulated **one** robot
instance, stepped one call at a time (Chapter 7's Gazebo, Chapter 13's
Isaac Sim, Chapter 20's MuJoCo). Isaac Lab's core departure: a single
environment object actually represents **N identical environments**
running in parallel on the GPU, and `env.step(actions)` steps all of them
in one call, returning batched results:

```python
obs, rewards, terminated, truncated, info = env.step(actions)
# actions:    shape [num_envs, action_dim]
# obs:        shape [num_envs, obs_dim]
# rewards:    shape [num_envs]
# terminated: shape [num_envs]  (bool — did each env reach a terminal state)
# truncated:  shape [num_envs]  (bool — did each env hit a time limit)
```

This is the single most important mental shift from every earlier
simulation chapter: there is no "the robot's position," only "every
environment's robot's position," as one tensor. Code that assumes a
single scalar value (reading `obs[0]` and treating it as *the*
observation) is implicitly only looking at environment 0 and ignoring
every other parallel instance — a mistake that's easy to make coming
from single-instance simulators and doesn't error, just silently ignores
most of what's actually running.

## The Gym-style interface

`reset()` and `step(action)` returning `(observation, reward, terminated,
truncated, info)` is not Isaac-Lab-specific — it's the standard interface
used across the RL ecosystem (originally popularized by OpenAI Gym, now
maintained as Gymnasium), and Isaac Lab environments implement it
(batched, per above) specifically so existing RL algorithms and
libraries written against this interface work with Isaac Lab environments
with little to no modification. This is the same "build on an existing
standard rather than inventing a new one" pattern Chapter 10 described
for ROS2 building on DDS.

## ManagerBasedEnv and task configuration

Rather than one monolithic environment class hardcoding observations,
actions, rewards, and termination conditions together, Isaac Lab
structures a task as a configuration composed of separate **manager**
components: an observation manager (what the policy sees), an action
manager (how policy outputs become robot commands), a reward manager
(one or more reward *terms*, combined), and a termination manager (what
ends an episode — falling over, running out of time, succeeding at the
task). This separation is what lets you, for instance, swap in a
different reward function for the same task without touching the
observation or termination logic at all — useful in Chapter 24 when
tuning what a policy is actually being rewarded for.

## Common pitfall: writing non-vectorized code

Iterating over environments with a Python `for` loop, or writing logic
that only handles a single scalar observation/action, defeats the entire
purpose of Isaac Lab's parallelism and often breaks outright once
`num_envs > 1` (shape mismatches, or code that silently only processes
environment 0). Isaac Lab code — custom reward functions, custom
observation terms, anything you write yourself — needs to be written in
tensor-batched style from the start: operations that apply to the whole
`[num_envs, ...]` tensor at once (e.g. `torch.where`, elementwise ops),
not Python-level loops over individual environments. This chapter's demo
uses only Isaac Lab's built-in CartPole task specifically to let you see
correctly-vectorized code before writing any of your own in Chapter 24.

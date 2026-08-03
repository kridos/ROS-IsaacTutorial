# Chapter 24 Deep Dive: Training a Policy (PPO)

## PPO, conceptually

**PPO** (Proximal Policy Optimization) alternates two phases, repeated
many times:

1. **Collect experience**: run the current policy (a neural network
   mapping observation -> action) in the environment for some number of
   steps — exactly Chapter 23's `env.step(actions)` loop, except actions
   now come from the policy network instead of `torch.rand(...)`.
2. **Update the policy**: adjust the network's weights to make
   actions that led to higher reward more likely in similar future
   situations, and lower-reward actions less likely.

The "proximal" part matters specifically: naively updating the policy
network as aggressively as possible toward whatever performed best in
the last batch of experience can make training unstable — a big enough
update can make the policy suddenly much worse, not better, which then
poisons the *next* batch of collected experience with a bad policy's
worse performance. PPO's clipped update rule limits how far the policy
is allowed to change in a single update step, trading some update speed
for training stability. You don't need to derive the exact clipping math
to use PPO effectively — knowing *why* it exists (stability during
training) is enough to reason about training behavior.

## Isaac Lab uses existing RL libraries, not its own PPO

Isaac Lab doesn't reimplement PPO itself — it integrates with existing,
established RL libraries (commonly `rsl_rl`, with support for others
like `stable-baselines3` depending on version) that already implement
PPO and other algorithms correctly and efficiently. This mirrors the
curriculum's recurring theme: Nav2 and MoveIt2 (Chapters 11-12) exist so
you don't reimplement navigation/motion-planning from scratch; here,
Isaac Lab provides the fast vectorized environment (Chapter 23) and lets
an established RL library provide the actual learning algorithm, rather
than reinventing either piece.

## Reading training progress

The primary signal that training is working is the **reward curve**:
average episode reward, plotted against training iteration, should
trend upward over time (often via TensorBoard, which Isaac Lab's
training scripts typically log to automatically). A flat or noisy,
non-improving curve after a reasonable number of iterations usually
means something's wrong (a reward function that doesn't actually reward
the intended behavior, a bug in the environment, or simply needing more
training time) rather than being an inherent limit of the task.

## Train and play are separate scripts

A `train_*.py`-style script runs the training loop and periodically
saves a **checkpoint** (the policy network's learned weights) to disk. A
separate `play_*.py`-style script loads that checkpoint and runs the
policy *without* further training — this is how you actually watch what
was learned, since a training script's own console/TensorBoard output
only shows you numbers (reward curves), not the resulting behavior.

## Common pitfall: reward hacking

A climbing reward curve does not automatically mean the policy learned
to do the thing you intended — it means the policy learned to maximize
the *literal* reward signal you wrote, which is not always the same
thing. This is a well-known general RL problem, not specific to Isaac
Lab: a poorly-specified reward can be maximized by degenerate behavior
that technically satisfies the reward function's letter while missing
its intent (a classic example outside this curriculum: a reward for
"distance traveled" without penalizing falling over can be maximized by
a robot that repeatedly falls forward rather than genuinely walking).
Always watch the trained policy's actual behavior (this chapter's
`play_trained_policy.py`), not just the training curve, before trusting
a training run succeeded.

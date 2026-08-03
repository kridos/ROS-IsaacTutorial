# Demo: Training a CartPole Policy with PPO

## Prerequisites

Same as Chapter 23 (Isaac Lab installed, NVIDIA GPU), plus `rsl_rl`
(commonly bundled with an Isaac Lab install — check `./isaaclab.sh -p -m pip show rsl_rl`
if unsure).

## Train

```bash
./isaaclab.sh -p train_cartpole_ppo.py
```

## Expected output

```
Training for 50 iterations with 512 parallel environments...
[rsl_rl logging: iteration, mean reward, mean episode length, ...]
Training complete. Checkpoint saved to: .../checkpoints/model_49.pt
View reward curves with: tensorboard --logdir .../checkpoints
```

## Watch the reward curve

```bash
tensorboard --logdir checkpoints
```

Open the printed URL in a browser. Expected: `Mean Reward` trending
upward over the 50 iterations — even a short run should show a visible
upward trend for a task as simple as CartPole (per DEEP_DIVE.md, a flat
curve after this many iterations would suggest something's misconfigured,
not that the task is inherently hard).

## Play the trained policy

```bash
./isaaclab.sh -p play_trained_policy.py checkpoints/model_49.pt
```

Expected:

```
Loaded checkpoint: checkpoints/model_49.pt
Episode 1: total reward = 187.0
Episode 2: total reward = 203.0
Episode 3: total reward = 195.0
Episode 4: total reward = 210.0
Episode 5: total reward = 198.0
```

Compare against Chapter 23's random-action run, where reward per episode
was essentially whatever chance produced (usually low — a random-action
cart rarely balances the pole for long). A meaningfully higher, more
consistent per-episode reward here confirms the policy actually learned
something, not just that the reward curve in TensorBoard went up.

## Try it: train longer

Change `NUM_ITERATIONS` to `500` in `train_cartpole_ppo.py` and re-run.
Expected: a noticeably higher and more stable per-episode reward in
`play_trained_policy.py`'s output than the 50-iteration run produced —
a direct look at how training duration affects the resulting policy's
quality.

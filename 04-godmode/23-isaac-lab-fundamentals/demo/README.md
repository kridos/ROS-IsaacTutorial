# Demo: Isaac Lab CartPole — Vectorized Environments

## Prerequisites

- NVIDIA GPU (Isaac Lab has no CPU-only path).
- Isaac Lab installed per NVIDIA's Isaac Lab installation docs (it
  installs Isaac Sim as a dependency, or expects an existing Isaac Sim
  install depending on install method — check current docs, this
  changes between releases).

## How to run

Isaac Lab ships its own launch wrapper (a thin layer over Isaac Sim's
`python.sh` from Chapter 13, adding Isaac Lab-specific CLI parsing):

```bash
./isaaclab.sh -p cartpole_env_demo.py
```

(Run from wherever `isaaclab.sh` lives in your Isaac Lab install —
typically the repo root if installed from source.)

## Expected output

```
Initial observation shape: (4, 4)  (num_envs=4)
step= 0  obs.shape=(4, 4)  rewards=[1. 1. 1. 1.]  terminated=[False False False False]
step=10  obs.shape=(4, 4)  rewards=[1. 0. 1. 1.]  terminated=[False  True False False]
step=20  obs.shape=(4, 4)  rewards=[1. 1. 1. 0.]  terminated=[False False False  True]
...
Done.
```

The leading `4` in every shape is `num_envs` — the same shape appears in
every printed tensor, confirming everything is genuinely batched across
all 4 environments rather than one shared/single value. `terminated`
turning `True` for a given environment (CartPole's pole fell past the
allowed angle, or the cart went out of bounds) happens independently per
environment — environment 1 can terminate while environments 0, 2, 3
keep running, exactly the "no single fact, only per-environment facts"
model DEEP_DIVE.md describes.

## Try it: scale up

Change `NUM_ENVS = 4` to `NUM_ENVS = 1024` and re-run. Expected: the
script still runs (this is the entire point of GPU parallelism — 1024
environments cost little more wall-clock time per step than 4 do), and
every printed tensor's leading dimension becomes `1024` instead of `4`.

## Try it: read a single environment's data

Add `print(obs['policy'][0])` after a step — indexing into the batch to
look at just environment 0's observation, the vectorized-tensor
equivalent of "what would a single-instance simulator have shown you."

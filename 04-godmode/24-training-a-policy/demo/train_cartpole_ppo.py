#!/usr/bin/env python3
"""Runs a short PPO training session against Chapter 23's CartPole
environment using rsl_rl (Isaac Lab's default RL library integration —
see DEEP_DIVE.md for why Isaac Lab doesn't implement PPO itself), saving
a checkpoint as the reward curve starts climbing.

Deliberately short (a small number of iterations) — enough to SEE
learning start happening, not a full convergence run, which would take
much longer than reasonable for a learning demo.

Run with Isaac Lab's launch wrapper — see demo/README.md.
"""

from isaaclab.app import AppLauncher

app_launcher = AppLauncher(headless=True)
simulation_app = app_launcher.app

import os  # noqa: E402
import gymnasium as gym  # noqa: E402
import isaaclab_tasks  # noqa: E402
from isaaclab_tasks.utils import parse_env_cfg  # noqa: E402
from isaaclab_rl.rsl_rl import RslRlVecEnvWrapper  # noqa: E402
from rsl_rl.runners import OnPolicyRunner  # noqa: E402

NUM_ENVS = 512  # far more than Ch23's 4 — training benefits from more
                # parallel experience per update, which is cheap thanks
                # to GPU-vectorized simulation (see Ch23's DEEP_DIVE.md)
NUM_ITERATIONS = 50  # short on purpose, see module docstring
CHECKPOINT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "checkpoints")

# Minimal PPO hyperparameters/network config, passed to rsl_rl's runner —
# a real project would usually load this from a YAML config file rather
# than a hardcoded dict, kept inline here to keep this demo self-contained
# in one file.
TRAIN_CFG = {
    "seed": 42,
    "num_steps_per_env": 24,
    "max_iterations": NUM_ITERATIONS,
    "save_interval": 25,
    "algorithm": {
        "class_name": "PPO",
        "clip_param": 0.2,        # the "proximal" clipping DEEP_DIVE.md describes
        "learning_rate": 1.0e-3,
        "num_learning_epochs": 5,
        "gamma": 0.99,
    },
    "policy": {
        "class_name": "ActorCritic",
        "actor_hidden_dims": [32, 32],
        "critic_hidden_dims": [32, 32],
    },
}


def main():
    env_cfg = parse_env_cfg("Isaac-Cartpole-v0", num_envs=NUM_ENVS)
    env = gym.make("Isaac-Cartpole-v0", cfg=env_cfg)
    env = RslRlVecEnvWrapper(env)  # adapts the Gym-style env to rsl_rl's expected interface

    os.makedirs(CHECKPOINT_DIR, exist_ok=True)
    runner = OnPolicyRunner(env, TRAIN_CFG, log_dir=CHECKPOINT_DIR, device="cuda")

    # runner.learn() IS the collect-experience/update-policy loop
    # DEEP_DIVE.md describes, run NUM_ITERATIONS times — reward progress
    # is logged to CHECKPOINT_DIR for TensorBoard, and a checkpoint is
    # saved every save_interval iterations per TRAIN_CFG above.
    print(f"Training for {NUM_ITERATIONS} iterations with {NUM_ENVS} parallel environments...")
    runner.learn(num_learning_iterations=NUM_ITERATIONS)

    final_checkpoint = os.path.join(CHECKPOINT_DIR, f"model_{NUM_ITERATIONS - 1}.pt")
    print(f"Training complete. Checkpoint saved to: {final_checkpoint}")
    print(f"View reward curves with: tensorboard --logdir {CHECKPOINT_DIR}")

    env.close()
    simulation_app.close()


if __name__ == "__main__":
    main()

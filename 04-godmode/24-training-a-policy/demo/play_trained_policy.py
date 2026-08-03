#!/usr/bin/env python3
"""Loads a checkpoint saved by train_cartpole_ppo.py and runs the
trained policy (no further learning) for a fixed number of episodes,
printing per-episode total reward — the "watch what was actually
learned" step DEEP_DIVE.md describes, and a direct comparison point
against Chapter 23's random-action baseline.

Run with Isaac Lab's launch wrapper — see demo/README.md.
Usage: ./isaaclab.sh -p play_trained_policy.py <checkpoint_path>
"""

import os
import sys

from isaaclab.app import AppLauncher

app_launcher = AppLauncher(headless=True)
simulation_app = app_launcher.app

import torch  # noqa: E402
import gymnasium as gym  # noqa: E402
import isaaclab_tasks  # noqa: E402
from isaaclab_tasks.utils import parse_env_cfg  # noqa: E402
from isaaclab_rl.rsl_rl import RslRlVecEnvWrapper  # noqa: E402
from rsl_rl.runners import OnPolicyRunner  # noqa: E402

NUM_ENVS = 4  # small — this is for watching behavior, not fast training
NUM_EPISODES = 5


def main():
    if len(sys.argv) < 2:
        print("Usage: play_trained_policy.py <checkpoint_path>")
        sys.exit(1)
    checkpoint_path = sys.argv[1]

    env_cfg = parse_env_cfg("Isaac-Cartpole-v0", num_envs=NUM_ENVS)
    env = gym.make("Isaac-Cartpole-v0", cfg=env_cfg)
    env = RslRlVecEnvWrapper(env)

    # Same TRAIN_CFG shape train_cartpole_ppo.py used — OnPolicyRunner
    # needs matching policy/algorithm config to correctly reconstruct the
    # network architecture the checkpoint's weights belong to.
    runner = OnPolicyRunner(env, {
        "algorithm": {"class_name": "PPO"},
        "policy": {
            "class_name": "ActorCritic",
            "actor_hidden_dims": [32, 32],
            "critic_hidden_dims": [32, 32],
        },
    }, log_dir=None, device="cuda")
    runner.load(checkpoint_path)
    policy = runner.get_inference_policy(device="cuda")

    print(f"Loaded checkpoint: {checkpoint_path}")

    obs, _ = env.reset()
    episode_rewards = torch.zeros(NUM_ENVS)
    completed_episodes = 0

    while completed_episodes < NUM_EPISODES:
        with torch.no_grad():
            # No exploration/randomness here — policy(obs) is a
            # deterministic (or near-deterministic) forward pass through
            # the trained network, unlike training's action sampling.
            actions = policy(obs)

        obs, rewards, terminated, truncated, _ = env.step(actions)
        episode_rewards += rewards.cpu()

        done = terminated | truncated
        for env_idx in torch.nonzero(done).flatten().tolist():
            completed_episodes += 1
            print(f"Episode {completed_episodes}: total reward = {episode_rewards[env_idx]:.1f}")
            episode_rewards[env_idx] = 0.0

    env.close()
    simulation_app.close()


if __name__ == "__main__":
    main()

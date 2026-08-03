#!/usr/bin/env python3
"""Runs Isaac Lab's built-in CartPole environment with 4 parallel
instances and random actions, printing the batched observation/reward
tensors' shapes and sample values each step — makes the "N environments
at once, as one batched tensor" mental model from DEEP_DIVE.md concrete
rather than abstract.

Run with Isaac Lab's own launch wrapper — see demo/README.md.
"""

from isaaclab.app import AppLauncher

# AppLauncher boots the underlying Isaac Sim/Omniverse application, same
# role Chapter 13's SimulationApp played directly — Isaac Lab wraps that
# same boot step behind its own launcher, which also parses Isaac
# Lab-specific CLI args (like --num_envs) automatically.
app_launcher = AppLauncher(headless=True)
simulation_app = app_launcher.app

import torch  # noqa: E402  (import must follow AppLauncher, like Ch13's SimulationApp)
import gymnasium as gym  # noqa: E402
import isaaclab_tasks  # noqa: E402  (registers built-in tasks, including CartPole, with gymnasium)
from isaaclab_tasks.utils import parse_env_cfg  # noqa: E402

NUM_ENVS = 4
NUM_STEPS = 50


def main():
    env_cfg = parse_env_cfg("Isaac-Cartpole-v0", num_envs=NUM_ENVS)
    env = gym.make("Isaac-Cartpole-v0", cfg=env_cfg)

    obs, info = env.reset()
    print(f"Initial observation shape: {tuple(obs['policy'].shape)}  (num_envs={NUM_ENVS})")

    for step in range(NUM_STEPS):
        # Random actions, shaped [num_envs, action_dim] — every environment
        # gets its own independent random action in this single call,
        # not a Python loop assigning one action per environment.
        actions = torch.rand(env.action_space.shape, device=env.unwrapped.device) * 2.0 - 1.0

        obs, rewards, terminated, truncated, info = env.step(actions)

        if step % 10 == 0:
            print(
                f"step={step:2d}  obs.shape={tuple(obs['policy'].shape)}  "
                f"rewards={rewards.cpu().numpy().round(3)}  "
                f"terminated={terminated.cpu().numpy()}"
            )

    env.close()
    print("Done.")
    simulation_app.close()


if __name__ == "__main__":
    main()

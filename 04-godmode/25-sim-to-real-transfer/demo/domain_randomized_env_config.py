#!/usr/bin/env python3
"""Extends Chapter 24's CartPole training setup with PHYSICAL dynamics
randomization (pole mass, cart friction, randomized per episode) — the
sim-to-real technique from DEEP_DIVE.md, distinct from Chapter 16's
visual randomization for perception.

This is a training-time modification: run this instead of Chapter 24's
train_cartpole_ppo.py to produce a checkpoint trained with randomized
dynamics rather than fixed simulation defaults.

Run with Isaac Lab's launch wrapper — see demo/README.md.
"""

from isaaclab.app import AppLauncher

app_launcher = AppLauncher(headless=True)
simulation_app = app_launcher.app

import os  # noqa: E402
import gymnasium as gym  # noqa: E402
import isaaclab_tasks  # noqa: E402
from isaaclab.envs.mdp import events as mdp_events  # noqa: E402
from isaaclab.managers import EventTermCfg, SceneEntityCfg  # noqa: E402
from isaaclab_tasks.utils import parse_env_cfg  # noqa: E402
from isaaclab_rl.rsl_rl import RslRlVecEnvWrapper  # noqa: E402
from rsl_rl.runners import OnPolicyRunner  # noqa: E402

NUM_ENVS = 512
NUM_ITERATIONS = 50
CHECKPOINT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "checkpoints_randomized")

TRAIN_CFG = {
    "seed": 42,
    "num_steps_per_env": 24,
    "max_iterations": NUM_ITERATIONS,
    "save_interval": 25,
    "algorithm": {"class_name": "PPO", "clip_param": 0.2, "learning_rate": 1.0e-3,
                  "num_learning_epochs": 5, "gamma": 0.99},
    "policy": {"class_name": "ActorCritic", "actor_hidden_dims": [32, 32],
               "critic_hidden_dims": [32, 32]},
}


def add_dynamics_randomization(env_cfg):
    """Attaches EventTerms that re-randomize pole mass and cart friction
    at the start of every episode (event_term "reset" mode) — this is
    what makes the policy trained here robust to not knowing the real
    robot's exact physical parameters, per DEEP_DIVE.md."""

    # randomize_rigid_body_mass: re-samples the pole link's mass within
    # the given range each time an environment resets, rather than every
    # environment always training against the same fixed mass value.
    env_cfg.events.randomize_pole_mass = EventTermCfg(
        func=mdp_events.randomize_rigid_body_mass,
        mode="reset",
        params={
            "asset_cfg": SceneEntityCfg("robot", body_names="pole"),
            "mass_distribution_params": (0.8, 1.2),  # +/-20% of nominal mass
            "operation": "scale",
        },
    )

    # randomize_rigid_body_material: re-samples friction/restitution for
    # the cart's contact surfaces each reset — the friction-randomization
    # half of this chapter's dynamics randomization.
    env_cfg.events.randomize_cart_friction = EventTermCfg(
        func=mdp_events.randomize_rigid_body_material,
        mode="reset",
        params={
            "asset_cfg": SceneEntityCfg("robot", body_names="cart"),
            "static_friction_range": (0.5, 1.5),
            "dynamic_friction_range": (0.4, 1.3),
            "restitution_range": (0.0, 0.1),
            "num_buckets": 64,
        },
    )
    return env_cfg


def main():
    env_cfg = parse_env_cfg("Isaac-Cartpole-v0", num_envs=NUM_ENVS)
    env_cfg = add_dynamics_randomization(env_cfg)
    env = gym.make("Isaac-Cartpole-v0", cfg=env_cfg)
    env = RslRlVecEnvWrapper(env)

    os.makedirs(CHECKPOINT_DIR, exist_ok=True)
    runner = OnPolicyRunner(env, TRAIN_CFG, log_dir=CHECKPOINT_DIR, device="cuda")

    print(f"Training with dynamics randomization for {NUM_ITERATIONS} iterations...")
    runner.learn(num_learning_iterations=NUM_ITERATIONS)

    final_checkpoint = os.path.join(CHECKPOINT_DIR, f"model_{NUM_ITERATIONS - 1}.pt")
    print(f"Training complete. Checkpoint saved to: {final_checkpoint}")

    env.close()
    simulation_app.close()


if __name__ == "__main__":
    main()

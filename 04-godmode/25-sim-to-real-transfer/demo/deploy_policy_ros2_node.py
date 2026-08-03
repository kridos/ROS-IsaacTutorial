#!/usr/bin/env python3
"""Loads a trained-policy checkpoint (Chapter 24/this chapter's output)
and runs it as a plain ROS2 node: subscribes to a sensor-observation
topic, runs one policy inference step per incoming message, publishes
the resulting action as a command topic.

Deliberately has NO Isaac Sim / Isaac Lab imports at all — this is the
"wrap the trained policy as a ROS2 node" deployment pattern from
DEEP_DIVE.md, runnable with plain ROS2 + PyTorch, independent of any
simulator, mirroring (inverted) Chapter 20's "no ROS2 dependency at the
simulation layer" point: here there's no SIMULATION dependency at the
deployed-node layer.

Usage: python3 deploy_policy_ros2_node.py <checkpoint_path>
"""

import sys

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import torch
import torch.nn as nn


class PolicyNetwork(nn.Module):
    """Matches the ActorCritic architecture shape from Chapter 24's
    TRAIN_CFG (actor_hidden_dims=[32, 32]) — a deployed node needs to
    reconstruct the same network structure the checkpoint's weights
    belong to before it can load them, same requirement as Chapter 24's
    play_trained_policy.py reconstructing via OnPolicyRunner."""

    def __init__(self, obs_dim: int, action_dim: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_dim, 32), nn.ELU(),
            nn.Linear(32, 32), nn.ELU(),
            nn.Linear(32, action_dim),
        )

    def forward(self, obs):
        return self.net(obs)


class PolicyDeploymentNode(Node):
    # CartPole's observation is [cart_pos, cart_vel, pole_angle, pole_vel]
    # and action is a single scalar force — matching Chapter 23/24's task,
    # since this demo deploys a CartPole-trained policy. A real deployment
    # would match whatever robot/task the policy was actually trained for.
    OBS_DIM = 4
    ACTION_DIM = 1

    def __init__(self, checkpoint_path: str):
        super().__init__("policy_deployment_node")

        self._policy = PolicyNetwork(self.OBS_DIM, self.ACTION_DIM)
        # Loading raw network weights directly here (not via rsl_rl's
        # OnPolicyRunner, which Chapter 24's play script used) — a
        # deployed node typically extracts just the actor network's
        # weights from the full training checkpoint ahead of time, so
        # the deployment dependency footprint is "PyTorch" rather than
        # "the entire RL training stack."
        # NOTE: rsl_rl's OnPolicyRunner checkpoints (Chapter 24) store the
        # full actor-critic model under its own key structure, not a bare
        # "actor_state_dict" — in practice you'd extract just the actor
        # network's weights into this simpler shape once, offline, as a
        # deployment-preparation step (so the deployed node's only
        # runtime dependency is PyTorch, not the full rsl_rl training
        # stack). This checkpoint's exact key name is illustrative of that
        # extracted, deployment-ready format, not rsl_rl's raw output.
        checkpoint = torch.load(checkpoint_path, map_location="cpu")
        self._policy.load_state_dict(checkpoint["actor_state_dict"])
        self._policy.eval()  # inference mode — disables training-only behavior (e.g. dropout)

        self._action_publisher = self.create_publisher(Float32MultiArray, "policy/action", 10)
        self.create_subscription(
            Float32MultiArray, "policy/observation", self._on_observation, 10
        )

        self.get_logger().info(f"Loaded policy from {checkpoint_path}, ready for inference")

    def _on_observation(self, msg: Float32MultiArray):
        if len(msg.data) != self.OBS_DIM:
            self.get_logger().warn(
                f"Expected observation of length {self.OBS_DIM}, got {len(msg.data)} — skipping"
            )
            return

        obs = torch.tensor(msg.data, dtype=torch.float32).unsqueeze(0)  # shape [1, OBS_DIM]

        # See DEEP_DIVE.md's control frequency pitfall: this callback
        # runs once per incoming observation message — whatever rate the
        # real sensor publishes at becomes this policy's effective
        # control rate, and that rate should match what it was trained
        # at as closely as possible.
        with torch.no_grad():
            action = self._policy(obs)

        action_msg = Float32MultiArray()
        action_msg.data = action.squeeze(0).tolist()
        self._action_publisher.publish(action_msg)


def main():
    if len(sys.argv) < 2:
        print("Usage: deploy_policy_ros2_node.py <checkpoint_path>")
        sys.exit(1)

    rclpy.init()
    node = PolicyDeploymentNode(sys.argv[1])
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()

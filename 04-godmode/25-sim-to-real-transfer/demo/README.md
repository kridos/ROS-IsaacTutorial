# Demo: Sim-to-Real Transfer

## Part 1: Train with dynamics randomization

Same prerequisites as Chapter 24.

```bash
./isaaclab.sh -p domain_randomized_env_config.py
```

Expected: similar training output to Chapter 24's `train_cartpole_ppo.py`,
saving to `checkpoints_randomized/` instead. Because pole mass and cart
friction now vary every episode (see DEEP_DIVE.md), the reward curve may
climb slightly less smoothly than Chapter 24's fixed-dynamics run — a
normal, expected trade-off: the policy is learning a harder, more
general problem (work across a range of physical parameters) rather than
the easier, narrower one (work for exactly one fixed set of parameters).

## Part 2: Deploy as a ROS2 node

## Prerequisites

Plain ROS2 (no Isaac Sim/Isaac Lab needed for this part) plus PyTorch
(`pip install torch` in an isolated venv — CPU-only is fine here, this
node runs a tiny 2-layer network, not training).

## How to run

```bash
python3 deploy_policy_ros2_node.py checkpoints_randomized/deployment_ready.pt
```

(See the script's comment on why a checkpoint prepared for deployment,
not rsl_rl's raw training checkpoint, is expected here.)

In another terminal, publish a fake observation to see inference run:

```bash
ros2 topic pub /policy/observation std_msgs/msg/Float32MultiArray "{data: [0.1, 0.0, 0.05, 0.0]}" --once
```

## Expected output

Node terminal:

```
[INFO] [policy_deployment_node]: Loaded policy from checkpoints_randomized/deployment_ready.pt, ready for inference
```

After the `ros2 topic pub` command:

```bash
ros2 topic echo /policy/action --once
```

Expected: a single float value (the policy's chosen cart force for that
observation) — confirming the deployed node ran real inference through
the loaded network and published a result, using only plain ROS2 +
PyTorch, no simulator involved at inference time.

## Try it: measure the control rate

Publish observations in a loop at a known rate (e.g. `ros2 topic pub
/policy/observation ... --rate 50`) and use `ros2 topic hz
/policy/action` to confirm the node's output rate matches — a hands-on
look at why DEEP_DIVE.md's control-frequency pitfall is something you can
directly verify, not just something to worry about abstractly.

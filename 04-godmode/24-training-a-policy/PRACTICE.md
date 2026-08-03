# Practice: Training a Policy (PPO)

1. **Train longer, systematically.** Do demo/README.md's "Try it: train
   longer" exercise at 3 different durations (50, 200, 500 iterations)
   and tabulate mean episode reward from `play_trained_policy.py` at
   each — a small, real experiment in how training duration affects
   policy quality, not just a single before/after comparison.

2. **Change a hyperparameter, deliberately.** Increase `learning_rate`
   in `TRAIN_CFG` by 10x and re-train. Expected (per DEEP_DIVE.md's PPO
   discussion): training may become less stable — confirm whether the
   reward curve gets noisier or actively degrades, connecting back to
   *why* PPO's clipping exists in the first place.

3. **Reward hacking, on purpose.** Modify the CartPole task's reward (if
   your Isaac Lab version exposes an easy override) to reward *only*
   staying alive, with no penalty for the cart drifting far from center.
   Train briefly and check via `play_trained_policy.py` whether the
   resulting policy does something degenerate (e.g. drifts to one side)
   — a hands-on look at DEEP_DIVE.md's reward-hacking pitfall.

4. **Watch training live.** Open TensorBoard *while* `train_cartpole_ppo.py`
   is still running (not after) and watch the reward curve update in
   real time — get comfortable reading training progress as it happens,
   which is how you'll actually monitor longer real training runs.

5. **Stretch:** modify `play_trained_policy.py` to also record each
   episode's full observation trajectory (not just total reward) and
   plot pole angle over time for one episode — confirm visually that the
   trained policy is actively correcting the pole, not just getting
   lucky.

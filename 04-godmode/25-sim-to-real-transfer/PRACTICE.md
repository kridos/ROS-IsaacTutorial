# Practice: Sim-to-Real Transfer

1. **Compare robustness, quantitatively.** Train two policies —
   Chapter 24's fixed-dynamics version and this chapter's
   randomized-dynamics version — then evaluate *both* against a test
   environment configured with a mass/friction *outside* the training
   randomization range. Which one degrades less? This is the actual
   point of domain randomization, made measurable.

2. **Widen or narrow the randomization range.** Change
   `mass_distribution_params` from `(0.8, 1.2)` to `(0.5, 1.5)` and
   retrain — does the policy get more robust, train more slowly, or
   both? Write a sentence on the trade-off you observe.

3. **Measure the control-rate pitfall directly.** Do demo/README.md's
   "Try it: measure the control rate" exercise at two different
   `--rate` values (e.g. 20 and 100) and compare the deployed node's
   actual output behavior/latency at each — connect back to
   DEEP_DIVE.md's warning about matching training and deployment rates.

4. **Simulate sensor noise in deployment.** Modify a copy of
   `deploy_policy_ros2_node.py` to add small random noise to incoming
   observations before running inference, simulating a noisier real
   sensor than the (possibly noiseless) training assumed — does the
   published action become visibly less stable?

5. **Stretch:** extract a real deployment-ready checkpoint from an
   `rsl_rl` training run (per the code comment in
   `deploy_policy_ros2_node.py` about checkpoint format conversion) —
   write the actual conversion script, going from Chapter 24's raw
   `OnPolicyRunner` checkpoint format to the simple `actor_state_dict`
   shape this chapter's deployment node expects.

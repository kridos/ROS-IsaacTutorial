# Practice: Isaac Lab Fundamentals

1. **Read a single environment's data.** Do demo/README.md's suggested
   exercise (index `obs['policy'][0]`) and extend it: print environment
   0's full observation *and* which environments have terminated so far,
   confirming your understanding of per-environment vs. batch-wide state.

2. **Scale up, and measure.** Do demo/README.md's "Try it: scale up"
   exercise (`num_envs = 1024`), and time how long `NUM_STEPS` takes to
   run at 4 vs. 1024 environments — confirm wall-clock time barely
   changes, the concrete payoff of GPU-vectorized simulation DEEP_DIVE.md
   describes.

3. **Break vectorization on purpose.** Write a *deliberately* broken
   version of the step loop that does `actions =
   torch.rand(env.action_space.shape[1:])` (missing the `num_envs`
   dimension) and observe the shape-mismatch error — then explain in one
   sentence which part of DEEP_DIVE.md's warning this demonstrates.

4. **A different built-in task.** Swap `"Isaac-Cartpole-v0"` for another
   Isaac Lab built-in task ID (check your installed version's available
   tasks) and adapt the print statements to that task's observation
   shape.

5. **Stretch:** write a *non-random* action policy by hand — e.g. for
   CartPole, a simple rule like "push right if the pole is leaning
   right" using `obs['policy']`'s pole-angle field — and compare its
   average reward over 50 steps against the random-action baseline,
   before you ever train anything with RL in Chapter 24.

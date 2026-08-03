# Practice: MuJoCo

1. **Remove the joint limit.** Do demo/README.md's suggested exercise
   (widen or remove `joint2`'s `range`) and additionally plot both
   joints' angle-over-time using matplotlib, comparing the
   limited-vs-unlimited runs on one chart.

2. **Read velocity too.** Implement demo/README.md's second suggested
   exercise (print `data.qvel`) and use it to detect when the arm has
   effectively "settled" (velocity near zero for N consecutive steps) —
   print the settling time.

3. **A third joint.** Extend `simple_arm.xml` with a third hinge joint
   (a wrist) following `joint2`'s pattern, add a matching motor to the
   `<actuator>` block, and update `run_sim.py` to drive and print all
   three joints.

4. **Passive vs. actuated.** Set `data.ctrl` to all zeros (no applied
   torque) and run the simulation — confirm the arm falls under gravity
   alone and settles hanging down, a baseline "passive dynamics" run to
   compare your actuated runs against.

5. **Stretch:** write a tiny proportional controller (no RL) that reads
   `data.qpos`, computes an error against a target joint angle, and sets
   `data.ctrl` proportionally to close that error each step — get the
   arm to hold a specific pose using hand-written control instead of
   the sinusoidal open-loop torque this chapter's demo uses.

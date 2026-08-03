# Practice: Capstone — Autonomous Mobile Manipulator

1. **Break the footprint pitfall, measure it.** Do demo/README.md's
   "Try it: remove the stow-before-navigate step" exercise, and this
   time actually measure the consequence: log the Nav2 planner's
   success/failure and any inflation-related warnings with and without
   the stow step, across a few runs, rather than just observing once.

2. **A third stop.** Extend `mission_coordinator.py`'s mission to visit a
   third waypoint after drop-off (e.g. return to a "home" position) —
   practice extending the mission-coordinator pattern beyond the
   pick-then-place shape this chapter's demo hardcodes.

3. **Real detection, swapped in.** Replace `_detect_object`'s hardcoded
   `SIMULATED_OBJECT_POSE` with a real subscription to a detection topic
   (Chapter 15's AprilTag pattern is the most direct fit — place an
   AprilTag on the block and localize it that way) — the natural next
   step DEEP_DIVE.md explicitly flags as out of scope for the base demo.

4. **Dynamic footprint, attempted.** Research Nav2's support for a
   dynamically-updated footprint (vs. the fixed `robot_radius` this
   capstone relies on) and attempt to wire the arm's current extension
   state into it — even a partial attempt will surface why the
   simpler stow-before-navigate rule was chosen for this chapter's demo.

5. **Stretch — the full curriculum, one more time:** re-run this
   capstone but swap Gazebo for Isaac Sim (Chapter 13/14's bridge
   pattern) underneath Nav2/MoveIt2 instead of Gazebo, and swap the
   simulated detection step for Isaac ROS AprilTag (Chapter 15) — at
   that point you've rebuilt this capstone using nearly every simulator
   and perception system this curriculum covered.

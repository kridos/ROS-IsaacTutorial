# Practice: Advanced MoveIt2 (Pick-and-Place)

1. **A second block.** Add a second `target_block2` to
   `planning_scene_setup.py` and extend `pick_and_place.py` to pick up
   both blocks in sequence, placing them at two different locations.

2. **Cartesian fraction failure, on purpose.** Set `PLACE_POSITION` to
   somewhere just barely out of a clean straight-line reach from the
   pre-place pose (e.g. behind an obstacle you add to the scene) and
   confirm `cartesian_move` correctly reports a low fraction and aborts,
   per DEEP_DIVE.md's warning not to trust a Cartesian call just because
   it didn't error.

3. **The pitfall, deliberately.** Follow demo/README.md's "Try it: skip
   the attach step" exercise, but this time add a second obstacle in the
   scene positioned so the un-attached block's stale collision geometry
   would visibly conflict with the retreat path — confirm you can *see*
   the consequence, not just infer it.

4. **Re-grasp after a failed pick.** Add retry logic: if the grasp
   approach's Cartesian fraction is too low, retreat to pre-grasp and
   try once more before giving up — a small taste of Chapter 17's
   retry-on-failure thinking, applied to manipulation instead of
   navigation.

5. **Stretch:** parameterize `pick_and_place.py` to accept grasp and
   place positions as command-line arguments instead of hardcoded
   constants, and write a small script that queues up 3 different
   pick-and-place tasks to run back to back.

# Practice: Isaac Sim Intro

1. **Import a different robot.** Run `import_and_spawn.py` against
   Chapter 5's `simple_arm.urdf.xacro` instead of Chapter 7's
   diff-drive robot, and confirm it imports and settles under gravity
   the same way.

2. **Multiple robots, one stage.** Modify the script to import and spawn
   the diff-drive robot twice, at two different `prim_path`s and initial
   positions on the same stage — a USD-side preview of Chapter 19's
   multi-robot chapter.

3. **Inspect the USD.** After running the script, open the generated
   `.usd` file in a text editor (USD's ASCII form, `.usda`, is
   human-readable if you export/convert to it) and find the prim
   corresponding to `left_wheel_joint` — confirm you can trace the same
   joint you wrote in URDF to its USD representation.

4. **Break the import on purpose.** Edit a copy of the diff-drive URDF to
   remove all `<inertial>` blocks, and run the import — observe whether
   PhysX complains or behaves oddly, connecting DEEP_DIVE.md's
   inertial-values pitfall to something you actually saw happen.

5. **Stretch:** modify the script to step physics for 10 seconds instead
   of 3, and print not just position but the robot's orientation
   (extract rotation from the transform matrix) each printed step —
   confirm it settles flat (no unexpected tipping) as further evidence
   the import produced a physically sane robot.

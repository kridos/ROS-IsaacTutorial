# Practice: MoveIt2 Basics

1. **Reach every corner.** Write a small script that requests plans to
   4-5 different target poses in sequence (a rough bounding box around
   the arm's reachable workspace) and logs which succeeded vs. failed —
   build an intuition for the arm's actual reach from Chapter 5's link
   lengths, rather than guessing.

2. **Named states.** Add a second named `group_state` to a copy of
   Chapter 12's SRDF (e.g. `"reach_forward"`, all joints at specific
   nonzero angles) and modify `move_to_pose.py` to optionally plan to a
   named state instead of a pose target.

3. **IK ambiguity.** Request a plan to the same reachable target pose
   five times in a row (calling `plan()` repeatedly) and log the
   resulting joint angles each time — since OMPL is sampling-based (per
   DEEP_DIVE.md), you may see slightly different joint configurations
   reach the same end-effector pose across runs.

4. **Diagnose a failure visually.** Deliberately request an unreachable
   pose target, then open RViz2's MotionPlanning display and find the
   goal-state coloring DEEP_DIVE.md describes — write one sentence on
   what you see and whether it confirms "unreachable" vs. "in collision."

5. **Stretch:** add a static box obstacle to the planning scene near the
   arm's workspace (a small taste of Chapter 18's Planning Scene
   Interface, used properly there) and confirm a plan that used to
   succeed now either fails or routes around it.

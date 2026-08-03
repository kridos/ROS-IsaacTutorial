# Practice: URDF/Xacro

1. **Add a third joint.** Extend `simple_arm.urdf.xacro` with a
   `link3`/`joint3` pair (a wrist), following the pattern of `joint2`.
   Confirm it shows up and moves correctly in RViz2 via
   `display.launch.py`.

2. **Xacro macro.** Refactor `simple_arm.urdf.xacro` so the repeated
   link+joint pattern (box geometry, collision, inertial) is a
   `<xacro:macro>` you call once per segment with different length
   parameters, instead of copy-pasted XML per link.

3. **Break the tree on purpose.** Change `joint2`'s `<parent
   link="link1"/>` to `<parent link="base_link"/>` (skipping link1) and
   see what RViz2 and `ros2 run tf2_tools view_frames` show — confirm it
   matches DEEP_DIVE.md's disconnected-tree description, then fix it.

4. **A different joint type.** Change `joint1` from `revolute` to
   `prismatic` (a sliding joint instead of rotating) with a sensible
   `<limit>`, and confirm the slider behavior changes accordingly in
   `joint_state_publisher_gui`.

5. **Stretch:** author a 4-wheel (not 2-wheel) rover chassis from
   scratch in Xacro, using properties for wheelbase/track width so the
   whole geometry scales from a couple of numbers — practice for
   Chapter 7's diff-drive robot, which you'll extend with sensors in
   Chapter 9 either way.

# Practice: Dev Environment

1. **Extend `verify_install.sh`.** Add a check that `~/ros2_ws` exists
   and has been built at least once (`install/setup.bash` present). Add
   a check that reports whether `ROS_DOMAIN_ID` collides with a commonly
   used default (0) and suggests picking a less common number.

2. **Break it, then fix it blind.** Comment out the `source
   /opt/ros/jazzy/setup.bash` line in your `.bashrc`, open a new
   terminal, and try to diagnose why `ros2` commands stopped working
   using only the symptoms (no re-reading DEEP_DIVE.md) — then check
   your diagnosis against the chapter.

3. **Second workspace.** Create a second colcon workspace
   (`~/ros2_ws_experiments/src`) and figure out how to have both it and
   `~/ros2_ws` sourced in the same terminal without one overwriting the
   other (hint: sourcing order and "overlaying," per DEEP_DIVE.md).

4. **Stretch:** write a one-shot setup script that does everything
   DEEP_DIVE.md's install steps do, idempotently (safe to run twice
   without erroring) — a rough first draft of what a real team's
   "new machine setup" script looks like.

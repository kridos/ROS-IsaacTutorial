# Practice: ROS2 <-> Isaac Sim Bridge

1. **A square path, Isaac Sim edition.** Port Chapter 7's Practice
   exercise #4 (drive a rough square via timed Twist commands) to run
   against this chapter's Isaac Sim robot instead of Gazebo — confirm
   the same ROS2-side code works unmodified against a different
   simulator underneath, which is the whole point of this chapter.

2. **Add odometry noise.** OmniGraph has nodes for adding noise to
   published data — find and attach one to the "ROS2 Publish Odometry"
   node so `/odom` includes some realistic jitter, then compare
   `drive_and_log_odom.py`'s output before/after.

3. **Compare the two bridges directly.** Run Chapter 7's Gazebo demo and
   this chapter's Isaac Sim demo side by side (different terminals,
   different `ROS_DOMAIN_ID` to avoid cross-talk) and drive both with
   identical `Twist` commands for 5 seconds — log both `/odom` outputs
   and compare the resulting trajectories.

4. **A third topic.** Add a "ROS2 Publish Clock" or joint-state
   publishing node to the OmniGraph, bridging one more piece of Isaac
   Sim's internal state to ROS2 beyond `/cmd_vel`/`/odom`.

5. **Stretch:** rebuild this chapter's OmniGraph through the Isaac Sim
   GUI (Window -> Visual Scripting -> Action Graph) by hand instead of
   programmatically, to directly compare the two ways of building the
   same graph DEEP_DIVE.md mentions.

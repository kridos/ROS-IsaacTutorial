# Practice: Isaac ROS

1. **Log VSLAM's confidence.** Extend `vslam_pose_listener.py` to track
   how often `VisualSlamStatus` reports lost tracking over a run
   (percentage of received status messages), and print a summary when
   the node shuts down.

2. **AprilTag distance filter.** Modify `apriltag_pose_logger.cpp` to
   only log detections within 2 meters of the camera (using the pose's
   translation magnitude), suppressing far-away/likely-unreliable
   detections.

3. **Combine with TF2.** Extend `vslam_pose_listener.py` to also look up
   `map -> odom` (if a map frame exists in your setup) alongside
   `odom -> base_link`, so you can see the full localization chain from
   Chapter 8's tree-composition perspective, not just VSLAM's direct
   output.

4. **Dev container sanity check.** Without running any perception node,
   write a short script/checklist confirming you're actually inside the
   Isaac ROS dev container (check for expected CUDA/TensorRT versions)
   *before* attempting to launch anything — practice catching
   DEEP_DIVE.md's most common pitfall preemptively.

5. **Stretch:** compare AMCL (Chapter 11) and VSLAM (this chapter)
   pose estimates for the same short robot run, logging both to a bag
   (Chapter 6) and plotting the two trajectories overlaid — a concrete
   look at how lidar-based and vision-based localization diverge.

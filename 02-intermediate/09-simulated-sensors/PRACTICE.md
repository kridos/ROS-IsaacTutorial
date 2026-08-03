# Practice: Simulated Sensors

1. **Add a second camera.** Add a rear-facing camera to
   `sensored_diffdrive.urdf.xacro` (own link, own optical frame, own
   `<sensor>` block, bridged on its own topic) and confirm both camera
   feeds show up correctly-oriented with `rqt_image_view`.

2. **Tune the lidar.** Change the lidar's `<samples>` from 360 to 36
   (10-degree resolution instead of 1-degree) and compare
   `sensor_subscriber.py`'s printed min/max range accuracy against an
   obstacle — a concrete look at the resolution/performance trade-off
   sensor configuration involves.

3. **Break the optical frame on purpose.** Remove the
   `camera_optical_joint`'s rotation (`rpy="0 0 0"` instead of the REP
   103 rotation) and view the camera feed with an RViz2 `Camera` display
   using TF — notice the image looks "wrong" relative to the robot even
   though the pixels themselves are unchanged, per DEEP_DIVE.md's
   optical-frame discussion.

4. **IMU sanity check.** Drive the robot in a circle (`angular.z` nonzero)
   and log `/imu`'s `angular_velocity.z` alongside your commanded value —
   confirm they roughly match, and describe in one sentence what the
   Gaussian noise model does to that comparison.

5. **Stretch:** add a depth camera (`type="camera"` with a depth output,
   or `type="rgbd_camera"` depending on your Gazebo version) alongside
   the RGB camera, bridge its topic, and visualize the resulting point
   cloud in RViz2 — a preview of the kind of data Chapter 15's Isaac ROS
   VSLAM consumes.

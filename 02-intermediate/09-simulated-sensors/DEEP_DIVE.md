# Chapter 9 Deep Dive: Simulated Sensors

## Sensor plugin blocks

Like Chapter 7's diff-drive plugin, each simulated sensor is a `<gazebo>`
extension block attached to a link, naming a `<sensor type="...">` and
its Gazebo-side topic. Key parameters, per sensor:

- **Camera** (`type="camera"`): `<update_rate>` (Hz), `<image><width>`/
  `<height>`, `<horizontal_fov>`. Publishes `sensor_msgs/msg/Image`.
- **Lidar** (`type="gpu_lidar"` — GPU-accelerated, preferred over the
  CPU `"lidar"` type for performance): `<update_rate>`, `<horizontal>`
  scan `<samples>`/`<min_angle>`/`<max_angle>`, `<range><min>`/`<max>`.
  Publishes `sensor_msgs/msg/LaserScan` (2D) via the bridge.
- **IMU** (`type="imu"`): `<update_rate>`, optional noise model per axis
  (`<noise type="gaussian">` with `<mean>`/`<stddev>`, since real IMUs are
  noisy and code consuming IMU data should be tested against noisy input,
  not a perfect signal). Publishes `sensor_msgs/msg/Imu` (orientation,
  angular velocity, linear acceleration).

## Bridging sensor topics

Same `ros_gz_bridge parameter_bridge` mechanism as Chapter 7, extended
with one line per sensor topic. Sensor topics conventionally bridge
**Gazebo → ROS2 only** (the `[` direction from Chapter 7's DEEP_DIVE.md)
since nothing should be publishing simulated sensor data from the ROS2
side back into Gazebo.

## Frame conventions: optical frame vs. robot frame

Camera data has a subtlety worth knowing before it confuses you: image
data is conventionally published in an **optical frame** following
REP 103 — Z pointing forward (out of the lens), X right, Y down — which
is different from the **robot frame** convention (X forward, Y left, Z
up) used for `base_link` and most everything else in this curriculum.
This isn't a Gazebo quirk, it's a ROS2-wide convention matching how
image processing math is normally written (row/column, Z-depth). A
camera link's URDF typically has a small child frame
(`camera_optical_frame`) rotated to match this convention, separate from
the camera link's own frame — downstream code (Isaac ROS's VSLAM in
Chapter 15, for instance) expects data in the optical frame, so getting
this rotation right (or wrong) is a common source of "my camera data
looks rotated 90 degrees for no reason" bugs.

## Update rate vs. physics step rate

A sensor's `<update_rate>` is independent of the physics engine's step
rate (often 1000 Hz internally, per Chapter 7's DEEP_DIVE.md). A camera
at 30 Hz and a lidar at 10 Hz both sample the same underlying physics
state at their own rates — this is normal and expected. What's a genuine
pitfall: setting a sensor's `update_rate` *higher* than the real-time
factor the simulation can actually sustain (see Chapter 7's RTF
pitfall) — the sensor will still claim to publish at the configured
rate, but the *wall-clock* rate you actually receive messages at will be
throttled by however slowly Gazebo is actually running, which can look
like a sensor bug when it's really a performance problem.

## Common pitfall

Beyond the optical-frame rotation confusion above: forgetting to add a
new sensor's topic to the `ros_gz_bridge` argument list (Chapter 7's
DEEP_DIVE.md pitfall, recurring here) is the single most common reason a
newly-added sensor's data "isn't showing up" in ROS2 — the sensor is
working fine inside Gazebo, it's just not crossing the bridge yet.
Always check `ros2 topic list` for the expected topic name after adding
a new sensor, before assuming the sensor plugin itself is broken.

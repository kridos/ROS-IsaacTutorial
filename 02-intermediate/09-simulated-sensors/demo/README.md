# Demo: Simulated Sensors (Camera, Lidar, IMU)

## Prerequisites

Same as Chapter 7's Gazebo demo (`ros-jazzy-ros-gz`, `ros-jazzy-ros-gz-bridge`,
`ros-jazzy-ros-gz-sim`, `ros-jazzy-xacro`).

## How to run

```bash
ros2 launch gazebo_sensors.launch.py
```

In another terminal:

```bash
python3 sensor_subscriber.py
```

## Expected output

`sensor_subscriber.py` logs, roughly interleaved at each sensor's own
rate (camera 30 Hz, IMU 100 Hz, lidar 10 Hz):

```
[INFO] [sensor_subscriber]: [camera] 640x480 encoding=rgb8 frame_id=camera_optical_frame
[INFO] [sensor_subscriber]: [imu] orientation quaternion=(0.00, 0.00, 0.00, 1.00) accel_z=9.81
[INFO] [sensor_subscriber]: [lidar] 360 samples, min=0.18m max=12.00m
```

The lidar's `min` value should roughly match the robot's distance to the
nearest visible obstacle (in the empty world, that's just the ground
plane's edge or nothing in range — try Chapter 7's driving commands to
move the robot near a spawned object, or add a `<model>` box to
`empty_world.sdf` if you want a nearby obstacle to see a smaller `min`
value). IMU `accel_z` should read close to `9.81` at rest (gravity, in
the robot's own frame) when the robot is stationary.

## Inspect raw messages

```bash
ros2 topic echo /scan --once
ros2 topic echo /imu --once
ros2 topic hz /camera/image_raw   # should settle near 30.0
```

## Try it: watch the camera feed

```bash
ros2 run rqt_image_view rqt_image_view /camera/image_raw
```

(from Chapter 6's rqt toolkit) — opens a live window showing what the
simulated camera sees.

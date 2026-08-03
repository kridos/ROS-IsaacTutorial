# Demo: Isaac ROS — VSLAM Pose Listener & AprilTag Logger

## Prerequisites

- NVIDIA Jetson or RTX GPU.
- The Isaac ROS dev container workflow — clone `isaac_ros_common` and use
  its `run_dev.sh` script to enter a container with the correct
  CUDA/TensorRT stack, per NVIDIA's Isaac ROS documentation (exact repo
  URLs/versions change between releases — check the current Isaac ROS
  docs rather than a hardcoded version here).
- `isaac_ros_visual_slam` and `isaac_ros_apriltag` packages installed
  inside that dev container.
- A stereo camera (real, or simulated via Isaac Sim's ROS2 bridge from
  Chapter 14, configured as a stereo pair) publishing image topics.

## Build the C++ demo package

Inside the dev container, from a colcon workspace:

```bash
cp -r cpp ~/isaac_ros-dev/workspaces/isaac_ros-dev/src/isaac_ros_perception_demo
cd ~/isaac_ros-dev/workspaces/isaac_ros-dev
colcon build --packages-select isaac_ros_perception_demo
source install/setup.bash
```

(Path shown matches the Isaac ROS dev container's default workspace
layout — adjust if your dev container setup differs.)

## How to run

```bash
ros2 launch isaac_ros_perception.launch.py
```

This starts Visual SLAM, AprilTag detection, and the C++
`apriltag_pose_logger`. In another terminal:

```bash
python3 python/vslam_pose_listener.py
```

## Expected output

`vslam_pose_listener.py`, once VSLAM has a lock on the scene:

```
[INFO] [vslam_pose_listener]: VSLAM odometry: x=0.021, y=0.003, z=0.000
[INFO] [vslam_pose_listener]: VSLAM tracking status: 0
[INFO] [vslam_pose_listener]: TF check: odom -> base_link transform is present
```

(`vo_state=0` typically means good tracking — check
`isaac_ros_visual_slam_interfaces/msg/VisualSlamStatus`'s definition for
your installed version's exact status code meanings.)

`apriltag_pose_logger` (in the launch terminal), when an AprilTag is
visible to the camera:

```
[INFO] [apriltag_pose_logger]: Tag id=3 detected at (0.412, -0.055, 1.203)
```

## Sanity-check without a real robot

If you don't have a stereo camera or AprilTags handy, confirm the nodes
at least start and advertise their topics correctly:

```bash
ros2 topic list | grep -E "visual_slam|tag_detections"
```

Expected: `/visual_slam/tracking/odometry`, `/visual_slam/status`, and
`/tag_detections` all present, even with no data flowing yet — confirms
the nodes launched successfully before troubleshooting camera input.

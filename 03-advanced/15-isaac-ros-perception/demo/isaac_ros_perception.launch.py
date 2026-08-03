"""Starts Isaac ROS Visual SLAM and AprilTag detection nodes (from the
Isaac ROS packages, assumed already installed inside the Isaac ROS dev
container per DEEP_DIVE.md) plus this chapter's two demo listener nodes.

This launch file intentionally does NOT start a camera source — run it
alongside a real or simulated stereo camera publishing to the topics
isaac_ros_visual_slam and isaac_ros_apriltag expect (see demo/README.md
for exact topic remapping if your camera publishes under different
names).

Run (inside the Isaac ROS dev container):
    ros2 launch isaac_ros_perception.launch.py
"""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    visual_slam_node = Node(
        package="isaac_ros_visual_slam",
        executable="isaac_ros_visual_slam",
        name="visual_slam_node",
        parameters=[{
            "enable_rectified_pose": True,
            "denoise_input_images": False,
            "enable_slam_visualization": True,
            "enable_landmarks_view": True,
            "enable_observations_view": True,
        }],
    )

    apriltag_node = Node(
        package="isaac_ros_apriltag",
        executable="isaac_ros_apriltag",
        name="apriltag_node",
    )

    # apriltag_pose_logger is the C++ demo package under demo/cpp — must
    # be colcon-built first (see demo/README.md). vslam_pose_listener.py
    # is a standalone script (like Chapters 2-3's Python demos) and is
    # NOT started here — run it directly with `python3` in its own
    # terminal per demo/README.md, so it stays copy-paste runnable
    # without requiring its own colcon package.
    apriltag_pose_logger_node = Node(
        package="isaac_ros_perception_demo",
        executable="apriltag_pose_logger",
        name="apriltag_pose_logger",
    )

    return LaunchDescription([
        visual_slam_node,
        apriltag_node,
        apriltag_pose_logger_node,
    ])

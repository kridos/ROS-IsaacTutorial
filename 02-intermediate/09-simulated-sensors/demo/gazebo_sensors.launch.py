"""Starts Gazebo with sensored_diffdrive.urdf.xacro, extending Chapter 7's
gazebo_sim.launch.py with three more bridge topics: camera, lidar, IMU.

Run: ros2 launch gazebo_sensors.launch.py
"""

import os

from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch.substitutions import Command
from launch_ros.actions import Node


def generate_launch_description():
    xacro_path = os.path.join(os.path.dirname(__file__), "sensored_diffdrive.urdf.xacro")

    # Reuse Chapter 7's empty_world.sdf rather than duplicating it — this
    # chapter only adds sensors to the robot, not the world.
    world_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "..",
        "01-beginner", "07-gazebo-basics", "demo", "empty_world.sdf",
    )

    gazebo_process = ExecuteProcess(
        cmd=["gz", "sim", "-r", world_path],
        output="screen",
    )

    robot_description = {"robot_description": Command(["xacro ", xacro_path])}
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        parameters=[robot_description],
    )

    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=["-topic", "robot_description", "-name", "sensored_diffdrive", "-z", "0.1"],
        output="screen",
    )

    # Same /cmd_vel and /odom bridge lines as Chapter 7, plus one line
    # per new sensor topic. Sensor topics bridge Gazebo -> ROS2 only
    # ("[" direction, see DEEP_DIVE.md) since nothing publishes simulated
    # sensor data from the ROS2 side.
    bridge_node = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist",
            "/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry",
            "/camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image",
            "/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan",
            "/imu@sensor_msgs/msg/Imu[gz.msgs.IMU",
        ],
        output="screen",
    )

    return LaunchDescription([
        gazebo_process,
        robot_state_publisher_node,
        spawn_robot,
        bridge_node,
    ])

"""Starts Gazebo with empty_world.sdf, publishes the robot description,
spawns simple_diffdrive into the running world, and bridges /cmd_vel and
/odom between Gazebo and ROS2.

Run: ros2 launch gazebo_sim.launch.py
"""

import os

from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch.substitutions import Command
from launch_ros.actions import Node


def generate_launch_description():
    xacro_path = os.path.join(os.path.dirname(__file__), "simple_diffdrive.urdf.xacro")
    world_path = os.path.join(os.path.dirname(__file__), "empty_world.sdf")

    # Start Gazebo itself as a plain subprocess (`gz sim`) — there's no
    # launch_ros wrapper for the Gazebo server the way there is for ROS2
    # nodes, since Gazebo isn't a ROS2 node. `-r` starts the simulation
    # running immediately instead of paused.
    gazebo_process = ExecuteProcess(
        cmd=["gz", "sim", "-r", world_path],
        output="screen",
    )

    # robot_state_publisher, same role as Chapter 5: expands the xacro
    # and publishes it on /robot_description, which `ros_gz_sim create`
    # (below) reads to know what to spawn.
    robot_description = {"robot_description": Command(["xacro ", xacro_path])}
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        parameters=[robot_description],
    )

    # ros_gz_sim's `create` executable spawns a model, read from the
    # /robot_description topic, into the already-running Gazebo world at
    # the given pose. This is the ROS2-side equivalent of dragging a
    # model into the Gazebo GUI by hand.
    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-topic", "robot_description",
            "-name", "simple_diffdrive",
            "-z", "0.1",  # spawn slightly above the ground to avoid initial collision penetration
        ],
        output="screen",
    )

    # The bridge: explicitly lists which topics cross between Gazebo's
    # transport and ROS2's, and in which direction (see DEEP_DIVE.md).
    # Format per argument: "<ros_topic>@<ros_type>[bridge_direction]<gz_type>"
    # where the bridge direction is @ (both ways), [ (Gazebo -> ROS2 only),
    # or ] (ROS2 -> Gazebo only).
    bridge_node = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist",
            "/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry",
        ],
        output="screen",
    )

    return LaunchDescription([
        gazebo_process,
        robot_state_publisher_node,
        spawn_robot,
        bridge_node,
    ])

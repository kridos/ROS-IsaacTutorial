"""Starts Gazebo with the Chapter 9 sensored robot, the Nav2 stack
(map_server, AMCL, planner, controller, bt_navigator, lifecycle manager)
using nav2_params.yaml, and RViz2 with Nav2's default navigation display.

Prerequisite: run generate_empty_map.py once first to create
empty_map.pgm/.yaml in this directory.

Run: ros2 launch nav2_sim.launch.py
"""

import os

from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    demo_dir = os.path.dirname(__file__)
    xacro_path = os.path.join(
        demo_dir, "..", "..", "09-simulated-sensors", "demo", "sensored_diffdrive.urdf.xacro"
    )
    world_path = os.path.join(
        demo_dir, "..", "..", "..", "01-beginner", "07-gazebo-basics", "demo", "empty_world.sdf"
    )
    params_path = os.path.join(demo_dir, "nav2_params.yaml")

    gazebo_process = ExecuteProcess(cmd=["gz", "sim", "-r", world_path], output="screen")

    robot_description = {"robot_description": Command(["xacro ", xacro_path])}
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        parameters=[robot_description, {"use_sim_time": True}],
    )

    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=["-topic", "robot_description", "-name", "sensored_diffdrive", "-z", "0.1"],
        output="screen",
    )

    # Same bridge topics as Chapter 9, minus camera (not needed for
    # navigation, kept out to reduce noise for this chapter's demo).
    bridge_node = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist",
            "/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry",
            "/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan",
        ],
        output="screen",
    )

    # Nav2's own bringup package provides a launch file that starts every
    # Nav2 node (map_server, amcl, controller_server, planner_server,
    # bt_navigator, and both lifecycle managers) wired together — we
    # include it rather than hand-listing each Node(...) ourselves, which
    # is both less error-prone and matches how Nav2 is used in practice.
    nav2_bringup_dir = get_package_share_directory("nav2_bringup")
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_dir, "launch", "bringup_launch.py")
        ),
        launch_arguments={
            "map": os.path.join(demo_dir, "empty_map.yaml"),
            "params_file": params_path,
            "use_sim_time": "true",
        }.items(),
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=["-d", os.path.join(nav2_bringup_dir, "rviz", "nav2_default_view.rviz")],
        parameters=[{"use_sim_time": True}],
    )

    return LaunchDescription([
        gazebo_process,
        robot_state_publisher_node,
        spawn_robot,
        bridge_node,
        nav2_launch,
        rviz_node,
    ])

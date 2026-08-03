"""Extends Chapter 11's nav2_sim.launch.py, pointing bt_navigator at this
chapter's custom_bt.xml instead of Nav2's stock default tree, via a
params override merged on top of Chapter 11's nav2_params.yaml.

Prerequisite: run Chapter 11's generate_empty_map.py once first (this
chapter reuses that map rather than duplicating map generation).

Run: ros2 launch nav2_custom_bt.launch.py
"""

import os
import tempfile

import yaml
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    demo_dir = os.path.dirname(__file__)
    ch11_dir = os.path.join(demo_dir, "..", "..", "..", "02-intermediate", "11-nav2-basics", "demo")
    ch9_dir = os.path.join(demo_dir, "..", "..", "..", "02-intermediate", "09-simulated-sensors", "demo")

    xacro_path = os.path.join(ch9_dir, "sensored_diffdrive.urdf.xacro")
    world_path = os.path.join(
        demo_dir, "..", "..", "..", "01-beginner", "07-gazebo-basics", "demo", "empty_world.sdf"
    )
    base_params_path = os.path.join(ch11_dir, "nav2_params.yaml")
    map_path = os.path.join(ch11_dir, "empty_map.yaml")
    custom_bt_path = os.path.join(demo_dir, "custom_bt.xml")

    # Merge Chapter 11's base params with this chapter's one override
    # (default_nav_to_pose_bt_xml) rather than hand-duplicating the whole
    # file — keeps this chapter's actual change (the custom tree) obvious
    # and avoids the two files drifting out of sync over time.
    with open(base_params_path, "r") as f:
        params = yaml.safe_load(f)
    params.setdefault("bt_navigator", {}).setdefault("ros__parameters", {})
    params["bt_navigator"]["ros__parameters"]["default_nav_to_pose_bt_xml"] = custom_bt_path

    merged_params_file = tempfile.NamedTemporaryFile(
        mode="w", suffix="_nav2_custom_bt_params.yaml", delete=False
    )
    yaml.safe_dump(params, merged_params_file)
    merged_params_file.close()

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

    nav2_bringup_dir = get_package_share_directory("nav2_bringup")
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_dir, "launch", "bringup_launch.py")
        ),
        launch_arguments={
            "map": map_path,
            "params_file": merged_params_file.name,
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

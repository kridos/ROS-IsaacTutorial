"""Starts Gazebo with mobile_manipulator.urdf.xacro, spawns the combined
robot, bridges cmd_vel/odom/scan, and brings up BOTH Nav2 (Chapter 11
pattern) and MoveIt2 (Chapter 12 pattern) against it simultaneously —
see DEEP_DIVE.md for why this is a genuinely different problem than
running either alone.

Prerequisite: run Chapter 11's generate_empty_map.py once first (this
capstone reuses that map).

Run: ros2 launch capstone_sim.launch.py
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
    xacro_path = os.path.join(demo_dir, "mobile_manipulator.urdf.xacro")
    world_path = os.path.join(
        demo_dir, "..", "..", "..", "01-beginner", "07-gazebo-basics", "demo", "empty_world.sdf"
    )
    nav2_params_path = os.path.join(
        demo_dir, "..", "..", "..", "02-intermediate", "11-nav2-basics", "demo", "nav2_params.yaml"
    )
    map_path = os.path.join(
        demo_dir, "..", "..", "..", "02-intermediate", "11-nav2-basics", "demo", "empty_map.yaml"
    )
    srdf_path = os.path.join(
        demo_dir, "..", "..", "..", "02-intermediate", "12-moveit2-basics", "demo", "arm_with_gripper.srdf"
    )

    gazebo_process = ExecuteProcess(cmd=["gz", "sim", "-r", world_path], output="screen")

    robot_description = {"robot_description": Command(["xacro ", xacro_path]), "use_sim_time": True}
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        parameters=[robot_description],
    )

    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=["-topic", "robot_description", "-name", "mobile_manipulator", "-z", "0.1"],
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

    # Nav2, same bringup pattern as Chapter 11 — reuses that chapter's
    # map and params file rather than duplicating them.
    nav2_bringup_dir = get_package_share_directory("nav2_bringup")
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_dir, "launch", "bringup_launch.py")
        ),
        launch_arguments={
            "map": map_path,
            "params_file": nav2_params_path,
            "use_sim_time": "true",
        }.items(),
    )

    # MoveIt2, same move_group pattern as Chapter 12 — using this
    # capstone's own robot_description (the combined mobile+arm URDF)
    # and Chapter 12's SRDF (the "arm" planning group definition still
    # applies unchanged, since joint1-3 are named identically here).
    with open(srdf_path, "r") as f:
        robot_description_semantic = {"robot_description_semantic": f.read()}

    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        name="move_group",
        output="screen",
        parameters=[
            robot_description,
            robot_description_semantic,
            {
                "robot_description_kinematics": {
                    "arm": {
                        "kinematics_solver": "kdl_kinematics_plugin/KDLKinematicsPlugin",
                        "kinematics_solver_search_resolution": 0.005,
                        "kinematics_solver_timeout": 0.05,
                    }
                },
                "planning_pipelines": ["ompl"],
                "ompl": {
                    "planning_plugin": "ompl_interface/OMPLPlanner",
                    "arm": {"planner_configs": ["RRTConnectkConfigDefault"]},
                    "RRTConnectkConfigDefault": {"type": "geometric::RRTConnect", "range": 0.0},
                },
            },
        ],
    )

    return LaunchDescription([
        gazebo_process,
        robot_state_publisher_node,
        spawn_robot,
        bridge_node,
        nav2_launch,
        move_group_node,
    ])

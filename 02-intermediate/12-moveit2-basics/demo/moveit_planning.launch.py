"""Starts robot_state_publisher (for arm_with_gripper.urdf.xacro),
move_group (MoveIt2's planning coordinator), and RViz2 with the
MotionPlanning display, so plans requested by move_to_pose.py are both
executed and visible.

This is a minimal, hand-assembled MoveIt2 launch file for learning
purposes — a real project would normally generate most of this
boilerplate (SRDF, kinematics config, OMPL planning config) via the
MoveIt Setup Assistant rather than writing it by hand, but seeing the
pieces explicitly here is the point of this chapter.

Run: ros2 launch moveit_planning.launch.py
"""

import os

from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node


def generate_launch_description():
    demo_dir = os.path.dirname(__file__)
    xacro_path = os.path.join(demo_dir, "arm_with_gripper.urdf.xacro")
    srdf_path = os.path.join(demo_dir, "arm_with_gripper.srdf")

    robot_description = {"robot_description": Command(["xacro ", xacro_path])}
    with open(srdf_path, "r") as f:
        robot_description_semantic = {"robot_description_semantic": f.read()}

    # Minimal kinematics config: KDL's numerical IK solver, a reasonable
    # default choice for a simple serial arm like this chapter's (see
    # DEEP_DIVE.md's forward/inverse kinematics section).
    kinematics_config = {
        "robot_description_kinematics": {
            "arm": {
                "kinematics_solver": "kdl_kinematics_plugin/KDLKinematicsPlugin",
                "kinematics_solver_search_resolution": 0.005,
                "kinematics_solver_timeout": 0.05,
            }
        }
    }

    # Minimal OMPL planning config: one planner (RRTConnect, a common
    # general-purpose default) for the "arm" group.
    ompl_config = {
        "planning_pipelines": ["ompl"],
        "ompl": {
            "planning_plugin": "ompl_interface/OMPLPlanner",
            "arm": {"planner_configs": ["RRTConnectkConfigDefault"]},
            "RRTConnectkConfigDefault": {
                "type": "geometric::RRTConnect",
                "range": 0.0,
            },
        },
    }

    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        name="move_group",
        output="screen",
        parameters=[
            robot_description,
            robot_description_semantic,
            kinematics_config,
            ompl_config,
        ],
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        parameters=[robot_description],
    )

    # A joint_state_publisher (non-GUI — move_group drives joint states
    # via planning/execution, unlike Chapter 5's manual sliders) keeps
    # TF valid for any joints move_group isn't actively reporting.
    joint_state_publisher_node = Node(
        package="joint_state_publisher",
        executable="joint_state_publisher",
        name="joint_state_publisher",
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        parameters=[robot_description, robot_description_semantic],
    )

    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_node,
        move_group_node,
        rviz_node,
    ])

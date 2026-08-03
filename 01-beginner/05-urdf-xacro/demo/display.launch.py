"""Launches robot_state_publisher (reads the Xacro, publishes TF),
joint_state_publisher_gui (slider controls for each joint), and rviz2
(pre-configured to show the robot model and TF frames).

Run: ros2 launch display.launch.py
"""

import os

from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node


def generate_launch_description():
    xacro_path = os.path.join(os.path.dirname(__file__), "simple_arm.urdf.xacro")
    rviz_config_path = os.path.join(os.path.dirname(__file__), "rviz_config.rviz")

    # xacro needs to be expanded into plain URDF XML before
    # robot_state_publisher can use it. `xacro` the CLI tool does this;
    # here we call it as a subprocess-in-a-string via the shell command
    # substitution `$(xacro ...)`, which robot_state_publisher's
    # `robot_description` parameter accepts as a plain string of URDF XML.
    #
    # Command() runs a shell command at launch time and substitutes its
    # stdout as the parameter value — this is the standard ROS2 launch
    # pattern for "expand this xacro file right before starting the node."
    robot_description = {
        "robot_description": Command(["xacro ", xacro_path])
    }

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        parameters=[robot_description],
    )

    # joint_state_publisher_gui: opens a small window with one slider per
    # revolute/prismatic joint found in the URDF, and publishes
    # sensor_msgs/msg/JointState with whatever the sliders are currently
    # set to. robot_state_publisher (above) turns that into TF.
    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher_gui",
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=["-d", rviz_config_path],
    )

    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node,
    ])

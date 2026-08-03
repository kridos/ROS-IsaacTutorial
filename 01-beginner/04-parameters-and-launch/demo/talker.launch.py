"""Launches configurable_talker.py with talker_config.yaml, and lets the
publish rate be overridden from the command line, e.g.:

    ros2 launch talker.launch.py rate:=5.0
"""

import os
import sys

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    # Resolve paths relative to this launch file, not the current working
    # directory — otherwise `ros2 launch` only works when run from this
    # exact folder, a common source of "file not found" confusion.
    script_path = os.path.join(os.path.dirname(__file__), "configurable_talker.py")
    config_path = os.path.join(os.path.dirname(__file__), "talker_config.yaml")

    # A launch-file-level argument, separate from the node's ROS2
    # parameters — this is what makes `rate:=5.0` on the command line
    # work. Default matches the YAML file's value so omitting it changes
    # nothing.
    rate_arg = DeclareLaunchArgument(
        "rate",
        default_value="2.0",
        description="Publish rate in Hz, overrides talker_config.yaml",
    )

    # This chapter's demo is a standalone script, not a colcon package
    # (see demo/README.md — kept copy-paste runnable like Chapters 2-3),
    # so we use ExecuteProcess to run it directly with python3 rather
    # than launch_ros's Node(...) action, which requires an installed
    # package + executable. From Chapter 5 onward, demos become proper
    # colcon packages and use Node(...) instead — this is the one chapter
    # where the two approaches differ.
    #
    # --ros-args --params-file <yaml> loads the YAML file's parameters;
    # -p publish_rate_hz:=<value> after it overrides just that one key.
    # A list element mixing a literal string and a LaunchConfiguration
    # (like the one below) is concatenated by `launch` into the final
    # command-line argument at run time.
    talker_process = ExecuteProcess(
        cmd=[
            sys.executable,
            script_path,
            "--ros-args",
            "--params-file", config_path,
            "-p", ["publish_rate_hz:=", LaunchConfiguration("rate")],
        ],
        output="screen",
    )

    return LaunchDescription([rate_arg, talker_process])

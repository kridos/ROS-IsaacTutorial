"""Spawns two instances of the Chapter 7 diff-drive robot into the same
Gazebo world, each under its own namespace (robot1, robot2) with
separately-namespaced bridges and TF frame prefixes — see DEEP_DIVE.md
for why both matter.

Run: ros2 launch multi_robot_sim.launch.py
"""

import os

from launch import LaunchDescription
from launch.actions import ExecuteProcess, GroupAction
from launch.substitutions import Command
from launch_ros.actions import Node, PushRosNamespace


def make_robot_group(namespace: str, spawn_x: float, xacro_path: str):
    """Builds one robot's full stack (state publisher, spawn, bridge)
    under the given namespace — called twice below with different
    namespaces and spawn positions so the two robots don't overlap."""
    robot_description = {
        "robot_description": Command(["xacro ", xacro_path]),
        # frame_prefix namespaces every TF frame this robot_state_publisher
        # produces (base_link -> robot1/base_link, etc.) — the TF-specific
        # step DEEP_DIVE.md warns is easy to forget even after namespacing
        # topics correctly.
        "frame_prefix": f"{namespace}/",
    }

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        parameters=[robot_description],
    )

    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-topic", "robot_description",
            "-name", f"{namespace}_diffdrive",
            "-x", str(spawn_x), "-z", "0.1",
        ],
        output="screen",
    )

    # Two collisions to avoid here, not one:
    #   - Gazebo side: gz-sim automatically scopes a plugin's non-absolute
    #     <topic> name (simple_diffdrive.urdf.xacro's plugin declares
    #     plain "cmd_vel"/"odom") under that model's own entity path, so
    #     the ACTUAL gz topic each spawned robot's plugin uses is
    #     /model/<entity_name>/cmd_vel — NOT a bare "cmd_vel" both robots
    #     would otherwise collide on inside Gazebo's own transport.
    #   - ROS2 side: ros_gz_bridge's <topic>@<type>[<type> syntax bridges
    #     a topic to itself under the same name on both sides, so we
    #     bridge the scoped gz name as-is, then use a ROS2 remapping
    #     (below) to rename it to the plain "cmd_vel"/"odom" this node
    #     publishes/subscribes under — which PushRosNamespace then
    #     namespaces into /robot1/cmd_vel, /robot2/cmd_vel, etc., the
    #     leading-slash-vs-relative distinction from Chapter 2, now
    #     load-bearing (see DEEP_DIVE.md).
    gz_model_name = f"{namespace}_diffdrive"
    gz_cmd_vel_topic = f"/model/{gz_model_name}/cmd_vel"
    gz_odom_topic = f"/model/{gz_model_name}/odom"
    bridge_node = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            f"{gz_cmd_vel_topic}@geometry_msgs/msg/Twist]gz.msgs.Twist",
            f"{gz_odom_topic}@nav_msgs/msg/Odometry[gz.msgs.Odometry",
        ],
        remappings=[
            (gz_cmd_vel_topic, "cmd_vel"),
            (gz_odom_topic, "odom"),
        ],
        output="screen",
    )

    return GroupAction([
        PushRosNamespace(namespace),
        robot_state_publisher_node,
        spawn_robot,
        bridge_node,
    ])


def generate_launch_description():
    demo_dir = os.path.dirname(__file__)
    xacro_path = os.path.join(
        demo_dir, "..", "..", "..", "01-beginner", "07-gazebo-basics",
        "demo", "simple_diffdrive.urdf.xacro",
    )
    world_path = os.path.join(
        demo_dir, "..", "..", "..", "01-beginner", "07-gazebo-basics",
        "demo", "empty_world.sdf",
    )

    gazebo_process = ExecuteProcess(cmd=["gz", "sim", "-r", world_path], output="screen")

    # Spawned 1m apart on the X axis so the two robots don't start out
    # overlapping/colliding with each other.
    robot1_group = make_robot_group("robot1", spawn_x=-0.5, xacro_path=xacro_path)
    robot2_group = make_robot_group("robot2", spawn_x=0.5, xacro_path=xacro_path)

    return LaunchDescription([gazebo_process, robot1_group, robot2_group])

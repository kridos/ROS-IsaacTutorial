#!/usr/bin/env python3
"""Extends Chapter 13's import_and_spawn.py: imports the diff-drive
robot, then builds an OmniGraph wiring /cmd_vel to the wheel joints and
the robot's odometry to /odom, then runs with the GUI open (not
headless, unlike Chapter 13) so you can watch it respond to
drive_and_log_odom.py commands live.

Run with Isaac Sim's own Python environment — see demo/README.md.
"""

import os

from isaacsim import SimulationApp

simulation_app = SimulationApp({"headless": False})

import omni.graph.core as og
from isaacsim.core.api import World
from isaacsim.core.utils.extensions import enable_extension
from isaacsim.core.utils.stage import add_reference_to_stage

enable_extension("isaacsim.asset.importer.urdf")
enable_extension("isaacsim.ros2.bridge")  # new in this chapter — see DEEP_DIVE.md
from isaacsim.asset.importer.urdf import _urdf  # noqa: E402


def urdf_to_usd(urdf_path: str, usd_output_path: str) -> str:
    """Same conversion helper as Chapter 13's import_and_spawn.py."""
    urdf_interface = _urdf.acquire_urdf_interface()
    import_config = _urdf.ImportConfig()
    import_config.merge_fixed_joints = False
    import_config.convex_decomp = False
    import_config.fix_base = False
    import_config.self_collision = False
    import_config.distance_scale = 1.0

    result, robot_model = urdf_interface.parse_urdf(urdf_path, import_config)
    urdf_interface.import_robot(
        os.path.dirname(urdf_path), os.path.basename(urdf_path),
        robot_model, import_config, usd_output_path,
    )
    return usd_output_path


def build_ros2_bridge_graph(robot_prim_path: str):
    """Builds the OmniGraph described in DEEP_DIVE.md: a tick source, a
    /cmd_vel subscriber feeding an articulation controller, and an
    odometry publisher reading the robot's current state."""
    graph_path = "/World/ROS2BridgeGraph"

    # og.Controller.edit both creates the graph and adds/connects nodes
    # in one call — the programmatic equivalent of wiring nodes together
    # by hand in the Action Graph GUI (see DEEP_DIVE.md).
    og.Controller.edit(
        {"graph_path": graph_path, "evaluator_name": "execution"},
        {
            og.Controller.Keys.CREATE_NODES: [
                ("OnTick", "omni.graph.action.OnPlaybackTick"),
                ("SubscribeTwist", "isaacsim.ros2.bridge.ROS2SubscribeTwist"),
                ("ArticulationController", "isaacsim.core.nodes.IsaacArticulationController"),
                ("PublishOdometry", "isaacsim.ros2.bridge.ROS2PublishOdometry"),
            ],
            og.Controller.Keys.CONNECT: [
                ("OnTick.outputs:tick", "SubscribeTwist.inputs:execIn"),
                ("OnTick.outputs:tick", "ArticulationController.inputs:execIn"),
                ("OnTick.outputs:tick", "PublishOdometry.inputs:execIn"),
                ("SubscribeTwist.outputs:linearVelocity", "ArticulationController.inputs:velocityCommand"),
                ("SubscribeTwist.outputs:angularVelocity", "ArticulationController.inputs:angularVelocityCommand"),
            ],
            og.Controller.Keys.SET_VALUES: [
                ("SubscribeTwist.inputs:topicName", "cmd_vel"),
                ("ArticulationController.inputs:robotPath", robot_prim_path),
                ("PublishOdometry.inputs:topicName", "odom"),
                ("PublishOdometry.inputs:chassisPrim", robot_prim_path),
            ],
        },
    )
    print(f"Built ROS2 bridge OmniGraph at {graph_path}")


def main():
    demo_dir = os.path.dirname(os.path.abspath(__file__))
    xacro_path = os.path.join(
        demo_dir, "..", "..", "..", "01-beginner", "07-gazebo-basics",
        "demo", "simple_diffdrive.urdf.xacro",
    )
    plain_urdf_path = os.path.join(demo_dir, "simple_diffdrive.urdf")
    os.system(f"xacro {xacro_path} -o {plain_urdf_path}")

    usd_output_path = os.path.join(demo_dir, "simple_diffdrive.usd")
    urdf_to_usd(plain_urdf_path, usd_output_path)

    world = World(stage_units_in_meters=1.0)
    world.scene.add_default_ground_plane()

    robot_prim_path = "/World/simple_diffdrive"
    add_reference_to_stage(usd_path=usd_output_path, prim_path=robot_prim_path)

    build_ros2_bridge_graph(robot_prim_path)

    world.reset()

    print("Simulation running — drive it with drive_and_log_odom.py in another terminal.")
    print("Close this window (or Ctrl+C in this terminal) to stop.")
    while simulation_app.is_running():
        world.step(render=True)

    simulation_app.close()


if __name__ == "__main__":
    main()

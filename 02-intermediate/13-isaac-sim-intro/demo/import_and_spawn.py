#!/usr/bin/env python3
"""Starts Isaac Sim headlessly, imports the Chapter 7 diff-drive robot's
URDF, spawns it into an empty stage, steps physics for a few seconds, and
prints the robot's world pose each step — confirming the import and
physics both work without needing the GUI.

Targets Isaac Sim 4.x. Must be run with Isaac Sim's own bundled Python
environment (see demo/README.md for the exact invocation) — this is NOT
a plain `python3 import_and_spawn.py` script; Isaac Sim's Python modules
only exist inside its own environment.
"""

import os

# SimulationApp must be constructed BEFORE importing most other Isaac Sim
# modules — it's what actually boots the underlying Omniverse Kit
# application that everything else (World, extensions, USD APIs) depends
# on. headless=True skips opening any GUI window, appropriate for a
# script meant to run in a terminal / CI-style environment.
from isaacsim import SimulationApp

simulation_app = SimulationApp({"headless": True})

# These imports only work AFTER SimulationApp() has run — they reach
# into the Kit application it just started.
import omni.usd
from isaacsim.core.api import World
from isaacsim.core.utils.extensions import enable_extension
from isaacsim.core.utils.stage import add_reference_to_stage

# The URDF importer is an extension, not always loaded by default (see
# DEEP_DIVE.md's common pitfall) — must be explicitly enabled before its
# API is usable.
enable_extension("isaacsim.asset.importer.urdf")
from isaacsim.asset.importer.urdf import _urdf  # noqa: E402  (import must follow enable_extension)


def urdf_to_usd(urdf_path: str, usd_output_path: str) -> str:
    """Runs the URDF importer, converting urdf_path into a USD file on
    disk at usd_output_path, and returns the path actually written."""
    urdf_interface = _urdf.acquire_urdf_interface()

    import_config = _urdf.ImportConfig()
    import_config.merge_fixed_joints = False
    import_config.convex_decomp = False
    import_config.fix_base = False  # let the robot fall/settle under gravity, don't pin it in place
    import_config.self_collision = False
    import_config.distance_scale = 1.0  # URDF is already in meters — no rescaling needed

    result, robot_model = urdf_interface.parse_urdf(urdf_path, import_config)
    urdf_interface.import_robot(
        os.path.dirname(urdf_path), os.path.basename(urdf_path),
        robot_model, import_config, usd_output_path,
    )
    return usd_output_path


def main():
    demo_dir = os.path.dirname(os.path.abspath(__file__))

    # Reuse Chapter 7's diff-drive URDF rather than duplicating it — this
    # chapter is about the IMPORT process, not a new robot design.
    xacro_path = os.path.join(
        demo_dir, "..", "..", "..", "01-beginner", "07-gazebo-basics",
        "demo", "simple_diffdrive.urdf.xacro",
    )
    # Isaac Sim's URDF importer expects plain URDF, not Xacro — the
    # `xacro` CLI (same tool from Chapter 5) expands it first.
    plain_urdf_path = os.path.join(demo_dir, "simple_diffdrive.urdf")
    os.system(f"xacro {xacro_path} -o {plain_urdf_path}")

    usd_output_path = os.path.join(demo_dir, "simple_diffdrive.usd")
    urdf_to_usd(plain_urdf_path, usd_output_path)
    print(f"Imported URDF -> USD at: {usd_output_path}")

    # World is Isaac Sim's core API's equivalent of "the stage plus a
    # physics context" — creating one sets up a ground plane and default
    # physics scene automatically (scene_prim_root default).
    world = World(stage_units_in_meters=1.0)
    world.scene.add_default_ground_plane()

    # add_reference_to_stage brings the imported USD robot onto the
    # current stage as a prim, at the given path — analogous to
    # Chapter 7's `ros_gz_sim create` spawning a robot into a running
    # Gazebo world, but here operating directly on the USD stage.
    robot_prim_path = "/World/simple_diffdrive"
    add_reference_to_stage(usd_path=usd_output_path, prim_path=robot_prim_path)

    world.reset()  # initializes physics for everything just added to the stage

    stage = omni.usd.get_context().get_stage()
    robot_prim = stage.GetPrimAtPath(robot_prim_path)

    # Step physics for 3 seconds (at the default 60 Hz physics rate) and
    # print the robot's world-space translation each step — confirms
    # both that the import succeeded (the prim exists and has a
    # transform) and that physics is actually being applied to it (the
    # Z position should settle near the ground plane height under
    # gravity, not stay frozen at the spawn height).
    for step in range(180):
        world.step(render=False)
        if step % 30 == 0:
            translation = omni.usd.get_world_transform_matrix(robot_prim).ExtractTranslation()
            print(f"step={step} position=({translation[0]:.3f}, {translation[1]:.3f}, {translation[2]:.3f})")

    print("Done.")
    simulation_app.close()


if __name__ == "__main__":
    main()

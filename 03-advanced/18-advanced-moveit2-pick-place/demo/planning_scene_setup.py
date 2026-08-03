#!/usr/bin/env python3
"""Adds a table and a target block as collision objects to the Chapter
12 arm's planning scene, via the Planning Scene Interface — run once
before pick_and_place.py so the scene has real obstacles in it instead
of Chapter 12's empty-scene assumption (see DEEP_DIVE.md)."""

import rclpy
from moveit.core.planning_scene import PlanningSceneMonitor
from moveit_msgs.msg import CollisionObject
from shape_msgs.msg import SolidPrimitive
from geometry_msgs.msg import Pose


def make_box_collision_object(object_id: str, size, position, frame_id="base_link") -> CollisionObject:
    obj = CollisionObject()
    obj.id = object_id
    obj.header.frame_id = frame_id

    primitive = SolidPrimitive()
    primitive.type = SolidPrimitive.BOX
    primitive.dimensions = list(size)

    pose = Pose()
    pose.position.x, pose.position.y, pose.position.z = position
    pose.orientation.w = 1.0

    obj.primitives.append(primitive)
    obj.primitive_poses.append(pose)
    obj.operation = CollisionObject.ADD
    return obj


def main():
    rclpy.init()
    node = rclpy.create_node("planning_scene_setup")

    # PlanningSceneMonitor connects to the already-running move_group
    # node's planning scene (started by Chapter 12's
    # moveit_planning.launch.py) rather than maintaining a separate scene
    # of its own — collision objects added here are visible to
    # pick_and_place.py's planning calls because both talk to the same
    # underlying scene.
    psm = PlanningSceneMonitor(node, "robot_description")
    psm.start_scene_monitor()
    psm.start_state_monitor()

    # Table: a wide, thin box below and slightly in front of the arm's
    # base — sized/positioned so the arm's reachable workspace (per
    # Chapter 12's link lengths) can plausibly reach objects on top of it.
    table = make_box_collision_object(
        "table", size=(0.4, 0.4, 0.05), position=(0.35, 0.0, 0.2)
    )

    # Target block: small box resting on top of the table.
    block = make_box_collision_object(
        "target_block", size=(0.03, 0.03, 0.03), position=(0.35, 0.0, 0.24)
    )

    with psm.read_write() as scene:
        scene.apply_collision_object(table)
        scene.apply_collision_object(block)
        scene.current_state.update()

    node.get_logger().info("Added 'table' and 'target_block' to the planning scene")

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

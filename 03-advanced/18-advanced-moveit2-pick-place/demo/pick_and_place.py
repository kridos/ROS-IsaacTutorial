#!/usr/bin/env python3
"""Runs the full pick-and-place sequence from DEEP_DIVE.md against the
target_block added by planning_scene_setup.py: pre-grasp -> Cartesian
approach -> grasp -> attach -> Cartesian retreat -> pre-place ->
Cartesian approach -> release -> detach -> Cartesian retreat.

Run planning_scene_setup.py first — this script assumes 'table' and
'target_block' already exist in the planning scene.
"""

import rclpy
from moveit.planning import MoveItPy
from geometry_msgs.msg import PoseStamped, Pose


# Positions matching planning_scene_setup.py's table/block placement.
GRASP_POSITION = (0.35, 0.0, 0.28)     # just above target_block's top face
PLACE_POSITION = (0.20, 0.25, 0.28)    # a different spot on the same table
RETREAT_HEIGHT = 0.15                   # how far straight up to retreat after grasp/place


def pose_at(position) -> Pose:
    pose = Pose()
    pose.position.x, pose.position.y, pose.position.z = position
    pose.orientation.w = 1.0
    return pose


def plan_and_execute(arm, pose_stamped: PoseStamped, stage_name: str) -> bool:
    """Chapter 12's free-form plan-and-execute pattern, reused for the
    pre-grasp and pre-place moves (which don't need a straight line)."""
    arm.set_start_state_to_current_state()
    arm.set_goal_state(pose_stamped_msg=pose_stamped, pose_link="gripper")
    plan_result = arm.plan()
    if not plan_result:
        print(f"[{stage_name}] Planning FAILED")
        return False
    print(f"[{stage_name}] Planning succeeded, executing...")
    return True


def cartesian_move(arm, waypoints, stage_name: str) -> bool:
    """Straight-line motion through the given waypoints, per DEEP_DIVE.md
    — used for the grasp approach and both retreats, where an arbitrary
    curved path from OMPL would be the wrong choice."""
    trajectory, fraction = arm.get_active_group().compute_cartesian_path(
        waypoints=waypoints, eef_step=0.01, avoid_collisions=True
    )
    if fraction < 0.95:
        # Below ~95% means compute_cartesian_path couldn't complete the
        # requested straight-line motion (joint limit or collision cut it
        # short) — treated as failure per DEEP_DIVE.md's warning not to
        # trust a low fraction just because the call itself didn't error.
        print(f"[{stage_name}] Cartesian path only {fraction * 100:.0f}% complete, aborting")
        return False
    print(f"[{stage_name}] Cartesian path {fraction * 100:.0f}% complete, executing...")
    arm.execute(trajectory)
    return True


def main():
    rclpy.init()
    arm_robot = MoveItPy(node_name="pick_and_place_client")
    arm = arm_robot.get_planning_component("arm")

    # --- Pick ---

    pre_grasp = PoseStamped()
    pre_grasp.header.frame_id = "base_link"
    pre_grasp.pose = pose_at((GRASP_POSITION[0], GRASP_POSITION[1], GRASP_POSITION[2] + RETREAT_HEIGHT))
    if not plan_and_execute(arm, pre_grasp, "pre-grasp"):
        return

    grasp_pose = pose_at(GRASP_POSITION)
    if not cartesian_move(arm, [grasp_pose], "grasp approach"):
        return

    # Gripper actuation is represented logically here, not as a real
    # joint command — Chapter 12's arm uses a simplified fixed gripper
    # link (see that chapter's URDF), so "closing the gripper" in this
    # demo means proceeding to attach the object, not commanding real
    # finger joints.
    print("[grasp] Closing gripper (logical step — see comment above)")

    # Attach BEFORE planning the retreat — see DEEP_DIVE.md's common
    # pitfall on why this ordering matters.
    arm_robot.get_planning_scene_monitor().read_write().apply_attached_collision_object(
        object_id="target_block", link_name="gripper"
    )
    print("[grasp] Attached target_block to gripper")

    retreat_pose = pose_at((GRASP_POSITION[0], GRASP_POSITION[1], GRASP_POSITION[2] + RETREAT_HEIGHT))
    if not cartesian_move(arm, [retreat_pose], "post-grasp retreat"):
        return

    # --- Place ---

    pre_place = PoseStamped()
    pre_place.header.frame_id = "base_link"
    pre_place.pose = pose_at((PLACE_POSITION[0], PLACE_POSITION[1], PLACE_POSITION[2] + RETREAT_HEIGHT))
    if not plan_and_execute(arm, pre_place, "pre-place"):
        return

    place_pose = pose_at(PLACE_POSITION)
    if not cartesian_move(arm, [place_pose], "place approach"):
        return

    print("[place] Opening gripper (logical step)")
    arm_robot.get_planning_scene_monitor().read_write().remove_attached_collision_object(
        object_id="target_block"
    )
    print("[place] Detached target_block from gripper")

    final_retreat = pose_at((PLACE_POSITION[0], PLACE_POSITION[1], PLACE_POSITION[2] + RETREAT_HEIGHT))
    cartesian_move(arm, [final_retreat], "post-place retreat")

    print("Pick-and-place sequence complete.")
    rclpy.shutdown()


if __name__ == "__main__":
    main()

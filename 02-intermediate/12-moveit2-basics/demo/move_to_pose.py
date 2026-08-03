#!/usr/bin/env python3
"""Requests a plan to a target end-effector pose for the "arm" planning
group and executes it, using MoveIt2's MoveGroupInterface — the same
"send a goal, track it to completion" shape as Chapter 3's actions and
Chapter 11's NavigateToPose, wrapped in a higher-level client here
instead of hand-written action-client boilerplate.

Usage: python3 move_to_pose.py [x] [y] [z]  (default: 0.3 0.0 0.5)
"""

import sys

import rclpy

# moveit_py is MoveIt2's current Python API (see DEEP_DIVE.md — this
# replaced the older moveit_commander package). Import path shown here
# matches recent MoveIt2 releases; check your installed version if this
# import fails, per the DEEP_DIVE.md note on API changes.
from moveit.planning import MoveItPy
from geometry_msgs.msg import PoseStamped


def build_target_pose(x: float, y: float, z: float) -> PoseStamped:
    pose = PoseStamped()
    pose.header.frame_id = "base_link"
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.position.z = z
    pose.pose.orientation.w = 1.0  # no rotation requested — position-only target
    return pose


def main():
    x = float(sys.argv[1]) if len(sys.argv) > 1 else 0.3
    y = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
    z = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5

    rclpy.init()

    # MoveItPy is the top-level entry point into the moveit_py API —
    # constructing it connects to the already-running move_group node
    # started by moveit_planning.launch.py rather than starting a new one.
    arm_robot = MoveItPy(node_name="move_to_pose_client")
    arm = arm_robot.get_planning_component("arm")

    target_pose = build_target_pose(x, y, z)
    print(f"Requesting plan to pose: x={x}, y={y}, z={z}")

    arm.set_start_state_to_current_state()
    arm.set_goal_state(pose_stamped_msg=target_pose, pose_link="gripper")

    plan_result = arm.plan()

    if plan_result:
        print("Planning succeeded, executing...")
        arm_robot.execute(plan_result.trajectory, controllers=[])
        print("Execution complete.")
    else:
        # See DEEP_DIVE.md's common pitfall: this doesn't distinguish
        # "unreachable," "in collision," and "planner ran out of time" —
        # use RViz2's MotionPlanning display to tell those apart.
        print("Planning FAILED — see DEEP_DIVE.md's common pitfall section.")

    rclpy.shutdown()


if __name__ == "__main__":
    main()
